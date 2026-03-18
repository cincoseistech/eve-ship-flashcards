# EVE Ship Flashcards

A configurable flashcard application for learning EVE Online ship identification and stats. Pulls data directly from CCP's Static Data Export and displays 3D ship renders from the EVE image server.

![Python](https://img.shields.io/badge/python-3.9+-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## Try it now

**[Launch in Browser](https://your-username-eve-ship-flashcards.streamlit.app)** — no install required

Or download for offline use from the [Releases page](https://github.com/YOUR_USERNAME/eve-ship-flashcards/releases).

## Features

- **400+ ships** with 100+ data attributes per ship
- **Ship renders** pulled from CCP's official image server
- **Fully configurable cards** — choose any combination of data fields and images for each side
- **Built-in study presets** — visual identification, fitting knowledge, tank profiles, navigation, electronic warfare
- **Custom presets** — save and load your own card configurations
- **Ship class filtering** — study specific hull classes or mix and match
- **Score tracking** — mark cards as correct or missed
- **Shuffle mode** — randomize the deck order
- **Automatic SDE updates** — re-download when CCP patches

## Requirements

- Python 3.9 or later
- Internet connection (for ship images and initial SDE download)

## Quick Start

### macOS

1. Clone or download this repository
2. Double-click `launch_mac.command`
3. If prompted about an unidentified developer, right-click the file and select Open

The launcher handles everything automatically on first run: virtual environment creation, dependency installation, SDE download, data export, and app launch.

### Windows

1. Clone or download this repository
2. Double-click `launch_windows.bat`

If Python is not in your PATH, download it from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"** during installation.

## Usage

The app opens in your default browser. Use the sidebar to configure:

**Presets** — Select a built-in study mode or load a custom preset.

**Ship Classes** — Filter the deck to specific hull classes (Frigate, Cruiser, Battleship, etc.)

**Front of Card** — Toggle the ship image and select which data fields appear on the front.

**Back of Card** — Toggle the ship image and select which data fields appear on the back.

**Display Options** — Toggle resistance percentage display.

### Built-in Presets

| Preset | Front | Back |
|--------|-------|------|
| Visual ID — Image to Name | Ship render | Name, class |
| Name ID — Name to Image | Ship name | Ship render, class |
| Fitting Knowledge — Name to Slots | Name, class | Slot layout, drones |
| Full Profile — Image to Stats | Ship render | Name, class, HP, fitting, speed, drones |
| Tank Profile — Name to Resists | Name, class | HP, all resistances |
| Navigation — Name to Movement | Name, class | Speed, agility, warp, sig radius |
| Electronic Warfare — Name to Sensors | Name, class | Scan res, target range, sensor strengths |
| Quick ID — Image to Class and Slots | Ship render | Name, class, market group, slots |

### Controls

| Button | Action |
|--------|--------|
| Shuffle Deck | Randomize card order |
| Reset Score | Zero the correct/missed counters |
| Previous / Next | Navigate through the deck |
| Flip Card | Toggle between front and back |
| Correct | Mark as known and advance |
| Missed | Mark as missed and advance |

## Updating Ship Data

When CCP releases a new expansion or rebalance:

- **macOS:** Run `./update_sde.sh` in Terminal
- **Windows:** Double-click `update_sde.bat`

This re-downloads the latest SDE and regenerates the ship data file.

## Project Structure
eve-ship-flashcards/
├── README.md
├── requirements.txt
├── .gitignore
├── launch_mac.command # macOS one-click launcher
├── launch_windows.bat # Windows one-click launcher
├── update_sde.sh # macOS SDE updater
├── update_sde.bat # Windows SDE updater
├── export_ships.py # SDE to Excel converter
└── flashcards.py # Main application
Generated at runtime (not committed):
- `venv/` — Python virtual environment
- `sde.sqlite` — EVE Static Data Export
- `eve_ships_complete.xlsx` — Exported ship data
- `flashcard_presets.json` — Custom preset storage

## Data Sources

- **Ship attributes:** [Fuzzwork SDE Conversions](https://www.fuzzwork.co.uk/dump/) (Steve Ronuken's conversion of CCP's Static Data Export)
- **Ship images:** [EVE Image Server](https://images.evetech.net/) (CCP's official renders)

## License

MIT License. This project is not affiliated with or endorsed by CCP Games. EVE Online and all related assets are property of CCP hf.
