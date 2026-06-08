import os
import subprocess
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from .install_utils import ensure_llama_swap, ensure_llama_cpp, get_os
from .paths import get_base_dir, get_commands_dir, get_user_data_dir

router = APIRouter()

class RunModelRequest(BaseModel):
    model_path: str
    alias: str
    ctx_size: int
    ngl: int
    port: int = 8080
    flash_attention: bool = False
    extra_args: Optional[List[str]] = []

@router.post("/start")
def start_model(req: RunModelRequest):
    try:
        ensure_llama_cpp()
        
        current_os = get_os()
        base_dir = get_base_dir()
        if current_os == "Windows":
            script_path = os.path.join(base_dir, "scripts", "run_model.ps1")
            cmd = [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", script_path,
                "-ModelPath", req.model_path,
                "-Alias", req.alias,
                "-CtxSize", str(req.ctx_size),
                "-Ngl", str(req.ngl),
                "-Port", str(req.port)
            ]
            if req.flash_attention:
                cmd.extend(["-ExtraArgs", "'-fa on'"])
            process = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=get_user_data_dir())
        else:
            script_path = os.path.join(base_dir, "scripts", "run_model.sh")
            cmd = [
                "bash", script_path,
                "--model", req.model_path,
                "--alias", req.alias,
                "--ctx-size", str(req.ctx_size),
                "--ngl", str(req.ngl),
                "--port", str(req.port)
            ]
            if req.flash_attention:
                cmd.extend(["--extra-args", "-fa on"])
            process = subprocess.Popen(cmd, start_new_session=True, cwd=get_user_data_dir())
            
        return {"status": "started", "message": f"Started {req.alias} on port {req.port}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/swap")
def start_swap():
    try:
        ensure_llama_swap()
        
        current_os = get_os()
        base_dir = get_base_dir()
        if current_os == "Windows":
            script_path = os.path.join(base_dir, "scripts", "start-swap.ps1")
            cmd = [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", script_path
            ]
            subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=get_user_data_dir())
        else:
            script_path = os.path.join(base_dir, "scripts", "start-swap.sh")
            cmd = ["bash", script_path]
            subprocess.Popen(cmd, start_new_session=True, cwd=get_user_data_dir())
            
        return {"status": "started", "message": "Started llama-swap"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class RunCommandRequest(BaseModel):
    filename: str

@router.post("/command")
def run_command_script(req: RunCommandRequest):
    """Execute a saved command script by filename."""
    if not (req.filename.endswith(".ps1") or req.filename.endswith(".sh")):
        return {"status": "error", "message": "Only .ps1 or .sh files are allowed."}
    if ".." in req.filename or "/" in req.filename or "\\" in req.filename:
        return {"status": "error", "message": "Invalid filename."}

    commands_dir = get_commands_dir()
    script_path = os.path.abspath(os.path.join(commands_dir, req.filename))

    if not script_path.startswith(os.path.abspath(commands_dir)):
        return {"status": "error", "message": "Invalid filename."}

    if not os.path.exists(script_path):
        return {"status": "error", "message": f"Command script '{req.filename}' not found."}

    try:
        ensure_llama_cpp()
        current_os = get_os()
        
        if req.filename.endswith(".ps1") and current_os == "Windows":
            cmd = [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", script_path
            ]
            subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=get_user_data_dir())
        elif req.filename.endswith(".sh") and current_os in ["Linux", "Darwin"]:
            cmd = ["bash", script_path]
            subprocess.Popen(cmd, start_new_session=True, cwd=get_user_data_dir())
        else:
            return {"status": "error", "message": f"Script {req.filename} no está soportado en este sistema operativo ({current_os})."}
            
        return {"status": "started", "message": f"Started command '{req.filename}'"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
