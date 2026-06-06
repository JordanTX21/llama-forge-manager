# LlamaForge Manager (Local AI Manager)

LlamaForge (anteriormente tu entorno de `llama.cpp`) es una plataforma completa de orquestación para Modelos de Lenguaje Locales. Incluye un backend inteligente y una interfaz de usuario modular diseñada con una estética minimalista "Apple-like", capaz de gestionar hardware, descargar modelos desde Hugging Face, y enrutar dinámicamente peticiones con `llama-swap`.

## Arquitectura

- **Frontend (`ui/`)**: Monolito Modular desarrollado con Vue 3, Composition API, TypeScript, Axios, y TailwindCSS v4.
- **Backend (`api/`)**: API REST impulsada por FastAPI y Uvicorn.
- **Orquestación Core**: Binarios oficiales de `llama.cpp` y `llama-server.exe`, gestionados mediante wrappers dinámicos de PowerShell (`run_model.ps1`, `start-swap.ps1`).

## Características Principales

1. **Dashboard en Tiempo Real**: Visualización de métricas de Hardware en vivo (Nvidia VRAM, CPU y RAM) usando `psutil` y `nvidia-smi`.
2. **Hugging Face Model Hub**: Gestor y descargador de modelos (GGUF) con integración a la librería CLI nativa de HF. 
3. **Advanced Settings & Llama-Swap**: Editor visual completo de configuraciones de inferencia:
   - Soporte para **Flash Attention**, **Thinking Mode** (Modelos de Razonamiento).
   - Control total de **Sampling** (Temp, Top-P, Min-P, Penalties).
   - Configuración de Hardware: Threads, MoE Cores, Core Ratios, CPU Strict.
   - Parámetros de **Memoria y Caché** (KV Unified, mlock, no-mmap).
   Los cambios se inyectan dinámicamente en los archivos `.ps1` y en el `config.yaml` maestro de llama-swap.
4. **Instalación de un Clic**: Gestor automático (`start-manager.ps1`) que crea el entorno virtual `venv`, instala las dependencias de Python y Node.js, e inicia todos los servidores.

## Instalación y Ejecución

Simplemente ejecuta el orquestador principal:

```powershell
.\start-manager.ps1
```

Este script automáticamente:
- Creará la carpeta `venv/` e instalará los paquetes de `requirements.txt`.
- Hará `npm install` dentro de la carpeta `ui/`.
- Levantará FastAPI en `http://localhost:8000`.
- Levantará Vue Vite en `http://localhost:5173`.

## Estructura del Proyecto

```text
C:\llama.cpp
├── api/                  # Backend REST en FastAPI
│   ├── commands.py       # Serialización y parseo de PowerShell y YAML (Config Avanzada)
│   ├── hardware.py       # Telemetría de sistema (RAM, GPU)
│   ├── huggingface.py    # Hub de descargas locales
│   └── runner.py         # Control de procesos
├── commands/             # Archivos auto-generados .ps1 por configuración
├── models/               # Archivos GGUF descargados organizados por Autor/Repo
├── scripts/              # Scripts nativos (run_model con soporte dinámico avanzado)
├── ui/                   # Frontend Monolito Modular
│   ├── src/modules/      # (dashboard, models, settings)
│   └── src/services/     # api.service.ts
├── config.yaml           # Configuración maestra para llama-swap (Auto-Generado)
├── requirements.txt      # Dependencias Python
└── start-manager.ps1     # Comando unificado de inicio
```
