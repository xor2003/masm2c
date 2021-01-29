/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "true.h"
#include <curses.h>

//namespace true {


int init(struct _STATE* _state)
{
X86_REGREF

_state->_indent=0;
logDebug=fopen("true.log","w");
ecx=0;

initscr();
resize_term(25, 80);
 cbreak(); // put keys directly to program
    noecho(); // do not echo
    keypad(stdscr, TRUE); // provide keypad buttons

    if (!has_colors())
    {
        printw("Unable to use colors");
    }
        start_color();

        realtocurs();
        curs_set(0);

        refresh();

  log_debug("~~~ heap_size=%d para=%d heap_ofs=%d", HEAP_SIZE, (HEAP_SIZE >> 4), seg_offset(heap) );
  /* We expect ram_top as Kbytes, so convert to paragraphs */
  mcb_init(seg_offset(heap), (HEAP_SIZE >> 4) - seg_offset(heap) - 1, MCB_LAST);

  R(MOV(ss, seg_offset(stack)));
#if _BITS == 32
  esp = ((dd)(db*)&m.stack[STACK_SIZE - 4]);
#else
  esp=0;
  sp = STACK_SIZE - 4;
  es=0;
 *(dw*)(raddr(0,0x408)) = 0x378; //LPT
#endif

        return(0);
}

void mainproc(_offsets _i, struct _STATE* _state){
X86_REGREF
__disp=_i;
if (__disp==kbegin) goto start;
else goto __dispatch_call;
 // Procedure start() start
start:
	R(MOV(ax, 0x4C00));	// 5 MOV     AX,4C00h
	R(_INT(0x21));	// 6 INT     21h


return;
__dispatch_call:
switch (__disp) {
case kstart: 	goto start;
default: log_error("Jump/call to nothere %d\n", __disp);stackDump(_state); abort();
};
}

 
struct Memory m = {
{0}, // padding
{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, // segment _text

                {0}
                };



//} // End of namespace DreamGen
