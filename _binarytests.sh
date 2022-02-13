#!/bin/sh
set -ex
#git clone https://github.com/igordejanovic/parglare.git parglaredev
#pip install parglaredev/
#rm -rf parglaredev/
python -m pip install -r testrequirements.txt

cd asmTests

./_tests.sh 

cd ../qemu_tests

./_test.sh 
