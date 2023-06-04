/* THIS IS GENERATED FILE */

        
        #include "snake.h"


namespace m2c{ m2cf* _ENTRY_POINT_ = &asmmain;}
        


 bool mainproc(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    mainproc:
    _begin:
#define left 0
	// 12 left equ 0
#define top 2
	// 13 top equ 2
#define row 15
	// 14 row equ 15
#define col 40
	// 15 col equ 40
#define right left+col
	// 16 right equ left+col
#define bottom top+row
	// 17 bottom equ top+row
	J(CALLF(asmmain,0));	J(RETN(0));
            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kmainproc: 	goto mainproc;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool asmmain(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    asmmain:
    _begin:
	R(ax = seg_offset(data););	// 40 	mov ax, data
	R(ds = ax;);	// 41 	mov ds, ax 
	R(ax = 0x0b800;);	// 43 	mov ax, 0b800H
	R(es = ax;);	// 44 	mov es, ax
	R(ax = 0x0003;);	// 47 	mov ax, 0003H
	R(_INT(0x10));	// 48 	int 10H
	R(bx = offset(data,msg));	// 50 	lea bx, msg
	R(dx = 00;);	// 51 	mov dx,00
	J(CALL(writestringat,0));	// 52 	call writestringat
	R(dx = offset(data,instructions));	// 54 	lea dx, instructions
	R(ah = 0x09;);	// 55 	mov ah, 09H
	R(_INT(0x21));	// 56 	int 21h
	R(ah = 0x07;);	// 58 	mov ah, 07h
	R(_INT(0x21));	// 59 	int 21h
	R(ax = 0x0003;);	// 60 	mov ax, 0003H
	R(_INT(0x10));	// 61 	int 10H
	J(CALL(printbox,0));	// 62     call printbox      
mainloop:
	// 4369 
	J(CALL(delay,0));	// 66     call delay             
	R(bx = offset(data,msg));	// 67     lea bx, msg
	R(dx = 00;);	// 68     mov dx, 00
	J(CALL(writestringat,0));	// 69     call writestringat
	J(CALL(shiftsnake,0));	// 70     call shiftsnake
	R(CMP(gameover, 1));	// 71     cmp gameover,1
	J(JZ(gameover_mainloop));	// 72     je gameover_mainloop
	J(CALL(keyboardfunctions,0));	// 74     call keyboardfunctions
	R(CMP(quit, 1));	// 75     cmp quit, 1
	J(JZ(quitpressed_mainloop));	// 76     je quitpressed_mainloop
	J(CALL(fruitgeneration,0));	// 77     call fruitgeneration
	J(CALL(draw,0));	// 78     call draw
	J(JMP(mainloop));	// 82     jmp mainloop
gameover_mainloop:
	// 4370 
	R(ax = 0x0003;);	// 85     mov ax, 0003H
	R(_INT(0x10));	// 86 	int 10H
	R(delaytime = 100;);	// 87     mov delaytime, 100
	R(dx = 0x0000;);	// 88     mov dx, 0000H
	R(bx = offset(data,gameovermsg));	// 89     lea bx, gameovermsg
	J(CALL(writestringat,0));	// 90     call writestringat
	J(CALL(delay,0));	// 91     call delay    
	J(JMP(quit_mainloop));	// 92     jmp quit_mainloop    
quitpressed_mainloop:
	// 4371 
	R(ax = 0x0003;);	// 95     mov ax, 0003H
	R(_INT(0x10));	// 96 	int 10H    
	R(delaytime = 100;);	// 97     mov delaytime, 100
	R(dx = 0x0000;);	// 98     mov dx, 0000H
	R(bx = offset(data,quitmsg));	// 99     lea bx, quitmsg
	J(CALL(writestringat,0));	// 100     call writestringat
	J(CALL(delay,0));	// 101     call delay    
	J(JMP(quit_mainloop));	// 102     jmp quit_mainloop    
quit_mainloop:
	// 4372 
	R(ax = 0x0003;);	// 109 mov ax, 0003H
	R(_INT(0x10));	// 110 int 10h    
	R(ax = 0x4c00;);	// 111 mov ax, 4c00h
	R(_INT(0x21));	// 112 int 21h  
	R(return delay(0, _state););
            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kmain: 	goto asmmain;
        case m2c::kgameover_mainloop: 	goto gameover_mainloop;
        case m2c::kmainloop: 	goto mainloop;
        case m2c::kquit_mainloop: 	goto quit_mainloop;
        case m2c::kquitpressed_mainloop: 	goto quitpressed_mainloop;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool delay(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    delay:
    _begin:
	R(ah = 00;);	// 123     mov ah, 00
	R(_INT(0x1A));	// 124     int 1Ah
	R(bx = dx;);	// 125     mov bx, dx
jmp_delay:
	// 4373 
	R(_INT(0x1A));	// 128     int 1Ah
	R(SUB(dx, bx));	// 129     sub dx, bx
	R(CMP(dl, delaytime));	// 131     cmp dl, delaytime                                                      
	J(JL(jmp_delay));	// 132     jl jmp_delay    
	J(RETN(0));	// 133     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kdelay: 	goto delay;
        case m2c::kjmp_delay: 	goto jmp_delay;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool fruitgeneration(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    fruitgeneration:
    _begin:
	R(ch = fruity;);	// 141     mov ch, fruity
	R(cl = fruitx;);	// 142     mov cl, fruitx
regenerate:
	// 4374 
	R(CMP(fruitactive, 1));	// 145     cmp fruitactive, 1
	J(JZ(ret_fruitactive));	// 146     je ret_fruitactive
	R(ah = 00;);	// 147     mov ah, 00
	R(_INT(0x1A));	// 148     int 1Ah
	R(PUSH(dx));	// 150     push dx
	R(ax = dx;);	// 151     mov ax, dx
	R(XOR(dx, dx));	// 152     xor dx, dx
	R(XOR(bh, bh));	// 153     xor bh, bh
	R(bl = row;);	// 154     mov bl, row
	R(DEC(bl));	// 155     dec bl
	R(DIV2(bx));	// 156     div bx
	R(fruity = dl;);	// 157     mov fruity, dl
	R(INC(fruity));	// 158     inc fruity
	R(POP(ax));	// 161     pop ax
	R(bl = col;);	// 162     mov bl, col
	R(DEC(dl));	// 163     dec dl
	R(XOR(bh, bh));	// 164     xor bh, bh
	R(XOR(dx, dx));	// 165     xor dx, dx
	R(DIV2(bx));	// 166     div bx
	R(fruitx = dl;);	// 167     mov fruitx, dl
	R(INC(fruitx));	// 168     inc fruitx
	R(CMP(fruitx, cl));	// 170     cmp fruitx, cl
	J(JNZ(nevermind));	// 171     jne nevermind
	R(CMP(fruity, ch));	// 172     cmp fruity, ch
	J(JNZ(nevermind));	// 173     jne nevermind
	J(JMP(regenerate));	// 174     jmp regenerate             
nevermind:
	// 4375 
	R(al = fruitx;);	// 176     mov al, fruitx
	R(ROR(al, 1));	// 177     ror al,1
	J(JC(regenerate));	// 178     jc regenerate
	R(ADD(fruity, top));	// 181     add fruity, top
	R(ADD(fruitx, left));	// 182     add fruitx, left 
	R(dh = fruity;);	// 184     mov dh, fruity
	R(dl = fruitx;);	// 185     mov dl, fruitx
	J(CALL(readcharat,0));	// 186     call readcharat
	R(CMP(bl, '*'));	// 187     cmp bl, '*'
	J(JZ(regenerate));	// 188     je regenerate
	R(CMP(bl, '^'));	// 189     cmp bl, '^'
	J(JZ(regenerate));	// 190     je regenerate
	R(CMP(bl, '<'));	// 191     cmp bl, '<'
	J(JZ(regenerate));	// 192     je regenerate
	R(CMP(bl, '>'));	// 193     cmp bl, '>'
	J(JZ(regenerate));	// 194     je regenerate
	R(CMP(bl, 'v'));	// 195     cmp bl, 'v'
	J(JZ(regenerate));	// 196     je regenerate    
ret_fruitactive:
	// 4376 
	J(RETN(0));	// 199     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kfruitgeneration: 	goto fruitgeneration;
        case m2c::knevermind: 	goto nevermind;
        case m2c::kregenerate: 	goto regenerate;
        case m2c::kret_fruitactive: 	goto ret_fruitactive;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool dispdigit(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    dispdigit:
    _begin:
	R(ADD(dl, '0'));	// 204     add dl, '0'
	R(ah = 0x02;);	// 205     mov ah, 02H
	R(_INT(0x21));	// 206     int 21H
	J(RETN(0));	// 207     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kdispdigit: 	goto dispdigit;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool dispnum(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    dispnum:
    _begin:
	R(TEST(ax, ax));	// 211     test ax,ax
	J(JZ(retz));	// 212     jz retz
	R(XOR(dx, dx));	// 213     xor dx, dx
	R(bx = 10;);	// 216     mov bx,10
	R(DIV2(bx));	// 217     div bx
	R(PUSH(dx));	// 219     push dx
	J(CALL(dispnum,0));	// 220     call dispnum  
	R(POP(dx));	// 221     pop dx
	J(CALL(dispdigit,0));	// 222     call dispdigit
	J(RETN(0));	// 223     ret
retz:
	// 4377 
	R(ah = 02;);	// 225     mov ah, 02  
	J(RETN(0));	// 226     ret    

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kdispnum: 	goto dispnum;
        case m2c::kretz: 	goto retz;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool setcursorpos(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    setcursorpos:
    _begin:
	R(ah = 0x02;);	// 234     mov ah, 02H
	R(PUSH(bx));	// 235     push bx
	R(bh = 0;);	// 236     mov bh,0
	R(_INT(0x10));	// 237     int 10h
	R(POP(bx));	// 238     pop bx
	J(RETN(0));	// 239     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::ksetcursorpos: 	goto setcursorpos;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool draw(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    draw:
    _begin:
	R(bx = offset(data,scoremsg));	// 245     lea bx, scoremsg
	R(dx = 0x0109;);	// 246     mov dx, 0109h
	J(CALL(writestringat,0));	// 247     call writestringat
	R(ADD(dx, 7));	// 250     add dx, 7
	J(CALL(setcursorpos,0));	// 251     call setcursorpos
	R(al = segmentcount;);	// 252     mov al, segmentcount
	R(DEC(al));	// 253     dec al
	R(XOR(ah, ah));	// 254     xor ah, ah
	J(CALL(dispnum,0));	// 255     call dispnum
	R(si = offset(data,head));	// 257     lea si, head
draw_loop:
	// 4378 
	R(MOV(bl, *(raddr(ds,si))));	// 259     mov bl, ds:[si]
	R(TEST(bl, bl));	// 260     test bl, bl
	J(JZ(out_draw));	// 261     jz out_draw
	R(MOV(dx, *(dw*)(raddr(ds,si+1))));	// 262     mov dx, ds:[si+1]
	J(CALL(writecharat,0));	// 263     call writecharat
	R(ADD(si, 3));	// 264     add si,3   
	J(JMP(draw_loop));	// 265     jmp draw_loop 
out_draw:
	// 4379 
	R(bl = 'F';);	// 268     mov bl, 'F'
	R(dh = fruity;);	// 269     mov dh, fruity
	R(dl = fruitx;);	// 270     mov dl, fruitx
	J(CALL(writecharat,0));	// 271     call writecharat
	R(fruitactive = 1;);	// 272     mov fruitactive, 1
	J(RETN(0));	// 274     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kdraw: 	goto draw;
        case m2c::kdraw_loop: 	goto draw_loop;
        case m2c::kout_draw: 	goto out_draw;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool readchar(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    readchar:
    _begin:
	R(ah = 0x01;);	// 285     mov ah, 01H
	R(_INT(0x16));	// 286     int 16H
	J(JNZ(keybdpressed));	// 287     jnz keybdpressed
	R(XOR(dl, dl));	// 288     xor dl, dl
	J(RETN(0));	// 289     ret
keybdpressed:
	// 4380 
	R(ah = 0x00;);	// 292     mov ah, 00H
	R(_INT(0x16));	// 293     int 16H
	R(dl = al;);	// 294     mov dl,al
	J(RETN(0));	// 295     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kkeybdpressed: 	goto keybdpressed;
        case m2c::kreadchar: 	goto readchar;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool keyboardfunctions(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    keyboardfunctions:
    _begin:
	J(CALL(readchar,0));	// 308     call readchar
	R(CMP(dl, 0));	// 309     cmp dl, 0
	J(JZ(next_14));	// 310     je next_14
	R(CMP(dl, 'w'));	// 313     cmp dl, 'w'
	J(JNZ(next_11));	// 314     jne next_11
	R(CMP(*(head), 'v'));	// 315     cmp head, 'v'
	J(JZ(next_14));	// 316     je next_14
	R(*(head) = '^';);	// 317     mov head, '^'
	J(RETN(0));	// 318     ret
next_11:
	// 4381 
	R(CMP(dl, 's'));	// 320     cmp dl, 's'
	J(JNZ(next_12));	// 321     jne next_12
	R(CMP(*(head), '^'));	// 322     cmp head, '^'
	J(JZ(next_14));	// 323     je next_14
	R(*(head) = 'v';);	// 324     mov head, 'v'
	J(RETN(0));	// 325     ret
next_12:
	// 4382 
	R(CMP(dl, 'a'));	// 327     cmp dl, 'a'
	J(JNZ(next_13));	// 328     jne next_13
	R(CMP(*(head), '>'));	// 329     cmp head, '>'
	J(JZ(next_14));	// 330     je next_14
	R(*(head) = '<';);	// 331     mov head, '<'
	J(RETN(0));	// 332     ret
next_13:
	// 4383 
	R(CMP(dl, 'd'));	// 334     cmp dl, 'd'
	J(JNZ(next_14));	// 335     jne next_14
	R(CMP(*(head), '<'));	// 336     cmp head, '<'
	J(JZ(next_14));	// 337     je next_14
	R(*(head) = '>';);	// 338     mov head,'>'
next_14:
	// 4384 
	R(CMP(dl, 'q'));	// 340     cmp dl, 'q'
	J(JZ(quit_keyboardfunctions));	// 341     je quit_keyboardfunctions
	J(RETN(0));	// 342     ret    
quit_keyboardfunctions:
	// 4385 
	R(INC(quit));	// 345     inc quit
	J(RETN(0));	// 346     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kkeyboardfunctions: 	goto keyboardfunctions;
        case m2c::knext_11: 	goto next_11;
        case m2c::knext_12: 	goto next_12;
        case m2c::knext_13: 	goto next_13;
        case m2c::knext_14: 	goto next_14;
        case m2c::kquit_keyboardfunctions: 	goto quit_keyboardfunctions;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool shiftsnake(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    shiftsnake:
    _begin:
	R(bx = offset(data,head););	// 358     mov bx, offset head
	R(XOR(ax, ax));	// 362     xor ax, ax
	R(MOV(al, *(raddr(ds,bx))));	// 363     mov al, [bx]
	R(PUSH(ax));	// 364     push ax
	R(INC(bx));	// 365     inc bx
	R(MOV(ax, *(dw*)(raddr(ds,bx))));	// 366     mov ax, [bx]
	R(INC(bx));	// 367     inc bx    
	R(INC(bx));	// 368     inc bx
	R(XOR(cx, cx));	// 369     xor cx, cx
l:
	// 4386 
	R(MOV(si, *(dw*)(raddr(ds,bx))));	// 371     mov si, [bx]
	R(TEST(si, *(dw*)(raddr(ds,bx))));	// 372     test si, [bx]
	J(JZ(outside));	// 373     jz outside
	R(INC(cx));	// 374     inc cx     
	R(INC(bx));	// 375     inc bx
	R(MOV(dx, *(dw*)(raddr(ds,bx))));	// 376     mov dx,[bx]
	R(MOV(*(dw*)(raddr(ds,bx)), ax));	// 377     mov [bx], ax
	R(ax = dx;);	// 378     mov ax,dx
	R(INC(bx));	// 379     inc bx
	R(INC(bx));	// 380     inc bx
	J(JMP(l));	// 381     jmp l
outside:
	// 4387 
	R(POP(ax));	// 389     pop ax
	R(PUSH(dx));	// 392     push dx
	R(bx = offset(data,head));	// 396     lea bx, head
	R(INC(bx));	// 397     inc bx
	R(MOV(dx, *(dw*)(raddr(ds,bx))));	// 398     mov dx, [bx]
	R(CMP(al, '<'));	// 400     cmp al, '<'
	J(JNZ(next_1));	// 401     jne next_1
	R(DEC(dl));	// 402     dec dl
	R(DEC(dl));	// 403     dec dl
	J(JMP(done_checking_the_head));	// 404     jmp done_checking_the_head
next_1:
	// 4388 
	R(CMP(al, '>'));	// 406     cmp al, '>'
	J(JNZ(next_2));	// 407     jne next_2                
	R(INC(dl));	// 408     inc dl 
	R(INC(dl));	// 409     inc dl
	J(JMP(done_checking_the_head));	// 410     jmp done_checking_the_head
next_2:
	// 4389 
	R(CMP(al, '^'));	// 413     cmp al, '^'
	J(JNZ(next_3));	// 414     jne next_3 
	R(DEC(dh));	// 415     dec dh               
	J(JMP(done_checking_the_head));	// 418     jmp done_checking_the_head
next_3:
	// 4390 
	R(INC(dh));	// 422     inc dh
done_checking_the_head:
	// 4391 
	R(MOV(*(dw*)(raddr(ds,bx)), dx));	// 425     mov [bx],dx
	J(CALL(readcharat,0));	// 427     call readcharat ;dx
	R(CMP(bl, 'F'));	// 430     cmp bl, 'F'
	J(JZ(i_ate_fruit));	// 431     je i_ate_fruit
	R(cx = dx;);	// 435     mov cx, dx
	R(POP(dx));	// 436     pop dx 
	R(CMP(bl, '*'));	// 437     cmp bl, '*'    ;the snake bit itself, gameover
	J(JZ(game_over));	// 438     je game_over
	R(bl = 0;);	// 439     mov bl, 0
	J(CALL(writecharat,0));	// 440     call writecharat
	R(dx = cx;);	// 441     mov dx, cx
	R(CMP(dh, top));	// 448     cmp dh, top
	J(JZ(game_over));	// 449     je game_over
	R(CMP(dh, bottom));	// 450     cmp dh, bottom
	J(JZ(game_over));	// 451     je game_over
	R(CMP(dl, left));	// 452     cmp dl,left
	J(JZ(game_over));	// 453     je game_over
	R(CMP(dl, right));	// 454     cmp dl, right
	J(JZ(game_over));	// 455     je game_over
	J(RETN(0));	// 461     ret
game_over:
	// 4392 
	R(INC(gameover));	// 463     inc gameover
	J(RETN(0));	// 464     ret
i_ate_fruit:
	// 4393 
	R(al = segmentcount;);	// 468     mov al, segmentcount
	R(XOR(ah, ah));	// 469     xor ah, ah
	R(bx = offset(data,body));	// 472     lea bx, body
	R(cx = 3;);	// 473     mov cx, 3
	R(MUL1_2(cx));	// 474     mul cx
	R(POP(dx));	// 476     pop dx
	R(ADD(bx, ax));	// 477     add bx, ax
	R(MOV(*(raddr(ds,bx)), '*'));	// 478     mov byte ptr ds:[bx], '*'
	R(MOV(*(dw*)(raddr(ds,bx+1)), dx));	// 479     mov [bx+1], dx
	R(INC(segmentcount));	// 480     inc segmentcount 
	R(dh = fruity;);	// 481     mov dh, fruity
	R(dl = fruitx;);	// 482     mov dl, fruitx
	R(bl = 0;);	// 483     mov bl, 0
	J(CALL(writecharat,0));	// 484     call writecharat
	R(fruitactive = 0;);	// 485     mov fruitactive, 0   
	J(RETN(0));	// 486     ret 

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kdone_checking_the_head: 	goto done_checking_the_head;
        case m2c::kgame_over: 	goto game_over;
        case m2c::ki_ate_fruit: 	goto i_ate_fruit;
        case m2c::kl: 	goto l;
        case m2c::knext_1: 	goto next_1;
        case m2c::knext_2: 	goto next_2;
        case m2c::knext_3: 	goto next_3;
        case m2c::koutside: 	goto outside;
        case m2c::kshiftsnake: 	goto shiftsnake;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool printbox(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    printbox:
    _begin:
	R(dh = top;);	// 504     mov dh, top
	R(dl = left;);	// 505     mov dl, left
	R(cx = col;);	// 506     mov cx, col
	R(bl = '*';);	// 507     mov bl, '*'
l1:
	// 4394 
	J(CALL(writecharat,0));	// 509     call writecharat
	R(INC(dl));	// 510     inc dl
	J(LOOP(l1));	// 511     loop l1
	R(cx = row;);	// 513     mov cx, row
l2:
	// 4395 
	J(CALL(writecharat,0));	// 515     call writecharat
	R(INC(dh));	// 516     inc dh
	J(LOOP(l2));	// 517     loop l2
	R(cx = col;);	// 519     mov cx, col
l3:
	// 4396 
	J(CALL(writecharat,0));	// 521     call writecharat
	R(DEC(dl));	// 522     dec dl
	J(LOOP(l3));	// 523     loop l3
	R(cx = row;);	// 525     mov cx, row     
l4:
	// 4397 
	J(CALL(writecharat,0));	// 527     call writecharat    
	R(DEC(dh));	// 528     dec dh 
	J(LOOP(l4));	// 529     loop l4    
	J(RETN(0));	// 531     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kl1: 	goto l1;
        case m2c::kl2: 	goto l2;
        case m2c::kl3: 	goto l3;
        case m2c::kl4: 	goto l4;
        case m2c::kprintbox: 	goto printbox;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool writecharat(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    writecharat:
    _begin:
	R(PUSH(dx));	// 547     push dx
	R(ax = dx;);	// 548     mov ax, dx
	R(AND(ax, 0x0FF00));	// 549     and ax, 0FF00H
	R(SHR(ax, 1));	// 550     shr ax,1
	R(SHR(ax, 1));	// 551     shr ax,1
	R(SHR(ax, 1));	// 552     shr ax,1
	R(SHR(ax, 1));	// 553     shr ax,1
	R(SHR(ax, 1));	// 554     shr ax,1
	R(SHR(ax, 1));	// 555     shr ax,1
	R(SHR(ax, 1));	// 556     shr ax,1
	R(SHR(ax, 1));	// 557     shr ax,1
	R(PUSH(bx));	// 560     push bx
	R(bh = 160;);	// 561     mov bh, 160
	R(MUL1_1(bh));	// 562     mul bh 
	R(POP(bx));	// 563     pop bx
	R(AND(dx, 0x0FF));	// 564     and dx, 0FFH
	R(SHL(dx, 1));	// 565     shl dx,1
	R(ADD(ax, dx));	// 566     add ax, dx
	R(di = ax;);	// 567     mov di, ax
	R(MOV(*(raddr(es,di)), bl));	// 568     mov es:[di], bl
	R(POP(dx));	// 569     pop dx
	J(RETN(0));	// 570     ret    

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kwritecharat: 	goto writecharat;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool readcharat(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    readcharat:
    _begin:
	R(PUSH(dx));	// 585     push dx
	R(ax = dx;);	// 586     mov ax, dx
	R(AND(ax, 0x0FF00));	// 587     and ax, 0FF00H
	R(SHR(ax, 1));	// 588     shr ax,1
	R(SHR(ax, 1));	// 589     shr ax,1
	R(SHR(ax, 1));	// 590     shr ax,1
	R(SHR(ax, 1));	// 591     shr ax,1
	R(SHR(ax, 1));	// 592     shr ax,1
	R(SHR(ax, 1));	// 593     shr ax,1
	R(SHR(ax, 1));	// 594     shr ax,1
	R(SHR(ax, 1));	// 595     shr ax,1    
	R(PUSH(bx));	// 596     push bx
	R(bh = 160;);	// 597     mov bh, 160
	R(MUL1_1(bh));	// 598     mul bh 
	R(POP(bx));	// 599     pop bx
	R(AND(dx, 0x0FF));	// 600     and dx, 0FFH
	R(SHL(dx, 1));	// 601     shl dx,1
	R(ADD(ax, dx));	// 602     add ax, dx
	R(di = ax;);	// 603     mov di, ax
	R(MOV(bl, *(raddr(es,di))));	// 604     mov bl,es:[di]
	R(POP(dx));	// 605     pop dx
	J(RETN(0));	// 606     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kreadcharat: 	goto readcharat;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool writestringat(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    writestringat:
    _begin:
	R(PUSH(dx));	// 619     push dx
	R(ax = dx;);	// 620     mov ax, dx
	R(AND(ax, 0x0FF00));	// 621     and ax, 0FF00H
	R(SHR(ax, 1));	// 622     shr ax,1
	R(SHR(ax, 1));	// 623     shr ax,1
	R(SHR(ax, 1));	// 624     shr ax,1
	R(SHR(ax, 1));	// 625     shr ax,1
	R(SHR(ax, 1));	// 626     shr ax,1
	R(SHR(ax, 1));	// 627     shr ax,1
	R(SHR(ax, 1));	// 628     shr ax,1
	R(SHR(ax, 1));	// 629     shr ax,1
	R(PUSH(bx));	// 631     push bx
	R(bh = 160;);	// 632     mov bh, 160
	R(MUL1_1(bh));	// 633     mul bh
	R(POP(bx));	// 635     pop bx
	R(AND(dx, 0x0FF));	// 636     and dx, 0FFH
	R(SHL(dx, 1));	// 637     shl dx,1
	R(ADD(ax, dx));	// 638     add ax, dx
	R(di = ax;);	// 639     mov di, ax
loop_writestringat:
	// 4398 
	R(MOV(al, *(raddr(ds,bx))));	// 642     mov al, [bx]
	R(TEST(al, al));	// 643     test al, al
	J(JZ(exit_writestringat));	// 644     jz exit_writestringat
	R(MOV(*(raddr(es,di)), al));	// 645     mov es:[di], al
	R(INC(di));	// 646     inc di
	R(INC(di));	// 647     inc di
	R(INC(bx));	// 648     inc bx
	J(JMP(loop_writestringat));	// 649     jmp loop_writestringat
exit_writestringat:
	// 4399 
	R(POP(dx));	// 653     pop dx
	J(RETN(0));	// 654     ret

            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
                case m2c::kexit_writestringat: 	goto exit_writestringat;
        case m2c::kloop_writestringat: 	goto loop_writestringat;
        case m2c::kwritestringat: 	goto writestringat;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
    };
}



 bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state){
    switch (__disp) {
        case m2c::kdelay: 	delay(0, _state); break;
        case m2c::kdispdigit: 	dispdigit(0, _state); break;
        case m2c::kdispnum: 	dispnum(0, _state); break;
        case m2c::kdone_checking_the_head: 	shiftsnake(__disp, _state); break;
        case m2c::kdraw: 	draw(0, _state); break;
        case m2c::kdraw_loop: 	draw(__disp, _state); break;
        case m2c::kexit_writestringat: 	writestringat(__disp, _state); break;
        case m2c::kfruitgeneration: 	fruitgeneration(0, _state); break;
        case m2c::kgame_over: 	shiftsnake(__disp, _state); break;
        case m2c::kgameover_mainloop: 	main(__disp, _state); break;
        case m2c::ki_ate_fruit: 	shiftsnake(__disp, _state); break;
        case m2c::kjmp_delay: 	delay(__disp, _state); break;
        case m2c::kkeybdpressed: 	readchar(__disp, _state); break;
        case m2c::kkeyboardfunctions: 	keyboardfunctions(0, _state); break;
        case m2c::kl: 	shiftsnake(__disp, _state); break;
        case m2c::kl1: 	printbox(__disp, _state); break;
        case m2c::kl2: 	printbox(__disp, _state); break;
        case m2c::kl3: 	printbox(__disp, _state); break;
        case m2c::kl4: 	printbox(__disp, _state); break;
        case m2c::kloop_writestringat: 	writestringat(__disp, _state); break;
        case m2c::kmain: 	asmmain(0, _state); break;
        case m2c::kmainloop: 	main(__disp, _state); break;
        case m2c::kmainproc: 	mainproc(0, _state); break;
        case m2c::knevermind: 	fruitgeneration(__disp, _state); break;
        case m2c::knext_1: 	shiftsnake(__disp, _state); break;
        case m2c::knext_11: 	keyboardfunctions(__disp, _state); break;
        case m2c::knext_12: 	keyboardfunctions(__disp, _state); break;
        case m2c::knext_13: 	keyboardfunctions(__disp, _state); break;
        case m2c::knext_14: 	keyboardfunctions(__disp, _state); break;
        case m2c::knext_2: 	shiftsnake(__disp, _state); break;
        case m2c::knext_3: 	shiftsnake(__disp, _state); break;
        case m2c::kout_draw: 	draw(__disp, _state); break;
        case m2c::koutside: 	shiftsnake(__disp, _state); break;
        case m2c::kprintbox: 	printbox(0, _state); break;
        case m2c::kquit_keyboardfunctions: 	keyboardfunctions(__disp, _state); break;
        case m2c::kquit_mainloop: 	main(__disp, _state); break;
        case m2c::kquitpressed_mainloop: 	main(__disp, _state); break;
        case m2c::kreadchar: 	readchar(0, _state); break;
        case m2c::kreadcharat: 	readcharat(0, _state); break;
        case m2c::kregenerate: 	fruitgeneration(__disp, _state); break;
        case m2c::kret_fruitactive: 	fruitgeneration(__disp, _state); break;
        case m2c::kretz: 	dispnum(__disp, _state); break;
        case m2c::ksetcursorpos: 	setcursorpos(0, _state); break;
        case m2c::kshiftsnake: 	shiftsnake(0, _state); break;
        case m2c::kwritecharat: 	writecharat(0, _state); break;
        case m2c::kwritestringat: 	writestringat(0, _state); break;
        default: m2c::log_error("Don't know how to call to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);m2c::stackDump(); abort();
     };
     return true;
}


        #include <algorithm>
        #include <iterator>
        #ifdef DOSBOX_CUSTOM
        #include <numeric>

         #define MYCOPY(x) {m2c::set_type(x);m2c::mycopy((db*)&x,(db*)&tmp999,sizeof(tmp999),#x);}

         namespace m2c {
          void   Initializer()
        #else
         #define MYCOPY(x) memcpy(&x,&tmp999,sizeof(tmp999));
         namespace {
          struct Initializer {
           Initializer()
        #endif
        {
            {char tmp999[28]="Welcome to the snake game!!";MYCOPY(msg)}
    {char tmp999[92]={'\n','\r','U','s','e',' ','a',',',' ','s',',',' ','d',' ','a','n','d',' ','f',' ','t','o',' ','c','o','n','t','r','o','l',' ','y','o','u','r',' ','s','n','a','k','e','\n','\r','U','s','e',' ','q',' ','a','n','y','t','i','m','e',' ','t','o',' ','q','u','i','t','\r','\n','P','r','e','s','s',' ','a','n','y',' ','k','e','y',' ','t','o',' ','c','o','n','t','i','n','u','e','$'};MYCOPY(instructions)}
    {char tmp999[37]="Thanks for playing! hope you enjoyed";MYCOPY(quitmsg)}
    {char tmp999[28]="OOPS!! your snake died! :P ";MYCOPY(gameovermsg)}
    {char tmp999[8]="Score: ";MYCOPY(scoremsg)}
    {char tmp999[3]={'^','\n','\n'};MYCOPY(head)}
    {db tmp999[48]={*,10,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};MYCOPY(body)}
    {db tmp999=1;MYCOPY(segmentcount)}
    {db tmp999=1;MYCOPY(fruitactive)}
    {db tmp999=8;MYCOPY(fruitx)}
    {db tmp999=8;MYCOPY(fruity)}
    {db tmp999=0;MYCOPY(gameover)}
    {db tmp999=0;MYCOPY(quit)}
    {db tmp999=5;MYCOPY(delaytime)}

        }
        #ifndef DOSBOX_CUSTOM
          };
         static const Initializer i;
        #endif
        }
        