#ifndef TASMRECOVER_ADDR_STUBS_H__
#define TASMRECOVER_ADDR_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace addr {

#define kbegin 0x1001
#define k_start 0x1111
#define klabel1 0x1112
#define klabel2 0x1113
#define klabel3 0x1114

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db var1[3];
dw var2[3];
dd var3[4];
 db dummy2[7]; // padding
 db _text[16]; // segment _text
dw myoffs;
dw dummy3;
dw dummy4;
 db dummy5[10]; // padding
 db seg003[16]; // segment seg003
char _a_mod_nst_669_s[56];
char _slider[10];
char dummy6[22];
db _myout[6336];
dw _word_245d4;
 db dummy7[6]; // padding
 db seg004[16]; // segment seg004
db _byte_34510[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class addrContext {
//public:
//      addrContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
