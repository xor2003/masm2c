 ~/clang8/bin/clang++ -w -fpermissive -m32 -lm -I.. -DNO_SHADOW_STACK test.cpp -DDEBUG=0  -emit-llvm -S  -Os 2>&1
