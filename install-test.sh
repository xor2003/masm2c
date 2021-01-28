#!/bin/sh -exv

pip install --upgrade pip
pip install coverage pytest

git clone https://github.com/igordejanovic/parglare.git parglare
pip install parglare

pip install .

pip install -e .[test]
