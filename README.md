
[![Build Status](https://travis-ci.com/xor2003/masm2c.svg?branch=master)](https://travis-ci.com/xor2003/masm2c)

Masm2c - 16bit assembler to C++ translator
==============

Portable MASM or Source-to-source_compiler https://en.wikipedia.org/wiki/Source-to-source_compiler
Translator may be used to port your DOS x86 (MASM) assembler code to C++ and SDL (Since there is no working decompiler for 16 bit DOS code yet.
Because of DOS segmentation model, etc)

Translator generates pseudo assembler instructions which can be compiled with C++ compiler and executed.

[![Test drive 3](http://img.youtube.com/vi/MzK9RVgeWGM/0.jpg)](http://www.youtube.com/watch?v=MzK9RVgeWGM "Test drive 3")

[![Cryo Dune](http://img.youtube.com/vi/f-HArAmtXTc/0.jpg)](http://www.youtube.com/watch?v=f-HArAmtXTc "Cryo Dune")

etc

The following assembler example:

```assembler
_DATA   segment use16 word public 'DATA'
_msg    db 'Hello World!',10,13,'$'

_DATA   ends

_TEXT   segment use16 word public 'CODE'
  assume  cs:_TEXT,ds:_DATA
start proc near

sti                             ; Set The Interrupt Flag
cld                             ; Clear The Direction Flag
push _data
pop ds
mov ah,9                        ; AH=09h - Print DOS Message
mov dx,offset _msg             ; DS:EDX -> $ Terminated String
int 21h                         ; DOS INT 21h

mov ax,4c00h                    ; AH=4Ch - Exit To DOS
int 21h                       ; DOS INT 21h
start endp

_TEXT   ends
```

Converts to a compilable and working C++ code:

```c++
start:
	R(STI);	// 12 sti
	R(CLD);	// 13 cld
	R(PUSH(seg_offset(_data)));	// 14 push _data
	R(POP(ds));	// 15 pop ds
	R(MOV(ah, 9));	// 16 mov ah,9
	R(MOV(dx, offset(_data,_msg)));	// 17 mov dx,offset _msg
	R(_INT(0x21));	// 18 int 21h
	R(MOV(ax, 0x4c00));	// 20 mov ax,4c00h
	R(_INT(0x21));	// 21 int 21h

struct Memory m = {
{0}, // padding
{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, // segment _data
{'H','e','l','l','o',' ','W','o','r','l','d','!','\n','\r','$'}, // _msg
...
```

Optionally you can compile output of masm2c (C code) for 32 bit plarform with optimization 
and decompile to get cleaner C code without dead code like x86 flags update.

Key features:
- Most of x86 instructions (except FPU) are supported (well tested with QEMU tests).
x86 flags: Carry, Zero, Sign, Overflow are supported for most of x86 instructions.
- Segment memory model and 16bit offsets.
- Internal SDL target: Some BIOS/DOS Int 10h, 21h interrupts are supported. Also DOS memory manager and stack emulated.
  CGA text mode is supported using Curses (PDcurses or NCurses).
  VGA 320x200x256 support (partial)
- Libdosbox target: Full interrupts, hardware support.
- structures support
- parser based on Masm EBNF
- segment merging as Masm do during linking. Many .asm sources can be converted individually and linked together using modern linker

(3rd-party code used from: ASM2C (x86 instruction emulation), tasm-recover (from SCUMMVM project; highly modified), QEMU x86 instructions test suit, FreeDOS memory manager.)

License: GPL2+

TODO: 
- full macros support
- add FPU instructions support (may use linux 387 emulator)

For easier disassembling (exe to asm) you may need to collect run-time information from dosbox or other emulator to annotate IDA disassembly. Maybe modify dosbox debugger tracing mechanism to collect:
- current instruction is code
- access to memory (offset of which segment)
- segment register values
In other repo there are scripts which can help to convert DOSBOX run-time traces into IDA annotations to simplify disassembly.

Assembler source code for Stunts game https://github.com/xor2003/restunts

Assembler source code for Tornado flight sim https://github.com/xor2003/tornado-dos-flightsim

See list of DOS games with debug information http://bringerp.free.fr/forum/viewtopic.php?f=1&t=128

How to convert your masm 16 bit source to C++:
-------------------------------

Prerequisite: your code should be compilable with uasm(jwasm)/masm6, link5/tlink and work under DOS.

masm2c.py <some.asm>

(Small source code modification might also be required to translate)

IDA Pro Free you can find here https://www.scummvm.org/news/20180331/

Inertia Player 1.22 source code
=============
Famous reverse engenerred MOD, S3M player.
Currently platform DOS (ASM), SDL2 (C)
There is disassembled source code for MASM, Nasm, C which can be built and running

TODO: finish sound support on SDL, finish porting (keyboard, graphics mode,...)

Building Inertia for SDL from source:
-------------------------------
1. get PDCurses or other curses library+headers, SDL2, mingw32 + a lot of luck
2. build_mingw.bat
3. execute:
iplay_m_.exe HACKER4.S3M 

Or just get prebuilt from release page

If you want to help me please contribute or send BTC to:

BTC: bc1qyaxs8dqn7mglp9w9zyvkfpz888x3aknr0jnsmx

