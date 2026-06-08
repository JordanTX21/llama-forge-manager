# LlamaForge Manager (Local AI Manager)

LlamaForge (anteriormente tu entorno de `llama.cpp`) es una plataforma completa de orquestación para Modelos de Lenguaje Locales. Incluye un backend inteligente y una interfaz de usuario modular diseñada con una estética minimalista "Apple-like", capaz de gestionar hardware, descargar modelos desde Hugging Face, y enrutar dinámicamente peticiones con `llama-swap`.

Recientemente reconstruido bajo una **arquitectura de puerto único** y soporte para **instalaciones globales (Winget/Homebrew)**.

## Arquitectura

- **Frontend (`ui/`)**: Monolito Modular desarrollado con Vue 3, Composition API, TypeScript, Axios, y TailwindCSS v4. Compilado y servido de forma estática por el backend.
- **Backend (`api/`)**: API REST impulsada por FastAPI y Uvicorn. Actúa como proxy inverso y sirve la SPA de Vue de forma nativa.
- **Orquestación Core**: Binarios oficiales de `llama.cpp` y `llama-server.exe`, gestionados mediante wrappers dinámicos de PowerShell y Bash.
- **Aislamiento de Perfil (`~/.llama-forge/`)**: Todos los modelos, configuraciones (`config.yaml`, `.env`) y comandos auto-generados se guardan en el directorio del usuario para permitir instalaciones de sistema globales de solo lectura.
- **Distribución Standalone**: Soporte para compilación de ejecutables únicos con PyInstaller (`run.py`).

## Mi Hardware

| Componente | Especificación                           |
| ---------- | ---------------------------------------- |
| CPU        | AMD Ryzen 5 7600X (6 cores / 12 threads) |
| GPU        | NVIDIA RTX 3060 12GB VRAM                |
| RAM        | 32GB                                     |

## Características Principales

1. **Dashboard en Tiempo Real**: Visualización de métricas de Hardware en vivo (Nvidia VRAM, CPU y RAM) usando `psutil` y `nvidia-smi`.
2. **Hugging Face Model Hub**: Gestor y descargador de modelos (GGUF) con integración a la librería CLI nativa de HF.
3. **Advanced Settings & Recomendaciones AI**: Editor visual de configuraciones de inferencia con recomendaciones automáticas basadas en tu hardware.
   - Soporte para **Flash Attention**, **Thinking Mode** (Modelos de Razonamiento).
   - Control total de **Sampling** (Temp, Top-P, Min-P, Penalties).
   - Configuración de Hardware: Threads, MoE Cores, Core Ratios, CPU Strict.
   - Parámetros de **Memoria y Caché** (KV Unified, mlock, no-mmap).
4. **Arquitectura de Puerto Único**: Todo se sirve a través de un solo puerto (por defecto 5170), simplificando el uso.

## Requisitos

Si deseas correr el proyecto desde el código fuente para desarrollo:
- **Python 3.10+**
- **Node.js 18+** y `npm`
- **Git**
- (Opcional) **Winget** (Windows) o **Homebrew** (macOS/Linux) para la instalación automatizada de dependencias del sistema como `llama-swap`.

## Instalación y Ejecución

### 1. Entorno de Desarrollo Local

El proyecto cuenta con un orquestador inteligente (`manager.py`) que gestiona entornos virtuales, instala dependencias de Python y Node.js, compila el frontend de Vue dinámicamente si detecta cambios, y levanta el servidor FastAPI.

```powershell
# Clona el repositorio
git clone https://github.com/tu-usuario/llama-forge.git
cd llama-forge

# Inicia el orquestador
python manager.py
```

El orquestador automáticamente:
- Creará la carpeta `venv/` e instalará los paquetes de `requirements.txt`.
- Hará `npm install` y `npm run build` en `ui/` (solo si se detectan cambios en el código fuente).
- Levantará el servidor unificado en el puerto `5170` (o el especificado por `DEFAULT_PORT`).

### 2. Versión Ejecutable (Standalone) / Distribución Global

Si descargas la versión compilada (vía PyInstaller, Winget o Homebrew), simplemente ejecuta el binario de la aplicación.
Toda la configuración se guardará y leerá automáticamente de tu directorio de usuario:
- **Windows**: `C:\Users\TuUsuario\.llama-forge`
- **macOS/Linux**: `~/.llama-forge`

Consulta el documento [docs/DISTRIBUTION.md](docs/DISTRIBUTION.md) para más detalles sobre cómo instalar vía Winget o Homebrew.

## Estructura del Proyecto

```text
C:\llama.cpp
├── api/                  # Backend REST en FastAPI
│   ├── commands.py       # Gestión de comandos y config.yaml maestro
│   ├── hardware.py       # Telemetría de sistema (RAM, GPU)
│   ├── huggingface.py    # Hub de descargas
│   ├── install_utils.py  # Utilidades para Winget/Homebrew
│   ├── main.py           # Entrypoint de FastAPI y Proxy SPA
│   ├── paths.py          # Resolución de rutas dinámicas (~/.llama-forge/)
│   └── runner.py         # Control de procesos
├── docs/                 # Documentación adicional (Distribución)
├── scripts/              # Scripts nativos (.ps1 y .sh)
├── ui/                   # Frontend Monolito Modular (Vue 3)
│   ├── src/              # Código fuente (dashboard, models, settings, i18n)
│   └── dist/             # Build de producción (generado por manager.py)
├── manager.py            # Orquestador de desarrollo local inteligente (auto-build)
├── run.py                # Entrypoint para PyInstaller (Ejecutable standalone)
└── requirements.txt      # Dependencias Python
```

## Modelos que yo utilizo

| Modelo              | Cuantización | Tamaño  | mmproj      | Estado     |
| ------------------- | ------------ | ------- | ----------- | ---------- |
| Qwen3.5-4B          | Q4_K_XL      | 2.9 GB  | 675 MB BF16 | Activo     |
| Qwen3.5-9B          | Q4_K_XL      | 5.9 GB  | 921 MB BF16 | Activo     |
| Qwen3.5-9B-MTP      | Q4_K_XL      | 6.1 GB  | —           | Descargado |
| Qwen3.6-35B-A3B     | IQ2_XXS      | 10.7 GB | 902 MB BF16 | Activo     |
| Qwen3.6-35B-A3B-MTP | MXFP4_MOE    | 22.1 GB | —           | Descargado |

**Nota**: El modelo Qwen3.6-35B-A3B-MTP (22.1 GB) excede la VRAM de 12GB de la RTX 3060, pero está disponible en config para uso con CPU offload.
