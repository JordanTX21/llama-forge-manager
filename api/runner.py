import os
import subprocess
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

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
        script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "run_model.ps1")
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
            # Asumimos que run_model.ps1 lo manejará o lo inyectamos como ExtraArgs
            cmd.extend(["-ExtraArgs", "'-fa on'"])
            
        process = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return {"status": "started", "message": f"Started {req.alias} on port {req.port}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/swap")
def start_swap():
    try:
        script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "start-swap.ps1")
        cmd = [
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",
            "-File", script_path
        ]
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return {"status": "started", "message": "Started llama-swap"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

class RunCommandRequest(BaseModel):
    filename: str

@router.post("/command")
def run_command_script(req: RunCommandRequest):
    """Execute a saved .ps1 command script by filename."""
    # Security: only allow .ps1 files, no path traversal
    if not req.filename.endswith(".ps1"):
        return {"status": "error", "message": "Only .ps1 files are allowed."}
    if ".." in req.filename or "/" in req.filename or "\\" in req.filename:
        return {"status": "error", "message": "Invalid filename."}

    commands_dir = os.path.join(os.path.dirname(__file__), "..", "commands")
    script_path = os.path.abspath(os.path.join(commands_dir, req.filename))

    # Ensure resolved path is still inside commands_dir
    if not script_path.startswith(os.path.abspath(commands_dir)):
        return {"status": "error", "message": "Invalid filename."}

    if not os.path.exists(script_path):
        return {"status": "error", "message": f"Command script '{req.filename}' not found."}

    try:
        cmd = [
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",
            "-File", script_path
        ]
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return {"status": "started", "message": f"Started command '{req.filename}'"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
