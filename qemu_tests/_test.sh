#!/bin/sh
set -ex
if [ -z "$CXX" ];then
  export CXX=g++
fi

# No need to generate reference each time
#gcc -O0  -m32 -lm test-i386.c -o test-i386 2>&1 | tee result.txt
#-Os -fdata-sections -ffunction-sections -static -s 
#./test-i386 > test-i386.txt

rm test-i386_conv test-i386_conv.txt || true
$CXX -O0  -I.. test-i386_conv.cpp -E -fpermissive > test-i386_conv.e
$CXX -O0 -w -fpermissive -m32 -lm -I.. test-i386_conv.cpp -o test-i386_conv 2>&1 | tee -a result.txt
# -ggdb3 -Og -Wa,-adhlns="test-i386_conv.lst" -fdata-sections -ffunction-sections -static -ftime-report

./test-i386_conv > test-i386_conv.txt
diff -diu --label real test-i386.txt --label emulated test-i386_conv.txt > test-i386.diff || true 

diff -diu test-i386_benchmark.diff test-i386.diff | tee -a result.txt