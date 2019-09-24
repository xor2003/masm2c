#ifndef TASMRECOVER_SNAKE_STUBS_H__
#define TASMRECOVER_SNAKE_STUBS_H__

/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "asm.h"

//namespace snake {

const dw kdummy = 1;
const dw kbegin = 0x1001;
const dw kmainproc = 0x0;
const dw k_main = 0x1111;
const dw kmainloop = 0x1112;
const dw kgameover_mainloop = 0x1113;
const dw kquitpressed_mainloop = 0x1114;
const dw kquit_mainloop = 0x1115;
const dw k_delay = 0x1116;
const dw kjmp_delay = 0x1117;
const dw kfruitgeneration = 0x1118;
const dw kregenerate = 0x1119;
const dw knevermind = 0x111a;
const dw kret_fruitactive = 0x111b;
const dw kdispdigit = 0x111c;
const dw kdispnum = 0x111d;
const dw kretz = 0x111e;
const dw ksetcursorpos = 0x111f;
const dw kdraw = 0x1120;
const dw kdraw_loop = 0x1121;
const dw kout_draw = 0x1122;
const dw kreadchar = 0x1123;
const dw kkeybdpressed = 0x1124;
const dw kkeyboardfunctions = 0x1125;
const dw knext_11 = 0x1126;
const dw knext_12 = 0x1127;
const dw knext_13 = 0x1128;
const dw knext_14 = 0x1129;
const dw kquit_keyboardfunctions = 0x112a;
const dw kshiftsnake = 0x112b;
const dw kl = 0x112c;
const dw koutside = 0x112d;
const dw knext_1 = 0x112e;
const dw knext_2 = 0x112f;
const dw knext_3 = 0x1130;
const dw kdone_checking_the_head = 0x1131;
const dw kgame_over = 0x1132;
const dw ki_ate_fruit = 0x1133;
const dw kprintbox = 0x1134;
const dw kl1 = 0x1135;
const dw kl2 = 0x1136;
const dw kl3 = 0x1137;
const dw kl4 = 0x1138;
const dw kwritecharat = 0x1139;
const dw kreadcharat = 0x113a;
const dw kwritestringat = 0x113b;
const dw kloop_writestringat = 0x113c;
const dw kexit_writestringat = 0x113d;
//namespace snake {
void mainproc(_offsets _i);
void _main(_offsets _i);
void _delay(_offsets _i);
void fruitgeneration(_offsets _i);
void dispdigit(_offsets _i);
void dispnum(_offsets _i);
void setcursorpos(_offsets _i);
void draw(_offsets _i);
void readchar(_offsets _i);
void keyboardfunctions(_offsets _i);
void shiftsnake(_offsets _i);
void printbox(_offsets _i);
void writecharat(_offsets _i);
void readcharat(_offsets _i);
void writestringat(_offsets _i);
void DispatchProc(_offsets i);
//} // End of namespace  snake
extern db SEGALIGN stack[STACK_SIZE];
                struct MYPACKED Memory{
                        db heap[HEAP_SIZE];
                };
struct MYPACKED type_data {
char msg[28];
char instructions[92];
char quitmsg[37];
char gameovermsg[28];
char scoremsg[8];
char head[3];
char body[3];
db dummy2[45];
db segmentcount;
db fruitactive;
db fruitx;
db fruity;
db gameover;
db quit;
db delaytime;
 db dummy3[5]; // padding
};
struct MYPACKED SEGALIGN type_text {
};

//class snakeContext {
//public:
//      snakeContext() {}

//      void _start();
//};

//} // End of namespace DreamGen

#endif
