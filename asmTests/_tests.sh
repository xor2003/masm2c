#!/bin/bash
set -ex
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
)

result=0

for name in $(ls *.asm *.lst|xargs)
do 
  n=$(echo $name| perl -pe 's!\.asm!!');
  export n
#  (
echo "Testing $n:"
./_singletest.sh $n 2>&1 | tee -a _result.log
res=$?
if [ $res -ne 0 ];then
  echo "$n failed with code $res" | tee -a _result.log
  result=$(( $result + 1 ))
  export result
fi
done
#cat _result.log
! grep 'error:' _result.log
echo "Total result: $result"
exit $result
