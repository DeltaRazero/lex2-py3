#!/usr/bin/env bash

# Clean dist folder (if it exists)
find ./ -type d -name "dist" -exec rm -r {} \; -prune

# Create source archive and wheel
python setup.py sdist bdist_wheel

# Clean after building
python setup.py clean --all
find ./ -type d -name "*.egg-info" -exec rm -r {} \; -prune
