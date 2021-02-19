#!/bin/sh +x
echo 		Ideal > iplay_tasm.asm
TOREMOVE='useless|gravis|wss|proaud|sbpro|sb'
#TOREMOVE='useless|mouse|midi|stereo|covox|adlib|wss|pcspeaker|proaud|sbpro|sb|gravis|inr|far|ult|psm|_669|e669'

cat IPLAY.asm | grep -vw "nop\|xchg	bx, bx\|Ideal\|p286n\|intel_syntax\|align [248]" | \
#cat IPLAY.asm | grep -vw "Ideal\|p286n\|intel_syntax" | \
perl -pe 's!seg dseg!dseg!; s!,\s+seg\s+!, !;s! seg ! !;s!argc\s*=\s*word\s+ptr!_argc		= word ptr!;s!argv\s*=\s*dword\s+ptr!_argv		= dword	ptr!; s!\[(bp+[^\[]*)(var|arg)(_[0-9A-F]+)([^\]]*)\]!\[ss:($1$2$3$4)\]!;s!\[((dword|word|byte) ptr bp+[^\[]*)(var|arg)(_[0-9A-F]+)([^\]]*)\]!\[ss:($1$3$4$5)\]!' \
| grep -vP "call\s+(useless|gravis_)|dw offset (${TOREMOVE})_|jnz\s+short gravis_13A6A" \
| perl  -pe "BEGIN{undef $/;} s/proc\s+(${TOREMOVE})_.*?(endp)\s+(${TOREMOVE})_[_A-Za-z0-9]+//smg" \
| perl -pe 's!jmp\s+\[snd_([a-z]+)_offs\+bx\]!jmp     sb16_$1!; s!\[sndcards_text_tbl\+si\]!offset sb16_txt!;' \
 >> iplay_tasm.asm
#| grep -vP "call\s+(useless|gravis_|mouse_)|dw offset (${TOREMOVE})_|jnz\s+short gravis_13A6A" \
#| perl  -pe "BEGIN{undef $/;} s/(midi_init:).*?(retn)//smg" \
#| perl  -pe "BEGIN{undef $/;} s!(dw offset mod_mk_module?)!off_25326 dw offset mod_mk_module!" \



#cat iplay.asm | perl -pe 's!short !!;s! near!!;s!ret[nf]!retcode!;s!call	!call	proc !' > iplay_tasm.asm
#cat iplay.asm | perl -pe 's!short !!;s!__dosretax near!__dosretax far!;s!_abs near!_abs far!' > iplay_tasm.asm

#/cygdrive/c/Program\ Files/DOSBox-0.74/DOSBox.exe  V.BAT
./build_tasm.bat
