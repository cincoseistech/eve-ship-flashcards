#!/bin/bash
if [ ! -f "sde.sqlite" ]; then
    curl -L -o sde.sqlite.bz2 https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2
    bunzip2 sde.sqlite.bz2
fi
if [ ! -f "eve_ships_complete.xlsx" ]; then
    python export_ships.py
fi
