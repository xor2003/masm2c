# shellcheck shell=sh
#
# Shared build configuration for asmTests scripts.
# Intentionally disables SDL/curses in test builds.

SDL="${SDL:--DNOSDL}"
CURSES="${CURSES:--DNOCURSES}"
# gnu++11 (not strict c++11): the runtime's variadic FPU macros rely on the
# GNU `, ##__VA_ARGS__` comma elision for operandless x87 forms (fld st, fxch).
OPT="${OPT:--std=gnu++11 -Wno-narrowing -mno-ms-bitfields -Wno-multichar ${SDL} ${CURSES} -D_GNU_SOURCE=1 -ggdb3 -O0 -I. -I.. -DSHADOW_STACK -DM2CDEBUG=3}"

export SDL CURSES OPT
