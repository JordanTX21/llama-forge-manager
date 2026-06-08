# Inicia llama-swap usando config.yaml

if (-not (Get-Command "llama-swap" -ErrorAction SilentlyContinue)) {
    if (Get-Command "winget" -ErrorAction SilentlyContinue) {
        Write-Host "Instalando llama-swap vía winget..."
        winget install llama-swap
    } else {
        Write-Host "Error: winget no está instalado. Por favor instala App Installer desde la Microsoft Store para obtener winget."
        exit 1
    }
}

Write-Host "Iniciando llama-swap con config.yaml en el puerto 8080..."
llama-swap --config config.yaml --listen 127.0.0.1:8080
