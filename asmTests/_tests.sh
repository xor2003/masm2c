#!/bin/bash
set -e
if [ -z "$CXX" ];then
  export CXX=g++
fi

filename="$1"

> _result.log

. ./_config.sh

(
cd ..
$CXX $OPT asm.cpp -c
$CXX $OPT memmgr.cpp -c
$CXX $OPT shadowstack.cpp -c
)

result=0

for name in $(ls *.asm *.lst|xargs)
do 
  echo "Testing $name:"
  ./_singletest.sh "$name" 2>&1 | tee -a _result.log
res=${PIPESTATUS[0]}
if [ $res -ne 0 ];then
  echo "$n failed with code $res" | tee -a _result.log
  result=$(( $result + 1 ))
  export result
fi
echo '-------------------------------------------------------------'
echo
done
#cat _result.log
! grep 'error:' _result.log
echo "Total result: $result"
exit $result
