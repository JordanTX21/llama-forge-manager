/**
 * Official documentation for llama.cpp parameters, extracted from tools/cli/README.md
 * and custom UI explanations.
 */
export const LLAMA_DOCS = {
  // Basic Form
  alias: "Identificador único del modelo para el servidor y la interfaz (llama-swap).",
  port: "Puerto en el que escuchará el servidor (ej. 8080).",
  model_path: "Ruta relativa o absoluta al archivo GGUF del modelo principal (-m, --model).",
  ctx_size: "Tamaño del prompt context en tokens (-c, --ctx-size). (default: 0 = loaded from model).",
  ngl: "Número máximo de capas a descargar a la GPU/VRAM (-ngl, --gpu-layers). Usa 999 para offload completo. (default: auto)",
  mmproj_path: "Ruta al archivo adaptador de visión multimodal (--mmproj).",
  flash_attention: "Habilita los kernels de aceleración v2. Ahorra VRAM y es más rápido (-fa, --flash-attn).",
  thinking_mode: "Parsear el contenido de pensamiento de los modelos de razonamiento (ej. DeepSeek-R1) en la UI.",

  // Advanced - Sampling
  temp: "Controla la aleatoriedad de las respuestas. (default: 0.8)",
  top_p: "Nucleus sampling: considera solo los tokens que suman hasta Top P de masa de probabilidad. (default: 0.9)",
  top_k: "Limita la selección a los K tokens más probables. (default: 40)",
  min_p: "Probabilidad mínima base dinámica respecto al token más probable. (default: 0.1)",
  presence_penalty: "Penaliza tokens nuevos según si ya aparecen en el texto generado (fomenta la diversidad). (default: 0.0)",
  repeat_penalty: "Penaliza la repetición estricta de secuencias. (default: 1.0)",

  // Advanced - Memory & Cache
  cache_type_k: "Tipo de dato para la caché KV (llaves). Ej: q8_0, q4_0, f16 (-ctk, --cache-type-k).",
  cache_type_v: "Tipo de dato para la caché KV (valores). Ej: q8_0, q4_0, f16 (-ctv, --cache-type-v).",
  kv_unified: "Combina la caché KV para K y V si la arquitectura lo permite.",
  no_mmap: "No usa archivos mapeados en memoria (--no-mmap). Carga más lenta pero reduce pageouts si no se usa mlock.",
  mlock: "Impide que el modelo sea movido al archivo de paginación (swap). Lo mantiene en RAM (--mlock).",

  // Advanced - Compute & Threads
  threads: "Número de hilos de CPU a utilizar durante la generación (-t, --threads).",
  threads_batch: "Número de hilos a utilizar durante el procesamiento de prompt y batches (-tb, --threads-batch).",
  np: "Número de slots/procesos paralelos a soportar simultáneamente (-np, --parallel).",
  cr: "Rango de CPUs para afinidad. Complementa --cpu-mask (-Cr, --cpu-range).",
  crb: "Rango de CPUs para afinidad durante batch. Complementa --cpu-mask-batch (-Crb, --cpu-range-batch).",
  cpu_strict: "Usa posicionamiento estricto de CPU (--cpu-strict).",
  cpu_strict_batch: "Usa posicionamiento estricto de CPU para batch (--cpu-strict-batch).",

  // Advanced - Batching
  batch_size: "Tamaño máximo lógico del batch (tokens procesados a la vez) (-b, --batch-size). (default: 2048)",
  ubatch_size: "Tamaño máximo físico (micro-batch) de procesamiento (-ub, --ubatch-size). (default: 512)",
  prio: "Establece la prioridad del proceso/hilo: low(-1), normal(0), medium(1), high(2), realtime(3) (--prio).",
  prio_batch: "Establece la prioridad del proceso/hilo para batch (--prio-batch).",
  poll: "Nivel de sondeo (polling) para esperar trabajo (0 = no polling) (--poll). (default: 50)",
  poll_batch: "Nivel de sondeo para esperar trabajo en batch (--poll-batch).",

  // Advanced - MoE & Speculative Decoding
  ncmoe: "Mantiene los pesos de Mixture of Experts (MoE) de las primeras N capas en la CPU (-ncmoe, --n-cpu-moe).",
  spec_type: "Tipo de decodificación especulativa (ej. draft-mtp).",
  spec_draft_n_max: "Máximo número de tokens en borrador para la decodificación especulativa.",

  // Misc
  jinja: "Utiliza el motor Jinja para parsear plantillas y formato de chat (chat template) si está disponible."
}
