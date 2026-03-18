#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Updating EVE Static Data Export..."

rm -f sde.sqlite sde.sqlite.bz2 eve_ships_complete.xlsx

echo "Downloading latest SDE..."
curl -L -o sde.sqlite.bz2 https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2

echo "Decompressing..."
bunzip2 sde.sqlite.bz2

echo "Exporting ship data..."
source venv/bin/activate
python export_ships.py

echo ""
echo "Update complete. Launch the app to use the new data."
