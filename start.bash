#!/bin/bash
set -e
PORT=${1:-5000}
if [ ! -f 'app.py' ]; then
  echo 'Only run from within the dir'
  exit 1
fi
if [ ! -d "venv" ]; then
  virtualenv --python=python3.12 venv
fi
source venv/bin/activate
pip3 install pip==25.0 pip-tools==7.4.1
pip-sync setup/requirements.txt

hypercorn --bind 0.0.0.0:$PORT app

