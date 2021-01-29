#ifndef TASMRECOVER_DATA_STUBS_H__
#define TASMRECOVER_DATA_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace data {

#define kbegin 0x1001
#define k_start 0x1111
#define kstart 0x1112
#define kfailure 0x1113
#define kexitlabel 0x1114
#define kprinteax 0x1115
#define kp1 0x1116
#define kp2 0x1117

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
db beginningdata;
db var1;
dw var2;
dd var3;
db var4;
db dummy2;
dw var5[3];
dd var6[4];
dd dummy3[2];
dw dummy4[2];
char dummy5[10];
db dummy6[4];
char dummy7[8];
char dummy8[4];
dd dummy9;
char ascii[11];
char doublequote[6];
db var7[25];
db enddata;
 db dummy10[11]; // padding
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy11[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class dataContext {
//public:
//      dataContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
