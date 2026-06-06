import os
import re
import yaml
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class CommandConfig(BaseModel):
    filename: str
    alias: str
    model_path: str
    mmproj_path: Optional[str] = ""
    port: int = 8080
    ctx_size: int
    ngl: int
    flash_attention: bool = False
    thinking_mode: bool = False

    threads: int = -1
    threads_batch: int = -1
    np: int = -1
    cr: str = ""
    crb: str = ""
    cpu_strict: bool = False
    cpu_strict_batch: bool = False

    batch_size: int = -1
    ubatch_size: int = -1
    prio: int = -1
    prio_batch: int = -1
    poll: int = -1
    poll_batch: int = -1

    cache_type_k: str = "q8_0"
    cache_type_v: str = "q8_0"
    kv_unified: bool = False
    no_mmap: bool = False
    mlock: bool = False

    ncmoe: int = -1
    spec_type: str = ""
    spec_draft_n_max: int = -1

    temp: float = 0.6
    top_p: float = 0.95
    top_k: int = 20
    min_p: float = 0.0
    presence_penalty: float = 0.0
    repeat_penalty: float = 1.0

    jinja: bool = False


def get_commands_dir():
    return os.path.join(os.path.dirname(__file__), "..", "commands")

def get_config_yaml_path():
    return os.path.join(os.path.dirname(__file__), "..", "config.yaml")

def _parse_int(content: str, pattern: str, default: int = -1) -> int:
    m = re.search(pattern, content)
    return int(m.group(1)) if m else default

def _parse_float(content: str, pattern: str, default: float) -> float:
    m = re.search(pattern, content)
    return float(m.group(1)) if m else default

def _parse_str(content: str, pattern: str, default: str = "") -> str:
    m = re.search(pattern, content)
    return m.group(1) if m else default

def _parse_bool(content: str, switch_name: str) -> bool:
    return switch_name in content

@router.get("/")
def list_commands() -> List[CommandConfig]:
    commands_dir = get_commands_dir()
    if not os.path.exists(commands_dir):
        return []

    configs = []
    for file in os.listdir(commands_dir):
        if file.endswith(".ps1"):
            filepath = os.path.join(commands_dir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            alias_m = re.search(r'-Alias\s+"([^"]+)"', content)
            model_path_m = re.search(r'-ModelPath\s+"([^"]+)"', content)
            
            if not alias_m or not model_path_m:
                continue

            configs.append(CommandConfig(
                filename=file,
                alias=alias_m.group(1),
                model_path=model_path_m.group(1),
                mmproj_path=_parse_str(content, r'-MmprojPath\s+"([^"]+)"', ""),
                port=_parse_int(content, r'\[int\]\$Port\s*=\s*(\d+)', 8080),
                ctx_size=_parse_int(content, r'-CtxSize\s+(\d+)', 4096),
                ngl=_parse_int(content, r'-Ngl\s+(\d+)', 0),
                flash_attention=_parse_bool(content, '-FlashAttention'),
                thinking_mode=_parse_bool(content, '-Thinking'),
                
                threads=_parse_int(content, r'-Threads\s+(\d+)', -1),
                threads_batch=_parse_int(content, r'-ThreadsBatch\s+(\d+)', -1),
                np=_parse_int(content, r'-Np\s+(\d+)', -1),
                cr=_parse_str(content, r'-Cr\s+"([^"]+)"', ""),
                crb=_parse_str(content, r'-Crb\s+"([^"]+)"', ""),
                cpu_strict=_parse_bool(content, '-CpuStrict'),
                cpu_strict_batch=_parse_bool(content, '-CpuStrictBatch'),
                
                batch_size=_parse_int(content, r'-BatchSize\s+(\d+)', -1),
                ubatch_size=_parse_int(content, r'-UbatchSize\s+(\d+)', -1),
                prio=_parse_int(content, r'-Prio\s+(\d+)', -1),
                prio_batch=_parse_int(content, r'-PrioBatch\s+(\d+)', -1),
                poll=_parse_int(content, r'-Poll\s+(\d+)', -1),
                poll_batch=_parse_int(content, r'-PollBatch\s+(\d+)', -1),
                
                cache_type_k=_parse_str(content, r'-CacheTypeK\s+"([^"]+)"', "q8_0"),
                cache_type_v=_parse_str(content, r'-CacheTypeV\s+"([^"]+)"', "q8_0"),
                kv_unified=_parse_bool(content, '-KvUnified'),
                no_mmap=_parse_bool(content, '-NoMmap'),
                mlock=_parse_bool(content, '-Mlock'),
                
                ncmoe=_parse_int(content, r'-NcMoe\s+(\d+)', -1),
                spec_type=_parse_str(content, r'-SpecType\s+"([^"]+)"', ""),
                spec_draft_n_max=_parse_int(content, r'-SpecDraftNMax\s+(\d+)', -1),
                
                temp=_parse_float(content, r'-Temp\s+([0-9.]+)', 0.6),
                top_p=_parse_float(content, r'-TopP\s+([0-9.]+)', 0.95),
                top_k=_parse_int(content, r'-TopK\s+(\d+)', 20),
                min_p=_parse_float(content, r'-MinP\s+([0-9.]+)', 0.0),
                presence_penalty=_parse_float(content, r'-PresencePenalty\s+([0-9.]+)', 0.0),
                repeat_penalty=_parse_float(content, r'-RepeatPenalty\s+([0-9.]+)', 1.0),
                
                jinja=_parse_bool(content, '-Jinja')
            ))
    return configs

@router.post("/")
def save_command(config: CommandConfig):
    if not config.filename.endswith('.ps1'):
        config.filename += '.ps1'
    
    commands_dir = get_commands_dir()
    os.makedirs(commands_dir, exist_ok=True)
    filepath = os.path.join(commands_dir, config.filename)

    def s(key: str, val: str) -> str: return f'\n    -{key} "{val}" `' if val else ""
    def i(key: str, val: int) -> str: return f'\n    -{key} {val} `' if val >= 0 else ""
    def f(key: str, val: float) -> str: return f'\n    -{key} {val} `'
    def b(key: str, val: bool) -> str: return f'\n    -{key} `' if val else ""

    args_str = (
        s("MmprojPath", config.mmproj_path) +
        i("Threads", config.threads) +
        i("ThreadsBatch", config.threads_batch) +
        i("Np", config.np) +
        s("Cr", config.cr) +
        s("Crb", config.crb) +
        b("CpuStrict", config.cpu_strict) +
        b("CpuStrictBatch", config.cpu_strict_batch) +
        
        i("BatchSize", config.batch_size) +
        i("UbatchSize", config.ubatch_size) +
        i("Prio", config.prio) +
        i("PrioBatch", config.prio_batch) +
        i("Poll", config.poll) +
        i("PollBatch", config.poll_batch) +
        
        s("CacheTypeK", config.cache_type_k) +
        s("CacheTypeV", config.cache_type_v) +
        b("KvUnified", config.kv_unified) +
        b("NoMmap", config.no_mmap) +
        b("Mlock", config.mlock) +
        
        i("NcMoe", config.ncmoe) +
        s("SpecType", config.spec_type) +
        i("SpecDraftNMax", config.spec_draft_n_max) +
        
        f("Temp", config.temp) +
        f("TopP", config.top_p) +
        i("TopK", config.top_k) +
        f("MinP", config.min_p) +
        f("PresencePenalty", config.presence_penalty) +
        f("RepeatPenalty", config.repeat_penalty) +
        
        b("Jinja", config.jinja) +
        b("FlashAttention", config.flash_attention) +
        b("Thinking", config.thinking_mode)
    )

    template = f"""param(
    [int]$Port = {config.port}
)

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$RunModelScript = Join-Path $RootDir "scripts\\run_model.ps1"

& $RunModelScript `
    -ModelPath "{config.model_path}" `
    -Alias "{config.alias}" `
    -CtxSize {config.ctx_size} `
    -Ngl {config.ngl} `
    -Port $Port `{args_str}
"""
    # Remove dangling backtick if any
    template = template.rstrip(" `\n") + "\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template)

    yaml_path = get_config_yaml_path()
    data = {"models": {}}
    if os.path.exists(yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file) or {"models": {}}
            if "models" not in data:
                data["models"] = {}

    data["models"][config.alias] = {
        "name": f"{config.alias} (Local)",
        "cmd": f"powershell.exe -ExecutionPolicy Bypass -File C:/llama.cpp/commands/{config.filename} -Port ${{PORT}}"
    }

    with open(yaml_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)

    return {"status": "success", "message": f"Command {config.filename} saved and config.yaml updated."}
