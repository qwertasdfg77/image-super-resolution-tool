@echo off
setlocal
set "APP_DIR=%~dp0"
set "INSTALLER=%APP_DIR%install_gpu.py"
set "PYTHON_INSTALLER=%TEMP%\python-3.12.10-amd64.exe"
set "PYTHON_URL=https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"

call :find_python

if not defined PYTHON_EXE (
    echo Python was not found. Trying winget...
    where winget >nul 2>nul
    if not errorlevel 1 (
        winget install --id Python.Python.3.12 --exact --source winget --scope user --accept-package-agreements --accept-source-agreements
    )
    call :find_python
)

if not defined PYTHON_EXE (
    echo Python was not found. Downloading Python installer from python.org...
    where curl >nul 2>nul
    if errorlevel 1 (
        echo curl.exe was not found. Please install Python 3.12 from https://www.python.org/downloads/windows/
        pause
        exit /b 1
    )
    curl.exe -L -o "%PYTHON_INSTALLER%" "%PYTHON_URL%"
    if errorlevel 1 (
        echo Python download failed. Please install Python 3.12 manually from https://www.python.org/downloads/windows/
        pause
        exit /b 1
    )
    start /wait "" "%PYTHON_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_tcltk=1 Include_launcher=0
    call :find_python
)

if not defined PYTHON_EXE (
    echo Python installation finished, but Python could not be found. Restart Windows or install Python 3.12 manually.
    pause
    exit /b 1
)

"%PYTHON_EXE%" "%INSTALLER%"
if errorlevel 1 (
    echo.
    echo Environment installation failed.
    pause
    exit /b 1
)

echo.
echo Environment is ready.
pause
exit /b 0

:find_python
set "PYTHON_EXE="
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
) do (
    if exist "%%~P" (
        set "PYTHON_EXE=%%~P"
        exit /b 0
    )
)
where py >nul 2>nul
if not errorlevel 1 (
    for /f "usebackq delims=" %%P in (`py -3 -c "import sys; print(sys.executable)" 2^>nul`) do (
        set "PYTHON_EXE=%%P"
        exit /b 0
    )
)
where python >nul 2>nul
if not errorlevel 1 (
    for /f "usebackq delims=" %%P in (`python -c "import sys; print(sys.executable)" 2^>nul`) do (
        echo %%P | findstr /i "\Microsoft\WindowsApps\" >nul
        if errorlevel 1 (
            set "PYTHON_EXE=%%P"
            exit /b 0
        )
    )
)
exit /b 0
