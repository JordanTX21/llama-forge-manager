from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers once we create them
from api.hardware import router as hardware_router
from api.huggingface import router as huggingface_router
from api.runner import router as runner_router
from api.commands import router as commands_router
from api.recommend import router as recommend_router

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

@app.get("/api/status")
def status():
    return {"status": "online"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
