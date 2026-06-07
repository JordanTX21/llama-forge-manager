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
    -m "models\Qwen\Qwen3.6-35B-A3B\Qwen3.6-35B-A3B-UD-IQ2_XXS.gguf" `
    -c 128000 `
    -ngl 999 `
    --port $Port `
    --host $HostAddr `
    -mm "models\Qwen\Qwen3.6-35B-A3B\mmproj-BF16.gguf" `
    -t 6 `
    -tb 8 `
    -np 1 `
    -Cr 0-11 `
    -Crb 0-11 `
    --cpu-strict 1 `
    --cpu-strict-batch 1 `
    -b 512 `
    -ub 512 `
    --prio 3 `
    --prio-batch 3 `
    --poll 100 `
    --poll-batch 1 `
    --cache-type-k "q4_0" `
    --cache-type-v "q4_0" `
    --no-mmap `
    --temp 0.6 `
    --top-p 0.95 `
    --top-k 20 `
    --min-p 0.0 `
    --presence-penalty 0.0 `
    --repeat-penalty 1.0 `
    --jinja `
    -fa on `
    --reasoning on `
    -a "Qwen3.6-35B-A3B"
