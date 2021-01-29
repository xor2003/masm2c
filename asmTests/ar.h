#ifndef TASMRECOVER_AR_STUBS_H__
#define TASMRECOVER_AR_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace ar {

#define kbegin 0x1001
#define k_start 0x1111
#define kstart 0x1112

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db var1[3];
dw var2[3];
dd var3[4];
 db dummy2[7]; // padding
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy3[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class arContext {
//public:
//      arContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
