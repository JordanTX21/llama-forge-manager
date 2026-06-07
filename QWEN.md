# LlamaForge Project Context

## Project Overview

**LlamaForge** is a complete local AI orchestration platform for running and managing large language models (LLMs) locally via `llama.cpp` on Windows. It provides a web-based dashboard for real-time hardware monitoring, model management (Hugging Face GGUF downloads), and inference configuration with `llama-swap` routing.

### Tech Stack

- **Backend**: FastAPI + Uvicorn (Python 3), `requirements.txt`: `huggingface_hub[cli]`, `fastapi`, `uvicorn`, `psutil`
- **Frontend**: Vue 3 + Composition API + TypeScript + Vite + TailwindCSS v4 (`@tailwindcss/vite`)
- **Orchestration**: PowerShell scripts wrapping `llama-server.exe` and `llama-swap`
- **Model Format**: GGUF (Hugging Face), organized as `models/<Author>/<Repo>/<filename>.gguf`

### Architecture

```
api/                  # FastAPI REST backend
├── main.py           # App entrypoint, CORS, router registration
├── hardware.py       # CPU/RAM/GPU metrics (nvidia-smi + psutil)
├── huggingface.py    # Model download + local model listing
├── runner.py         # Start model / start llama-swap
└── commands.py       # Auto-generate .ps1 command files + config.yaml

ui/                   # Vue 3 frontend (Vite dev server)
├── src/
│   ├── components/   # Shared UI components
│   ├── modules/      # Page modules (dashboard, models, settings)
│   ├── router/       # Vue Router config
│   └── services/     # API client (api.service.ts → http://localhost:8000/api)
└── vite.config.ts    # Vue + TailwindCSS v4 plugin, @ → src/ alias

scripts/              # Core PowerShell scripts
├── run_model.ps1     # Launch llama-server with parsed args
└── download_model.ps1# HF model download wrapper

commands/             # Auto-generated .ps1 files (one per saved config)
models/               # Downloaded GGUF files
config.yaml           # Auto-generated llama-swap master config
```

### Three Main Routes

1. `/` — Dashboard (real-time hardware metrics)
2. `/models` — Model Hub (browse, download, list local models)
3. `/settings` — Inference Config (visual editor for llama-server + llama-swap parameters)

## Key Files

| File                             | Purpose                                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `start-manager.ps1`              | Single command to set up venv, install deps, start backend + frontend                                           |
| `start-swap.ps1`                 | Launch `llama-swap --config config.yaml --listen 127.0.0.1:8080`                                                |
| `api/main.py`                    | FastAPI app, CORS, router prefix registration                                                                   |
| `api/commands.py`                | Parse/generate `.ps1` command files and `config.yaml`                                                           |
| `scripts/run_model.ps1`          | Wraps `llama-server.exe` with all inference arguments                                                           |
| `.env.example`                   | Config keys: `LLAMA_BIN_DIR`, `LLAMA_SERVER_EXE`, `DEFAULT_CTX_SIZE`, `DEFAULT_NGL`, `DEFAULT_HOST`, `HF_TOKEN` |
| `ui/src/services/api.service.ts` | HTTP client targeting `http://localhost:8000/api`                                                               |

## Building and Running

```powershell
# Start everything (backend + frontend + venv setup)
.\start-manager.ps1
```

This script:

1. Creates `venv/` if missing, installs `requirements.txt`
2. Runs `npm install` in `ui/` if `node_modules/` is missing
3. Starts FastAPI on `http://127.0.0.1:8000`
4. Starts Vite dev on `http://localhost:5173`
5. Press any key to stop both processes

### Individual Services

```powershell
# Backend only (from venv)
uvicorn api.main:app --host 127.0.0.1 --port 8000

# Frontend only (inside ui/)
npm run dev

# Frontend build
npm run build   # runs vue-tsc -b && vite build

# llama-swap only
.\scripts\start-swap.ps1
```

## API Endpoints

| Method | Endpoint                    | Description                                                 |
| ------ | --------------------------- | ----------------------------------------------------------- |
| GET    | `/api/status`               | Health check                                                |
| GET    | `/api/hardware/`            | CPU/RAM/GPU metrics                                         |
| POST   | `/api/huggingface/download` | Download GGUF model (triggers PowerShell script)            |
| GET    | `/api/huggingface/local`    | List downloaded models                                      |
| GET    | `/api/commands/`            | List all command configs (parses `.ps1` files)              |
| POST   | `/api/commands/`            | Save command config (writes `.ps1` + updates `config.yaml`) |
| POST   | `/api/runner/start`         | Start a model directly via `run_model.ps1`                  |
| POST   | `/api/runner/swap`          | Start llama-swap                                            |

API docs available at `http://localhost:8000/docs`.

## Key Constraints

- **Windows-only**: All orchestration is PowerShell. Scripts use `-ExecutionPolicy Bypass`.
- **`llama-server.exe` path**: Resolved from `.env` (`LLAMA_BIN_DIR`, `LLAMA_SERVER_EXE`) or defaults to `bin\llama-b9037-bin-win-cuda-13.1-x64\llama-server.exe`.
- **`config.yaml`**: Auto-generated by `api/commands.py` (POST `/api/commands/`). Gitignored — do not hand-edit.
- **`commands/*.ps1`**: Auto-generated from the Settings UI. Each wraps `scripts/run_model.ps1` with parsed args.
- **`.env`**: Copy `.env.example` to `.env` to configure. `scripts/run_model.ps1` reads it and exports vars to the process environment.
- **Frontend API client**: Hardcodes `http://localhost:8000/api`. Change for non-local dev.
- **TailwindCSS v4**: Via `@tailwindcss/vite` plugin — no `tailwind.config.js`. Styles written as utility classes directly.

## Generated / Excluded Files

- **Gitignored**: `bin/`, `models/`, `venv/`, `.env`, `config.yaml`
- **Not gitignored but auto-generated**: `commands/` directory
- **Do not commit**: Model files, venv, generated configs, or `.env`

## Environment Variables (.env)

| Key                | Default            | Description                          |
| ------------------ | ------------------ | ------------------------------------ |
| `LLAMA_BIN_DIR`    | (empty)            | Path to llama.cpp binary directory   |
| `LLAMA_SERVER_EXE` | `llama-server.exe` | llama-server executable name         |
| `DEFAULT_CTX_SIZE` | `262144`           | Default context size                 |
| `DEFAULT_NGL`      | `99`               | Default GPU layers                   |
| `DEFAULT_HOST`     | `127.0.0.1`        | Default bind host                    |
| `HF_TOKEN`         | (empty)            | HuggingFace token for private models |
