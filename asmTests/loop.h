#ifndef TASMRECOVER_LOOP_STUBS_H__
#define TASMRECOVER_LOOP_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace loop {

#define kbegin 0x1001
#define kstart 0x1111
#define ktoto 0x1112
#define ktoto1 0x1113
#define ktoto2 0x1114
#define kfailure 0x1115
#define kexitlabel 0x1116

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy2[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class loopContext {
//public:
//      loopContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
