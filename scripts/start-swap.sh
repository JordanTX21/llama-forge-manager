#!/bin/bash
# Inicia llama-swap usando config.yaml

if ! command -v llama-swap &> /dev/null; then
    if command -v brew &> /dev/null; then
        echo "Instalando llama-swap vía brew..."
        brew tap mostlygeek/llama-swap
        brew install llama-swap
    else
        echo "Error: brew no está instalado. Instala Homebrew (https://brew.sh/) antes de continuar."
        exit 1
    fi
fi

echo "Iniciando llama-swap con config.yaml en el puerto 8080..."
# El entorno virtual (run.py/manager.py) o runner.py configuran el CWD a ~/.llama-forge/

llama-swap --config config.yaml --listen 127.0.0.1:8080
