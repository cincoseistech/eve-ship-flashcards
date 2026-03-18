#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "==========================================="
echo "  EVE Ship Flashcards"
echo "==========================================="
echo ""

# --- Check for Python 3 ---
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "ERROR: Python 3 is required but not installed."
    echo ""
    echo "Install it from https://www.python.org/downloads/"
    echo "or via Homebrew:  brew install python"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Using: $($PYTHON --version)"
echo ""

# --- Create virtual environment if needed ---
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv venv
    echo "  Done."
    echo ""
fi

# --- Activate ---
source venv/bin/activate

# --- Install dependencies if needed ---
if ! python -c "import streamlit, pandas, openpyxl" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    echo "  Done."
    echo ""
fi

# --- Download SDE if needed ---
if [ ! -f "sde.sqlite" ]; then
    echo "Downloading EVE Static Data Export..."
    echo "  This is ~150MB and only needs to happen once."
    curl -L -o sde.sqlite.bz2 https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2
    echo ""
    echo "Decompressing..."
    bunzip2 sde.sqlite.bz2
    echo "  Done."
    echo ""
fi

# --- Export ship data if needed ---
if [ ! -f "eve_ships_complete.xlsx" ]; then
    echo "Exporting ship data to Excel..."
    python export_ships.py
    echo ""
fi

# --- Launch ---
echo "==========================================="
echo "  Starting application..."
echo "  Your browser will open automatically."
echo "  To stop: close this terminal window"
echo "         or press Ctrl+C"
echo "==========================================="
echo ""

streamlit run flashcards.py --server.headless true --browser.gatherUsageStats false
