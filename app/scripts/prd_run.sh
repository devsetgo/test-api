#!/bin/bash
set -e
set -x

# run dev
read_var() {
    VAR=$(grep $1 $2 | xargs)
    IFS="=" read -ra VAR <<< "$VAR"
    echo ${VAR[1],,}
}

LOGURU_LOGGING_LEVEL=$(read_var LOGURU_LOGGING_LEVEL .env)
gunicorn -c gunicorn_cfg.py main:app #--log-level ${LOGURU_LOGGING_LEVEL,,}
