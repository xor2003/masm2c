#!/bin/sh +x
echo 		Ideal > iplay_f.asm

cat IPLAY.asm | grep -vw "nop\|xchg	bx, bx\|Ideal\|p286n\|intel_syntax\|align [248]" | \
perl -pe 's!seg dseg!dseg!; s!,\s+seg\s+!, !;s! seg ! !;s!argc\s*=\s*word\s+ptr!_argc		= word ptr!;s!argv\s*=\s*dword\s+ptr!_argv		= dword	ptr!; s!\[(bp+[^\[]*)(var|arg)(_[0-9A-F]+)([^\]]*)\]!\[ss:($1$2$3$4)\]!;s!\[((dword|word|byte) ptr bp+[^\[]*)(var|arg)(_[0-9A-F]+)([^\]]*)\]!\[ss:($1$3$4$5)\]!' \
>> iplay_f.asm
#cat iplay.asm | perl -pe 's!short !!;s! near!!;s!ret[nf]!retcode!;s!call	!call	proc !' > iplay_f.asm
#cat iplay.asm | perl -pe 's!short !!;s!__dosretax near!__dosretax far!;s!_abs near!_abs far!' > iplay_f.asm

#/cygdrive/c/Program\ Files/DOSBox-0.74/DOSBox.exe  V.BAT
./V7.bat
