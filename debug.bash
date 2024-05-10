#!/bin/bash
source venv/bin/activate
FLASK_DEBUG=1 quart run --reload
