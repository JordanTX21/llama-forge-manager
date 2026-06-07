import os
import re
import yaml
from fastapi import APIRouter, HTTPException
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
    
    raw_content: Optional[str] = None


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

def _parse_bool(content: str, switch_name: str, has_on: bool = False) -> bool:
    if has_on:
        return bool(re.search(rf'{switch_name}(?:\s+on)?\b', content))
    return switch_name in content

def parse_ps1_content(content: str, filename: str) -> CommandConfig:
    def get_val(pattern, default=""):
        m = re.search(pattern, content)
        if m:
            val = m.group(1).strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            if val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            return val
        return default

    alias = get_val(r'-a\s+([^\s`\n\r]+|"[^"]+")')
    model_path = get_val(r'-m\s+([^\s`\n\r]+|"[^"]+")')
    mmproj_path = get_val(r'-mm\s+([^\s`\n\r]+|"[^"]+")')
    
    if model_path.startswith("..\\"):
        model_path = model_path[3:]
    elif model_path.startswith("../"):
        model_path = model_path[3:]
        
    if mmproj_path.startswith("..\\"):
        mmproj_path = mmproj_path[3:]
    elif mmproj_path.startswith("../"):
        mmproj_path = mmproj_path[3:]
        
    return CommandConfig(
        filename=filename,
        alias=alias,
        model_path=model_path,
        mmproj_path=mmproj_path,
        port=_parse_int(content, r'\[int\]\$Port\s*=\s*(\d+)', 8080),
        ctx_size=_parse_int(content, r'-c\s+(\d+)', 4096),
        ngl=_parse_int(content, r'-ngl\s+(\d+)', 0),
        flash_attention=bool(re.search(r'-fa\s+on\b', content) or re.search(r'--flash-attn\b', content)),
        thinking_mode=bool(re.search(r'--reasoning(?:-format)?(?:\s+on)?\b', content) or re.search(r'--reasoning\b', content)),
        
        threads=_parse_int(content, r'-t\s+(\d+)', -1),
        threads_batch=_parse_int(content, r'-tb\s+(\d+)', -1),
        np=_parse_int(content, r'-np\s+(\d+)', -1),
        cr=get_val(r'-Cr\s+([^\s`\n\r]+|"[^"]+")'),
        crb=get_val(r'-Crb\s+([^\s`\n\r]+|"[^"]+")'),
        cpu_strict=bool(re.search(r'--cpu-strict\s+1\b', content)),
        cpu_strict_batch=bool(re.search(r'--cpu-strict-batch\s+1\b', content)),
        
        batch_size=_parse_int(content, r'-b\s+(\d+)', -1),
        ubatch_size=_parse_int(content, r'-ub\s+(\d+)', -1),
        prio=_parse_int(content, r'--prio\s+(\d+)', -1),
        prio_batch=_parse_int(content, r'--prio-batch\s+(\d+)', -1),
        poll=_parse_int(content, r'--poll\s+(\d+)', -1),
        poll_batch=_parse_int(content, r'--poll-batch\s+(\d+)', -1),
        
        cache_type_k=get_val(r'--cache-type-k\s+([^\s`\n\r]+|"[^"]+")', "q8_0"),
        cache_type_v=get_val(r'--cache-type-v\s+([^\s`\n\r]+|"[^"]+")', "q8_0"),
        kv_unified=_parse_bool(content, '--kv-unified'),
        no_mmap=_parse_bool(content, '--no-mmap'),
        mlock=_parse_bool(content, '--mlock'),
        
        ncmoe=_parse_int(content, r'-ncmoe\s+(\d+)', -1),
        spec_type=get_val(r'--spec-type\s+([^\s`\n\r]+|"[^"]+")'),
        spec_draft_n_max=_parse_int(content, r'--spec-draft-n-max\s+(\d+)', -1),
        
        temp=_parse_float(content, r'--temp\s+([0-9.]+)', 0.6),
        top_p=_parse_float(content, r'--top-p\s+([0-9.]+)', 0.95),
        top_k=_parse_int(content, r'--top-k\s+(\d+)', 20),
        min_p=_parse_float(content, r'--min-p\s+([0-9.]+)', 0.0),
        presence_penalty=_parse_float(content, r'--presence-penalty\s+([0-9.]+)', 0.0),
        repeat_penalty=_parse_float(content, r'--repeat-penalty\s+([0-9.]+)', 1.0),
        
        jinja=_parse_bool(content, '--jinja'),
        raw_content=content
    )

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

            try:
                conf = parse_ps1_content(content, file)
                if conf.alias and conf.model_path:
                    configs.append(conf)
            except Exception as e:
                print(f"Error parsing {file}: {e}")
                
    return configs

@router.post("/")
def save_command(config: CommandConfig):
    if not config.filename.endswith('.ps1'):
        config.filename += '.ps1'
    
    commands_dir = get_commands_dir()
    os.makedirs(commands_dir, exist_ok=True)
    filepath = os.path.join(commands_dir, config.filename)

    if config.raw_content:
        try:
            parsed = parse_ps1_content(config.raw_content, config.filename)
            if not parsed.alias or not parsed.model_path:
                raise ValueError("Missing Alias (-a) or Model Path (-m) in raw code.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse raw code: {e}")
            
        template = config.raw_content
    else:
        def s(key: str, val: str) -> str: return f'\n    {key} "{val}" `' if val else ""
        def s_no_quote(key: str, val: str) -> str: return f'\n    {key} {val} `' if val else ""
        def i(key: str, val: int) -> str: return f'\n    {key} {val} `' if val >= 0 else ""
        def f(key: str, val: float) -> str: return f'\n    {key} {val} `'
        def b(key: str, val: bool) -> str: return f'\n    {key} `' if val else ""

        args_str = (
            s("-mm", config.mmproj_path) +
            i("-t", config.threads) +
            i("-tb", config.threads_batch) +
            i("-np", config.np) +
            s_no_quote("-Cr", config.cr) +
            s_no_quote("-Crb", config.crb) +
            (f'\n    --cpu-strict 1 `' if config.cpu_strict else '') +
            (f'\n    --cpu-strict-batch 1 `' if config.cpu_strict_batch else '') +
            
            i("-b", config.batch_size) +
            i("-ub", config.ubatch_size) +
            i("--prio", config.prio) +
            i("--prio-batch", config.prio_batch) +
            i("--poll", config.poll) +
            i("--poll-batch", config.poll_batch) +
            
            s("--cache-type-k", config.cache_type_k) +
            s("--cache-type-v", config.cache_type_v) +
            b("--kv-unified", config.kv_unified) +
            b("--no-mmap", config.no_mmap) +
            b("--mlock", config.mlock) +
            
            i("-ncmoe", config.ncmoe) +
            s("--spec-type", config.spec_type) +
            i("--spec-draft-n-max", config.spec_draft_n_max) +
            
            f("--temp", config.temp) +
            f("--top-p", config.top_p) +
            i("--top-k", config.top_k) +
            f("--min-p", config.min_p) +
            f("--presence-penalty", config.presence_penalty) +
            f("--repeat-penalty", config.repeat_penalty) +
            
            b("--jinja", config.jinja) +
            (f'\n    -fa on `' if config.flash_attention else '') +
            (f'\n    --reasoning on `' if config.thinking_mode else '')
        )

        template = f"""param(
    [int]$Port = {config.port}
)

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $RootDir

$EnvPath = Join-Path $RootDir ".env"
if (Test-Path $EnvPath) {{
    Get-Content $EnvPath | ForEach-Object {{
        if ($_ -match '^\\s*([^#]+?)\\s*=\\s*(.*)$') {{ Set-Item -Path "Env:\$($matches[1])" -Value $matches[2] }}
    }}
}}

$BinDir = if ($env:LLAMA_BIN_DIR) {{ $env:LLAMA_BIN_DIR }} else {{ "bin\\llama-b9037-bin-win-cuda-13.1-x64" }}
$ExeName = if ($env:LLAMA_SERVER_EXE) {{ $env:LLAMA_SERVER_EXE }} else {{ "llama-server.exe" }}
$LlamaExe = Join-Path $RootDir (Join-Path $BinDir $ExeName)
$HostAddr = if ($env:DEFAULT_HOST) {{ $env:DEFAULT_HOST }} else {{ "127.0.0.1" }}

& $LlamaExe `
    -m "{config.model_path}" `
    -c {config.ctx_size} `
    -ngl {config.ngl} `
    --port $Port `
    --host $HostAddr `{args_str}
    -a "{config.alias}"
"""
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

    conf_alias = config.alias
    if config.raw_content:
        parsed = parse_ps1_content(config.raw_content, config.filename)
        conf_alias = parsed.alias
        
    data["models"][conf_alias] = {
        "name": f"{conf_alias} (Local)",
        "cmd": f"powershell.exe -ExecutionPolicy Bypass -File C:/llama.cpp/commands/{config.filename} -Port ${{PORT}}"
    }

    with open(yaml_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)

    return {"status": "success", "message": f"Command {config.filename} saved and config.yaml updated."}
