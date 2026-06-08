param(
    [string]$ModelPath,
    [string]$Alias,
    [int]$CtxSize = 4096,
    [int]$Ngl = 0,
    [int]$Port = 8080,
    [string]$ExtraArgs = ""
)

# El CWD está configurado a ~/.llama-forge/ por runner.py
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^\s*([^#]+?)\s*=\s*(.*)$') { Set-Item -Path "Env:\$($matches[1])" -Value $matches[2] }
    }
}

$ExeName = if ($env:LLAMA_SERVER_EXE) { $env:LLAMA_SERVER_EXE } else { "llama-server.exe" }
$LlamaExe = if ($env:LLAMA_BIN_DIR) { Join-Path $env:LLAMA_BIN_DIR $ExeName } elseif (Get-Command $ExeName -ErrorAction SilentlyContinue) { $ExeName } else { Join-Path "bin" $ExeName }

if (-not (Get-Command $LlamaExe -ErrorAction SilentlyContinue) -and -not (Test-Path $LlamaExe)) {
    if (Get-Command "winget" -ErrorAction SilentlyContinue) {
        Write-Host "Instalando llama.cpp vía winget..."
        winget install llama.cpp
        $LlamaExe = $ExeName # winget puts it in PATH
    } else {
        Write-Host "Error: winget no está instalado."
        exit 1
    }
}

$HostAddr = if ($env:DEFAULT_HOST) { $env:DEFAULT_HOST } else { "127.0.0.1" }

if ($ExtraArgs) {
    Invoke-Expression "& `"$LlamaExe`" -m `"$ModelPath`" -c $CtxSize -ngl $Ngl --port $Port --host $HostAddr -a `"$Alias`" $ExtraArgs"
} else {
    & $LlamaExe -m "$ModelPath" -c $CtxSize -ngl $Ngl --port $Port --host $HostAddr -a "$Alias"
}
