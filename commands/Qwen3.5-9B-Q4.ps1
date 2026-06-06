param(
    [int]$Port = 8080
)

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$RunModelScript = Join-Path $RootDir "scripts\run_model.ps1"

# Suponiendo las rutas estándar por analogía con el 4B
& $RunModelScript `
    -ModelPath "models\Qwen\Qwen3.5-9B\Qwen3.5-9B-UD-Q4_K_XL.gguf" `
    -MmprojPath "models\Qwen\Qwen3.5-9B\mmproj-BF16.gguf" `
    -Alias "Qwen3.5-9B" `
    -CtxSize 32768 `
    -Ngl 99 `
    -Port $Port
