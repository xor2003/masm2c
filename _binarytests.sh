#!/bin/sh
set -ex
#git clone https://github.com/igordejanovic/parglare.git parglaredev
#pip install parglaredev/
#rm -rf parglaredev/
pip install -r requirements.txt

cd asmTests

python ./run_tests.py

cd ../qemu_tests

./_test.sh 
