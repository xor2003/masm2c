#ifndef TASMRECOVER_FILE_STUBS_H__
#define TASMRECOVER_FILE_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace file {

#define kbegin 0x1001
#define k_start 0x1111
#define kstart 0x1112
#define kfailure 0x1113
#define kexitlabel 0x1114
#define kload_raw 0x1115
#define knoerror 0x1116

struct MYPACKED Memory{
 db dummy1[4096]; // protective
 db _data[16]; // segment _data
dd load_handle;
char filename[10];
db buffer[64000];
 db dummy2[2]; // padding
 db _text[16]; // segment _text
 db stackseg[16]; // segment stackseg
db dummy3[4096];

                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                };

//class fileContext {
//public:
//      fileContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
