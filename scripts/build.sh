#!/bin/bash
set -e
set -x

# upgrade
# docker build -t mikeryan56/test-api -f dockerfile_pypy .

CAL_VER=$(date '+%Y-%m-%d')
echo 'Docker Build Python'
docker build -t mikeryan56/test-api:$CAL_VER-python38 -f ./dockerfiles/dockerfile_python .
echo "Running Docker Image"
docker run mikeryan56/test-api:$CAL_VER-python38
# echo 'Docker Build with PyPy'
# docker build -t mikeryan56/test-api:$CAL_VER -f ./docker/dockerfile_pypy .

