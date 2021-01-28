#!/bin/sh -e
> _result.log

#export CXX="g++ -m32"
#SDL=$(pkg-config --cflags --libs sdl2)
SDL=-DNOSDL
CURSES=$(pkg-config --cflags --libs ncurses)
export OPT="-m32 -Wno-narrowing -mno-ms-bitfields  -Wno-multichar $SDL $CURSES -D_GNU_SOURCE=1   -ggdb3 -O0 -I. -I.. -DDEBUG=3"
#-D_DEFAULT_SOURCE -D_XOPEN_SOURCE=600 -DCHTYPE_16 
#  -mconsole -DSDL_MAIN_HANDLED

cd ..
$CXX $OPT asm.cpp -c
$CXX $OPT memmgr.cpp -c
cd asmTests

fail()
{
  echo "$n failed $1"
  exit 1
}

ls *.asm | \
while read name;
do 
  n=$(echo $name| perl -pe 's!\.asm!!');
#  (
echo "Testing $n:"
./_singletest.sh $n 2>&1 | tee -a _result.log || fail $?
done