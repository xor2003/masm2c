/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */

                #include "vikings.exe.h"

                

 bool _group2(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;

    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    _group2:
    _begin:
sub_1be8a:
	// 32316 
cs=0xd4f;eip=0x0003ba; 	T(CMP(bx, 0x10));	// 32318 cmp     bx, 10h ;~ 0D4F:03BA
ret_d4f_3bd:
	// 5926 
cs=0xd4f;eip=0x0003bd; 	J(JNC(loc_1beb4));	// 32319 jnb     short loc_1BEB4 ;~ 0D4F:03BD
cs=0xd4f;eip=0x0003bf; 	T(SHL(bx, 1));	// 32320 shl     bx, 1 ;~ 0D4F:03BF
cs=0xd4f;eip=0x0003c1; 	T(SHL(bx, 1));	// 32321 shl     bx, 1 ;~ 0D4F:03C1
cs=0xd4f;eip=0x0003c3; 	T(LES(bx, *(dw*)(raddr(cs,bx+0x124))));	// 32322 les     bx, cs:[bx+124h] ;~ 0D4F:03C3
cs=0xd4f;eip=0x0003c8; 	T(MOV(cx, es));	// 32323 mov     cx, es ;~ 0D4F:03C8
cs=0xd4f;eip=0x0003ca; 	T(OR(cx, bx));	// 32324 or      cx, bx ;~ 0D4F:03CA
cs=0xd4f;eip=0x0003cc; 	J(JZ(loc_1beb4));	// 32325 jz      short loc_1BEB4 ;~ 0D4F:03CC
loc_1be9e:
	// 5927 
cs=0xd4f;eip=0x0003ce; 	T(MOV(cx, *(dw*)(raddr(es,bx))));	// 32328 mov     cx, es:[bx] ;~ 0D4F:03CE
cs=0xd4f;eip=0x0003d1; 	T(CMP(cx, ax));	// 32329 cmp     cx, ax ;~ 0D4F:03D1
cs=0xd4f;eip=0x0003d3; 	J(JZ(loc_1bebb));	// 32330 jz      short loc_1BEBB ;~ 0D4F:03D3
cs=0xd4f;eip=0x0003d5; 	T(ADD(bx, 4));	// 32331 add     bx, 4 ;~ 0D4F:03D5
cs=0xd4f;eip=0x0003d8; 	T(CMP(cx, 0x0FFFF));	// 32332 cmp     cx, 0FFFFh ;~ 0D4F:03D8
cs=0xd4f;eip=0x0003db; 	J(JNZ(loc_1be9e));	// 32333 jnz     short loc_1BE9E ;~ 0D4F:03DB
cs=0xd4f;eip=0x0003dd; 	T(MOV(ax, 0));	// 32334 mov     ax, 0 ;~ 0D4F:03DD
cs=0xd4f;eip=0x0003e0; 	T(MOV(dx, 0));	// 32335 mov     dx, 0 ;~ 0D4F:03E0
cs=0xd4f;eip=0x0003e3; 	J(RETF(0));	// 32336 retf ;~ 0D4F:03E3
loc_1beb4:
	// 5928 
cs=0xd4f;eip=0x0003e4; 	T(MOV(ax, 0));	// 32341 mov     ax, 0 ;~ 0D4F:03E4
cs=0xd4f;eip=0x0003e7; 	T(MOV(dx, 0));	// 32342 mov     dx, 0 ;~ 0D4F:03E7
cs=0xd4f;eip=0x0003ea; 	J(RETF(0));	// 32343 retf ;~ 0D4F:03EA
loc_1bebb:
	// 5929 
cs=0xd4f;eip=0x0003eb; 	T(MOV(ax, *(dw*)(raddr(es,bx+2))));	// 32347 mov     ax, es:[bx+2] ;~ 0D4F:03EB
cs=0xd4f;eip=0x0003ef; 	T(MOV(dx, es));	// 32348 mov     dx, es ;~ 0D4F:03EF
cs=0xd4f;eip=0x0003f1; 	J(RETF(0));	// 32349 retf ;~ 0D4F:03F1
sub_1bec2:
	// 32356 
cs=0xd4f;eip=0x0003f2; 	T(MOV(bx, sp));	// 32358 mov     bx, sp ;~ 0D4F:03F2
ret_d4f_3f4:
	// 5930 
cs=0xd4f;eip=0x0003f4; 	T(MOV(bx, *(dw*)(raddr(ss,bx+4))));	// 32359 mov     bx, ss:[bx+4] ;~ 0D4F:03F4
cs=0xd4f;eip=0x0003f8; 	X(PUSH(cs));	// 32360 push    cs ;~ 0D4F:03F8
cs=0xd4f;eip=0x0003f9; 	J(CALL(sub_1be8a,0));	// 32361 call    near ptr sub_1BE8A ;~ 0D4F:03F9
cs=0xd4f;eip=0x0003fc; 	T(CMP(ax, 0));	// 32362 cmp     ax, 0 ;~ 0D4F:03FC
cs=0xd4f;eip=0x0003ff; 	J(JNZ(loc_1bed6));	// 32363 jnz     short loc_1BED6 ;~ 0D4F:03FF
cs=0xd4f;eip=0x000401; 	T(CMP(dx, 0));	// 32364 cmp     dx, 0 ;~ 0D4F:0401
cs=0xd4f;eip=0x000404; 	J(JZ(locret_1bed9));	// 32365 jz      short locret_1BED9 ;~ 0D4F:0404
loc_1bed6:
	// 5931 
__disp=(dx<<16)+ax;
cs=0xd4f;eip=0x000406; R(JMP(__dispatch_call));

cs=0xd4f;eip=0x000406; 	X(PUSH(dx));	// 32368 push    dx ;~ 0D4F:0406
cs=0xd4f;eip=0x000407; 	X(PUSH(ax));	// 32369 push    ax ;~ 0D4F:0407
cs=0xd4f;eip=0x000408; 	J(RETF(0));	// 32370 retf ;~ 0D4F:0408
locret_1bed9:
	// 5932 
cs=0xd4f;eip=0x000409; 	J(RETF(0));	// 32374 retf ;~ 0D4F:0409
seg002_40a_proc:
	// 32379 
loc_1beda:
	// 5933 
cs=0xd4f;eip=0x00040a; 	T(ADD(al, *(raddr(ds,bx+si))));	// 32381 add     al, [bx+si] ;~ 0D4F:040A
sub_1bedc:
	// 32386 
cs=0xd4f;eip=0x00040c; 	X(DEC(*(dw*)(raddr(cs,m2c::kloc_1beda))));	// 32387 dec     word ptr cs:loc_1BEDA ;~ 0D4F:040C
cs=0xd4f;eip=0x000411; 	J(JNZ(locret_1bf1a));	// 32388 jnz     short locret_1BF1A ;~ 0D4F:0411
cs=0xd4f;eip=0x000413; 	X(MOV(*(dw*)(raddr(cs,m2c::kloc_1beda)), 2));	// 32389 mov     word ptr cs:loc_1BEDA, 2 ;~ 0D4F:0413
cs=0xd4f;eip=0x00041a; 	T(MOV(al, 0x36));	// 32390 mov     al, 36h ; '6' ;~ 0D4F:041A
cs=0xd4f;eip=0x00041c; 	R(OUT(0x43, al));	// 32391 out     43h, al         ; Timer 8253-5 (AT: 8254.2). ;~ 0D4F:041C
cs=0xd4f;eip=0x00041e; 	T(MOV(ax, 0x7FFF));	// 32392 mov     ax, 7FFFh ;~ 0D4F:041E
cs=0xd4f;eip=0x000421; 	J({;});	// 32393 jmp     short $+2 ;~ 0D4F:0421
loc_1bef3:
	// 5934 
cs=0xd4f;eip=0x000423; 	R(OUT(0x40, al));	// 32397 out     40h, al         ; Timer 8253-5 (AT: 8254.2). ;~ 0D4F:0423
cs=0xd4f;eip=0x000425; 	T(MOV(al, ah));	// 32398 mov     al, ah ;~ 0D4F:0425
cs=0xd4f;eip=0x000427; 	J({;});	// 32399 jmp     short $+2 ;~ 0D4F:0427
loc_1bef9:
	// 5935 
cs=0xd4f;eip=0x000429; 	R(OUT(0x40, al));	// 32403 out     40h, al         ; Timer 8253-5 (AT: 8254.2). ;~ 0D4F:0429
cs=0xd4f;eip=0x00042b; 	T(MOV(dx, 0x3DA));	// 32404 mov     dx, 3DAh ;~ 0D4F:042B
loc_1befe:
	// 5936 
cs=0xd4f;eip=0x00042e; 	R(IN(al, dx));	// 32407 in      al, dx          ; Video status bits: ;~ 0D4F:042E
cs=0xd4f;eip=0x00042f; 	T(TEST(al, 8));	// 32412 test    al, 8 ;~ 0D4F:042F
cs=0xd4f;eip=0x000431; 	J(JZ(loc_1befe));	// 32413 jz      short loc_1BEFE ;~ 0D4F:0431
cs=0xd4f;eip=0x000433; 	T(MOV(al, 0x36));	// 32414 mov     al, 36h ; '6' ;~ 0D4F:0433
cs=0xd4f;eip=0x000435; 	R(OUT(0x43, al));	// 32415 out     43h, al         ; Timer 8253-5 (AT: 8254.2). ;~ 0D4F:0435
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000437; 	T(MOV(ax, *(dw*)(((db*)&word_1bbf2))));	// 32416 mov     ax, cs:word_1BBF2 ;~ 0D4F:0437
cs=0xd4f;eip=0x00043b; 	J({;});	// 32417 jmp     short $+2 ;~ 0D4F:043B
loc_1bf0d:
	// 5937 
cs=0xd4f;eip=0x00043d; 	R(OUT(0x40, al));	// 32421 out     40h, al         ; Timer 8253-5 (AT: 8254.2). ;~ 0D4F:043D
cs=0xd4f;eip=0x00043f; 	T(MOV(al, ah));	// 32422 mov     al, ah ;~ 0D4F:043F
cs=0xd4f;eip=0x000441; 	J({;});	// 32423 jmp     short $+2 ;~ 0D4F:0441
loc_1bf13:
	// 5938 
cs=0xd4f;eip=0x000443; 	R(OUT(0x40, al));	// 32427 out     40h, al         ; Timer 8253-5 (AT: 8254.2). ;~ 0D4F:0443
cs=0xd4f;eip=0x000445; 	J(CALLF(sub_1797b,0));	// 32428 call    sub_1797B ;~ 0D4F:0445
locret_1bf1a:
	// 5939 
cs=0xd4f;eip=0x00044a; 	J(RETF(0));	// 32431 retf ;~ 0D4F:044A
seg002_44b_proc:
	// 32435 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00044b; 	X(INC(*(dw*)(((db*)&word_1bad2))));	// 32435 inc     cs:word_1BAD2 ;~ 0D4F:044B
ret_d4f_450:
	// 5940 
cs=0xd4f;eip=0x000450; 	T(CLD);	// 32436 cld ;~ 0D4F:0450
cs=0xd4f;eip=0x000451; 	X(PUSH(ax));	// 32437 push    ax ;~ 0D4F:0451
cs=0xd4f;eip=0x000452; 	X(PUSH(bx));	// 32438 push    bx ;~ 0D4F:0452
cs=0xd4f;eip=0x000453; 	X(PUSH(cx));	// 32439 push    cx ;~ 0D4F:0453
cs=0xd4f;eip=0x000454; 	X(PUSH(dx));	// 32440 push    dx ;~ 0D4F:0454
cs=0xd4f;eip=0x000455; 	X(PUSH(si));	// 32441 push    si ;~ 0D4F:0455
cs=0xd4f;eip=0x000456; 	X(PUSH(di));	// 32442 push    di ;~ 0D4F:0456
cs=0xd4f;eip=0x000457; 	X(PUSH(bp));	// 32443 push    bp ;~ 0D4F:0457
cs=0xd4f;eip=0x000458; 	X(PUSH(es));	// 32444 push    es ;~ 0D4F:0458
cs=0xd4f;eip=0x000459; 	X(PUSH(ds));	// 32445 push    ds ;~ 0D4F:0459
cs=0xd4f;eip=0x00045a; 	X(PUSH(cs));	// 32446 push    cs ;~ 0D4F:045A
cs=0xd4f;eip=0x00045b; 	J(CALL(sub_1bedc,0));	// 32447 call    near ptr sub_1BEDC ;~ 0D4F:045B
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00045e; 	T(CMP(*(dw*)(((db*)&word_1bad2)), 1));	// 32448 cmp     cs:word_1BAD2, 1 ;~ 0D4F:045E
cs=0xd4f;eip=0x000464; 	J(JZ(loc_1bf39));	// 32449 jz      short loc_1BF39 ;~ 0D4F:0464
cs=0xd4f;eip=0x000466; 	J(JMP(loc_1bfc7));	// 32450 jmp     loc_1BFC7 ;~ 0D4F:0466
loc_1bf39:
	// 5941 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000469; 	X(MOV(*(dw*)((byte_1bc85)+0x1FF), ss));	// 32454 mov     word ptr cs:byte_1BC85+1FFh, ss ;~ 0D4F:0469
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00046e; 	X(MOV(*(dw*)((byte_1bc85)+0x201), sp));	// 32455 mov     word ptr cs:byte_1BC85+201h, sp ;~ 0D4F:046E
cs=0xd4f;eip=0x000473; 	T(MOV(ax, cs));	// 32456 mov     ax, cs ;~ 0D4F:0473
cs=0xd4f;eip=0x000475; 	R(MOV(ss, ax));	// 32457 mov     ss, ax ;~ 0D4F:0475
cs=0xd4f;eip=0x000477; 	T(MOV(sp, 0x3B4));	// 32459 mov     sp, 3B4h ;~ 0D4F:0477
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00047a; 	X(MOV(*(dw*)(((db*)&word_1bbec)), 0));	// 32460 mov     cs:word_1BBEC, 0 ;~ 0D4F:047A
loc_1bf51:
	// 5942 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000481; 	T(MOV(si, *(dw*)(((db*)&word_1bbec))));	// 32463 mov     si, cs:word_1BBEC ;~ 0D4F:0481
cs=0xd4f;eip=0x000486; 	T(SHL(si, 1));	// 32464 shl     si, 1 ;~ 0D4F:0486
cs=0xd4f;eip=0x000488; 	T(CMP(*(dw*)(raddr(cs,si+0x6A)), 2));	// 32465 cmp     word ptr cs:[si+6Ah], 2 ;~ 0D4F:0488
cs=0xd4f;eip=0x00048e; 	J(JNZ(loc_1bfb0));	// 32466 jnz     short loc_1BFB0 ;~ 0D4F:048E
cs=0xd4f;eip=0x000490; 	T(MOV(ds, *(dw*)(raddr(cs,si+0x48))));	// 32467 mov     ds, word ptr cs:[si+48h] ;~ 0D4F:0490
cs=0xd4f;eip=0x000495; 	T(SHL(si, 1));	// 32468 shl     si, 1 ;~ 0D4F:0495
cs=0xd4f;eip=0x000497; 	T(MOV(ax, *(dw*)(raddr(cs,si+0x8C))));	// 32469 mov     ax, cs:[si+8Ch] ;~ 0D4F:0497
cs=0xd4f;eip=0x00049c; 	T(MOV(dx, *(dw*)(raddr(cs,si+0x8E))));	// 32470 mov     dx, cs:[si+8Eh] ;~ 0D4F:049C
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0004a1; 	T(ADD(ax, *(dw*)(((db*)&word_1bbe4))));	// 32471 add     ax, cs:word_1BBE4 ;~ 0D4F:04A1
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0004a6; 	T(ADC(dx, *(dw*)(((db*)&word_1bbe6))));	// 32472 adc     dx, cs:word_1BBE6 ;~ 0D4F:04A6
cs=0xd4f;eip=0x0004ab; 	T(CMP(dx, *(dw*)(raddr(cs,si+0x0D2))));	// 32473 cmp     dx, cs:[si+0D2h] ;~ 0D4F:04AB
cs=0xd4f;eip=0x0004b0; 	J(JC(loc_1bf8b));	// 32474 jb      short loc_1BF8B ;~ 0D4F:04B0
cs=0xd4f;eip=0x0004b2; 	J(JA(loc_1bf97));	// 32475 ja      short loc_1BF97 ;~ 0D4F:04B2
cs=0xd4f;eip=0x0004b4; 	T(CMP(ax, *(dw*)(raddr(cs,si+0x0D0))));	// 32476 cmp     ax, cs:[si+0D0h] ;~ 0D4F:04B4
cs=0xd4f;eip=0x0004b9; 	J(JNC(loc_1bf97));	// 32477 jnb     short loc_1BF97 ;~ 0D4F:04B9
loc_1bf8b:
	// 5943 
cs=0xd4f;eip=0x0004bb; 	X(MOV(*(dw*)(raddr(cs,si+0x8C)), ax));	// 32480 mov     cs:[si+8Ch], ax ;~ 0D4F:04BB
cs=0xd4f;eip=0x0004c0; 	X(MOV(*(dw*)(raddr(cs,si+0x8E)), dx));	// 32481 mov     cs:[si+8Eh], dx ;~ 0D4F:04C0
cs=0xd4f;eip=0x0004c5; 	J(JMP(loc_1bfb0));	// 32482 jmp     short loc_1BFB0 ;~ 0D4F:04C5
loc_1bf97:
	// 5944 
cs=0xd4f;eip=0x0004c7; 	T(SUB(ax, *(dw*)(raddr(cs,si+0x0D0))));	// 32487 sub     ax, cs:[si+0D0h] ;~ 0D4F:04C7
cs=0xd4f;eip=0x0004cc; 	T(SBB(dx, *(dw*)(raddr(cs,si+0x0D2))));	// 32488 sbb     dx, cs:[si+0D2h] ;~ 0D4F:04CC
cs=0xd4f;eip=0x0004d1; 	X(MOV(*(dw*)(raddr(cs,si+0x8C)), ax));	// 32489 mov     cs:[si+8Ch], ax ;~ 0D4F:04D1
cs=0xd4f;eip=0x0004d6; 	X(MOV(*(dw*)(raddr(cs,si+0x8E)), dx));	// 32490 mov     cs:[si+8Eh], dx ;~ 0D4F:04D6
cs=0xd4f;eip=0x0004db; 	J(CALLF(__dispatch_call,*(dd*)(raddr(cs,si+4))));	// 32491 call    dword ptr cs:[si+4] ;~ 0D4F:04DB
loc_1bfb0:
	// 5945 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0004e0; 	X(INC(*(dw*)(((db*)&word_1bbec))));	// 32495 inc     cs:word_1BBEC ;~ 0D4F:04E0
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0004e5; 	T(CMP(*(dw*)(((db*)&word_1bbec)), 0x10));	// 32496 cmp     cs:word_1BBEC, 10h ;~ 0D4F:04E5
cs=0xd4f;eip=0x0004eb; 	J(JBE(loc_1bf51));	// 32497 jbe     short loc_1BF51 ;~ 0D4F:04EB
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0004ed; 	R(MOV(ss, *(dw*)((byte_1bc85)+0x1FF)));	// 32498 mov     ss, word ptr cs:byte_1BC85+1FFh ;~ 0D4F:04ED
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0004f2; 	T(MOV(sp, *(dw*)((byte_1bc85)+0x201)));	// 32500 mov     sp, word ptr cs:byte_1BC85+201h ;~ 0D4F:04F2
loc_1bfc7:
	// 5946 
cs=0xd4f;eip=0x0004f7; 	X(POP(ds));	// 32503 pop     ds ;~ 0D4F:04F7
cs=0xd4f;eip=0x0004f8; 	X(POP(es));	// 32504 pop     es ;~ 0D4F:04F8
cs=0xd4f;eip=0x0004f9; 	X(POP(bp));	// 32505 pop     bp ;~ 0D4F:04F9
cs=0xd4f;eip=0x0004fa; 	X(POP(di));	// 32506 pop     di ;~ 0D4F:04FA
cs=0xd4f;eip=0x0004fb; 	X(POP(si));	// 32507 pop     si ;~ 0D4F:04FB
cs=0xd4f;eip=0x0004fc; 	X(POP(dx));	// 32508 pop     dx ;~ 0D4F:04FC
cs=0xd4f;eip=0x0004fd; 	X(POP(cx));	// 32509 pop     cx ;~ 0D4F:04FD
cs=0xd4f;eip=0x0004fe; 	X(POP(bx));	// 32510 pop     bx ;~ 0D4F:04FE
cs=0xd4f;eip=0x0004ff; 	T(MOV(al, 0x20));	// 32511 mov     al, 20h ; ' ' ;~ 0D4F:04FF
cs=0xd4f;eip=0x000501; 	R(OUT(0x20, al));	// 32512 out     20h, al         ; Interrupt controller, 8259A. ;~ 0D4F:0501
cs=0xd4f;eip=0x000503; 	X(POP(ax));	// 32513 pop     ax ;~ 0D4F:0503
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000504; 	T(CMP(*(dw*)((atest)), 0x6554));	// 32514 cmp     word ptr cs:aTest, 6554h ; "Test" ;~ 0D4F:0504
cs=0xd4f;eip=0x00050b; 	J(JNZ(loc_1bfec));	// 32515 jnz     short loc_1BFEC ;~ 0D4F:050B
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00050d; 	T(CMP(*(dw*)((atest)+2), 0x7473));	// 32516 cmp     word ptr cs:aTest+2, 7473h ; "st" ;~ 0D4F:050D
cs=0xd4f;eip=0x000514; 	J(JNZ(loc_1bfec));	// 32517 jnz     short loc_1BFEC ;~ 0D4F:0514
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000516; 	X(DEC(*(dw*)(((db*)&word_1bad2))));	// 32518 dec     cs:word_1BAD2 ;~ 0D4F:0516
cs=0xd4f;eip=0x00051b; 	R(IRET);	// 32519 iret ;~ 0D4F:051B
loc_1bfec:
	// 5947 
cs=0xd4f;eip=0x00051c; 	T(MOV(ax, 0x2DBA));	// 32524 mov     ax, 2DBAh ;~ 0D4F:051C
cs=0xd4f;eip=0x00051f; 	T(XOR(bx, bx));	// 32525 xor     bx, bx ;~ 0D4F:051F
cs=0xd4f;eip=0x000521; 	J(CALLF(sub_10dba,0));	// 32526 call    far ptr sub_10DBA ;~ 0D4F:0521
cs=0xd4f;eip=0x000526; 	J(JMP(loc_1bfec));	// 32528 jmp     short loc_1BFEC ;~ 0D4F:0526
sub_1bff8:
	// 32533 
cs=0xd4f;eip=0x000528; 	X(PUSH(ds));	// 32534 push    ds ;~ 0D4F:0528
ret_d4f_529:
	// 5948 
cs=0xd4f;eip=0x000529; 	X(PUSH(si));	// 32535 push    si ;~ 0D4F:0529
cs=0xd4f;eip=0x00052a; 	X(PUSH(di));	// 32536 push    di ;~ 0D4F:052A
cs=0xd4f;eip=0x00052b; 	X(PUSHF);	// 32537 pushf ;~ 0D4F:052B
cs=0xd4f;eip=0x00052c; 	T(CLI);	// 32538 cli ;~ 0D4F:052C
cs=0xd4f;eip=0x00052d; 	T(CLD);	// 32539 cld ;~ 0D4F:052D
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00052e; 	X(MOV(*(dw*)(((db*)&word_1bbe4)), 0x0FFFF));	// 32540 mov     cs:word_1BBE4, 0FFFFh ;~ 0D4F:052E
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000535; 	X(MOV(*(dw*)(((db*)&word_1bbe6)), 0x0FFFF));	// 32541 mov     cs:word_1BBE6, 0FFFFh ;~ 0D4F:0535
cs=0xd4f;eip=0x00053c; 	X(PUSH(cs));	// 32542 push    cs ;~ 0D4F:053C
cs=0xd4f;eip=0x00053d; 	X(POP(es));	// 32543 pop     es ;~ 0D4F:053D
cs=0xd4f;eip=0x00053e; 	T(MOV(di, 0x6A));	// 32545 mov     di, 6Ah ; 'j' ;~ 0D4F:053E
cs=0xd4f;eip=0x000541; 	T(MOV(cx, 0x11));	// 32546 mov     cx, 11h ;~ 0D4F:0541
cs=0xd4f;eip=0x000544; 	T(MOV(ax, 0));	// 32547 mov     ax, 0 ;~ 0D4F:0544
	// 32548 rep stosw ;~ 0D4F:0547
cs=0xd4f;eip=0x000547; 	X(	REP STOSW);	// 32548 rep stosw ;~ 0D4F:0547
cs=0xd4f;eip=0x000549; 	T(MOV(di, 0x8C));	// 32549 mov     di, 8Ch ; 'Œ' ;~ 0D4F:0549
cs=0xd4f;eip=0x00054c; 	T(MOV(cx, 0x22));	// 32550 mov     cx, 22h ; '"' ;~ 0D4F:054C
	// 32551 rep stosw ;~ 0D4F:054F
cs=0xd4f;eip=0x00054f; 	X(	REP STOSW);	// 32551 rep stosw ;~ 0D4F:054F
cs=0xd4f;eip=0x000551; 	T(MOV(di, 0x0D0));	// 32552 mov     di, 0D0h ; 'Ð' ;~ 0D4F:0551
cs=0xd4f;eip=0x000554; 	T(MOV(cx, 0x22));	// 32553 mov     cx, 22h ; '"' ;~ 0D4F:0554
	// 32554 rep stosw ;~ 0D4F:0557
cs=0xd4f;eip=0x000557; 	X(	REP STOSW);	// 32554 rep stosw ;~ 0D4F:0557
loc_1c029:
	// 5949 
cs=0xd4f;eip=0x000559; //  	T(OR(bh, 0));	// 32557 or      bh, 0 ;~ 0D4F:0559
seg002_55c_proc:
	// 32560 
//cs=0xd4f;eip=0x00055c; 	X(PUSH(cs));	// 32560 push    cs ;~ 0D4F:055C
//cs=0xd4f;eip=0x00055d; 	J(CALL(_group2,m2c::kloc_1c029));	// 32561 call    near ptr loc_1C029+1 ;~ 0D4F:055D
R(POPF);
cs=0xd4f;eip=0x000560; 	X(POP(di));	// 32562 pop     di ;~ 0D4F:0560
cs=0xd4f;eip=0x000561; 	X(POP(si));	// 32563 pop     si ;~ 0D4F:0561
cs=0xd4f;eip=0x000562; 	X(POP(ds));	// 32564 pop     ds ;~ 0D4F:0562
cs=0xd4f;eip=0x000563; 	J(RETF(0));	// 32565 retf ;~ 0D4F:0563
ret_d4f_564:
	// 5950 
cs=0xd4f;eip=0x000564; 	X(PUSHF);	// 32567 pushf ;~ 0D4F:0564
	cs=seg_offset(seg002);
//x0r
cs=0xd4f;eip=0x000565; 	J(CALLF(__dispatch_call,*(dd*)(((db*)&dword_1bbe8))));	// 32568 call    cs:dword_1BBE8 ;~ 0D4F:0565
cs=0xd4f;eip=0x00056a; 	J(RETF(0));	// 32569 retf ;~ 0D4F:056A
sub_1c03b:
	// 32574 
cs=0xd4f;eip=0x00056b; 	X(PUSH(ds));	// 32575 push    ds ;~ 0D4F:056B
ret_d4f_56c:
	// 5951 
cs=0xd4f;eip=0x00056c; 	X(PUSH(si));	// 32576 push    si ;~ 0D4F:056C
cs=0xd4f;eip=0x00056d; 	X(PUSH(di));	// 32577 push    di ;~ 0D4F:056D
cs=0xd4f;eip=0x00056e; 	X(PUSHF);	// 32578 pushf ;~ 0D4F:056E
cs=0xd4f;eip=0x00056f; 	T(CLI);	// 32579 cli ;~ 0D4F:056F
cs=0xd4f;eip=0x000570; 	T(MOV(ax, 0));	// 32580 mov     ax, 0 ;~ 0D4F:0570
cs=0xd4f;eip=0x000573; 	T(MOV(es, ax));	// 32581 mov     es, ax ;~ 0D4F:0573
cs=0xd4f;eip=0x000575; 	T(MOV(bx, *(dw*)(raddr(es,0x20))));	// 32583 mov     bx, es:20h ;~ 0D4F:0575
cs=0xd4f;eip=0x00057a; 	T(MOV(es, *(dw*)(raddr(es,0x22))));	// 32584 mov     es, word ptr es:22h ;~ 0D4F:057A
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00057f; 	X(MOV(*(dw*)(((db*)&dword_1bbe8)), bx));	// 32586 mov     word ptr cs:dword_1BBE8, bx ;~ 0D4F:057F
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000584; 	X(MOV(*(dw*)(((db*)&dword_1bbe8)+2), es));	// 32587 mov     word ptr cs:dword_1BBE8+2, es ;~ 0D4F:0584
cs=0xd4f;eip=0x000589; 	T(MOV(bx, 0x564));	// 32588 mov     bx, 564h ;~ 0D4F:0589
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00058c; 	X(MOV(*(dw*)(((db*)&word_1bb14)), bx));	// 32589 mov     cs:word_1BB14, bx ;~ 0D4F:058C
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000591; 	X(MOV(*(dw*)(((db*)&word_1bb16)), cs));	// 32590 mov     cs:word_1BB16, cs ;~ 0D4F:0591
cs=0xd4f;eip=0x000596; 	T(MOV(ax, cs));	// 32591 mov     ax, cs ;~ 0D4F:0596
cs=0xd4f;eip=0x000598; 	T(MOV(ds, ax));	// 32592 mov     ds, ax ;~ 0D4F:0598
cs=0xd4f;eip=0x00059a; 	T(MOV(dx, 0x44B));	// 32594 mov     dx, 44Bh ;~ 0D4F:059A
cs=0xd4f;eip=0x00059d; 	T(MOV(ax, 0));	// 32595 mov     ax, 0 ;~ 0D4F:059D
cs=0xd4f;eip=0x0005a0; 	T(MOV(es, ax));	// 32596 mov     es, ax ;~ 0D4F:05A0
cs=0xd4f;eip=0x0005a2; 	X(MOV(*(dw*)(raddr(es,0x20)), dx));	// 32598 mov     es:20h, dx ;~ 0D4F:05A2
cs=0xd4f;eip=0x0005a7; 	X(MOV(*(dw*)(raddr(es,0x22)), ds));	// 32599 mov     word ptr es:22h, ds ;~ 0D4F:05A7
loc_1c07c:
	// 5952 
cs=0xd4f;eip=0x0005ac; //  	T(OR(bh, 0));	// 32602 or      bh, 0 ;~ 0D4F:05AC
seg002_5af_proc:
	// 32605 
//cs=0xd4f;eip=0x0005af; 	X(PUSH(cs));	// 32605 push    cs ;~ 0D4F:05AF
//cs=0xd4f;eip=0x0005b0; 	J(CALL(_group2,m2c::kloc_1c07c));	// 32606 call    near ptr loc_1C07C+1 ;~ 0D4F:05B0
R(POPF);
cs=0xd4f;eip=0x0005b3; 	X(POP(di));	// 32607 pop     di ;~ 0D4F:05B3
cs=0xd4f;eip=0x0005b4; 	X(POP(si));	// 32608 pop     si ;~ 0D4F:05B4
cs=0xd4f;eip=0x0005b5; 	X(POP(ds));	// 32609 pop     ds ;~ 0D4F:05B5
cs=0xd4f;eip=0x0005b6; 	J(RETF(0));	// 32611 retf ;~ 0D4F:05B6
sub_1c087:
	// 32616 
cs=0xd4f;eip=0x0005b7; 	X(PUSH(ds));	// 32617 push    ds ;~ 0D4F:05B7
ret_d4f_5b8:
	// 5953 
cs=0xd4f;eip=0x0005b8; 	X(PUSH(si));	// 32618 push    si ;~ 0D4F:05B8
cs=0xd4f;eip=0x0005b9; 	X(PUSH(di));	// 32619 push    di ;~ 0D4F:05B9
cs=0xd4f;eip=0x0005ba; 	X(PUSHF);	// 32620 pushf ;~ 0D4F:05BA
cs=0xd4f;eip=0x0005bb; 	T(CLI);	// 32621 cli ;~ 0D4F:05BB
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0005bc; 	X(MOV(*(dw*)(((db*)&word_1bbec)), 0x0FFFF));	// 32622 mov     cs:word_1BBEC, 0FFFFh ;~ 0D4F:05BC
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0005c3; 	T(MOV(dx, *(dw*)(((db*)&dword_1bbe8))));	// 32623 mov     dx, word ptr cs:dword_1BBE8 ;~ 0D4F:05C3
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0005c8; 	T(MOV(ds, *(dw*)(((db*)&dword_1bbe8)+2)));	// 32624 mov     ds, word ptr cs:dword_1BBE8+2 ;~ 0D4F:05C8
cs=0xd4f;eip=0x0005cd; 	T(MOV(ax, 0));	// 32625 mov     ax, 0 ;~ 0D4F:05CD
cs=0xd4f;eip=0x0005d0; 	T(MOV(es, ax));	// 32626 mov     es, ax ;~ 0D4F:05D0
cs=0xd4f;eip=0x0005d2; 	X(MOV(*(dw*)(raddr(es,0x20)), dx));	// 32627 mov     es:20h, dx ;~ 0D4F:05D2
cs=0xd4f;eip=0x0005d7; 	X(MOV(*(dw*)(raddr(es,0x22)), ds));	// 32628 mov     word ptr es:22h, ds ;~ 0D4F:05D7
loc_1c0ac:
	// 5954 
cs=0xd4f;eip=0x0005dc; //  	T(OR(bh, 0));	// 32631 or      bh, 0 ;~ 0D4F:05DC
seg002_5df_proc:
	// 32634 
//cs=0xd4f;eip=0x0005df; 	X(PUSH(cs));	// 32634 push    cs ;~ 0D4F:05DF
//cs=0xd4f;eip=0x0005e0; 	J(CALL(_group2,m2c::kloc_1c0ac));	// 32635 call    near ptr loc_1C0AC+1 ;~ 0D4F:05E0
R(POPF);
cs=0xd4f;eip=0x0005e3; 	X(POP(di));	// 32636 pop     di ;~ 0D4F:05E3
cs=0xd4f;eip=0x0005e4; 	X(POP(si));	// 32637 pop     si ;~ 0D4F:05E4
cs=0xd4f;eip=0x0005e5; 	X(POP(ds));	// 32638 pop     ds ;~ 0D4F:05E5
cs=0xd4f;eip=0x0005e6; 	J(RETF(0));	// 32639 retf ;~ 0D4F:05E6
sub_1c0b7:
	// 32645 
#undef arg_2
#define arg_2 6
	// 32648 arg_2           = word ptr  6 ;~ 0D4F:05E7
ret_d4f_5e7:
	// 5955 
cs=0xd4f;eip=0x0005e7; 	X(PUSH(bp));	// 32650 push    bp ;~ 0D4F:05E7
cs=0xd4f;eip=0x0005e8; 	T(MOV(bp, sp));	// 32651 mov     bp, sp ;~ 0D4F:05E8
cs=0xd4f;eip=0x0005ea; 	X(PUSH(ds));	// 32652 push    ds ;~ 0D4F:05EA
cs=0xd4f;eip=0x0005eb; 	X(PUSH(si));	// 32653 push    si ;~ 0D4F:05EB
cs=0xd4f;eip=0x0005ec; 	X(PUSH(di));	// 32654 push    di ;~ 0D4F:05EC
cs=0xd4f;eip=0x0005ed; 	X(PUSHF);	// 32655 pushf ;~ 0D4F:05ED
cs=0xd4f;eip=0x0005ee; 	T(CLI);	// 32656 cli ;~ 0D4F:05EE
cs=0xd4f;eip=0x0005ef; 	T(MOV(al, 0x36));	// 32657 mov     al, 36h ; '6' ;~ 0D4F:05EF
cs=0xd4f;eip=0x0005f1; 	R(OUT(0x43, al));	// 32658 out     43h, al         ; Timer 8253-5 (AT: 8254.2). ;~ 0D4F:05F1
cs=0xd4f;eip=0x0005f3; 	T(MOV(ax, *(dw*)(raddr(ss,bp+arg_2))));	// 32659 mov     ax, [bp+arg_2] ;~ 0D4F:05F3
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0005f6; 	X(MOV(*(dw*)(((db*)&word_1bbf2)), ax));	// 32660 mov     cs:word_1BBF2, ax ;~ 0D4F:05F6
cs=0xd4f;eip=0x0005fa; 	J({;});	// 32661 jmp     short $+2 ;~ 0D4F:05FA
loc_1c0cc:
	// 5956 
cs=0xd4f;eip=0x0005fc; 	R(OUT(0x40, al));	// 32665 out     40h, al         ; Timer 8253-5 (AT: 8254.2). ;~ 0D4F:05FC
cs=0xd4f;eip=0x0005fe; 	T(MOV(al, ah));	// 32666 mov     al, ah ;~ 0D4F:05FE
cs=0xd4f;eip=0x000600; 	J({;});	// 32667 jmp     short $+2 ;~ 0D4F:0600
loc_1c0d2:
	// 5957 
cs=0xd4f;eip=0x000602; 	R(OUT(0x40, al));	// 32671 out     40h, al         ; Timer 8253-5 (AT: 8254.2). ;~ 0D4F:0602
loc_1c0d4:
	// 5958 
cs=0xd4f;eip=0x000604; //  	T(OR(bh, 0));	// 32674 or      bh, 0 ;~ 0D4F:0604
seg002_607_proc:
	// 32677 
//cs=0xd4f;eip=0x000607; 	X(PUSH(cs));	// 32677 push    cs ;~ 0D4F:0607
//cs=0xd4f;eip=0x000608; 	J(CALL(_group2,m2c::kloc_1c0d4));	// 32678 call    near ptr loc_1C0D4+1 ;~ 0D4F:0608
R(POPF);
cs=0xd4f;eip=0x00060b; 	X(POP(di));	// 32679 pop     di ;~ 0D4F:060B
cs=0xd4f;eip=0x00060c; 	X(POP(si));	// 32680 pop     si ;~ 0D4F:060C
cs=0xd4f;eip=0x00060d; 	X(POP(ds));	// 32681 pop     ds ;~ 0D4F:060D
cs=0xd4f;eip=0x00060e; 	X(POP(bp));	// 32682 pop     bp ;~ 0D4F:060E
cs=0xd4f;eip=0x00060f; 	J(RETF(0));	// 32683 retf ;~ 0D4F:060F
sub_1c0e0:
	// 32689 
#undef arg_0
#define arg_0 6
	// 32691 arg_0           = word ptr  6 ;~ 0D4F:0610
ret_d4f_610:
	// 5959 
cs=0xd4f;eip=0x000610; 	X(PUSH(bp));	// 32693 push    bp ;~ 0D4F:0610
cs=0xd4f;eip=0x000611; 	T(MOV(bp, sp));	// 32694 mov     bp, sp ;~ 0D4F:0611
cs=0xd4f;eip=0x000613; 	X(PUSH(ds));	// 32695 push    ds ;~ 0D4F:0613
cs=0xd4f;eip=0x000614; 	X(PUSH(si));	// 32696 push    si ;~ 0D4F:0614
cs=0xd4f;eip=0x000615; 	X(PUSH(di));	// 32697 push    di ;~ 0D4F:0615
cs=0xd4f;eip=0x000616; 	T(MOV(ax, 0));	// 32698 mov     ax, 0 ;~ 0D4F:0616
cs=0xd4f;eip=0x000619; 	T(CMP(*(dw*)(raddr(ss,bp+arg_0)), 0x0D68D));	// 32699 cmp     [bp+arg_0], 0D68Dh ;~ 0D4F:0619
cs=0xd4f;eip=0x00061e; 	J(JNC(loc_1c0fd));	// 32700 jnb     short loc_1C0FD ;~ 0D4F:061E
cs=0xd4f;eip=0x000620; 	T(MOV(ax, *(dw*)(raddr(ss,bp+arg_0))));	// 32701 mov     ax, [bp+arg_0] ;~ 0D4F:0620
cs=0xd4f;eip=0x000623; 	T(MOV(bx, 0x20BC));	// 32702 mov     bx, 20BCh ;~ 0D4F:0623
cs=0xd4f;eip=0x000626; 	T(MOV(cx, 0x2710));	// 32703 mov     cx, 2710h ;~ 0D4F:0626
cs=0xd4f;eip=0x000629; 	T(MUL1_2(cx));	// 32704 mul     cx ;~ 0D4F:0629
cs=0xd4f;eip=0x00062b; 	T(DIV2(bx));	// 32705 div     bx ;~ 0D4F:062B
loc_1c0fd:
	// 5960 
cs=0xd4f;eip=0x00062d; 	X(PUSH(ax));	// 32708 push    ax ;~ 0D4F:062D
cs=0xd4f;eip=0x00062e; 	X(PUSH(cs));	// 32709 push    cs ;~ 0D4F:062E
cs=0xd4f;eip=0x00062f; 	J(CALL(sub_1c0b7,0));	// 32710 call    sub_1C0B7 ;~ 0D4F:062F
cs=0xd4f;eip=0x000632; 	T(ADD(sp, 2));	// 32711 add     sp, 2 ;~ 0D4F:0632
cs=0xd4f;eip=0x000635; 	X(POP(di));	// 32712 pop     di ;~ 0D4F:0635
cs=0xd4f;eip=0x000636; 	X(POP(si));	// 32713 pop     si ;~ 0D4F:0636
cs=0xd4f;eip=0x000637; 	X(POP(ds));	// 32714 pop     ds ;~ 0D4F:0637
cs=0xd4f;eip=0x000638; 	X(POP(bp));	// 32715 pop     bp ;~ 0D4F:0638
cs=0xd4f;eip=0x000639; 	J(RETF(0));	// 32716 retf ;~ 0D4F:0639
sub_1c10a:
	// 32724 
#undef arg_0
#define arg_0 6
	// 32726 arg_0           = word ptr  6 ;~ 0D4F:063A
#undef arg_2
#define arg_2 8
	// 32727 arg_2           = word ptr  8 ;~ 0D4F:063A
#undef arg_4
#define arg_4 0x0A
	// 32728 arg_4           = word ptr  0Ah ;~ 0D4F:063A
#undef arg_6
#define arg_6 0x0C
	// 32729 arg_6           = word ptr  0Ch ;~ 0D4F:063A
ret_d4f_63a:
	// 5961 
cs=0xd4f;eip=0x00063a; 	X(PUSH(bp));	// 32731 push    bp ;~ 0D4F:063A
cs=0xd4f;eip=0x00063b; 	T(MOV(bp, sp));	// 32732 mov     bp, sp ;~ 0D4F:063B
cs=0xd4f;eip=0x00063d; 	X(PUSH(ds));	// 32733 push    ds ;~ 0D4F:063D
cs=0xd4f;eip=0x00063e; 	X(PUSH(si));	// 32734 push    si ;~ 0D4F:063E
cs=0xd4f;eip=0x00063f; 	X(PUSH(di));	// 32735 push    di ;~ 0D4F:063F
cs=0xd4f;eip=0x000640; 	T(MOV(ax, *(dw*)(raddr(ss,bp+arg_0))));	// 32736 mov     ax, [bp+arg_0] ;~ 0D4F:0640
cs=0xd4f;eip=0x000643; 	T(MOV(dx, *(dw*)(raddr(ss,bp+arg_2))));	// 32737 mov     dx, [bp+arg_2] ;~ 0D4F:0643
cs=0xd4f;eip=0x000646; 	T(MOV(bx, *(dw*)(raddr(ss,bp+arg_4))));	// 32738 mov     bx, [bp+arg_4] ;~ 0D4F:0646
cs=0xd4f;eip=0x000649; 	T(MOV(cx, *(dw*)(raddr(ss,bp+arg_6))));	// 32739 mov     cx, [bp+arg_6] ;~ 0D4F:0649
cs=0xd4f;eip=0x00064c; 	T(OR(cx, cx));	// 32740 or      cx, cx ;~ 0D4F:064C
cs=0xd4f;eip=0x00064e; 	J(JNZ(loc_1c128));	// 32741 jnz     short loc_1C128 ;~ 0D4F:064E
cs=0xd4f;eip=0x000650; 	T(OR(dx, dx));	// 32742 or      dx, dx ;~ 0D4F:0650
cs=0xd4f;eip=0x000652; 	J(JZ(loc_1c14c));	// 32743 jz      short loc_1C14C ;~ 0D4F:0652
cs=0xd4f;eip=0x000654; 	T(OR(bx, bx));	// 32744 or      bx, bx ;~ 0D4F:0654
cs=0xd4f;eip=0x000656; 	J(JZ(loc_1c14c));	// 32745 jz      short loc_1C14C ;~ 0D4F:0656
loc_1c128:
	// 5962 
cs=0xd4f;eip=0x000658; 	T(MOV(bp, cx));	// 32748 mov     bp, cx ;~ 0D4F:0658
cs=0xd4f;eip=0x00065a; 	T(MOV(cx, 0x20));	// 32749 mov     cx, 20h ; ' ' ;~ 0D4F:065A
cs=0xd4f;eip=0x00065d; 	T(XOR(di, di));	// 32750 xor     di, di ;~ 0D4F:065D
cs=0xd4f;eip=0x00065f; 	T(XOR(si, si));	// 32751 xor     si, si ;~ 0D4F:065F
loc_1c131:
	// 5963 
cs=0xd4f;eip=0x000661; 	T(SHL(ax, 1));	// 32754 shl     ax, 1 ;~ 0D4F:0661
cs=0xd4f;eip=0x000663; 	T(RCL(dx, 1));	// 32755 rcl     dx, 1 ;~ 0D4F:0663
cs=0xd4f;eip=0x000665; 	T(RCL(si, 1));	// 32756 rcl     si, 1 ;~ 0D4F:0665
cs=0xd4f;eip=0x000667; 	T(RCL(di, 1));	// 32757 rcl     di, 1 ;~ 0D4F:0667
cs=0xd4f;eip=0x000669; 	T(CMP(di, bp));	// 32758 cmp     di, bp ;~ 0D4F:0669
cs=0xd4f;eip=0x00066b; 	J(JC(loc_1c148));	// 32759 jb      short loc_1C148 ;~ 0D4F:066B
cs=0xd4f;eip=0x00066d; 	J(JA(loc_1c143));	// 32760 ja      short loc_1C143 ;~ 0D4F:066D
cs=0xd4f;eip=0x00066f; 	T(CMP(si, bx));	// 32761 cmp     si, bx ;~ 0D4F:066F
cs=0xd4f;eip=0x000671; 	J(JC(loc_1c148));	// 32762 jb      short loc_1C148 ;~ 0D4F:0671
loc_1c143:
	// 5964 
cs=0xd4f;eip=0x000673; 	T(SUB(si, bx));	// 32765 sub     si, bx ;~ 0D4F:0673
cs=0xd4f;eip=0x000675; 	T(SBB(di, bp));	// 32766 sbb     di, bp ;~ 0D4F:0675
cs=0xd4f;eip=0x000677; 	T(INC(ax));	// 32767 inc     ax ;~ 0D4F:0677
loc_1c148:
	// 5965 
cs=0xd4f;eip=0x000678; 	J(LOOP(loc_1c131));	// 32771 loop    loc_1C131 ;~ 0D4F:0678
cs=0xd4f;eip=0x00067a; 	J(JMP(loc_1c150));	// 32772 jmp     short loc_1C150 ;~ 0D4F:067A
loc_1c14c:
	// 5966 
cs=0xd4f;eip=0x00067c; 	T(DIV2(bx));	// 32777 div     bx ;~ 0D4F:067C
cs=0xd4f;eip=0x00067e; 	T(XOR(dx, dx));	// 32778 xor     dx, dx ;~ 0D4F:067E
loc_1c150:
	// 5967 
cs=0xd4f;eip=0x000680; 	X(POP(di));	// 32781 pop     di ;~ 0D4F:0680
cs=0xd4f;eip=0x000681; 	X(POP(si));	// 32782 pop     si ;~ 0D4F:0681
cs=0xd4f;eip=0x000682; 	X(POP(ds));	// 32783 pop     ds ;~ 0D4F:0682
cs=0xd4f;eip=0x000683; 	X(POP(bp));	// 32784 pop     bp ;~ 0D4F:0683
cs=0xd4f;eip=0x000684; 	J(RETF(0));	// 32785 retf ;~ 0D4F:0684
sub_1c155:
	// 32792 
cs=0xd4f;eip=0x000685; 	X(PUSH(ds));	// 32793 push    ds ;~ 0D4F:0685
ret_d4f_686:
	// 5968 
cs=0xd4f;eip=0x000686; 	X(PUSH(si));	// 32794 push    si ;~ 0D4F:0686
cs=0xd4f;eip=0x000687; 	X(PUSH(di));	// 32795 push    di ;~ 0D4F:0687
cs=0xd4f;eip=0x000688; 	X(PUSHF);	// 32796 pushf ;~ 0D4F:0688
cs=0xd4f;eip=0x000689; 	T(CLI);	// 32797 cli ;~ 0D4F:0689
cs=0xd4f;eip=0x00068a; 	T(CLD);	// 32798 cld ;~ 0D4F:068A
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00068b; 	X(MOV(*(dw*)(((db*)&word_1bbee)), 0x0FFFF));	// 32799 mov     cs:word_1BBEE, 0FFFFh ;~ 0D4F:068B
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000692; 	X(MOV(*(dw*)(((db*)&word_1bbf0)), 0x0FFFF));	// 32800 mov     cs:word_1BBF0, 0FFFFh ;~ 0D4F:0692
cs=0xd4f;eip=0x000699; 	T(MOV(si, 0));	// 32801 mov     si, 0 ;~ 0D4F:0699
loc_1c16c:
	// 5969 
cs=0xd4f;eip=0x00069c; 	T(MOV(bx, si));	// 32804 mov     bx, si ;~ 0D4F:069C
cs=0xd4f;eip=0x00069e; 	T(SHL(bx, 1));	// 32805 shl     bx, 1 ;~ 0D4F:069E
cs=0xd4f;eip=0x0006a0; 	T(CMP(*(dw*)(raddr(cs,bx+0x6A)), 0));	// 32806 cmp     word ptr cs:[bx+6Ah], 0 ;~ 0D4F:06A0
cs=0xd4f;eip=0x0006a6; 	J(JZ(loc_1c19d));	// 32807 jz      short loc_1C19D ;~ 0D4F:06A6
cs=0xd4f;eip=0x0006a8; 	T(SHL(bx, 1));	// 32808 shl     bx, 1 ;~ 0D4F:06A8
cs=0xd4f;eip=0x0006aa; 	T(MOV(ax, *(dw*)(raddr(cs,bx+0x0D0))));	// 32809 mov     ax, cs:[bx+0D0h] ;~ 0D4F:06AA
cs=0xd4f;eip=0x0006af; 	T(MOV(dx, *(dw*)(raddr(cs,bx+0x0D2))));	// 32810 mov     dx, cs:[bx+0D2h] ;~ 0D4F:06AF
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006b4; 	T(CMP(dx, *(dw*)(((db*)&word_1bbf0))));	// 32811 cmp     dx, cs:word_1BBF0 ;~ 0D4F:06B4
cs=0xd4f;eip=0x0006b9; 	J(JC(loc_1c194));	// 32812 jb      short loc_1C194 ;~ 0D4F:06B9
cs=0xd4f;eip=0x0006bb; 	J(JA(loc_1c19d));	// 32813 ja      short loc_1C19D ;~ 0D4F:06BB
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006bd; 	T(CMP(ax, *(dw*)(((db*)&word_1bbee))));	// 32814 cmp     ax, cs:word_1BBEE ;~ 0D4F:06BD
cs=0xd4f;eip=0x0006c2; 	J(JNC(loc_1c19d));	// 32815 jnb     short loc_1C19D ;~ 0D4F:06C2
loc_1c194:
	// 5970 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006c4; 	X(MOV(*(dw*)(((db*)&word_1bbee)), ax));	// 32818 mov     cs:word_1BBEE, ax ;~ 0D4F:06C4
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006c8; 	X(MOV(*(dw*)(((db*)&word_1bbf0)), dx));	// 32819 mov     cs:word_1BBF0, dx ;~ 0D4F:06C8
loc_1c19d:
	// 5971 
cs=0xd4f;eip=0x0006cd; 	T(INC(si));	// 32823 inc     si ;~ 0D4F:06CD
cs=0xd4f;eip=0x0006ce; 	T(CMP(si, 0x10));	// 32824 cmp     si, 10h ;~ 0D4F:06CE
cs=0xd4f;eip=0x0006d1; 	J(JBE(loc_1c16c));	// 32825 jbe     short loc_1C16C ;~ 0D4F:06D1
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006d3; 	T(MOV(ax, *(dw*)(((db*)&word_1bbee))));	// 32826 mov     ax, cs:word_1BBEE ;~ 0D4F:06D3
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006d7; 	T(MOV(dx, *(dw*)(((db*)&word_1bbf0))));	// 32827 mov     dx, cs:word_1BBF0 ;~ 0D4F:06D7
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006dc; 	T(CMP(ax, *(dw*)(((db*)&word_1bbe4))));	// 32828 cmp     ax, cs:word_1BBE4 ;~ 0D4F:06DC
cs=0xd4f;eip=0x0006e1; 	J(JNZ(loc_1c1ba));	// 32829 jnz     short loc_1C1BA ;~ 0D4F:06E1
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006e3; 	T(CMP(dx, *(dw*)(((db*)&word_1bbe6))));	// 32830 cmp     dx, cs:word_1BBE6 ;~ 0D4F:06E3
cs=0xd4f;eip=0x0006e8; 	J(JZ(loc_1c1df));	// 32831 jz      short loc_1C1DF ;~ 0D4F:06E8
loc_1c1ba:
	// 5972 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006ea; 	X(MOV(*(dw*)(((db*)&word_1bbec)), 0x0FFFF));	// 32834 mov     cs:word_1BBEC, 0FFFFh ;~ 0D4F:06EA
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006f1; 	X(MOV(*(dw*)(((db*)&word_1bbe4)), ax));	// 32835 mov     cs:word_1BBE4, ax ;~ 0D4F:06F1
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0006f5; 	X(MOV(*(dw*)(((db*)&word_1bbe6)), dx));	// 32836 mov     cs:word_1BBE6, dx ;~ 0D4F:06F5
cs=0xd4f;eip=0x0006fa; 	X(PUSH(ax));	// 32837 push    ax ;~ 0D4F:06FA
cs=0xd4f;eip=0x0006fb; 	X(PUSH(cs));	// 32838 push    cs ;~ 0D4F:06FB
cs=0xd4f;eip=0x0006fc; 	J(CALL(sub_1c0e0,0));	// 32839 call    near ptr sub_1C0E0 ;~ 0D4F:06FC
cs=0xd4f;eip=0x0006ff; 	T(ADD(sp, 2));	// 32840 add     sp, 2 ;~ 0D4F:06FF
cs=0xd4f;eip=0x000702; 	X(PUSH(cs));	// 32841 push    cs ;~ 0D4F:0702
cs=0xd4f;eip=0x000703; 	X(POP(es));	// 32842 pop     es ;~ 0D4F:0703
cs=0xd4f;eip=0x000704; 	T(MOV(di, 0x8C));	// 32844 mov     di, 8Ch ; 'Œ' ;~ 0D4F:0704
cs=0xd4f;eip=0x000707; 	T(MOV(cx, 0x22));	// 32845 mov     cx, 22h ; '"' ;~ 0D4F:0707
cs=0xd4f;eip=0x00070a; 	T(MOV(ax, 0));	// 32846 mov     ax, 0 ;~ 0D4F:070A
	// 32847 rep stosw ;~ 0D4F:070D
cs=0xd4f;eip=0x00070d; 	X(	REP STOSW);	// 32847 rep stosw ;~ 0D4F:070D
loc_1c1df:
	// 5973 
cs=0xd4f;eip=0x00070f; //  	T(OR(bh, 0));	// 32851 or      bh, 0 ;~ 0D4F:070F
seg002_712_proc:
	// 32854 
//cs=0xd4f;eip=0x000712; 	X(PUSH(cs));	// 32854 push    cs ;~ 0D4F:0712
//cs=0xd4f;eip=0x000713; 	J(CALL(_group2,m2c::kloc_1c1df));	// 32855 call    near ptr loc_1C1DF+1 ;~ 0D4F:0713
R(POPF);
cs=0xd4f;eip=0x000716; 	X(POP(di));	// 32856 pop     di ;~ 0D4F:0716
cs=0xd4f;eip=0x000717; 	X(POP(si));	// 32857 pop     si ;~ 0D4F:0717
cs=0xd4f;eip=0x000718; 	X(POP(ds));	// 32858 pop     ds ;~ 0D4F:0718
cs=0xd4f;eip=0x000719; 	J(RETF(0));	// 32859 retf ;~ 0D4F:0719
sub_1c1ea:
	// 32864 
cs=0xd4f;eip=0x00071a; 	X(PUSH(ds));	// 32865 push    ds ;~ 0D4F:071A
ret_d4f_71b:
	// 5974 
cs=0xd4f;eip=0x00071b; 	X(PUSH(si));	// 32866 push    si ;~ 0D4F:071B
cs=0xd4f;eip=0x00071c; 	X(PUSH(di));	// 32867 push    di ;~ 0D4F:071C
cs=0xd4f;eip=0x00071d; 	X(PUSHF);	// 32868 pushf ;~ 0D4F:071D
cs=0xd4f;eip=0x00071e; 	T(CLI);	// 32869 cli ;~ 0D4F:071E
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00071f; 	X(MOV(*(dw*)(((db*)&word_1bad0)), 0));	// 32870 mov     cs:word_1BAD0, 0 ;~ 0D4F:071F
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000726; 	X(MOV(*(dw*)(((db*)&word_1bad2)), 0));	// 32871 mov     cs:word_1BAD2, 0 ;~ 0D4F:0726
cs=0xd4f;eip=0x00072d; 	T(CLD);	// 32872 cld ;~ 0D4F:072D
cs=0xd4f;eip=0x00072e; 	T(MOV(ax, cs));	// 32873 mov     ax, cs ;~ 0D4F:072E
cs=0xd4f;eip=0x000730; 	T(MOV(es, ax));	// 32874 mov     es, ax ;~ 0D4F:0730
cs=0xd4f;eip=0x000732; 	T(MOV(di, 0x124));	// 32875 mov     di, 124h ;~ 0D4F:0732
cs=0xd4f;eip=0x000735; 	T(MOV(cx, 0x20));	// 32876 mov     cx, 20h ; ' ' ;~ 0D4F:0735
cs=0xd4f;eip=0x000738; 	T(MOV(ax, 0));	// 32877 mov     ax, 0 ;~ 0D4F:0738
	// 32878 rep stosw ;~ 0D4F:073B
cs=0xd4f;eip=0x00073b; 	X(	REP STOSW);	// 32878 rep stosw ;~ 0D4F:073B
cs=0xd4f;eip=0x00073d; 	T(MOV(di, 0x164));	// 32879 mov     di, 164h ;~ 0D4F:073D
cs=0xd4f;eip=0x000740; 	T(MOV(cx, 0x10));	// 32880 mov     cx, 10h ;~ 0D4F:0740
cs=0xd4f;eip=0x000743; 	T(MOV(ax, 0x0FFFF));	// 32881 mov     ax, 0FFFFh ;~ 0D4F:0743
	// 32882 rep stosw ;~ 0D4F:0746
cs=0xd4f;eip=0x000746; 	X(	REP STOSW);	// 32882 rep stosw ;~ 0D4F:0746
cs=0xd4f;eip=0x000748; 	T(MOV(di, 0x184));	// 32883 mov     di, 184h ;~ 0D4F:0748
cs=0xd4f;eip=0x00074b; 	T(MOV(cx, 0x10));	// 32884 mov     cx, 10h ;~ 0D4F:074B
cs=0xd4f;eip=0x00074e; 	T(MOV(ax, 0));	// 32885 mov     ax, 0 ;~ 0D4F:074E
	// 32886 rep stosw ;~ 0D4F:0751
cs=0xd4f;eip=0x000751; 	X(	REP STOSW);	// 32886 rep stosw ;~ 0D4F:0751
loc_1c223:
	// 5975 
cs=0xd4f;eip=0x000753; //  	T(OR(bh, 0));	// 32889 or      bh, 0 ;~ 0D4F:0753
seg002_756_proc:
	// 32892 
//cs=0xd4f;eip=0x000756; 	X(PUSH(cs));	// 32892 push    cs ;~ 0D4F:0756
//cs=0xd4f;eip=0x000757; 	J(CALL(_group2,m2c::kloc_1c223));	// 32893 call    near ptr loc_1C223+1 ;~ 0D4F:0757
R(POPF);
cs=0xd4f;eip=0x00075a; 	X(POP(di));	// 32894 pop     di ;~ 0D4F:075A
cs=0xd4f;eip=0x00075b; 	X(POP(si));	// 32895 pop     si ;~ 0D4F:075B
cs=0xd4f;eip=0x00075c; 	X(POP(ds));	// 32896 pop     ds ;~ 0D4F:075C
cs=0xd4f;eip=0x00075d; 	J(RETF(0));	// 32897 retf ;~ 0D4F:075D
sub_1c22e:
	// 32903 
#undef arg_2
#define arg_2 6
	// 32905 arg_2           = word ptr  6 ;~ 0D4F:075E
#undef arg_4
#define arg_4 8
	// 32906 arg_4           = word ptr  8 ;~ 0D4F:075E
ret_d4f_75e:
	// 5976 
cs=0xd4f;eip=0x00075e; 	X(PUSH(bp));	// 32908 push    bp ;~ 0D4F:075E
cs=0xd4f;eip=0x00075f; 	T(MOV(bp, sp));	// 32909 mov     bp, sp ;~ 0D4F:075F
cs=0xd4f;eip=0x000761; 	X(PUSH(ds));	// 32910 push    ds ;~ 0D4F:0761
cs=0xd4f;eip=0x000762; 	X(PUSH(si));	// 32911 push    si ;~ 0D4F:0762
cs=0xd4f;eip=0x000763; 	X(PUSH(di));	// 32912 push    di ;~ 0D4F:0763
cs=0xd4f;eip=0x000764; 	X(PUSHF);	// 32913 pushf ;~ 0D4F:0764
cs=0xd4f;eip=0x000765; 	T(CLI);	// 32914 cli ;~ 0D4F:0765
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000766; 	X(MOV(*(dw*)(((db*)&word_1bc78)), 0));	// 32915 mov     cs:word_1BC78, 0 ;~ 0D4F:0766
loc_1c23d:
	// 5977 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00076d; 	T(MOV(si, *(dw*)(((db*)&word_1bc78))));	// 32918 mov     si, cs:word_1BC78 ;~ 0D4F:076D
cs=0xd4f;eip=0x000772; 	T(SHL(si, 1));	// 32919 shl     si, 1 ;~ 0D4F:0772
cs=0xd4f;eip=0x000774; 	T(MOV(dx, *(dw*)(raddr(cs,si+0x164))));	// 32920 mov     dx, cs:[si+164h] ;~ 0D4F:0774
cs=0xd4f;eip=0x000779; 	T(SHL(si, 1));	// 32921 shl     si, 1 ;~ 0D4F:0779
cs=0xd4f;eip=0x00077b; 	T(MOV(ax, *(dw*)(raddr(cs,si+0x124))));	// 32922 mov     ax, cs:[si+124h] ;~ 0D4F:077B
cs=0xd4f;eip=0x000780; 	T(OR(ax, *(dw*)(raddr(cs,si+0x126))));	// 32923 or      ax, cs:[si+126h] ;~ 0D4F:0780
cs=0xd4f;eip=0x000785; 	J(JZ(loc_1c276));	// 32924 jz      short loc_1C276 ;~ 0D4F:0785
cs=0xd4f;eip=0x000787; 	T(CMP(dx, 0x0FFFF));	// 32925 cmp     dx, 0FFFFh ;~ 0D4F:0787
cs=0xd4f;eip=0x00078a; 	J(JZ(loc_1c264));	// 32926 jz      short loc_1C264 ;~ 0D4F:078A
cs=0xd4f;eip=0x00078c; 	X(PUSH(dx));	// 32927 push    dx ;~ 0D4F:078C
cs=0xd4f;eip=0x00078d; 	X(PUSH(cs));	// 32928 push    cs ;~ 0D4F:078D
cs=0xd4f;eip=0x00078e; 	J(CALL(sub_1c35e,0));	// 32929 call    sub_1C35E ;~ 0D4F:078E
cs=0xd4f;eip=0x000791; 	T(ADD(sp, 2));	// 32930 add     sp, 2 ;~ 0D4F:0791
loc_1c264:
	// 5978 
cs=0xd4f;eip=0x000794; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_4))));	// 32933 push    [bp+arg_4] ;~ 0D4F:0794
cs=0xd4f;eip=0x000797; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_2))));	// 32934 push    [bp+arg_2] ;~ 0D4F:0797
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x00079a; 	X(PUSH(*(dw*)(((db*)&word_1bc78))));	// 32935 push    cs:word_1BC78 ;~ 0D4F:079A
cs=0xd4f;eip=0x00079f; 	X(PUSH(cs));	// 32936 push    cs ;~ 0D4F:079F
cs=0xd4f;eip=0x0007a0; 	J(CALL(sub_1c6d0,0));	// 32937 call    near ptr sub_1C6D0 ;~ 0D4F:07A0
cs=0xd4f;eip=0x0007a3; 	T(ADD(sp, 6));	// 32938 add     sp, 6 ;~ 0D4F:07A3
loc_1c276:
	// 5979 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0007a6; 	X(INC(*(dw*)(((db*)&word_1bc78))));	// 32941 inc     cs:word_1BC78 ;~ 0D4F:07A6
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0007ab; 	T(CMP(*(dw*)(((db*)&word_1bc78)), 0x10));	// 32942 cmp     cs:word_1BC78, 10h ;~ 0D4F:07AB
cs=0xd4f;eip=0x0007b1; 	J(JNZ(loc_1c23d));	// 32943 jnz     short loc_1C23D ;~ 0D4F:07B1
cs=0xd4f;eip=0x0007b3; 	X(PUSH(cs));	// 32944 push    cs ;~ 0D4F:07B3
cs=0xd4f;eip=0x0007b4; 	J(CALL(sub_1c3a7,0));	// 32945 call    sub_1C3A7 ;~ 0D4F:07B4
loc_1c287:
	// 5980 
cs=0xd4f;eip=0x0007b7; //  	T(OR(bh, 0));	// 32948 or      bh, 0 ;~ 0D4F:07B7
seg002_7ba_proc:
	// 32951 
//cs=0xd4f;eip=0x0007ba; 	X(PUSH(cs));	// 32951 push    cs ;~ 0D4F:07BA
//cs=0xd4f;eip=0x0007bb; 	J(CALL(_group2,m2c::kloc_1c287));	// 32952 call    near ptr loc_1C287+1 ;~ 0D4F:07BB
R(POPF);
cs=0xd4f;eip=0x0007be; 	X(POP(di));	// 32953 pop     di ;~ 0D4F:07BE
cs=0xd4f;eip=0x0007bf; 	X(POP(si));	// 32954 pop     si ;~ 0D4F:07BF
cs=0xd4f;eip=0x0007c0; 	X(POP(ds));	// 32955 pop     ds ;~ 0D4F:07C0
cs=0xd4f;eip=0x0007c1; 	X(POP(bp));	// 32956 pop     bp ;~ 0D4F:07C1
cs=0xd4f;eip=0x0007c2; 	J(RETF(0));	// 32957 retf ;~ 0D4F:07C2
sub_1c293:
	// 32963 
#undef arg_2
#define arg_2 6
	// 32966 arg_2           = dword ptr  6 ;~ 0D4F:07C3
ret_d4f_7c3:
	// 5981 
cs=0xd4f;eip=0x0007c3; 	X(PUSH(bp));	// 32968 push    bp ;~ 0D4F:07C3
cs=0xd4f;eip=0x0007c4; 	T(MOV(bp, sp));	// 32969 mov     bp, sp ;~ 0D4F:07C4
cs=0xd4f;eip=0x0007c6; 	X(PUSH(ds));	// 32970 push    ds ;~ 0D4F:07C6
cs=0xd4f;eip=0x0007c7; 	X(PUSH(si));	// 32971 push    si ;~ 0D4F:07C7
cs=0xd4f;eip=0x0007c8; 	X(PUSH(di));	// 32972 push    di ;~ 0D4F:07C8
cs=0xd4f;eip=0x0007c9; 	X(PUSHF);	// 32973 pushf ;~ 0D4F:07C9
cs=0xd4f;eip=0x0007ca; 	T(CLI);	// 32974 cli ;~ 0D4F:07CA
cs=0xd4f;eip=0x0007cb; 	T(MOV(cx, ds));	// 32975 mov     cx, ds ;~ 0D4F:07CB
cs=0xd4f;eip=0x0007cd; 	T(MOV(bx, 0));	// 32976 mov     bx, 0 ;~ 0D4F:07CD
loc_1c2a0:
	// 5982 
cs=0xd4f;eip=0x0007d0; 	T(CMP(*(dw*)(raddr(cs,bx+0x6A)), 0));	// 32979 cmp     word ptr cs:[bx+6Ah], 0 ;~ 0D4F:07D0
cs=0xd4f;eip=0x0007d6; 	J(JZ(loc_1c2b6));	// 32980 jz      short loc_1C2B6 ;~ 0D4F:07D6
cs=0xd4f;eip=0x0007d8; 	T(ADD(bx, 2));	// 32981 add     bx, 2 ;~ 0D4F:07D8
cs=0xd4f;eip=0x0007db; 	T(CMP(bx, 0x20));	// 32982 cmp     bx, 20h ; ' ' ;~ 0D4F:07DB
cs=0xd4f;eip=0x0007de; 	J(JC(loc_1c2a0));	// 32983 jb      short loc_1C2A0 ;~ 0D4F:07DE
cs=0xd4f;eip=0x0007e0; 	T(MOV(ax, 0x0FFFF));	// 32984 mov     ax, 0FFFFh ;~ 0D4F:07E0
cs=0xd4f;eip=0x0007e3; 	J(JMP(loc_1c352));	// 32985 jmp     loc_1C352 ;~ 0D4F:07E3
loc_1c2b6:
	// 5983 
cs=0xd4f;eip=0x0007e6; 	T(MOV(ax, bx));	// 32989 mov     ax, bx ;~ 0D4F:07E6
cs=0xd4f;eip=0x0007e8; 	T(SHR(ax, 1));	// 32990 shr     ax, 1 ;~ 0D4F:07E8
cs=0xd4f;eip=0x0007ea; 	X(MOV(*(dw*)(raddr(cs,bx+0x6A)), 1));	// 32991 mov     word ptr cs:[bx+6Ah], 1 ;~ 0D4F:07EA
cs=0xd4f;eip=0x0007f1; 	X(MOV(*(dw*)(raddr(cs,bx+0x48)), cx));	// 32992 mov     cs:[bx+48h], cx ;~ 0D4F:07F1
cs=0xd4f;eip=0x0007f6; 	T(SHL(bx, 1));	// 32993 shl     bx, 1 ;~ 0D4F:07F6
cs=0xd4f;eip=0x0007f8; 	T(LDS(si, *(dd*)(raddr(ss,bp+arg_2))));	// 32994 lds     si, [bp+arg_2] ;~ 0D4F:07F8
cs=0xd4f;eip=0x0007fb; 	X(MOV(*(dw*)(raddr(cs,bx+4)), si));	// 32995 mov     cs:[bx+4], si ;~ 0D4F:07FB
cs=0xd4f;eip=0x000800; 	X(MOV(*(dw*)(raddr(cs,bx+6)), ds));	// 32996 mov     word ptr cs:[bx+6], ds ;~ 0D4F:0800
cs=0xd4f;eip=0x000805; 	X(MOV(*(dw*)(raddr(cs,bx+0x0D0)), 0x0FFFF));	// 32997 mov     word ptr cs:[bx+0D0h], 0FFFFh ;~ 0D4F:0805
cs=0xd4f;eip=0x00080c; 	X(MOV(*(dw*)(raddr(cs,bx+0x0D2)), 0x0FFFF));	// 32998 mov     word ptr cs:[bx+0D2h], 0FFFFh ;~ 0D4F:080C
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000813; 	X(INC(*(dw*)(((db*)&word_1bad0))));	// 32999 inc     cs:word_1BAD0 ;~ 0D4F:0813
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000818; 	T(CMP(*(dw*)(((db*)&word_1bad0)), 1));	// 33000 cmp     cs:word_1BAD0, 1 ;~ 0D4F:0818
cs=0xd4f;eip=0x00081e; 	J(JNZ(loc_1c352));	// 33001 jnz     short loc_1C352 ;~ 0D4F:081E
cs=0xd4f;eip=0x000820; 	X(PUSH(ax));	// 33002 push    ax ;~ 0D4F:0820
cs=0xd4f;eip=0x000821; 	X(PUSH(cs));	// 33003 push    cs ;~ 0D4F:0821
cs=0xd4f;eip=0x000822; 	J(CALL(sub_1bff8,0));	// 33004 call    sub_1BFF8 ;~ 0D4F:0822
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000825; 	X(MOV(*(dw*)(((db*)&word_1bb5a)), 1));	// 33005 mov     cs:word_1BB5A, 1 ;~ 0D4F:0825
cs=0xd4f;eip=0x00082c; 	X(PUSH(cs));	// 33006 push    cs ;~ 0D4F:082C
cs=0xd4f;eip=0x00082d; 	J(CALL(sub_1c03b,0));	// 33007 call    sub_1C03B ;~ 0D4F:082D
cs=0xd4f;eip=0x000830; 	X(PUSH(ax));	// 33008 push    ax ;~ 0D4F:0830
cs=0xd4f;eip=0x000831; 	X(PUSH(bp));	// 33009 push    bp ;~ 0D4F:0831
cs=0xd4f;eip=0x000832; 	T(MOV(bp, sp));	// 33010 mov     bp, sp ;~ 0D4F:0832
cs=0xd4f;eip=0x000834; 	X(MOV(*(dw*)(raddr(ss,bp+2)), 0));	// 33011 mov     word ptr [bp+2], 0 ;~ 0D4F:0834
cs=0xd4f;eip=0x000839; 	X(POP(bp));	// 33012 pop     bp ;~ 0D4F:0839
cs=0xd4f;eip=0x00083a; 	X(PUSH(ax));	// 33013 push    ax ;~ 0D4F:083A
cs=0xd4f;eip=0x00083b; 	X(PUSH(bp));	// 33014 push    bp ;~ 0D4F:083B
cs=0xd4f;eip=0x00083c; 	T(MOV(bp, sp));	// 33015 mov     bp, sp ;~ 0D4F:083C
cs=0xd4f;eip=0x00083e; 	X(MOV(*(dw*)(raddr(ss,bp+2)), 0x0D68D));	// 33016 mov     word ptr [bp+2], 0D68Dh ;~ 0D4F:083E
cs=0xd4f;eip=0x000843; 	X(POP(bp));	// 33017 pop     bp ;~ 0D4F:0843
cs=0xd4f;eip=0x000844; 	X(PUSH(ax));	// 33018 push    ax ;~ 0D4F:0844
cs=0xd4f;eip=0x000845; 	X(PUSH(bp));	// 33019 push    bp ;~ 0D4F:0845
cs=0xd4f;eip=0x000846; 	T(MOV(bp, sp));	// 33020 mov     bp, sp ;~ 0D4F:0846
cs=0xd4f;eip=0x000848; 	X(MOV(*(dw*)(raddr(ss,bp+2)), 0x10));	// 33021 mov     word ptr [bp+2], 10h ;~ 0D4F:0848
cs=0xd4f;eip=0x00084d; 	X(POP(bp));	// 33022 pop     bp ;~ 0D4F:084D
cs=0xd4f;eip=0x00084e; 	X(PUSH(cs));	// 33023 push    cs ;~ 0D4F:084E
cs=0xd4f;eip=0x00084f; 	J(CALL(sub_1c451,0));	// 33024 call    sub_1C451 ;~ 0D4F:084F
cs=0xd4f;eip=0x000852; 	T(ADD(sp, 6));	// 33025 add     sp, 6 ;~ 0D4F:0852
cs=0xd4f;eip=0x000855; 	X(PUSH(ax));	// 33026 push    ax ;~ 0D4F:0855
cs=0xd4f;eip=0x000856; 	X(PUSH(bp));	// 33027 push    bp ;~ 0D4F:0856
cs=0xd4f;eip=0x000857; 	T(MOV(bp, sp));	// 33028 mov     bp, sp ;~ 0D4F:0857
cs=0xd4f;eip=0x000859; 	X(MOV(*(dw*)(raddr(ss,bp+2)), 0x10));	// 33029 mov     word ptr [bp+2], 10h ;~ 0D4F:0859
cs=0xd4f;eip=0x00085e; 	X(POP(bp));	// 33030 pop     bp ;~ 0D4F:085E
cs=0xd4f;eip=0x00085f; 	X(PUSH(cs));	// 33031 push    cs ;~ 0D4F:085F
cs=0xd4f;eip=0x000860; 	J(CALL(sub_1c3c5,0));	// 33032 call    sub_1C3C5 ;~ 0D4F:0860
cs=0xd4f;eip=0x000863; 	T(ADD(sp, 2));	// 33033 add     sp, 2 ;~ 0D4F:0863
cs=0xd4f;eip=0x000866; 	X(POP(ax));	// 33034 pop     ax ;~ 0D4F:0866
cs=0xd4f;eip=0x000867; 	T(MOV(bx, ax));	// 33035 mov     bx, ax ;~ 0D4F:0867
cs=0xd4f;eip=0x000869; 	T(SHL(bx, 1));	// 33036 shl     bx, 1 ;~ 0D4F:0869
cs=0xd4f;eip=0x00086b; 	X(MOV(*(dw*)(raddr(cs,bx+0x6A)), 1));	// 33037 mov     word ptr cs:[bx+6Ah], 1 ;~ 0D4F:086B
cs=0xd4f;eip=0x000872; 	T(SHL(bx, 1));	// 33038 shl     bx, 1 ;~ 0D4F:0872
cs=0xd4f;eip=0x000874; 	X(MOV(*(dw*)(raddr(cs,bx+0x0D0)), 0x0FFFF));	// 33039 mov     word ptr cs:[bx+0D0h], 0FFFFh ;~ 0D4F:0874
cs=0xd4f;eip=0x00087b; 	X(MOV(*(dw*)(raddr(cs,bx+0x0D2)), 0x0FFFF));	// 33040 mov     word ptr cs:[bx+0D2h], 0FFFFh ;~ 0D4F:087B
loc_1c352:
	// 5984 
cs=0xd4f;eip=0x000882; //  	T(OR(bh, 0));	// 33044 or      bh, 0 ;~ 0D4F:0882
seg002_885_proc:
	// 33047 
//cs=0xd4f;eip=0x000885; 	X(PUSH(cs));	// 33047 push    cs ;~ 0D4F:0885
//cs=0xd4f;eip=0x000886; 	J(CALL(_group2,m2c::kloc_1c352));	// 33048 call    near ptr loc_1C352+1 ;~ 0D4F:0886
R(POPF);
cs=0xd4f;eip=0x000889; 	X(POP(di));	// 33049 pop     di ;~ 0D4F:0889
cs=0xd4f;eip=0x00088a; 	X(POP(si));	// 33050 pop     si ;~ 0D4F:088A
cs=0xd4f;eip=0x00088b; 	X(POP(ds));	// 33051 pop     ds ;~ 0D4F:088B
cs=0xd4f;eip=0x00088c; 	X(POP(bp));	// 33052 pop     bp ;~ 0D4F:088C
cs=0xd4f;eip=0x00088d; 	J(RETF(0));	// 33053 retf ;~ 0D4F:088D
sub_1c35e:
	// 33059 
#undef arg_2
#define arg_2 6
	// 33062 arg_2           = word ptr  6 ;~ 0D4F:088E
ret_d4f_88e:
	// 5985 
cs=0xd4f;eip=0x00088e; 	X(PUSH(bp));	// 33064 push    bp ;~ 0D4F:088E
cs=0xd4f;eip=0x00088f; 	T(MOV(bp, sp));	// 33065 mov     bp, sp ;~ 0D4F:088F
cs=0xd4f;eip=0x000891; 	X(PUSH(ds));	// 33066 push    ds ;~ 0D4F:0891
cs=0xd4f;eip=0x000892; 	X(PUSH(si));	// 33067 push    si ;~ 0D4F:0892
cs=0xd4f;eip=0x000893; 	X(PUSH(di));	// 33068 push    di ;~ 0D4F:0893
cs=0xd4f;eip=0x000894; 	X(PUSHF);	// 33069 pushf ;~ 0D4F:0894
cs=0xd4f;eip=0x000895; 	T(CLI);	// 33070 cli ;~ 0D4F:0895
cs=0xd4f;eip=0x000896; 	T(MOV(bx, *(dw*)(raddr(ss,bp+arg_2))));	// 33071 mov     bx, [bp+arg_2] ;~ 0D4F:0896
cs=0xd4f;eip=0x000899; 	T(CMP(bx, 0x0FFFF));	// 33072 cmp     bx, 0FFFFh ;~ 0D4F:0899
cs=0xd4f;eip=0x00089c; 	J(JZ(loc_1c39b));	// 33073 jz      short loc_1C39B ;~ 0D4F:089C
cs=0xd4f;eip=0x00089e; 	T(SHL(bx, 1));	// 33074 shl     bx, 1 ;~ 0D4F:089E
cs=0xd4f;eip=0x0008a0; 	T(CMP(*(dw*)(raddr(cs,bx+0x6A)), 0));	// 33075 cmp     word ptr cs:[bx+6Ah], 0 ;~ 0D4F:08A0
cs=0xd4f;eip=0x0008a6; 	J(JZ(loc_1c39b));	// 33076 jz      short loc_1C39B ;~ 0D4F:08A6
cs=0xd4f;eip=0x0008a8; 	X(MOV(*(dw*)(raddr(cs,bx+0x6A)), 0));	// 33077 mov     word ptr cs:[bx+6Ah], 0 ;~ 0D4F:08A8
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x0008af; 	X(DEC(*(dw*)(((db*)&word_1bad0))));	// 33078 dec     cs:word_1BAD0 ;~ 0D4F:08AF
cs=0xd4f;eip=0x0008b4; 	J(JNZ(loc_1c39b));	// 33079 jnz     short loc_1C39B ;~ 0D4F:08B4
cs=0xd4f;eip=0x0008b6; 	X(PUSH(ax));	// 33080 push    ax ;~ 0D4F:08B6
cs=0xd4f;eip=0x0008b7; 	X(PUSH(bp));	// 33081 push    bp ;~ 0D4F:08B7
cs=0xd4f;eip=0x0008b8; 	T(MOV(bp, sp));	// 33082 mov     bp, sp ;~ 0D4F:08B8
cs=0xd4f;eip=0x0008ba; 	X(MOV(*(dw*)(raddr(ss,bp+2)), 0));	// 33083 mov     word ptr [bp+2], 0 ;~ 0D4F:08BA
cs=0xd4f;eip=0x0008bf; 	X(POP(bp));	// 33084 pop     bp ;~ 0D4F:08BF
cs=0xd4f;eip=0x0008c0; 	X(PUSH(cs));	// 33085 push    cs ;~ 0D4F:08C0
cs=0xd4f;eip=0x0008c1; 	J(CALL(sub_1c0b7,0));	// 33086 call    sub_1C0B7 ;~ 0D4F:08C1
cs=0xd4f;eip=0x0008c4; 	T(ADD(sp, 2));	// 33087 add     sp, 2 ;~ 0D4F:08C4
cs=0xd4f;eip=0x0008c7; 	X(PUSH(cs));	// 33088 push    cs ;~ 0D4F:08C7
cs=0xd4f;eip=0x0008c8; 	J(CALL(sub_1c087,0));	// 33089 call    sub_1C087 ;~ 0D4F:08C8
loc_1c39b:
	// 5986 
cs=0xd4f;eip=0x0008cb;// 	T(OR(bh, 0));	// 33093 or      bh, 0 ;~ 0D4F:08CB
seg002_8ce_proc:
	// 33096 
//cs=0xd4f;eip=0x0008ce; 	X(PUSH(cs));	// 33096 push    cs ;~ 0D4F:08CE
//cs=0xd4f;eip=0x0008cf; 	J(CALL(_group2,m2c::kloc_1c39b));	// 33097 call    near ptr loc_1C39B+1 ;~ 0D4F:08CF
R(POPF);
cs=0xd4f;eip=0x0008d2; 	X(POP(di));	// 33098 pop     di ;~ 0D4F:08D2
cs=0xd4f;eip=0x0008d3; 	X(POP(si));	// 33099 pop     si ;~ 0D4F:08D3
cs=0xd4f;eip=0x0008d4; 	X(POP(ds));	// 33100 pop     ds ;~ 0D4F:08D4
cs=0xd4f;eip=0x0008d5; 	X(POP(bp));	// 33101 pop     bp ;~ 0D4F:08D5
cs=0xd4f;eip=0x0008d6; 	J(RETF(0));	// 33102 retf ;~ 0D4F:08D6
sub_1c3a7:
	// 33107 
cs=0xd4f;eip=0x0008d7; 	X(PUSH(ds));	// 33108 push    ds ;~ 0D4F:08D7
ret_d4f_8d8:
	// 5987 
cs=0xd4f;eip=0x0008d8; 	X(PUSH(si));	// 33109 push    si ;~ 0D4F:08D8
cs=0xd4f;eip=0x0008d9; 	X(PUSH(di));	// 33110 push    di ;~ 0D4F:08D9
cs=0xd4f;eip=0x0008da; 	X(PUSHF);	// 33111 pushf ;~ 0D4F:08DA
cs=0xd4f;eip=0x0008db; 	T(CLI);	// 33112 cli ;~ 0D4F:08DB
cs=0xd4f;eip=0x0008dc; 	T(MOV(si, 0x0F));	// 33113 mov     si, 0Fh ;~ 0D4F:08DC
loc_1c3af:
	// 5988 
cs=0xd4f;eip=0x0008df; 	X(PUSH(si));	// 33116 push    si ;~ 0D4F:08DF
cs=0xd4f;eip=0x0008e0; 	X(PUSH(cs));	// 33117 push    cs ;~ 0D4F:08E0
cs=0xd4f;eip=0x0008e1; 	J(CALL(sub_1c35e,0));	// 33118 call    sub_1C35E ;~ 0D4F:08E1
cs=0xd4f;eip=0x0008e4; 	T(ADD(sp, 2));	// 33119 add     sp, 2 ;~ 0D4F:08E4
cs=0xd4f;eip=0x0008e7; 	T(DEC(si));	// 33120 dec     si ;~ 0D4F:08E7
cs=0xd4f;eip=0x0008e8; 	J(JGE(loc_1c3af));	// 33121 jge     short loc_1C3AF ;~ 0D4F:08E8
loc_1c3ba:
	// 5989 
cs=0xd4f;eip=0x0008ea; //  	T(OR(bh, 0));	// 33124 or      bh, 0 ;~ 0D4F:08EA
seg002_8ed_proc:
	// 33127 
//cs=0xd4f;eip=0x0008ed; 	X(PUSH(cs));	// 33127 push    cs ;~ 0D4F:08ED
//cs=0xd4f;eip=0x0008ee; 	J(CALL(_group2,m2c::kloc_1c3ba));	// 33128 call    near ptr loc_1C3BA+1 ;~ 0D4F:08EE
R(POPF);
cs=0xd4f;eip=0x0008f1; 	X(POP(di));	// 33129 pop     di ;~ 0D4F:08F1
cs=0xd4f;eip=0x0008f2; 	X(POP(si));	// 33130 pop     si ;~ 0D4F:08F2
cs=0xd4f;eip=0x0008f3; 	X(POP(ds));	// 33131 pop     ds ;~ 0D4F:08F3
cs=0xd4f;eip=0x0008f4; 	J(RETF(0));	// 33132 retf ;~ 0D4F:08F4
sub_1c3c5:
	// 33138 
#undef arg_2
#define arg_2 6
	// 33141 arg_2           = word ptr  6 ;~ 0D4F:08F5
ret_d4f_8f5:
	// 5990 
cs=0xd4f;eip=0x0008f5; 	X(PUSH(bp));	// 33143 push    bp ;~ 0D4F:08F5
cs=0xd4f;eip=0x0008f6; 	T(MOV(bp, sp));	// 33144 mov     bp, sp ;~ 0D4F:08F6
cs=0xd4f;eip=0x0008f8; 	X(PUSH(ds));	// 33145 push    ds ;~ 0D4F:08F8
cs=0xd4f;eip=0x0008f9; 	X(PUSH(si));	// 33146 push    si ;~ 0D4F:08F9
cs=0xd4f;eip=0x0008fa; 	X(PUSH(di));	// 33147 push    di ;~ 0D4F:08FA
cs=0xd4f;eip=0x0008fb; 	X(PUSHF);	// 33148 pushf ;~ 0D4F:08FB
cs=0xd4f;eip=0x0008fc; 	T(CLI);	// 33149 cli ;~ 0D4F:08FC
cs=0xd4f;eip=0x0008fd; 	T(MOV(bx, *(dw*)(raddr(ss,bp+arg_2))));	// 33150 mov     bx, [bp+arg_2] ;~ 0D4F:08FD
cs=0xd4f;eip=0x000900; 	T(SHL(bx, 1));	// 33151 shl     bx, 1 ;~ 0D4F:0900
cs=0xd4f;eip=0x000902; 	T(CMP(*(dw*)(raddr(cs,bx+0x6A)), 1));	// 33152 cmp     word ptr cs:[bx+6Ah], 1 ;~ 0D4F:0902
cs=0xd4f;eip=0x000908; 	J(JNZ(loc_1c3e1));	// 33153 jnz     short loc_1C3E1 ;~ 0D4F:0908
cs=0xd4f;eip=0x00090a; 	X(MOV(*(dw*)(raddr(cs,bx+0x6A)), 2));	// 33154 mov     word ptr cs:[bx+6Ah], 2 ;~ 0D4F:090A
loc_1c3e1:
	// 5991 
cs=0xd4f;eip=0x000911; //  	T(OR(bh, 0));	// 33158 or      bh, 0 ;~ 0D4F:0911
seg002_914_proc:
	// 33161 
//cs=0xd4f;eip=0x000914; 	X(PUSH(cs));	// 33161 push    cs ;~ 0D4F:0914
//cs=0xd4f;eip=0x000915; 	J(CALL(_group2,m2c::kloc_1c3e1));	// 33162 call    near ptr loc_1C3E1+1 ;~ 0D4F:0915
R(POPF);
cs=0xd4f;eip=0x000918; 	X(POP(di));	// 33163 pop     di ;~ 0D4F:0918
cs=0xd4f;eip=0x000919; 	X(POP(si));	// 33164 pop     si ;~ 0D4F:0919
cs=0xd4f;eip=0x00091a; 	X(POP(ds));	// 33165 pop     ds ;~ 0D4F:091A
cs=0xd4f;eip=0x00091b; 	X(POP(bp));	// 33166 pop     bp ;~ 0D4F:091B
cs=0xd4f;eip=0x00091c; 	J(RETF(0));	// 33167 retf ;~ 0D4F:091C
ret_d4f_91d:
	// 5992 
cs=0xd4f;eip=0x00091d; 	X(PUSH(ds));	// 33169 push    ds ;~ 0D4F:091D
cs=0xd4f;eip=0x00091e; 	X(PUSH(si));	// 33170 push    si ;~ 0D4F:091E
cs=0xd4f;eip=0x00091f; 	X(PUSH(di));	// 33171 push    di ;~ 0D4F:091F
cs=0xd4f;eip=0x000920; 	X(PUSHF);	// 33172 pushf ;~ 0D4F:0920
cs=0xd4f;eip=0x000921; 	T(CLI);	// 33173 cli ;~ 0D4F:0921
cs=0xd4f;eip=0x000922; 	T(MOV(si, 0x0F));	// 33174 mov     si, 0Fh ;~ 0D4F:0922
loc_1c3f5:
	// 5993 
cs=0xd4f;eip=0x000925; 	X(PUSH(si));	// 33177 push    si ;~ 0D4F:0925
cs=0xd4f;eip=0x000926; 	X(PUSH(cs));	// 33178 push    cs ;~ 0D4F:0926
cs=0xd4f;eip=0x000927; 	J(CALL(sub_1c3c5,0));	// 33179 call    sub_1C3C5 ;~ 0D4F:0927
cs=0xd4f;eip=0x00092a; 	T(ADD(sp, 2));	// 33180 add     sp, 2 ;~ 0D4F:092A
cs=0xd4f;eip=0x00092d; 	T(DEC(si));	// 33181 dec     si ;~ 0D4F:092D
cs=0xd4f;eip=0x00092e; 	J(JGE(loc_1c3f5));	// 33182 jge     short loc_1C3F5 ;~ 0D4F:092E
loc_1c400:
	// 5994 
cs=0xd4f;eip=0x000930; //  	T(OR(bh, 0));	// 33185 or      bh, 0 ;~ 0D4F:0930
//cs=0xd4f;eip=0x000933; 	X(PUSH(cs));	// 33186 push    cs ;~ 0D4F:0933
//cs=0xd4f;eip=0x000934; 	J(CALL(_group2,m2c::kloc_1c400));	// 33187 call    near ptr loc_1C400+1 ;~ 0D4F:0934
R(POPF);
cs=0xd4f;eip=0x000937; 	X(POP(di));	// 33188 pop     di ;~ 0D4F:0937
cs=0xd4f;eip=0x000938; 	X(POP(si));	// 33189 pop     si ;~ 0D4F:0938
cs=0xd4f;eip=0x000939; 	X(POP(ds));	// 33190 pop     ds ;~ 0D4F:0939
cs=0xd4f;eip=0x00093a; 	J(RETF(0));	// 33191 retf ;~ 0D4F:093A
sub_1c40b:
	// 33197 
#undef arg_0
#define arg_0 6
	// 33199 arg_0           = word ptr  6 ;~ 0D4F:093B
ret_d4f_93b:
	// 5995 
cs=0xd4f;eip=0x00093b; 	X(PUSH(bp));	// 33201 push    bp ;~ 0D4F:093B
cs=0xd4f;eip=0x00093c; 	T(MOV(bp, sp));	// 33202 mov     bp, sp ;~ 0D4F:093C
cs=0xd4f;eip=0x00093e; 	X(PUSH(ds));	// 33203 push    ds ;~ 0D4F:093E
cs=0xd4f;eip=0x00093f; 	X(PUSH(si));	// 33204 push    si ;~ 0D4F:093F
cs=0xd4f;eip=0x000940; 	X(PUSH(di));	// 33205 push    di ;~ 0D4F:0940
cs=0xd4f;eip=0x000941; 	X(PUSHF);	// 33206 pushf ;~ 0D4F:0941
cs=0xd4f;eip=0x000942; 	T(CLI);	// 33207 cli ;~ 0D4F:0942
cs=0xd4f;eip=0x000943; 	T(MOV(bx, *(dw*)(raddr(ss,bp+arg_0))));	// 33208 mov     bx, [bp+arg_0] ;~ 0D4F:0943
cs=0xd4f;eip=0x000946; 	T(SHL(bx, 1));	// 33209 shl     bx, 1 ;~ 0D4F:0946
cs=0xd4f;eip=0x000948; 	T(CMP(*(dw*)(raddr(cs,bx+0x6A)), 2));	// 33210 cmp     word ptr cs:[bx+6Ah], 2 ;~ 0D4F:0948
cs=0xd4f;eip=0x00094e; 	J(JNZ(loc_1c427));	// 33211 jnz     short loc_1C427 ;~ 0D4F:094E
cs=0xd4f;eip=0x000950; 	X(MOV(*(dw*)(raddr(cs,bx+0x6A)), 1));	// 33212 mov     word ptr cs:[bx+6Ah], 1 ;~ 0D4F:0950
loc_1c427:
	// 5996 
cs=0xd4f;eip=0x000957; //  	T(OR(bh, 0));	// 33216 or      bh, 0 ;~ 0D4F:0957
//cs=0xd4f;eip=0x00095a; 	X(PUSH(cs));	// 33217 push    cs ;~ 0D4F:095A
//cs=0xd4f;eip=0x00095b; 	J(CALL(_group2,m2c::kloc_1c427));	// 33218 call    near ptr loc_1C427+1 ;~ 0D4F:095B
R(POPF);
cs=0xd4f;eip=0x00095e; 	X(POP(di));	// 33219 pop     di ;~ 0D4F:095E
cs=0xd4f;eip=0x00095f; 	X(POP(si));	// 33220 pop     si ;~ 0D4F:095F
cs=0xd4f;eip=0x000960; 	X(POP(ds));	// 33221 pop     ds ;~ 0D4F:0960
cs=0xd4f;eip=0x000961; 	X(POP(bp));	// 33222 pop     bp ;~ 0D4F:0961
cs=0xd4f;eip=0x000962; 	J(RETF(0));	// 33223 retf ;~ 0D4F:0962
seg002_963_proc:
	// 33227 
cs=0xd4f;eip=0x000963; 	X(PUSH(ds));	// 33227 push    ds ;~ 0D4F:0963
ret_d4f_964:
	// 5997 
cs=0xd4f;eip=0x000964; 	X(PUSH(si));	// 33228 push    si ;~ 0D4F:0964
cs=0xd4f;eip=0x000965; 	X(PUSH(di));	// 33229 push    di ;~ 0D4F:0965
cs=0xd4f;eip=0x000966; 	X(PUSHF);	// 33230 pushf ;~ 0D4F:0966
cs=0xd4f;eip=0x000967; 	T(CLI);	// 33231 cli ;~ 0D4F:0967
cs=0xd4f;eip=0x000968; 	T(MOV(si, 0x0F));	// 33232 mov     si, 0Fh ;~ 0D4F:0968
loc_1c43b:
	// 5998 
cs=0xd4f;eip=0x00096b; 	X(PUSH(si));	// 33235 push    si ;~ 0D4F:096B
cs=0xd4f;eip=0x00096c; 	X(PUSH(cs));	// 33236 push    cs ;~ 0D4F:096C
cs=0xd4f;eip=0x00096d; 	J(CALL(sub_1c40b,0));	// 33237 call    near ptr sub_1C40B ;~ 0D4F:096D
cs=0xd4f;eip=0x000970; 	T(ADD(sp, 2));	// 33238 add     sp, 2 ;~ 0D4F:0970
cs=0xd4f;eip=0x000973; 	T(DEC(si));	// 33239 dec     si ;~ 0D4F:0973
cs=0xd4f;eip=0x000974; 	J(JGE(loc_1c43b));	// 33240 jge     short loc_1C43B ;~ 0D4F:0974
loc_1c446:
	// 5999 
cs=0xd4f;eip=0x000976; //  	T(OR(bh, 0));	// 33243 or      bh, 0 ;~ 0D4F:0976
//cs=0xd4f;eip=0x000979; 	X(PUSH(cs));	// 33244 push    cs ;~ 0D4F:0979
//cs=0xd4f;eip=0x00097a; 	J(CALL(_group2,m2c::kloc_1c446));	// 33245 call    near ptr loc_1C446+1 ;~ 0D4F:097A
R(POPF);
cs=0xd4f;eip=0x00097d; 	X(POP(di));	// 33246 pop     di ;~ 0D4F:097D
cs=0xd4f;eip=0x00097e; 	X(POP(si));	// 33247 pop     si ;~ 0D4F:097E
cs=0xd4f;eip=0x00097f; 	X(POP(ds));	// 33248 pop     ds ;~ 0D4F:097F
cs=0xd4f;eip=0x000980; 	J(RETF(0));	// 33249 retf ;~ 0D4F:0980
sub_1c451:
	// 33255 
#undef arg_2
#define arg_2 6
	// 33258 arg_2           = word ptr  6 ;~ 0D4F:0981
#undef arg_4
#define arg_4 8
	// 33259 arg_4           = word ptr  8 ;~ 0D4F:0981
#undef arg_6
#define arg_6 0x0A
	// 33260 arg_6           = word ptr  0Ah ;~ 0D4F:0981
ret_d4f_981:
	// 6000 
cs=0xd4f;eip=0x000981; 	X(PUSH(bp));	// 33262 push    bp ;~ 0D4F:0981
cs=0xd4f;eip=0x000982; 	T(MOV(bp, sp));	// 33263 mov     bp, sp ;~ 0D4F:0982
cs=0xd4f;eip=0x000984; 	X(PUSH(ds));	// 33264 push    ds ;~ 0D4F:0984
cs=0xd4f;eip=0x000985; 	X(PUSH(si));	// 33265 push    si ;~ 0D4F:0985
cs=0xd4f;eip=0x000986; 	X(PUSH(di));	// 33266 push    di ;~ 0D4F:0986
cs=0xd4f;eip=0x000987; 	X(PUSHF);	// 33267 pushf ;~ 0D4F:0987
cs=0xd4f;eip=0x000988; 	T(CLI);	// 33268 cli ;~ 0D4F:0988
cs=0xd4f;eip=0x000989; 	T(MOV(bx, *(dw*)(raddr(ss,bp+arg_2))));	// 33269 mov     bx, [bp+arg_2] ;~ 0D4F:0989
cs=0xd4f;eip=0x00098c; 	T(SHL(bx, 1));	// 33270 shl     bx, 1 ;~ 0D4F:098C
cs=0xd4f;eip=0x00098e; 	T(MOV(ax, *(dw*)(raddr(cs,bx+0x6A))));	// 33271 mov     ax, cs:[bx+6Ah] ;~ 0D4F:098E
cs=0xd4f;eip=0x000993; 	X(PUSH(ax));	// 33272 push    ax ;~ 0D4F:0993
cs=0xd4f;eip=0x000994; 	X(MOV(*(dw*)(raddr(cs,bx+0x6A)), 1));	// 33273 mov     word ptr cs:[bx+6Ah], 1 ;~ 0D4F:0994
cs=0xd4f;eip=0x00099b; 	T(SHL(bx, 1));	// 33274 shl     bx, 1 ;~ 0D4F:099B
cs=0xd4f;eip=0x00099d; 	T(MOV(ax, *(dw*)(raddr(ss,bp+arg_4))));	// 33275 mov     ax, [bp+arg_4] ;~ 0D4F:099D
cs=0xd4f;eip=0x0009a0; 	T(MOV(dx, *(dw*)(raddr(ss,bp+arg_6))));	// 33276 mov     dx, [bp+arg_6] ;~ 0D4F:09A0
cs=0xd4f;eip=0x0009a3; 	X(MOV(*(dw*)(raddr(cs,bx+0x0D0)), ax));	// 33277 mov     cs:[bx+0D0h], ax ;~ 0D4F:09A3
cs=0xd4f;eip=0x0009a8; 	X(MOV(*(dw*)(raddr(cs,bx+0x0D2)), dx));	// 33278 mov     cs:[bx+0D2h], dx ;~ 0D4F:09A8
cs=0xd4f;eip=0x0009ad; 	X(MOV(*(dw*)(raddr(cs,bx+0x8C)), 0));	// 33279 mov     word ptr cs:[bx+8Ch], 0 ;~ 0D4F:09AD
cs=0xd4f;eip=0x0009b4; 	X(MOV(*(dw*)(raddr(cs,bx+0x8E)), 0));	// 33280 mov     word ptr cs:[bx+8Eh], 0 ;~ 0D4F:09B4
cs=0xd4f;eip=0x0009bb; 	X(PUSH(cs));	// 33281 push    cs ;~ 0D4F:09BB
cs=0xd4f;eip=0x0009bc; 	J(CALL(sub_1c155,0));	// 33282 call    sub_1C155 ;~ 0D4F:09BC
cs=0xd4f;eip=0x0009bf; 	X(POP(ax));	// 33283 pop     ax ;~ 0D4F:09BF
cs=0xd4f;eip=0x0009c0; 	T(MOV(bx, *(dw*)(raddr(ss,bp+arg_2))));	// 33284 mov     bx, [bp+arg_2] ;~ 0D4F:09C0
cs=0xd4f;eip=0x0009c3; 	T(SHL(bx, 1));	// 33285 shl     bx, 1 ;~ 0D4F:09C3
cs=0xd4f;eip=0x0009c5; 	X(MOV(*(dw*)(raddr(cs,bx+0x6A)), ax));	// 33286 mov     cs:[bx+6Ah], ax ;~ 0D4F:09C5
loc_1c49a:
	// 6001 
cs=0xd4f;eip=0x0009ca; //  	T(OR(bh, 0));	// 33289 or      bh, 0 ;~ 0D4F:09CA
seg002_9cd_proc:
	// 33292 
//cs=0xd4f;eip=0x0009cd; 	X(PUSH(cs));	// 33292 push    cs ;~ 0D4F:09CD
//cs=0xd4f;eip=0x0009ce; 	J(CALL(_group2,m2c::kloc_1c49a));	// 33293 call    near ptr loc_1C49A+1 ;~ 0D4F:09CE
R(POPF);
cs=0xd4f;eip=0x0009d1; 	X(POP(di));	// 33294 pop     di ;~ 0D4F:09D1
cs=0xd4f;eip=0x0009d2; 	X(POP(si));	// 33295 pop     si ;~ 0D4F:09D2
cs=0xd4f;eip=0x0009d3; 	X(POP(ds));	// 33296 pop     ds ;~ 0D4F:09D3
cs=0xd4f;eip=0x0009d4; 	X(POP(bp));	// 33297 pop     bp ;~ 0D4F:09D4
cs=0xd4f;eip=0x0009d5; 	J(RETF(0));	// 33298 retf ;~ 0D4F:09D5
sub_1c4a6:
	// 33304 
#undef arg_2
#define arg_2 6
	// 33307 arg_2           = word ptr  6 ;~ 0D4F:09D6
#undef arg_4
#define arg_4 8
	// 33308 arg_4           = word ptr  8 ;~ 0D4F:09D6
#undef arg_6
#define arg_6 0x0A
	// 33309 arg_6           = word ptr  0Ah ;~ 0D4F:09D6
ret_d4f_9d6:
	// 6002 
cs=0xd4f;eip=0x0009d6; 	X(PUSH(bp));	// 33311 push    bp ;~ 0D4F:09D6
cs=0xd4f;eip=0x0009d7; 	T(MOV(bp, sp));	// 33312 mov     bp, sp ;~ 0D4F:09D7
cs=0xd4f;eip=0x0009d9; 	X(PUSH(ds));	// 33313 push    ds ;~ 0D4F:09D9
cs=0xd4f;eip=0x0009da; 	X(PUSH(si));	// 33314 push    si ;~ 0D4F:09DA
cs=0xd4f;eip=0x0009db; 	X(PUSH(di));	// 33315 push    di ;~ 0D4F:09DB
cs=0xd4f;eip=0x0009dc; 	X(PUSHF);	// 33316 pushf ;~ 0D4F:09DC
cs=0xd4f;eip=0x0009dd; 	T(CLI);	// 33317 cli ;~ 0D4F:09DD
cs=0xd4f;eip=0x0009de; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_6))));	// 33318 push    [bp+arg_6] ;~ 0D4F:09DE
cs=0xd4f;eip=0x0009e1; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_4))));	// 33319 push    [bp+arg_4] ;~ 0D4F:09E1
cs=0xd4f;eip=0x0009e4; 	X(PUSH(ax));	// 33320 push    ax ;~ 0D4F:09E4
cs=0xd4f;eip=0x0009e5; 	X(PUSH(bp));	// 33321 push    bp ;~ 0D4F:09E5
cs=0xd4f;eip=0x0009e6; 	T(MOV(bp, sp));	// 33322 mov     bp, sp ;~ 0D4F:09E6
cs=0xd4f;eip=0x0009e8; 	X(MOV(*(dw*)(raddr(ss,bp+2)), 0x0F));	// 33323 mov     word ptr [bp+2], 0Fh ;~ 0D4F:09E8
cs=0xd4f;eip=0x0009ed; 	X(POP(bp));	// 33324 pop     bp ;~ 0D4F:09ED
cs=0xd4f;eip=0x0009ee; 	X(PUSH(ax));	// 33325 push    ax ;~ 0D4F:09EE
cs=0xd4f;eip=0x0009ef; 	X(PUSH(bp));	// 33326 push    bp ;~ 0D4F:09EF
cs=0xd4f;eip=0x0009f0; 	T(MOV(bp, sp));	// 33327 mov     bp, sp ;~ 0D4F:09F0
cs=0xd4f;eip=0x0009f2; 	X(MOV(*(dw*)(raddr(ss,bp+2)), 0x4240));	// 33328 mov     word ptr [bp+2], 4240h ;~ 0D4F:09F2
cs=0xd4f;eip=0x0009f7; 	X(POP(bp));	// 33329 pop     bp ;~ 0D4F:09F7
cs=0xd4f;eip=0x0009f8; 	X(PUSH(cs));	// 33330 push    cs ;~ 0D4F:09F8
cs=0xd4f;eip=0x0009f9; 	J(CALL(sub_1c10a,0));	// 33331 call    near ptr sub_1C10A ;~ 0D4F:09F9
cs=0xd4f;eip=0x0009fc; 	T(ADD(sp, 8));	// 33332 add     sp, 8 ;~ 0D4F:09FC
cs=0xd4f;eip=0x0009ff; 	X(PUSH(dx));	// 33333 push    dx ;~ 0D4F:09FF
cs=0xd4f;eip=0x000a00; 	X(PUSH(ax));	// 33334 push    ax ;~ 0D4F:0A00
cs=0xd4f;eip=0x000a01; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_2))));	// 33335 push    [bp+arg_2] ;~ 0D4F:0A01
cs=0xd4f;eip=0x000a04; 	X(PUSH(cs));	// 33336 push    cs ;~ 0D4F:0A04
cs=0xd4f;eip=0x000a05; 	J(CALL(sub_1c451,0));	// 33337 call    sub_1C451 ;~ 0D4F:0A05
cs=0xd4f;eip=0x000a08; 	T(ADD(sp, 6));	// 33338 add     sp, 6 ;~ 0D4F:0A08
loc_1c4db:
	// 6003 
cs=0xd4f;eip=0x000a0b; //  	T(OR(bh, 0));	// 33341 or      bh, 0 ;~ 0D4F:0A0B
seg002_a0e_proc:
	// 33344 
//cs=0xd4f;eip=0x000a0e; 	X(PUSH(cs));	// 33344 push    cs ;~ 0D4F:0A0E
//cs=0xd4f;eip=0x000a0f; 	J(CALL(_group2,m2c::kloc_1c4db));	// 33345 call    near ptr loc_1C4DB+1 ;~ 0D4F:0A0F
R(POPF);
cs=0xd4f;eip=0x000a12; 	X(POP(di));	// 33346 pop     di ;~ 0D4F:0A12
cs=0xd4f;eip=0x000a13; 	X(POP(si));	// 33347 pop     si ;~ 0D4F:0A13
cs=0xd4f;eip=0x000a14; 	X(POP(ds));	// 33348 pop     ds ;~ 0D4F:0A14
cs=0xd4f;eip=0x000a15; 	X(POP(bp));	// 33349 pop     bp ;~ 0D4F:0A15
cs=0xd4f;eip=0x000a16; 	J(RETF(0));	// 33350 retf ;~ 0D4F:0A16
ret_d4f_a17:
	// 6004 
cs=0xd4f;eip=0x000a17; 	X(PUSH(bp));	// 33352 push    bp ;~ 0D4F:0A17
cs=0xd4f;eip=0x000a18; 	T(MOV(bp, sp));	// 33353 mov     bp, sp ;~ 0D4F:0A18
cs=0xd4f;eip=0x000a1a; 	X(PUSH(ds));	// 33354 push    ds ;~ 0D4F:0A1A
cs=0xd4f;eip=0x000a1b; 	X(PUSH(si));	// 33355 push    si ;~ 0D4F:0A1B
cs=0xd4f;eip=0x000a1c; 	X(PUSH(di));	// 33356 push    di ;~ 0D4F:0A1C
cs=0xd4f;eip=0x000a1d; 	X(PUSHF);	// 33357 pushf ;~ 0D4F:0A1D
cs=0xd4f;eip=0x000a1e; 	T(CLI);	// 33358 cli ;~ 0D4F:0A1E
cs=0xd4f;eip=0x000a1f; 	T(CMP(*(dw*)(raddr(ss,bp+8)), 0));	// 33359 cmp     word ptr [bp+8], 0 ;~ 0D4F:0A1F
cs=0xd4f;eip=0x000a23; 	J(JNZ(loc_1c4fd));	// 33360 jnz     short loc_1C4FD ;~ 0D4F:0A23
cs=0xd4f;eip=0x000a25; 	T(MOV(ax, 0x0D68D));	// 33361 mov     ax, 0D68Dh ;~ 0D4F:0A25
cs=0xd4f;eip=0x000a28; 	T(MOV(dx, 0));	// 33362 mov     dx, 0 ;~ 0D4F:0A28
cs=0xd4f;eip=0x000a2b; 	J(JMP(loc_1c50b));	// 33363 jmp     short loc_1C50B ;~ 0D4F:0A2B
loc_1c4fd:
	// 6005 
cs=0xd4f;eip=0x000a2d; 	T(MOV(ax, 0x2710));	// 33367 mov     ax, 2710h ;~ 0D4F:0A2D
cs=0xd4f;eip=0x000a30; 	T(MOV(bx, 0x2E9C));	// 33368 mov     bx, 2E9Ch ;~ 0D4F:0A30
cs=0xd4f;eip=0x000a33; 	X(MUL1_2(*(dw*)(raddr(ss,bp+8))));	// 33369 mul     word ptr [bp+8] ;~ 0D4F:0A33
cs=0xd4f;eip=0x000a36; 	T(DIV2(bx));	// 33370 div     bx ;~ 0D4F:0A36
cs=0xd4f;eip=0x000a38; 	T(MOV(dx, 0));	// 33371 mov     dx, 0 ;~ 0D4F:0A38
loc_1c50b:
	// 6006 
cs=0xd4f;eip=0x000a3b; 	X(PUSH(dx));	// 33374 push    dx ;~ 0D4F:0A3B
cs=0xd4f;eip=0x000a3c; 	X(PUSH(ax));	// 33375 push    ax ;~ 0D4F:0A3C
cs=0xd4f;eip=0x000a3d; 	X(PUSH(*(dw*)(raddr(ss,bp+6))));	// 33376 push    word ptr [bp+6] ;~ 0D4F:0A3D
cs=0xd4f;eip=0x000a40; 	X(PUSH(cs));	// 33377 push    cs ;~ 0D4F:0A40
cs=0xd4f;eip=0x000a41; 	J(CALL(sub_1c451,0));	// 33378 call    sub_1C451 ;~ 0D4F:0A41
cs=0xd4f;eip=0x000a44; 	T(ADD(sp, 6));	// 33379 add     sp, 6 ;~ 0D4F:0A44
loc_1c517:
	// 6007 
cs=0xd4f;eip=0x000a47; //  	T(OR(bh, 0));	// 33382 or      bh, 0 ;~ 0D4F:0A47
//cs=0xd4f;eip=0x000a4a; 	X(PUSH(cs));	// 33383 push    cs ;~ 0D4F:0A4A
//cs=0xd4f;eip=0x000a4b; 	J(CALL(_group2,m2c::kloc_1c517));	// 33384 call    near ptr loc_1C517+1 ;~ 0D4F:0A4B
R(POPF);
cs=0xd4f;eip=0x000a4e; 	X(POP(di));	// 33385 pop     di ;~ 0D4F:0A4E
cs=0xd4f;eip=0x000a4f; 	X(POP(si));	// 33386 pop     si ;~ 0D4F:0A4F
cs=0xd4f;eip=0x000a50; 	X(POP(ds));	// 33387 pop     ds ;~ 0D4F:0A50
cs=0xd4f;eip=0x000a51; 	X(POP(bp));	// 33388 pop     bp ;~ 0D4F:0A51
cs=0xd4f;eip=0x000a52; 	J(RETF(0));	// 33389 retf ;~ 0D4F:0A52
ret_d4f_a53:
	// 6008 
cs=0xd4f;eip=0x000a53; 	X(PUSH(ds));	// 33391 push    ds ;~ 0D4F:0A53
cs=0xd4f;eip=0x000a54; 	X(PUSH(si));	// 33392 push    si ;~ 0D4F:0A54
cs=0xd4f;eip=0x000a55; 	X(PUSH(di));	// 33393 push    di ;~ 0D4F:0A55
cs=0xd4f;eip=0x000a56; 	X(PUSHF);	// 33394 pushf ;~ 0D4F:0A56
cs=0xd4f;eip=0x000a57; 	T(CLI);	// 33395 cli ;~ 0D4F:0A57
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000a58; 	T(MOV(ax, *(dw*)(((db*)&word_1bbf2))));	// 33396 mov     ax, cs:word_1BBF2 ;~ 0D4F:0A58
loc_1c52c:
	// 6009 
cs=0xd4f;eip=0x000a5c; //  	T(OR(bh, 0));	// 33399 or      bh, 0 ;~ 0D4F:0A5C
//cs=0xd4f;eip=0x000a5f; 	X(PUSH(cs));	// 33400 push    cs ;~ 0D4F:0A5F
//cs=0xd4f;eip=0x000a60; 	J(CALL(_group2,m2c::kloc_1c52c));	// 33401 call    near ptr loc_1C52C+1 ;~ 0D4F:0A60
R(POPF);
cs=0xd4f;eip=0x000a63; 	X(POP(di));	// 33402 pop     di ;~ 0D4F:0A63
cs=0xd4f;eip=0x000a64; 	X(POP(si));	// 33403 pop     si ;~ 0D4F:0A64
cs=0xd4f;eip=0x000a65; 	X(POP(ds));	// 33404 pop     ds ;~ 0D4F:0A65
cs=0xd4f;eip=0x000a66; 	J(RETF(0));	// 33405 retf ;~ 0D4F:0A66
sub_1c537:
	// 33411 
#undef arg_2
#define arg_2 6
	// 33413 arg_2           = dword ptr  6 ;~ 0D4F:0A67
ret_d4f_a67:
	// 6010 
cs=0xd4f;eip=0x000a67; 	X(PUSH(bp));	// 33415 push    bp ;~ 0D4F:0A67
cs=0xd4f;eip=0x000a68; 	T(MOV(bp, sp));	// 33416 mov     bp, sp ;~ 0D4F:0A68
cs=0xd4f;eip=0x000a6a; 	X(PUSH(ds));	// 33417 push    ds ;~ 0D4F:0A6A
cs=0xd4f;eip=0x000a6b; 	X(PUSH(si));	// 33418 push    si ;~ 0D4F:0A6B
cs=0xd4f;eip=0x000a6c; 	X(PUSH(di));	// 33419 push    di ;~ 0D4F:0A6C
cs=0xd4f;eip=0x000a6d; 	X(PUSHF);	// 33420 pushf ;~ 0D4F:0A6D
cs=0xd4f;eip=0x000a6e; 	T(CLI);	// 33421 cli ;~ 0D4F:0A6E
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000a6f; 	X(MOV(*(dw*)(((db*)&word_1bc78)), 0));	// 33422 mov     cs:word_1BC78, 0 ;~ 0D4F:0A6F
loc_1c546:
	// 6011 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000a76; 	T(MOV(si, *(dw*)(((db*)&word_1bc78))));	// 33425 mov     si, cs:word_1BC78 ;~ 0D4F:0A76
cs=0xd4f;eip=0x000a7b; 	T(SHL(si, 1));	// 33426 shl     si, 1 ;~ 0D4F:0A7B
cs=0xd4f;eip=0x000a7d; 	T(SHL(si, 1));	// 33427 shl     si, 1 ;~ 0D4F:0A7D
cs=0xd4f;eip=0x000a7f; 	T(MOV(ax, *(dw*)(raddr(cs,si+0x124))));	// 33428 mov     ax, cs:[si+124h] ;~ 0D4F:0A7F
cs=0xd4f;eip=0x000a84; 	T(OR(ax, *(dw*)(raddr(cs,si+0x126))));	// 33429 or      ax, cs:[si+126h] ;~ 0D4F:0A84
cs=0xd4f;eip=0x000a89; 	J(JZ(loc_1c56d));	// 33430 jz      short loc_1C56D ;~ 0D4F:0A89
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000a8b; 	X(INC(*(dw*)(((db*)&word_1bc78))));	// 33431 inc     cs:word_1BC78 ;~ 0D4F:0A8B
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000a90; 	T(CMP(*(dw*)(((db*)&word_1bc78)), 0x10));	// 33432 cmp     cs:word_1BC78, 10h ;~ 0D4F:0A90
cs=0xd4f;eip=0x000a96; 	J(JNZ(loc_1c546));	// 33433 jnz     short loc_1C546 ;~ 0D4F:0A96
cs=0xd4f;eip=0x000a98; 	T(MOV(ax, 0x0FFFF));	// 33434 mov     ax, 0FFFFh ;~ 0D4F:0A98
cs=0xd4f;eip=0x000a9b; 	J(JMP(loc_1c5b5));	// 33435 jmp     short loc_1C5B5 ;~ 0D4F:0A9B
loc_1c56d:
	// 6012 
cs=0xd4f;eip=0x000a9d; 	T(LES(di, *(dd*)(raddr(ss,bp+arg_2))));	// 33439 les     di, [bp+arg_2] ;~ 0D4F:0A9D
cs=0xd4f;eip=0x000aa0; 	T(MOV(ax, 0x0FFFF));	// 33441 mov     ax, 0FFFFh ;~ 0D4F:0AA0
cs=0xd4f;eip=0x000aa3; 	T(CMP(*(dw*)(raddr(es,di+2)), 0x6F43));	// 33442 cmp     word ptr es:[di+2], 6F43h ;~ 0D4F:0AA3
cs=0xd4f;eip=0x000aa9; 	J(JNZ(loc_1c5b5));	// 33443 jnz     short loc_1C5B5 ;~ 0D4F:0AA9
cs=0xd4f;eip=0x000aab; 	T(CMP(*(dw*)(raddr(es,di+4)), 0x7970));	// 33444 cmp     word ptr es:[di+4], 7970h ;~ 0D4F:0AAB
cs=0xd4f;eip=0x000ab1; 	J(JNZ(loc_1c5b5));	// 33445 jnz     short loc_1C5B5 ;~ 0D4F:0AB1
cs=0xd4f;eip=0x000ab3; 	T(ADD(di, *(dw*)(raddr(es,di))));	// 33446 add     di, es:[di] ;~ 0D4F:0AB3
cs=0xd4f;eip=0x000ab6; 	X(MOV(*(dw*)(raddr(cs,si+0x124)), di));	// 33447 mov     cs:[si+124h], di ;~ 0D4F:0AB6
cs=0xd4f;eip=0x000abb; 	X(MOV(*(dw*)(raddr(cs,si+0x126)), es));	// 33448 mov     word ptr cs:[si+126h], es ;~ 0D4F:0ABB
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000ac0; 	X(PUSH(*(dw*)(((db*)&word_1bc78))));	// 33449 push    cs:word_1BC78 ;~ 0D4F:0AC0
cs=0xd4f;eip=0x000ac5; 	X(PUSH(cs));	// 33450 push    cs ;~ 0D4F:0AC5
cs=0xd4f;eip=0x000ac6; 	J(CALL(sub_1c5ef,0));	// 33451 call    near ptr sub_1C5EF ;~ 0D4F:0AC6
cs=0xd4f;eip=0x000ac9; 	T(ADD(sp, 2));	// 33452 add     sp, 2 ;~ 0D4F:0AC9
cs=0xd4f;eip=0x000acc; 	T(MOV(es, dx));	// 33453 mov     es, dx ;~ 0D4F:0ACC
cs=0xd4f;eip=0x000ace; 	T(MOV(di, ax));	// 33454 mov     di, ax ;~ 0D4F:0ACE
cs=0xd4f;eip=0x000ad0; 	T(OR(dx, ax));	// 33455 or      dx, ax ;~ 0D4F:0AD0
cs=0xd4f;eip=0x000ad2; 	T(MOV(ax, 0x0FFFF));	// 33456 mov     ax, 0FFFFh ;~ 0D4F:0AD2
cs=0xd4f;eip=0x000ad5; 	J(JZ(loc_1c5b5));	// 33457 jz      short loc_1C5B5 ;~ 0D4F:0AD5
cs=0xd4f;eip=0x000ad7; 	T(MOV(dx, *(dw*)(raddr(es,di))));	// 33458 mov     dx, es:[di] ;~ 0D4F:0AD7
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000ada; 	T(CMP(dx, *(dw*)(((db*)&word_1be88))));	// 33459 cmp     dx, cs:word_1BE88 ;~ 0D4F:0ADA
cs=0xd4f;eip=0x000adf; 	J(JA(loc_1c5b5));	// 33460 ja      short loc_1C5B5 ;~ 0D4F:0ADF
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000ae1; 	T(MOV(ax, *(dw*)(((db*)&word_1bc78))));	// 33461 mov     ax, cs:word_1BC78 ;~ 0D4F:0AE1
loc_1c5b5:
	// 6013 
cs=0xd4f;eip=0x000ae5; //  	T(OR(bh, 0));	// 33465 or      bh, 0 ;~ 0D4F:0AE5
seg002_ae8_proc:
	// 33468 
//cs=0xd4f;eip=0x000ae8; 	X(PUSH(cs));	// 33468 push    cs ;~ 0D4F:0AE8
//cs=0xd4f;eip=0x000ae9; 	J(CALL(_group2,m2c::kloc_1c5b5));	// 33469 call    near ptr loc_1C5B5+1 ;~ 0D4F:0AE9
R(POPF);
cs=0xd4f;eip=0x000aec; 	X(POP(di));	// 33470 pop     di ;~ 0D4F:0AEC
cs=0xd4f;eip=0x000aed; 	X(POP(si));	// 33471 pop     si ;~ 0D4F:0AED
cs=0xd4f;eip=0x000aee; 	X(POP(ds));	// 33472 pop     ds ;~ 0D4F:0AEE
cs=0xd4f;eip=0x000aef; 	X(POP(bp));	// 33473 pop     bp ;~ 0D4F:0AEF
cs=0xd4f;eip=0x000af0; 	J(RETF(0));	// 33474 retf ;~ 0D4F:0AF0
ret_d4f_af1:
	// 6014 
cs=0xd4f;eip=0x000af1; 	X(PUSH(bp));	// 33476 push    bp ;~ 0D4F:0AF1
cs=0xd4f;eip=0x000af2; 	T(MOV(bp, sp));	// 33477 mov     bp, sp ;~ 0D4F:0AF2
cs=0xd4f;eip=0x000af4; 	X(PUSH(ds));	// 33478 push    ds ;~ 0D4F:0AF4
cs=0xd4f;eip=0x000af5; 	X(PUSH(si));	// 33479 push    si ;~ 0D4F:0AF5
cs=0xd4f;eip=0x000af6; 	X(PUSH(di));	// 33480 push    di ;~ 0D4F:0AF6
cs=0xd4f;eip=0x000af7; 	X(PUSHF);	// 33481 pushf ;~ 0D4F:0AF7
cs=0xd4f;eip=0x000af8; 	T(CLI);	// 33482 cli ;~ 0D4F:0AF8
cs=0xd4f;eip=0x000af9; 	T(MOV(bx, *(dw*)(raddr(ss,bp+6))));	// 33483 mov     bx, [bp+6] ;~ 0D4F:0AF9
cs=0xd4f;eip=0x000afc; 	T(CMP(bx, 0x10));	// 33484 cmp     bx, 10h ;~ 0D4F:0AFC
cs=0xd4f;eip=0x000aff; 	J(JNC(loc_1c5e3));	// 33485 jnb     short loc_1C5E3 ;~ 0D4F:0AFF
cs=0xd4f;eip=0x000b01; 	T(SHL(bx, 1));	// 33486 shl     bx, 1 ;~ 0D4F:0B01
cs=0xd4f;eip=0x000b03; 	T(SHL(bx, 1));	// 33487 shl     bx, 1 ;~ 0D4F:0B03
cs=0xd4f;eip=0x000b05; 	X(MOV(*(dw*)(raddr(cs,bx+0x124)), 0));	// 33488 mov     word ptr cs:[bx+124h], 0 ;~ 0D4F:0B05
cs=0xd4f;eip=0x000b0c; 	X(MOV(*(dw*)(raddr(cs,bx+0x126)), 0));	// 33489 mov     word ptr cs:[bx+126h], 0 ;~ 0D4F:0B0C
loc_1c5e3:
	// 6015 
cs=0xd4f;eip=0x000b13; //  	T(OR(bh, 0));	// 33493 or      bh, 0 ;~ 0D4F:0B13
//cs=0xd4f;eip=0x000b16; 	X(PUSH(cs));	// 33494 push    cs ;~ 0D4F:0B16
//cs=0xd4f;eip=0x000b17; 	J(CALL(_group2,m2c::kloc_1c5e3));	// 33495 call    near ptr loc_1C5E3+1 ;~ 0D4F:0B17
R(POPF);
cs=0xd4f;eip=0x000b1a; 	X(POP(di));	// 33496 pop     di ;~ 0D4F:0B1A
cs=0xd4f;eip=0x000b1b; 	X(POP(si));	// 33497 pop     si ;~ 0D4F:0B1B
cs=0xd4f;eip=0x000b1c; 	X(POP(ds));	// 33498 pop     ds ;~ 0D4F:0B1C
cs=0xd4f;eip=0x000b1d; 	X(POP(bp));	// 33499 pop     bp ;~ 0D4F:0B1D
cs=0xd4f;eip=0x000b1e; 	J(RETF(0));	// 33500 retf ;~ 0D4F:0B1E
sub_1c5ef:
	// 33506 
#undef arg_0
#define arg_0 6
	// 33509 arg_0           = word ptr  6 ;~ 0D4F:0B1F
ret_d4f_b1f:
	// 6016 
cs=0xd4f;eip=0x000b1f; 	X(PUSH(bp));	// 33511 push    bp ;~ 0D4F:0B1F
cs=0xd4f;eip=0x000b20; 	T(MOV(bp, sp));	// 33512 mov     bp, sp ;~ 0D4F:0B20
cs=0xd4f;eip=0x000b22; 	X(PUSH(ax));	// 33513 push    ax ;~ 0D4F:0B22
cs=0xd4f;eip=0x000b23; 	X(PUSH(bp));	// 33514 push    bp ;~ 0D4F:0B23
cs=0xd4f;eip=0x000b24; 	T(MOV(bp, sp));	// 33515 mov     bp, sp ;~ 0D4F:0B24
cs=0xd4f;eip=0x000b26; 	X(MOV(*(dw*)(raddr(ss,bp+2)), seg_offset(seg002)));	// 33516 mov     word ptr [bp+2], seg seg002 ;~ 0D4F:0B26
cs=0xd4f;eip=0x000b2b; 	X(POP(bp));	// 33517 pop     bp ;~ 0D4F:0B2B
cs=0xd4f;eip=0x000b2c; 	X(PUSH(ax));	// 33518 push    ax ;~ 0D4F:0B2C
cs=0xd4f;eip=0x000b2d; 	X(PUSH(bp));	// 33519 push    bp ;~ 0D4F:0B2D
cs=0xd4f;eip=0x000b2e; 	T(MOV(bp, sp));	// 33520 mov     bp, sp ;~ 0D4F:0B2E
cs=0xd4f;eip=0x000b30; 	X(MOV(*(dw*)(raddr(ss,bp+2)), 0x0A53));	// 33521 mov     word ptr [bp+2], 0A53h ;~ 0D4F:0B30
cs=0xd4f;eip=0x000b35; 	X(POP(bp));	// 33522 pop     bp ;~ 0D4F:0B35
cs=0xd4f;eip=0x000b36; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_0))));	// 33523 push    [bp+arg_0] ;~ 0D4F:0B36
cs=0xd4f;eip=0x000b39; 	T(MOV(ax, 0x64));	// 33524 mov     ax, 64h ; 'd' ;~ 0D4F:0B39
cs=0xd4f;eip=0x000b3c; 	X(PUSH(cs));	// 33525 push    cs ;~ 0D4F:0B3C
cs=0xd4f;eip=0x000b3d; 	J(CALL(sub_1bec2,0));	// 33526 call    near ptr sub_1BEC2 ;~ 0D4F:0B3D
cs=0xd4f;eip=0x000b40; 	T(ADD(sp, 6));	// 33527 add     sp, 6 ;~ 0D4F:0B40
cs=0xd4f;eip=0x000b43; 	X(POP(bp));	// 33528 pop     bp ;~ 0D4F:0B43
cs=0xd4f;eip=0x000b44; 	J(RETF(0));	// 33529 retf ;~ 0D4F:0B44
sub_1c615:
	// 33536 
cs=0xd4f;eip=0x000b45; 	T(MOV(ax, 0x65));	// 33537 mov     ax, 65h ; 'e' ;~ 0D4F:0B45
ret_d4f_b48:
	// 6017 
cs=0xd4f;eip=0x000b48; 	J(JMP(sub_1bec2));	// 33538 jmp     near ptr sub_1BEC2 ;~ 0D4F:0B48
sub_1c61b:
	// 33546 
#undef arg_2
#define arg_2 6
	// 33548 arg_2           = word ptr  6 ;~ 0D4F:0B4B
#undef arg_4
#define arg_4 8
	// 33549 arg_4           = word ptr  8 ;~ 0D4F:0B4B
#undef arg_6
#define arg_6 0x0A
	// 33550 arg_6           = word ptr  0Ah ;~ 0D4F:0B4B
#undef arg_8
#define arg_8 0x0C
	// 33551 arg_8           = word ptr  0Ch ;~ 0D4F:0B4B
#undef arg_a
#define arg_a 0x0E
	// 33552 arg_A           = word ptr  0Eh ;~ 0D4F:0B4B
ret_d4f_b4b:
	// 6018 
cs=0xd4f;eip=0x000b4b; 	X(PUSH(bp));	// 33554 push    bp ;~ 0D4F:0B4B
cs=0xd4f;eip=0x000b4c; 	T(MOV(bp, sp));	// 33555 mov     bp, sp ;~ 0D4F:0B4C
cs=0xd4f;eip=0x000b4e; 	X(PUSH(ds));	// 33556 push    ds ;~ 0D4F:0B4E
cs=0xd4f;eip=0x000b4f; 	X(PUSH(si));	// 33557 push    si ;~ 0D4F:0B4F
cs=0xd4f;eip=0x000b50; 	X(PUSH(di));	// 33558 push    di ;~ 0D4F:0B50
cs=0xd4f;eip=0x000b51; 	X(PUSHF);	// 33559 pushf ;~ 0D4F:0B51
cs=0xd4f;eip=0x000b52; 	T(CLI);	// 33560 cli ;~ 0D4F:0B52
cs=0xd4f;eip=0x000b53; 	T(CMP(*(dw*)(raddr(ss,bp+arg_2)), 0x10));	// 33561 cmp     [bp+arg_2], 10h ;~ 0D4F:0B53
cs=0xd4f;eip=0x000b57; 	J(JC(loc_1c62c));	// 33562 jb      short loc_1C62C ;~ 0D4F:0B57
cs=0xd4f;eip=0x000b59; 	J(JMP(loc_1c6c4));	// 33563 jmp     loc_1C6C4 ;~ 0D4F:0B59
loc_1c62c:
	// 6019 
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000b5c; 	X(MOV(*(dw*)(((db*)&word_1bc7e)), 0x0FFFF));	// 33567 mov     cs:word_1BC7E, 0FFFFh ;~ 0D4F:0B5C
cs=0xd4f;eip=0x000b63; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_2))));	// 33568 push    [bp+arg_2] ;~ 0D4F:0B63
cs=0xd4f;eip=0x000b66; 	X(PUSH(cs));	// 33569 push    cs ;~ 0D4F:0B66
cs=0xd4f;eip=0x000b67; 	J(CALL(sub_1c5ef,0));	// 33570 call    near ptr sub_1C5EF ;~ 0D4F:0B67
cs=0xd4f;eip=0x000b6a; 	T(ADD(sp, 2));	// 33571 add     sp, 2 ;~ 0D4F:0B6A
cs=0xd4f;eip=0x000b6d; 	T(MOV(es, dx));	// 33572 mov     es, dx ;~ 0D4F:0B6D
cs=0xd4f;eip=0x000b6f; 	T(MOV(di, ax));	// 33573 mov     di, ax ;~ 0D4F:0B6F
cs=0xd4f;eip=0x000b71; 	T(MOV(si, *(dw*)(raddr(es,di+0x14))));	// 33574 mov     si, es:[di+14h] ;~ 0D4F:0B71
cs=0xd4f;eip=0x000b75; 	T(CMP(si, 0x0FFFF));	// 33575 cmp     si, 0FFFFh ;~ 0D4F:0B75
cs=0xd4f;eip=0x000b78; 	J(JZ(loc_1c68b));	// 33576 jz      short loc_1C68B ;~ 0D4F:0B78
cs=0xd4f;eip=0x000b7a; 	T(ADD(si, 5));	// 33577 add     si, 5 ;~ 0D4F:0B7A
cs=0xd4f;eip=0x000b7d; 	T(MOV(ax, 0x67));	// 33578 mov     ax, 67h ; 'g' ;~ 0D4F:0B7D
cs=0xd4f;eip=0x000b80; 	T(MOV(bx, *(dw*)(raddr(ss,bp+arg_2))));	// 33579 mov     bx, [bp+arg_2] ;~ 0D4F:0B80
cs=0xd4f;eip=0x000b83; 	X(PUSH(cs));	// 33580 push    cs ;~ 0D4F:0B83
cs=0xd4f;eip=0x000b84; 	J(CALL(sub_1be8a,0));	// 33581 call    near ptr sub_1BE8A ;~ 0D4F:0B84
cs=0xd4f;eip=0x000b87; 	T(MOV(bx, ax));	// 33582 mov     bx, ax ;~ 0D4F:0B87
cs=0xd4f;eip=0x000b89; 	T(OR(bx, dx));	// 33583 or      bx, dx ;~ 0D4F:0B89
cs=0xd4f;eip=0x000b8b; 	J(JZ(loc_1c68b));	// 33584 jz      short loc_1C68B ;~ 0D4F:0B8B
cs=0xd4f;eip=0x000b8d; 	T(MOV(es, dx));	// 33585 mov     es, dx ;~ 0D4F:0B8D
cs=0xd4f;eip=0x000b8f; 	T(MOV(bx, ax));	// 33586 mov     bx, ax ;~ 0D4F:0B8F
cs=0xd4f;eip=0x000b91; 	X(PUSH(es));	// 33587 push    es ;~ 0D4F:0B91
cs=0xd4f;eip=0x000b92; 	X(PUSH(bx));	// 33588 push    bx ;~ 0D4F:0B92
cs=0xd4f;eip=0x000b93; 	X(PUSH(cs));	// 33589 push    cs ;~ 0D4F:0B93
cs=0xd4f;eip=0x000b94; 	J(CALL(sub_1c293,0));	// 33590 call    sub_1C293 ;~ 0D4F:0B94
cs=0xd4f;eip=0x000b97; 	T(ADD(sp, 4));	// 33591 add     sp, 4 ;~ 0D4F:0B97
cs=0xd4f;eip=0x000b9a; 	T(MOV(bx, *(dw*)(raddr(ss,bp+arg_2))));	// 33592 mov     bx, [bp+arg_2] ;~ 0D4F:0B9A
cs=0xd4f;eip=0x000b9d; 	T(SHL(bx, 1));	// 33593 shl     bx, 1 ;~ 0D4F:0B9D
cs=0xd4f;eip=0x000b9f; 	X(MOV(*(dw*)(raddr(cs,bx+0x164)), ax));	// 33594 mov     cs:[bx+164h], ax ;~ 0D4F:0B9F
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000ba4; 	X(MOV(*(dw*)(((db*)&word_1bc7e)), ax));	// 33595 mov     cs:word_1BC7E, ax ;~ 0D4F:0BA4
cs=0xd4f;eip=0x000ba8; 	X(PUSH(ax));	// 33596 push    ax ;~ 0D4F:0BA8
cs=0xd4f;eip=0x000ba9; 	X(PUSH(bp));	// 33597 push    bp ;~ 0D4F:0BA9
cs=0xd4f;eip=0x000baa; 	T(MOV(bp, sp));	// 33598 mov     bp, sp ;~ 0D4F:0BAA
cs=0xd4f;eip=0x000bac; 	X(MOV(*(dw*)(raddr(ss,bp+2)), 0));	// 33599 mov     word ptr [bp+2], 0 ;~ 0D4F:0BAC
cs=0xd4f;eip=0x000bb1; 	X(POP(bp));	// 33600 pop     bp ;~ 0D4F:0BB1
cs=0xd4f;eip=0x000bb2; 	X(PUSH(si));	// 33601 push    si ;~ 0D4F:0BB2
cs=0xd4f;eip=0x000bb3; 	X(PUSH(ax));	// 33602 push    ax ;~ 0D4F:0BB3
cs=0xd4f;eip=0x000bb4; 	X(PUSH(cs));	// 33603 push    cs ;~ 0D4F:0BB4
cs=0xd4f;eip=0x000bb5; 	J(CALL(sub_1c4a6,0));	// 33604 call    sub_1C4A6 ;~ 0D4F:0BB5
cs=0xd4f;eip=0x000bb8; 	T(ADD(sp, 6));	// 33605 add     sp, 6 ;~ 0D4F:0BB8
loc_1c68b:
	// 6020 
cs=0xd4f;eip=0x000bbb; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_a))));	// 33609 push    [bp+arg_A] ;~ 0D4F:0BBB
cs=0xd4f;eip=0x000bbe; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_8))));	// 33610 push    [bp+arg_8] ;~ 0D4F:0BBE
cs=0xd4f;eip=0x000bc1; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_6))));	// 33611 push    [bp+arg_6] ;~ 0D4F:0BC1
cs=0xd4f;eip=0x000bc4; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_4))));	// 33612 push    [bp+arg_4] ;~ 0D4F:0BC4
cs=0xd4f;eip=0x000bc7; 	X(PUSH(*(dw*)(raddr(ss,bp+arg_2))));	// 33613 push    [bp+arg_2] ;~ 0D4F:0BC7
cs=0xd4f;eip=0x000bca; 	T(MOV(ax, 0x66));	// 33614 mov     ax, 66h ; 'f' ;~ 0D4F:0BCA
cs=0xd4f;eip=0x000bcd; 	X(PUSH(cs));	// 33615 push    cs ;~ 0D4F:0BCD
cs=0xd4f;eip=0x000bce; 	J(CALL(sub_1bec2,0));	// 33616 call    near ptr sub_1BEC2 ;~ 0D4F:0BCE
cs=0xd4f;eip=0x000bd1; 	T(ADD(sp, 0x0A));	// 33617 add     sp, 0Ah ;~ 0D4F:0BD1
cs=0xd4f;eip=0x000bd4; 	T(MOV(bx, *(dw*)(raddr(ss,bp+arg_2))));	// 33618 mov     bx, [bp+arg_2] ;~ 0D4F:0BD4
cs=0xd4f;eip=0x000bd7; 	T(SHL(bx, 1));	// 33619 shl     bx, 1 ;~ 0D4F:0BD7
cs=0xd4f;eip=0x000bd9; 	X(MOV(*(dw*)(raddr(cs,bx+0x184)), 1));	// 33620 mov     word ptr cs:[bx+184h], 1 ;~ 0D4F:0BD9
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000be0; 	T(CMP(*(dw*)(((db*)&word_1bc7e)), 0x0FFFF));	// 33621 cmp     cs:word_1BC7E, 0FFFFh ;~ 0D4F:0BE0
cs=0xd4f;eip=0x000be6; 	J(JZ(loc_1c6c4));	// 33622 jz      short loc_1C6C4 ;~ 0D4F:0BE6
	cs=seg_offset(seg002);
cs=0xd4f;eip=0x000be8; 	X(PUSH(*(dw*)(((db*)&word_1bc7e))));	// 33623 push    cs:word_1BC7E ;~ 0D4F:0BE8
cs=0xd4f;eip=0x000bed; 	X(PUSH(cs));	// 33624 push    cs ;~ 0D4F:0BED
cs=0xd4f;eip=0x000bee; 	J(CALL(sub_1c3c5,0));	// 33625 call    sub_1C3C5 ;~ 0D4F:0BEE
cs=0xd4f;eip=0x000bf1; 	T(ADD(sp, 2));	// 33626 add     sp, 2 ;~ 0D4F:0BF1
loc_1c6c4:
	// 6021 
cs=0xd4f;eip=0x000bf4; //  	T(OR(bh, 0));	// 33630 or      bh, 0 ;~ 0D4F:0BF4
seg002_bf7_proc:
	// 33633 
//cs=0xd4f;eip=0x000bf7; 	X(PUSH(cs));	// 33633 push    cs ;~ 0D4F:0BF7
//cs=0xd4f;eip=0x000bf8; 	J(CALL(_group2,m2c::kloc_1c6c4));	// 33634 call    near ptr loc_1C6C4+1 ;~ 0D4F:0BF8
R(POPF);
cs=0xd4f;eip=0x000bfb; 	X(POP(di));	// 33635 pop     di ;~ 0D4F:0BFB
cs=0xd4f;eip=0x000bfc; 	X(POP(si));	// 33636 pop     si ;~ 0D4F:0BFC
cs=0xd4f;eip=0x000bfd; 	X(POP(ds));	// 33637 pop     ds ;~ 0D4F:0BFD
cs=0xd4f;eip=0x000bfe; 	X(POP(bp));	// 33638 pop     bp ;~ 0D4F:0BFE
cs=0xd4f;eip=0x000bff; 	J(RETF(0));	// 33639 retf ;~ 0D4F:0BFF
sub_1c6d0:
	// 33644 
cs=0xd4f;eip=0x000c00; 	T(MOV(bx, sp));	// 33645 mov     bx, sp ;~ 0D4F:0C00
ret_d4f_c02:
	// 6022 
cs=0xd4f;eip=0x000c02; 	T(MOV(bx, *(dw*)(raddr(ss,bx+4))));	// 33646 mov     bx, ss:[bx+4] ;~ 0D4F:0C02
cs=0xd4f;eip=0x000c06; 	T(CMP(bx, 0x10));	// 33647 cmp     bx, 10h ;~ 0D4F:0C06
cs=0xd4f;eip=0x000c09; 	J(JNC(locret_1c702));	// 33648 jnb     short locret_1C702 ;~ 0D4F:0C09
cs=0xd4f;eip=0x000c0b; 	T(SHL(bx, 1));	// 33649 shl     bx, 1 ;~ 0D4F:0C0B
cs=0xd4f;eip=0x000c0d; 	T(MOV(dx, 0));	// 33650 mov     dx, 0 ;~ 0D4F:0C0D
cs=0xd4f;eip=0x000c10; 	X(XCHG(dx, *(dw*)(raddr(cs,bx+0x184))));	// 33651 xchg    dx, cs:[bx+184h] ;~ 0D4F:0C10
cs=0xd4f;eip=0x000c15; 	T(CMP(dx, 0));	// 33652 cmp     dx, 0 ;~ 0D4F:0C15
cs=0xd4f;eip=0x000c18; 	J(JZ(locret_1c702));	// 33653 jz      short locret_1C702 ;~ 0D4F:0C18
cs=0xd4f;eip=0x000c1a; 	T(MOV(dx, *(dw*)(raddr(cs,bx+0x164))));	// 33654 mov     dx, cs:[bx+164h] ;~ 0D4F:0C1A
cs=0xd4f;eip=0x000c1f; 	T(CMP(dx, 0x0FFFF));	// 33655 cmp     dx, 0FFFFh ;~ 0D4F:0C1F
cs=0xd4f;eip=0x000c22; 	J(JZ(loc_1c6fc));	// 33656 jz      short loc_1C6FC ;~ 0D4F:0C22
cs=0xd4f;eip=0x000c24; 	X(PUSH(dx));	// 33657 push    dx ;~ 0D4F:0C24
cs=0xd4f;eip=0x000c25; 	X(PUSH(cs));	// 33658 push    cs ;~ 0D4F:0C25
cs=0xd4f;eip=0x000c26; 	J(CALL(sub_1c35e,0));	// 33659 call    sub_1C35E ;~ 0D4F:0C26
cs=0xd4f;eip=0x000c29; 	T(ADD(sp, 2));	// 33660 add     sp, 2 ;~ 0D4F:0C29
loc_1c6fc:
	// 6023 
cs=0xd4f;eip=0x000c2c; 	T(MOV(ax, 0x68));	// 33663 mov     ax, 68h ; 'h' ;~ 0D4F:0C2C
cs=0xd4f;eip=0x000c2f; 	J(JMP(sub_1bec2));	// 33664 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C2F
locret_1c702:
	// 6024 
cs=0xd4f;eip=0x000c32; 	J(RETF(0));	// 33669 retf ;~ 0D4F:0C32
seg002_c33_proc:
	// 33673 
cs=0xd4f;eip=0x000c33; 	T(MOV(ax, 0x78));	// 33673 mov     ax, 78h ; 'x' ;~ 0D4F:0C33
ret_d4f_c36:
	// 6025 
cs=0xd4f;eip=0x000c36; 	J(JMP(sub_1bec2));	// 33674 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C36
ret_d4f_c39:
	// 6026 
cs=0xd4f;eip=0x000c39; 	T(MOV(ax, 0x79));	// 33676 mov     ax, 79h ; 'y' ;~ 0D4F:0C39
cs=0xd4f;eip=0x000c3c; 	J(JMP(sub_1bec2));	// 33677 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C3C
ret_d4f_c3f:
	// 6027 
cs=0xd4f;eip=0x000c3f; 	T(MOV(ax, 0x86));	// 33679 mov     ax, 86h ; '†' ;~ 0D4F:0C3F
cs=0xd4f;eip=0x000c42; 	J(JMP(sub_1bec2));	// 33680 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C42
ret_d4f_c45:
	// 6028 
cs=0xd4f;eip=0x000c45; 	T(MOV(ax, 0x7A));	// 33682 mov     ax, 7Ah ; 'z' ;~ 0D4F:0C45
cs=0xd4f;eip=0x000c48; 	J(JMP(sub_1bec2));	// 33683 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C48
ret_d4f_c4b:
	// 6029 
cs=0xd4f;eip=0x000c4b; 	T(MOV(ax, 0x7B));	// 33685 mov     ax, 7Bh ; '{' ;~ 0D4F:0C4B
cs=0xd4f;eip=0x000c4e; 	J(JMP(sub_1bec2));	// 33686 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C4E
ret_d4f_c51:
	// 6030 
cs=0xd4f;eip=0x000c51; 	T(MOV(ax, 0x85));	// 33688 mov     ax, 85h ; '…' ;~ 0D4F:0C51
cs=0xd4f;eip=0x000c54; 	J(JMP(sub_1bec2));	// 33689 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C54
ret_d4f_c57:
	// 6031 
cs=0xd4f;eip=0x000c57; 	T(MOV(ax, 0x7C));	// 33691 mov     ax, 7Ch ; '|' ;~ 0D4F:0C57
cs=0xd4f;eip=0x000c5a; 	J(JMP(sub_1bec2));	// 33692 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C5A
ret_d4f_c5d:
	// 6032 
cs=0xd4f;eip=0x000c5d; 	T(MOV(ax, 0x7D));	// 33694 mov     ax, 7Dh ; '}' ;~ 0D4F:0C5D
cs=0xd4f;eip=0x000c60; 	J(JMP(sub_1bec2));	// 33695 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C60
ret_d4f_c63:
	// 6033 
cs=0xd4f;eip=0x000c63; 	T(MOV(ax, 0x7E));	// 33697 mov     ax, 7Eh ; '~' ;~ 0D4F:0C63
cs=0xd4f;eip=0x000c66; 	J(JMP(sub_1bec2));	// 33698 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C66
ret_d4f_c69:
	// 6034 
cs=0xd4f;eip=0x000c69; 	T(MOV(ax, 0x7F));	// 33700 mov     ax, 7Fh ;~ 0D4F:0C69
cs=0xd4f;eip=0x000c6c; 	J(JMP(sub_1bec2));	// 33701 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C6C
ret_d4f_c6f:
	// 6035 
cs=0xd4f;eip=0x000c6f; 	T(MOV(ax, 0x80));	// 33703 mov     ax, 80h ; '€' ;~ 0D4F:0C6F
cs=0xd4f;eip=0x000c72; 	J(JMP(sub_1bec2));	// 33704 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C72
ret_d4f_c75:
	// 6036 
cs=0xd4f;eip=0x000c75; 	T(MOV(ax, 0x81));	// 33706 mov     ax, 81h ;~ 0D4F:0C75
cs=0xd4f;eip=0x000c78; 	J(JMP(sub_1bec2));	// 33707 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C78
ret_d4f_c7b:
	// 6037 
cs=0xd4f;eip=0x000c7b; 	T(MOV(ax, 0x82));	// 33709 mov     ax, 82h ; '‚' ;~ 0D4F:0C7B
cs=0xd4f;eip=0x000c7e; 	J(JMP(sub_1bec2));	// 33710 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C7E
ret_d4f_c81:
	// 6038 
cs=0xd4f;eip=0x000c81; 	T(MOV(ax, 0x83));	// 33712 mov     ax, 83h ; 'ƒ' ;~ 0D4F:0C81
cs=0xd4f;eip=0x000c84; 	J(JMP(sub_1bec2));	// 33713 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C84
ret_d4f_c87:
	// 6039 
cs=0xd4f;eip=0x000c87; 	T(MOV(ax, 0x84));	// 33715 mov     ax, 84h ; '„' ;~ 0D4F:0C87
cs=0xd4f;eip=0x000c8a; 	J(JMP(sub_1bec2));	// 33716 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C8A
ret_d4f_c8d:
	// 6040 
cs=0xd4f;eip=0x000c8d; 	T(MOV(ax, 0x96));	// 33718 mov     ax, 96h ; '–' ;~ 0D4F:0C8D
cs=0xd4f;eip=0x000c90; 	J(JMP(sub_1bec2));	// 33719 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C90
sub_1c763:
	// 33724 
cs=0xd4f;eip=0x000c93; 	T(MOV(ax, 0x97));	// 33725 mov     ax, 97h ; '—' ;~ 0D4F:0C93
ret_d4f_c96:
	// 6041 
cs=0xd4f;eip=0x000c96; 	J(JMP(sub_1bec2));	// 33726 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C96
sub_1c769:
	// 33733 
cs=0xd4f;eip=0x000c99; 	T(MOV(ax, 0x98));	// 33735 mov     ax, 98h ; '˜' ;~ 0D4F:0C99
ret_d4f_c9c:
	// 6042 
cs=0xd4f;eip=0x000c9c; 	J(JMP(sub_1bec2));	// 33736 jmp     near ptr sub_1BEC2 ;~ 0D4F:0C9C
sub_1c76f:
	// 33743 
cs=0xd4f;eip=0x000c9f; 	T(MOV(ax, 0x99));	// 33744 mov     ax, 99h ; '™' ;~ 0D4F:0C9F
ret_d4f_ca2:
	// 6043 
cs=0xd4f;eip=0x000ca2; 	J(JMP(sub_1bec2));	// 33745 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CA2
sub_1c775:
	// 33752 
cs=0xd4f;eip=0x000ca5; 	T(MOV(ax, 0x9A));	// 33753 mov     ax, 9Ah ; 'š' ;~ 0D4F:0CA5
ret_d4f_ca8:
	// 6044 
cs=0xd4f;eip=0x000ca8; 	J(JMP(sub_1bec2));	// 33754 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CA8
sub_1c77b:
	// 33761 
cs=0xd4f;eip=0x000cab; 	T(MOV(ax, 0x9B));	// 33762 mov     ax, 9Bh ; '›' ;~ 0D4F:0CAB
ret_d4f_cae:
	// 6045 
cs=0xd4f;eip=0x000cae; 	J(JMP(sub_1bec2));	// 33763 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CAE
sub_1c781:
	// 33770 
cs=0xd4f;eip=0x000cb1; 	T(MOV(ax, 0x9C));	// 33771 mov     ax, 9Ch ; 'œ' ;~ 0D4F:0CB1
ret_d4f_cb4:
	// 6046 
cs=0xd4f;eip=0x000cb4; 	J(JMP(sub_1bec2));	// 33772 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CB4
seg002_cb7_proc:
	// 33776 
cs=0xd4f;eip=0x000cb7; 	T(MOV(ax, 0x9D));	// 33776 mov     ax, 9Dh ;~ 0D4F:0CB7
ret_d4f_cba:
	// 6047 
cs=0xd4f;eip=0x000cba; 	J(JMP(sub_1bec2));	// 33777 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CBA
ret_d4f_cbd:
	// 6048 
cs=0xd4f;eip=0x000cbd; 	T(MOV(ax, 0x9E));	// 33779 mov     ax, 9Eh ; 'ž' ;~ 0D4F:0CBD
cs=0xd4f;eip=0x000cc0; 	J(JMP(sub_1bec2));	// 33780 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CC0
ret_d4f_cc3:
	// 6049 
cs=0xd4f;eip=0x000cc3; 	T(MOV(ax, 0x9F));	// 33782 mov     ax, 9Fh ; 'Ÿ' ;~ 0D4F:0CC3
cs=0xd4f;eip=0x000cc6; 	J(JMP(sub_1bec2));	// 33783 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CC6
sub_1c799:
	// 33788 
cs=0xd4f;eip=0x000cc9; 	T(MOV(ax, 0x0AA));	// 33789 mov     ax, 0AAh ; 'ª' ;~ 0D4F:0CC9
ret_d4f_ccc:
	// 6050 
cs=0xd4f;eip=0x000ccc; 	J(JMP(sub_1bec2));	// 33790 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CCC
sub_1c79f:
	// 33797 
cs=0xd4f;eip=0x000ccf; 	T(MOV(ax, 0x0AB));	// 33799 mov     ax, 0ABh ; '«' ;~ 0D4F:0CCF
ret_d4f_cd2:
	// 6051 
cs=0xd4f;eip=0x000cd2; 	J(JMP(sub_1bec2));	// 33800 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CD2
seg002_cd5_proc:
	// 33804 
cs=0xd4f;eip=0x000cd5; 	T(MOV(ax, 0x0AD));	// 33804 mov     ax, 0ADh ; '­' ;~ 0D4F:0CD5
ret_d4f_cd8:
	// 6052 
cs=0xd4f;eip=0x000cd8; 	J(JMP(sub_1bec2));	// 33805 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CD8
sub_1c7ab:
	// 33810 
cs=0xd4f;eip=0x000cdb; 	T(MOV(ax, 0x0AE));	// 33811 mov     ax, 0AEh ; '®' ;~ 0D4F:0CDB
ret_d4f_cde:
	// 6053 
cs=0xd4f;eip=0x000cde; 	J(JMP(sub_1bec2));	// 33812 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CDE
seg002_ce1_proc:
	// 33816 
cs=0xd4f;eip=0x000ce1; 	T(MOV(ax, 0x0AF));	// 33816 mov     ax, 0AFh ; '¯' ;~ 0D4F:0CE1
ret_d4f_ce4:
	// 6054 
cs=0xd4f;eip=0x000ce4; 	J(JMP(sub_1bec2));	// 33817 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CE4
ret_d4f_ce7:
	// 6055 
cs=0xd4f;eip=0x000ce7; 	T(MOV(ax, 0x0B0));	// 33819 mov     ax, 0B0h ; '°' ;~ 0D4F:0CE7
cs=0xd4f;eip=0x000cea; 	J(JMP(sub_1bec2));	// 33820 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CEA
sub_1c7bd:
	// 33825 
cs=0xd4f;eip=0x000ced; 	T(MOV(ax, 0x0B1));	// 33826 mov     ax, 0B1h ; '±' ;~ 0D4F:0CED
ret_d4f_cf0:
	// 6056 
cs=0xd4f;eip=0x000cf0; 	J(JMP(sub_1bec2));	// 33827 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CF0
seg002_cf3_proc:
	// 33831 
cs=0xd4f;eip=0x000cf3; 	T(MOV(ax, 0x0B2));	// 33831 mov     ax, 0B2h ; '²' ;~ 0D4F:0CF3
ret_d4f_cf6:
	// 6057 
cs=0xd4f;eip=0x000cf6; 	J(JMP(sub_1bec2));	// 33832 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CF6
ret_d4f_cf9:
	// 6058 
cs=0xd4f;eip=0x000cf9; 	T(MOV(ax, 0x0B3));	// 33834 mov     ax, 0B3h ; '³' ;~ 0D4F:0CF9
cs=0xd4f;eip=0x000cfc; 	J(JMP(sub_1bec2));	// 33835 jmp     near ptr sub_1BEC2 ;~ 0D4F:0CFC
ret_d4f_cff:
	// 6059 
cs=0xd4f;eip=0x000cff; 	T(MOV(ax, 0x0B4));	// 33837 mov     ax, 0B4h ; '´' ;~ 0D4F:0CFF
cs=0xd4f;eip=0x000d02; 	J(JMP(sub_1bec2));	// 33838 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D02
ret_d4f_d05:
	// 6060 
cs=0xd4f;eip=0x000d05; 	T(MOV(ax, 0x0B5));	// 33840 mov     ax, 0B5h ; 'µ' ;~ 0D4F:0D05
cs=0xd4f;eip=0x000d08; 	J(JMP(sub_1bec2));	// 33841 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D08
ret_d4f_d0b:
	// 6061 
cs=0xd4f;eip=0x000d0b; 	T(MOV(ax, 0x0B6));	// 33843 mov     ax, 0B6h ; '¶' ;~ 0D4F:0D0B
cs=0xd4f;eip=0x000d0e; 	J(JMP(sub_1bec2));	// 33844 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D0E
ret_d4f_d11:
	// 6062 
cs=0xd4f;eip=0x000d11; 	T(MOV(ax, 0x0B7));	// 33846 mov     ax, 0B7h ; '·' ;~ 0D4F:0D11
cs=0xd4f;eip=0x000d14; 	J(JMP(sub_1bec2));	// 33847 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D14
ret_d4f_d17:
	// 6063 
cs=0xd4f;eip=0x000d17; 	T(MOV(ax, 0x0B9));	// 33849 mov     ax, 0B9h ; '¹' ;~ 0D4F:0D17
cs=0xd4f;eip=0x000d1a; 	J(JMP(sub_1bec2));	// 33850 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D1A
ret_d4f_d1d:
	// 6064 
cs=0xd4f;eip=0x000d1d; 	T(MOV(ax, 0x0BA));	// 33852 mov     ax, 0BAh ; 'º' ;~ 0D4F:0D1D
cs=0xd4f;eip=0x000d20; 	J(JMP(sub_1bec2));	// 33853 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D20
ret_d4f_d23:
	// 6065 
cs=0xd4f;eip=0x000d23; 	T(MOV(ax, 0x0BB));	// 33855 mov     ax, 0BBh ; '»' ;~ 0D4F:0D23
cs=0xd4f;eip=0x000d26; 	J(JMP(sub_1bec2));	// 33856 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D26
ret_d4f_d29:
	// 6066 
cs=0xd4f;eip=0x000d29; 	T(MOV(ax, 0x0BC));	// 33858 mov     ax, 0BCh ; '¼' ;~ 0D4F:0D29
cs=0xd4f;eip=0x000d2c; 	J(JMP(sub_1bec2));	// 33859 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D2C
ret_d4f_d2f:
	// 6067 
cs=0xd4f;eip=0x000d2f; 	T(MOV(ax, 0x0BD));	// 33861 mov     ax, 0BDh ; '½' ;~ 0D4F:0D2F
cs=0xd4f;eip=0x000d32; 	J(JMP(sub_1bec2));	// 33862 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D32
ret_d4f_d35:
	// 6068 
cs=0xd4f;eip=0x000d35; 	T(MOV(ax, 0x0BE));	// 33864 mov     ax, 0BEh ; '¾' ;~ 0D4F:0D35
cs=0xd4f;eip=0x000d38; 	J(JMP(sub_1bec2));	// 33865 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D38
ret_d4f_d3b:
	// 6069 
cs=0xd4f;eip=0x000d3b; 	T(MOV(ax, 0x0BF));	// 33867 mov     ax, 0BFh ; '¿' ;~ 0D4F:0D3B
cs=0xd4f;eip=0x000d3e; 	J(JMP(sub_1bec2));	// 33868 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D3E
ret_d4f_d41:
	// 6070 
cs=0xd4f;eip=0x000d41; 	T(MOV(ax, 0x0C0));	// 33870 mov     ax, 0C0h ; 'À' ;~ 0D4F:0D41
cs=0xd4f;eip=0x000d44; 	J(JMP(sub_1bec2));	// 33871 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D44
ret_d4f_d47:
	// 6071 
cs=0xd4f;eip=0x000d47; 	T(MOV(ax, 0x0C1));	// 33873 mov     ax, 0C1h ; 'Á' ;~ 0D4F:0D47
cs=0xd4f;eip=0x000d4a; 	J(JMP(sub_1bec2));	// 33874 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D4A
ret_d4f_d4d:
	// 6072 
cs=0xd4f;eip=0x000d4d; 	T(MOV(ax, 0x0C2));	// 33876 mov     ax, 0C2h ; 'Â' ;~ 0D4F:0D4D
cs=0xd4f;eip=0x000d50; 	J(JMP(sub_1bec2));	// 33877 jmp     near ptr sub_1BEC2 ;~ 0D4F:0D50

    assert(0);
    __dispatch_call:
#ifdef DOSBOX_CUSTOM
    if ((__disp >> 16) == 0xf000)
	{cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
    if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
#endif
    switch (__disp) {
        case m2c::kloc_1be9e: 	goto loc_1be9e;
        case m2c::kloc_1beb4: 	goto loc_1beb4;
        case m2c::kloc_1bebb: 	goto loc_1bebb;
        case m2c::kloc_1bed6: 	goto loc_1bed6;
        case m2c::kloc_1beda: 	goto loc_1beda;
        case m2c::kloc_1bef3: 	goto loc_1bef3;
        case m2c::kloc_1bef9: 	goto loc_1bef9;
        case m2c::kloc_1befe: 	goto loc_1befe;
        case m2c::kloc_1bf0d: 	goto loc_1bf0d;
        case m2c::kloc_1bf13: 	goto loc_1bf13;
        case m2c::kloc_1bf39: 	goto loc_1bf39;
        case m2c::kloc_1bf51: 	goto loc_1bf51;
        case m2c::kloc_1bf8b: 	goto loc_1bf8b;
        case m2c::kloc_1bf97: 	goto loc_1bf97;
        case m2c::kloc_1bfb0: 	goto loc_1bfb0;
        case m2c::kloc_1bfc7: 	goto loc_1bfc7;
        case m2c::kloc_1bfec: 	goto loc_1bfec;
        case m2c::kloc_1c029: 	goto loc_1c029;
        case m2c::kloc_1c07c: 	goto loc_1c07c;
        case m2c::kloc_1c0ac: 	goto loc_1c0ac;
        case m2c::kloc_1c0cc: 	goto loc_1c0cc;
        case m2c::kloc_1c0d2: 	goto loc_1c0d2;
        case m2c::kloc_1c0d4: 	goto loc_1c0d4;
        case m2c::kloc_1c0fd: 	goto loc_1c0fd;
        case m2c::kloc_1c128: 	goto loc_1c128;
        case m2c::kloc_1c131: 	goto loc_1c131;
        case m2c::kloc_1c143: 	goto loc_1c143;
        case m2c::kloc_1c148: 	goto loc_1c148;
        case m2c::kloc_1c14c: 	goto loc_1c14c;
        case m2c::kloc_1c150: 	goto loc_1c150;
        case m2c::kloc_1c16c: 	goto loc_1c16c;
        case m2c::kloc_1c194: 	goto loc_1c194;
        case m2c::kloc_1c19d: 	goto loc_1c19d;
        case m2c::kloc_1c1ba: 	goto loc_1c1ba;
        case m2c::kloc_1c1df: 	goto loc_1c1df;
        case m2c::kloc_1c223: 	goto loc_1c223;
        case m2c::kloc_1c23d: 	goto loc_1c23d;
        case m2c::kloc_1c264: 	goto loc_1c264;
        case m2c::kloc_1c276: 	goto loc_1c276;
        case m2c::kloc_1c287: 	goto loc_1c287;
        case m2c::kloc_1c2a0: 	goto loc_1c2a0;
        case m2c::kloc_1c2b6: 	goto loc_1c2b6;
        case m2c::kloc_1c352: 	goto loc_1c352;
        case m2c::kloc_1c39b: 	goto loc_1c39b;
        case m2c::kloc_1c3af: 	goto loc_1c3af;
        case m2c::kloc_1c3ba: 	goto loc_1c3ba;
        case m2c::kloc_1c3e1: 	goto loc_1c3e1;
        case m2c::kloc_1c3f5: 	goto loc_1c3f5;
        case m2c::kloc_1c400: 	goto loc_1c400;
        case m2c::kloc_1c427: 	goto loc_1c427;
        case m2c::kloc_1c43b: 	goto loc_1c43b;
        case m2c::kloc_1c446: 	goto loc_1c446;
        case m2c::kloc_1c49a: 	goto loc_1c49a;
        case m2c::kloc_1c4db: 	goto loc_1c4db;
        case m2c::kloc_1c4fd: 	goto loc_1c4fd;
        case m2c::kloc_1c50b: 	goto loc_1c50b;
        case m2c::kloc_1c517: 	goto loc_1c517;
        case m2c::kloc_1c52c: 	goto loc_1c52c;
        case m2c::kloc_1c546: 	goto loc_1c546;
        case m2c::kloc_1c56d: 	goto loc_1c56d;
        case m2c::kloc_1c5b5: 	goto loc_1c5b5;
        case m2c::kloc_1c5e3: 	goto loc_1c5e3;
        case m2c::kloc_1c62c: 	goto loc_1c62c;
        case m2c::kloc_1c68b: 	goto loc_1c68b;
        case m2c::kloc_1c6c4: 	goto loc_1c6c4;
        case m2c::kloc_1c6fc: 	goto loc_1c6fc;
        case m2c::klocret_1bed9: 	goto locret_1bed9;
        case m2c::klocret_1bf1a: 	goto locret_1bf1a;
        case m2c::klocret_1c702: 	goto locret_1c702;
        case m2c::kret_d4f_3bd: 	goto ret_d4f_3bd;
        case m2c::kret_d4f_3f4: 	goto ret_d4f_3f4;
        case m2c::kret_d4f_450: 	goto ret_d4f_450;
        case m2c::kret_d4f_529: 	goto ret_d4f_529;
        case m2c::kret_d4f_564: 	goto ret_d4f_564;
        case m2c::kret_d4f_56c: 	goto ret_d4f_56c;
        case m2c::kret_d4f_5b8: 	goto ret_d4f_5b8;
        case m2c::kret_d4f_610: 	goto ret_d4f_610;
        case m2c::kret_d4f_686: 	goto ret_d4f_686;
        case m2c::kret_d4f_71b: 	goto ret_d4f_71b;
        case m2c::kret_d4f_75e: 	goto ret_d4f_75e;
        case m2c::kret_d4f_7c3: 	goto ret_d4f_7c3;
        case m2c::kret_d4f_8d8: 	goto ret_d4f_8d8;
        case m2c::kret_d4f_91d: 	goto ret_d4f_91d;
        case m2c::kret_d4f_964: 	goto ret_d4f_964;
        case m2c::kret_d4f_a17: 	goto ret_d4f_a17;
        case m2c::kret_d4f_a53: 	goto ret_d4f_a53;
        case m2c::kret_d4f_a67: 	goto ret_d4f_a67;
        case m2c::kret_d4f_af1: 	goto ret_d4f_af1;
        case m2c::kret_d4f_b48: 	goto ret_d4f_b48;
        case m2c::kret_d4f_b4b: 	goto ret_d4f_b4b;
        case m2c::kret_d4f_c02: 	goto ret_d4f_c02;
        case m2c::kret_d4f_c36: 	goto ret_d4f_c36;
        case m2c::kret_d4f_c39: 	goto ret_d4f_c39;
        case m2c::kret_d4f_c3f: 	goto ret_d4f_c3f;
        case m2c::kret_d4f_c45: 	goto ret_d4f_c45;
        case m2c::kret_d4f_c4b: 	goto ret_d4f_c4b;
        case m2c::kret_d4f_c51: 	goto ret_d4f_c51;
        case m2c::kret_d4f_c57: 	goto ret_d4f_c57;
        case m2c::kret_d4f_c5d: 	goto ret_d4f_c5d;
        case m2c::kret_d4f_c63: 	goto ret_d4f_c63;
        case m2c::kret_d4f_c69: 	goto ret_d4f_c69;
        case m2c::kret_d4f_c6f: 	goto ret_d4f_c6f;
        case m2c::kret_d4f_c75: 	goto ret_d4f_c75;
        case m2c::kret_d4f_c7b: 	goto ret_d4f_c7b;
        case m2c::kret_d4f_c81: 	goto ret_d4f_c81;
        case m2c::kret_d4f_c87: 	goto ret_d4f_c87;
        case m2c::kret_d4f_c8d: 	goto ret_d4f_c8d;
        case m2c::kret_d4f_c96: 	goto ret_d4f_c96;
        case m2c::kret_d4f_c9c: 	goto ret_d4f_c9c;
        case m2c::kret_d4f_ca2: 	goto ret_d4f_ca2;
        case m2c::kret_d4f_ca8: 	goto ret_d4f_ca8;
        case m2c::kret_d4f_cae: 	goto ret_d4f_cae;
        case m2c::kret_d4f_cb4: 	goto ret_d4f_cb4;
        case m2c::kret_d4f_cba: 	goto ret_d4f_cba;
        case m2c::kret_d4f_cbd: 	goto ret_d4f_cbd;
        case m2c::kret_d4f_cc3: 	goto ret_d4f_cc3;
        case m2c::kret_d4f_ccc: 	goto ret_d4f_ccc;
        case m2c::kret_d4f_cd2: 	goto ret_d4f_cd2;
        case m2c::kret_d4f_cd8: 	goto ret_d4f_cd8;
        case m2c::kret_d4f_cde: 	goto ret_d4f_cde;
        case m2c::kret_d4f_ce4: 	goto ret_d4f_ce4;
        case m2c::kret_d4f_ce7: 	goto ret_d4f_ce7;
        case m2c::kret_d4f_cf0: 	goto ret_d4f_cf0;
        case m2c::kret_d4f_cf6: 	goto ret_d4f_cf6;
        case m2c::kret_d4f_cf9: 	goto ret_d4f_cf9;
        case m2c::kret_d4f_cff: 	goto ret_d4f_cff;
        case m2c::kret_d4f_d05: 	goto ret_d4f_d05;
        case m2c::kret_d4f_d0b: 	goto ret_d4f_d0b;
        case m2c::kret_d4f_d11: 	goto ret_d4f_d11;
        case m2c::kret_d4f_d17: 	goto ret_d4f_d17;
        case m2c::kret_d4f_d1d: 	goto ret_d4f_d1d;
        case m2c::kret_d4f_d23: 	goto ret_d4f_d23;
        case m2c::kret_d4f_d29: 	goto ret_d4f_d29;
        case m2c::kret_d4f_d2f: 	goto ret_d4f_d2f;
        case m2c::kret_d4f_d35: 	goto ret_d4f_d35;
        case m2c::kret_d4f_d3b: 	goto ret_d4f_d3b;
        case m2c::kret_d4f_d41: 	goto ret_d4f_d41;
        case m2c::kret_d4f_d47: 	goto ret_d4f_d47;
        case m2c::kret_d4f_d4d: 	goto ret_d4f_d4d;
        case m2c::kseg002_44b_proc: 	goto seg002_44b_proc;
        case m2c::kseg002_55c_proc: 	goto seg002_55c_proc;
        case m2c::kseg002_5af_proc: 	goto seg002_5af_proc;
        case m2c::kseg002_5df_proc: 	goto seg002_5df_proc;
        case m2c::kseg002_607_proc: 	goto seg002_607_proc;
        case m2c::kseg002_712_proc: 	goto seg002_712_proc;
        case m2c::kseg002_756_proc: 	goto seg002_756_proc;
        case m2c::kseg002_7ba_proc: 	goto seg002_7ba_proc;
        case m2c::kseg002_885_proc: 	goto seg002_885_proc;
        case m2c::kseg002_8ce_proc: 	goto seg002_8ce_proc;
        case m2c::kseg002_8ed_proc: 	goto seg002_8ed_proc;
        case m2c::kseg002_914_proc: 	goto seg002_914_proc;
        case m2c::kseg002_963_proc: 	goto seg002_963_proc;
        case m2c::kseg002_9cd_proc: 	goto seg002_9cd_proc;
        case m2c::kseg002_a0e_proc: 	goto seg002_a0e_proc;
        case m2c::kseg002_ae8_proc: 	goto seg002_ae8_proc;
        case m2c::kseg002_bf7_proc: 	goto seg002_bf7_proc;
        case m2c::kseg002_c33_proc: 	goto seg002_c33_proc;
        case m2c::kseg002_cb7_proc: 	goto seg002_cb7_proc;
        case m2c::kseg002_cd5_proc: 	goto seg002_cd5_proc;
        case m2c::kseg002_ce1_proc: 	goto seg002_ce1_proc;
        case m2c::kseg002_cf3_proc: 	goto seg002_cf3_proc;
        case m2c::ksub_1be8a: 	goto sub_1be8a;
        case m2c::ksub_1bec2: 	goto sub_1bec2;
        case m2c::ksub_1bedc: 	goto sub_1bedc;
        case m2c::ksub_1bff8: 	goto sub_1bff8;
        case m2c::ksub_1c03b: 	goto sub_1c03b;
        case m2c::ksub_1c087: 	goto sub_1c087;
        case m2c::ksub_1c0b7: 	goto sub_1c0b7;
        case m2c::ksub_1c10a: 	goto sub_1c10a;
        case m2c::ksub_1c155: 	goto sub_1c155;
        case m2c::ksub_1c1ea: 	goto sub_1c1ea;
        case m2c::ksub_1c35e: 	goto sub_1c35e;
        case m2c::ksub_1c3a7: 	goto sub_1c3a7;
        case m2c::ksub_1c3c5: 	goto sub_1c3c5;
        case m2c::ksub_1c40b: 	goto sub_1c40b;
        case m2c::ksub_1c451: 	goto sub_1c451;
        case m2c::ksub_1c4a6: 	goto sub_1c4a6;
        case m2c::ksub_1c5ef: 	goto sub_1c5ef;
        case m2c::ksub_1c615: 	goto sub_1c615;
        case m2c::ksub_1c6d0: 	goto sub_1c6d0;
        case m2c::ksub_1c763: 	goto sub_1c763;
        case m2c::ksub_1c769: 	goto sub_1c769;
        case m2c::ksub_1c76f: 	goto sub_1c76f;
        case m2c::ksub_1c775: 	goto sub_1c775;
        case m2c::ksub_1c77b: 	goto sub_1c77b;
        case m2c::ksub_1c781: 	goto sub_1c781;
        case m2c::ksub_1c799: 	goto sub_1c799;
        case m2c::ksub_1c79f: 	goto sub_1c79f;
        case m2c::ksub_1c7ab: 	goto sub_1c7ab;
        case m2c::ksub_1c7bd: 	goto sub_1c7bd;
        default: m2c::log_error("Don't know how to jump to 0x%x. See " __FILE__ " line %d\n", __disp, __LINE__);return __dispatch_call(__disp,_state);//m2c::stackDump(); abort();
    };
}

