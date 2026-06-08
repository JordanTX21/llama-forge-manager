import platform
import shutil
import subprocess

def get_os():
    return platform.system()

def _run_cmd(cmd: list, error_msg: str):
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"{error_msg}. Detalles del error: {e.stderr.strip() or e.stdout.strip()}")
    except FileNotFoundError:
        executable = cmd[0]
        if executable == "winget":
            raise RuntimeError(f"No se pudo encontrar '{executable}'. Por favor, instala App Installer desde la Microsoft Store para obtener winget.")
        elif executable == "brew":
            raise RuntimeError(f"No se pudo encontrar '{executable}'. Por favor, instala Homebrew (https://brew.sh/) antes de continuar.")
        else:
            raise RuntimeError(f"El ejecutable '{executable}' no está disponible o no se encuentra en el PATH.")

def ensure_llama_swap():
    """Valida si llama-swap está instalado; si no, lo instala según el OS."""
    if shutil.which("llama-swap") is not None:
        return

    current_os = get_os()
    if current_os == "Windows":
        _run_cmd(
            ["winget", "install", "llama-swap"],
            "Error al intentar instalar llama-swap usando winget"
        )
    elif current_os in ["Linux", "Darwin"]:
        _run_cmd(
            ["brew", "tap", "mostlygeek/llama-swap"],
            "Error al añadir el repositorio (tap) de llama-swap a brew"
        )
        _run_cmd(
            ["brew", "install", "llama-swap"],
            "Error al instalar llama-swap usando brew"
        )
    else:
        raise RuntimeError(f"Sistema operativo no soportado para instalación automática: {current_os}")

def ensure_llama_cpp():
    """Valida si llama-server está instalado; si no, lo instala según el OS."""
    if shutil.which("llama-server") is not None or shutil.which("llama-server.exe") is not None:
        return
        
    current_os = get_os()
    if current_os == "Windows":
        _run_cmd(
            ["winget", "install", "llama.cpp"],
            "Error al intentar instalar llama.cpp usando winget"
        )
    elif current_os in ["Linux", "Darwin"]:
        _run_cmd(
            ["brew", "install", "llama.cpp"],
            "Error al intentar instalar llama.cpp usando brew"
        )
    else:
        raise RuntimeError(f"Sistema operativo no soportado para instalación automática: {current_os}")
