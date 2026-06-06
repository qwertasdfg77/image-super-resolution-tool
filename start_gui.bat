@echo off
set "APP_DIR=%~dp0"
set "SCRIPT=%APP_DIR%dlss_like_super_resolution_gui.py"
set "VENV_PYTHONW=%APP_DIR%.venv\Scripts\pythonw.exe"
set "VENV_PYTHON=%APP_DIR%.venv\Scripts\python.exe"
set "CODEX_PYTHONW=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\pythonw.exe"
set "CODEX_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if exist "%VENV_PYTHONW%" (
    start "" "%VENV_PYTHONW%" "%SCRIPT%"
    exit /b 0
)

if exist "%VENV_PYTHON%" (
    start "" "%VENV_PYTHON%" "%SCRIPT%"
    exit /b 0
)

if exist "%CODEX_PYTHONW%" (
    start "" "%CODEX_PYTHONW%" "%SCRIPT%"
    exit /b 0
)

if exist "%CODEX_PYTHON%" (
    start "" "%CODEX_PYTHON%" "%SCRIPT%"
    exit /b 0
)

powershell -ExecutionPolicy Bypass -NoExit -File "%APP_DIR%install_gpu.ps1"
