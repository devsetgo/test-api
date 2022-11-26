#!/bin/bash
set -e
set -x

# mkdocs
mkdocs build

# Copy Contribute to Github Contributing
cp docs/index.md README.md
cp docs/contribute.md CONTRIBUTING.md

mkdocs gh-deploy
