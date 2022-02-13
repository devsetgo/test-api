#!/bin/bash
set -e
set -x
#delete db
DB_NAME="~/pynote_2/src/sqlite_db/api.db"
if [[ -f DB_NAME ]]
then
    echo "deleting api.db"
    rm DB_NAME
fi

#delete logs
LOG_NAME="~/pynote_2/src/logging/log.log"
if [[ -f LOG_NAME ]]
then
    echo "deleting api.db"
    rm LOG_NAME
fi

# run dev
uvicorn main:app --port 5000 --reload --log-level debug

