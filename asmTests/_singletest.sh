#!/bin/sh
set -x
if [ -z "$CXX" ];then
  export CXX=g++
fi
name="$1"
n="$(echo $name| perl -pe 's!(\.asm|\.lst)!!')"

rm $n.cpp $n.h $n.err $n.log $n.txt $n.asm.log $n.o $n 2>/dev/null || true
##./ml /c /Fl $1.asm
#uasm /c /Fl $1.asm
if [ -z "$name" ];then
  exit 0
elif [ ! -r "$name" ];then
  echo "No such file $name"
  exit 2
fi


../masm2c.py -m separate "$name" > "$n.txt" 2>&1
res=$?
if [ "${res}" -ne 0 ];then
   cat "$n.txt"
   exit "${res}"
fi  


./build.sh $n > "$n.txt" 2>&1
res=$?
if [ "${res}" -ne 0 ];then
   cat "$n.txt" asm.log
   exit "${res}"
fi  
rm asm.log || true

./$n > "$n.txt" 2>&1
res=$?
if [ "${res}" -ne 0 ];then
   cat "$n.txt"
   exit "${res}"
fi  
#python ../_masm61.py  $1.asm

