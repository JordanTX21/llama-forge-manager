#!/bin/bash

# Default values
REPO_ID=""
FILENAME=""
LOCAL_DIR=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --repo-id) REPO_ID="$2"; shift ;;
        --filename) FILENAME="$2"; shift ;;
        --local-dir) LOCAL_DIR="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$REPO_ID" ] || [ -z "$FILENAME" ]; then
    echo "Usage: $0 --repo-id <repo> --filename <file> [--local-dir <dir>]"
    exit 1
fi

# Load .env if exists
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$ROOT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
    # Load .env safely ignoring comments
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Compute LocalDir if not provided
if [ -z "$LOCAL_DIR" ]; then
    if [[ "$REPO_ID" == *"/"* ]]; then
        AUTHOR=$(echo "$REPO_ID" | cut -d'/' -f1)
        REPONAME=$(echo "$REPO_ID" | cut -d'/' -f2)
    else
        AUTHOR="Uncategorized"
        REPONAME="$REPO_ID"
    fi
    LOCAL_DIR="$ROOT_DIR/models/$AUTHOR/$REPONAME"
fi

# We don't prepend ROOT_DIR if LOCAL_DIR is absolute (starts with /)
if [[ "$LOCAL_DIR" != /* ]]; then
    LOCAL_DIR="$ROOT_DIR/$LOCAL_DIR"
fi

echo "Downloading $FILENAME from $REPO_ID to $LOCAL_DIR..."

CMD_ARGS=("download" "$REPO_ID" "$FILENAME" "--local-dir" "$LOCAL_DIR" "--local-dir-use-symlinks" "False")

if [ -n "$HF_TOKEN" ]; then
    CMD_ARGS+=("--token" "$HF_TOKEN")
fi

huggingface-cli "${CMD_ARGS[@]}"

echo "Download complete! Saved in $LOCAL_DIR"
