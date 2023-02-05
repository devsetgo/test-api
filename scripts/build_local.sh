#!/bin/bash
set -e
set -x

# upgrade
# docker build -t mikeryan56/test-api -f dockerfile_pypy .

CAL_VER=$(TZ=":US/Eastern" date '+%Y-%m-%d')
echo 'Docker Build Python'
docker build -t test-api:$CAL_VER-local -f ./dockerfiles/dockerfile_python .
# echo "Running Docker Image"
# docker run mikeryan56/test-api:$CAL_VER-python38
echo "run"
docker run test-api:$CAL_VER-local

