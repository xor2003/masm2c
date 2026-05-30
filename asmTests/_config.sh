# shellcheck shell=sh
#
# Shared build configuration for asmTests scripts.
# Intentionally disables SDL/curses in test builds.

SDL="${SDL:--DNOSDL}"
CURSES="${CURSES:--DNOCURSES}"
OPT="${OPT:--std=c++11 -Wno-narrowing -mno-ms-bitfields -Wno-multichar ${SDL} ${CURSES} -D_GNU_SOURCE=1 -ggdb3 -O0 -I. -I.. -DSHADOW_STACK -DM2CDEBUG=3}"

export SDL CURSES OPT
