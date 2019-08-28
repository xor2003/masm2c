#!/bin/sh
CC="C:/inertia_player/BC5/BIN/BCC.EXE"
OPT="-1- -Os -a16 -v -G -d -w-par -c -mh -M -IC:/inertia_player/BC5/INCLUDE -LC:/inertia_player/BC5/LIB  -DDEBUG=3"
$CC $OPT asm.cpp
# $CC $OPT -S asm.cpp
$CC $OPT memmgr.cpp
# C:/inertia_player/BC5/BIN/CPP.EXE  $OPT $1.cpp
# $CC $OPT -S $1.cpp
cp --force $1.cpp $1_build.cpp
rm $1_build.obj $1_build.exe $1_build.asm  2>/dev/null
$CC $OPT -B $1_build.cpp
perl -i -pe 's!^\s*([a-z0-9_@]+)::?!$1::!' $1_build.asm
./uasm64 -Fl $1_build.asm
cp --force $1_build.obj $1.obj
rm $1_build.*  2>/dev/null
C:/inertia_player/BC5/BIN/ulink.exe -vv -Tde c0h.obj $1.obj asm.obj memmgr.obj,$1.exe,,gen.lib pdcurses.lib mathh.lib ch.lib