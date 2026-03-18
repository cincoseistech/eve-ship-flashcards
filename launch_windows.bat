@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ===========================================
echo   EVE Ship Flashcards
echo ===========================================
echo.

REM --- Check for Python ---
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python 3 is required but not found in PATH.
    echo.
    echo Download it from https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo Using: %PYVER%
echo.

REM --- Create virtual environment if needed ---
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo   Done.
    echo.
)

REM --- Activate ---
call venv\Scripts\activate.bat

REM --- Install dependencies if needed ---
python -c "import streamlit, pandas, openpyxl" 2>nul
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    echo   Done.
    echo.
)

REM --- Download SDE if needed ---
if not exist "sde.sqlite" (
    echo Downloading EVE Static Data Export...
    echo   This is ~150MB and only needs to happen once.
    echo.

    where curl >nul 2>nul
    if %errorlevel% equ 0 (
        curl -L -o sde.sqlite.bz2 https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2
    ) else (
        powershell -Command "Invoke-WebRequest -Uri 'https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2' -OutFile 'sde.sqlite.bz2'"
    )

    echo Decompressing...
    python -c "import bz2, shutil; shutil.copyfileobj(bz2.BZ2File('sde.sqlite.bz2'), open('sde.sqlite','wb'))"
    del sde.sqlite.bz2
    echo   Done.
    echo.
)

REM --- Export ship data if needed ---
if not exist "eve_ships_complete.xlsx" (
    echo Exporting ship data to Excel...
    python export_ships.py
    echo.
)

REM --- Launch ---
echo ===========================================
echo   Starting application...
echo   Your browser will open automatically.
echo   To stop: close this window
echo          or press Ctrl+C
echo ===========================================
echo.

streamlit run flashcards.py --server.headless true --browser.gatherUsageStats false
