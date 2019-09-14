#!/bin/bash
set -e
set -x

# run dev
uvicorn main:app --workers 2
