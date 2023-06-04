/* THIS IS GENERATED FILE */

        
#ifndef __M2C_SNAKE_STUBS_H__
#define __M2C_SNAKE_STUBS_H__

#include "asm.h"



extern db& default_seg;
extern db& data;
extern char (& msg)[28];
extern char (& instructions)[92];
extern char (& quitmsg)[37];
extern char (& gameovermsg)[28];
extern char (& scoremsg)[8];
extern char (& head)[3];
extern db (& body)[48];
extern db& segmentcount;
extern db& fruitactive;
extern db& fruitx;
extern db& fruity;
extern db& gameover;
extern db& quit;
extern db& delaytime;
extern db& text;

namespace m2c{
void   Initializer();
static const dd kbegin = 0x1001;
static const dd kmainproc = 0x1002;
static const dd kmain = 0x1003;
static const dd kmainloop = 0x1004;
static const dd kgameover_mainloop = 0x1005;
static const dd kquitpressed_mainloop = 0x1006;
static const dd kquit_mainloop = 0x1007;
static const dd kdelay = 0x1008;
static const dd kjmp_delay = 0x1009;
static const dd kfruitgeneration = 0x100a;
static const dd kregenerate = 0x100b;
static const dd knevermind = 0x100c;
static const dd kret_fruitactive = 0x100d;
static const dd kdispdigit = 0x100e;
static const dd kdispnum = 0x100f;
static const dd kretz = 0x1010;
static const dd ksetcursorpos = 0x1011;
static const dd kdraw = 0x1012;
static const dd kdraw_loop = 0x1013;
static const dd kout_draw = 0x1014;
static const dd kreadchar = 0x1015;
static const dd kkeybdpressed = 0x1016;
static const dd kkeyboardfunctions = 0x1017;
static const dd knext_11 = 0x1018;
static const dd knext_12 = 0x1019;
static const dd knext_13 = 0x101a;
static const dd knext_14 = 0x101b;
static const dd kquit_keyboardfunctions = 0x101c;
static const dd kshiftsnake = 0x101d;
static const dd kl = 0x101e;
static const dd koutside = 0x101f;
static const dd knext_1 = 0x1020;
static const dd knext_2 = 0x1021;
static const dd knext_3 = 0x1022;
static const dd kdone_checking_the_head = 0x1023;
static const dd kgame_over = 0x1024;
static const dd ki_ate_fruit = 0x1025;
static const dd kprintbox = 0x1026;
static const dd kl1 = 0x1027;
static const dd kl2 = 0x1028;
static const dd kl3 = 0x1029;
static const dd kl4 = 0x102a;
static const dd kwritecharat = 0x102b;
static const dd kreadcharat = 0x102c;
static const dd kwritestringat = 0x102d;
static const dd kloop_writestringat = 0x102e;
static const dd kexit_writestringat = 0x102f;
}

bool delay(m2c::_offsets, struct m2c::_STATE*);
bool dispdigit(m2c::_offsets, struct m2c::_STATE*);
bool dispnum(m2c::_offsets, struct m2c::_STATE*);
bool draw(m2c::_offsets, struct m2c::_STATE*);
bool fruitgeneration(m2c::_offsets, struct m2c::_STATE*);
bool keyboardfunctions(m2c::_offsets, struct m2c::_STATE*);
bool asmmain(m2c::_offsets, struct m2c::_STATE*);
static bool mainproc(m2c::_offsets, struct m2c::_STATE*);
bool printbox(m2c::_offsets, struct m2c::_STATE*);
bool readchar(m2c::_offsets, struct m2c::_STATE*);
bool readcharat(m2c::_offsets, struct m2c::_STATE*);
bool setcursorpos(m2c::_offsets, struct m2c::_STATE*);
bool shiftsnake(m2c::_offsets, struct m2c::_STATE*);
bool writecharat(m2c::_offsets, struct m2c::_STATE*);
bool writestringat(m2c::_offsets, struct m2c::_STATE*);

bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state);



#endif
