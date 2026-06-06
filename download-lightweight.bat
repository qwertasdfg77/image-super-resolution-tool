@echo off
setlocal
set "URL=https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest/download/ImageSuperResolutionTool-Lightweight.zip"
set "OUT=%USERPROFILE%\Desktop\ImageSuperResolutionTool-Lightweight.zip"
set "DEST=%USERPROFILE%\Desktop"

echo Downloading ImageSuperResolutionTool-Lightweight.zip...
where curl >nul 2>nul
if errorlevel 1 (
    echo curl.exe was not found. Please download the zip from the Latest Release page.
    pause
    exit /b 1
)

curl.exe -L --fail --retry 3 -o "%OUT%" "%URL%"
if errorlevel 1 (
    echo Download failed. Please download the zip from the Latest Release page.
    pause
    exit /b 1
)

where tar >nul 2>nul
if errorlevel 1 (
    echo Download finished: %OUT%
    echo Please extract it manually.
    pause
    exit /b 0
)

tar.exe -xf "%OUT%" -C "%DEST%"
if errorlevel 1 (
    echo Download finished: %OUT%
    echo Automatic extraction failed. Please extract it manually.
    pause
    exit /b 0
)

echo Ready: %DEST%\ImageSuperResolutionTool-Lightweight
pause
