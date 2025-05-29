#!/bin/sh -ex

export SDL="-DNOSDL"
export CURSES="-DNOCURSES $(pkg-config --cflags --libs ncurses)"
export CURSES="-DNOCURSES"
# Added -I../.. to include asm.h from parent directory
export OPT="-std=c++14 -Wno-narrowing -mno-ms-bitfields  -Wno-multichar -Wno-overflow $SDL $CURSES -D_GNU_SOURCE=1   -ggdb3 -O0 -I. -I.. -I../.."
