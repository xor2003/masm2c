#!/bin/sh -ex
rm test-i386_conv test-i386_conv.txt || true
# g++ -O0  -I.. test-i386_conv.cpp -E -fpermissive > test-i386_conv.e
$CXX -O0  -I.. test-i386_conv.cpp -o test-i386_conv -fpermissive -w 2>&1 
# -Og -ggdb3
./test-i386_conv > test-i386_conv.txt
diff -u test-i386.txt test-i386_conv.txt 