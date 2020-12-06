#!/bin/bash
set -e
set -x

# upgrade
# docker build -t mikeryan56/test-api -f dockerfile_pypy .

CAL_VER=$(date '+%Y-%m-%d')
echo 'Docker Build Python'
docker build -t mikeryan56/test-api:$CAL_VER-python38 -f ./docker/dockerfile_python .
echo 'Docker Build with PyPy'
# docker build -t mikeryan56/test-api:$CAL_VER -f ./docker/dockerfile_pypy .

