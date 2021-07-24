#!/bin/sh -ex
#git clone https://github.com/igordejanovic/parglare.git parglaredev
#pip install parglaredev/
#rm -rf parglaredev/
pip install -r requirements.txt

cd asmTests


./_tests.sh 
