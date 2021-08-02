#!/bin/bash
set -e
set -x

# upgrade
# docker build -t mikeryan56/test-api -f dockerfile_pypy .

CAL_VER=$(date '+%Y-%m-%d')
echo 'Docker Build Python'
docker build -t mikeryan56/test-api:$CAL_VER -f /dockerfiles/dockerfile_python .
docker push mikeryan56/test-api:$CAL_VER

