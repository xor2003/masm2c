#!/bin/sh -ex

#export CXX="g++"
#SDL=$(pkg-config --cflags --libs sdl2)
export SDL="-DNOSDL"
export CURSES="-DNOCURSES $(pkg-config --cflags --libs ncurses)"
export OPT="-std=c++11 -Wno-narrowing -mno-ms-bitfields  -Wno-multichar $SDL $CURSES -D_GNU_SOURCE=1   -ggdb3 -O0 -I. -I.. -DSHADOW_STACK -DM2CDEBUG=3"
#-D_DEFAULT_SOURCE -D_XOPEN_SOURCE=600 -DCHTYPE_16 
#  -mconsole -DSDL_MAIN_HANDLED
