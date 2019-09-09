#!/bin/sh -e
CC="C:/inertia_player/BC5/BIN/BCC.EXE"
OPT="-1- -d -Os -a16 -v -G -d -w-par -c -mh -M -IC:/inertia_player/BC5/INCLUDE -LC:/inertia_player/BC5/LIB -DDEBUG=2"
$CC $OPT asm.cpp
# $CC $OPT -S asm.cpp
$CC $OPT memmgr.cpp
cp --force $1.cpp $1_build.cpp
rm $1_build.obj $1_build.exe $1_build.asm  2>/dev/null || true
set -x
$CC $OPT -B $1_build.cpp || true
set +x
test -r $1_build.asm
perl -i -pe 's!^\s*([a-z0-9_@]+)::?!$1::!' $1_build.asm
./uasm64 -Fl=$1.lst -Zi3 $1_build.asm | grep -vi warning
cp --force $1_build.obj $1.obj
#rm $1_build.*  2>/dev/null || true
C:/inertia_player/BC5/BIN/ulink.exe -vv -s -Tde c0h.obj $1.obj asm.obj memmgr.obj,$1.exe,,gen.lib pdcurses.lib mathh.lib ch.lib | grep -vi  warning | grep -vi defined