import os
import json
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import platform
from dotenv import load_dotenv
from api.paths import get_env_path

# Load environment variables to ensure we have the defaults available
load_dotenv(get_env_path())

router = APIRouter()

# Helper to resolve user home directory across platforms
def get_opencode_path():
    system = platform.system()
    if system == "Windows":
        return os.path.expanduser("~\\.config\\opencode\\opencode.json")
    else:
        return os.path.expanduser("~/.config/opencode/opencode.json")

def get_qwencode_path():
    system = platform.system()
    if system == "Windows":
        return os.path.expanduser("~\\.qwen\\settings.json")
    else:
        return os.path.expanduser("~/.qwen/settings.json")

AGENTS_CONFIG = {
    "opencode": {
        "id": "opencode",
        "name": "Opencode",
        "image": "agents/opencode.webp",
        "get_path": get_opencode_path
    },
    "qwencode": {
        "id": "qwencode",
        "name": "QwenCode",
        "image": "agents/qwen.webp",
        "get_path": get_qwencode_path
    }
}

class AgentConfigureRequest(BaseModel):
    agent_id: str
    model_name: str
    endpoint: str

@router.get("/status")
def get_agents_status():
    installed = []
    for agent_id, agent_info in AGENTS_CONFIG.items():
        path = agent_info["get_path"]()
        if os.path.exists(path):
            installed.append({
                "id": agent_info["id"],
                "name": agent_info["name"],
                "image": agent_info["image"]
            })
    return {"installed": installed}

@router.post("/configure")
def configure_agent(req: AgentConfigureRequest):
    if req.agent_id not in AGENTS_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found in registry")
    
    agent = AGENTS_CONFIG[req.agent_id]
    path = agent["get_path"]()
    
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"{agent['name']} config file not found")
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remove trailing commas from JSON to prevent strict parsing errors
            content = re.sub(r',\s*([}\]])', r'\1', content)
            config = json.loads(content)
            
        if req.agent_id == "opencode":
            config["model"] = f"llama.cpp/{req.model_name}"
            
            if "provider" not in config:
                config["provider"] = {}
            if "llama.cpp" not in config["provider"]:
                config["provider"]["llama.cpp"] = {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "Llama.cpp (local)",
                    "options": {},
                    "models": {}
                }
            
            config["provider"]["llama.cpp"]["options"]["baseURL"] = req.endpoint
            if "models" not in config["provider"]["llama.cpp"]:
                config["provider"]["llama.cpp"]["models"] = {}
                
            config["provider"]["llama.cpp"]["models"][req.model_name] = {
                "name": f"{req.model_name} (local)",
                "limit": {
                    "context": int(os.environ.get("DEFAULT_MAX_CONTEXT_TOKENS", 128000)),
                    "output": int(os.environ.get("DEFAULT_MAX_OUTPUT_TOKENS", 65536))
                }
            }
            
        elif req.agent_id == "qwencode":
            # Qwencode structure update
            if "modelProviders" not in config:
                config["modelProviders"] = {}
            if "openai" not in config["modelProviders"]:
                config["modelProviders"]["openai"] = []
                
            # Find the llama.cpp provider entry
            llama_cpp_entry = None
            for entry in config["modelProviders"]["openai"]:
                if entry.get("id") == "llama.cpp":
                    llama_cpp_entry = entry
                    break
                    
            if not llama_cpp_entry:
                llama_cpp_entry = {
                    "id": "llama.cpp",
                    "name": "llama.cpp",
                    "envKey": "LLAMA_CPP_API_KEY",
                    "generationConfig": {
                        "contextWindowSize": int(os.environ.get("DEFAULT_MAX_CONTEXT_TOKENS", 128000))
                    }
                }
                config["modelProviders"]["openai"].append(llama_cpp_entry)
                
            llama_cpp_entry["baseUrl"] = req.endpoint
            
            if "model" not in config:
                config["model"] = {}
            # Setting to llama.cpp or the model name
            config["model"]["name"] = "llama.cpp"
            
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        return {"status": "success", "message": f"{agent['name']} configured successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
