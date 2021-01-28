#!/bin/sh

pip install --upgrade pip || exit 1
pip install coverage pytest || exit 1

git clone https://github.com/igordejanovic/parglare.git parglare
pip install parglare

pip install -e .[test] || exit 1
