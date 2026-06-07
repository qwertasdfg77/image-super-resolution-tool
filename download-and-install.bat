@echo off
setlocal
set "URL=https://github.com/qwertasdfg77/image-super-resolution-tool/releases/latest/download/ImageSuperResolutionTool-ModelIncluded.zip"
set "ZIP=%USERPROFILE%\Desktop\ImageSuperResolutionTool-ModelIncluded.zip"
set "DESKTOP=%USERPROFILE%\Desktop"
set "APPDIR=%DESKTOP%\ImageSuperResolutionTool-ModelIncluded"

echo Downloading ImageSuperResolutionTool-ModelIncluded.zip...
where curl >nul 2>nul
if errorlevel 1 (
    echo curl.exe was not found. Please download the zip from the Latest Release page.
    pause
    exit /b 1
)

curl.exe -L --fail --retry 3 -o "%ZIP%" "%URL%"
if errorlevel 1 (
    echo Download failed. Please download the zip from the Latest Release page.
    pause
    exit /b 1
)

where tar >nul 2>nul
if errorlevel 1 (
    echo tar.exe was not found. Download finished:
    echo %ZIP%
    echo Please extract it manually.
    pause
    exit /b 1
)

if exist "%APPDIR%" (
    echo Removing old app folder...
    rmdir /s /q "%APPDIR%"
)
for /d %%D in ("%DESKTOP%\ImageSuperResolutionTool-Light*") do (
    echo Removing old app folder...
    rmdir /s /q "%%~D"
)

tar.exe -xf "%ZIP%" -C "%DESKTOP%"
if errorlevel 1 (
    echo Extraction failed. Please extract the zip manually.
    pause
    exit /b 1
)

if not exist "%APPDIR%\install_gpu.bat" (
    echo App folder was not found after extraction.
    pause
    exit /b 1
)

echo Installing runtime environment...
call "%APPDIR%\install_gpu.bat"
if errorlevel 1 (
    echo Runtime installation failed.
    pause
    exit /b 1
)

echo Opening app...
call "%APPDIR%\start_gui.bat"
exit /b 0
