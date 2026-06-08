param(
    [Parameter(Mandatory=$true)]
    [string]$RepoId,
    [Parameter(Mandatory=$true)]
    [string]$Filename,
    [string]$LocalDir = ""
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

if ([string]::IsNullOrEmpty($LocalDir)) {
    # Extraer nombre del modelo (ej: Qwen/Qwen2.5-7B -> Qwen2.5-7B)
    $Parts = $RepoId -split '/'
    $RepoName = if ($Parts.Count -gt 1) { $Parts[1] } else { $Parts[0] }
    
    # Podemos también usar la estructura autor/modelo si preferimos
    $Author = if ($Parts.Count -gt 1) { $Parts[0] } else { "Uncategorized" }
    
    $LocalDir = "models\$Author\$RepoName"
}

$FullLocalDir = if ([System.IO.Path]::IsPathRooted($LocalDir)) { $LocalDir } else { Join-Path $RootDir $LocalDir }

Write-Host "Downloading $Filename from $RepoId to $FullLocalDir..."

$RunArgs = @(
    "download",
    $RepoId,
    $Filename,
    "--local-dir", $FullLocalDir,
    "--local-dir-use-symlinks", "False"
)

if ($env:HF_TOKEN) {
    $RunArgs += "--token", $env:HF_TOKEN
}

& huggingface-cli @RunArgs

Write-Host "Download complete! Saved in $FullLocalDir"
