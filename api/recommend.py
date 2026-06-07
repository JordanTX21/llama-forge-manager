"""
Smart Config Recommendation Engine.

Analyzes user hardware (VRAM, RAM, CPU) and model metadata to generate
optimal llama-server configuration parameters.

Strategy: Try Hugging Face API first for precise metadata, fall back to
filename-based heuristics if unavailable.
"""

import os
import re
import math
import httpx
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict

from api.hardware import get_nvidia_vram
import psutil

router = APIRouter()

# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class RecommendationRequest(BaseModel):
    model_path: str          # relative path inside models/ dir
    model_size_mb: float     # file size in MB
    filename: str            # e.g. "Qwen3-32B-Q4_K_M.gguf"


class RecommendedConfig(BaseModel):
    ngl: int = 999
    ctx_size: int = 8192
    threads: int = -1
    threads_batch: int = -1
    flash_attention: bool = True
    cache_type_k: str = "q8_0"
    cache_type_v: str = "q8_0"
    batch_size: int = 2048
    ubatch_size: int = 512
    thinking_mode: bool = False
    jinja: bool = True
    mlock: bool = False
    no_mmap: bool = False


class RecommendationResponse(BaseModel):
    config: RecommendedConfig
    confidence: str          # "high" | "medium" | "low"
    tier: str                # "OPTIMAL" | "GOOD" | "CONSTRAINED"
    explanation: Dict[str, str]
    hardware_summary: Dict[str, str]
    model_summary: Dict[str, str]


# ---------------------------------------------------------------------------
# Model metadata estimation from filename (Alternativa A)
# ---------------------------------------------------------------------------

# Common quantization patterns and their approximate bits-per-weight
QUANT_BPW: Dict[str, float] = {
    "F32":    32.0,
    "F16":    16.0,
    "BF16":   16.0,
    "Q8_0":   8.5,
    "Q8_1":   9.0,
    "Q6_K":   6.6,
    "Q5_K_M": 5.7,
    "Q5_K_S": 5.5,
    "Q5_K":   5.5,
    "Q5_0":   5.5,
    "Q5_1":   6.0,
    "Q4_K_M": 4.8,
    "Q4_K_S": 4.6,
    "Q4_K":   4.6,
    "Q4_0":   4.5,
    "Q4_1":   5.0,
    "Q3_K_M": 3.9,
    "Q3_K_S": 3.5,
    "Q3_K_L": 4.1,
    "Q3_K":   3.5,
    "Q2_K":   3.2,
    "Q2_K_S": 3.0,
    "IQ4_XS": 4.3,
    "IQ4_NL": 4.5,
    "IQ3_XXS": 3.1,
    "IQ3_XS": 3.3,
    "IQ3_S":  3.4,
    "IQ3_M":  3.5,
    "IQ2_XXS": 2.1,
    "IQ2_XS": 2.3,
    "IQ2_S":  2.5,
    "IQ2_M":  2.7,
    "IQ1_S":  1.6,
    "IQ1_M":  1.8,
}

# Approximate layer count by parameter size (billions)
PARAM_LAYERS: Dict[str, int] = {
    "0.5B": 24, "1B": 24, "1.5B": 28, "2B": 24, "3B": 28,
    "4B": 32, "7B": 32, "8B": 32, "9B": 32,
    "13B": 40, "14B": 40, "15B": 40,
    "20B": 44, "22B": 48, "27B": 48,
    "30B": 60, "32B": 64, "34B": 60,
    "35B": 64, "40B": 60,
    "65B": 80, "70B": 80, "72B": 80,
    "105B": 80, "110B": 80,
    "141B": 128, "236B": 128, "405B": 126,
    "671B": 160,
}


def _extract_quant(filename: str) -> tuple[str, float]:
    """Extract quantization type and bits-per-weight from filename."""
    upper = filename.upper()
    # Try longest match first
    for quant in sorted(QUANT_BPW.keys(), key=len, reverse=True):
        if quant.replace("_", "").replace("-", "") in upper.replace("_", "").replace("-", ""):
            return quant, QUANT_BPW[quant]
    # Default: assume Q4_K_M as the most common
    return "Q4_K_M", 4.8


def _extract_param_size(filename: str) -> tuple[str, float]:
    """Extract parameter count (billions) from filename like 'Qwen3-32B'."""
    m = re.search(r'(\d+(?:\.\d+)?)\s*[Bb]\b', filename)
    if m:
        val = m.group(1)
        return f"{val}B", float(val)
    return "unknown", 0.0


def _estimate_layers(param_str: str, param_b: float) -> int:
    """Estimate number of transformer layers."""
    if param_str in PARAM_LAYERS:
        return PARAM_LAYERS[param_str]
    # Interpolate: rough heuristic
    if param_b <= 1:
        return 24
    elif param_b <= 3:
        return 28
    elif param_b <= 10:
        return 32
    elif param_b <= 20:
        return 40
    elif param_b <= 35:
        return 64
    elif param_b <= 75:
        return 80
    else:
        return 128


def _is_reasoning_model(filename: str) -> bool:
    """Detect reasoning/thinking models from filename."""
    lower = filename.lower()
    indicators = ["r1", "reasoning", "think", "cot", "deepseek-r", "qwq"]
    return any(ind in lower for ind in indicators)


def _is_vision_model(filename: str) -> bool:
    """Detect multimodal/vision models."""
    lower = filename.lower()
    return any(x in lower for x in ["vision", "mmproj", "vl", "minicpm-v"])


def _is_moe_model(filename: str) -> bool:
    """Detect Mixture of Experts models."""
    lower = filename.lower()
    return any(x in lower for x in ["moe", "mixtral", "dbrx", "qwen3-235b", "deepseek-v3"])


def estimate_model_metadata(filename: str, size_mb: float) -> dict:
    """
    Estimate model metadata from filename and file size.
    Returns dict with quant, bpw, param_str, param_b, estimated_layers,
    is_reasoning, is_vision, is_moe.
    """
    quant, bpw = _extract_quant(filename)
    param_str, param_b = _extract_param_size(filename)

    # If we couldn't get param size from name, estimate from file size + bpw
    if param_b == 0 and size_mb > 0:
        # model_size_bytes ≈ param_count * bpw / 8
        param_b = round((size_mb / 1024) * 8 / bpw, 1)
        param_str = f"~{param_b}B"

    layers = _estimate_layers(param_str.replace("~", ""), param_b)

    return {
        "quant": quant,
        "bpw": bpw,
        "param_str": param_str,
        "param_b": param_b,
        "estimated_layers": layers,
        "is_reasoning": _is_reasoning_model(filename),
        "is_vision": _is_vision_model(filename),
        "is_moe": _is_moe_model(filename),
    }


# ---------------------------------------------------------------------------
# Hugging Face metadata (Alternativa B)
# ---------------------------------------------------------------------------

async def _fetch_hf_metadata(author: str, repo: str) -> Optional[dict]:
    """
    Try to fetch model metadata from HF API.
    Returns enriched metadata dict or None on failure.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = f"https://huggingface.co/api/models/{author}/{repo}"
            resp = await client.get(url)
            if resp.status_code != 200:
                return None
            data = resp.json()

            tags = data.get("tags", [])
            # Try to extract num_hidden_layers from config
            config = data.get("config", {})
            num_layers = None
            max_position = None
            if config:
                num_layers = config.get("num_hidden_layers")
                max_position = config.get("max_position_embeddings")

            return {
                "hf_tags": tags,
                "hf_num_layers": num_layers,
                "hf_max_position": max_position,
                "hf_available": True,
            }
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Recommendation calculation
# ---------------------------------------------------------------------------

def _get_hardware() -> dict:
    """Collect current hardware info."""
    cpu_cores = psutil.cpu_count(logical=False) or 4
    cpu_threads = psutil.cpu_count(logical=True) or 8
    ram = psutil.virtual_memory()
    gpu = get_nvidia_vram()

    return {
        "cpu_cores": cpu_cores,
        "cpu_threads": cpu_threads,
        "ram_total_gb": round(ram.total / (1024**3), 2),
        "ram_free_gb": round(ram.available / (1024**3), 2),
        "vram_total_mb": gpu.get("total_mb", 0) if gpu.get("available") else 0,
        "vram_free_mb": gpu.get("free_mb", 0) if gpu.get("available") else 0,
        "gpu_available": gpu.get("available", False),
    }


def calculate_recommendation(
    hardware: dict,
    model_meta: dict,
    model_size_mb: float,
) -> RecommendationResponse:
    """
    Core recommendation engine. Takes hardware info + model metadata
    and produces an optimal configuration.
    """
    vram_free_mb = hardware["vram_free_mb"]
    vram_free_gb = vram_free_mb / 1024
    ram_free_gb = hardware["ram_free_gb"]
    cpu_cores = hardware["cpu_cores"]
    cpu_threads = hardware["cpu_threads"]
    gpu_available = hardware["gpu_available"]

    model_size_gb = model_size_mb / 1024
    estimated_layers = model_meta["estimated_layers"]
    bpw = model_meta["bpw"]
    param_b = model_meta["param_b"]
    is_reasoning = model_meta["is_reasoning"]
    is_moe = model_meta["is_moe"]

    explanation: Dict[str, str] = {}
    confidence = "medium"

    # ── NGL (GPU Layers) ──────────────────────────────────────────────
    # KV cache overhead estimate: ~1.5GB for 8k ctx, scales with ctx
    kv_overhead_gb = 1.5
    effective_vram_gb = max(0, vram_free_gb - kv_overhead_gb)

    if not gpu_available:
        ngl = 0
        explanation["ngl"] = "Sin GPU detectada. Ejecución en CPU solamente."
    elif model_size_gb <= effective_vram_gb:
        ngl = 999  # Full offload
        explanation["ngl"] = (
            f"Modelo ({model_size_gb:.1f}GB) cabe completamente en VRAM "
            f"({vram_free_gb:.1f}GB libre). Offload completo."
        )
    else:
        # Partial offload: estimate how many layers fit
        gb_per_layer = model_size_gb / estimated_layers if estimated_layers > 0 else 1
        ngl = max(0, math.floor(effective_vram_gb / gb_per_layer))
        explanation["ngl"] = (
            f"Offload parcial: {ngl}/{estimated_layers} capas en GPU. "
            f"Modelo ({model_size_gb:.1f}GB) excede VRAM libre ({vram_free_gb:.1f}GB)."
        )

    # ── Context Size ──────────────────────────────────────────────────
    if gpu_available and vram_free_gb >= 16:
        ctx_size = 16384
        explanation["ctx_size"] = "VRAM abundante (≥16GB). Contexto amplio de 16K."
    elif gpu_available and vram_free_gb >= 8:
        ctx_size = 8192
        explanation["ctx_size"] = "VRAM suficiente (≥8GB). Contexto estándar de 8K."
    elif gpu_available and vram_free_gb >= 4:
        ctx_size = 4096
        explanation["ctx_size"] = "VRAM limitada (<8GB). Contexto reducido a 4K."
    else:
        ctx_size = 2048
        explanation["ctx_size"] = "Recursos limitados. Contexto mínimo de 2K para estabilidad."

    # If model barely fits, reduce context to leave room
    if gpu_available and model_size_gb > (effective_vram_gb * 0.8) and ctx_size > 4096:
        ctx_size = 4096
        explanation["ctx_size"] += " Reducido por presión de VRAM."

    # ── Threads ───────────────────────────────────────────────────────
    threads = cpu_cores  # Physical cores for generation
    threads_batch = cpu_threads  # Logical threads for prompt processing
    explanation["threads"] = (
        f"Generación: {threads} hilos (cores físicos). "
        f"Batch: {threads_batch} hilos (threads lógicos)."
    )

    # ── Flash Attention ───────────────────────────────────────────────
    flash_attention = gpu_available
    explanation["flash_attention"] = (
        "Habilitado: GPU detectada, ahorra VRAM y acelera inferencia."
        if gpu_available else
        "Deshabilitado: sin GPU."
    )

    # ── Cache Types ───────────────────────────────────────────────────
    if not gpu_available:
        cache_k = "f16"
        cache_v = "f16"
        explanation["cache_type"] = "CPU-only: f16 para máxima compatibilidad."
    elif ngl == 999 and vram_free_gb > model_size_gb + 4:
        cache_k = "q8_0"
        cache_v = "q8_0"
        explanation["cache_type"] = "VRAM holgada: q8_0 para buena calidad de caché."
    elif ngl == 999:
        cache_k = "q4_0"
        cache_v = "q4_0"
        explanation["cache_type"] = "VRAM justa: q4_0 para ahorrar memoria en KV cache."
    else:
        cache_k = "q4_0"
        cache_v = "q4_0"
        explanation["cache_type"] = "Offload parcial: q4_0 para maximizar capas en GPU."

    # ── Batch Size ────────────────────────────────────────────────────
    if ram_free_gb >= 16:
        batch_size = 2048
        ubatch_size = 512
    elif ram_free_gb >= 8:
        batch_size = 1024
        ubatch_size = 256
    else:
        batch_size = 512
        ubatch_size = 128
    explanation["batch_size"] = (
        f"Batch: {batch_size}, micro-batch: {ubatch_size}. "
        f"Ajustado a RAM disponible ({ram_free_gb:.1f}GB libre)."
    )

    # ── Thinking Mode ─────────────────────────────────────────────────
    thinking_mode = is_reasoning
    explanation["thinking_mode"] = (
        "Habilitado: modelo de razonamiento detectado en el nombre."
        if is_reasoning else
        "Deshabilitado: no es un modelo de razonamiento."
    )

    # ── Mlock / No-Mmap ───────────────────────────────────────────────
    mlock = False
    no_mmap = False
    if not gpu_available and ram_free_gb > model_size_gb * 1.5:
        mlock = True
        explanation["mlock"] = "CPU-only con RAM suficiente: mlock para evitar paginación."
    else:
        explanation["mlock"] = "No necesario con GPU o RAM limitada."

    # ── Tier & Confidence ─────────────────────────────────────────────
    total_mem_gb = vram_free_gb + ram_free_gb
    if gpu_available and model_size_gb <= effective_vram_gb:
        tier = "OPTIMAL"
        confidence = "high"
    elif model_size_gb <= total_mem_gb * 0.7:
        tier = "GOOD"
        confidence = "high" if param_b > 0 else "medium"
    elif model_size_gb <= total_mem_gb:
        tier = "CONSTRAINED"
        confidence = "medium"
    else:
        tier = "CONSTRAINED"
        confidence = "low"

    # If we detected param size from name, bump confidence
    if param_b > 0 and model_meta.get("quant") != "Q4_K_M":
        confidence = "high" if confidence == "medium" else confidence

    # ── Hardware summary ──────────────────────────────────────────────
    hw_summary = {
        "cpu": f"{cpu_cores} cores / {cpu_threads} threads",
        "ram": f"{hardware['ram_total_gb']}GB total, {ram_free_gb:.1f}GB libre",
    }
    if gpu_available:
        hw_summary["gpu"] = f"{hardware['vram_total_mb']}MB total, {vram_free_mb}MB libre"
    else:
        hw_summary["gpu"] = "No detectada"

    # ── Model summary ─────────────────────────────────────────────────
    model_summary = {
        "tamaño": f"{model_size_gb:.1f}GB",
        "parámetros": model_meta["param_str"],
        "cuantización": model_meta["quant"],
        "capas_estimadas": str(estimated_layers),
    }
    if is_reasoning:
        model_summary["tipo"] = "Razonamiento"
    if is_moe:
        model_summary["tipo"] = model_summary.get("tipo", "") + " MoE"
    if model_meta.get("is_vision"):
        model_summary["tipo"] = model_summary.get("tipo", "") + " Visión"

    config = RecommendedConfig(
        ngl=ngl,
        ctx_size=ctx_size,
        threads=threads,
        threads_batch=threads_batch,
        flash_attention=flash_attention,
        cache_type_k=cache_k,
        cache_type_v=cache_v,
        batch_size=batch_size,
        ubatch_size=ubatch_size,
        thinking_mode=thinking_mode,
        jinja=True,
        mlock=mlock,
        no_mmap=no_mmap,
    )

    return RecommendationResponse(
        config=config,
        confidence=confidence,
        tier=tier,
        explanation=explanation,
        hardware_summary=hw_summary,
        model_summary=model_summary,
    )


# ---------------------------------------------------------------------------
# API Endpoint
# ---------------------------------------------------------------------------

@router.post("/", response_model=RecommendationResponse)
async def get_recommendation(req: RecommendationRequest):
    """
    Generate an optimal llama-server configuration recommendation
    based on user hardware and model characteristics.
    """
    # 1. Collect hardware
    hardware = _get_hardware()

    # 2. Estimate model metadata from filename (Alternativa A)
    model_meta = estimate_model_metadata(req.filename, req.model_size_mb)

    # 3. Try to enrich with HF metadata (Alternativa B)
    # Extract author/repo from model_path like "models/Qwen/Qwen3-32B-GGUF/file.gguf"
    parts = req.model_path.replace("\\", "/").split("/")
    if len(parts) >= 3:
        author = parts[-3] if parts[-3] != "models" else (parts[-2] if len(parts) >= 2 else "")
        repo = parts[-2] if parts[-3] != "models" else ""
        # Reconstruct: path could be models/Author/Repo/file.gguf
        for i, p in enumerate(parts):
            if p == "models" and i + 2 < len(parts):
                author = parts[i + 1]
                repo = parts[i + 2]
                break

        if author and repo:
            hf_data = await _fetch_hf_metadata(author, repo)
            if hf_data and hf_data.get("hf_available"):
                # Enrich with HF data
                if hf_data.get("hf_num_layers"):
                    model_meta["estimated_layers"] = hf_data["hf_num_layers"]
                if hf_data.get("hf_max_position"):
                    model_meta["hf_max_position"] = hf_data["hf_max_position"]
                # Check tags for reasoning/moe
                tags = hf_data.get("hf_tags", [])
                tag_str = " ".join(tags).lower()
                if "reasoning" in tag_str or "cot" in tag_str:
                    model_meta["is_reasoning"] = True
                if "moe" in tag_str:
                    model_meta["is_moe"] = True

    # 4. Calculate recommendation
    return calculate_recommendation(hardware, model_meta, req.model_size_mb)
