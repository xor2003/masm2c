#!/bin/sh
set -ex     
. ./_config.sh

if [ -z "$CXX" ];then
  export CXX=g++
fi

(
cd ..
#$CXX $OPT asm.cpp -c
#$CXX $OPT memmgr.cpp -c
#$CXX $OPT shadowstack.cpp -c
)
# ../asm.o ../memmgr.o ../shadowstack.o
$CXX test_insn_tests.cpp $OPT -lgtest -lgtest_main -o test_insn_tests

