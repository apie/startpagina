#!/bin/bash
set -e
if [ ! -f 'app.py' ]; then
  echo 'Only run from within the dir'
  exit 1
fi
if [ ! -d "venv" ]; then
  virtualenv --python=python3.10 venv
fi
source venv/bin/activate
pip3 install pip==23.3.1 pip-tools==7.3.0
pip-sync setup/requirements.txt

hypercorn --bind 0.0.0.0:5000 app

