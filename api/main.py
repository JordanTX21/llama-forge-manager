from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers once we create them
from api.hardware import router as hardware_router
from api.huggingface import router as huggingface_router
from api.runner import router as runner_router
from api.commands import router as commands_router
from api.recommend import router as recommend_router
from api.agents import router as agents_router

app = FastAPI(title="Local AI Manager API")

# Allow CORS for the Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hardware_router, prefix="/api/hardware", tags=["Hardware"])
app.include_router(huggingface_router, prefix="/api/huggingface", tags=["Hugging Face"])
app.include_router(runner_router, prefix="/api/runner", tags=["Runner"])
app.include_router(commands_router, prefix="/api/commands", tags=["Commands"])
app.include_router(recommend_router, prefix="/api/recommend", tags=["Recommend"])
app.include_router(agents_router, prefix="/api/agents", tags=["Agents"])

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

@app.get("/api/status")
def status():
    return {"status": "online"}

from api.paths import get_base_dir

# Serve frontend static files
ui_dist_path = os.path.abspath(os.path.join(get_base_dir(), "ui", "dist"))

if os.path.exists(ui_dist_path):
    # Mount the assets directory specifically
    assets_path = os.path.join(ui_dist_path, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    # Catch-all for SPA routing and other static files at root level
    @app.api_route("/{path_name:path}", methods=["GET"])
    async def catch_all(path_name: str):
        file_path = os.path.join(ui_dist_path, path_name)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
            
        index_path = os.path.join(ui_dist_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
            
        return {"error": "Frontend no compilado o index.html no encontrado. Ejecuta 'npm run build' en ui/"}

