#!/bin/sh -exv

pip install --upgrade pip
pip install pytest coverage
pip install -r requirements.txt

#git clone https://github.com/igordejanovic/parglare.git parglaredev
#pip install parglaredev/

pip install -e .[test]
