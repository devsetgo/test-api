#!/bin/bash
set -e
set -x

# rm logfile/app_log.log
echo "log cleared"

# delete db
# rm sqlite_db/api.db
echo "db removed"
# run isort recursively
# isort -rc .

#run pre-commit
pre-commit run -a

# Run Pytest
python3 -m pytest -n auto

# python3 -m pytest -v -s
sed -i "s/<source>\/workspace\/src<\/source>/<source>\/github\/workspace\/src<\/source>/g" /workspace/src/coverage.xml
# create coverage-badge
coverage-badge -o ../coverage.svg -f
# delete db
# rm sqlite_db/api.db
# echo "db removed"
# generate flake8 report
flake8 --tee . > flake8_report/report.txt
