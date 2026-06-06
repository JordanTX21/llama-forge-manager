Write-Host "Iniciando Local AI Manager..." -ForegroundColor Cyan

# 1. Configurar Entorno Virtual de Python
$VenvDir = "venv"
if (-Not (Test-Path -Path $VenvDir)) {
    Write-Host "Creando entorno virtual de Python en .\$VenvDir..." -ForegroundColor Yellow
    python -m venv $VenvDir
}

# 2. Instalar dependencias del backend
Write-Host "Instalando/Verificando dependencias del backend..." -ForegroundColor Yellow
& ".\$VenvDir\Scripts\pip.exe" install -r requirements.txt -q

# 3. Instalar dependencias del frontend si no existen
$NodeModulesDir = "ui\node_modules"
if (-Not (Test-Path -Path $NodeModulesDir)) {
    Write-Host "Instalando dependencias del frontend (npm install)..." -ForegroundColor Yellow
    Set-Location -Path "ui"
    npm install
    Set-Location -Path ".."
}

# 4. Iniciar Backend
Write-Host "Levantando Backend (FastAPI en puerto 8000)..." -ForegroundColor Yellow
$BackendProcess = Start-Process -FilePath ".\$VenvDir\Scripts\uvicorn.exe" -ArgumentList "api.main:app --host 127.0.0.1 --port 8000" -PassThru -NoNewWindow

# 5. Iniciar Frontend
Write-Host "Levantando Frontend (Vue 3 en puerto 5173)..." -ForegroundColor Yellow
$FrontendProcess = Start-Process -FilePath "npm.cmd" -ArgumentList "run dev --prefix ./ui" -PassThru -NoNewWindow

Write-Host "========================================" -ForegroundColor Green
Write-Host "Manager en linea." -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "Presiona cualquier tecla para detener ambos servicios..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "Deteniendo servicios..." -ForegroundColor Yellow
Stop-Process -Id $BackendProcess.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $FrontendProcess.Id -Force -ErrorAction SilentlyContinue
Write-Host "Servicios detenidos." -ForegroundColor Red
