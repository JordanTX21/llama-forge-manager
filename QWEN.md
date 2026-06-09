# LlamaForge Project Context

## Project Overview

**LlamaForge** is a complete local AI orchestration platform for running and managing large language models (LLMs) locally via `llama.cpp` on Windows. It provides a web-based dashboard for real-time hardware monitoring, model management (Hugging Face GGUF downloads), and inference configuration with `llama-swap` routing.

The application uses a **single-port architecture** where the FastAPI backend serves as a reverse proxy, compiling and serving the Vue 3 frontend statically. User data (models, configs, commands) is isolated in `~/.llama-forge/` to support global installations.

### Tech Stack

- **Backend**: FastAPI + Uvicorn (Python 3), `requirements.txt`: `huggingface_hub[cli]`, `fastapi`, `uvicorn`, `psutil`, `httpx`, `pyyaml`, `python-dotenv`
- **Frontend**: Vue 3 + Composition API + TypeScript + Vite + TailwindCSS v4 (`@tailwindcss/vite`)
- **Orchestration**: PowerShell scripts (`.ps1`) and Bash scripts (`.sh`) wrapping `llama-server.exe`
- **Model Format**: GGUF (Hugging Face), organized as `models/<Author>/<Repo>/<filename>.gguf`
- **Distribution**: Standalone executable via PyInstaller (`run.py`)

### Architecture

```
api/                  # FastAPI REST backend
├── main.py           # App entrypoint, CORS, SPA proxy, router registration
├── hardware.py       # CPU/RAM/GPU metrics (nvidia-smi + psutil)
├── huggingface.py    # Model download + local model listing
├── runner.py         # Start model / start llama-swap
├── commands.py       # Parse/generate command scripts + config.yaml
├── recommend.py      # AI-based inference config recommendations
├── agents.py         # Code agent integration (Opencode, QwenCode)
└── paths.py          # Dynamic path resolution (~/.llama-forge/)

ui/                   # Vue 3 frontend (Vite → dist/)
├── src/
│   ├── components/   # Shared UI components
│   ├── composables/  # Vue composables (reactive utilities)
│   ├── modules/      # Page modules (dashboard, models, settings)
│   ├── router/       # Vue Router config
│   ├── services/     # API client (http client)
│   ├── stores/       # Pinia stores
│   └── i18n/         # Internationalization
└── vite.config.ts    # Vue + TailwindCSS v4 plugin, @ → ui/src/ alias

scripts/              # Core orchestration scripts
├── run_model.ps1/.sh # Launch llama-server with parsed args
└── start-swap.ps1/.sh # Launch llama-swap

manager.py            # Dev orchestrator (auto-build, venv, unified port)
run.py                # PyInstaller standalone entrypoint
```

### User Data Isolation

All user-specific data is stored in `~/.llama-forge/`:

- **Windows**: `C:\Users\<User>\.llama-forge\`
- **macOS/Linux**: `~/.llama-forge/`

Contents:

- `config.yaml` — llama-swap master config (auto-generated, do not hand-edit)
- `.env` — Environment variables copied from `.env.example`
- `commands/` — Auto-generated `.ps1`/`.sh` scripts
- `models/` — Downloaded GGUF files
- `bin/` — llama.cpp binaries

### Three Main Routes

1. `/` — Dashboard (real-time hardware metrics)
2. `/models` — Model Hub (browse, download, list local models)
3. `/settings` — Inference Config (visual editor for llama-server + llama-swap parameters)

## Key Files

| File                    | Purpose                                                                                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `manager.py`            | Dev orchestrator: creates venv, installs deps, auto-builds frontend, starts unified server on port 5170 (or `DEFAULT_PORT`)     |
| `run.py`                | Standalone entrypoint for PyInstaller builds; reads `DEFAULT_PORT` from `~/.llama-forge/.env`                                   |
| `api/main.py`           | FastAPI app, CORS, SPA catch-all proxy, router registration                                                                     |
| `api/paths.py`          | Path resolution utilities; `get_user_data_dir()`, `get_commands_dir()`, `get_models_dir()`, etc.                                |
| `api/commands.py`       | Parse/generate `.ps1`/`.sh` command files and `config.yaml`                                                                     |
| `api/agents.py`         | Code agent integration (Opencode, QwenCode) — configure model endpoints                                                         |
| `api/recommend.py`      | AI-based inference parameter recommendations based on hardware                                                                  |
| `scripts/run_model.ps1` | Wraps `llama-server.exe` with all inference arguments                                                                           |
| `.env.example`          | Config keys: `LLAMA_BIN_DIR`, `LLAMA_SERVER_EXE`, `DEFAULT_CTX_SIZE`, `DEFAULT_NGL`, `DEFAULT_HOST`, `HF_TOKEN`, `DEFAULT_PORT` |
| `ui/vite.config.ts`     | Vue + TailwindCSS v4 plugin config                                                                                              |
| `ui/src/services/`      | HTTP client targeting backend API                                                                                               |

## Building and Running

### Development Mode

```powershell
# Start everything (backend + frontend + auto-build)
python manager.py
```

`manager.py` does:

1. Creates `venv/` if missing, installs `requirements.txt`
2. Runs `npm install` in `ui/` if `node_modules/` is missing
3. Auto-builds frontend (`npm run build`) only when source changes detected
4. Starts FastAPI serving API + compiled frontend on single port (default `5170` or `DEFAULT_PORT` from `.env`)

### Standalone Distribution

```python
# Build with PyInstaller
python run.py
```

`run.py` reads `DEFAULT_PORT` from `~/.llama-forge/.env`, copies `.env.example` to `~/.llama-forge/.env` if missing, and starts the app.

### Individual Services

```powershell
# Backend only (from venv)
uvicorn api.main:app --host 127.0.0.1 --port 8000

# Frontend only (inside ui/)
npm run dev

# Frontend build
npm run build   # runs vue-tsc -b && vite build
```

## API Endpoints

| Method | Endpoint                    | Description                                                       |
| ------ | --------------------------- | ----------------------------------------------------------------- |
| GET    | `/api/status`               | Health check                                                      |
| GET    | `/api/hardware/`            | CPU/RAM/GPU metrics (uses `nvidia-smi` + `psutil`)                |
| POST   | `/api/huggingface/download` | Download GGUF model (triggers PowerShell script)                  |
| GET    | `/api/huggingface/local`    | List downloaded models                                            |
| GET    | `/api/commands/`            | List all command configs (parses `.ps1`/`.sh` files)              |
| POST   | `/api/commands/`            | Save command config (writes `.ps1`/`.sh` + updates `config.yaml`) |
| POST   | `/api/runner/start`         | Start a model directly via `run_model.ps1`                        |
| POST   | `/api/runner/swap`          | Start llama-swap                                                  |
| GET    | `/api/recommend/`           | AI-based inference parameter recommendations                      |
| GET    | `/api/agents/status`        | Check installed code agents (Opencode, QwenCode)                  |
| POST   | `/api/agents/configure`     | Configure agent model endpoint                                    |

API docs available at `http://localhost:8000/docs`.

## Environment Variables (.env)

| Key                          | Default            | Description                           |
| ---------------------------- | ------------------ | ------------------------------------- |
| `LLAMA_BIN_DIR`              | (empty)            | Path to llama.cpp binary directory    |
| `LLAMA_SERVER_EXE`           | `llama-server.exe` | llama-server executable name          |
| `DEFAULT_CTX_SIZE`           | `262144`           | Default context size                  |
| `DEFAULT_NGL`                | `99`               | Default GPU layers                    |
| `DEFAULT_HOST`               | `127.0.0.1`        | Default bind host                     |
| `HF_TOKEN`                   | (empty)            | HuggingFace token for private models  |
| `DEFAULT_PORT`               | `5170`             | Unified server port (dev mode)        |
| `DEFAULT_MAX_CONTEXT_TOKENS` | `128000`           | Default max context tokens for agents |
| `DEFAULT_MAX_OUTPUT_TOKENS`  | `65536`            | Default max output tokens for agents  |

## Development Conventions

- **Backend**: Python typing, Pydantic models for request/response validation, regex-based parsing for PowerShell scripts
- **Frontend**: Vue 3 Composition API with `<script setup>`, TypeScript, TailwindCSS utility classes (v4, no config file)
- **Orchestration**: PowerShell on Windows, Bash on macOS/Linux; scripts read `.env` and export vars to process environment
- **Path Resolution**: All user data isolated in `~/.llama-forge/` via `api/paths.py` utilities
- **Auto-generation**: `commands/*.ps1` and `config.yaml` are auto-generated — do not hand-edit

## Generated / Excluded Files

- **Gitignored**: `bin/`, `models/`, `venv/`, `.env`, `config.yaml`, `commands/`, `ui/dist/`
- **Not gitignored but auto-generated**: `commands/` directory
- **Do not commit**: Model files, venv, generated configs, `.env`, or build artifacts

## Hardware Context (User's Machine)

| Component | Specification                            |
| --------- | ---------------------------------------- |
| CPU       | AMD Ryzen 5 7600X (6 cores / 12 threads) |
| GPU       | NVIDIA RTX 3060 12GB VRAM                |
| RAM       | 32GB                                     |

## Active Models

| Model               | Quantization | Size    | mmproj      | Status     |
| ------------------- | ------------ | ------- | ----------- | ---------- |
| Qwen3.5-4B          | Q4_K_XL      | 2.9 GB  | 675 MB BF16 | Active     |
| Qwen3.5-9B          | Q4_K_XL      | 5.9 GB  | 921 MB BF16 | Active     |
| Qwen3.5-9B-MTP      | Q4_K_XL      | 6.1 GB  | —           | Downloaded |
| Qwen3.6-35B-A3B     | IQ2_XXS      | 10.7 GB | 902 MB BF16 | Active     |
| Qwen3.6-35B-A3B-MTP | MXFP4_MOE    | 22.1 GB | —           | Downloaded |

Note: Qwen3.6-35B-A3B-MTP (22.1 GB) exceeds 12GB VRAM but is available for CPU offload.
