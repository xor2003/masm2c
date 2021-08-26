#!/bin/sh
set -ex     
. ./_config.sh

if [ -z "$CXX" ];then
  export CXX=g++
fi

#$CC $OPT $1.cpp -E >$1.e
#$CXX $OPT $1.cpp -c
#$CXX  $1.o ../asm.o ../memmgr.o  -o $1 $OPT
$CXX _data.cpp $1.cpp ../asm.o ../memmgr.o $OPT -o $1


