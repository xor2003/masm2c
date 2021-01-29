#ifndef TASMRECOVER_TRUE_STUBS_H__
#define TASMRECOVER_TRUE_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace true {

#define kbegin 0x1001
#define k_start 0x1111
#define kstart 0x1112

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _text[16]; // segment _text

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class trueContext {
//public:
//      trueContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
