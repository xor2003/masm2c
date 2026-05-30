#!/bin/sh
set -eux

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

#git clone https://github.com/igordejanovic/parglare.git parglaredev
#pip install parglaredev/

python -m pip install -e .[dev]
