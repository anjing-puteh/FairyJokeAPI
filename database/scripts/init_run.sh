#!/bin/bash

venv=${VENV:-sandbox}
[ -d "$venv" ] || python -m venv "$venv"
source "$venv/bin/activate"
pip install --upgrade -r requirements.txt
alembic upgrade head

export SDVX_DATA="$HOME/Downloads/KFC-2022091301/contents/data"
./scripts/import_games.py
./scripts/import_sdvx_data.py "$SDVX_DATA/others/music_db.xml" EG
./scripts/import_sdvx_data.py "$SDVX_DATA/others/appeal_card.xml" EG

uvicorn app:app --reload --host 0.0.0.0 --port "${1:-57302}"
