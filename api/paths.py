import os
import sys
from pathlib import Path

def get_base_dir() -> str:
    """Returns the base directory of the application. Handles PyInstaller _MEIPASS."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_user_data_dir() -> str:
    """Returns the user-specific data directory for llama-forge."""
    home = str(Path.home())
    data_dir = os.path.join(home, ".llama-forge")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_commands_dir() -> str:
    commands_dir = os.path.join(get_user_data_dir(), "commands")
    os.makedirs(commands_dir, exist_ok=True)
    return commands_dir

def get_models_dir() -> str:
    models_dir = os.path.join(get_user_data_dir(), "models")
    os.makedirs(models_dir, exist_ok=True)
    return models_dir

def get_config_yaml_path() -> str:
    return os.path.join(get_user_data_dir(), "config.yaml")

def get_env_path() -> str:
    return os.path.join(get_user_data_dir(), ".env")

def get_bin_dir() -> str:
    """Returns the local bin dir relative to the user data dir or base dir."""
    bin_dir = os.path.join(get_user_data_dir(), "bin")
    os.makedirs(bin_dir, exist_ok=True)
    return bin_dir
