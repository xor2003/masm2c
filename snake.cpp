/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

#include "snake.h"
#include <curses.h>

//namespace snake {
 db SEGALIGN stack[STACK_SIZE]={0};
Memory m = {

                {0}, // heap
                };
type_data SEGALIGN data ={
"Welcome to the snake game!!", // msg
{'\n','\r','U','s','e',' ','a',',',' ','s',',',' ','d',' ','a','n','d',' ','f',' ','t','o',' ','c','o','n','t','r','o','l',' ','y','o','u','r',' ','s','n','a','k','e','\n','\r','U','s','e',' ','q',' ','a','n','y','t','i','m','e',' ','t','o',' ','q','u','i','t','\r','\n','P','r','e','s','s',' ','a','n','y',' ','k','e','y',' ','t','o',' ','c','o','n','t','i','n','u','e','$'}, // instructions
"Thanks for playing! hope you enjoyed", // quitmsg
"OOPS!! your snake died! :P ", // gameovermsg
"Score: ", // scoremsg
{'^','\n','\n'}, // head
{'*','\n',11}, // body
{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, // dummy2
1, // segmentcount
1, // fruitactive
8, // fruitx
8, // fruity
0, // gameover
0, // quit
5, // delaytime
{0,0,0,0,0}, // padding
};
type_text SEGALIGN text ={
};

X86_REGREF
X86_EREGREF

int init()
{

_indent=0;
logDebug=fopen("snake.log","w");
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

R(MOV(ss, seg_offset(stack)));
#if _TRG_BITS == 16
  esp = STACK_SIZE - 4;
  es=0;
#else
  esp = (dd)(db*)&stack[STACK_SIZE-4];
#endif

#if ! __BORLANDC__ && ! __DMC__
  log_debug("~~~ heap_size=%d para=%d heap_ofs=%d", HEAP_SIZE, (HEAP_SIZE >> 4), seg_offset(heap) );
  /* We expect ram_top as Kbytes, so convert to paragraphs */
  mcb_init(seg_offset(heap), (HEAP_SIZE >> 4) - seg_offset(heap) - 1, MCB_LAST);

 #if _SRC_BITS == 16 && ! _SRC_PROTECTED_MODE
 *(dw*)(raddr(0,0x408)) = 0x378; //LPT
 #endif

#endif

        return(0);
}




void mainproc(_offsets _i){
#define LEFT 0	// 12 left equ 0
#define TOP 2	// 13 tOp equ 2
#define ROW 20	// 14 row equ 15
#define COL 75	// 15 col equ 40
#define RIGHT LEFT+COL	// 16 right equ left+col
#define BOTTOM TOP+ROW	// 17 bottom equ top+row
	R(CALL(_main));	// 1 call _main
}



void _main(_offsets _i){
 // far
	R(MOV(ax, seg_offset(data)));	// 41 mov ax, data
	R(MOV(ds, ax));	// 42 mov ds, ax
	R(MOV(ax, 0x0b800));	// 44 mov ax, 0b800H
	R(MOV(es, ax));	// 45 mov es, ax
	R(MOV(ax, 0x0003));	// 48 mov ax, 0003H
	R(INT(0x10));	// 49 int 10H
	R(bx = offset(data,msg));	// 51 lea bx, msg
	R(MOV(dx, 0));	// 52 mov dx,00
	R(CALL(writestringat));	// 53 call writestringat
	R(dx = offset(data,instructions));	// 55 lea dx, instructions
	R(MOV(ah, 0x09));	// 56 mov ah, 09H
	R(INT(0x21));	// 57 int 21h
	R(MOV(ah, 0x07));	// 59 mov ah, 07h
	R(INT(0x21));	// 60 int 21h
	R(MOV(ax, 0x0003));	// 61 mov ax, 0003H
	R(INT(0x10));	// 62 int 10H
	R(CALL(printbox));	// 63 call printbox
L(mainloop:)
	R(CALL(_delay));	// 67 call _delay
	R(bx = offset(data,msg));	// 68 lea bx, msg
	R(MOV(dx, 0));	// 69 mov dx, 00
	R(CALL(writestringat));	// 70 call writestringat
	R(CALL(shiftsnake));	// 71 call shiftsnake
	R(CMP(data.gameover, 1));	// 72 cmp gameover,1
		R(JZ(gameover_mainloop));	// 73 je gameover_mainloop
	R(CALL(keyboardfunctions));	// 75 call keyboardfunctions
	R(CMP(data.quit, 1));	// 76 cmp quit, 1
		R(JZ(quitpressed_mainloop));	// 77 je quitpressed_mainloop
	R(CALL(fruitgeneration));	// 78 call fruitgeneration
	R(CALL(draw));	// 79 call draw
		R(JMP(mainloop));	// 83 jmp mainloop
L(gameover_mainloop:)
	R(MOV(ax, 0x0003));	// 86 mov ax, 0003H
	R(INT(0x10));	// 87 int 10H
	R(MOV(data.delaytime, 100));	// 88 mov delaytime, 100
	R(MOV(dx, 0x0000));	// 89 mov dx, 0000H
	R(bx = offset(data,gameovermsg));	// 90 lea bx, gameovermsg
	R(CALL(writestringat));	// 91 call writestringat
	R(CALL(_delay));	// 92 call _delay
		R(JMP(quit_mainloop));	// 93 jmp quit_mainloop
L(quitpressed_mainloop:)
	R(MOV(ax, 0x0003));	// 96 mov ax, 0003H
	R(INT(0x10));	// 97 int 10H
	R(MOV(data.delaytime, 100));	// 98 mov delaytime, 100
	R(MOV(dx, 0x0000));	// 99 mov dx, 0000H
	R(bx = offset(data,quitmsg));	// 100 lea bx, quitmsg
	R(CALL(writestringat));	// 101 call writestringat
	R(CALL(_delay));	// 102 call _delay
		R(JMP(quit_mainloop));	// 103 jmp quit_mainloop
L(quit_mainloop:)
	R(MOV(ax, 0x0003));	// 110 mov ax, 0003H
	R(INT(0x10));	// 111 int 10h
	R(MOV(ax, 0x4c00));	// 112 mov ax, 4c00h
	R(INT(0x21));	// 113 int 21h
}



void writestringat(_offsets _i){
	R(PUSH(dx));	// 619 push dx
	R(MOV(ax, dx));	// 620 mov ax, dx
	R(AND(ax, 0x0FF00));	// 621 and ax, 0FF00H
	R(SHR(ax, 8));	// 622 shr ax,1
	R(PUSH(bx));	// 631 push bx
	R(MOV(bh, 160));	// 632 mov bh, 160
	R(MUL1_1(bh));	// 633 mul bh
	R(POP(bx));	// 635 pop bx
	R(AND(dx, 0x0FF));	// 636 and dx, 0FFH
	R(SHL(dx, 1));	// 637 shl dx,1
	R(ADD(ax, dx));	// 638 add ax, dx
	R(MOV(di, ax));	// 639 mov di, ax
L(loop_writestringat:)
	R(MOV(al, *(raddr(ds,bx))));	// 642 mov al, [bx]
	R(TEST(al, al));	// 643 test al, al
		R(JZ(exit_writestringat));	// 644 jz exit_writestringat
mvaddch(di/160, (di/2)%80, al); refresh();
//	R(MOV(*(raddr(es,di)), al));	// 645 mov es:[di], al
	R(INC(di));	// 646 inc di
	R(INC(di));	// 647 inc di
	R(INC(bx));	// 648 inc bx
		R(JMP(loop_writestringat));	// 649 jmp loop_writestringat
L(exit_writestringat:)
	R(POP(dx));	// 654 pop dx
	R(RETN);	// 655 ret
}



void readcharat(_offsets _i){
	R(PUSH(dx));	// 585 push dx
	R(MOV(ax, dx));	// 586 mov ax, dx
	R(AND(ax, 0x0FF00));	// 587 and ax, 0FF00H
	R(SHR(ax, 8));	// 588 shr ax,1
	R(PUSH(bx));	// 596 push bx
	R(MOV(bh, 160));	// 597 mov bh, 160
	R(MUL1_1(bh));	// 598 mul bh
	R(POP(bx));	// 599 pop bx
	R(AND(dx, 0x0FF));	// 600 and dx, 0FFH
	R(SHL(dx, 1));	// 601 shl dx,1
	R(ADD(ax, dx));	// 602 add ax, dx
	R(MOV(di, ax));	// 603 mov di, ax
//	R(MOV(bl, *(raddr(es,di))));	// 604 mov bl,es:[di]
mvinnstr(di/160, (di/2)%80, (char*)&bl, 1);
	R(POP(dx));	// 605 pop dx
	R(RETN);	// 606 ret
}



void writecharat(_offsets _i){
	R(PUSH(dx));	// 547 push dx
	R(MOV(ax, dx));	// 548 mov ax, dx
	R(AND(ax, 0x0FF00));	// 549 and ax, 0FF00H
	R(SHR(ax, 8));	// 550 shr ax,1
	R(PUSH(bx));	// 560 push bx
	R(MOV(bh, 160));	// 561 mov bh, 160
	R(MUL1_1(bh));	// 562 mul bh
	R(POP(bx));	// 563 pop bx
	R(AND(dx, 0x0FF));	// 564 and dx, 0FFH
	R(SHL(dx, 1));	// 565 shl dx,1
	R(ADD(ax, dx));	// 566 add ax, dx
	R(MOV(di, ax));	// 567 mov di, ax
if (bl==0) bl=' ';
mvaddch(di/160, (di/2)%80, bl); refresh();
//	R(MOV(*(raddr(es,di)), bl));	// 568 mov es:[di], bl
	R(POP(dx));	// 569 pop dx
	R(RETN);	// 570 ret
}



void printbox(_offsets _i){
	R(MOV(dh, TOP));	// 505 mov dh, top
	R(MOV(dl, LEFT));	// 506 mov dl, left
	R(MOV(cx, COL));	// 507 mov cx, col
	R(MOV(bl, '*'));	// 508 mov bl, '*'
L(l1:)
	R(CALL(writecharat));	// 510 call writecharat
	R(INC(dl));	// 511 inc dl
		R(LOOP(l1));	// 512 loop l1
	R(MOV(cx, ROW));	// 514 mov cx, row
L(l2:)
	R(CALL(writecharat));	// 516 call writecharat
	R(INC(dh));	// 517 inc dh
		R(LOOP(l2));	// 518 loop l2
	R(MOV(cx, COL));	// 520 mov cx, col
L(l3:)
	R(CALL(writecharat));	// 522 call writecharat
	R(DEC(dl));	// 523 dec dl
		R(LOOP(l3));	// 524 loop l3
	R(MOV(cx, ROW));	// 526 mov cx, row
L(l4:)
	R(CALL(writecharat));	// 528 call writecharat
	R(DEC(dh));	// 529 dec dh
		R(LOOP(l4));	// 530 loop l4
	R(RETN);	// 532 ret
}



void shiftsnake(_offsets _i){
	R(MOV(bx, offset(data,head)));	// 358 mov bx, offset head
	ax = 0;AFFECT_ZF(0); AFFECT_SF(ax,0);	// 362 xor ax, ax
	R(MOV(al, *(raddr(ds,bx))));	// 363 mov al, [bx]
	R(PUSH(ax));	// 364 push ax
	R(INC(bx));	// 365 inc bx
	R(MOV(ax, *(dw*)(raddr(ds,bx))));	// 366 mov ax, [bx]
	R(INC(bx));	// 367 inc bx
	R(INC(bx));	// 368 inc bx
	cx = 0;AFFECT_ZF(0); AFFECT_SF(cx,0);	// 369 xor cx, cx
assert(data.gameover == 0);
L(l:)
	R(MOV(si, *(dw*)(raddr(ds,bx))));	// 371 mov si, [bx]
	R(TEST(si, *(dw*)(raddr(ds,bx))));	// 372 test si, [bx]
		R(JZ(outside));	// 373 jz outside
	R(INC(cx));	// 374 inc cx
	R(INC(bx));	// 375 inc bx
	R(MOV(dx, *(dw*)(raddr(ds,bx))));	// 376 mov dx,[bx]
assert(data.gameover == 0);
	R(MOV(*(dw*)(raddr(ds,bx)), ax));	// 377 mov [bx], ax
assert(data.gameover == 0);
	R(MOV(ax, dx));	// 378 mov ax,dx
	R(INC(bx));	// 379 inc bx
	R(INC(bx));	// 380 inc bx
		R(JMP(l));	// 381 jmp l
L(outside:)

	R(POP(ax));	// 389 pop ax
	R(PUSH(dx));	// 392 push dx
	R(bx = offset(data,head));	// 396 lea bx, head
	R(INC(bx));	// 397 inc bx
	R(MOV(dx, *(dw*)(raddr(ds,bx))));	// 398 mov dx, [bx]
	R(CMP(al, '<'));	// 400 cmp al, '<'
		R(JNZ(next_1));	// 401 jne next_1
	R(DEC(dl));	// 402 dec dl
	R(DEC(dl));	// 403 dec dl
		R(JMP(done_checking_the_head));	// 404 jmp done_checking_the_head
L(next_1:)
assert(data.gameover == 0);
	R(CMP(al, '>'));	// 406 cmp al, '>'
		R(JNZ(next_2));	// 407 jne next_2
	R(INC(dl));	// 408 inc dl
	R(INC(dl));	// 409 inc dl
		R(JMP(done_checking_the_head));	// 410 jmp done_checking_the_head
L(next_2:)
assert(data.gameover == 0);
	R(CMP(al, '^'));	// 413 cmp al, '^'
		R(JNZ(next_3));	// 414 jne next_3
	R(DEC(dh));	// 415 dec dh
		R(JMP(done_checking_the_head));	// 418 jmp done_checking_the_head
L(next_3:)
	R(INC(dh));	// 423 inc dh
L(done_checking_the_head:)
assert(data.gameover == 0);
	R(MOV(*(dw*)(raddr(ds,bx)), dx));	// 425 mov [bx],dx
	R(CALL(readcharat));	// 427 call readcharat ;dx
	R(CMP(bl, 'F'));	// 430 cmp bl, 'F'
		R(JZ(i_ate_fruit));	// 431 je i_ate_fruit
	R(MOV(cx, dx));	// 435 mov cx, dx
	R(POP(dx));	// 436 pop dx
	R(CMP(bl, '*'));	// 437 cmp bl, '*'    ;the snake bit itself, gameover
		R(JZ(game_over));	// 438 je game_over
	R(MOV(bl, 0));	// 439 mov bl, 0
	R(CALL(writecharat));	// 440 call writecharat
	R(MOV(dx, cx));	// 441 mov dx, cx
	R(CMP(dh, TOP));	// 448 cmp dh, top
		R(JZ(game_over));	// 449 je game_over
	R(CMP(dh, BOTTOM));	// 450 cmp dh, bottom
		R(JZ(game_over));	// 451 je game_over
	R(CMP(dl, LEFT));	// 452 cmp dl,left
		R(JZ(game_over));	// 453 je game_over
	R(CMP(dl, RIGHT));	// 454 cmp dl, right
		R(JZ(game_over));	// 455 je game_over
	R(RETN);	// 461 ret
L(game_over:)
	R(INC(data.gameover));	// 464 inc gameover
	R(RETN);	// 465 ret
L(i_ate_fruit:)
	R(MOV(al, data.segmentcount));	// 469 mov al, segmentcount
	ah = 0;AFFECT_ZF(0); AFFECT_SF(ah,0);	// 470 xor ah, ah
	R(bx = offset(data,body));	// 473 lea bx, body
	R(MOV(cx, 3));	// 474 mov cx, 3
	R(MUL1_2(cx));	// 475 mul cx
	R(POP(dx));	// 477 pop dx
	R(ADD(bx, ax));	// 478 add bx, ax
	R(MOV(*(raddr(ds,bx)), '*'));	// 479 mov byte ptr ds:[bx], '*'
	R(MOV(*(dw*)(raddr(ds,bx+1)), dx));	// 480 mov [bx+1], dx
	R(INC(data.segmentcount));	// 481 inc segmentcount
	R(MOV(dh, data.fruity));	// 482 mov dh, fruity
	R(MOV(dl, data.fruitx));	// 483 mov dl, fruitx
	R(MOV(bl, 0));	// 484 mov bl, 0
	R(CALL(writecharat));	// 485 call writecharat
	R(MOV(data.fruitactive, 0));	// 486 mov fruitactive, 0
	R(RETN);	// 487 ret
}



void keyboardfunctions(_offsets _i){
	R(CALL(readchar));	// 309 call readchar
	R(CMP(dl, 0));	// 310 cmp dl, 0
		R(JZ(next_14));	// 311 je next_14
	R(CMP(dl, 'w'));	// 314 cmp dl, 'w'
		R(JNZ(next_11));	// 315 jne next_11
	R(CMP(*(raddr(ds,offset(data,head))), 'v'));	// 316 cmp head, 'v'
		R(JZ(next_14));	// 317 je next_14
	R(MOV(*(raddr(ds,offset(data,head))), '^'));	// 318 mov head, '^'
	R(RETN);	// 319 ret
L(next_11:)
	R(CMP(dl, 's'));	// 321 cmp dl, 's'
		R(JNZ(next_12));	// 322 jne next_12
	R(CMP(*(raddr(ds,offset(data,head))), '^'));	// 323 cmp head, '^'
		R(JZ(next_14));	// 324 je next_14
	R(MOV(*(raddr(ds,offset(data,head))), 'v'));	// 325 mov head, 'v'
	R(RETN);	// 326 ret
L(next_12:)
	R(CMP(dl, 'a'));	// 328 cmp dl, 'a'
		R(JNZ(next_13));	// 329 jne next_13
	R(CMP(*(raddr(ds,offset(data,head))), '>'));	// 330 cmp head, '>'
		R(JZ(next_14));	// 331 je next_14
	R(MOV(*(raddr(ds,offset(data,head))), '<'));	// 332 mov head, '<'
	R(RETN);	// 333 ret
L(next_13:)
	R(CMP(dl, 'd'));	// 335 cmp dl, 'd'
		R(JNZ(next_14));	// 336 jne next_14
	R(CMP(*(raddr(ds,offset(data,head))), '<'));	// 337 cmp head, '<'
		R(JZ(next_14));	// 338 je next_14
	R(MOV(*(raddr(ds,offset(data,head))), '>'));	// 339 mov head,'>'
L(next_14:)
	R(CMP(dl, 'q'));	// 341 cmp dl, 'q'
		R(JZ(quit_keyboardfunctions));	// 342 je quit_keyboardfunctions
	R(RETN);	// 343 ret
L(quit_keyboardfunctions:)
	R(INC(data.quit));	// 346 inc quit
	R(RETN);	// 347 ret
}



void readchar(_offsets _i){
	R(MOV(ah, 0x01));	// 286 mov ah, 01H
	R(INT(0x16));	// 287 int 16H
		R(JNZ(keybdpressed));	// 288 jnz keybdpressed
	dl = 0;AFFECT_ZF(0); AFFECT_SF(dl,0);	// 289 xor dl, dl
	R(RETN);	// 290 ret
L(keybdpressed:)
	R(MOV(ah, 0x00));	// 293 mov ah, 00H
	R(INT(0x16));	// 294 int 16H
	R(MOV(dl, al));	// 295 mov dl,al
	R(RETN);	// 296 ret
}



void draw(_offsets _i){
	R(bx = offset(data,scoremsg));	// 246 lea bx, scoremsg
	R(MOV(dx, 109));	// 247 mov dx, 0109
	R(CALL(writestringat));	// 248 call writestringat
	R(ADD(dx, 7));	// 251 add dx, 7
	R(CALL(setcursorpos));	// 252 call setcursorpos
	R(MOV(al, data.segmentcount));	// 253 mov al, segmentcount
	R(DEC(al));	// 254 dec al
	ah = 0;AFFECT_ZF(0); AFFECT_SF(ah,0);	// 255 xor ah, ah
	R(CALL(dispnum));	// 256 call dispnum
	R(si = offset(data,head));	// 258 lea si, head
L(draw_loop:)
	R(MOV(bl, *(raddr(ds,si))));	// 260 mov bl, ds:[si]
	R(TEST(bl, bl));	// 261 test bl, bl
		R(JZ(out_draw));	// 262 jz out_draw
	R(MOV(dx, *(dw*)(raddr(ds,si+1))));	// 263 mov dx, ds:[si+1]
	R(CALL(writecharat));	// 264 call writecharat
	R(ADD(si, 3));	// 265 add si,3
		R(JMP(draw_loop));	// 266 jmp draw_loop
L(out_draw:)
	R(MOV(bl, 'F'));	// 269 mov bl, 'F'
	R(MOV(dh, data.fruity));	// 270 mov dh, fruity
	R(MOV(dl, data.fruitx));	// 271 mov dl, fruitx
	R(CALL(writecharat));	// 272 call writecharat
	R(MOV(data.fruitactive, 1));	// 273 mov fruitactive, 1
	R(RETN);	// 275 ret
}



void setcursorpos(_offsets _i){
	R(MOV(ah, 0x02));	// 235 mov ah, 02H
	R(PUSH(bx));	// 236 push bx
	R(MOV(bh, 0));	// 237 mov bh,0
	R(INT(0x10));	// 238 int 10h
	R(POP(bx));	// 239 pop bx
	R(RETN);	// 240 ret
}



void dispnum(_offsets _i){
	R(TEST(ax, ax));	// 212 test ax,ax
		R(JZ(retz));	// 213 jz retz
	dx = 0;AFFECT_ZF(0); AFFECT_SF(dx,0);	// 214 xor dx, dx
	R(MOV(bx, 10));	// 217 mov bx,10
	R(DIV2(bx));	// 218 div bx
	R(PUSH(dx));	// 220 push dx
	R(CALL(dispnum));	// 221 call dispnum
	R(POP(dx));	// 222 pop dx
	R(CALL(dispdigit));	// 223 call dispdigit
	R(RETN);	// 224 ret
L(retz:)
	R(MOV(ah, 2));	// 226 mov ah, 02
	R(RETN);	// 227 ret
}



void dispdigit(_offsets _i){
	R(ADD(dl, '0'));	// 205 add dl, '0'
	R(MOV(ah, 0x02));	// 206 mov ah, 02H
	R(INT(0x21));	// 207 int 21H
	R(RETN);	// 208 ret
}



void fruitgeneration(_offsets _i){
	R(MOV(ch, data.fruity));	// 142 mov ch, fruity
	R(MOV(cl, data.fruitx));	// 143 mov cl, fruitx
L(regenerate:)
	R(CMP(data.fruitactive, 1));	// 146 cmp fruitactive, 1
		R(JZ(ret_fruitactive));	// 147 je ret_fruitactive
	R(MOV(ah, 0));	// 148 mov ah, 00
	R(INT(0x1A));	// 149 int 1Ah
	R(PUSH(dx));	// 151 push dx
	R(MOV(ax, dx));	// 152 mov ax, dx
	dx = 0;AFFECT_ZF(0); AFFECT_SF(dx,0);	// 153 xor dx, dx
	bh = 0;AFFECT_ZF(0); AFFECT_SF(bh,0);	// 154 xor bh, bh
	R(MOV(bl, ROW));	// 155 mov bl, row
	R(DEC(bl));	// 156 dec bl
	R(DIV2(bx));	// 157 div bx
	R(MOV(data.fruity, dl));	// 158 mov fruity, dl
	R(INC(data.fruity));	// 159 inc fruity
	R(POP(ax));	// 162 pop ax
	R(MOV(bl, COL));	// 163 mov bl, col
	R(DEC(dl));	// 164 dec dl
	bh = 0;AFFECT_ZF(0); AFFECT_SF(bh,0);	// 165 xor bh, bh
	dx = 0;AFFECT_ZF(0); AFFECT_SF(dx,0);	// 166 xor dx, dx
	R(DIV2(bx));	// 167 div bx
	R(MOV(data.fruitx, dl));	// 168 mov fruitx, dl
	R(INC(data.fruitx));	// 169 inc fruitx
	R(CMP(data.fruitx, cl));	// 171 cmp fruitx, cl
		R(JNZ(nevermind));	// 172 jne nevermind
	R(CMP(data.fruity, ch));	// 173 cmp fruity, ch
		R(JNZ(nevermind));	// 174 jne nevermind
		R(JMP(regenerate));	// 175 jmp regenerate
L(nevermind:)
	R(MOV(al, data.fruitx));	// 177 mov al, fruitx
	R(ROR(al, 1));	// 178 ror al,1
		R(JC(regenerate));	// 179 jc regenerate
	R(ADD(data.fruity, TOP));	// 182 add fruity, toP
	R(ADD(data.fruitx, LEFT));	// 183 add fruitx, left
	R(MOV(dh, data.fruity));	// 185 mov dh, fruity
	R(MOV(dl, data.fruitx));	// 186 mov dl, fruitx
	R(CALL(readcharat));	// 187 call readcharat
	R(CMP(bl, '*'));	// 188 cmp bl, '*'
		R(JZ(regenerate));	// 189 je regenerate
	R(CMP(bl, '^'));	// 190 cmp bl, '^'
		R(JZ(regenerate));	// 191 je regenerate
	R(CMP(bl, '<'));	// 192 cmp bl, '<'
		R(JZ(regenerate));	// 193 je regenerate
	R(CMP(bl, '>'));	// 194 cmp bl, '>'
		R(JZ(regenerate));	// 195 je regenerate
	R(CMP(bl, 'v'));	// 196 cmp bl, 'v'
		R(JZ(regenerate));	// 197 je regenerate
L(ret_fruitactive:)
	R(RETN);	// 200 ret
}



void _delay(_offsets _i){
	R(MOV(ah, 0));	// 124 mov ah, 00
	R(INT(0x1A));	// 125 int 1Ah
	R(MOV(bx, dx));	// 126 mov bx, dx
L(jmp_delay:)
	R(INT(0x1A));	// 129 int 1Ah
	R(SUB(dx, bx));	// 130 sub dx, bx
	R(CMP(dl, data.delaytime));	// 132 cmp dl, delaytime
		R(JL(jmp_delay));	// 133 jl jmp_delay
	R(RETN);	// 134 ret
}


void DispatchProc(_offsets i){
__disp=i;
L(__dispatch_call:)
switch (__disp) {
                };
}



//} // End of namespace DreamGen
