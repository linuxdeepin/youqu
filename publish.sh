#!/bin/bash
rm -rf dist
pip3 install --upgrade pip
pip3 install --upgrade build
pip3 install --upgrade twine
python3 -m build
twine upload dist/*