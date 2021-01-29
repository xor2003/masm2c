#!/bin/sh -ex
> _result.log

. ./_config.sh

cd ..
$CXX $OPT asm.cpp -c
$CXX $OPT memmgr.cpp -c
cd asmTests

fail()
{
  echo "$n failed $1"
  #exit $1
}

ls *.asm | \
while read name;
do 
  n=$(echo $name| perl -pe 's!\.asm!!');
#  (
echo "Testing $n:"
./_singletest.sh $n 2>&1 || fail $? 
done | tee -a _result.log