param(
    [Parameter(Mandatory=$true)]
    [string]$ModelPath,
    [Parameter(Mandatory=$true)]
    [string]$Alias,
    [string]$MmprojPath = "",
    [int]$Port = 8080,
    [Parameter(Mandatory=$true)]
    [int]$CtxSize,
    [Parameter(Mandatory=$true)]
    [int]$Ngl,
    [switch]$FlashAttention,
    [switch]$Thinking,
    
    # Threads & Compute
    [int]$Threads = -1,
    [int]$ThreadsBatch = -1,
    [int]$Np = -1,
    [string]$Cr = "",
    [string]$Crb = "",
    [switch]$CpuStrict,
    [switch]$CpuStrictBatch,
    
    # Batching
    [int]$BatchSize = -1,
    [int]$UbatchSize = -1,
    [int]$Prio = -1,
    [int]$PrioBatch = -1,
    [int]$Poll = -1,
    [int]$PollBatch = -1,

    # Memory & Cache
    [string]$CacheTypeK = "q8_0",
    [string]$CacheTypeV = "q8_0",
    [switch]$KvUnified,
    [switch]$NoMmap,
    [switch]$Mlock,
    
    # MoE & Speculative
    [int]$NcMoe = -1,
    [string]$SpecType = "",
    [int]$SpecDraftNMax = -1,

    # Sampling
    [float]$Temp = 0.6,
    [float]$TopP = 0.95,
    [int]$TopK = 20,
    [float]$MinP = 0.0,
    [float]$PresencePenalty = 0.0,
    [float]$RepeatPenalty = 1.0,

    # Misc
    [switch]$Jinja,

    [string]$BinDirOverride = "",
    [string[]]$ExtraArgs = @()
)

$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$EnvPath = Join-Path $RootDir ".env"

if (Test-Path $EnvPath) {
    Get-Content $EnvPath | ForEach-Object {
        if ($_ -match '^\s*([^#]+?)\s*=\s*(.*)$') {
            Set-Item -Path "Env:\$($matches[1])" -Value $matches[2]
        }
    }
}

if ($BinDirOverride) {
    $BinDir = $BinDirOverride
} else {
    $BinDir = if ($env:LLAMA_BIN_DIR) { $env:LLAMA_BIN_DIR } else { "bin\llama-b9037-bin-win-cuda-13.1-x64" }
}

$ExeName = if ($env:LLAMA_SERVER_EXE) { $env:LLAMA_SERVER_EXE } else { "llama-server.exe" }
$HostAddr = if ($env:DEFAULT_HOST) { $env:DEFAULT_HOST } else { "127.0.0.1" }

$LlamaExe = Join-Path $RootDir (Join-Path $BinDir $ExeName)
$FullModelPath = Join-Path $RootDir $ModelPath

$RunArgs = @(
    "-m", $FullModelPath,
    "-c", $CtxSize,
    "-ngl", $Ngl,
    "--cache-type-k", $CacheTypeK,
    "--cache-type-v", $CacheTypeV,
    "--temp", $Temp,
    "--top-p", $TopP,
    "--top-k", $TopK,
    "--min-p", $MinP,
    "--presence-penalty", $PresencePenalty,
    "--repeat-penalty", $RepeatPenalty,
    "--host", $HostAddr,
    "--port", $Port,
    "-a", $Alias
)

# Conditional Injections
if ($Threads -gt 0) { $RunArgs += "-t"; $RunArgs += $Threads }
if ($ThreadsBatch -gt 0) { $RunArgs += "-tb"; $RunArgs += $ThreadsBatch }
if ($Np -gt 0) { $RunArgs += "-np"; $RunArgs += $Np }
if ($Cr) { $RunArgs += "-Cr"; $RunArgs += $Cr }
if ($Crb) { $RunArgs += "-Crb"; $RunArgs += $Crb }
if ($CpuStrict) { $RunArgs += "--cpu-strict"; $RunArgs += "1" }
if ($CpuStrictBatch) { $RunArgs += "--cpu-strict-batch"; $RunArgs += "1" }

if ($BatchSize -gt 0) { $RunArgs += "-b"; $RunArgs += $BatchSize }
if ($UbatchSize -gt 0) { $RunArgs += "-ub"; $RunArgs += $UbatchSize }
if ($Prio -ge 0) { $RunArgs += "--prio"; $RunArgs += $Prio }
if ($PrioBatch -ge 0) { $RunArgs += "--prio-batch"; $RunArgs += $PrioBatch }
if ($Poll -ge 0) { $RunArgs += "--poll"; $RunArgs += $Poll }
if ($PollBatch -ge 0) { $RunArgs += "--poll-batch"; $RunArgs += $PollBatch }

if ($KvUnified) { $RunArgs += "--kv-unified" }
if ($NoMmap) { $RunArgs += "--no-mmap" }
if ($Mlock) { $RunArgs += "--mlock" }

if ($NcMoe -gt 0) { $RunArgs += "-ncmoe"; $RunArgs += $NcMoe }
if ($SpecType) { $RunArgs += "--spec-type"; $RunArgs += $SpecType }
if ($SpecDraftNMax -gt 0) { $RunArgs += "--spec-draft-n-max"; $RunArgs += $SpecDraftNMax }

if ($Jinja) { $RunArgs += "--jinja" }

if ($Thinking) {
    $RunArgs += "--reasoning"
    $RunArgs += "on"
}

if ($FlashAttention) {
    $RunArgs += "-fa"
    $RunArgs += "on"
}

if ($MmprojPath) {
    $FullMmprojPath = Join-Path $RootDir $MmprojPath
    $RunArgs += "-mm", $FullMmprojPath
}

if ($ExtraArgs.Count -gt 0) {
    $RunArgs += $ExtraArgs
}

Write-Host "Running llama-server for model $Alias on port $Port"
Write-Host "Executable: $LlamaExe"

& $LlamaExe @RunArgs
