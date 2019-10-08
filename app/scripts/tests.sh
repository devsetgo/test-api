#!/bin/bash
set -e
set -x

# run isort recursively
# isort -rc .

#run pre-commit
pre-commit run -a

# bash scripts/test.sh --cov-report=html ${@}
# python3 -m pytest
python3 -m pytest -v -s

# create coverage-badge
coverage-badge -o ../coverage.svg -f

# delete db
rm sqlite_db/test-api.db
echo "db removed"
