#ifndef TASMRECOVER_JXX_STUBS_H__
#define TASMRECOVER_JXX_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace jxx {

#define kbegin 0x1001
#define kstart 0x1111
#define karbdfarbarbarbarb8 0x1112
#define karbdfarbarbarbarb9 0x1113
#define knext 0x1114
#define karbdfarbarbarbarb 0x1115
#define karbdfarbarbarbarb1 0x1116
#define karbdfarbarbarbarb2 0x1117
#define karbdfarbarbarbarb3 0x1118
#define karbdfarbarbarbarb4 0x1119
#define karbdfarbarbarbarb5 0x111a
#define karbdfarbarbarbarb6 0x111b
#define karbdfarbarbarbarb7 0x111c
#define kgood 0x111d
#define kfailure 0x111e
#define kexitlabel 0x111f

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db a[3];
db b;
 db dummy2[12]; // padding
 db _text[16]; // segment _text
dw jtable;
dw dummy3;
dw dummy4;
dw dummy5;
 db dummy6[8]; // padding
 db stackseg[16]; // segment stackseg
db dummy7[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class jxxContext {
//public:
//      jxxContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
