#!/bin/bash
# Script de Bash para ejecutar modelos de llama.cpp localmente

MODEL_PATH=""
ALIAS=""
CTX_SIZE="4096"
NGL="0"
PORT="8080"
EXTRA_ARGS=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --model) MODEL_PATH="$2"; shift ;;
        --alias) ALIAS="$2"; shift ;;
        --ctx-size) CTX_SIZE="$2"; shift ;;
        --ngl) NGL="$2"; shift ;;
        --port) PORT="$2"; shift ;;
        --extra-args) EXTRA_ARGS="$2"; shift ;;
        *) echo "Parámetro desconocido: $1"; exit 1 ;;
    esac
    shift
done

# El CWD está configurado a ~/.llama-forge/ por runner.py
if [ -f ".env" ]; then
    export $(grep -v '^#' ".env" | xargs)
fi

LLAMA_EXE="${LLAMA_SERVER_EXE:-llama-server}"

if ! command -v "$LLAMA_EXE" &> /dev/null && [ ! -f "${LLAMA_BIN_DIR:-}/$LLAMA_EXE" ]; then
    if command -v brew &> /dev/null; then
        echo "Instalando llama.cpp vía brew..."
        brew install llama.cpp
        LLAMA_EXE="llama-server"
    else
        echo "Error: brew no está instalado. Instala Homebrew (https://brew.sh/) antes de continuar."
        exit 1
    fi
fi

HOST_ADDR="${DEFAULT_HOST:-127.0.0.1}"

# Si se pasó extra_args como string único (ej. "-fa on"), no ponerle comillas dobles aquí al evaluar
eval "$LLAMA_EXE \
    -m \"$MODEL_PATH\" \
    -c $CTX_SIZE \
    -ngl $NGL \
    --port $PORT \
    --host $HOST_ADDR $EXTRA_ARGS \
    -a \"$ALIAS\""
