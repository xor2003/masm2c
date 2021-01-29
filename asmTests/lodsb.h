#ifndef TASMRECOVER_LODSB_STUBS_H__
#define TASMRECOVER_LODSB_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace lodsb {

#define kbegin 0x1001
#define kstart 0x1111
#define kfailure 0x1112
#define kexitlabel 0x1113

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db var1[3];
dw var2[3];
dd var3[4];
db var4[100];
char var5[4];
 db dummy2[15]; // padding
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy3[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class lodsbContext {
//public:
//      lodsbContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
