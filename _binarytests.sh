#!/bin/sh -ex
cd asmTests

#git clone https://github.com/igordejanovic/parglare.git parglaredev
#pip install parglaredev/
#rm -rf parglaredev/
pip install -r requirements.txt

./_tests.sh 
