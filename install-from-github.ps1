param(
    [string]$InstallDir = (Join-Path $env:LOCALAPPDATA "Programs\ImageSuperResolutionTool"),
    [string]$WorkDir = (Join-Path $env:TEMP "ImageSuperResolutionToolInstall"),
    [switch]$SkipShortcut,
    [switch]$KeepDownloads,
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$repo = "qwertasdfg77/image-super-resolution-tool"
$tag = "v1.0.0"
$releaseBase = "https://github.com/$repo/releases/download/$tag"
$zipName = "image-super-resolution-tool-full.zip"
$packageRoot = "image-super-resolution-tool"
$expectedZipHash = "8CF07431598A6D9058689D912821887745CF10BC41F4F464F13054214F15E60B"

$assets = @(
    @{
        Name = "image-super-resolution-tool-full.zip.001"
        Hash = "052FA9C8EBDF4A6B9A56392B8A08EEFBBABC530748EA9C1536C747485173C125"
    },
    @{
        Name = "image-super-resolution-tool-full.zip.002"
        Hash = "0F1311455BC3C82F9BCD1F554B555EE66FEAC3566ABFF07E3011AE445566EFA6"
    }
)

function Write-Step([string]$Message) {
    Write-Host ""
    Write-Host "== $Message =="
}

function Get-Hash([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToUpperInvariant()
}

function Test-RemoteAsset([string]$Url) {
    $request = [System.Net.HttpWebRequest]::Create($Url)
    $request.Method = "HEAD"
    $request.AllowAutoRedirect = $true
    $response = $request.GetResponse()
    try {
        if ([int]$response.StatusCode -lt 200 -or [int]$response.StatusCode -gt 399) {
            throw "Remote asset is not available: $Url"
        }
    } finally {
        $response.Dispose()
    }
}

function Download-Asset([string]$Name, [string]$ExpectedHash, [string]$Destination) {
    $url = "$releaseBase/$Name"
    if (Test-Path -LiteralPath $Destination) {
        $existingHash = Get-Hash $Destination
        if ($existingHash -eq $ExpectedHash) {
            Write-Host "Already downloaded: $Name"
            return
        }
        Remove-Item -LiteralPath $Destination -Force
    }

    Write-Host "Downloading: $Name"
    Invoke-WebRequest -Uri $url -OutFile $Destination -UseBasicParsing
    $actualHash = Get-Hash $Destination
    if ($actualHash -ne $ExpectedHash) {
        throw "SHA256 mismatch for $Name. Please run the installer again."
    }
}

function Merge-Package([string]$OutputZip) {
    if (Test-Path -LiteralPath $OutputZip) {
        $existingHash = Get-Hash $OutputZip
        if ($existingHash -eq $expectedZipHash) {
            Write-Host "Merged package already exists."
            return
        }
        Remove-Item -LiteralPath $OutputZip -Force
    }

    Write-Host "Merging package parts..."
    $outStream = [System.IO.File]::Create($OutputZip)
    try {
        foreach ($asset in $assets) {
            $partPath = Join-Path $WorkDir $asset.Name
            $inStream = [System.IO.File]::OpenRead($partPath)
            try {
                $inStream.CopyTo($outStream)
            } finally {
                $inStream.Dispose()
            }
        }
    } finally {
        $outStream.Dispose()
    }

    $actualHash = Get-Hash $OutputZip
    if ($actualHash -ne $expectedZipHash) {
        throw "Merged package SHA256 mismatch. Please run the installer again."
    }
}

function New-AppShortcut([string]$ShortcutPath, [string]$TargetPath, [string]$WorkingDirectory) {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($ShortcutPath)
    $shortcut.TargetPath = $TargetPath
    $shortcut.WorkingDirectory = $WorkingDirectory
    $shortcut.IconLocation = "$env:SystemRoot\System32\shell32.dll,167"
    $shortcut.Save()
}

function Create-Shortcuts([string]$AppDir) {
    $target = Join-Path $AppDir "start_gui.bat"
    if (-not (Test-Path -LiteralPath $target)) {
        throw "Cannot create shortcuts because start_gui.bat was not found."
    }

    $desktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "图片超分辨率工具.lnk"
    New-AppShortcut -ShortcutPath $desktopShortcut -TargetPath $target -WorkingDirectory $AppDir

    $startMenuDir = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\图片超分辨率工具"
    New-Item -ItemType Directory -Path $startMenuDir -Force | Out-Null
    $startMenuShortcut = Join-Path $startMenuDir "图片超分辨率工具.lnk"
    New-AppShortcut -ShortcutPath $startMenuShortcut -TargetPath $target -WorkingDirectory $AppDir
}

Write-Step "Checking release files"
foreach ($asset in $assets) {
    Test-RemoteAsset "$releaseBase/$($asset.Name)"
}
if ($CheckOnly) {
    Write-Host "Release files are reachable."
    exit 0
}

Write-Step "Preparing folders"
New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null

Write-Step "Downloading package"
foreach ($asset in $assets) {
    Download-Asset -Name $asset.Name -ExpectedHash $asset.Hash -Destination (Join-Path $WorkDir $asset.Name)
}

Write-Step "Merging package"
$zipPath = Join-Path $WorkDir $zipName
Merge-Package -OutputZip $zipPath

Write-Step "Extracting package"
$extractDir = Join-Path $WorkDir "extract"
if (Test-Path -LiteralPath $extractDir) {
    Remove-Item -LiteralPath $extractDir -Recurse -Force
}
New-Item -ItemType Directory -Path $extractDir -Force | Out-Null
Expand-Archive -LiteralPath $zipPath -DestinationPath $extractDir -Force

$sourceDir = Join-Path $extractDir $packageRoot
if (-not (Test-Path -LiteralPath $sourceDir)) {
    throw "Package root folder was not found after extraction."
}

Write-Step "Installing files"
Copy-Item -Path (Join-Path $sourceDir "*") -Destination $InstallDir -Recurse -Force

if (-not $SkipShortcut) {
    Write-Step "Creating shortcuts"
    Create-Shortcuts -AppDir $InstallDir
}

if (-not $KeepDownloads) {
    Write-Step "Cleaning temporary files"
    Remove-Item -LiteralPath $WorkDir -Recurse -Force
}

Write-Step "Done"
Write-Host "Installed to: $InstallDir"
Write-Host "Start the tool with: $(Join-Path $InstallDir 'start_gui.bat')"
