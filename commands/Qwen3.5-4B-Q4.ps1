param(
    [int]$Port = 8080
)

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $RootDir

$EnvPath = Join-Path $RootDir ".env"
if (Test-Path $EnvPath) {
    Get-Content $EnvPath | ForEach-Object {
        if ($_ -match '^\s*([^#]+?)\s*=\s*(.*)$') { Set-Item -Path "Env:\$($matches[1])" -Value $matches[2] }
    }
}

$BinDir = if ($env:LLAMA_BIN_DIR) { $env:LLAMA_BIN_DIR } else { "bin\llama-b9037-bin-win-cuda-13.1-x64" }
$ExeName = if ($env:LLAMA_SERVER_EXE) { $env:LLAMA_SERVER_EXE } else { "llama-server.exe" }
$LlamaExe = Join-Path $RootDir (Join-Path $BinDir $ExeName)
$HostAddr = if ($env:DEFAULT_HOST) { $env:DEFAULT_HOST } else { "127.0.0.1" }

& $LlamaExe `
    -m "models\Qwen\Qwen3.5-4B\Qwen3.5-4B-UD-Q4_K_XL.gguf" `
    -c 262144 `
    -ngl 99 `
    --port $Port `
    --host $HostAddr `
    -mm "models\Qwen\Qwen3.5-4B\mmproj-BF16.gguf" `
    --cache-type-k "q8_0" `
    --cache-type-v "q8_0" `
    --temp 0.6 `
    --top-p 0.95 `
    --top-k 20 `
    --min-p 0.0 `
    --presence-penalty 0.0 `
    --repeat-penalty 1.0 `
    -fa on `
    --reasoning on `
    -a "Qwen3.5-4B"
