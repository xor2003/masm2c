#!/bin/sh -exv

pip install --upgrade pip
pip install pytest
pip install coverage

git clone https://github.com/igordejanovic/parglare.git parglaredev
pip install parglaredev/

pip install -e .[test]
