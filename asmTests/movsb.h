#ifndef TASMRECOVER_MOVSB_STUBS_H__
#define TASMRECOVER_MOVSB_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace movsb {

#define kbegin 0x1001
#define k_start 0x1111
#define kstart 0x1112
#define kfintest 0x1113
#define kfailure 0x1114
#define kexitlabel 0x1115

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db dummy2[4];
db var1[3];
dw var2[3];
dd var3[4];
db var4[100];
db testoverlap[14];
char str1[5];
char str2[5];
char str3[5];
 db dummy3[2]; // padding
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy4[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class movsbContext {
//public:
//      movsbContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
