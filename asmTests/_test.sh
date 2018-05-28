#!/bin/sh
ls *.asm | while read name;do n=$(echo $name| perl -pe 's!\.asm!!');(python ../tasm-recover $name >${name}.txt && g++ ${n}.cpp -o ${n}&& ./${n}.exe )|| echo "$n failed";done