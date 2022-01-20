/*
 *  x86 CPU test
 *
 *  Copyright (c) 2003 Fabrice Bellard
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, see <http://www.gnu.org/licenses/>.
 */
#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
/*
#include <string.h>
#include <inttypes.h>
#include <math.h>
#include <signal.h>
#include <setjmp.h>
#include <errno.h>
#include <sys/ucontext.h>
#include <sys/mman.h>
*/
#include <iostream>
#include <ios>

#if !defined(__x86_64__)
//#define TEST_VM86
//#define TEST_SEGS
#endif
//#define LINUX_VM86_IOPL_FIX
//#define TEST_P4_FLAGS
#ifdef __SSE__
#define TEST_SSE
#define TEST_CMOV  1
#define TEST_FCOMI 1
#else
#undef TEST_SSE
#define TEST_CMOV  1
#define TEST_FCOMI 1
#endif

#if defined(__x86_64__)
#define FMT64X "%016lx"
#define FMTLX "%016lx"
#define X86_64_ONLY(x) x
#else
#define FMT64X "%016" PRIx64
#define FMTLX "%08lx"
#define X86_64_ONLY(x)
#endif

#ifdef TEST_VM86
#include <asm/vm86.h>
#endif

#define xglue(x, y) x ## y
#define glue(x, y) xglue(x, y)
#define stringify(s)	tostring(s)
#define tostring(s)	#s

#define CC_C   	0x0001
#define CC_P 	0x0004
#define CC_A	0x0010
#define CC_Z	0x0040
#define CC_S    0x0080
#define CC_O    0x0800

#define __init_call	__attribute__ ((unused,__section__ ("initcall")))

//#define CC_MASK (CC_C | CC_P | CC_Z | CC_S | CC_O | CC_A)
#define CC_MASK (CC_C | CC_Z | CC_S | CC_O)


//--------------------------------------------
#define _BITS 32
#define _PROTECTED_MODE 1

#include <asm.h>

struct Memory
{
  db stack[STACK_SIZE];
  db heap[HEAP_SIZE];
};

static struct Memory mm;
struct Memory &m = mm;

db (&stack)[STACK_SIZE] = m.stack;
db (&heap)[HEAP_SIZE] = m.heap;


m2c::_STATE sstate;
m2c::_STATE * _state = &sstate;
     X86_REGREF
       namespace
       m2c
     {
       void
       log_debug (const char *fmt, ...)
       {
         printf ("unimp ");
       }
     }

//--------------------------------------------
#define __init_call	__attribute__ ((unused,__section__ ("initcall")))

#if defined(__x86_64__)
static
  inline
  dd
i2l (dd v)
{
  return v | ((v ^ 0xabcd) << 32);
}
#else
static
  inline
  dd
i2l (dd v)
{
  return v;
}
#endif

#undef CC_MASK
/*
#ifdef TEST_P4_FLAGS
#define CC_MASK (CC_C | CC_P | CC_Z | CC_S | CC_O | CC_A)
#else
#define CC_MASK (CC_O | CC_C)
#endif
*/
#define CC_MASK (CC_O | CC_C)

#define OP mul
//#include "test-i386-muldiv.h"

#define OP imul
//#include "test-i386-muldiv.h"

dd
test_imulb_o (dd op0, dd op1, dd & flags)
{
  dd
    res,
    s1,
    s0;
  s0 = op0;
  s1 = op1;
  res = s0;
  flags = 0;

asm ("push %4\n" "POPF;" "imul" "b %b2\n" "PUSHF;" "pop %1\n": "=a" (res), "=g" (flags):"q" (s1), "0" (res),
       "1" (flags));
  flags &= CC_MASK;
//    printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n",
//           "imulb", s0, s1, res, flags & (CC_MASK));
  return res;
}

dd
test_imulb_m (dd op0, dd op1, dd & flags)
{
  dd
    res,
    s1,
    s0;
  s0 = op0;
  s1 = op1;
  res = s0;
  flags = 0;
  eax = res;
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (IMUL1_1 ((db) s1));        // 8690 mul     cl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx
  res = eax;

  flags &= CC_MASK;
//    printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n",
//           "imulb", s0, s1, res, flags & (CC_MASK));
  return res;
}

void
test_imulw_o (dd op0h, dd op0, dd op1, dd & resh, dd & res, dd & flags)
{
  dd
    s1;
  s1 = op1;
  resh = op0h;
  res = op0;
  flags = 0;
/*
    asm ("push %5\n"
         "POPF;"
         "imulw %w3\n"
         "PUSHF;"
         "pop %1\n"
         : "=a" (res), "=g" (flags), "=d" (resh)
         : "q" (s1), "0" (res), "1" (flags), "2" (resh));
*/
  edx = resh;
  eax = res;
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (IMUL1_2 ((dw) s1));        // 8690 mul     cl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx
  resh = edx;
  res = eax;
  flags &= CC_MASK;
//    printf("%-10s AH=%08lx AL=%08lx B=%08lx RH=%08lx RL=%08lx CC=%04lx\n",
//           "imulw", op0h, op0, s1, resh, res, flags & (CC_MASK));
}

void
test_imulw_m (dd op0h, dd op0, dd op1, dd & resh, dd & res, dd & flags)
{
  dd
    s1;
  s1 = op1;
  resh = op0h;
  res = op0;
  flags = 0;

asm ("push %5\n" "POPF;" "imulw %w3\n" "PUSHF;" "pop %1\n": "=a" (res), "=g" (flags), "=d" (resh):"q" (s1), "0" (res), "1" (flags),
       "2" (resh));

  flags &= CC_MASK;
//    printf("%-10s AH=%08lx AL=%08lx B=%08lx RH=%08lx RL=%08lx CC=%04lx\n",
//           "imulw", op0h, op0, s1, resh, res, flags & (CC_MASK));
}

void
test_imull (dd op0h, dd op0, dd op1)
{
  dd
    res,
    s1,
    flags,
    resh;
  s1 = op1;
  resh = op0h;
  res = op0;
  flags = 0;
  edx = resh;
  eax = res;
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (IMUL1_4 ((dd) s1));        // 8690 mul     cl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx
  resh = edx;
  res = eax;
  printf ("%-10s AH=%08lx AL=%08lx B=%08lx RH=%08lx RL=%08lx CC=%04lx\n",
          "imull", op0h, op0, s1, resh, res, flags & (CC_MASK));
}


void
test_imulw2 (dd op0, dd op1)
{
  dd
    res,
    s1,
    s0,
    flags;
  s0 = op0;
  s1 = op1;
  res = s0;
  flags = 0;
/*
    asm volatile ("push %4\n"
         "POPF;"
         "imulw %w2, %w0\n"
         "PUSHF;"
         "pop %1\n"
         : "=q" (res), "=g" (flags)
         : "q" (s1), "0" (res), "1" (flags));
*/
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (IMUL2_2 (*(dw *) & res, (dw) s1)); // 8690 mul     cl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx

  printf ("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imulw", s0, s1, res, flags & (CC_MASK));
}

void
test_imull2 (dd op0, dd op1)
{
  dd
    res,
    s1,
    s0,
    flags;
  s0 = op0;
  s1 = op1;
  res = s0;
  flags = 0;
/*
    asm volatile ("push %4\n"
         "POPF;"
         "imull %k2, %k0\n"
         "PUSHF;"
         "pop %1\n"
         : "=q" (res), "=g" (flags)
         : "q" (s1), "0" (res), "1" (flags));
*/
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (IMUL2_4 (*(dd *) & res, (dd) s1)); // 8690 mul     cl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx

  printf ("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imull", s0, s1, res, flags & (CC_MASK));
}



dd
test_divb_o (dd op0, dd op1, dd & flags)
{
  dd
    res,
    s1,
    s0;                         //, flags;
  s0 = op0;
  s1 = op1;
  res = s0;
  flags = 0;

asm ("push %4\n" "POPF;" "div" "b %b2\n" "PUSHF;" "pop %1\n": "=a" (res), "=g" (flags):"q" (s1), "0" (res),
       "1" (flags));
  flags &= 0;
  //printf ("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "divb", s0, s1, res, flags & (0));
  return res;
}

dd
test_divb_m (dd op0, dd op1, dd & flags)
{
  dd
    res,
    s1,
    s0;                         //, flags;
  s0 = op0;
  s1 = op1;
  res = s0;
  flags = 0;
/*
    asm ("push %4\n"
         "POPF;"
         "div""b %b2\n"
         "PUSHF;"
         "pop %1\n"
         : "=a" (res), "=g" (flags)
         : "q" (s1), "0" (res), "1" (flags));
*/
  eax = res;
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (DIV1 ((db) s1));           // 9094 div     dl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx
  res = eax;
  flags &= 0;
  //printf ("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "divb", s0, s1, res, flags & (0));
  return res;
}

void
test_divw (dd op0h, dd op0, dd op1)
{
  dd
    res,
    s1,
    flags,
    resh;
  s1 = op1;
  resh = op0h;
  res = op0;
  flags = 0;
/*
    asm ("push %5\n"
         "POPF;"
         "divw %w3\n"
         "PUSHF;"
         "pop %1\n"
         : "=a" (res), "=g" (flags), "=d" (resh)
         : "q" (s1), "0" (res), "1" (flags), "2" (resh));
*/
  edx = resh;
  eax = res;
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (DIV2 ((dw) s1));           // 9094 div     dl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx
  res = eax;
  resh = edx;

  printf ("%-10s AH=%08lx AL=%08lx B=%08lx RH=%08lx RL=%08lx CC=%04lx\n",
          "divw", op0h, op0, s1, resh, res, flags & (0));
}

void
test_divl (dd op0h, dd op0, dd op1)
{
  dd
    res,
    s1,
    flags,
    resh;
  s1 = op1;
  resh = op0h;
  res = op0;
  flags = 0;
/*
    asm ("push %5\n"
         "POPF;"
         "divl %k3\n"
         "PUSHF;"
         "pop %1\n"
         : "=a" (res), "=g" (flags), "=d" (resh)
         : "q" (s1), "0" (res), "1" (flags), "2" (resh));
*/
  edx = resh;
  eax = res;
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (DIV4 ((dd) s1));           // 9094 div     dl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx
  res = eax;
  resh = edx;

  printf ("%-10s AH=%08lx AL=%08lx B=%08lx RH=%08lx RL=%08lx CC=%04lx\n",
          "divl", op0h, op0, s1, resh, res, flags & (0));
}





void
test_idivb (dd op0, dd op1)
{
  dd
    res,
    s1,
    s0,
    flags;
  s0 = op0;
  s1 = op1;
  res = s0;
  flags = 0;
  eax = res;
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (IDIV1 ((db) s1));          // 9094 div     dl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx
  res = eax;
  printf ("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "idivb", s0, s1, res, flags & (0));
}

void
test_idivw (dd op0h, dd op0, dd op1)
{
  dd
    res,
    s1,
    flags,
    resh;
  s1 = op1;
  resh = op0h;
  res = op0;
  flags = 0;
  edx = resh;
  eax = res;
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (IDIV2 ((dd) s1));          // 9094 div     dl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx
  res = eax;
  resh = edx;
  printf ("%-10s AH=%08lx AL=%08lx B=%08lx RH=%08lx RL=%08lx CC=%04lx\n",
          "idivw", op0h, op0, s1, resh, res, flags & (0));
}

void
test_idivl (dd op0h, dd op0, dd op1)
{
  dd
    res,
    s1,
    flags,
    resh;
  s1 = op1;
  resh = op0h;
  res = op0;
  flags = 0;

  edx = resh;
  eax = res;
  R (PUSH (flags));             // 8688 push    edx
  R (POPF);                     // 8689 popf
  R (IDIV4 ((dd) s1));          // 9094 div     dl
  R (PUSHF);                    // 8691 pushf
  R (POP (flags));              // 8692 pop     edx
  res = eax;
  resh = edx;
  printf ("%-10s AH=%08lx AL=%08lx B=%08lx RH=%08lx RL=%08lx CC=%04lx\n",
          "idivl", op0h, op0, s1, resh, res, flags & (0));
}


void
test_mul (void)
{
/*
    test_imulb(0x1234561d, 4);
    test_imulb(3, -4);
    test_imulb(0x80, 0x80);
    test_imulb(0x10, 0x10);

    test_imulw(0, 0x1234001d, 45);
    test_imulw(0, 23, -45);
    test_imulw(0, 0x8000, 0x8000);
    test_imulw(0, 0x100, 0x100);

    test_imull(0, 0x1234001d, 45);
    test_imull(0, 23, -45);
    test_imull(0, 0x80000000, 0x80000000);
    test_imull(0, 0x10000, 0x10000);

    test_mulb(0x1234561d, 4);
    test_mulb(3, -4);
    test_mulb(0x80, 0x80);
    test_mulb(0x10, 0x10);

    test_mulw(0, 0x1234001d, 45);
    test_mulw(0, 23, -45);
    test_mulw(0, 0x8000, 0x8000);
    test_mulw(0, 0x100, 0x100);

    test_mull(0, 0x1234001d, 45);
    test_mull(0, 23, -45);
    test_mull(0, 0x80000000, 0x80000000);
    test_mull(0, 0x10000, 0x10000);

    test_imulw2(0x1234001d, 45);
    test_imulw2(23, -45);
    test_imulw2(0x8000, 0x8000);
    test_imulw2(0x100, 0x100);

    test_imull2(0x1234001d, 45);
    test_imull2(23, -45);
    test_imull2(0x80000000, 0x80000000);
    test_imull2(0x10000, 0x10000);


    { dd res, flags, s1; flags = 0; res = 0; s1 = 0x1234; dd op0=45;
	R(PUSH(flags));R(POPF);R(IMUL3_2( *(dw *)&res,s1,op0 ));R(PUSHF);R(POP(flags));
 printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imulw im", (dd)45, (dd)0x1234, res, flags & (0));};
    { dd res, flags, s1; flags = 0; res = 0; s1 = 23; dd op0=-45;
	R(PUSH(flags));R(POPF);R(IMUL3_2( *(dw *)&res,s1,op0 ));R(PUSHF);R(POP(flags));
 printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imulw im", (dd)-45, (dd)23, res, flags & (0));};
    { dd res, flags, s1; flags = 0; res = 0; s1 = 0x80000000; dd op0=0x8000;
	R(PUSH(flags));R(POPF);R(IMUL3_2( *(dw *)&res,s1,op0 ));R(PUSHF);R(POP(flags));
 printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imulw im", (dd)0x8000, (dd)0x80000000, res, flags & (0));};
    { dd res, flags, s1; flags = 0; res = 0; s1 = 0x1000; dd op0=0x7fff;
	R(PUSH(flags));R(POPF);R(IMUL3_2( *(dw *)&res,s1,op0 ));R(PUSHF);R(POP(flags));
 printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imulw im", (dd)0x7fff, (dd)0x1000, res, flags & (0));};

    { dd res, flags, s1; flags = 0; res = 0; s1 = 0x1234;dd op0=45;
	R(PUSH(flags));R(POPF);R(IMUL3_4( *(dd *)&res,s1,op0 ));R(PUSHF);R(POP(flags));
 printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imull im", (dd)45, (dd)0x1234, res, flags & (0));};
    { dd res, flags, s1; flags = 0; res = 0; s1 = 23;dd op0=-45;
	R(PUSH(flags));R(POPF);R(IMUL3_4( *(dd *)&res,s1,op0 ));R(PUSHF);R(POP(flags));
 printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imull im", (dd)-45, (dd)23, res, flags & (0));};
    { dd res, flags, s1; flags = 0; res = 0; s1 = 0x80000000; dd op0=0x8000;
	R(PUSH(flags));R(POPF);R(IMUL3_4( *(dd *)&res,s1,op0 ));R(PUSHF);R(POP(flags));
 printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imull im", (dd)0x8000, (dd)0x80000000, res, flags & (0));};
    { dd res, flags, s1; flags = 0; res = 0; s1 = 0x1000; dd op0=0x7fff;
	R(PUSH(flags));R(POPF);R(IMUL3_4( *(dd *)&res,s1,op0 ));R(PUSHF);R(POP(flags));
 printf("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imull im", (dd)0x7fff, (dd)0x1000, res, flags & (0));};

    test_idivb(0x12341678, 0x127e);
    test_idivb(0x43210123, -5);
    test_idivb(0x12340004, -1);

    test_idivw(0, 0x12345678, 12347);
    test_idivw(0, -23223, -45);
    test_idivw(0, 0x12348000, -1);
    test_idivw(0x12343, 0x12345678, 0x81238567);

    test_idivl(0, 0x12345678, 12347);
    test_idivl(0, -233223, -45);
    test_idivl(0, 0x80000000, -1);
    test_idivl(0x12343, 0x12345678, 0x81234567);

    test_divb(0x12341678, 0x127e);
    test_divb(0x43210123, -5);
    test_divb(0x12340004, -1);

    test_divw(0, 0x12345678, 12347);
    test_divw(0, -23223, -45);
    test_divw(0, 0x12348000, -1);
    test_divw(0x12343, 0x12345678, 0x81238567);

    test_divl(0, 0x12345678, 12347);
    test_divl(0, -233223, -45);
    test_divl(0, 0x80000000, -1);
    test_divl(0x12343, 0x12345678, 0x81234567);
*/
}



int
main (int argc, char **argv)
{
  R (MOV (ss, seg_offset (stack)));
  esp = ((dd) (db *) & m.stack[STACK_SIZE - 4]);

  {
    dd
      s0 = 255;
    while (s0 != 0)
      {
        dd
          s1 = s0;
        dd
          fo = 0;
        dd
          fm = 0;
        dd
          reso = test_imulb_o (s0, s1, fo);
        dd
          resm = test_imulb_m (s0, s1, fm);
        if (resm != reso || fo != fm)
          {
            printf ("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "imulb", s0, s1, reso, fo);
          }
        s0 -= 1;
      }
  }

  {
    dd
      s0 = 255;
    while (s0 != 0)
      {
        dd
          s1 = 255;
        while (s1 != 0)
          {
            dd
              s0h = s0;
            dd
              fo = 0;
            dd
              fm = 0;
            dd
              resho = 0;
            dd
              reso = 0;
            dd
              reshm = 0;
            dd
              resm = 0;
            test_imulw_o (s0h, s0, s1, resho, reso, fo);
            test_imulw_m (s0h, s0, s1, reshm, resm, fm);
            if (reshm != resho || resm != reso || fo != fm)
              {
                printf ("%-10s AH=%08lx AL=%08lx B=%08lx RH=%08lx RL=%08lx CC=%04lx\n",
                        "imulw", s0h, s0, s1, resho, reso, fo);
              }
            s1 -= 1;
          }
        s0 -= 1;
      }
  }

  {
    dd
      s0 = 255;
    while (s0 != 0)
      {
        dd
          s1 = 255;
        while (s1 != 0)
          {
            dd
              fo = 0;
            dd
              fm = 0;
            dd
              reso = test_divb_o (s0, s1, fo);
            dd
              resm = test_divb_m (s0, s1, fm);
            if (resm != reso || fo != fm)
              {
                printf ("%-10s A=%08lx B=%08lx R=%08lx CC=%04lx\n", "divb", s0, s1, reso, fo);
              }
            s1 -= 1;
          }
        s0 -= 1;
      }
  }

 printf ("1\n");
eax=4; edx=0x640000;
MUL1_4(edx);
assert(eax==0x01900000);
assert(edx==0x000000);
 printf ("2\n");



  return 0;
}
