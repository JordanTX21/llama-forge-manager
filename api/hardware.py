import subprocess
import psutil
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

def get_nvidia_vram() -> dict:
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=memory.total,memory.free,memory.used', '--format=csv,nounits,noheader'],
            capture_output=True, text=True, check=True
        )
        # nvidia-smi output: "12288, 10000, 2288"
        total, free, used = [int(x.strip()) for x in result.stdout.strip().split(',')]
        return {"total_mb": total, "free_mb": free, "used_mb": used, "available": True}
    except Exception as e:
        return {"available": False, "error": str(e)}

@router.get("/")
def get_hardware_info() -> Dict[str, Any]:
    # CPU
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    ram = psutil.virtual_memory()
    
    # GPU
    gpu_info = get_nvidia_vram()
    
    return {
        "cpu": {
            "cores": cpu_cores,
            "threads": cpu_threads,
            "usage_percent": psutil.cpu_percent()
        },
        "ram": {
            "total_gb": round(ram.total / (1024**3), 2),
            "free_gb": round(ram.available / (1024**3), 2),
            "usage_percent": ram.percent
        },
        "gpu": gpu_info
    }
