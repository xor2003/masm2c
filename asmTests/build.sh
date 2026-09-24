#!/bin/sh
set -ex     
. ./_config.sh

if [ -z "$CXX" ];then
  export CXX=g++
fi

#$CC $OPT $1.cpp -E >$1.e
#$CXX $OPT $1.cpp -c
#$CXX  $1.o ../asm.o ../memmgr.o  -o $1 $OPT
DATA_REFS=""
for f in _data_refs_*.cpp; do
  [ -e "$f" ] && DATA_REFS="$DATA_REFS $f"
done
$CXX _data.cpp $DATA_REFS $1.cpp ../asm.o ../memmgr.o ../shadowstack.o $OPT -o $1


