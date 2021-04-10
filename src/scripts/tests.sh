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

# bash scripts/test.sh --cov-report=html ${@}
python3 -m pytest
# python3 -m pytest -v -s

# create coverage-badge
coverage-badge -o ../coverage.svg -f
cp ~/test-api/src/coverage.xml ~/test-api/coverage-report.xml
# delete db
# rm sqlite_db/api.db
# echo "db removed"
# generate flake8 report
flake8 --tee . > flake8_report/report.txt
