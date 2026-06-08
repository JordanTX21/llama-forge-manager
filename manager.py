import os
import sys
import subprocess
import shutil
import platform

def print_step(msg):
    print(f"\n\033[96m>>> {msg}\033[0m")

def print_success(msg):
    print(f"\033[92m{msg}\033[0m")

def print_error(msg):
    print(f"\033[91m{msg}\033[0m")

def run_cmd(cmd, cwd=None):
    try:
        subprocess.run(cmd, cwd=cwd, check=True, shell=platform.system() == "Windows")
    except subprocess.CalledProcessError as e:
        print_error(f"Error al ejecutar: {' '.join(cmd)}")
        sys.exit(1)

def get_env_var(key, default):
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    parts = line.split("=", 1)
                    if len(parts) == 2 and parts[0].strip() == key:
                        return parts[1].strip()
    return default

def needs_rebuild(ui_dir, dist_dir):
    if not os.path.exists(dist_dir):
        return True
    dist_mtime = os.path.getmtime(dist_dir)
    src_dir = os.path.join(ui_dir, "src")
    if os.path.exists(src_dir):
        for root, _, files in os.walk(src_dir):
            for file in files:
                if os.path.getmtime(os.path.join(root, file)) > dist_mtime:
                    return True
    for file in ["package.json", "vite.config.ts"]:
        p = os.path.join(ui_dir, file)
        if os.path.exists(p) and os.path.getmtime(p) > dist_mtime:
            return True
    return False

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    ui_dir = os.path.join(root_dir, "ui")
    venv_dir = os.path.join(root_dir, "venv")

    print_step("Iniciando Local AI Manager...")

    # 1. Configurar Entorno Virtual de Python
    if not os.path.exists(venv_dir):
        print_step("Creando entorno virtual de Python...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

    # Definir el ejecutable de python local del venv
    if platform.system() == "Windows":
        venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
        venv_pip = os.path.join(venv_dir, "Scripts", "pip.exe")
        uvicorn_exe = os.path.join(venv_dir, "Scripts", "uvicorn.exe")
    else:
        venv_python = os.path.join(venv_dir, "bin", "python")
        venv_pip = os.path.join(venv_dir, "bin", "pip")
        uvicorn_exe = os.path.join(venv_dir, "bin", "uvicorn")

    # 2. Instalar dependencias del backend
    print_step("Verificando dependencias del backend...")
    run_cmd([venv_pip, "install", "-r", "requirements.txt", "-q"], cwd=root_dir)

    # 3. Instalar dependencias del frontend si no existen
    node_modules_dir = os.path.join(ui_dir, "node_modules")
    if not os.path.exists(node_modules_dir):
        print_step("Instalando dependencias del frontend (npm install)...")
        # Verify npm exists
        if shutil.which("npm") is None:
            print_error("npm no está instalado. Por favor instala Node.js.")
            sys.exit(1)
        run_cmd(["npm", "install"], cwd=ui_dir)

    # 4. Construir frontend si no existe dist o si el código fuente es más reciente
    dist_dir = os.path.join(ui_dir, "dist")
    if needs_rebuild(ui_dir, dist_dir):
        print_step("Construyendo/Actualizando el frontend (npm run build)...")
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)
        run_cmd(["npm", "run", "build"], cwd=ui_dir)
    else:
        print_step("Frontend al día (dist/ encontrado y sin cambios). Omitiendo build.")

    # 5. Iniciar Backend
    default_port = get_env_var("DEFAULT_PORT", "8000")
    print_step(f"Levantando App unificada (FastAPI sirviendo Frontend y API) en el puerto {default_port}...")

    print_success("========================================")
    print_success("Manager en linea.")
    print_success(f"Aplicacion: http://localhost:{default_port}")
    print_success("========================================")
    print("Presiona Ctrl+C para detener el servicio...")

    try:
        subprocess.run([uvicorn_exe, "api.main:app", "--host", "127.0.0.1", "--port", default_port], cwd=root_dir, check=True)
    except KeyboardInterrupt:
        print("\nServicio detenido por el usuario.")
    except Exception as e:
        print_error(f"Error al levantar el backend: {e}")

if __name__ == "__main__":
    main()
