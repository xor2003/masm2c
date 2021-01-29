#ifndef TASMRECOVER_MEM2_STUBS_H__
#define TASMRECOVER_MEM2_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace mem2 {

#define kbegin 0x1001
#define kstart 0x1111
#define kfailure 0x1112
#define kexitlabel 0x1113

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db a;
db b;
db cc;
db d;
db e;
db f;
char pas_de_mem[70];
char pbs1[43];
char pbs2[56];
char ascii[11];
 db dummy2[6]; // padding
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy3[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class mem2Context {
//public:
//      mem2Context() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
