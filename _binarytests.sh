#!/bin/sh -ex
cd asmTests

git clone https://github.com/igordejanovic/parglare.git parglaredev
pip install parglaredev/
rm -rf parglaredev/

./_tests.sh 
