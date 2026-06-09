import os
import threading
import time
import requests
from fastapi import APIRouter, Query
from pydantic import BaseModel
from api.paths import get_models_dir

router = APIRouter()

active_downloads = {}

class DownloadRequest(BaseModel):
    repo_id: str
    filename: str

def format_size(size_in_bytes):
    if size_in_bytes < 1024:
        return f"{size_in_bytes}B"
    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.1f}KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.1f}MB"
    else:
        return f"{size_in_bytes / (1024 * 1024 * 1024):.2f}GB"

def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"
    else:
        return f"{int(seconds // 3600):02d}:{int((seconds % 3600) // 60):02d}:{int(seconds % 60):02d}"

def native_download_worker(repo_id: str, filename: str, target_dir: str, download_id: str):
    active_downloads[download_id] = {
        "status": "downloading",
        "progress": 0,
        "speed": "",
        "eta": "",
        "downloaded": "",
        "total": ""
    }
    
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, filename)
    part_path = target_path + ".part"
    
    url = f"https://huggingface.co/{repo_id}/resolve/main/{filename}"
    headers = {}
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"
        
    try:
        with requests.get(url, headers=headers, stream=True, allow_redirects=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get("content-length", 0))
            active_downloads[download_id]["total"] = format_size(total_size) if total_size else "?"
            
            downloaded_size = 0
            start_time = time.time()
            last_update_time = start_time
            last_update_size = 0
            
            with open(part_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024): # 1MB chunks
                    if not chunk:
                        continue
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    current_time = time.time()
                    time_diff = current_time - last_update_time
                    
                    if time_diff >= 0.5: # Update state every 0.5 seconds
                        speed_bytes = (downloaded_size - last_update_size) / time_diff
                        active_downloads[download_id]["speed"] = f"{format_size(speed_bytes)}/s"
                        
                        if total_size > 0:
                            active_downloads[download_id]["progress"] = int((downloaded_size / total_size) * 100)
                            if speed_bytes > 0:
                                eta_seconds = (total_size - downloaded_size) / speed_bytes
                                active_downloads[download_id]["eta"] = format_time(eta_seconds)
                        
                        active_downloads[download_id]["downloaded"] = format_size(downloaded_size)
                        last_update_time = current_time
                        last_update_size = downloaded_size
        
        # Finish
        if os.path.exists(target_path):
            os.remove(target_path)
        os.rename(part_path, target_path)
        
        active_downloads[download_id]["status"] = "completed"
        active_downloads[download_id]["progress"] = 100
        active_downloads[download_id]["downloaded"] = active_downloads[download_id]["total"]
        active_downloads[download_id]["eta"] = ""
        active_downloads[download_id]["speed"] = ""
        
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        active_downloads[download_id]["status"] = "error"

@router.post("/download")
def download_model(req: DownloadRequest):
    try:
        author = req.repo_id.split('/')[0] if '/' in req.repo_id else 'Uncategorized'
        repo_name = req.repo_id.split('/')[1] if '/' in req.repo_id else req.repo_id
        target_dir = os.path.join(get_models_dir(), author, repo_name)
        
        download_id = f"{req.repo_id}/{req.filename}"
        
        if download_id in active_downloads and active_downloads[download_id]["status"] == "downloading":
            return {"status": "started", "message": "Already downloading"}
            
        thread = threading.Thread(target=native_download_worker, args=(req.repo_id, req.filename, target_dir, download_id), daemon=True)
        thread.start()
        
        return {"status": "started", "message": f"Downloading {req.filename} from {req.repo_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/download/status")
def get_download_status(repo_id: str, filename: str):
    download_id = f"{repo_id}/{filename}"
    if download_id in active_downloads:
        return active_downloads[download_id]
    return {"status": "idle"}

@router.get("/local")
def list_local_models():
    models_dir = get_models_dir()
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
