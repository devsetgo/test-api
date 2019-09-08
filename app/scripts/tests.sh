#!/bin/bash
set -e
set -x

#run pre-commit
pre-commit run -a

# bash scripts/test.sh --cov-report=html ${@}
python3 -m pytest

# create coverage-badge
coverage-badge -o ../coverage.svg -f
