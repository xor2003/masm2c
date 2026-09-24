#ifndef TEST_GLOBALS_H
#define TEST_GLOBALS_H

#include "asm.h"

#define _BITS 32
#define _PROTECTED_MODE 1

namespace m2c {
  extern struct Memory m;
  extern db(& stack)[STACK_SIZE];
  extern db(& heap)[HEAP_SIZE];
}

extern m2c::_STATE sstate;
extern m2c::_STATE* _state;
extern dword eax, ebx, ecx, edx, esi, edi, esp, ebp, eip;
extern word ax, bx, cx, dx, si, di, sp, bp, ip;
extern byte al, ah, bl, bh, cl, ch, dl, dh, sil, dil, spl, bpl;
extern word cs, ds, es, fs, gs, ss;
extern bool CF, PF, AF, ZF, SF, DF, OF, IF;
extern m2c::eflags m2cflags;
extern dword stackPointer, __disp, _source;
extern m2c::m2cf* _ENTRY_POINT_;

#endif // TEST_GLOBALS_H