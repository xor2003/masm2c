#ifndef TASMRECOVER_VBL_STUBS_H__
#define TASMRECOVER_VBL_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace vbl {

#define kbegin 0x1001
#define kstart 0x1111
#define karbvbl12 0x1112
#define karbvbl22 0x1113
#define kdffd 0x1114
#define karbvbl1 0x1115
#define karbvbl2 0x1116
#define kfailure 0x1117
#define kexitlabel 0x1118
#define kaffpal 0x1119
#define karbarbsaaccvaaaax 0x111a

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db pal_jeu[16];
db dummy2[16];
db dummy3[16];
db dummy4[16];
db dummy5[16];
db dummy6[16];
db dummy7[16];
db dummy8[16];
db dummy9[16];
db dummy10[16];
db dummy11[16];
db dummy12[16];
db dummy13[16];
db dummy14[16];
db dummy15[16];
db dummy16[16];
db dummy17[16];
db dummy18[16];
db dummy19[16];
db dummy20[16];
db dummy21[16];
db dummy22[16];
db dummy23[16];
db dummy24[16];
db dummy25[16];
db dummy26[16];
db dummy27[16];
db dummy28[16];
db dummy29[16];
db dummy30[16];
db dummy31[16];
db dummy32[16];
db dummy33[16];
db dummy34[16];
db dummy35[16];
db dummy36[16];
db dummy37[16];
db dummy38[16];
db dummy39[16];
db dummy40[16];
db dummy41[16];
db dummy42[16];
db dummy43[16];
db dummy44[16];
db dummy45[16];
db dummy46[16];
db dummy47[16];
db dummy48[16];
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy49[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class vblContext {
//public:
//      vblContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
