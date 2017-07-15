#!/bin/bash

set -e

DIR="$(dirname "$0")"

cd "$DIR"

VENV="letter-game-venv"

if [ ! -d "$VENV" ]; then
  virtualenv letter-game-venv
  source "$VENV/bin/activate"
  pip install pygame
  pip install requests
else
  source "$VENV/bin/activate"
fi


python LetterGameMain.py "$@"
