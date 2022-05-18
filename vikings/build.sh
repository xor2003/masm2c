#!/bin/sh
set -ex     
#. ./_config.sh

if [ -z "$CXX" ];then
  export CXX=g++
fi

export SDL="$(pkg-config --cflags --libs sdl2)"
export CURSES="-DNOCURSES $(pkg-config --cflags --libs ncurses)"
export OPT="-Wno-narrowing -mno-ms-bitfields  -Wno-multichar $SDL $CURSES -D_GNU_SOURCE=1   -ggdb3 -O0 -I. -I.. -DM2CDEBUG=3"

(
cd ..
$CXX $OPT asm.cpp -c
$CXX $OPT memmgr.cpp -c
$CXX $OPT shadowstack.cpp -c
)


#

$CXX -c vikings.exe.cpp $OPT 
$CXX -c _data.cpp $OPT 
$CXX -c vikings.exe_default_seg.cpp $OPT 
$CXX -c vikings.exe_seg000.cpp $OPT 
$CXX -c vikings.exe_seg002.cpp $OPT 
$CXX -c vikings.exe_seg003.cpp $OPT

$CXX vikings.exe.o _data.o vikings.exe_default_seg.o vikings.exe_seg000.o vikings.exe_seg002.o vikings.exe_seg003.o  ../asm.o ../memmgr.o ../shadowstack.o $OPT -o vikings




