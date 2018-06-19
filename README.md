MASM x86 to C translator and Inertia Player 1.22 source code.
==============
Translator may be used to port your DOS assembler code to SDL C.
Dos binary 16real/32protected bit -> IDA Pro (disassembly) -> export assembler (masm format) -> Tasmx to compile (dosbox debugger to fix) -> MASM Converter -> C SDL source.
- Most of x86 instructions (except FPU) are supported (well tested with QEMU tests).
- flags: Carry, Zero, Sign are supported for most of instructions.
- Some Int 10h, 21h interrupts are supported.
  Also DOS memory manager and stack.
- CGA text mode is supported using Curses (PDcurses or NCurses).

Other code used: ASM2C (x86 instruction emulation), tasm_recover (from SCUMMVM project; highly modified), QEMU x86 test suit, FreeDOS memory manager.
License: GPL2.
Sure ASM2C is better but it written on swift and less instructions supported, also only protected mode.

Inertia Player 1.22
=============
Famous reverse engenerred MOD, S3M player.
Currently platform DOS, SDL (you can run it in DOSBOX)
There is source code for MASM, TASM Ideal and Nasm, gcc which can be built and running

TODO: fix sound on SDL, finish porting.
TODO: add FPU instructions support.
