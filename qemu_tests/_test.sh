#!/bin/sh
set -ex
if [ -z "$CXX" ];then
  export CXX=g++
fi

# No need to generate reference each time
#gcc -O0 -m32 test-i386.c -o test-i386 -fpermissive -w 
#./test-i386 > test-i386.txt

rm test-i386_conv test-i386_conv.txt || true
# g++ -O0  -I.. test-i386_conv.cpp -E -fpermissive > test-i386_conv.e
$CXX -O0 -m32 -ggdb3 -I.. test-i386_conv.cpp -o test-i386_conv -fpermissive -w
# -Og -ggdb3
./test-i386_conv > test-i386_conv.txt
diff -u --label real test-i386.txt --label emulated test-i386_conv.txt > test-i386.diff || true 

diff -u test-i386_benchmark.diff test-i386.diff