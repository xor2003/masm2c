#ifndef TASMRECOVER_INCLUDE_STUBS_H__
#define TASMRECOVER_INCLUDE_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace include {

#define kbegin 0x1001
#define k_start 0x1111
#define kstart 0x1112
#define kfailure 0x1113
#define kexitlabel 0x1114

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
 db _text[16]; // segment _text
 db some_seg[16]; // segment some_seg
 db stackseg[16]; // segment stackseg
db dummy2[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class includeContext {
//public:
//      includeContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
