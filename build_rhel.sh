#!/bin/sh +x
/opt/rh/devtoolset-7/root/usr/bin/g++ iplay_masm_.cpp -o iplay_masm -O0 -lncurses -ltinfo -ggdb -Wno-multichar 2&>1 #-DDEBUG 

