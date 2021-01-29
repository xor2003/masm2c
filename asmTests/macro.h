#ifndef TASMRECOVER_MACRO_STUBS_H__
#define TASMRECOVER_MACRO_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace macro {

#define kbegin 0x1001
#define k_start 0x1111
#define kstart 0x1112
#define kcc 0x1113
#define kop 0x1114
#define kfailure 0x1115
#define kexitlabel 0x1116

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db varmac1[10];
db dummy2[10];
db last_voice;
dd changement;
dw fx[14];
 db dummy3[11]; // padding
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy4[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class macroContext {
//public:
//      macroContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
