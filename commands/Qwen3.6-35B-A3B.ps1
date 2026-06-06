param(
    [int]$Port = 8080
)

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$RunModelScript = Join-Path $RootDir "scripts\run_model.ps1"

$ExtraArgs = @(
    "-ncmoe", "27",
    "-t", "6",
    "-tb", "8",
    "-np", "1",
    "-b", "512",
    "-ub", "512",
    "-Cr", "0-11",
    "-Crb", "0-11",
    "--cpu-strict", "1",
    "--cpu-strict-batch", "1",
    "--jinja",
    "--prio", "3",
    "--prio-batch", "3",
    "--poll", "100",
    "--poll-batch", "1",
    "--spec-type", "draft-mtp",
    "--spec-draft-n-max", "2",
    "--kv-unified",
    "--no-mmap",
    "--mlock"
)

# Overriding BinDir, CtxSize, Ngl is also needed based on the original bat script
& $RunModelScript `
    -ModelPath "models\Qwen\Qwen3.6-35B-A3B-MTP\Qwen3.6-35B-A3B-MXFP4_MOE.gguf" `
    -Alias "Qwen3.6-35B-A3B" `
    -BinDirOverride "bin\llama-b9297-bin-win-cuda-13.1-x64" `
    -CtxSize 16384 `
    -Ngl 25 `
    -Port $Port `
    -ExtraArgs $ExtraArgs
