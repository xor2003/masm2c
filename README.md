MASM x86 to C translator and Inertia Player 1.22 source code.
==============
Translator may be used to port your DOS assembler code to SDL C. Since there is no working decompiler for 16 bit DOS code yet.
Your porting path:
DOS binary 16 bit real or 32 bit protected modes -> IDA Pro (disassembly) -> export assembler (masm format) -> Tasmx to compile (dosbox debugger to fix) -> MASM Converter -> C SDL source.

Key features:
- Segment memory model and 16bit offsets.
- Most of x86 instructions (except FPU) are supported (well tested with QEMU tests).
- flags: Carry, Zero, Sign are supported for most of x86 instructions.
- Some BIOS/DOS Int 10h, 21h interrupts are supported.
  Also DOS memory manager and stack.
- CGA text mode is supported using Curses (PDcurses or NCurses).

Other code reused: ASM2C (x86 instruction emulation), tasm-recover (from SCUMMVM project; highly modified), QEMU x86 test suit, FreeDOS memory manager.

To translate execute: tasm-recover masm_source.asm
License: GPL2.
Sure ASM2C is better but it written on swift and less instructions supported, also only protected mode.
TODO: add FPU instructions support.

Inertia Player 1.22
=============
Famous reverse engenerred MOD, S3M player.
Currently platform DOS (ASM), SDL (C)
There is source code for MASM, TASM Ideal and Nasm, gcc which can be built and running

TODO: fix sound on SDL, finish porting.
