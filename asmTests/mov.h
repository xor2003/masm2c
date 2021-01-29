#ifndef TASMRECOVER_MOV_STUBS_H__
#define TASMRECOVER_MOV_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace mov {

#define kbegin 0x1001
#define k_start 0x1111
#define kstart 0x1112
#define kfailure 0x1113
#define kexitlabel 0x1114

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db a;
dw b;
dd cc;
db d;
db e;
db f;
dd g;
db h;
db h2;
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy2[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class movContext {
//public:
//      movContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
