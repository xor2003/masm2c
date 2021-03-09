#!/bin/bash -ex

filename="$1"

> _result.log

. ./_config.sh

(
cd ..
$CXX $OPT asm.cpp -c
$CXX $OPT memmgr.cpp -c
)

result=0

for name in $(ls *.asm|xargs)
do 
  n=$(echo $name| perl -pe 's!\.asm!!');
  export n
#  (
echo "Testing $n:"
./_singletest.sh $n 2>&1 >> _result.log
res=$?
if [ $res -ne 0 ];then
  echo "$n failed $res" >> _result.log
  result=$(( $result + 1 ))
  export result
fi
cat _result.log
done

echo "Total result: $result"
exit $result
