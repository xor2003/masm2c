#include "test_globals.h"
#ifdef R
#undef R
#endif
#ifdef T
#undef T
#endif
#include <gtest/gtest.h>

namespace m2c {
    struct Memory {
        db stack[STACK_SIZE];
        db heap[HEAP_SIZE];
    };
    struct Memory m;
    db(& stack)[STACK_SIZE] = m.stack;
    db(& heap)[HEAP_SIZE] = m.heap;
}

m2c::_STATE sstate;
m2c::_STATE* _state = &sstate;
dword eax, ebx, ecx, edx, esi, edi, esp, ebp, eip;
word ax, bx, cx, dx, si, di, sp, bp, ip;
byte al, ah, bl, bh, cl, ch, dl, dh, sil, dil, spl, bpl;
word cs, ds, es, fs, gs, ss;
bool CF, PF, AF, ZF, SF, DF, OF, IF;
m2c::eflags m2cflags(_state);
dword stackPointer, __disp, _source;

namespace {
    bool run_tests(m2c::_offsets, struct m2c::_STATE*) {
        int argc = 1;
        char* argv[] = { (char*)"instruction_tests", nullptr };
        ::testing::InitGoogleTest(&argc, argv);
        return RUN_ALL_TESTS();
    }
}

m2c::m2cf* m2c::_ENTRY_POINT_ = run_tests;