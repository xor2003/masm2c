#!/bin/sh
set +x
~/clang8/bin/clang++ -Os -w -fpermissive -m32 -lm -I.. -DNOSDL -DNO_SHADOW_STACK -DM2CDEBUG=-1 test-i386_conv.cpp -S -emit-llvm
perl -i -pe 's!^declare (i\d+) (\@llvm\.f.*)!define $1 $2 {ret $1 0}!' test-i386_conv.ll
perl -i -pe 's!llvm\.f!f!g' test-i386_conv.ll
exit 0
perl -ni -e 'print unless / = comdat any/' test-i386_conv.ll 
perl -ni -e 'print unless /= global /' test-i386_conv.ll 
perl -ni -e 'print unless /= external hidden global /' test-i386_conv.ll 
perl -ni -e 'print unless /= internal global /' test-i386_conv.ll 
perl -ni -e 'print unless /= private unnamed_addr constant /' test-i386_conv.ll 
perl -ni -e 'print unless /= local_unnamed_addr global /' test-i386_conv.ll 
perl -ni -e 'print unless /= local_unnamed_addr constant /' test-i386_conv.ll 
perl -ni -e 'print unless /= appending global /' test-i386_conv.ll 

perl -i -pe 's!dso_local !!g; s!comdat align!align!g; s!comdat !!g; s!section "\.text\.startup"!!' test-i386_conv.ll

