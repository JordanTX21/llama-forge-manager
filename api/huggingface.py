import os
import subprocess
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class DownloadRequest(BaseModel):
    repo_id: str
    filename: str

@router.post("/download")
def download_model(req: DownloadRequest):
    # En un entorno real, esto debería ser asíncrono o enviar a una cola/websocket
    # Para el MVP, llamamos al script de PowerShell existente.
    try:
        script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "download_model.ps1")
        cmd = [
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",
            "-File", script_path,
            "-RepoId", req.repo_id,
            "-Filename", req.filename
        ]
        
        # Iniciar proceso
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Aquí idealmente leeríamos stdout/stderr progresivamente para la UI
        # Por ahora lo dejamos corriendo en background.
        
        return {"status": "started", "message": f"Downloading {req.filename} from {req.repo_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/local")
def list_local_models():
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    if not os.path.exists(models_dir):
        return {"models": []}
    
    downloaded_models = []
    # Estructura típica: models/<Author>/<Repo>/<filename>.gguf
    for author in os.listdir(models_dir):
        author_path = os.path.join(models_dir, author)
        if os.path.isdir(author_path):
            for repo in os.listdir(author_path):
                repo_path = os.path.join(author_path, repo)
                if os.path.isdir(repo_path):
                    for file in os.listdir(repo_path):
                        if file.endswith(".gguf"):
                            size_mb = round(os.path.getsize(os.path.join(repo_path, file)) / (1024 * 1024), 2)
                            downloaded_models.append({
                                "id": f"{author}/{repo}/{file}",
                                "author": author,
                                "repo": repo,
                                "filename": file,
                                "size_mb": size_mb,
                                "path": os.path.join("models", author, repo, file)
                            })
    return {"models": downloaded_models}
