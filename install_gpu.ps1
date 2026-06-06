$ErrorActionPreference = "Stop"

$appDir = $PSScriptRoot
$venvDir = Join-Path $appDir ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$python312Url = "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"
$pythonInstaller = Join-Path $env:TEMP "python-3.12.10-amd64.exe"

function Test-RealPython {
    param([string]$Path)

    if (-not $Path) { return $false }
    if (-not (Test-Path $Path)) { return $false }
    if ($Path -like "*\Microsoft\WindowsApps\*") { return $false }

    try {
        $version = & $Path -c "import sys; print(sys.version_info[:2] >= (3, 10) and sys.version_info[:2] <= (3, 12))" 2>$null
        return ($LASTEXITCODE -eq 0 -and $version -match "True")
    } catch {
        return $false
    }
}

function Find-Python {
    $candidates = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python310\python.exe")
    )

    foreach ($candidate in $candidates) {
        if (Test-RealPython $candidate) { return $candidate }
    }

    $command = Get-Command python -ErrorAction SilentlyContinue
    if ($command -and (Test-RealPython $command.Source)) { return $command.Source }

    return $null
}

function Install-UserPython {
    Write-Host "Python 3.10-3.12 was not found. Installing Python 3.12 for this user..."

    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        & $winget.Source install --id Python.Python.3.12 --exact --source winget --scope user --accept-package-agreements --accept-source-agreements
        $pythonPath = Find-Python
        if ($pythonPath) { return $pythonPath }
        Write-Host "Winget did not expose Python immediately. Trying direct Python installer..."
    }

    if (-not (Test-Path $pythonInstaller)) {
        Write-Host "Downloading Python installer..."
        Invoke-WebRequest -Uri $python312Url -OutFile $pythonInstaller
    }

    Write-Host "Running Python installer..."
    $process = Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_tcltk=1 Include_launcher=0" -Wait -PassThru
    if ($process.ExitCode -ne 0) {
        throw "Python installer failed with exit code $($process.ExitCode)."
    }

    $pythonPath = Find-Python
    if (-not $pythonPath) {
        throw "Python installation finished, but Python could not be found. Restart Windows or install Python 3.12 manually from python.org."
    }
    return $pythonPath
}

Write-Host "Preparing DLSS-like super-resolution environment..."

$basePython = Find-Python
if (-not $basePython) {
    $basePython = Install-UserPython
}

Write-Host "Using base Python: $basePython"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating local runtime environment: $venvDir"
    & $basePython -m venv $venvDir
}

if (-not (Test-Path $venvPython)) {
    throw "The local Python environment was not created correctly."
}

Write-Host "Installing GPU dependencies. This can take a while because PyTorch is large..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
& $venvPython -m pip install -r (Join-Path $appDir "requirements.txt")

Write-Host ""
Write-Host "Checking CUDA..."
& $venvPython -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'not found')"

Write-Host ""
Write-Host "Done. You can now double-click 打开超分工具.bat to open the tool."
