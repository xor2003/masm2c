#!/bin/sh -ex
     
. ./_config.sh
#$CC $OPT $1.cpp -E >$1.e
#$CXX $OPT $1.cpp -c
#$CXX  $1.o ../asm.o ../memmgr.o  -o $1 $OPT
$CXX  $1.cpp ../asm.o ../memmgr.o $OPT -o $1


