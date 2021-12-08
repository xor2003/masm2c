#!/bin/sh
set -ex
if [ -z "$CXX" ];then
  export CXX=g++
fi

# No need to generate reference each time
#gcc -Os -fdata-sections -ffunction-sections  -m32 -lm test-i386.c -static -s -o test-i386
#./test-i386 > test-i386.txt

rm test-i386_conv test-i386_conv.txt || true
# g++ -O0  -I.. test-i386_conv.cpp -E -fpermissive > test-i386_conv.e
$CXX -w -fpermissive -Og -ggdb3 -Wa,-adhlns="test-i386_conv.lst" -fdata-sections -ffunction-sections  -m32 -lm -static -I.. test-i386_conv.cpp -o test-i386_conv 

./test-i386_conv > test-i386_conv.txt
diff -u --label real test-i386.txt --label emulated test-i386_conv.txt > test-i386.diff || true 

diff -u test-i386_benchmark.diff test-i386.diff