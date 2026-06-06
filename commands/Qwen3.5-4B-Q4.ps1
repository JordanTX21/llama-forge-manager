param(
    [int]$Port = 8080
)

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$RunModelScript = Join-Path $RootDir "scripts\run_model.ps1"

& $RunModelScript `
    -ModelPath "models\Qwen\Qwen3.5-4B\Qwen3.5-4B-UD-Q4_K_XL.gguf" `
    -MmprojPath "models\Qwen\Qwen3.5-4B\mmproj-BF16.gguf" `
    -Alias "Qwen3.5-4B" `
    -CtxSize 65536 `
    -Ngl 99 `
    -Port $Port
