@echo off
cd /d "%~dp0"

echo Updating EVE Static Data Export...

if exist sde.sqlite del sde.sqlite
if exist sde.sqlite.bz2 del sde.sqlite.bz2
if exist eve_ships_complete.xlsx del eve_ships_complete.xlsx

echo Downloading latest SDE...
where curl >nul 2>nul
if %errorlevel% equ 0 (
    curl -L -o sde.sqlite.bz2 https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2
) else (
    powershell -Command "Invoke-WebRequest -Uri 'https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2' -OutFile 'sde.sqlite.bz2'"
)

echo Decompressing...
call venv\Scripts\activate.bat
python -c "import bz2, shutil; shutil.copyfileobj(bz2.BZ2File('sde.sqlite.bz2'), open('sde.sqlite','wb'))"
del sde.sqlite.bz2

echo Exporting ship data...
python export_ships.py

echo.
echo Update complete. Launch the app to use the new data.
pause
