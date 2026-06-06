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
        script_path = os.path.join(os.path.dirname(__file__), "..", "start-swap.ps1")
        cmd = [
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",
            "-File", script_path
        ]
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return {"status": "started", "message": "Started llama-swap"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
