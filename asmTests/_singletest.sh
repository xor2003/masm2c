#!/bin/sh
set -ex
if [ -z "$CXX" ];then
  export CXX=g++
fi
rm $1.cpp $1.h $1.err $1.log $1.txt $1.asm.log $1.o $1 2>/dev/null || true
##./ml /c /Fl $1.asm
#uasm /c /Fl $1.asm
if [ -r "$1.asm" ];then
  name=$1.asm
elif [ -r "$1.lst" ];then
  name=$1.lst
elif [ -z "$1" ];then
  echo "No such file $1"
  exit 2
fi
../masm2c.py -m separate $name 2>&1 | tee $1.txt
echo "Converting result $?"
./build.sh $1 2>&1
rm asm.log || true
./$1 2>&1
#python ../_masm61.py  $1.asm

