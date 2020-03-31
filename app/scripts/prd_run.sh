#!/bin/bash
set -e
set -x

# run dev
# uvicorn main:app --port 5000 --workers 4 --log-level warning
gunicorn -c gunicorn_cfg.py main:app
