import multiprocessing
import uvicorn
import os
import sys
import shutil
from api.main import app
from api.paths import get_env_path, get_user_data_dir

def ensure_env_file():
    """Copia el .env default al directorio del usuario si no existe."""
    target_env = get_env_path()
    if not os.path.exists(target_env):
        # Determinar de donde copiar el .env.example
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        example_env = os.path.join(base_dir, ".env.example")
        if os.path.exists(example_env):
            shutil.copy(example_env, target_env)
            print(f"[*] Archivo .env por defecto creado en {target_env}")
        else:
            print("[!] No se encontró .env.example para inicializar la configuración.")

def get_port():
    env_path = get_env_path()
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    parts = line.split("=", 1)
                    if len(parts) == 2 and parts[0].strip() == "DEFAULT_PORT":
                        try:
                            return int(parts[1].strip())
                        except ValueError:
                            pass
    return 8000

if __name__ == '__main__':
    # Necesario para que uvicorn funcione correctamente en Windows cuando es empaquetado por PyInstaller
    multiprocessing.freeze_support()
    
    print("========================================")
    print("Llama Forge Manager (Standalone Mode)")
    print(f"Data Directory: {get_user_data_dir()}")
    print("========================================")
    
    ensure_env_file()
    port = get_port()
    
    print(f"Iniciando aplicación en http://localhost:{port}")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
