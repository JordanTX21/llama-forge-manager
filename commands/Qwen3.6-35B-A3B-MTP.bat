@echo off
setlocal

set PORT_ARG=%1
if "%PORT_ARG%"=="" set PORT_ARG=8080

set SCRIPT_DIR=%~dp0
:: 1. FORZAR EL DIRECTORIO DE TRABAJO A LA CARPETA DEL SCRIPT
cd /d "%SCRIPT_DIR%"

set ROOT=%SCRIPT_DIR%..

:: 2. Ahora las rutas relativas funcionarán perfectamente siempre
..\bin\llama-b9297-bin-win-cuda-13.1-x64\llama-server.exe ^
-m ..\models\Qwen\Qwen3.6-35B-A3B-MTP\Qwen3.6-35B-A3B-MXFP4_MOE.gguf ^
-c 128000 ^
-ngl 999 ^
-ncmoe 27 ^
-fa on ^
-t 6 ^
-tb 8 ^
-np 1 ^
-b 512 ^
-ub 512 ^
-Cr 0-11 ^
-Crb 0-11 ^
--cpu-strict 1 ^
--cpu-strict-batch 1 ^
--jinja ^
--reasoning on ^
--cache-type-k q4_0 ^
--cache-type-v q4_0 ^
--prio 3 ^
--prio-batch 3 ^
--poll 100 ^
--poll-batch 1 ^
--spec-type draft-mtp ^
--spec-draft-n-max 2 ^
--temp 0.6 ^
--top-p 0.95 ^
--top-k 20 ^
--min-p 0.0 ^
--presence-penalty 0.0 ^
--repeat-penalty 1.0 ^
--no-mmap ^
--host 127.0.0.1 ^
--port %PORT_ARG% ^
-a Qwen3.6-35B-A3B