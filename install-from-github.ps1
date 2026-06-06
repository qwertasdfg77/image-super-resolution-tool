param(
    [string]$InstallDir = (Join-Path $env:LOCALAPPDATA "Programs\ImageSuperResolutionTool"),
    [string]$WorkDir = (Join-Path $env:TEMP "ImageSuperResolutionToolInstall"),
    [string]$ReleaseTag = "v1.0.2",
    [switch]$SkipShortcut,
    [switch]$KeepDownloads,
    [switch]$CheckOnly,
    [int]$MaxRetries = 3
)

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$repo = "qwertasdfg77/image-super-resolution-tool"
$tag = $ReleaseTag
$releaseBase = "https://github.com/$repo/releases/download/$tag"
$zipName = "image-super-resolution-tool-full.zip"
$packageRoot = "image-super-resolution-tool"
$expectedZipHash = "F7E5AF75328545E508DEF25DA1BE5A885C5EE4B36A065CBF74121C6C2CFEAC62"

$assets = @(
    @{
        Name = "image-super-resolution-tool-full.zip.001"
        Hash = "5DBB138CA33030690473838E72589AB42A71CEB1D96107301B8B355074BF88B1"
    },
    @{
        Name = "image-super-resolution-tool-full.zip.002"
        Hash = "017C985A9FBD5D566D482FC15D47BC138EA74B36B7FC041B59CAECC95A8807F1"
    }
)

function Write-Step([string]$Message) {
    Write-Host ""
    Write-Host "== $Message =="
}

function Format-Bytes([double]$Bytes) {
    if ($Bytes -ge 1GB) { return "{0:N2} GB" -f ($Bytes / 1GB) }
    if ($Bytes -ge 1MB) { return "{0:N1} MB" -f ($Bytes / 1MB) }
    if ($Bytes -ge 1KB) { return "{0:N1} KB" -f ($Bytes / 1KB) }
    return "{0:N0} B" -f $Bytes
}

function Format-Duration([double]$Seconds) {
    if ($Seconds -lt 0 -or [double]::IsNaN($Seconds) -or [double]::IsInfinity($Seconds)) {
        return "--:--"
    }
    $span = [TimeSpan]::FromSeconds([Math]::Round($Seconds))
    if ($span.TotalHours -ge 1) {
        return "{0:00}:{1:00}:{2:00}" -f [Math]::Floor($span.TotalHours), $span.Minutes, $span.Seconds
    }
    return "{0:00}:{1:00}" -f $span.Minutes, $span.Seconds
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

function Download-FileWithProgress([string]$Url, [string]$Destination, [string]$DisplayName) {
    $tempDestination = "$Destination.download"
    if (Test-Path -LiteralPath $tempDestination) {
        Remove-Item -LiteralPath $tempDestination -Force
    }

    $request = [System.Net.HttpWebRequest]::Create($Url)
    $request.Method = "GET"
    $request.AllowAutoRedirect = $true
    $request.UserAgent = "ImageSuperResolutionToolInstaller/1.0.1"
    $response = $request.GetResponse()
    $totalBytes = [int64]$response.ContentLength
    $inputStream = $response.GetResponseStream()
    $outputStream = [System.IO.File]::Create($tempDestination)
    $buffer = New-Object byte[] (1024 * 1024)
    $downloaded = [int64]0
    $startedAt = Get-Date
    $lastPrintedAt = Get-Date

    try {
        while ($true) {
            $read = $inputStream.Read($buffer, 0, $buffer.Length)
            if ($read -le 0) { break }

            $outputStream.Write($buffer, 0, $read)
            $downloaded += $read

            $now = Get-Date
            if (($now - $lastPrintedAt).TotalSeconds -ge 1 -or ($totalBytes -gt 0 -and $downloaded -eq $totalBytes)) {
                $elapsed = [Math]::Max(0.1, ($now - $startedAt).TotalSeconds)
                $speed = $downloaded / $elapsed
                $eta = if ($totalBytes -gt 0 -and $speed -gt 0) { ($totalBytes - $downloaded) / $speed } else { -1 }
                $status = "$(Format-Bytes $downloaded)"
                if ($totalBytes -gt 0) {
                    $status = "$status / $(Format-Bytes $totalBytes)"
                }
                $status = "$status | $(Format-Bytes $speed)/s | ETA $(Format-Duration $eta)"

                if ($totalBytes -gt 0) {
                    $percent = [Math]::Min(100, [Math]::Round(($downloaded / $totalBytes) * 100, 1))
                    Write-Progress -Activity "Downloading $DisplayName" -Status $status -PercentComplete $percent
                    Write-Host ("{0,6:N1}%  {1}" -f $percent, $status)
                } else {
                    Write-Progress -Activity "Downloading $DisplayName" -Status $status
                    Write-Host $status
                }
                $lastPrintedAt = $now
            }
        }
    } finally {
        if ($outputStream) { $outputStream.Dispose() }
        if ($inputStream) { $inputStream.Dispose() }
        if ($response) { $response.Dispose() }
        Write-Progress -Activity "Downloading $DisplayName" -Completed
    }

    Move-Item -LiteralPath $tempDestination -Destination $Destination -Force
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

    for ($attempt = 1; $attempt -le $MaxRetries; $attempt++) {
        try {
            Write-Host "Downloading: $Name (attempt $attempt/$MaxRetries)"
            Download-FileWithProgress -Url $url -Destination $Destination -DisplayName $Name
            break
        } catch {
            if (Test-Path -LiteralPath $Destination) {
                Remove-Item -LiteralPath $Destination -Force
            }
            if (Test-Path -LiteralPath "$Destination.download") {
                Remove-Item -LiteralPath "$Destination.download" -Force
            }
            if ($attempt -ge $MaxRetries) {
                throw "Download failed after $MaxRetries attempts: $Name. $($_.Exception.Message)"
            }
            $delay = [Math]::Min(30, [Math]::Pow(2, $attempt))
            Write-Warning "Download failed: $Name. Retrying in $delay seconds..."
            Start-Sleep -Seconds $delay
        }
    }

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
