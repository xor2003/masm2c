
; ---------------------------------------------------------------------------

struc	struct_0 ; (sizeof=0xA)
.word_244B7:	resw	1
.anonymous_0:	resw	1
.anonymous_1:	resw	1
.anonymous_2:	resw	1
.anonymous_3:	resw	1			; offset (00019050)
endstruc	;		struct_0


;
; Input	MD5   :	3ADEF234086ACD44430B68CC52471B0D
; Input	CRC32 :	B294245C

; File Name   :	I:\IPLAY.EXE
; Format      :	MS-DOS executable (EXE)
; Base Address:	1000h Range: 10000h-35510h Loaded length: 16308h
; Entry	Point :	1905:42

		CPU	686
		pmmx

; ===========================================================================

; Segment type:	Pure code
SEGMENT	seg000	ALIGN=1	public	CLASS=CODE	use16

; =============== S U B	R O U T	I N E =======================================


moduleread:		; CODE XREF: read_module+56P
					; DATA XREF: seg003:off_245C8o	...
		push	ds
		push	dx
		push	cs
		call	near snd_offx

loc_10006:
		push	cs
		call	near memfree_125DA
		pop	dx
		mov	ax, 3D00h
		int	21h		; DOS -	2+ - OPEN DISK FILE WITH HANDLE
					; DS:DX	-> ASCIZ filename
					; AL = access mode
					; 0 - read
		mov	bx, seg003
		mov	ds, bx
		mov	[savesp_245D0],	sp
		mov	[fhandle_module], ax
		mov	dx, eModuleNotFound ; "Module not found\r\n"

loc_1001F:
		mov	ax, 0FFFFh
		jb	short lfreaderr
		call	ems_save_mapctx
		cld

loc_10028:
		mov	BYTE [byte_2461B], 0

loc_1002D:
		mov	WORD [word_24662], 0

loc_10033:
		mov	dx, chrin
		mov	cx, 1084
		call	dosfread
		push	cs

loc_1003D:
		call	near clean_11C43

loc_10040:
		mov	bx, off_25326
		mov	dl, 23

loc_10045:				; CODE XREF: moduleread+5Fj
		movzx	cx, byte [bx+4]

loc_10049:
		mov	di, chrin
		add	di, [bx+2]
		lea	si, [bx+5]

loc_10052:
		mov	ax, [bx]
		mov	bx, si
		add	bx, cx
		cld
		repe cmpsb
		jz	short loc_10064
		dec	dl
		jnz	short loc_10045
		mov	ax, mod_n_t_module ; N.T.

loc_10064:				; CODE XREF: moduleread+5Bj
		mov	BYTE [byte_24665], 1
		call	ax

loc_1006B:
		mov	bx, [fhandle_module]
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle
		adc	WORD [word_24662], 0
		call	ems_restore_mapctx

loc_1007B:
		movzx	ax, BYTE [byte_2461B]

loc_10080:
		inc	ax
		cmp	ax, [word_245D4]
		jbe	short loc_1008A
		mov	ax, [word_245D4]

loc_1008A:				; CODE XREF: moduleread+85j
		push	cs
		call	near sub_12B83
		mov	si, dword_27BC8
		push	cs

loc_10092:
		call	near sub_12B18
		xor	ax, ax
		pop	ds
		retf
; ---------------------------------------------------------------------------

loc_10099:				; CODE XREF: mod_n_t_module+6Dj
					; mod_n_t_module+15Cj ...
		mov	dx, aNotEnoughMemory ; "Not enough Memory available\r\n"
		mov	ax, 0FFFEh

lfreaderr:				; CODE XREF: moduleread+22j
					; dosseek+18j ...
		push	ax
		push	dx
		mov	bx, [fhandle_module]
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle
		call	ems_restore_mapctx
		push	cs
		call	near memfree_125DA
		mov	ax, ds
		mov	fs, ax
		pop	dx
		pop	ax
		mov	sp, [savesp_245D0]
		pop	ds
		stc
		retf


; =============== S U B	R O U T	I N E =======================================

; N.T.

mod_n_t_module:	; DATA XREF: moduleread+61o
		mov	DWORD [module_type_text], 2E542E4Eh
		mov	WORD [word_245D2], 0Fh
		mov	WORD [word_245D4], 4
		mov	si, byte_306DE
		call	mod_1021E
		call	mod_102F5
		mov	dx, 258h
		xor	cx, cx
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		adc	WORD [word_24662], 0
		jmp	loc_101B7
; ---------------------------------------------------------------------------

mod_flt8_module:			; DATA XREF: seg003:0DDAo
		mov	DWORD [module_type_text], 38544C46h ;	FLT8
		mov	WORD [moduleflag_246D0], 11b
		mov	WORD [word_245D2], 1Fh
		mov	WORD [word_245D4], 8
		mov	si, byte_308BE
		call	mod_1021E
		mov	si, byte_27FE8
		mov	cx, 80h	; 'Ä'

loc_10118:				; CODE XREF: mod_n_t_module+5Fj
		shr	byte [si], 1
		inc	si
		dec	cx
		jnz	short loc_10118
		call	mod_1024A
		call	mod_102F5
		call	mod_read_10311
		call	near mod_readfile_11F4E
		jb	loc_10099
		retn
; ---------------------------------------------------------------------------

mod_tdz_module:				; DATA XREF: seg003:0E04o
		mov	al, [byte_30943]
		jmp	short loc_10137
; ---------------------------------------------------------------------------

mod_chn_module:				; DATA XREF: seg003:0DF5o
		mov	al, [byte_30940]

loc_10137:				; CODE XREF: mod_n_t_module+75j
		xor	ah, ah
		inc	WORD [word_24662]
		sub	al, 30h	; '0'
		jbe	short locret_10154
		cmp	al, 9
		ja	short locret_10154
		dec	WORD [word_24662]
		mov	WORD [word_245D2], 1Fh
		mov	[word_245D4], ax

loc_10152:
		jmp	short loc_101A6
; ---------------------------------------------------------------------------

locret_10154:				; CODE XREF: mod_n_t_module+82j
					; mod_n_t_module+86j ...
		retn
; ---------------------------------------------------------------------------

mod_ch_module:				; DATA XREF: seg003:0DFDo
		inc	WORD [word_24662]
		movzx	ax, BYTE [byte_30940]
		sub	al, '0'
		jb	short locret_10154
		cmp	al, 9
		ja	short locret_10154
		imul	dx, ax,	10
		mov	al, byte [unk_30941]
		sub	al, '0'
		jb	short locret_10154
		cmp	al, 9
		ja	short locret_10154
		add	ax, dx
		jz	short locret_10154
		cmp	ax, ' '
		ja	short locret_10154
		dec	WORD [word_24662]
		mov	WORD [word_245D2], 1Fh
		mov	[word_245D4], ax
		jmp	short loc_101A6
; ---------------------------------------------------------------------------

mod_cd81_module:			; DATA XREF: seg003:0DE3o seg003:0DECo
		mov	WORD [word_245D2], 1Fh
		mov	WORD [word_245D4], 8
		jmp	short loc_101A6
; ---------------------------------------------------------------------------

mod_mk_module:				; DATA XREF: seg003:0D9Bo seg003:0DA4o ...
		mov	WORD [word_245D2], 1Fh
		mov	WORD [word_245D4], 4

loc_101A6:				; CODE XREF: mod_n_t_module:loc_10152j
					; mod_n_t_module+CDj ...
		mov	eax, dword	[byte_30940]
		mov	[module_type_text], eax
		mov	si, byte_308BE
		call	mod_1021E
		call	mod_102F5

loc_101B7:				; CODE XREF: mod_n_t_module+31j
		call	mod_1024A
		cmp	DWORD [module_type_text], 2E4B2E4Dh ;	M.K.
		jnz	short loc_10213
		xor	dx, dx
		xor	cx, cx
		mov	bx, [fhandle_module]
		mov	ax, 4202h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from end of file
		shl	edx, 10h
		mov	dx, ax
		push	edx
		mov	dx, 1084
		xor	cx, cx
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		pop	edx
		movzx	eax, WORD [word_245F2]
		shl	eax, 0Bh

loc_101F4:
		add	eax, [dword_245C4]
		add	eax, 1084
		cmp	eax, edx
		jnz	short loc_10213
		mov	WORD [word_245D4], 8
		mov	DWORD [module_type_text], 20574F57h ;	WOW

loc_10213:				; CODE XREF: mod_n_t_module+106j
					; mod_n_t_module+145j
		call	mod_read_10311
		call	near mod_readfile_11F4E
		jb	loc_10099
		retn


; =============== S U B	R O U T	I N E =======================================


mod_1021E:		; CODE XREF: mod_n_t_module+18p
					; mod_n_t_module+52p ...
		mov	ax, ds
		mov	es, ax
		cld
		lodsb
		xor	ah, ah
		mov	[word_245FA], ax
		lodsb
		cmp	al, 78h	; 'x'
		jb	short loc_10230
		xor	al, al

loc_10230:				; CODE XREF: mod_1021E+Ej
		mov	[word_245F8], ax
		mov	di, byte_27FE8
		mov	cx, 20h	; ' '
		cld
		rep movsd
		mov	si, chrin ; in
		mov	di, asc_246B0 ; out
		mov	cx, 14h		; count
		call	copy_printable
		retn


; =============== S U B	R O U T	I N E =======================================


mod_1024A:		; CODE XREF: mod_n_t_module+61p
					; mod_n_t_module:loc_101B7p
		mov	si, chrin
		mov	di, myout ; out
		mov	cx, [word_245D2]

loc_10254:				; CODE XREF: mod_1024A+A6j
		push	cx
		add	si, 20		; in
		mov	cx, 16h		; count
		call	copy_printable
		sub	si, 20
		pop	cx
		movzx	edx, word [si+2Ah]
		xchg	dl, dh
		shl	edx, 1
		cmp	edx, 100000h
		cmc
		adc	WORD [word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	al, [si+2Ch]
		and	al, 0Fh
		mov	[di+3Eh], al
		mov	ax, [freq_245DE]
		mov	[di+36h], ax
		mov	al, [si+2Dh]
		mov	[di+3Dh], al
		movzx	ebx, word [si+2Eh]
		xchg	bl, bh
		shl	ebx, 1
		movzx	eax, word [si+30h]
		xchg	al, ah
		shl	eax, 1
		mov	[di+28h], eax
		cmp	eax, 2
		jbe	short loc_102DC
		cmp	ebx, edx
		jb	short loc_102C1
		shr	ebx, 1
		cmp	ebx, edx
		jnb	short loc_102DC

loc_102C1:				; CODE XREF: mod_1024A+6Dj
		or	byte [di+3Ch], 8
		add	eax, ebx
		cmp	eax, edx
		jbe	short loc_102DF
		mov	eax, [di+28h]
		shr	eax, 1
		add	eax, ebx
		cmp	eax, edx
		jbe	short loc_102DF

loc_102DC:				; CODE XREF: mod_1024A+68j
					; mod_1024A+75j
		mov	eax, edx

loc_102DF:				; CODE XREF: mod_1024A+81j
					; mod_1024A+90j
		dec	eax
		mov	[di+2Ch], eax
		mov	[di+24h], ebx
		add	si, 1Eh
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_10254
		retn


; =============== S U B	R O U T	I N E =======================================


mod_102F5:		; CODE XREF: mod_n_t_module+1Bp
					; mod_n_t_module+64p ...
		mov	si, byte_27FE8
		xor	bx, bx
		mov	cx, 80h	; 'Ä'
		cld

loc_102FE:				; CODE XREF: mod_102F5+13j
		lodsb
		and	al, 7Fh
		cmp	al, bl
		jb	short loc_10307
		mov	bl, al

loc_10307:				; CODE XREF: mod_102F5+Ej
		dec	cx
		jnz	short loc_102FE
		inc	bl
		mov	[word_245F2], bx
		retn


; =============== S U B	R O U T	I N E =======================================


mod_read_10311:	; CODE XREF: mod_n_t_module+67p
					; mod_n_t_module:loc_10213p
		mov	cx, [word_245F2]

loc_10315:				; CODE XREF: mod_read_10311+D5j
		push	cx
		mov	dx, word_31508
		mov	cx, [word_245D4]
		shl	cx, 8
		call	dosfread
		test	WORD [moduleflag_246D0], 10b
		jz	short loc_1035C
		mov	ax, ds
		mov	es, ax
		mov	si, word_31508
		mov	di, byte_31D08
		mov	cx, 200h
		cld
		rep movsd
		mov	si, byte_31D08
		mov	di, word_31508
		mov	bx, 40h	; '@'

loc_10345:				; CODE XREF: mod_read_10311+49j
		mov	cx, 4
		rep movsd
		add	si, 3F0h
		mov	cx, 4
		rep movsd
		sub	si, 400h
		dec	bx
		jnz	short loc_10345

loc_1035C:				; CODE XREF: mod_read_10311+18j
		call	memalloc12k
		mov	si, word_31508
		mov	cx, 40h	; '@'

loc_10365:				; CODE XREF: mod_read_10311+CEj
		push	cx
		mov	cx, [word_245D4]
		xor	ch, ch

loc_1036C:				; CODE XREF: mod_read_10311+C5j
		push	cx
		mov	eax, [si]
		add	si, 4
		mov	edx, eax
		xchg	al, ah
		xor	bl, bl
		and	ax, 0FFFh
		jz	short loc_103B9
		mov	bx, 72
		cmp	ax, 214
		jbe	short loc_10399
		mov	bx, 48
		cmp	ax, 428
		jbe	short loc_10399
		mov	bx, 24
		cmp	ax, 856
		jbe	short loc_10399
		xor	bx, bx

loc_10399:				; CODE XREF: mod_read_10311+74j
					; mod_read_10311+7Cj ...
		cmp	ax, [table_25118+bx]
		jnb	short loc_103A8
		add	bx, 2
		cmp	bx, 166
		jb	short loc_10399

loc_103A8:				; CODE XREF: mod_read_10311+8Cj
		mov	ax, bx
		shr	ax, 1
		mov	bl, 12
		div	bl
		inc	ah
		shl	al, 4
		or	al, ah
		mov	bl, al

loc_103B9:				; CODE XREF: mod_read_10311+6Cj
		mov	bh, dl
		and	bh, 30h
		rol	edx, 10h
		mov	al, dl
		shr	al, 4
		or	bh, al
		and	dl, 0Fh
		mov	cl, 0FFh
		call	sub_11BA6
		pop	cx
		inc	ch
		cmp	ch, cl
		jb	short loc_1036C
		mov	byte [es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	short loc_10365
		call	mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_10315
		retn


; =============== S U B	R O U T	I N E =======================================

; 2STM

_2stm_module:	; DATA XREF: seg003:0E19o
		mov	DWORD [module_type_text], 4D545332h
		jmp	short loc_103FF
; ---------------------------------------------------------------------------

stm_module:				; DATA XREF: seg003:0E0Co
		mov	DWORD [module_type_text], 204D5453h ;	STM

loc_103FF:				; CODE XREF: _2stm_module+9j
		mov	WORD [moduleflag_246D0], 1000b
		mov	WORD [word_245D4], 4
		mov	WORD [word_245D2], 1Fh
		mov	WORD [freq_245DE], 8448
		mov	al, 60h	; '`'
		call	sub_13E9B
		mov	[byte_24679], ah
		mov	[byte_2467A], al
		movzx	ax, BYTE [byte_30529]
		mov	[word_245F2], ax
		mov	ax, ds
		mov	es, ax
		mov	si, chrin ; in
		mov	di, asc_246B0 ; "				"
		mov	cx, 14h		; count
		call	copy_printable
		mov	si, my_in ; in
		mov	di, myout ; out
		mov	cx, [word_245D2]

loc_10445:				; CODE XREF: _2stm_module+E3j
		push	cx
		mov	cx, 0Ch		; count
		call	copy_printable
		pop	cx

loc_1044D:
		movzx	eax, word [si+10h]
		mov	edx, eax
		add	eax, 0Fh
		and	al, 0F0h
		cmp	eax, 100000h
		cmc
		adc	WORD [word_24662], 0

loc_10467:
		mov	[di+20h], eax
		add	[dword_245C4], eax
		movzx	eax, word [si+0Eh]
		shl	eax, 4
		mov	[di+38h], eax
		mov	ax, [si+18h]
		or	ax, ax
		jnz	short loc_10487
		mov	ax, [freq_245DE]

loc_10487:				; CODE XREF: _2stm_module+97j
		mov	[di+36h], ax
		mov	al, [si+16h]
		mov	[di+3Dh], al
		movzx	ebx, word [si+12h]
		mov	[di+24h], ebx
		movzx	eax, word [si+14h]
		cmp	ax, 0FFFFh
		jnz	short loc_104B6
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_104C7
; ---------------------------------------------------------------------------

loc_104B6:				; CODE XREF: _2stm_module+B6j
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	byte [di+3Ch], 8

loc_104C7:				; CODE XREF: _2stm_module+C9j
		add	si, 20h	; ' '
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_10445
		mov	dx, byte_27FE8
		mov	cx, 80h	; 'Ä'
		mov	eax, 410h
		call	dosseek
		mov	si, byte_27FE8
		xor	ax, ax

loc_104E6:				; CODE XREF: _2stm_module+105j
		cmp	byte [si], 63h ; 'c'
		jnb	short loc_104F2
		inc	ax
		inc	si
		cmp	ax, 80h	; 'Ä'
		jb	short loc_104E6

loc_104F2:				; CODE XREF: _2stm_module+FEj
		mov	[word_245FA], ax
		mov	cx, [word_245F2]

loc_104F9:				; CODE XREF: _2stm_module+195j
		push	cx
		mov	dx, chrin
		mov	cx, 400h
		call	dosfread
		call	memalloc12k
		mov	si, chrin
		mov	cx, 40h	; '@'

loc_1050C:				; CODE XREF: _2stm_module+18Ej
		push	cx
		mov	cx, [word_245D4]
		xor	ch, ch

loc_10513:				; CODE XREF: _2stm_module+185j
		push	cx
		xor	bx, bx
		xor	dx, dx
		xor	cl, cl
		mov	al, [si]
		cmp	al, 0FEh ; '˛'
		jz	short loc_10565
		mov	cl, 0FFh
		cmp	al, 0FFh
		jz	short loc_1052E
		cmp	al, 0FBh ; '˚'
		jnb	short loc_10565
		inc	al
		mov	bl, al

loc_1052E:				; CODE XREF: _2stm_module+139j
		mov	bh, [si+1]
		shr	bh, 3
		mov	ax, [si+1]
		and	ax, 0F007h
		shr	ah, 1
		or	al, ah
		cmp	al, 40h	; '@'
		jbe	short loc_10544
		mov	al, 0FFh

loc_10544:				; CODE XREF: _2stm_module+155j
		mov	cl, al
		mov	ax, [si+2]
		and	al, 0Fh
		jz	short loc_10565
		cmp	al, 0Ah
		ja	short loc_10565
		mov	dh, ah
		rol	ebx, 10h
		mov	bl, al
		and	bx, 0Fh
		mov	dl, byte [cs:asc_1058C+bx] ; "\x18\v\r\n\x02\x01\x03\x04\a"
		ror	ebx, 10h

loc_10565:				; CODE XREF: _2stm_module+133j
					; _2stm_module+13Dj ...
		call	sub_11BA6
		add	si, 4
		pop	cx
		inc	ch
		cmp	ch, cl
		jb	short loc_10513
		mov	byte [es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	short loc_1050C
		call	mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_104F9
		call	near mod_readfile_11F4E
		jb	loc_10099
		retn

; ---------------------------------------------------------------------------
asc_1058C	db 0,18h,0Bh,0Dh,0Ah	; DATA XREF: _2stm_module+171r
		db 2,1,3,4,7,0

; =============== S U B	R O U T	I N E =======================================

; S3M

s3m_module:		; DATA XREF: seg003:0E26o
		mov	DWORD [module_type_text], 204D3353h
		mov	WORD [moduleflag_246D0], 10000b
		mov	BYTE [byte_2467E], 1
		mov	BYTE [byte_24673], 80h ; 'Ä'
		mov	WORD [freq_245DE], 8363
		mov	BYTE [byte_2461A], 2
		cmp	WORD [word_30532], 2
		jnb	short loc_105C7
		mov	BYTE [byte_24673], 0

loc_105C7:				; CODE XREF: s3m_module+29j
		mov	ax, ds
		mov	es, ax
		mov	si, chrin ; in
		mov	di, asc_246B0 ; "				"
		mov	cx, 1Ch		; count
		call	copy_printable
		test	byte [config_word+1], 20h
		jz	short loc_1061E
		mov	dx, 64h	; 'd'
		mov	cl, [byte_3053B]
		and	cx, 7Fh
		jz	short loc_10618
		test	BYTE [byte_3053B], 80h
		jz	short loc_105FF
		mov	ax, 0Bh
		mul	cx
		shrd	ax, dx,	3
		sub	ax, 2
		mov	cx, ax

loc_105FF:				; CODE XREF: s3m_module+58j
		mov	ax, 100
		mul	cx
		mov	cx, '0'
		div	cx
		mov	dx, 100
		cmp	ax, 100
		jbe	short loc_10618
		cmp	ax, 2500
		ja	short loc_10618
		mov	dx, ax

loc_10618:				; CODE XREF: s3m_module+51j
					; s3m_module+78j ...
		mov	ax, dx
		push	cs
		call	near change_amplif

loc_1061E:				; CODE XREF: s3m_module+45j
		xor	si, si
		mov	di, volume_25908
		xor	dx, dx
		mov	cx, 20h	; ' '

loc_10628:				; CODE XREF: s3m_module+AEj
		mov	al, [byte_30548+si]
		cmp	al, 0FFh
		jz	short loc_10640
		mov	dx, si
		shr	al, 4
		mov	ah, 1
		cmp	al, 1
		jz	short loc_1063D
		mov	ah, 0

loc_1063D:				; CODE XREF: s3m_module+A2j
		mov	[di+1Dh], ah

loc_10640:				; CODE XREF: s3m_module+97j
		inc	si
		add	di, 50h	; 'P'
		dec	cx
		jnz	short loc_10628
		inc	dx
		mov	[word_245D4], dx
		mov	cx, [word_245D4]
		xor	si, si

loc_10652:				; CODE XREF: s3m_module+CEj
		mov	al, [byte_2461E]
		test	BYTE [byte_30548+si], 8
		jz	short loc_1065F
		mov	al, [byte_2461F]

loc_1065F:				; CODE XREF: s3m_module+C3j
		mov	byte [dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_10652
		mov	ax, [word_3052A]
		cmp	ax, 63h	; 'c'
		jb	short loc_10672
		mov	ax, 63h	; 'c'

loc_10672:				; CODE XREF: s3m_module+D6j
		mov	[word_245D2], ax
		mov	ax, [word_3052C]
		cmp	ax, 100h
		jb	short loc_10680
		mov	ax, 100h

loc_10680:				; CODE XREF: s3m_module+E4j
		mov	[word_245F2], ax
		mov	al, [byte_30539]
		mov	[byte_24679], al
		mov	al, [byte_3053A]
		mov	[byte_2467A], al
		mov	ax, ds
		mov	es, ax
		mov	di, myout ; out
		mov	bx, (dword_30566+2)
		add	bx, word [unk_30528]
		movzx	ecx, WORD [word_245D2]

loc_106A3:				; CODE XREF: s3m_module+1CAj
		push	bx
		push	cx
		mov	dx, word_31508
		mov	cx, 50h	; 'P'
		movzx	eax, word [bx]
		shl	eax, 4
		call	dosseek
		mov	si, word_31508
		xor	eax, eax
		xor	edx, edx
		cmp	byte [si], 1
		jnz	short loc_106D8
		movzx	eax, word [si+10h]
		mov	edx, eax
		cmp	eax, 100000h
		cmc
		adc	WORD [word_24662], 0

loc_106D8:				; CODE XREF: s3m_module+12Bj
		mov	[di+20h], eax
		add	[dword_245C4], eax
		movzx	eax, word [si+0Eh]
		shl	eax, 4
		mov	[di+38h], eax
		mov	ax, [si+20h]
		or	ax, ax
		jnz	short loc_106F8
		mov	ax, [freq_245DE]

loc_106F8:				; CODE XREF: s3m_module+15Cj
		mov	[di+36h], ax
		mov	al, [si+1Ch]
		cmp	al, 3Fh	; '?'
		jb	short loc_10704
		mov	al, 3Fh	; '?'

loc_10704:				; CODE XREF: s3m_module+169j
		mov	[di+3Dh], al
		test	byte [si+1Fh], 1
		jnz	short loc_10720

loc_1070D:				; CODE XREF: s3m_module+18Dj
					; s3m_module+1A0j ...
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_1074F
; ---------------------------------------------------------------------------

loc_10720:				; CODE XREF: s3m_module+174j
		cmp	word [si+14h], 0FFFFh
		jz	short loc_1070D
		movzx	edx, word [si+14h]
		mov	[di+24h], edx
		movzx	eax, word [si+18h]
		or	eax, eax
		jz	short loc_1070D
		dec	eax
		jz	short loc_1070D
		mov	[di+2Ch], eax
		inc	eax
		sub	eax, [di+24h]
		mov	[di+28h], eax
		or	byte [di+3Ch], 8

loc_1074F:				; CODE XREF: s3m_module+187j
		add	si, 30h	; '0'   ; in
		mov	cx, 1Ch		; count
		call	copy_printable
		pop	cx
		pop	bx
		add	di, 40h	; '@'
		add	bx, 2
		dec	cx
		jnz	loc_106A3
		mov	si, (dword_30566+2)
		xor	di, di
		xor	bx, bx
		mov	ax, word [unk_30528]
		cmp	ax, 80h	; 'Ä'
		mov	ah, al
		ja	short loc_1079A
		xor	cl, cl

loc_10778:				; CODE XREF: s3m_module+1FFj
		mov	al, [si]
		cmp	al, 0F0h ; ''
		jnb	short loc_1078F
		mov	BYTE [byte_27FE8+di], al
		inc	bl
		inc	di
		cmp	cl, 0F0h ; ''
		jb	short loc_1078F
		mov	BYTE [byte_280E7+di], 0FFh

loc_1078F:				; CODE XREF: s3m_module+1E5j
					; s3m_module+1F1j
		mov	cl, al
		inc	si
		inc	bh
		cmp	bh, ah
		jb	short loc_10778
		jmp	short loc_107AC
; ---------------------------------------------------------------------------

loc_1079A:				; CODE XREF: s3m_module+1DDj
					; s3m_module+213j
		mov	al, [si]
		cmp	al, 0FFh
		jz	short loc_107AC
		mov	BYTE [byte_27FE8+di], al
		inc	bl
		inc	di
		inc	si
		cmp	bl, ah
		jb	short loc_1079A

loc_107AC:				; CODE XREF: s3m_module+201j
					; s3m_module+207j
		xor	bh, bh
		mov	[word_245FA], bx
		xor	ax, ax

loc_107B4:				; CODE XREF: s3m_module+323j
		push	ax
		mov	bx, (dword_30566+2)
		add	bx, word [unk_30528]
		add	ax, [word_3052A]
		shl	ax, 1
		add	bx, ax
		mov	dx, word_31508
		mov	cx, 2
		movzx	eax, word [bx]
		or	ax, ax
		jnz	short loc_107E0

loc_107D2:				; CODE XREF: s3m_module+25Bj
		call	memalloc12k
		mov	cx, 40h	; '@'
		xor	al, al
		cld
		rep stosb
		jmp	loc_108B1
; ---------------------------------------------------------------------------

loc_107E0:				; CODE XREF: s3m_module+239j
		shl	eax, 4
		call	dosseek
		mov	dx, word_31508
		mov	cx, [word_31508]
		cmp	cx, 308Fh
		jnb	short loc_107D2
		add	cx, 0Fh
		and	cl, 0F0h
		sub	cx, 2
		call	dosfread
		call	memalloc12k
		mov	si, word_31508
		mov	cx, 40h	; '@'

loc_10809:				; CODE XREF: s3m_module+316j
		push	cx
		lodsb
		or	al, al
		jz	loc_108A6

loc_10811:				; CODE XREF: s3m_module+30Bj
		xor	bx, bx
		mov	ch, al
		test	ch, 20h
		jz	short loc_1082D
		mov	bx, [si]
		add	si, 2
		cmp	bl, 0FEh ; '˛'
		jnb	short loc_10826
		inc	bl

loc_10826:				; CODE XREF: s3m_module+28Bj
		cmp	bh, 63h	; 'c'
		jbe	short loc_1082D
		xor	bh, bh

loc_1082D:				; CODE XREF: s3m_module+281j
					; s3m_module+292j
		mov	cl, 0FFh
		test	ch, 40h
		jz	short loc_1083E
		mov	cl, [si]
		inc	si
		cmp	cl, 40h	; '@'
		jbe	short loc_1083E
		mov	cl, 0FFh

loc_1083E:				; CODE XREF: s3m_module+29Bj
					; s3m_module+2A3j
		test	ch, 80h
		jz	short loc_1088D
		mov	dx, [si]
		add	si, 2
		cmp	dl, 19h
		ja	short loc_1088D
		rol	ebx, 10h
		movzx	bx, dl
		mov	dl, [cs:s3mtable_108D6+bx]
		cmp	dl, 0FFh
		jz	short loc_10885
		cmp	dl, 0Fh
		jz	short loc_10880
		cmp	dl, 0Eh
		jnz	short loc_10887
		mov	bl, dh
		shr	bl, 4
		mov	al, [cs:s3mtable_108F0+bx]
		cmp	al, 0FFh
		jz	short loc_10885
		shl	al, 4
		and	dh, 0Fh
		or	dh, al
		jmp	short loc_10887
; ---------------------------------------------------------------------------

loc_10880:				; CODE XREF: s3m_module+2CAj
		cmp	dh, 20h	; ' '
		ja	short loc_10887

loc_10885:				; CODE XREF: s3m_module+2C5j
					; s3m_module+2DDj
		xor	dx, dx

loc_10887:				; CODE XREF: s3m_module+2CFj
					; s3m_module+2E7j ...
		ror	ebx, 10h
		jmp	short loc_1088F
; ---------------------------------------------------------------------------

loc_1088D:				; CODE XREF: s3m_module+2AAj
					; s3m_module+2B4j
		xor	dx, dx

loc_1088F:				; CODE XREF: s3m_module+2F4j
		and	ch, 1Fh
		cmp	byte [word_245D4+1], ch
		jnb	short loc_1089C
		mov	byte [word_245D4+1], ch

loc_1089C:				; CODE XREF: s3m_module+2FFj
		call	sub_11BA6
		lodsb
		or	al, al
		jnz	loc_10811

loc_108A6:				; CODE XREF: s3m_module+276j
		mov	byte [es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	loc_10809

loc_108B1:				; CODE XREF: s3m_module+246j
		call	mem_reallocx
		pop	ax
		inc	ax
		cmp	ax, [word_245F2]
		jb	loc_107B4
		mov	ax, [word_245D4]
		inc	ah
		cmp	al, ah
		jb	short loc_108C9
		mov	al, ah

loc_108C9:				; CODE XREF: s3m_module+32Ej
		xor	ah, ah
		mov	[word_245D4], ax
		call	near mod_readfile_11F4E
		jb	loc_10099
		retn

; ---------------------------------------------------------------------------
s3mtable_108D6	db 0FFh,10h,0Bh,0Dh,15h,12h,11h,13h,14h,1Bh,1Dh,17h,16h
					; DATA XREF: s3m_module+2BDr
		db 0FFh,0FFh,9,0FFh,1Ch,7,0Eh,0Fh,0FFh,0FFh,0FFh,8,0FFh
s3mtable_108F0	db 0,3,5,4,7,0FFh,0FFh,0FFh,8,0FFh,0FFh,6,0Ch,0Dh,0FFh
					; DATA XREF: s3m_module+2D6r
		db 0FFh

; =============== S U B	R O U T	I N E =======================================

; E669

e669_module:	; DATA XREF: seg003:0E61o
		mov	DWORD [module_type_text], 39363645h
		jmp	short loc_10914
; ---------------------------------------------------------------------------

_669_module:				; DATA XREF: seg003:0E5Ao
		mov	DWORD [module_type_text], 20393636h ;	669

loc_10914:				; CODE XREF: e669_module+9j
		mov	WORD [moduleflag_246D0], 100b
		mov	BYTE [byte_24673], 80h ; 'Ä'
		mov	BYTE [byte_2467E], 2
		mov	WORD [word_245D4], 8
		movzx	ax, BYTE [byte_30576]
		mov	[word_245D2], ax
		mov	al, [byte_30577]
		mov	[word_245F2], ax
		mov	ah, [byte_2461F]
		mov	al, [byte_2461E]
		shl	eax, 10h
		mov	ah, [byte_2461F]
		mov	al, [byte_2461E]
		mov	[dword_27BC8], eax
		mov	[dword_27BCC], eax
		mov	ax, ds
		mov	es, ax
		mov	si, (chrin+1)
		mov	cx, 4Ch	; 'L'

loc_1095C:				; CODE XREF: e669_module+60j
		inc	si		; in
		cmp	byte [si], 20h ; ' '
		loope	loc_1095C
		mov	di, asc_246B0 ; "				"
		mov	cx, 20h	; ' '   ; count
		call	copy_printable
		xor	si, si
		xor	bh, bh

loc_1096F:				; CODE XREF: e669_module+91j
		mov	bl, [byte_30579+si]
		cmp	bl, 0FFh
		jz	short loc_10993
		mov	BYTE [byte_27FE8+si], bl
		mov	al, [byte_305F9+bx]
		mov	BYTE [byte_280E8+si], al
		mov	al, [byte_30679+bx]
		mov	BYTE [byte_281E8+si], al
		inc	si
		cmp	si, 80h	; 'Ä'
		jb	short loc_1096F

loc_10993:				; CODE XREF: e669_module+76j
		mov	[word_245FA], si
		mov	al, [byte_280E8]
		mov	[byte_24679], al
		mov	BYTE [byte_2467A], 50h ; 'P'
		mov	dx, chrin
		imul	cx, [word_245D2], 25
		mov	eax, 497
		call	dosseek
		mov	si, chrin ; in
		mov	di, myout ; out
		mov	cx, [word_245D2]

loc_109BD:				; CODE XREF: e669_module+127j
		push	cx
		mov	cx, 0Dh		; count
		call	copy_printable
		pop	cx
		mov	edx, [si+0Dh]
		cmp	edx, 100000h
		cmc
		adc	WORD [word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	byte [di+3Dh], 3Fh ; '?'
		mov	word [di+36h], 2100h
		mov	ebx, [si+11h]
		mov	[di+24h], ebx
		mov	eax, [si+15h]
		cmp	eax, 0FFFFFh
		jb	short loc_10A0F
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_10A20
; ---------------------------------------------------------------------------

loc_10A0F:				; CODE XREF: e669_module+FAj
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	byte [di+3Ch], 8

loc_10A20:				; CODE XREF: e669_module+10Dj
		add	si, 19h
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_109BD
		mov	cx, [word_245F2]

loc_10A2D:				; CODE XREF: e669_module+1C9j
		push	cx
		mov	dx, word_31508
		mov	cx, 600h
		call	dosfread
		call	memalloc12k
		mov	si, word_31508
		mov	cx, 40h	; '@'

loc_10A40:				; CODE XREF: e669_module+1C0j
		push	cx
		mov	cx, [word_245D4]
		xor	ch, ch

loc_10A47:				; CODE XREF: e669_module+1B7j
		push	cx
		mov	al, [si]
		xor	bx, bx
		mov	cl, 0FFh
		cmp	al, 0FFh
		jz	short loc_10A83
		cmp	al, 0FEh ; '˛'
		jz	short loc_10A75
		shr	al, 2
		xor	ah, ah
		mov	dl, 0Ch
		div	dl
		inc	ah
		shl	al, 4
		or	al, ah
		mov	bl, al
		mov	ax, [si]
		xchg	al, ah
		shr	ax, 4
		and	al, 3Fh
		inc	al
		mov	bh, al

loc_10A75:				; CODE XREF: e669_module+154j
		mov	al, [si+1]
		and	al, 0Fh
		mov	ah, 44h	; 'D'
		mul	ah
		shr	ax, 4
		mov	cl, al

loc_10A83:				; CODE XREF: e669_module+150j
		mov	al, [si+2]
		mov	ah, al
		and	ah, 0Fh
		mov	dh, ah
		shr	al, 4
		cmp	al, 5
		ja	short loc_10AAA
		mov	dl, 0Fh
		jz	short loc_10AAC
		cmp	al, 4
		jz	short loc_10AAA
		cmp	al, 2
		jz	short loc_10AAA
		cmp	al, 3
		jnz	short loc_10AAA
		mov	dl, 1
		mov	dh, ah
		jmp	short loc_10AAC
; ---------------------------------------------------------------------------

loc_10AAA:				; CODE XREF: e669_module+192j
					; e669_module+19Aj ...
		xor	dx, dx

loc_10AAC:				; CODE XREF: e669_module+196j
					; e669_module+1A8j
		call	sub_11BA6
		add	si, 3
		pop	cx
		inc	ch
		cmp	ch, cl
		jb	short loc_10A47
		mov	byte [es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	loc_10A40
		call	mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_10A2D
		call	near mod_readfile_11F4E
		jb	loc_10099
		retn


; =============== S U B	R O U T	I N E =======================================

; MTM

mtm_module:		; DATA XREF: seg003:0E2Fo
		mov	DWORD [module_type_text], 204D544Dh
		mov	WORD [moduleflag_246D0], 100000b
		mov	BYTE [byte_24679], 6
		mov	BYTE [byte_2467A], 7Dh ; '}'
		mov	BYTE [byte_24673], 80h ; 'Ä'
		mov	ax, ds
		mov	es, ax
		mov	si, myin	; in
		mov	di, asc_246B0 ; "				"
		mov	cx, 14h		; count
		call	copy_printable
		cmp	BYTE [sndcard_type],	0
		jnz	short loc_10B25
		xor	si, si
		mov	cx, 10h

loc_10B0F:				; CODE XREF: mtm_module+4Ej
		mov	al, byte [word_3052A+si]
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:byte_13C54+di]
		mov	byte [dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_10B0F

loc_10B25:				; CODE XREF: mtm_module+33j
		movzx	ax, BYTE [byte_30526]
		mov	[word_245D2], ax
		mov	al, [byte_30522]
		inc	al
		mov	[word_245F2], ax
		movzx	ax, BYTE [byte_30523]
		inc	ax
		mov	[word_245FA], ax
		mov	dx, chrin
		imul	cx, [word_245D2], 25h
		add	cx, 0C2h ; '¬'
		xor	eax, eax
		call	dosseek
		mov	si, unk_3054A
		mov	di, myout
		mov	cx, [word_245D2]

; START	OF FUNCTION CHUNK FOR snd_off

loc_10B5A:				; CODE XREF: snd_off-3660j
		push	cx
		mov	cx, 16h		; count
		call	copy_printable
		pop	cx
		mov	edx, [si+16h]

loc_10B66:				; CODE XREF: snd_off+1Ej
		cmp	edx, 100000h
		cmc
		adc	WORD [word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	al, [si+23h]
		mov	[di+3Dh], al
		mov	al, [si+22h]
		and	al, 0Fh
		mov	[di+3Eh], al
		mov	ax, [freq_245DE]
		mov	[di+36h], ax
		mov	ebx, [si+1Ah]
		mov	[di+24h], ebx
		mov	eax, [si+1Eh]
		cmp	eax, 2
		ja	short loc_10BB5
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_10BC6
; ---------------------------------------------------------------------------

loc_10BB5:				; CODE XREF: snd_off-368Dj
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	byte [di+3Ch], 8

loc_10BC6:				; CODE XREF: snd_off-367Aj
		add	si, 25h	; '%'
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_10B5A
		mov	di, byte_27FE8
		mov	cx, 20h	; ' '
		cld
		rep movsd
		imul	ax, [word_245D2], 37
		add	ax, 0C2h ; '¬'
		movzx	eax, ax
		mov	[chrin], eax
		movzx	eax, WORD [word_30520]
		imul	eax, 192	; CODE XREF: snd_deinit+16j
		add	eax, [chrin]
		mov	dx, byte_33508
		mov	cx, [word_245F2]
		shl	cx, 6
		call	dosseek
		mov	si, byte_33508
		mov	cx, [word_245F2]
		mov	ax, 4

loc_10C12:				; CODE XREF: snd_off-3603j
		mov	bp, 1

loc_10C15:				; CODE XREF: snd_off-3606j
		cmp	word [si], 0
		jz	short loc_10C20
		cmp	bp, ax
		jb	short loc_10C20
		mov	ax, bp

loc_10C20:				; CODE XREF: snd_off-3615j
					; snd_off-3611j
		add	si, 2
		inc	bp
		cmp	bp, 20h	; ' '
		jbe	short loc_10C15
		dec	cx
		jnz	short loc_10C12
		mov	[word_245D4], ax
		mov	bx, byte_33508
		mov	cx, [word_245F2]

loc_10C36:				; CODE XREF: snd_off-354Aj
		push	bx
		push	cx
		mov	si, word_31508
		mov	cx, [word_245D4]

loc_10C3F:				; CODE XREF: snd_off-35AFj
		push	bx
		push	cx
		push	si
		mov	ax, [bx]
		or	ax, ax
		jnz	short loc_10C5A
		mov	ax, ds
		mov	es, ax
		mov	di, si
		mov	cx, 48
		xor	eax, eax
		cld
		rep stosd
		jmp	short loc_10C73
; ---------------------------------------------------------------------------

loc_10C5A:				; CODE XREF: snd_off-35E7j
		dec	ax
		movzx	eax, ax
		imul	eax, 192
		add	eax, [chrin]
		mov	dx, si
		mov	cx, 192
		call	dosseek

loc_10C73:				; CODE XREF: snd_off-35D5j
		pop	si
		pop	cx
		pop	bx
		add	bx, 2
		add	si, 192
		dec	cx
		jnz	short loc_10C3F
		call	memalloc12k
		mov	si, word_31508
		mov	cx, 40h	; '@'

loc_10C89:				; CODE XREF: snd_off-3555j
		push	cx
		push	si
		mov	cx, [word_245D4]
		xor	ch, ch

loc_10C91:				; CODE XREF: snd_off-3562j
		push	cx

loc_10C92:
		xor	bx, bx
		mov	al, [si]
		shr	al, 2
		jz	short loc_10CAA
		xor	ah, ah
		mov	dl, 0Ch
		div	dl
		inc	ah
		shl	al, 4
		or	al, ah
		mov	bl, al

loc_10CAA:				; CODE XREF: snd_off-3594j
		mov	ax, [si]
		mov	dl, ah
		xchg	al, ah
		shr	ax, 4
		and	al, 3Fh
		mov	bh, al
		and	dl, 0Fh
		mov	dh, [si+2]
		mov	cl, 0FFh
		call	sub_11BA6
		add	si, 192
		pop	cx
		inc	ch
		cmp	ch, cl
		jb	short loc_10C91
		mov	byte [es:di], 0
		inc	di
		pop	si
		pop	cx
		add	si, 3
		dec	cx
		jnz	short loc_10C89
		call	mem_reallocx
		pop	cx
		pop	bx
		add	bx, 40h	; '@'
		dec	cx
		jnz	loc_10C36
		mov	ax, 192
		mul	WORD [word_30520]
		mov	cx, dx
		imul	dx, [word_245D2], 37
		add	dx, 0C2h ; '¬'
		add	dx, [word_30524]
		adc	cx, 0
		add	dx, ax
		adc	cx, 0
		mov	ax, [word_245F2]
		shl	ax, 6
		add	dx, ax
		adc	cx, 0
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		adc	WORD [word_24662], 0
		call	near mod_readfile_11F4E
		jb	loc_10099
		retn
; END OF FUNCTION CHUNK	FOR snd_off

; =============== S U B	R O U T	I N E =======================================

; PSM

psm_module:		; DATA XREF: seg003:0E37o
		mov	DWORD [module_type_text], 204D5350h
		mov	WORD [moduleflag_246D0], 1000000b
		mov	ax, [word_30556]
		mov	[word_245D4], ax
		mov	ax, [word_30554]
		mov	[word_245D2], ax
		mov	WORD [freq_245DE], 8448
		mov	al, [byte_3054B]
		mov	[byte_24679], al
		mov	al, [byte_3054C]
		mov	[byte_2467A], al
		movzx	ax, BYTE [byte_30550]
		mov	[word_245FA], ax
		mov	ax, [word_30552]
		mov	[word_245F2], ax
		mov	ax, ds
		mov	es, ax
		mov	si, myin	; in
		mov	di, asc_246B0 ; "				"
		mov	cx, 30		; count
		call	copy_printable
		mov	dx, byte_3059A
		mov	cx, [word_245D2]
		shl	cx, 6
		mov	eax, [dword_30566]
		call	dosseek
		mov	si, byte_3059A
		mov	di, myout ; out
		mov	cx, [word_245D2]

loc_10D8C:				; CODE XREF: psm_module+FAj
		push	cx
		push	si
		add	si, 0Dh		; in
		mov	cx, 16h		; count
		call	copy_printable
		pop	si
		pop	cx
		mov	edx, [si+30h]
		cmp	edx, 100000h
		cmc
		adc	WORD [word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	byte [di+3Fh], 1
		mov	eax, [si+25h]
		mov	[di+38h], eax
		mov	ax, [si+3Eh]
		jnz	short loc_10DC7
		mov	ax, [freq_245DE]

loc_10DC7:				; CODE XREF: psm_module+9Cj
		mov	[di+36h], ax
		mov	al, [si+3Dh]
		mov	[di+3Dh], al
		mov	ebx, [si+34h]
		mov	[di+24h], ebx
		or	ebx, ebx
		jnz	short loc_10DF0
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_10E19
; ---------------------------------------------------------------------------

loc_10DF0:				; CODE XREF: psm_module+B5j
		mov	eax, [si+38h]
		mov	[di+28h], eax
		add	eax, ebx
		dec	eax
		mov	[di+2Ch], eax
		cmp	eax, edx
		jb	short loc_10E15
		dec	edx
		mov	[di+2Ch], edx
		sub	edx, ebx
		inc	edx
		mov	[di+28h], edx

loc_10E15:				; CODE XREF: psm_module+DEj
		or	byte [di+3Ch], 8

loc_10E19:				; CODE XREF: psm_module+C8j
		add	si, 40h	; '@'
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_10D8C
		mov	dx, byte_27FE8
		mov	cx, [word_245FA]
		mov	eax, [dword_3055A]
		call	dosseek
		mov	dx, [word_30562]
		mov	cx, [word_30564]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		adc	WORD [word_24662], 0
		mov	cx, [word_245F2]

loc_10E4C:				; CODE XREF: psm_module+1DCj
		push	cx
		mov	dx, word_31508
		mov	cx, 4
		call	dosfread
		xor	si, si
		mov	cx, [word_245FA]
		mov	ax, [my_seg_index]
		mov	dl, [byte_3150A]
		dec	dl
		and	dl, 3Fh

loc_10E68:				; CODE XREF: psm_module+14Ej
		cmp	BYTE [byte_27FE8+si], al
		jnz	short loc_10E72
		mov	BYTE [byte_281E8+si], dl

loc_10E72:				; CODE XREF: psm_module+146j
		inc	si
		dec	cx
		jnz	short loc_10E68
		mov	dx, byte_3150C
		mov	cx, [word_31508]
		sub	cx, 4
		call	dosfread
		call	memalloc12k
		mov	si, byte_3150C
		mov	cx, 40h	; '@'

loc_10E8C:				; CODE XREF: psm_module+1D5j
		push	cx
		lodsb
		or	al, al
		jz	short loc_10EF4

loc_10E92:				; CODE XREF: psm_module+1CCj
		xor	bx, bx
		mov	ch, al
		test	ch, 80h
		jz	short loc_10EBD
		mov	bx, [si]
		add	si, 2
		or	bl, bl
		jz	short loc_10EB6
		dec	bl
		movzx	ax, bl
		mov	bl, 0Ch
		div	bl
		inc	ah
		shl	al, 4
		or	al, ah
		mov	bl, al

loc_10EB6:				; CODE XREF: psm_module+17Cj
		cmp	bh, 63h	; 'c'
		jbe	short loc_10EBD
		xor	bh, bh

loc_10EBD:				; CODE XREF: psm_module+173j
					; psm_module+193j
		mov	cl, 0FFh
		test	ch, 40h
		jz	short loc_10ECE
		mov	cl, [si]
		inc	si
		cmp	cl, 40h	; '@'
		jbe	short loc_10ECE
		mov	cl, 0FFh

loc_10ECE:				; CODE XREF: psm_module+19Cj
					; psm_module+1A4j
		test	ch, 20h
		jz	short loc_10EDD
		mov	dx, [si]
		add	si, 2
		cmp	dl, 0Fh
		jbe	short loc_10EDF

loc_10EDD:				; CODE XREF: psm_module+1ABj
		xor	dx, dx

loc_10EDF:				; CODE XREF: psm_module+1B5j
		and	ch, 1Fh
		cmp	byte [word_245D4+1], ch
		jnb	short loc_10EEC
		mov	byte [word_245D4+1], ch

loc_10EEC:				; CODE XREF: psm_module+1C0j
		call	sub_11BA6
		lodsb
		or	al, al
		jnz	short loc_10E92

loc_10EF4:				; CODE XREF: psm_module+16Aj
		mov	byte [es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	short loc_10E8C
		call	mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_10E4C
		mov	ax, [word_245D4]
		inc	ah
		cmp	al, ah
		jb	short loc_10F11
		mov	al, ah

loc_10F11:				; CODE XREF: psm_module+1E7j
		xor	ah, ah
		mov	[word_245D4], ax
		call	near mod_readfile_11F4E
		jb	loc_10099
		retn


; =============== S U B	R O U T	I N E =======================================

; FAR

faar_module:		; DATA XREF: seg003:0E40o
		mov	DWORD [module_type_text], 20524146h
		mov	WORD [moduleflag_246D0], 10000000b
		mov	BYTE [byte_24673], 0
		mov	BYTE [byte_2467E], 2
		mov	WORD [word_245D4], 10h
		mov	al, byte [word_30552+1]
		and	ax, 0Fh
		mov	di, ax
		mov	al, [cs:table_14057+di]
		mov	[byte_2467B], al
		mov	BYTE [byte_2467C], 0
		call far calc_14043
		mov	[byte_2467A], al
		mov	BYTE [byte_24679], 4
		cmp	BYTE [sndcard_type],	0
		jnz	short loc_10F80
		xor	si, si
		mov	cx, [word_245D4]

loc_10F6A:				; CODE XREF: faar_module+60j
		mov	al, byte [word_30554+si]
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:byte_13C54+di]
		mov	byte [dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_10F6A

loc_10F80:				; CODE XREF: faar_module+44j
		mov	ax, ds
		mov	es, ax
		mov	si, myin	; in
		mov	di, asc_246B0 ; "				"
		mov	cx, 20h	; ' '   ; count
		call	copy_printable
		mov	dx, (dword_30566+2)
		mov	cx, 303h
		movzx	eax, word [dword_30566+2]
		add	eax, 62h ; 'b'
		call	dosseek
		movzx	ax, BYTE [byte_30669]
		cmp	ax, 100h
		jb	short loc_10FB0
		mov	ax, 100h

loc_10FB0:				; CODE XREF: faar_module+8Dj
		mov	[word_245FA], ax
		movzx	ax, BYTE [byte_3066A]
		mov	[word_245F8], ax
		mov	si, (dword_30566+2)
		mov	di, byte_27FE8
		mov	cx, [word_245FA]
		cld
		rep movsb
		mov	bx, byte_3066B
		xor	ax, ax
		xor	dx, dx

loc_10FCF:				; CODE XREF: faar_module+C0j
		inc	dx
		cmp	word [bx], 0
		jz	short loc_10FD7
		mov	ax, dx

loc_10FD7:				; CODE XREF: faar_module+B5j
		add	bx, 2
		cmp	dx, 100h
		jb	short loc_10FCF
		or	ax, ax
		stc
		jz	loc_10099
		cmp	ax, 100h
		jb	short loc_10FEF
		mov	ax, 100h

loc_10FEF:				; CODE XREF: faar_module+CCj
		mov	[word_245F2], ax
		mov	byte [chrin+3], 0
		mov	si, byte_3066B
		mov	cx, [word_245F2]

loc_10FFE:				; CODE XREF: faar_module+214j
		push	cx
		push	si
		mov	ax, [si]
		or	ax, ax
		jnz	short loc_1100F
		call	memalloc12k
		mov	cx, 40h	; '@'
		jmp	loc_11120
; ---------------------------------------------------------------------------

loc_1100F:				; CODE XREF: faar_module+E6j
		sub	ax, 2
		shr	ax, 2
		xor	dx, dx
		div	WORD [word_245D4]
		push	ax
		dec	al
		and	al, 3Fh
		mov	byte [chrin], al
		xor	di, di
		mov	cx, [word_245FA]
		mov	ah, byte [chrin+3]

loc_1102D:				; CODE XREF: faar_module+11Bj
		cmp	ah, [byte_27FE8+di]
		jnz	short loc_11037
		mov	BYTE [byte_281E8+di], al

loc_11037:				; CODE XREF: faar_module+113j
		inc	di
		dec	cx
		jnz	short loc_1102D
		mov	dx, word_31508
		mov	cx, [si]
		call	dosfread
		mov	byte [chrin+1], 0
		call	memalloc12k
		pop	cx
		xor	ch, ch
		mov	si, byte_3150A

loc_11051:				; CODE XREF: faar_module+1F7j
		push	cx
		mov	cx, [word_245D4]
		xor	ch, ch

loc_11058:				; CODE XREF: faar_module+1ECj
		push	cx
		xor	bx, bx
		mov	cl, 0FFh
		mov	al, [si]
		or	al, al
		jz	short loc_11082
		dec	al
		xor	ah, ah
		mov	dl, 0Ch
		div	dl
		inc	al
		inc	ah
		shl	al, 4
		or	al, ah
		mov	bl, al
		mov	bh, [si+1]
		inc	bh
		cmp	bh, 63h	; 'c'
		jb	short loc_11082
		xor	bh, bh

loc_11082:				; CODE XREF: faar_module+143j
					; faar_module+160j
		mov	cl, 0FFh
		mov	al, [si+2]
		or	al, al
		jz	short loc_11094
		dec	al
		and	al, 0Fh
		shl	al, 2
		mov	cl, al

loc_11094:				; CODE XREF: faar_module+16Bj
		mov	dl, [si+3]
		mov	dh, dl
		shr	dl, 4
		and	dh, 0Fh
		cmp	dl, 3
		jz	short loc_110CB
		cmp	dl, 4
		jz	short loc_110E4
		cmp	dl, 5
		jz	short loc_110CF
		cmp	dl, 6
		jz	short loc_110D9
		cmp	dl, 0Bh
		jz	short loc_110FA

loc_110B8:
		cmp	dl, 0Dh
		jz	short loc_110EF
		cmp	dl, 0Eh
		jz	short loc_110F3
		cmp	dl, 0Fh
		jz	short loc_110EB
		xor	dx, dx
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110CB:				; CODE XREF: faar_module+184j
		mov	dl, 19h
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110CF:				; CODE XREF: faar_module+18Ej
		shr	dh, 1
		mov	byte [chrin+1], dh
		xor	dx, dx
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110D9:				; CODE XREF: faar_module+193j
		shl	dh, 4
		or	dh, byte [chrin+1]
		mov	dl, 4
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110E4:				; CODE XREF: faar_module+189j
		mov	dl, 0Eh

loc_110E6:
		or	dh, 90h
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110EB:				; CODE XREF: faar_module+1A7j
		mov	dl, 1Fh
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110EF:				; CODE XREF: faar_module+19Dj
		mov	dl, 20h	; ' '
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110F3:				; CODE XREF: faar_module+1A2j
		mov	dl, 20h	; ' '
		shl	dh, 4
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110FA:				; CODE XREF: faar_module+198j
		mov	dl, 0Eh

loc_110FC:
		or	dh, 80h

loc_110FF:				; CODE XREF: faar_module+1ABj
					; faar_module+1AFj ...
		call	sub_11BA6
		add	si, 4
		pop	cx
		inc	ch
		cmp	ch, cl
		jb	loc_11058
		mov	byte [es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	loc_11051
		mov	cx, 3Fh	; '?'
		sub	cl, byte [chrin]

loc_11120:				; CODE XREF: faar_module+EEj
		xor	al, al
		cld
		rep stosb
		call	mem_reallocx
		pop	si
		pop	cx
		inc	byte [chrin+3]
		add	si, 2
		dec	cx
		jnz	loc_10FFE
		mov	ax, ds
		mov	es, ax

loc_1113A:
		mov	dx, myin
		mov	cx, 8
		call	dosfread
		mov	si, myin
		mov	di, myout

loc_11149:
		xor	ax, ax
		mov	[word_245D2], ax
		mov	ch, 8

loc_11150:				; CODE XREF: faar_module+305j
		mov	cl, 8

loc_11152:				; CODE XREF: faar_module+2FEj
		inc	ax
		shr	byte [si], 1
		jnb	loc_11217
		push	ax
		push	cx
		push	si
		push	di
		mov	[word_245D2], ax
		push	di
		mov	dx, word_31508
		mov	cx, 30h	; '0'
		call	dosfread
		xor	dx, dx
		xor	cx, cx
		mov	bx, [fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		pop	di		; out
		mov	[di+38h], ax
		mov	[di+3Ah], dx
		mov	si, word_31508 ;	in

loc_11181:
		mov	edx, [si+20h]
		cmp	edx, 100000h
		cmc

loc_1118D:
		adc	WORD [word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	al, [si+25h]
		ror	al, 4
		shr	al, 2
		mov	[di+3Dh], al
		mov	ax, [freq_245DE]
		mov	[di+36h], ax

loc_111AD:
		test	byte [si+2Fh], 8
		jnz	short loc_111C6

loc_111B3:				; CODE XREF: faar_module+2AFj
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_111E8
; ---------------------------------------------------------------------------

loc_111C6:				; CODE XREF: faar_module+293j
		mov	eax, [si+2Ah]
		or	eax, eax
		jz	short loc_111B3
		mov	[di+2Ch], eax
		mov	ebx, [si+26h]
		mov	[di+24h], ebx

loc_111DB:
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	byte [di+3Ch], 8

loc_111E8:				; CODE XREF: faar_module+2A6j
		mov	cx, 20h	; ' '   ; count
		call	copy_printable
		test	byte [si+2Eh], 1
		jz	short loc_11204
		or	byte [di+3Ch], 4
		shr	dword [di+24h], 1
		shr	dword [di+2Ch], 1
		shr	dword [di+28h], 1

loc_11204:				; CODE XREF: faar_module+2D4j
		mov	dx, [si+20h]
		mov	cx, [si+22h]
		mov	bx, [fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		pop	di
		pop	si
		pop	cx
		pop	ax

loc_11217:				; CODE XREF: faar_module+237j
		add	di, 40h	; '@'
		dec	cl
		jnz	loc_11152
		inc	si
		dec	ch
		jnz	loc_11150
		cmp	WORD [word_245D2], 0
		stc
		jz	loc_10099
		call	near mod_readfile_11F4E
		jb	loc_10099
		retn


; =============== S U B	R O U T	I N E =======================================

; ULT

ult_module:		; DATA XREF: seg003:0E49o
		mov	DWORD [module_type_text], 20544C55h
		mov	WORD [moduleflag_246D0], 1000000000b
		mov	BYTE [byte_24673], 0
		mov	word [chrin], 40h ;	'@'
		mov	ax, [word_30515]

loc_11256:
		xchg	al, ah
		mov	[word_30515], ax
		cmp	ax, 3034h
		jb	short loc_11265
		add	word [chrin], 2

loc_11265:				; CODE XREF: ult_module+25j
		mov	BYTE [byte_24679], 6
		mov	BYTE [byte_2467A], 7Dh ; '}'

loc_1126F:
		mov	ax, ds
		mov	es, ax
		mov	si, myin_0 ; in
		mov	di, asc_246B0 ; "				"
		mov	cx, 20h	; ' '   ; count
		call	copy_printable
		mov	dx, my_in
		mov	cx, 1
		movzx	eax, BYTE [byte_30537]
		shl	eax, 5
		add	eax, 30h ; '0'
		call	dosseek
		movzx	ax, BYTE [my_in]
		mov	[word_245D2], ax
		mul	word [chrin]
		mov	cx, ax
		mov	dx, byte_30539
		call	dosfread
		mov	si, byte_30539 ;	in
		mov	di, myout ; out
		mov	cx, [word_245D2]

loc_112B4:				; CODE XREF: ult_module+131j
		push	cx
		push	si
		push	di
		mov	edx, [si+38h]
		sub	edx, [si+34h]
		jnb	short loc_112C4
		xor	edx, edx

loc_112C4:				; CODE XREF: ult_module+86j
		cmp	edx, 100000h
		cmc
		adc	WORD [word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	al, [si+3Ch]
		shr	al, 2
		mov	[di+3Dh], al
		mov	ax, [freq_245DE]
		cmp	WORD [word_30515], 3034h
		jb	short loc_112F1
		mov	ax, [si+3Eh]

loc_112F1:				; CODE XREF: ult_module+B3j
		mov	[di+36h], ax
		mov	al, [si+3Dh]
		and	al, 1Ch
		mov	[di+3Ch], al
		test	al, 4
		jz	short loc_11316
		add	[dword_245C4], edx
		cmp	edx, 80000h
		cmc
		adc	WORD [word_24662], 0
		shl	dword [di+20h], 1

loc_11316:				; CODE XREF: ult_module+C5j
		test	al, 8
		jnz	short loc_1132D

loc_1131A:				; CODE XREF: ult_module+FBj
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_11359
; ---------------------------------------------------------------------------

loc_1132D:				; CODE XREF: ult_module+DFj
		mov	eax, [si+30h]
		or	eax, eax
		jz	short loc_1131A
		dec	eax
		mov	ebx, [si+2Ch]
		test	byte [di+3Ch], 4
		jz	short loc_11348
		shr	ebx, 1
		shr	eax, 1

loc_11348:				; CODE XREF: ult_module+107j
		mov	[di+24h], ebx
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax

loc_11359:				; CODE XREF: ult_module+F2j
		mov	cx, 20h	; ' '   ; count
		call	copy_printable
		pop	di
		pop	si
		pop	cx
		add	di, 40h	; '@'

loc_11365:
		add	si, word [chrin]
		dec	cx
		jnz	loc_112B4
		mov	dx, byte_30539
		mov	cx, 102h
		call	dosfread
		mov	WORD [word_245F8], 0
		mov	si, byte_30539
		xor	ax, ax

loc_11382:				; CODE XREF: ult_module+153j
		cmp	byte [si], 0FFh
		jz	short loc_1138E
		inc	ax
		inc	si
		cmp	ax, 100h
		jb	short loc_11382

loc_1138E:				; CODE XREF: ult_module+14Cj
		mov	[word_245FA], ax
		mov	ax, ds
		mov	es, ax
		mov	si, byte_30539
		mov	di, byte_27FE8
		mov	cx, [word_245FA]
		cld
		rep movsb
		movzx	ax, BYTE [byte_30639]
		inc	ax
		mov	[word_245D4], ax
		movzx	ax, BYTE [byte_3063A]
		inc	ax
		mov	[word_245F2], ax
		mov	BYTE [byte_2467E], 0
		mov	ax, [word_30515]
		cmp	ax, 3031h
		jz	short loc_113C6
		mov	BYTE [byte_2467E], 2

loc_113C6:				; CODE XREF: ult_module+186j
		cmp	ax, 3033h
		jb	short loc_113F8
		mov	dx, word_3063B
		mov	cx, [word_245D4]
		call	dosfread
		cmp	BYTE [sndcard_type],	0
		jnz	short loc_113F8
		xor	si, si
		mov	cx, [word_245D4]

loc_113E2:				; CODE XREF: ult_module+1BDj
		mov	al, byte [word_3063B+si]
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:byte_13C54+di]
		mov	byte [dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_113E2

loc_113F8:				; CODE XREF: ult_module+190j
					; ult_module+1A1j
		mov	si, dword_30518
		mov	cx, [word_245D4]

loc_113FF:				; CODE XREF: ult_module+1F9j
		push	cx
		push	si
		xor	dx, dx
		xor	cx, cx
		mov	bx, [fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		mov	[si], ax
		mov	[si+2],	dx
		mov	cx, [word_245F2]

loc_11417:				; CODE XREF: ult_module+1F1j
		push	cx
		mov	byte [word_3063B+1], 1
		mov	cx, 40h	; '@'

loc_11420:				; CODE XREF: ult_module+1EDj
		push	cx
		call	ult_read
		pop	cx
		dec	cx
		jnz	short loc_11420
		pop	cx
		dec	cx
		jnz	short loc_11417
		pop	si
		pop	cx
		add	si, 4
		dec	cx
		jnz	short loc_113FF
		mov	cx, [word_245F2]

loc_11438:				; CODE XREF: ult_module+2C6j
		push	cx
		mov	si, dword_30518
		mov	di, byte_30908
		mov	cx, [word_245D4]

loc_11443:				; CODE XREF: ult_module+250j
		push	cx
		mov	dx, [si]
		mov	cx, [si+2]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		mov	byte [word_3063B+1], 1
		mov	cx, 40h	; '@'

loc_1145A:				; CODE XREF: ult_module+237j
		push	cx
		call	ult_read
		mov	eax, [dword_3063D]
		mov	[di], eax
		mov	al, [byte_30641]
		mov	[di+4],	al
		add	di, 5
		pop	cx
		dec	cx
		jnz	short loc_1145A
		xor	dx, dx
		xor	cx, cx
		mov	bx, [fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		mov	[si], ax
		mov	[si+2],	dx
		pop	cx
		add	si, 4
		dec	cx
		jnz	short loc_11443
		call	memalloc12k
		mov	si, byte_30908
		mov	cx, 40h	; '@'

loc_11494:				; CODE XREF: ult_module+2BFj
		push	cx
		push	si
		mov	cx, [word_245D4]
		xor	ch, ch

loc_1149C:				; CODE XREF: ult_module+2B2j
		push	cx
		xor	bx, bx
		mov	al, [si]
		or	al, al
		jz	short loc_114C0
		dec	al
		xor	ah, ah
		mov	cl, 0Ch
		div	cl
		shl	al, 4
		inc	ah
		or	al, ah
		mov	bl, al
		mov	bh, [si+1]
		cmp	bh, 63h	; 'c'
		jb	short loc_114C0
		xor	bh, bh

loc_114C0:				; CODE XREF: ult_module+26Aj
					; ult_module+283j
		mov	cl, 0FFh
		mov	al, [si+2]
		mov	dl, al
		shr	al, 4
		mov	ah, [si+4]
		and	dl, 0Fh
		mov	dh, [si+3]
		call	ult_1150B
		xchg	ax, dx
		call	ult_1150B
		cmp	dl, al
		ja	short loc_114DF
		xchg	ax, dx

loc_114DF:				; CODE XREF: ult_module+2A3j
		call	sub_11BA6
		pop	cx
		add	si, 140h
		inc	ch
		cmp	ch, cl
		jb	short loc_1149C
		mov	byte [es:di], 0
		inc	di
		pop	si
		pop	cx
		add	si, 5
		dec	cx
		jnz	short loc_11494
		call	mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_11438
		call	near mod_readfile_11F4E
		jb	loc_10099
		retn


; =============== S U B	R O U T	I N E =======================================


ult_1150B:		; CODE XREF: ult_module+29Ap
					; ult_module+29Ep
		cmp	al, 5
		jz	short loc_11520
		cmp	al, 0Ah
		jz	short loc_11523
		cmp	al, 0Bh
		jz	short loc_1152A
		cmp	al, 0Ch
		jz	short loc_11531
		cmp	al, 0Eh
		jz	short loc_11539
		retn
; ---------------------------------------------------------------------------

loc_11520:				; CODE XREF: ult_1150B+2j
		xor	ax, ax
		retn
; ---------------------------------------------------------------------------

loc_11523:				; CODE XREF: ult_1150B+6j
		shr	ah, 2
		and	ah, 33h
		retn
; ---------------------------------------------------------------------------

loc_1152A:				; CODE XREF: ult_1150B+Aj
		and	ax, 0F00h
		or	ax, 800Eh
		retn
; ---------------------------------------------------------------------------

loc_11531:				; CODE XREF: ult_1150B+Ej
		mov	cl, ah
		shr	cl, 2
		xor	ax, ax
		retn
; ---------------------------------------------------------------------------

loc_11539:				; CODE XREF: ult_1150B+12j
		push	dx
		mov	dx, ax
		shr	dx, 4
		cmp	dl, 0EAh ; 'Í'
		jz	short loc_1154B
		cmp	dl, 0EBh ; 'Î'
		jz	short loc_1154B
		pop	dx
		retn
; ---------------------------------------------------------------------------

loc_1154B:				; CODE XREF: ult_1150B+37j
					; ult_1150B+3Cj
		mov	dh, ah
		and	dh, 0F0h
		and	ah, 0Fh
		shr	ah, 2
		or	ah, dh
		pop	dx
		retn


; =============== S U B	R O U T	I N E =======================================


ult_read:		; CODE XREF: ult_module+1E8p
					; ult_module+222p
		dec	byte [word_3063B+1]
		jnz	short locret_11584
		mov	dx, word_3063B
		mov	cx, 2
		call	dosfread
		cmp	byte [word_3063B], 0FCh ; '¸'
		jz	short loc_11585
		mov	ax, [word_3063B]
		mov	word [dword_3063D],	ax
		mov	byte [word_3063B+1], 1
		mov	dx, (dword_3063D+2)
		mov	cx, 3
		call	dosfread

locret_11584:				; CODE XREF: ult_read+4j
		retn
; ---------------------------------------------------------------------------

loc_11585:				; CODE XREF: ult_read+14j
		mov	dx, dword_3063D
		mov	cx, 5
		call	dosfread
		retn


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


 ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


inr_read_118B0:	; CODE XREF: inr_module+152p
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	es, ax
		shl	dx, 6
		mov	ax, dx
		add	ax, myout
		push	ax
		mov	cx, 96
		mov	bx, [fhandle_module]
		mov	dx, aInertiaSample ; "Inertia Sample: "
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	bx
		jb	loc_119B2
		lea	di, [bx]
		mov	si, asc_25856 ; "				\r\n\x1A"
		cld
		mov	cx, 8
		rep movsd
		mov	di, bx
		mov	ecx, [dword_25892]
		mov	[di+24h], ecx
		mov	eax, [dword_25896]
		mov	[di+2Ch], eax
		sub	eax, ecx
		inc	eax
		mov	[di+28h], eax
		mov	ax, [word_2588E]
		mov	[di+36h], ax
		mov	al, [byte_2588C]
		mov	[di+3Eh], al
		mov	al, [byte_2588B]
		mov	[di+3Dh], al
		mov	al, [byte_2588D]
		mov	[di+3Ch], al
		mov	eax, [dword_25886]
		mov	[di+20h], eax

loc_1191C:				; CODE XREF: inr_read_118B0+FCj
		mov	dx, chrin
		mov	cx, 8
		mov	bx, [fhandle_module]
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		jb	loc_119B2
		mov	eax, [myin]
		mov	[dword_257A0], eax
		xor	cx, cx
		xor	dx, dx
		mov	bx, [fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		shl	edx, 10h
		mov	dx, ax
		add	[dword_257A0], edx
		mov	eax, [chrin]
		cmp	eax, 54414453h	; SDAT
		jnz	short loc_11967	; SAMP
		mov	[di+38h], edx
		test	BYTE [sndflags_24622], 4
		jnz	short loc_11999
		jmp	short loc_11999
; ---------------------------------------------------------------------------

loc_11967:				; CODE XREF: inr_read_118B0+A8j
		cmp	eax, 504D4153h	; SAMP
		jnz	short loc_11991	; ENDS
		xor	cx, cx
		xor	dx, dx
		mov	bx, [fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		mov	dx, ax
		mov	cx, dx
		sub	dx, 8
		sub	cx, 0
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		jmp	short loc_119AF
; ---------------------------------------------------------------------------

loc_11991:				; CODE XREF: inr_read_118B0+BDj
		cmp	eax, 53444E45h	; ENDS
		jz	short loc_119AF

loc_11999:				; CODE XREF: inr_read_118B0+B3j
					; inr_read_118B0+B5j
		mov	dx, word [dword_257A0]
		mov	cx, word [dword_257A0+2]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		jb	short loc_119B2
		jmp	loc_1191C
; ---------------------------------------------------------------------------

loc_119AF:				; CODE XREF: inr_read_118B0+DFj
					; inr_read_118B0+E7j
		clc
		pop	ds
		retn
; ---------------------------------------------------------------------------

loc_119B2:				; CODE XREF: inr_read_118B0+20j
					; inr_read_118B0+7Aj ...
		mov	ax, 0FFFEh
		pop	ds
		retn


; =============== S U B	R O U T	I N E =======================================


; void __usercall inr_read_119B7(void *buffer<edi>)
inr_read_119B7:	; CODE XREF: inr_module+B0p
					; inr_module+C5p ...
		mov	ecx, [myin]
		mov	bx, [fhandle_module]
		mov	dx, di
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		retn


; =============== S U B	R O U T	I N E =======================================

; INR

inr_module:		; DATA XREF: seg003:off_25326o
		mov	DWORD [module_type_text], 20524E49h
		mov	WORD [moduleflag_246D0], 100000000b
		mov	BYTE [byte_24673], 0
		mov	WORD [word_245F2], 0
		mov	WORD [word_245D2], 0
		mov	ax, ds
		mov	es, ax
		cld
		mov	dx, aInertiaModule ; "Inertia Module: "
		mov	cx, 50h	; 'P'
		xor	eax, eax
		call	dosseek
		mov	si, (aInertiaModule+10h)
		mov	di, asc_246B0 ; "				"
		mov	cx, 8
		cld
		rep movsd
		mov	al, [byte_257DB]
		mov	[byte_2461A], al
		mov	al, [byte_257DC]
		mov	[byte_2467E], al
		mov	ax, [word_257E6]
		mov	[word_245D4], ax
		dec	ax
		mov	[byte_2461B], al
		mov	ax, [word_257EC]
		mov	[freq_245DE], ax
		mov	ax, [word_257EE]
		mov	[word_245FA], ax
		mov	ax, [word_257F0]
		mov	[word_245F8], ax
		mov	al, [byte_257F2]
		mov	[byte_2467A], al
		mov	al, [byte_257F3]
		mov	[byte_24679], al

loc_11A39:				; CODE XREF: inr_module+172j
		mov	cx, 8
		mov	bx, [fhandle_module]
		mov	dx, chrin
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		jb	loc_11B3D
		mov	eax, [myin]
		mov	[dword_257A0], eax
		xor	cx, cx
		xor	dx, dx
		mov	bx, [fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		add	word [dword_257A0],	ax
		adc	word [dword_257A0+2], dx
		mov	eax, [chrin]
		cmp	eax, 54534C54h	; TLST
		jnz	short loc_11A81	; BLST
		mov	di, byte_280E8 ;	buffer
		call	inr_read_119B7
		jb	loc_11B3D
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11A81:				; CODE XREF: inr_module+ABj
		cmp	eax, 54534C42h	; BLST
		jnz	short loc_11A96	; PLST
		mov	di, byte_281E8 ;	buffer
		call	inr_read_119B7
		jb	loc_11B3D
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11A96:				; CODE XREF: inr_module+C0j
		cmp	eax, 54534C50h	; PLST
		jnz	short loc_11AAA	; PATT
		mov	di, byte_27FE8 ;	buffer
		call	inr_read_119B7
		jb	loc_11B3D
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11AAA:				; CODE XREF: inr_module+D5j
		cmp	eax, 54544150h	; PATT
		jnz	short loc_11B09	; SAMP
		mov	ebx, [myin]
		cmp	ebx, 40h ; '@'
		ja	short loc_11AC0
		mov	bx, 40h	; '@'   ; bytes

loc_11AC0:				; CODE XREF: inr_module+F4j
		call	memalloc
		jb	short loc_11B3D
		mov	ecx, [myin]
		mov	di, [word_245F2]
		inc	WORD [word_245F2]
		shl	di, 1
		mov	WORD [segs_table+di], ax
		cmp	cx, 40h	; '@'
		jbe	short loc_11AF3
		mov	WORD [myseg_size+di], cx
		xor	dx, dx
		mov	bx, [fhandle_module]
		push	ds
		mov	ds, ax
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	ds
		jb	short loc_11B3D
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11AF3:				; CODE XREF: inr_module+114j
		mov	WORD [myseg_size+di], 40h ; '@'
		xor	di, di
		mov	es, ax
		mov	cx, 10h
		xor	eax, eax
		cld
		rep stosd
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11B09:				; CODE XREF: inr_module+E9j
		cmp	eax, 504D4153h	; SAMP
		jnz	short loc_11B20	; ENDM
		mov	dx, [word_245D2]
		inc	WORD [word_245D2]
		call	inr_read_118B0
		jb	short loc_11B3D
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11B20:				; CODE XREF: inr_module+148j
		cmp	eax, 4D444E45h	; ENDM
		jz	short loc_11B41

loc_11B28:				; CODE XREF: inr_module+B7j
					; inr_module+CCj ...
		mov	dx, word [dword_257A0]
		mov	cx, word [dword_257A0+2]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		jnb	loc_11A39

loc_11B3D:				; CODE XREF: inr_module+80j
					; inr_module+B3j ...
		mov	ax, 0FFFEh
		retn
; ---------------------------------------------------------------------------

loc_11B41:				; CODE XREF: inr_module+15Fj
		call	near mod_readfile_11F4E
		retn


; =============== S U B	R O U T	I N E =======================================


dosseek:		; CODE XREF: _2stm_module+F3p
					; s3m_module+11Cp ...
		push	cx
		push	dx
		mov	dx, ax
		shr	eax, 10h
		mov	cx, ax
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		pop	dx
		pop	cx
		mov	ax, 0FFFCh
		jb	lfreaderr


; =============== S U B	R O U T	I N E =======================================


dosfread:		; CODE XREF: moduleread+39p
					; mod_read_10311+Fp ...
		mov	bx, [fhandle_module]
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		mov	cx, ax
		mov	ax, 0FFFCh
		jb	lfreaderr	; 1 problem here
		retn


; =============== S U B	R O U T	I N E =======================================


memalloc12k:	; CODE XREF: mod_read_10311:loc_1035Cp
					; _2stm_module+118p ...
		mov	ebx, 12352	; bytes
		call	memalloc
		jb	loc_10099
		mov	es, ax
		xor	di, di
		retn


; =============== S U B	R O U T	I N E =======================================


mem_reallocx:	; CODE XREF: mod_read_10311+D0p
					; _2stm_module+190p ...
		mov	bx, [my_seg_index]
		shl	bx, 1
		mov	WORD [segs_table+bx], es
		mov	WORD [myseg_size+bx], di
		movzx	ebx, di
		mov	ax, es
		call	memrealloc
		adc	WORD [word_24662], 0
		inc	WORD [my_seg_index]
		retn


; =============== S U B	R O U T	I N E =======================================


sub_11BA6:		; CODE XREF: mod_read_10311+BDp
					; _2stm_module:loc_10565p ...
		and	ch, 1Fh
		or	bl, bl
		jz	short loc_11BB2
		cmp	bl, 0FFh
		jnz	short loc_11BBB

loc_11BB2:				; CODE XREF: sub_11BA6+5j
		or	bh, bh
		jz	short loc_11BBE
		cmp	bh, 0FFh
		jz	short loc_11BBE

loc_11BBB:				; CODE XREF: sub_11BA6+Aj
		or	ch, 20h

loc_11BBE:				; CODE XREF: sub_11BA6+Ej
					; sub_11BA6+13j
		cmp	cl, 40h	; '@'
		ja	short loc_11BC6
		or	ch, 40h

loc_11BC6:				; CODE XREF: sub_11BA6+1Bj
		or	dx, dx
		jz	short loc_11BD1
		or	dl, dl
		jz	short loc_11C08

loc_11BCE:				; CODE XREF: sub_11BA6+64j
		or	ch, 80h

loc_11BD1:				; CODE XREF: sub_11BA6+22j
		test	ch, 0E0h
		jz	short locret_11C03
		mov	[es:di], ch
		inc	di
		test	ch, 80h
		jz	short loc_11BE5
		mov	[es:di], dx
		add	di, 2

loc_11BE5:				; CODE XREF: sub_11BA6+37j
		test	ch, 40h
		jz	short loc_11BEE
		mov	[es:di], cl
		inc	di

loc_11BEE:				; CODE XREF: sub_11BA6+42j
		test	ch, 20h
		jz	short loc_11BF9
		mov	[es:di], bx
		add	di, 2

loc_11BF9:				; CODE XREF: sub_11BA6+4Bj
		mov	al, ch
		and	al, 1Fh
		cmp	al, [byte_2461B]
		ja	short loc_11C04

locret_11C03:				; CODE XREF: sub_11BA6+2Ej
		retn
; ---------------------------------------------------------------------------

loc_11C04:				; CODE XREF: sub_11BA6+5Bj
		mov	[byte_2461B], al
		retn
; ---------------------------------------------------------------------------

loc_11C08:				; CODE XREF: sub_11BA6+26j
		mov	dl, 1Dh
		jmp	short loc_11BCE


; =============== S U B	R O U T	I N E =======================================


sub_11C0C:		; CODE XREF: sub_1415E+65p
		xor	si, si
		or	al, al
		jz	short locret_11C28
		xor	bx, bx

loc_11C14:				; CODE XREF: sub_11C0C+16j
					; sub_11C0C+1Aj
		mov	bl, [cs:byte_11C29+bx]
		add	si, bx
		mov	bl, [es:si]
		inc	si
		shr	bl, 5
		jnz	short loc_11C14
		dec	al
		jnz	short loc_11C14

locret_11C28:				; CODE XREF: sub_11C0C+4j
		retn

; ---------------------------------------------------------------------------
byte_11C29	db 0			; DATA XREF: sub_11C0C:loc_11C14r
					; sub_13623+1A1r
		db 2, 1, 3, 2, 4, 3, 5

; =============== S U B	R O U T	I N E =======================================


; int __usercall copy_printable<eax>(char *in<esi>, char *out<edi>, int	count<ecx>)
copy_printable:	; CODE XREF: mod_1021E+28p
					; mod_1024A+11p ...
		push	si
		push	di

loc_11C33:				; CODE XREF: copy_printable+Dj
		mov	al, [si]
		inc	si
		cmp	al, 20h	; ' '
		jb	short loc_11C40
		mov	[di], al
		inc	di
		dec	cx
		jnz	short loc_11C33

loc_11C40:				; CODE XREF: copy_printable+7j
		pop	di
		pop	si
		retn


; =============== S U B	R O U T	I N E =======================================


clean_11C43:		; CODE XREF: moduleread:loc_1003Dp
					; sub_12DA8+75p ...
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	BYTE [byte_24679], 6
		mov	BYTE [byte_2467A], 125
		mov	BYTE [byte_2467E], 0
		mov	WORD [moduleflag_246D0], 1
		mov	WORD [my_seg_index],	0
		mov	WORD [word_245F0], 0
		mov	WORD [word_245F6], 0
		mov	BYTE [byte_24673], 0
		mov	WORD [word_24630], 2
		mov	WORD [word_245FA], 0
		mov	WORD [word_245F8], 0
		mov	WORD [word_245D4], 4
		mov	WORD [word_245D6], 4
		mov	WORD [word_245D8], 0
		mov	WORD [word_245DA], 0
		mov	WORD [word_245D2], 0
		mov	WORD [freq_245DE], 8287
		test	BYTE [flag_playsetttings], 8
		jnz	short loc_11CB8
		mov	WORD [freq_245DE], 8363

loc_11CB8:				; CODE XREF: clean_11C43+6Dj
		mov	BYTE [byte_2461A], 0
		mov	DWORD [dword_245C4], 0
		mov	WORD [amplification], 100
		mov	BYTE [byte_24625], 0
		mov	ax, ds
		mov	es, ax
		cld
		mov	di, asc_246B0 ; "				"
		mov	cx, 8
		mov	eax, '    '
		rep stosd
		mov	di, volume_25908
		xor	eax, eax
		mov	cx, 280h
		rep stosd
		mov	di, byte_282E8
		mov	cx, 8
		rep stosd
		mov	di, dword_27BC8
		mov	ah, [byte_2461E]
		mov	al, [byte_2461F]
		shl	eax, 10h
		mov	ah, [byte_2461F]
		mov	al, [byte_2461E]
		mov	cx, 8
		rep stosd
		mov	di, myout
		xor	eax, eax
		mov	cx, 630h
		rep stosd
		mov	dx, 63h	; 'c'
		mov	di, myout
		mov	eax, '    '

loc_11D2D:				; CODE XREF: clean_11C43+FCj
		mov	cx, 8
		rep stosd
		sub	di, 20h	; ' '
		mov	word [di+32h], 0FFFFh
		add	di, 40h	; '@'
		dec	dx
		jnz	short loc_11D2D
		mov	di, segs_table
		mov	cx, 80h	; 'Ä'
		xor	eax, eax
		rep stosd
		mov	di, byte_280E8
		mov	cx, 40h	; '@'
		rep stosd
		mov	di, byte_27FE8
		mov	cx, 40h	; '@'
		rep stosd
		mov	di, byte_282E8
		mov	cx, 8
		rep stosd
		mov	di, byte_281E8
		mov	cx, 40h	; '@'
		mov	eax, 3F3F3F3Fh
		rep stosd
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


ems_init:		; CODE XREF: sub_12DA8+103p
		mov	BYTE [ems_enabled], 0
		mov	ax, 1
		test	byte [config_word],	2
		jz	short loc_11E00
		xor	ax, ax
		mov	es, ax
		mov	ax, 1
		mov	es, word [es:19Eh]
		cmp	dword [es:0Ah], 584D4D45h ;	EMMX
		jnz	short loc_11E00
		cmp	dword [es:0Eh], 30585858h ;	XXX0
		jnz	short loc_11E00
		mov	ah, 40h	; '@'
		int	67h		;  - LIM EMS - GET MANAGER STATUS
					; Return: AH = status
		mov	bx, ax
		mov	ax, 2
		or	bh, bh
		jnz	short loc_11E00
		mov	ah, 46h	; 'F'
		int	67h		;  - LIM EMS - GET EMM VERSION
					; Return: AH = status
		mov	bx, ax
		mov	ax, 2
		or	bh, bh
		jnz	short loc_11E00
		mov	ax, 3
		cmp	bl, 40h	; '@'
		jb	short loc_11E00
		mov	ah, 41h	; 'A'
		int	67h		;  - LIM EMS - GET PAGE	FRAME SEGMENT
					; Return: AH = 00h function successful,	BX = segment of	page frame
					; AH = error code
		cmp	ah, 0
		mov	ax, 2
		jnz	short loc_11E00
		mov	[ems_pageframe], bx
		mov	ah, 43h	; 'C'
		mov	bx, 1
		int	67h		;  - LIM EMS - GET HANDLE AND ALLOCATE MEMORY
					; BX = number of logical pages to allocate
					; Return: AH = status
		cmp	ah, 0
		mov	ax, 8
		jnz	short loc_11E00
		mov	[ems_handle], dx
		mov	BYTE [ems_enabled], 1
		mov	WORD [ems_log_pagenum], 0
		xor	ax, ax
		clc
		retn
; ---------------------------------------------------------------------------

loc_11E00:				; CODE XREF: ems_init+Dj ems_init+25j	...
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


ems_release:	; CODE XREF: ems_deinit+7p
		cmp	BYTE [ems_enabled], 1
		jnz	short locret_11E1D
		mov	bx, 8000h
		call	ems_mapmem
		mov	dx, [ems_handle]
		mov	ah, 45h	; 'E'
		int	67h		;  - LIM EMS - RELEASE HANDLE AND MEMORY
					; DX = EMM handle
					; Return: AH = status
		mov	WORD [ems_log_pagenum], 0

locret_11E1D:				; CODE XREF: ems_release+5j
		retn


; =============== S U B	R O U T	I N E =======================================


ems_realloc:	; CODE XREF: memfree_125DA+6p
		cmp	BYTE [ems_enabled], 1
		jnz	short locret_11E36
		mov	dx, [ems_handle]
		mov	bx, 1
		mov	ah, 51h	; 'Q'
		int	67h		;  - LIM EMS 4.0 - REALLOCATE PAGES
					; DX = handle
					; BX = number of pages to be allocated to handle
					; Return: BX = actual number of	pages allocated	to handle
					; AH = status
		mov	WORD [ems_log_pagenum], 0

locret_11E36:				; CODE XREF: ems_realloc+5j
		retn


; =============== S U B	R O U T	I N E =======================================


ems_deinit:		; CODE XREF: deinit_125B9+Fp
		cmp	BYTE [ems_enabled], 1
		jnz	short locret_11E46
		call	ems_release
		mov	BYTE [ems_enabled], 0

locret_11E46:				; CODE XREF: ems_deinit+5j
		retn


; =============== S U B	R O U T	I N E =======================================


ems_save_mapctx:	; CODE XREF: moduleread+24p
					; volume_prep+16p ...
		cmp	BYTE [ems_enabled], 1
		jnz	short locret_11E67
		mov	cx, 32h	; '2'

loc_11E51:				; CODE XREF: ems_save_mapctx+19j
		mov	dx, [ems_handle]
		mov	ax, 4700h
		int	67h		;  - LIM EMS - SAVE MAPPING CONTEXT
					; DX = handle
					; Return: AH = status
		cmp	ah, 0
		jz	short locret_11E67
		dec	cx
		jnz	short loc_11E51
		mov	BYTE [byte_246A5], 1

locret_11E67:				; CODE XREF: ems_save_mapctx+5j
					; ems_save_mapctx+16j
		retn


; =============== S U B	R O U T	I N E =======================================


ems_restore_mapctx:	; CODE XREF: moduleread+78p
					; moduleread+A9p ...
		cmp	BYTE [ems_enabled], 1
		jnz	short locret_11E8A
		cmp	BYTE [byte_246A5], 1
		jnz	short locret_11E8A
		mov	cx, 32h	; '2'

loc_11E79:				; CODE XREF: ems_restore_mapctx+20j
		mov	dx, [ems_handle]
		mov	ax, 4800h
		int	67h		;  - LIM EMS - RESTORE MAPPING CONTEXT
					; DX = handle
					; Return: AH = status
		cmp	ah, 0
		jz	short locret_11E8A
		dec	cx
		jnz	short loc_11E79

locret_11E8A:				; CODE XREF: ems_restore_mapctx+5j
					; ems_restore_mapctx+Cj ...
		retn


; =============== S U B	R O U T	I N E =======================================


ems_mapmem:		; CODE XREF: useless_11787+34p
					; ems_release+Ap ...
		cmp	BYTE [ems_enabled], 1
		jnz	short locret_11EC4
		mov	cx, 32h	; '2'
		cmp	bx, [ems_log_pagenum]
		jb	short loc_11E9E
		mov	bx, 0FFFFh	; EMS UNMAP

loc_11E9E:				; CODE XREF: ems_mapmem+Ej
					; ems_mapmem+37j
		push	bx
		mov	dx, [ems_handle]
		push	bx
		mov	ax, 4400h
		int	67h		;  - LIM EMS - MAP MEMORY
					; AL = physical	page number (0-3)
					; BX = logical page number, DX = handle
					; Return: AH = status
		pop	bx
		inc	bx
		jz	short loc_11EB3
		cmp	bx, [ems_log_pagenum]
		jb	short loc_11EB6

loc_11EB3:				; CODE XREF: ems_mapmem+20j
		mov	bx, 0FFFFh

loc_11EB6:				; CODE XREF: ems_mapmem+26j
		mov	ax, 4401h
		int	67h		;  - LIM EMS - MAP MEMORY
					; AL = physical	page number (0-3)
					; BX = logical page number, DX = handle
					; Return: AH = status
		cmp	ah, 0
		pop	bx
		jz	short locret_11EC4
		dec	cx
		jnz	short loc_11E9E

locret_11EC4:				; CODE XREF: ems_mapmem+5j
					; ems_mapmem+34j
		retn


; =============== S U B	R O U T	I N E =======================================


ems_mapmem2:	; CODE XREF: ems_mapmemx+48p
					; ems_mapmemx+F4p ...
		cmp	BYTE [ems_enabled], 1
		jnz	short locret_11EFE
		mov	cx, 32h	; '2'
		cmp	bx, [ems_log_pagenum]
		jb	short loc_11ED8
		mov	bx, 0FFFFh

loc_11ED8:				; CODE XREF: ems_mapmem2+Ej
					; ems_mapmem2+37j
		push	bx
		mov	dx, [ems_handle]
		push	bx
		mov	ax, 4402h
		int	67h		;  - LIM EMS - MAP MEMORY
					; AL = physical	page number (0-3)
					; BX = logical page number, DX = handle
					; Return: AH = status
		pop	bx
		inc	bx
		jz	short loc_11EED
		cmp	bx, [ems_log_pagenum]
		jb	short loc_11EF0

loc_11EED:				; CODE XREF: ems_mapmem2+20j
		mov	bx, 0FFFFh

loc_11EF0:				; CODE XREF: ems_mapmem2+26j
		mov	ax, 4403h
		int	67h		;  - LIM EMS - MAP MEMORY
					; AL = physical	page number (0-3)
					; BX = logical page number, DX = handle
					; Return: AH = status
		cmp	ah, 0
		pop	bx
		jz	short locret_11EFE
		dec	cx
		jnz	short loc_11ED8

locret_11EFE:				; CODE XREF: ems_mapmem2+5j
					; ems_mapmem2+34j
		retn


; =============== S U B	R O U T	I N E =======================================


ems_realloc2:	; CODE XREF: mod_readfile_11F4E+36p
		inc	BYTE [byte_24617]
		cmp	BYTE [ems_enabled], 1
		jnz	short loc_11F3C
		mov	ebx, [di+20h]
		shr	ebx, 4
		add	bx, 102h
		dec	bx
		shr	bx, 0Ah
		inc	bx
		mov	ah, 51h	; 'Q'
		mov	dx, [ems_handle]
		add	bx, [ems_log_pagenum]
		push	bx
		int	67h		;  - LIM EMS 4.0 - REALLOCATE PAGES
					; DX = handle
					; BX = number of pages to be allocated to handle
					; Return: BX = actual number of	pages allocated	to handle
					; AH = status
		pop	bx
		cmp	ah, 0
		jnz	short loc_11F3C
		mov	cx, [ems_log_pagenum]
		mov	[ems_log_pagenum], bx
		mov	bx, cx
		mov	ax, [ems_pageframe]
		retn
; ---------------------------------------------------------------------------

loc_11F3C:				; CODE XREF: ems_realloc2+9j
					; ems_realloc2+2Dj
		mov	ebx, [di+20h]
		add	ebx, 1020h	; bytes
		call	memalloc
		mov	cx, 0FFFFh
		retn


; =============== S U B	R O U T	I N E =======================================


mod_readfile_11F4E:	; CODE XREF: mod_n_t_module+6Ap
					; mod_n_t_module+159p ...
		mov	BYTE [byte_24617], 0
		cmp	WORD [word_24662], 0
		stc
		jnz	short locret_11FD3
		test	BYTE [sndflags_24622], 4
		jnz	short loc_11FD6
		test	BYTE [sndflags_24622], 10h
		jnz	short loc_11FD2
		mov	cx, [word_245D2]
		mov	di, myout

loc_11F70:				; CODE XREF: mod_readfile_11F4E+82j
		push	cx
		cmp	dword [di+20h], 0
		jz	short loc_11FCB
		mov	BYTE [byte_24675], 1
		mov	al, [di+3Fh]
		mov	[byte_24674], al
		push	di
		call	ems_realloc2
		pop	di
		jb	short loc_11FD4
		mov	[di+30h], ax
		mov	[di+32h], cx
		mov	es, ax
		test	WORD [moduleflag_246D0], 10111011000b
		jz	short loc_11FA9
		mov	dx, [di+38h]
		mov	cx, [di+3Ah]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file

loc_11FA9:				; CODE XREF: mod_readfile_11F4E+4Aj
		mov	bx, [fhandle_module]
		mov	ecx, [di+20h]
		push	di
		push	es
		mov	dx, [di+32h]
		call	mod_readfile_12247
		adc	WORD [word_24662], 0
		pop	es
		pop	di
		mov	ax, es
		push	di
		call	ems_mapmemx
		pop	di
		or	byte [di+3Ch], 1

loc_11FCB:				; CODE XREF: mod_readfile_11F4E+28j
		add	di, 40h	; '@'
		pop	cx
		dec	cx
		jnz	short loc_11F70

loc_11FD2:				; CODE XREF: mod_readfile_11F4E+19j
		clc

locret_11FD3:				; CODE XREF: mod_readfile_11F4E+Bj
		retn
; ---------------------------------------------------------------------------

loc_11FD4:				; CODE XREF: mod_readfile_11F4E+3Aj
		pop	cx
		retn
; ---------------------------------------------------------------------------

loc_11FD6:				; CODE XREF: mod_readfile_11F4E+12j
		mov	eax, 10000h
		mov	cl, [dma_channel_0]
		call	alloc_dma_buf
		jb	locret_1221F
		mov	word [dma_buf_pointer+2], ax
		mov	word [dma_buf_pointer], 0
		mov	di, myout
		mov	cx, [word_245D2]

loc_11FF7:				; CODE XREF: mod_readfile_11F4E+1D9j
		push	cx
		cmp	dword [di+20h], 0
		jz	loc_12106
		inc	BYTE [byte_24617]
		mov	BYTE [byte_24675], 1
		mov	al, [di+3Fh]
		mov	[byte_24674], al
		test	WORD [moduleflag_246D0], 10111011000b
		jz	short loc_12027
		mov	dx, [di+38h]
		mov	cx, [di+3Ah]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file

loc_12027:				; CODE XREF: mod_readfile_11F4E+C8j
		test	byte [di+3Ch], 4
		jz	short loc_1206B
		mov	eax, [di+20h]
		add	eax, 1Fh
		and	al, 0E0h
		shr	eax, 2
		mov	bx, [word_24630]
		shl	bx, 2
		add	ax, bx
		jnb	short loc_12056
		and	WORD [word_24630], 0C000h
		add	WORD [word_24630], 4000h
		jb	loc_12117

loc_12056:				; CODE XREF: mod_readfile_11F4E+F6j
		mov	ax, [word_24630]
		mov	bx, ax
		and	bx, 0C000h
		and	ax, 3FFFh
		shr	ax, 1
		or	ax, bx		; CODE XREF: snd_initialze+13j

loc_12066:				; CODE XREF: snd_initialze+13j
		mov	[di+34h], ax
		jmp	short loc_12071
; ---------------------------------------------------------------------------

loc_1206B:				; CODE XREF: mod_readfile_11F4E+DDj
		mov	ax, [word_24630]
		mov	[di+34h], ax

loc_12071:				; CODE XREF: mod_readfile_11F4E+11Bj
		mov	ecx, [di+20h]

loc_12075:				; CODE XREF: mod_readfile_11F4E+174j
		cmp	ecx, 8000h
		jbe	short loc_120C4
		sub	ecx, 8000h
		push	ecx
		mov	cx, 8000h
		mov	bx, [fhandle_module]
		mov	ah, 3Fh	; '?'
		push	di
		push	ds
		lds	dx, [dma_buf_pointer]
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	ds
		pop	di
		adc	WORD [word_24662], 0
		les	si, [dma_buf_pointer]
		mov	cx, 8000h
		call	mod_sub_12220
		push	di

loc_120AA:
		mov	cx, 8000h
		mov	ax, [word_24630]
		call	nongravis_182E7
		xor	word [dma_buf_pointer], 8000h
		add	WORD [word_24630], 800h
		pop	di
		pop	ecx
		jmp	short loc_12075
; ---------------------------------------------------------------------------

loc_120C4:				; CODE XREF: mod_readfile_11F4E+12Ej
		jcxz loc_120E7
		mov	bx, [fhandle_module]
		mov	ah, 3Fh	; '?'
		push	di
		push	cx
		push	ds
		lds	dx, [dma_buf_pointer]
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	ds
		pop	cx
		pop	di
		push	di
		adc	WORD [word_24662], 0
		les	si, [dma_buf_pointer]
		push	cx
		call	mod_sub_12220
		pop	cx

loc_120E7:				; CODE XREF: mod_readfile_11F4E:loc_120C4j
		push	cx
		mov	ax, [word_24630]
		call	nongravis_182E7
		xor	word [dma_buf_pointer], 8000h
		pop	ax
		add	ax, 21h	; '!'
		and	al, 0E0h
		shr	ax, 4

loc_120FD:
		add	[word_24630], ax
		pop	di
		or	byte [di+3Ch], 1

loc_12106:				; CODE XREF: mod_readfile_11F4E+AFj
		pop	cx
		mov	dx, [word_24630]
		shr	dx, 1
		mov	al, [byte_24628]
		shl	ax, 0Dh
		cmp	dx, ax
		jbe	short loc_12123

loc_12117:				; CODE XREF: mod_readfile_11F4E+104j
		call	memfree_18A28
		mov	dx, aNotEnoughDramOn ; "Not enough DRAM on UltraSound\r\n"
		mov	ax, 0FFFDh
		jmp	lfreaderr
; ---------------------------------------------------------------------------

loc_12123:				; CODE XREF: mod_readfile_11F4E+1C7j
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_11FF7

loc_1212B:				; CODE XREF: mod_readfile_11F4E+1E2j
		cmp	BYTE [byte_2466E], 1
		jz	short loc_1212B
		call	memfree_18A28
		mov	di, myout
		mov	cx, [word_245D2]

loc_1213C:				; CODE XREF: mod_readfile_11F4E+2CCj
		test	byte [di+3Ch], 1
		jz	loc_12216
		push	cx
		xor	ax, ax
		test	byte [di+3Ch], 4
		jnz	short loc_121B9
		test	byte [di+3Ch], 8
		jz	short loc_1219E
		mov	edx, [di+24h]
		push	edi
		movzx	edi, word [di+34h]
		shl	edi, 4
		add	edi, edx
		inc	edi
		pop	edi
		mov	edx, [di+2Ch]
		push	edi
		movzx	edi, word [di+34h]
		shl	edi, 4
		add	edi, edx
		add	edi, 2
		pop	edi
		mov	edx, [di+24h]
		push	edi
		movzx	edi, word [di+34h]
		shl	edi, 4
		add	edi, edx
		pop	edi

loc_1219E:				; CODE XREF: mod_readfile_11F4E+203j
		mov	edx, [di+2Ch]
		push	edi
		movzx	edi, word [di+34h]
		shl	edi, 4
		add	edi, edx
		inc	edi
		pop	edi
		jmp	short loc_12215
; ---------------------------------------------------------------------------

loc_121B9:				; CODE XREF: mod_readfile_11F4E+1FDj
		test	byte [di+3Ch], 8
		jz	short loc_121EE
		mov	edx, [di+24h]
		test	byte [di+3Ch], 10h
		jz	short loc_121CD
		mov	edx, [di+2Ch]

loc_121CD:				; CODE XREF: mod_readfile_11F4E+279j
		push	edi
		mov	bx, [di+34h]
		movzx	edi, bx
		and	di, 1FFFh
		and	bx, 0C000h
		shr	bx, 1
		or	di, bx
		shl	edi, 4
		add	edi, edx
		pop	edi

loc_121EE:				; CODE XREF: mod_readfile_11F4E+26Fj
		mov	edx, [di+2Ch]
		push	edi
		mov	bx, [di+34h]
		movzx	edi, bx
		and	di, 1FFFh
		and	bx, 0C000h
		shr	bx, 1
		or	di, bx
		shl	edi, 4
		add	edi, edx
		inc	edi
		pop	edi

loc_12215:				; CODE XREF: mod_readfile_11F4E+269j
		pop	cx

loc_12216:				; CODE XREF: mod_readfile_11F4E+1F2j
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_1213C
		clc

locret_1221F:				; CODE XREF: mod_readfile_11F4E+95j
		retn


; =============== S U B	R O U T	I N E =======================================


mod_sub_12220:	; CODE XREF: mod_readfile_11F4E+158p
					; mod_readfile_11F4E+195p ...
		cmp	BYTE [byte_24674], 1
		jz	short loc_12228
		retn
; ---------------------------------------------------------------------------

loc_12228:				; CODE XREF: mod_sub_12220+5j
		mov	al, [byte_24676]
		cmp	BYTE [byte_24675], 0
		jz	short loc_12239
		mov	BYTE [byte_24675], 0
		xor	al, al

loc_12239:				; CODE XREF: mod_sub_12220+10j
					; mod_sub_12220+21j
		add	al, [es:si]
		mov	[es:si], al
		inc	si
		dec	cx
		jnz	short loc_12239
		mov	[byte_24676], al
		retn


; =============== S U B	R O U T	I N E =======================================


mod_readfile_12247:	; CODE XREF: mod_readfile_11F4E+68p
		mov	edi, ecx
		xor	esi, esi
		mov	bp, es

loc_1224F:				; CODE XREF: mod_readfile_12247+98j
		push	dx
		cmp	dx, 0FFFFh
		jz	short loc_12262
		push	dx
		push	cx
		push	bx
		push	ax
		mov	bx, dx
		call	ems_mapmem
		pop	ax
		pop	bx
		pop	cx
		pop	dx

loc_12262:				; CODE XREF: mod_readfile_12247+Cj
		xor	dx, dx
		mov	ecx, 8000h
		cmp	edi, ecx
		ja	short loc_12271
		mov	cx, di

loc_12271:				; CODE XREF: mod_readfile_12247+26j
		push	bx
		push	esi
		push	edi
		push	bp
		push	es
		push	ds
		mov	ds, bp
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	ds
		pushf
		push	ax
		or	ax, ax
		jz	short loc_122B8
		push	ax
		push	bp
		mov	es, bp
		xor	si, si
		mov	cx, ax
		call	mod_sub_12220
		pop	bp
		pop	ax
		cmp	BYTE [byte_24673], 0
		jz	short loc_122B8
		mov	fs, bp
		mov	cx, ax
		add	cx, 3
		shr	cx, 2
		jz	short loc_122B8
		mov	edx, 80808080h
		xor	si, si

loc_122AE:				; CODE XREF: mod_readfile_12247+6Fj
		xor	[fs:si], edx
		add	si, 4
		dec	cx
		jnz	short loc_122AE

loc_122B8:				; CODE XREF: mod_readfile_12247+3Dj
					; mod_readfile_12247+51j ...
		pop	ax
		popf
		pop	es
		pop	bp
		pop	edi
		pop	esi
		pop	bx
		pop	dx
		jb	short locret_122E7
		or	ax, ax
		jz	short loc_122E3
		movzx	eax, ax
		add	esi, eax
		cmp	dx, 0FFFFh
		jnz	short loc_122DA
		add	bp, 800h
		jmp	short loc_122DC
; ---------------------------------------------------------------------------

loc_122DA:				; CODE XREF: mod_readfile_12247+8Bj
		inc	dx
		inc	dx

loc_122DC:				; CODE XREF: mod_readfile_12247+91j
		sub	edi, eax
		ja	loc_1224F

loc_122E3:				; CODE XREF: mod_readfile_12247+7Fj
		mov	ecx, esi
		clc

locret_122E7:				; CODE XREF: mod_readfile_12247+7Bj
		retn


; =============== S U B	R O U T	I N E =======================================


ems_mapmemx:	; CODE XREF: mod_readfile_11F4E+75p
		test	byte [di+3Ch], 8
		jnz	loc_12386
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		mov	edx, [di+20h]
		add	edx, 800h
		cmp	word [di+32h], 0FFFFh
		jz	short loc_1234E
		push	eax
		push	ecx
		push	edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem
		pop	edx
		pop	ecx
		pop	eax
		push	eax
		push	ecx
		push	edx
		mov	ebx, edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem2
		pop	edx
		pop	ecx
		pop	eax
		and	ecx, 3FFFh
		and	edx, 3FFFh
		add	edx, 8000h

loc_1234E:				; CODE XREF: ems_mapmemx+20j
		mov	si, dx
		and	si, 0Fh
		shr	edx, 4
		add	dx, ax
		mov	fs, dx
		mov	di, cx
		and	di, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	es, cx
		mov	cx, 200h
		cld

loc_1236C:				; CODE XREF: ems_mapmemx+9Bj
		mov	eax, [es:di]
		mov	[fs:si], eax
		mov	dword [es:di], 0
		add	si, 4
		add	di, 4
		dec	cx
		jnz	short loc_1236C
		retn
; ---------------------------------------------------------------------------

loc_12386:				; CODE XREF: ems_mapmemx+4j
		push	ax
		push	di
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		cmp	word [di+32h], 0FFFFh
		jz	short loc_123B0
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem
		pop	eax
		pop	ecx
		and	ecx, 3FFFh

loc_123B0:				; CODE XREF: ems_mapmemx+ADj
		mov	si, cx
		and	si, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	fs, cx
		mov	ecx, [di+20h]
		add	ecx, 800h
		mov	ebx, ecx
		cmp	word [di+32h], 0FFFFh
		jz	short loc_123EE
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem2
		pop	eax
		pop	ecx
		and	ecx, 3FFFh
		add	cx, 8000h

loc_123EE:				; CODE XREF: ems_mapmemx+E7j
		mov	bx, cx
		and	bx, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	es, cx
		mov	di, bx
		mov	cx, 200h
		cld
		fs rep movsd
		pop	di
		pop	ax
		mov	ecx, [di+24h]
		mov	ebx, ecx
		cmp	word [di+32h], 0FFFFh
		jz	short loc_1242D
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem
		pop	eax
		pop	ecx
		and	ecx, 3FFFh

loc_1242D:				; CODE XREF: ems_mapmemx+12Aj
		mov	si, cx
		and	si, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	fs, cx
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		cmp	word [di+32h], 0FFFFh
		jz	short loc_12466
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem2
		pop	eax
		pop	ecx
		and	ecx, 3FFFh
		add	cx, 8000h

loc_12466:				; CODE XREF: ems_mapmemx+15Fj
		mov	bx, cx
		and	bx, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	es, cx
		cmp	dword [di+28h], 800h
		ja	short loc_12497
		mov	edx, [di+28h]
		add	dx, si
		mov	di, bx
		mov	bp, si
		mov	cx, 800h
		cld

loc_1248B:				; CODE XREF: ems_mapmemx+1ACj
		fs movsb
		cmp	si, dx
		jb	short loc_12493
		mov	si, bp

loc_12493:				; CODE XREF: ems_mapmemx+1A7j
		dec	cx
		jnz	short loc_1248B
		retn
; ---------------------------------------------------------------------------

loc_12497:				; CODE XREF: ems_mapmemx+193j
		mov	di, bx
		mov	cx, 200h
		cld
		fs rep movsd
		retn


; =============== S U B	R O U T	I N E =======================================


ems_mapmemy:
		test	byte [di+3Ch], 8
		jnz	loc_1253B
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		mov	edx, [di+20h]
		add	edx, 800h
		cmp	word [di+32h], 0FFFFh
		jz	short loc_12508
		push	eax
		push	ecx
		push	edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem
		pop	edx
		pop	ecx
		pop	eax
		push	eax
		push	ecx
		push	edx
		mov	ebx, edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem2
		pop	edx
		pop	ecx
		pop	eax
		and	ecx, 3FFFh
		and	edx, 3FFFh
		add	edx, 8000h

loc_12508:				; CODE XREF: ems_mapmemy+20j
		mov	si, dx
		and	si, 0Fh
		shr	edx, 4
		add	dx, ax
		mov	fs, dx
		mov	di, cx
		and	di, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	es, cx
		mov	cx, 200h
		xor	eax, eax
		cld

loc_12529:				; CODE XREF: ems_mapmemy+96j
		mov	eax, [fs:si]
		mov	[es:di], eax
		add	si, 4
		add	di, 4
		dec	cx
		jnz	short loc_12529
		retn
; ---------------------------------------------------------------------------

loc_1253B:				; CODE XREF: ems_mapmemy+4j
		mov	ecx, [di+20h]
		add	ecx, 800h
		mov	ebx, ecx
		cmp	word [di+32h], 0FFFFh
		jz	short loc_12568
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem
		pop	eax
		pop	ecx
		and	ecx, 3FFFh

loc_12568:				; CODE XREF: ems_mapmemy+ABj
		mov	si, cx
		and	si, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	fs, cx
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		cmp	word [di+32h], 0FFFFh
		jz	short loc_125A1
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	ems_mapmem2
		pop	eax
		pop	ecx
		and	ecx, 3FFFh
		add	cx, 8000h

loc_125A1:				; CODE XREF: ems_mapmemy+E0j
		mov	bx, cx
		and	bx, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	es, cx
		mov	di, bx
		mov	cx, 200h
		cld
		fs rep movsd
		retn


; =============== S U B	R O U T	I N E =======================================


deinit_125B9:	; CODE XREF: start:loc_1907CP
					; start+1BFP
		pushf
		push	ds
		mov	ax, seg003
		mov	ds, ax
		push	cs
		call	near snd_offx
		push	cs
		call	near memfree_125DA
		call	ems_deinit
		mov	ax, [word_2460C]
		call	setmemallocstrat
		call	snd_deinit
		call	initclockfromrtc
		pop	ds
		popf
		retf


; =============== S U B	R O U T	I N E =======================================


memfree_125DA:	; CODE XREF: moduleread+7p
					; moduleread+ADp ...
		push	ds
		mov	ax, seg003
		mov	ds, ax
		call	ems_realloc
		cmp	word [dword_24640+2], 0
		jz	short loc_125F6
		call	memfree_18A28
		mov	DWORD [dword_24640], 0

loc_125F6:				; CODE XREF: memfree_125DA+Ej
		cmp	BYTE [byte_24665], 1
		jnz	short loc_1265B
		test	BYTE [sndflags_24622], 4
		jnz	short loc_1263D
		test	BYTE [sndflags_24622], 10h
		jnz	short loc_1263D
		mov	di, myout
		mov	cx, [word_245D2]

loc_12612:				; CODE XREF: memfree_125DA+61j
		push	cx
		test	byte [di+3Ch], 1
		jz	short loc_12636
		cmp	word [di+32h], 0FFFFh
		jnz	short loc_12636
		cmp	word [di+30h], 0
		jz	short loc_12636
		mov	ax, [di+30h]
		push	di
		call	memfree
		pop	di
		and	byte [di+3Ch], 0FEh
		mov	word [di+30h], 0

loc_12636:				; CODE XREF: memfree_125DA+3Dj
					; memfree_125DA+43j ...
		pop	cx
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_12612

loc_1263D:				; CODE XREF: memfree_125DA+28j
					; memfree_125DA+2Fj
		mov	di, segs_table
		mov	cx, [word_245F2]

loc_12644:				; CODE XREF: memfree_125DA+7Fj
		mov	ax, [di]
		or	ax, ax
		jz	short loc_12655
		push	cx
		push	di
		call	memfree
		pop	di
		pop	cx
		mov	word [di], 0

loc_12655:				; CODE XREF: memfree_125DA+6Ej
		add	di, 2
		dec	cx
		jnz	short loc_12644

loc_1265B:				; CODE XREF: memfree_125DA+21j
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


sub_1265D:		; CODE XREF: read_module+86P
					; keyb_19EFDP ...
		mov	ax, seg003
		mov	es, ax
		mov	ax, [es:volume_245FC]
		dec	ax
		mov	cl, al
		mov	si, volume_25908
		mov	di, asc_246B0 ; "				"
		movzx	bp, BYTE [es:sndcard_type]
		mov	ch, [es:byte_24666]
		mov	bh, [es:byte_24667]
		mov	dl, [es:sndflags_24622]
		mov	dh, [es:byte_24628]
		dec	dh
		and	dh, 3
		shl	dh, 1
		or	dh, [es:byte_24623]
		shl	dh, 1
		or	dh, [es:byte_24671]
		shl	dh, 3
		mov	al, byte [es:word_245F6]
		mov	ah, byte [es:word_245F0]
		retf


; =============== S U B	R O U T	I N E =======================================


sub_126A9:		; CODE XREF: read_module+6AP
					; text_init2+225P
		mov	ax, seg003
		mov	es, ax
		mov	di, asc_246B0 ; "				"
		mov	si, myout
		mov	bl, byte [es:word_245FA]
		mov	bh, byte [es:word_245D2]
		mov	cl, byte [es:word_245D4]
		mov	ch, [es:byte_24617]
		mov	eax, [es:module_type_text]
		retf


; =============== S U B	R O U T	I N E =======================================


volume_prep:		; CODE XREF: seg001:18BEP
					; f2_draw_waves+CP ...
		push	ds
		mov	bx, seg003
		mov	ds, bx
		mov	[word_24610], ax
		mov	[my_size], cx
		test	BYTE [sndflags_24622], 4
		jnz	short loc_12702
		push	di
		push	es
		call	ems_save_mapctx
		pop	es
		pop	di
		mov	si, volume_25908
		mov	dx, [word_245D4]

loc_126F0:				; CODE XREF: volume_prep+2Dj
		push	dx
		push	si
		call	volume_prepare_waves
		pop	si
		pop	dx
		add	si, 50h	; 'P'
		dec	dx
		jnz	short loc_126F0
		call	ems_restore_mapctx
		pop	ds
		retf
; ---------------------------------------------------------------------------

loc_12702:				; CODE XREF: volume_prep+12j
		push	di
		push	es
		cmp	word [dword_24640+2], 0
		jnz	short loc_12721
		mov	eax, 800h
		mov	cl, [dma_channel_0]
		call	alloc_dma_buf
		mov	word [dword_24640+2], ax
		mov	word [dword_24640],	0

loc_12721:				; CODE XREF: volume_prep+3Bj
		mov	ax, ds
		mov	es, ax
		cld
		mov	si, volume_25908
		mov	cx, [word_245D4]

loc_1272D:				; CODE XREF: volume_prep+87j
		pushf
		cli
		mov	dx, [gravis_port]
		dec	dx
		mov	al, [si+18h]
		out	dx, al
		inc	dx
		mov	al, 8Ah	; 'ä'
		out	dx, al
		inc	dx
		in	ax, dx
		dec	dx
		and	ah, 1Fh
		shl	eax, 10h
		mov	al, 8Bh	; 'ã'
		out	dx, al
		inc	dx
		in	ax, dx
		dec	dx
		popf
		mov	[si+4],	eax
		add	si, 50h	; 'P'
		dec	cx
		jnz	short loc_1272D
		pop	es
		pop	di
		mov	si, volume_25908
		mov	ax, [word_245D4]

loc_1275F:				; CODE XREF: volume_prep+C8j
		push	ax
		push	si
		test	byte [si+17h], 1
		jnz	short loc_1276C
		call	memclean
		jmp	short loc_1278F
; ---------------------------------------------------------------------------

loc_1276C:				; CODE XREF: volume_prep+97j
					; volume_prep+A3j
		cmp	BYTE [byte_2466E], 1
		jz	short loc_1276C
		push	si
		push	di
		push	es
		mov	eax, [dword_24640]
		call	sub_1279A
		pop	es
		pop	di
		pop	si

loc_12780:				; CODE XREF: volume_prep+B7j
		cmp	BYTE [byte_2466E], 1
		jz	short loc_12780
		lfs	ax, [dword_24640]
		call	sub_1281A

loc_1278F:				; CODE XREF: volume_prep+9Cj
		pop	si
		pop	ax
		add	si, 50h	; 'P'
		dec	al
		jnz	short loc_1275F
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


sub_1279A:		; CODE XREF: volume_prep+ACp
		mov	[dma_buf_pointer], eax
		mov	ax, [word_24610]
		xor	ah, ah
		imul	ax, [si+20h]
		mul	WORD [my_size]
		shrd	ax, dx,	8
		add	ax, 30h	; '0'
		test	WORD [word_24610], 8000h
		jz	short loc_127BD
		add	ax, 100h

loc_127BD:				; CODE XREF: sub_1279A+1Ej
		test	byte [si+19h], 4
		setnz	cl
		shl	ax, cl
		cmp	ax, 800h
		jb	short loc_127CE
		mov	ax, 800h

loc_127CE:				; CODE XREF: sub_1279A+2Fj
		mov	cx, ax
		mov	eax, [si+4]
		shr	eax, 0Dh
		and	al, 0FEh
		test	byte [si+19h], 4
		jz	sub_182DB
		mov	eax, [si+4]
		shr	eax, 0Dh
		mov	dx, ax
		and	dx, 0C000h
		and	ax, 1FFFh
		shl	ax, 1
		or	ax, dx
		push	cx
		call	sub_182DB
		pop	cx

loc_127FC:				; CODE XREF: sub_1279A+67j
		cmp	BYTE [byte_2466E], 1
		jz	short loc_127FC
		shr	cx, 1
		push	ds
		lds	di, [dma_buf_pointer]
		lea	bx, [di+1]

loc_1280D:				; CODE XREF: sub_1279A+7Cj
		mov	al, [bx]
		mov	[di], al
		add	bx, 2
		inc	di
		dec	cx
		jnz	short loc_1280D
		pop	ds
		retn


; =============== S U B	R O U T	I N E =======================================


sub_1281A:		; CODE XREF: volume_prep+BEp
		shl	eax, 10h
		mov	ax, [word_24610]
		xor	ah, ah
		mul	word [si+20h]
		mov	bp, ax
		shr	bp, 8
		mov	dh, al
		xor	dl, dl
		shr	eax, 10h
		jmp	short loc_12898


; =============== S U B	R O U T	I N E =======================================


volume_prepare_waves: ; CODE XREF: volume_prep+24p
		test	byte [si+17h], 1
		jz	memclean
		test	BYTE [sndflags_24622], 1
		jz	memclean
		push	di
		push	es
		mov	bx, [si+26h]
		mov	eax, [si+4]
		shr	eax, 22
		add	bx, ax
		push	si
		call	ems_mapmem
		pop	si
		mov	eax, [si+4]
		mov	bx, ax
		shr	eax, 12
		cmp	word [si+26h], 0FFFFh
		jz	short loc_12870
		and	eax, 3FFh

loc_12870:				; CODE XREF: volume_prepare_waves+33j
		add	ax, [si+24h]
		mov	fs, ax
		mov	ax, [word_24610]
		xor	ah, ah
		mul	word [si+20h]
		mul	WORD [freq1]
		mov	bp, 22050
		div	bp
		mov	dx, ax
		movzx	ax, bh
		and	al, 0Fh
		mov	bp, dx
		shr	bp, 8
		mov	dh, dl
		mov	dl, bl
		pop	es
		pop	di

loc_12898:				; CODE XREF: sub_1281A+19j
		movzx	ebx, byte [si+23h]
		mov	si, ax
		test	WORD [word_24610], 4000h
		jz	short loc_128BB
		cmp	WORD [amplification], 120
		jbe	short loc_128BB
		mov	ax, 100
		push	dx
		mul	bx
		div	WORD [amplification]
		pop	dx
		mov	bx, ax

loc_128BB:				; CODE XREF: volume_prepare_waves+70j
					; volume_prepare_waves+77j
		shl	ebx, 9
		add	bx, vlm_byte_table
		inc	bx
		mov	cx, [my_size]
		test	WORD [word_24610], 8000h
		jz	short loc_1291E
		shl	ecx, 16
		shl	esi, 16
		mov	si, ax
		mov	cx, 100h

loc_128DD:				; CODE XREF: volume_prepare_waves+DFj
		mov	eax, [fs:si]
		inc	si
		or	al, al
		jns	short loc_12913
		or	ah, ah
		js	short loc_12913
		ror	eax, 8
		cmp	al, ah
		jg	short loc_12913
		ror	eax, 8
		cmp	al, ah
		jg	short loc_12913
		rol	eax, 16
		mov	ax, [fs:si+3]
		rol	eax, 8
		cmp	al, ah
		jg	short loc_12913
		ror	eax, 8
		inc	si
		cmp	al, ah
		jle	short loc_1291A

loc_12913:				; CODE XREF: volume_prepare_waves+AFj
					; volume_prepare_waves+B3j ...
		dec	cx
		jnz	short loc_128DD
		shr	esi, 16

loc_1291A:				; CODE XREF: volume_prepare_waves+DCj
		shr	ecx, 16

loc_1291E:				; CODE XREF: volume_prepare_waves+99j
		xor	eax, eax

loc_12921:				; CODE XREF: volume_prepare_waves+21Cj
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	short locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	short locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	short locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	short locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	short locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jz	short locret_12A55
		mov	al, [fs:si]
		mov	al, [ebx+eax*2]
		mov	[es:di], al
		add	dl, dh
		inc	di
		adc	si, bp
		dec	cx
		jnz	loc_12921

locret_12A55:				; CODE XREF: volume_prepare_waves+FCj
					; volume_prepare_waves+110j ...
		retn


; =============== S U B	R O U T	I N E =======================================


memclean:		; CODE XREF: volume_prep+99p
					; volume_prepare_waves+4j ...
		cld
		mov	cx, [my_size]
		xor	ax, ax
		shr	cx, 1
		rep stosw
		adc	cx, cx
		rep stosb
		retn


; =============== S U B	R O U T	I N E =======================================


volume_12A66:	; CODE XREF: vlm_141DF+1p snd_off+14p
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	cx, [word_245D4]
		mov	bx, volume_25908

loc_12A73:				; CODE XREF: volume_12A66+19j
		push	bx
		push	cx
		call	WORD [off_245CE]
		pop	cx
		pop	bx
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_12A73
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


change_volume:	; CODE XREF: keyb_19EFD+17P
					; keyb_19EFD+23AP ...
		push	ds
		mov	cx, seg003
		mov	ds, cx
		cmp	ax, -1
		jz	short loc_12AA9
		mov	[volume_245FC],	ax
		mov	cx, [word_245D4]
		mov	bx, volume_25908

loc_12A98:				; CODE XREF: change_volume+24j
		push	bx
		push	cx
		mov	al, [bx+8]
		call	WORD [off_245CC]
		pop	cx
		pop	bx
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_12A98

loc_12AA9:				; CODE XREF: change_volume+9j
		mov	ax, [volume_245FC]
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


change_amplif:	; CODE XREF: s3m_module+84p
					; eff_14020+9p	...
		push	ds
		mov	cx, seg003
		mov	ds, cx
		cmp	ax, -1
		jz	short loc_12ACE
		mov	[amplification], ax
		mov	BYTE [byte_24625], 0
		cmp	ax, 100
		jbe	short loc_12ACB
		mov	BYTE [byte_24625], 1

loc_12ACB:				; CODE XREF: change_amplif+16j
		call	sub_13044

loc_12ACE:				; CODE XREF: change_amplif+9j
		mov	ax, [amplification]
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


get_playsettings:	; CODE XREF: keyb_19EFD+2AP
					; keyb_19EFD+350P ...
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	al, [flag_playsetttings]
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


set_playsettings:	; CODE XREF: keyb_19EFD+357P
					; keyb_19EFD+36FP ...
		push	ds
		mov	bx, seg003
		mov	ds, bx
		mov	[flag_playsetttings], al
		call	someplaymode
		and	byte [config_word+1], 0FEh
		test	BYTE [flag_playsetttings], 10h
		jz	short loc_12AFB
		or	byte [config_word+1], 1

loc_12AFB:				; CODE XREF: set_playsettings+16j
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


sub_12AFD:		; CODE XREF: keyb_19EFD+1F9P
		push	ds
		mov	bx, seg003
		mov	ds, bx
		movzx	bx, ch
		cmp	bx, [word_245D4]
		jnb	short loc_12B16
		imul	bx, 80
		add	bx, volume_25908
		call	eff_13A43

loc_12B16:				; CODE XREF: sub_12AFD+Dj
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


sub_12B18:		; CODE XREF: moduleread:loc_10092p
					; sub_12EBA+5Fp
		push	ax
		push	ds
		push	es
		mov	ax, seg003
		mov	es, ax
		mov	di, dword_27BC8
		mov	cx, 8
		cld
		rep movsd
		mov	ds, ax
		mov	BYTE [byte_2461C], 0
		mov	BYTE [byte_2461D], 0
		mov	si, dword_27BC8
		mov	bx, volume_25908
		mov	cx, [word_245D4]
		xor	al, al

loc_12B42:				; CODE XREF: sub_12B18+65j
		push	ax
		mov	[bx+18h], al
		mov	al, [si]
		mov	[bx+3Ah], al
		test	BYTE [sndflags_24622], 4
		jnz	short loc_12B5F
		cmp	al, 40h	; '@'
		mov	al, 0
		jb	short loc_12B5A
		mov	al, 80h	; 'Ä'

loc_12B5A:				; CODE XREF: sub_12B18+3Ej
		mov	[bx+3Ah], al
		jmp	short loc_12B62
; ---------------------------------------------------------------------------

loc_12B5F:				; CODE XREF: sub_12B18+38j

loc_12B62:				; CODE XREF: sub_12B18+45j
		mov	al, [bx+3Ah]
		cmp	al, 0
		jz	short loc_12B71
		inc	BYTE [byte_2461D]
		cmp	al, 80h	; 'Ä'
		jz	short loc_12B75

loc_12B71:				; CODE XREF: sub_12B18+4Fj
		inc	BYTE [byte_2461C]

loc_12B75:				; CODE XREF: sub_12B18+57j
		pop	ax
		add	bx, 80
		inc	si
		inc	al
		dec	cx
		jnz	short loc_12B42
		pop	es
		pop	ds
		pop	ax
		retf


; =============== S U B	R O U T	I N E =======================================


sub_12B83:		; CODE XREF: moduleread+8Bp
		push	ax
		push	ds
		mov	bx, seg003
		mov	ds, bx
		xor	ah, ah
		cmp	al, 20h	; ' '
		jb	short loc_12B92
		mov	al, 20h	; ' '

loc_12B92:				; CODE XREF: sub_12B83+Bj
		cmp	al, 2
		ja	short loc_12B98
		mov	al, 2

loc_12B98:				; CODE XREF: sub_12B83+11j
		mov	[word_245D4], ax
		mov	di, volume_25908
		mov	cx, [word_245D4]
		xor	dx, dx
		xor	bx, bx

loc_12BA6:				; CODE XREF: sub_12B83+4Cj
		cmp	byte [di+1Dh], 0
		jnz	short loc_12BB3
		mov	[di+18h], dl
		inc	dl
		jmp	short loc_12BCB
; ---------------------------------------------------------------------------

loc_12BB3:				; CODE XREF: sub_12B83+27j
		cmp	byte [di+1Dh], 1
		jnz	short loc_12BC0
		mov	[di+18h], dh
		inc	dh
		jmp	short loc_12BCB
; ---------------------------------------------------------------------------

loc_12BC0:				; CODE XREF: sub_12B83+34j
		cmp	byte [di+1Dh], 2
		jnz	short loc_12BCB
		mov	[di+18h], bl
		inc	bl

loc_12BCB:				; CODE XREF: sub_12B83+2Ej
					; sub_12B83+3Bj ...
		add	di, 80
		dec	cx
		jnz	short loc_12BA6
		xor	ah, ah
		mov	al, dl
		mov	[word_245D6], ax
		mov	al, dh
		mov	[word_245D8], ax
		mov	al, bl
		mov	[word_245DA], ax
		test	BYTE [sndflags_24622], 4
		jz	short loc_12BEF
		mov	ax, [word_245D6]

loc_12BEF:				; CODE XREF: sub_12B83+64j
		call	sub_13044
		call	someplaymode
		pop	ds
		pop	ax
		retf


; =============== S U B	R O U T	I N E =======================================


someplaymode:	; CODE XREF: set_playsettings+9p
					; sub_12B83+6Fp
		mov	edx, 3
		mov	eax, 1775763456
		mov	ecx, 369D800h
		cmp	BYTE [byte_2461A], 0
		jnz	short loc_12C3C
		mov	edx, 3
		mov	eax, 1643177984
		mov	ecx, 361F0F0h
		test	BYTE [flag_playsetttings], 8
		jnz	short loc_12C3C
		mov	edx, 3
		mov	eax, 1776914432
		mov	ecx, 369E990h

loc_12C3C:				; CODE XREF: someplaymode+17j
					; someplaymode+30j
		mov	[dword_245C0], ecx
		movzx	edi, WORD [freq1]
		mov	cl, [byte_2461A]
		shl	edi, cl
		div	edi
		mov	[dword_245BC], eax
		test	BYTE [sndflags_24622], 4
		jz	short loc_12C86
		movzx	ecx, BYTE [byte_24629]
		mov	eax, 385532977
		test	BYTE [flag_playsetttings], 8
		jnz	short loc_12C75
		mov	eax, 389081954

loc_12C75:				; CODE XREF: someplaymode+75j
		mul	ecx
		mov	cl, 12
		add	cl, [byte_2461A]
		shrd	eax, edx, cl
		mov	[dword_2463C], eax

loc_12C86:				; CODE XREF: someplaymode+62j
		mov	di, volume_25908
		mov	cx, [word_245D4]
		xor	ax, ax

loc_12C8F:				; CODE XREF: someplaymode+9Ej
		mov	[di+3Eh], ax
		add	di, 50h	; 'P'
		dec	cx
		jnz	short loc_12C8F
		retn


; =============== S U B	R O U T	I N E =======================================


getset_playstate:	; CODE XREF: keyb_19EFD+401P
					; keyb_19EFD:loc_1A30DP ...
		push	bx
		push	ds
		mov	bx, seg003
		mov	ds, bx
		cmp	al, 0FFh
		jz	short loc_12CA7
		mov	[play_state], al

loc_12CA7:				; CODE XREF: getset_playstate+9j
		mov	al, [play_state]
		pop	ds
		pop	bx
		retf


; =============== S U B	R O U T	I N E =======================================


sub_12CAD:		; CODE XREF: keyb_19EFD+3CCP
					; keyb_19EFD+3DCP ...
		push	ds
		push	es
		mov	ax, seg003
		mov	ds, ax
		mov	es, ax
		mov	si, word_246A6
		mov	al, ch
		or	al, 0E0h
		mov	[word_246A9], bx
		mov	[byte_246A8], cl
		mov	[word_246A6], dx
		call	sub_13623
		pop	es
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


read_sndsettings:	; CODE XREF: read_module+7DP
					; callsubx+3DP
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	al, [sndcard_type]
		mov	dx, [snd_base_port]
		mov	cl, [irq_number]
		mov	ch, [dma_channel]
		mov	ah, [freq_246D7]
		mov	bl, [byte_246D8]
		mov	bh, [byte_246D9]
		mov	bp, [freq1]
		test	BYTE [sndflags_24622], 4
		jz	short loc_12CFF
		mov	bp, [freq2]

loc_12CFF:				; CODE XREF: read_sndsettings+2Aj
		mov	si, [config_word]
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


sub_12D05:		; CODE XREF: start-2DP	start+285P
		push	ds
		push	di
		push	es
		mov	ax, seg003
		mov	ds, ax
		mov	si, aDeviceNotIniti ; "Device not initialised!"
		cmp	BYTE [snd_init], 1
		jnz	short loc_12D2E
		movzx	si, BYTE [sndcard_type]
		shl	si, 1
		mov	si, sb16_txt
		mov	di, chrin
		call	myasmsprintf
		mov	byte [di], 0
		mov	si, chrin

loc_12D2E:				; CODE XREF: sub_12D05+10j
		pop	es
		pop	di

loc_12D30:
		call	strcpy_count_0
		pop	ds
		retf


; =============== S U B	R O U T	I N E =======================================


sub_12D35:		; CODE XREF: dosexec+5CP dosexec+8BP
		push	ax
		push	bx
		push	ds
		mov	bx, seg003
		mov	ds, bx
		cmp	al, 1
		jz	short loc_12D4E

loc_12D41:
		mov	BYTE [cs:byte_14F71], 0
		call	setmemalloc1
		pop	ds
		pop	bx
		pop	ax
		retf
; ---------------------------------------------------------------------------

loc_12D4E:				; CODE XREF: sub_12D35+Aj
		mov	BYTE [cs:byte_14F71], 1
		mov	ax, [word_2460C]
		call	setmemallocstrat
		call	initclockfromrtc
		pop	ds
		pop	bx
		pop	ax
		retf


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


sub_12DA8:		; CODE XREF: callsubx+24P
		pushf
		cli
		push	ds
		mov	bp, seg003
		mov	ds, bp
		mov	[sndcard_type],	al
		mov	[snd_base_port], dx
		mov	[irq_number], cl
		mov	[dma_channel], ch
		mov	[freq_246D7], ah
		mov	[byte_246D8], bl
		mov	[byte_246D9], bh
		movzx	ax, ah
		imul	ax, 1000
		mov	[freq1], ax
		mov	[config_word], si
		mov	ax, di
		mov	BYTE [byte_246DC], 4Bh ; 'K'
		mov	WORD [off_245CA], sub_13177
		mov	WORD [off_245C8], sub_13429
		mov	WORD [off_245CC], sub_131EF
		mov	WORD [off_245CE], sub_131DA
		mov	BYTE [byte_24623], 0
		mov	BYTE [bit_mode], 8
		mov	WORD [word_245E8], 400h
		mov	BYTE [snd_set_flag],	0
		mov	al, 8
		call	getint_vect
		mov	word [cs:int8addr],	bx
		mov	word [cs:int8addr+2], dx
		push	cs
		call	near clean_11C43
		call	snd_initialze
		jb	loc_12EB2
		call	getmemallocstrat
		mov	[word_2460C], ax
		call	setmemalloc1
		mov	al, [byte_246DC]
		mov	ah, al
		and	ax, 0F00Fh
		shr	ah, 4
		movzx	di, al
		mov	al, [cs:byte_13C54+di]
		movzx	di, ah
		mov	ah, [cs:byte_13C54+di]
		test	BYTE [sndflags_24622], 4
		jnz	short loc_12E55
		mov	ax, 80h	; 'Ä'

loc_12E55:				; CODE XREF: sub_12DA8+A8j
		mov	[byte_2461E], ah
		mov	[byte_2461F], al
		push	cs
		call	near clean_11C43
		mov	al, 0
		test	byte [config_word+1], 1
		jz	short loc_12E6B
		or	al, 10h

loc_12E6B:				; CODE XREF: sub_12DA8+BFj
		test	byte [config_word],	4
		jz	short loc_12E74
		or	al, 4

loc_12E74:				; CODE XREF: sub_12DA8+C8j
		test	byte [config_word],	80h
		jz	short loc_12E7D
		or	al, 8

loc_12E7D:				; CODE XREF: sub_12DA8+D1j
		mov	[flag_playsetttings], al
		mov	ax, 400h
		mov	cl, [byte_24623]
		and	cl, 1
		cmp	BYTE [bit_mode], 16
		jnz	short loc_12E9F
		mov	WORD [off_245E0], myin
		mov	WORD [off_245E2], chrin
		inc	cl

loc_12E9F:				; CODE XREF: sub_12DA8+E7j
		shr	ax, cl
		mov	[word_245E8], ax
		test	BYTE [sndflags_24622], 1
		jz	short loc_12EAE
		call	ems_init

loc_12EAE:				; CODE XREF: sub_12DA8+101j
		pop	ds
		popf
		clc
		retf
; ---------------------------------------------------------------------------

loc_12EB2:				; CODE XREF: sub_12DA8+7Bj
		mov	bx, ds
		mov	fs, bx
		pop	ds
		popf
		stc
		retf


; =============== S U B	R O U T	I N E =======================================


sub_12EBA:		; CODE XREF: read_module+E3P
		pushf
		cli
		push	ds
		push	es
		mov	ax, seg003
		mov	ds, ax
		mov	BYTE [byte_24669], 0
		mov	BYTE [byte_2466A], 0
		mov	BYTE [byte_2466B], 0
		mov	BYTE [byte_2466C], 0
		mov	BYTE [byte_2466D], 0
		mov	BYTE [byte_24671], 0
		mov	BYTE [play_state], 0
		mov	WORD [word_24600], 0
		mov	WORD [word_24602], 0
		mov	BYTE [byte_24620], 0
		mov	BYTE [byte_24621], 0
		mov	ax, ds
		mov	es, ax
		mov	di, volume_25908
		xor	eax, eax
		mov	cx, 280h
		cld
		rep stosd
		xor	ax, ax
		xor	bx, bx
		push	cs
		call	near sub_12F56
		mov	si, dword_27BC8
		push	cs
		call	near sub_12B18
		mov	al, [byte_2467A]
		call	sub_13CF6
		mov	al, [byte_24679]
		call	eff_13CE8
		mov	al, [byte_24679]
		mov	[byte_24668], al
		movzx	ax, BYTE [byte_2467A]
		shl	ax, 1
		mov	dl, 5
		div	dl
		mov	[byte_2467B], al
		mov	BYTE [byte_2467C], 0
		call	snd_on
		pop	es
		pop	ds
		popf
		retf


; =============== S U B	R O U T	I N E =======================================


snd_offx:		; CODE XREF: moduleread+3p
					; deinit_125B9+8p ...
		pushf
		cli
		push	ds
		mov	ax, seg003
		mov	ds, ax
		call	snd_off
		pop	ds
		popf
		retf


; =============== S U B	R O U T	I N E =======================================


sub_12F56:		; CODE XREF: sub_12EBA+58p
					; keyb_19EFD+167P ...
		pushf
		cli
		push	ds
		push	es
		mov	cx, seg003
		mov	ds, cx
		mov	[word_245F0], ax
		mov	[byte_24669], bl
		push	bx
		call	sub_1415E
		pop	bx
		cmp	bh, 1
		jnz	short loc_12F78
		mov	BYTE [byte_24668], 0
		call	sub_135CA

loc_12F78:				; CODE XREF: sub_12F56+18j
		pop	es
		pop	ds
		popf
		retf


; =============== S U B	R O U T	I N E =======================================


get_12F7C:		; CODE XREF: keyb_19EFD+148P
					; keyb_19EFD+174P
		pushf
		cli
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	ax, [word_245F0]
		mov	bx, [word_245F6]
		pop	ds
		popf
		retf


; =============== S U B	R O U T	I N E =======================================


set_timer_int:	; CODE XREF: covox_init+2Dp
					; stereo_init+30p ...
		mov	ebx, 1000h	; bytes
		push	dx		; dx = subrouting offset
		call	memalloc
		pop	dx
		jb	short locret_12FB3
		mov	word [dma_buf_pointer], 0
		mov	word [dma_buf_pointer+2], ax
		push	ax
		push	dx
		call	memfill8080
		pop	bx
		mov	dx, cs
		mov	al, 8
		call	setint_vect
		pop	ax
		clc

locret_12FB3:				; CODE XREF: set_timer_int+Bj
		retn


; =============== S U B	R O U T	I N E =======================================


clean_int8_mem_timr: ; CODE	XREF: covox_cleanp
					; stereo_cleanp ...
		mov	dx, word [cs:int8addr+2]
		mov	bx, word [cs:int8addr]
		mov	al, 8
		call	setint_vect
		call	clean_timer
		mov	ax, word [dma_buf_pointer+2]
		call	memfree
		retn


; =============== S U B	R O U T	I N E =======================================


configure_timer:	; CODE XREF: covox_setp stereo_setp ...
		call	sub_13017
		pushf
		cli
		mov	dx, 12h
		mov	ax, 34DCh
		div	WORD [freq1]
		call	set_timer
		mov	BYTE [cs:byte_14F70], 1
		mov	ax, [word_245E4]
		mov	[cs:word_14F6C], ax
		popf
		retn


; =============== S U B	R O U T	I N E =======================================


memfill8080:	; CODE XREF: set_timer_int+18p
					; covox_sndoffp ...
		pushf
		cli
		xor	ax, ax
		call	set_timer
		mov	BYTE [cs:byte_14F70], 0
		mov	WORD [cs:word_14F6C], 1
		mov	es, word [dma_buf_pointer+2]
		xor	di, di
		mov	cx, 400h
		mov	eax, 80808080h
		cld
		rep stosd
		popf
		retn


; =============== S U B	R O U T	I N E =======================================


sub_13017:		; CODE XREF: configure_timerp
					; proaud_setp ...
		mov	di, myout
		mov	cx, [word_245D2]

loc_1301E:				; CODE XREF: sub_13017+19j
		test	byte [di+3Ch], 8
		jnz	short loc_1302C
		mov	eax, [di+2Ch]
		mov	[di+24h], eax

loc_1302C:				; CODE XREF: sub_13017+Bj
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_1301E
		mov	WORD [word_24600], 0

loc_13038:				; CODE XREF: sub_13017+2Aj
		call	sub_16C69
		cmp	WORD [word_24600], 800h
		jbe	short loc_13038
		retn


; =============== S U B	R O U T	I N E =======================================


sub_13044:		; CODE XREF: change_amplif:loc_12ACBp
					; sub_12B83:loc_12BEFp
		mov	al, [byte_2467E]
		cmp	al, 0
		jz	short loc_13080
		cmp	al, 1
		jz	short loc_1305A
		cmp	al, 2
		jz	short loc_1306D
		mov	BYTE [byte_2467E], 0
		jmp	short loc_13080
; ---------------------------------------------------------------------------

loc_1305A:				; CODE XREF: sub_13044+9j
		mov	BYTE [byte_2467D], 3Fh ; '?'
		mov	WORD [off_2462E], table_24798
		mov	WORD [off_24656], table_25221
		jmp	short loc_13091
; ---------------------------------------------------------------------------

loc_1306D:				; CODE XREF: sub_13044+Dj
		mov	BYTE [byte_2467D], 3Fh ; '?'
		mov	WORD [off_2462E], table_24818
		mov	WORD [off_24656], table_25261
		jmp	short loc_13091
; ---------------------------------------------------------------------------

loc_13080:				; CODE XREF: sub_13044+5j
					; sub_13044+14j
		mov	BYTE [byte_2467D], 40h ; '@'
		mov	WORD [off_2462E], table_24716
		mov	WORD [off_24656], table_251E0

loc_13091:				; CODE XREF: sub_13044+27j
					; sub_13044+3Aj
		mov	di, vlm_byte_table
		movzx	eax, WORD [word_245D6]
		cmp	ax, 2
		ja	short loc_130A2
		mov	ax, 2

loc_130A2:				; CODE XREF: sub_13044+59j
		cmp	BYTE [byte_24623], 1
		jnz	short loc_130AE
		shr	ax, 1
		adc	ax, 0

loc_130AE:				; CODE XREF: sub_13044+63j
		movzx	ebp, ax
		mov	si, [off_24656]
		movzx	cx, BYTE [byte_2467D]
		inc	cx

loc_130BC:				; CODE XREF: sub_13044+122j
		push	cx
		push	ebp
		movzx	eax, byte [si]
		inc	si
		movzx	edx, WORD [amplification]
		shl	edx, 16
		mul	edx
		mov	ecx, 100
		div	ecx
		xor	edx, edx
		div	ebp
		mov	bp, ax
		shr	eax, 16
		mov	ecx, eax
		cmp	BYTE [byte_24625], 1
		jz	short loc_13120
		xor	ax, ax
		xor	dx, dx
		mov	bl, 80h	; 'Ä'

loc_130F6:				; CODE XREF: sub_13044+BDj
		mov	[di], ax
		add	dx, bp
		adc	ax, cx
		add	di, 2
		dec	bl
		jnz	short loc_130F6
		add	di, 100h
		xor	ax, ax
		xor	dx, dx
		mov	bl, 80h	; 'Ä'

loc_1310D:				; CODE XREF: sub_13044+D4j
		sub	di, 2
		sub	dx, bp
		sbb	ax, cx
		mov	[di], ax
		dec	bl
		jnz	short loc_1310D
		add	di, 100h
		jmp	short loc_13162
; ---------------------------------------------------------------------------

loc_13120:				; CODE XREF: sub_13044+AAj
		xor	eax, eax
		xor	dx, dx
		mov	bl, 80h	; 'Ä'

loc_13127:				; CODE XREF: sub_13044+F7j
		cmp	eax, 7FFFh
		jg	short loc_1316B
		mov	[di], ax

loc_13131:				; CODE XREF: sub_13044+12Bj
		add	dx, bp
		adc	eax, ecx
		add	di, 2
		dec	bl
		jnz	short loc_13127
		add	di, 100h
		xor	eax, eax
		xor	dx, dx
		mov	bl, 80h	; 'Ä'

loc_13148:				; CODE XREF: sub_13044+118j
		sub	di, 2
		sub	dx, bp
		sbb	eax, ecx
		cmp	eax, 0FFFF8000h
		jl	short loc_13171
		mov	[di], ax

loc_1315A:				; CODE XREF: sub_13044+131j
		dec	bl
		jnz	short loc_13148
		add	di, 100h

loc_13162:				; CODE XREF: sub_13044+DAj
		pop	ebp
		pop	cx
		dec	cx
		jnz	loc_130BC
		retn
; ---------------------------------------------------------------------------

loc_1316B:				; CODE XREF: sub_13044+E9j
		mov	word [di], 7FFFh
		jmp	short loc_13131
; ---------------------------------------------------------------------------

loc_13171:				; CODE XREF: sub_13044+112j
		mov	word [di], 8000h
		jmp	short loc_1315A


; =============== S U B	R O U T	I N E =======================================


sub_13177:		; CODE XREF: sub_13429+4Ap
					; DATA XREF: sub_12DA8+38o
		or	ax, ax
		jz	short locret_131B2
		or	byte [bx+3Dh], 4
		cmp	byte [bx+1Dh], 1
		jz	short loc_131B3
		cmp	ax, [bx+3Eh]
		jz	short locret_131B2
		mov	[bx+3Eh], ax
		movzx	edi, ax
		xor	edx, edx
		mov	eax, [dword_245BC]
		div	edi
		mov	[bx+20h], ax
		mov	cl, [byte_2461A]
		shl	edi, cl
		xor	edx, edx
		mov	eax, [dword_245C0]
		div	edi
		mov	[bx+1Eh], ax

locret_131B2:				; CODE XREF: sub_13177+2j
					; sub_13177+11j
		retn
; ---------------------------------------------------------------------------

loc_131B3:				; CODE XREF: sub_13177+Cj
					; gravis_13215+Cj
		movzx	edi, ax
		xor	edx, edx
		mov	cl, [byte_2461A]
		shl	edi, cl
		xor	edx, edx
		mov	eax, [dword_245C0]
		div	edi
		mov	[bx+1Eh], ax
		retn


; =============== S U B	R O U T	I N E =======================================


nullsub_5:		; CODE XREF: sub_131DA+4j
					; gravis_13272+4j
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_131EF

loc_131D0:				; CODE XREF: sub_131EF+4j
					; gravis_132A9+4j ...
		xor	ah, ah
		imul	ax, [volume_245FC]
		xor	al, al
		retn
; END OF FUNCTION CHUNK	FOR sub_131EF

; =============== S U B	R O U T	I N E =======================================


sub_131DA:		; CODE XREF: sub_13429+74j
					; DATA XREF: sub_12DA8+4Ao
		cmp	byte [bx+1Dh], 1
		jz	short nullsub_5
		test	byte [bx+17h], 1
		jz	short locret_131EE
		and	byte [bx+17h], 0FEh
		mov	byte [bx+35h], 0

locret_131EE:				; CODE XREF: sub_131DA+Aj
		retn


; =============== S U B	R O U T	I N E =======================================


sub_131EF:		; CODE XREF: sub_13429+4Fp
					; sub_13429+55p
					; DATA XREF: ...

; FUNCTION CHUNK AT 31D0 SIZE 0000000A BYTES

		cmp	byte [bx+1Dh], 1
		jz	short loc_131D0
		and	byte [bx+3Dh], 0BFh
		cmp	al, [byte_2467D]
		jbe	short loc_13202
		mov	al, [byte_2467D]

loc_13202:				; CODE XREF: sub_131EF+Ej
		xor	ah, ah
		mov	[bx+22h], al
		mul	WORD [volume_245FC]
		mov	al, [bx+23h]
		mov	[bx+36h], ax
		mov	[bx+23h], ah
		retn


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


sub_13429:		; DATA XREF: sub_12DA8+3Eo
		test	byte [bx+17h], 4
		jz	short locret_13498
		mov	al, [bx+2]
		cmp	al, [bx+3]
		jz	short loc_13471
		mov	[bx+3],	al
		dec	al
		xor	ah, ah
		shl	ax, 6
		mov	di, ax
		add	di, myout
		mov	eax, [bx+28h]
		mov	[bx+40h], eax
		mov	eax, [bx+2Ch]
		mov	[bx+44h], eax
		mov	eax, [bx+30h]
		mov	[bx+48h], eax
		mov	al, [di+3Ch]
		mov	[bx+19h], al
		mov	ax, [di+32h]
		mov	[bx+26h], ax
		mov	ax, [di+30h]
		mov	[bx+24h], ax

loc_13471:				; CODE XREF: sub_13429+Cj
		mov	ax, [bx]
		call	sub_13177
		xor	al, al
		call	sub_131EF
		mov	al, [bx+8]
		call	sub_131EF
		test	byte [bx+17h], 2
		jnz	short loc_13499
		or	byte [bx+17h], 1
		movzx	eax, word [bx+4Ch]
		shl	eax, 8
		mov	[bx+4],	eax

locret_13498:				; CODE XREF: sub_13429+4j
		retn
; ---------------------------------------------------------------------------

loc_13499:				; CODE XREF: sub_13429+5Cj
		test	byte [bx+17h], 1
		jnz	sub_131DA
		retn


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


sub_135CA:		; CODE XREF: sub_12F56+1Fp
					; sub_140B6+3Cp ...
		mov	bx, volume_25908
		mov	cx, [word_245D4]
		xor	ax, ax

loc_135D3:				; CODE XREF: sub_135CA+1Aj
		mov	byte [bx+3Dh], 0
		test	byte [bx+17h], 10h
		jnz	short loc_135E0
		mov	[bx+0Ah], ax

loc_135E0:				; CODE XREF: sub_135CA+11j
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_135D3
		les	si, [pointer_245B4]
		mov	al, [es:si]
		inc	si
		or	al, al
		jz	short loc_135FD

loc_135F2:				; CODE XREF: sub_135CA+31j
		call	sub_13623
		mov	al, [es:si]
		inc	si
		or	al, al
		jnz	short loc_135F2

loc_135FD:				; CODE XREF: sub_135CA+26j
		mov	word [pointer_245B4], si
		mov	bx, volume_25908
		mov	cx, [word_245D4]

loc_13608:				; CODE XREF: sub_135CA+56j
		test	byte [bx+17h], 1
		jz	short loc_1361C
		test	byte [bx+3Dh], 0Ch
		jnz	short loc_1361C
		mov	ax, [bx]
		push	cx
		call	WORD [off_245CA]
		pop	cx

loc_1361C:				; CODE XREF: sub_135CA+42j
					; sub_135CA+48j
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_13608
		retn


; =============== S U B	R O U T	I N E =======================================


sub_13623:		; CODE XREF: sub_12CAD+1Cp
					; sub_135CA:loc_135F2p

; FUNCTION CHUNK AT 38BD SIZE 00000015 BYTES
; FUNCTION CHUNK AT 3ACE SIZE 00000009 BYTES
; FUNCTION CHUNK AT 3B66 SIZE 00000012 BYTES
; FUNCTION CHUNK AT 3BF1 SIZE 00000011 BYTES
; FUNCTION CHUNK AT 3CAE SIZE 00000005 BYTES
; FUNCTION CHUNK AT 3DF9 SIZE 00000025 BYTES
; FUNCTION CHUNK AT 3ED3 SIZE 00000031 BYTES

		mov	dh, al
		and	dh, 0E0h
		and	ax, 1Fh
		cmp	ax, [word_245D4]
		jnb	loc_137BE
		shl	ax, 4
		mov	bx, ax
		shl	ax, 2
		add	bx, ax
		add	bx, volume_25908
		test	dh, 80h
		jz	short loc_13661

loc_13646:
		and	dh, 7Fh
		mov	ax, [es:si]
		add	si, 2
		or	ax, ax
		jz	short loc_13661
		and	byte [bx+17h], 0EFh
		cmp	al, 20h	; ' '
		ja	short loc_13661
		or	dh, 80h
		mov	[bx+0Ah], ax

loc_13661:				; CODE XREF: sub_13623+21j
					; sub_13623+2Ej ...
		test	dh, 40h
		jz	short loc_13677
		and	dh, 0BFh
		mov	al, [es:si]
		inc	si
		cmp	al, 40h	; '@'
		ja	short loc_13677
		or	dh, 40h
		mov	[bx+8],	al

loc_13677:				; CODE XREF: sub_13623+41j
					; sub_13623+4Cj
		mov	[bx+3Dh], dh
		test	dh, 20h
		jz	sub_137D5
		mov	dx, [es:si]
		add	si, 2
		or	dh, dh
		jz	loc_13718
		movzx	ax, dh
		cmp	ax, [word_245D2]
		ja	loc_13718
		dec	ax
		shl	ax, 6
		mov	di, ax
		add	di, myout
		and	byte [bx+17h], 0FBh
		mov	al, [di+3Ch]
		and	al, 1
		shl	al, 2
		or	[bx+17h], al
		or	byte [bx+3Dh], 10h
		mov	[bx+2],	dh
		mov	word [bx+4Ch], 0
		test	byte [bx+17h], 40h
		jz	short loc_136CB
		and	byte [bx+17h], 0BFh
		mov	byte [bx+3], 0

loc_136CB:				; CODE XREF: sub_13623+9Ej
		mov	eax, [di+24h]
		mov	[bx+28h], eax
		mov	eax, [di+28h]
		mov	[bx+2Ch], eax
		mov	eax, [di+2Ch]
		mov	[bx+30h], eax
		mov	cl, [di+3Eh]
		and	cx, 0Fh
		shl	cx, 3
		mov	ax, cx
		neg	ax
		shl	cx, 4
		add	ax, cx
		add	ax, word_24998
		mov	[bx+38h], ax
		mov	ax, [freq_245DE]
		mov	cx, [di+36h]
		jcxz loc_13705
		mov	ax, cx

loc_13705:				; CODE XREF: sub_13623+DEj
		mov	[bx+14h], ax
		test	byte [bx+3Dh], 40h
		jnz	short loc_13718
		mov	al, [di+3Dh]
		mov	[bx+8],	al
		or	byte [bx+3Dh], 40h

loc_13718:				; CODE XREF: sub_13623+66j
					; sub_13623+71j ...
		or	dl, dl
		jz	sub_137D5
		cmp	dl, 0FEh ; '˛'
		jz	loc_137CE
		cmp	dl, 0FFh
		jz	sub_137D5
		mov	[bx+35h], dl
		or	byte [bx+3Dh], 8
		test	BYTE [sndflags_24622], 10h
		jnz	short loc_13742
		test	byte [bx+17h], 4
		jz	loc_137CE

loc_13742:				; CODE XREF: sub_13623+115j
		mov	al, [bx+35h]
		call	sub_13826
		xchg	ax, [bx]
		test	byte [bx+3Dh], 80h
		jz	short loc_13791
		mov	[word_245DC], ax
		mov	ax, [bx+0Ah]
		and	ah, 0F0h
		cmp	al, 3
		jz	loc_138BD
		cmp	al, 5
		jz	loc_138BD
		cmp	al, 9
		jz	loc_13ACE
		cmp	al, 0Ch
		jz	loc_13B66
		cmp	ax, 500Eh
		jz	loc_13BF1
		cmp	ax, 0D00Eh
		jz	loc_13CAE
		cmp	al, 13h
		jz	loc_13DF9
		cmp	al, 16h
		jz	loc_13DF9
		cmp	al, 19h
		jz	loc_13ED3

loc_13791:				; CODE XREF: sub_13623+12Bj
					; sub_13623+4B1j ...
		call	WORD [off_245C8]
		test	byte [bx+9], 4
		jnz	short loc_1379F
		mov	byte [bx+0Dh], 0

loc_1379F:				; CODE XREF: sub_13623+176j
		test	byte [bx+9], 40h
		jnz	short loc_137A9
		mov	byte [bx+0Fh], 0

loc_137A9:				; CODE XREF: sub_13623+180j
		movzx	di, byte [bx+0Ah]
		cmp	di, 32
		ja	eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		jmp	WORD [cs:effoff_18FA2+di]
; ---------------------------------------------------------------------------

loc_137BE:				; CODE XREF: sub_13623+Cj
		movzx	di, dh
		shr	di, 5
		mov	al, [cs:byte_11C29+di]
		xor	ah, ah
		add	si, ax
		retn
; ---------------------------------------------------------------------------

loc_137CE:				; CODE XREF: sub_13623+FEj
					; sub_13623+11Bj
		call	sub_137D5
		jmp	WORD [off_245CE]


; =============== S U B	R O U T	I N E =======================================


sub_137D5:		; CODE XREF: sub_13623+5Aj
					; sub_13623+F7j ...
		test	byte [bx+3Dh], 40h
		jnz	short loc_137F0
		movzx	di, byte [bx+0Ah]
		cmp	di, 32
		ja	eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		jmp	WORD [cs:effoff_18F60+di]
; ---------------------------------------------------------------------------

loc_137F0:				; CODE XREF: sub_137D5+4j
		movzx	di, byte [bx+0Ah]
		cmp	di, 32
		ja	eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		call	WORD [cs:effoff_18F60+di]
		test	byte [bx+3Dh], 40h
		jz	short locret_13812
		mov	al, [bx+8]
		jmp	WORD [off_245CC]
; ---------------------------------------------------------------------------

locret_13812:				; CODE XREF: sub_137D5+34j
		retn


; =============== S U B	R O U T	I N E =======================================


sub_13813:		; CODE XREF: sub_140B6+24p
					; sub_140B6+4Ap ...
		movzx	di, byte [bx+0Ah]
		cmp	di, 32
		ja	short eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		jmp	WORD [cs:effoff_18FE4+di]


; =============== S U B	R O U T	I N E =======================================


sub_13826:		; CODE XREF: sub_13623+122p
					; sub_13623+5D7p ...
		mov	cl, al
		movzx	di, cl
		dec	di
		and	di, 0Fh
		shl	di, 1
		shr	cl, 4
		cmp	BYTE [byte_2461A], 0
		jnz	short loc_1386C
		mov	ch, cl
		xor	cl, cl
		xor	ax, ax
		or	ch, ch
		jz	short loc_13863
		mov	ax, 24

loc_13848:
		dec	ch
		jz	short loc_13863
		mov	ax, 48
		dec	ch
		jz	short loc_13863
		mov	ax, 72
		dec	ch
		jz	short loc_13863
		mov	ax, 96
		dec	ch
		jz	short loc_13863
		mov	cl, ch

loc_13863:				; CODE XREF: sub_13826+1Dj
					; sub_13826+24j ...
		add	di, ax
		add	di, [bx+38h]
		sub	di, word_246DE

loc_1386C:				; CODE XREF: sub_13826+13j
		mov	ax, [word_246DE+di]
		shr	ax, cl
		mov	cx, [bx+14h]
		jcxz locret_1387D
		mul	WORD [freq_245DE]
		div	cx

locret_1387D:				; CODE XREF: sub_13826+4Fj
		retn


; =============== S U B	R O U T	I N E =======================================


eff_nullsub:	; CODE XREF: sub_13623+18Dj
					; sub_13623+196j ...
		retn


; =============== S U B	R O U T	I N E =======================================


eff_1387F:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	BYTE [byte_24668], 0
		jnz	short eff_nullsub


; =============== S U B	R O U T	I N E =======================================


eff_13886:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		shl	ax, 4

loc_1388B:				; CODE XREF: eff_13DE5+5j
		sub	[bx], ax
		cmp	word [bx], 0A0h ; '†'
		jge	short loc_13897
		mov	word [bx], 0A0h ; '†'

loc_13897:				; CODE XREF: eff_13886+Bj
		mov	ax, [bx]
		jmp	WORD [off_245CA]


; =============== S U B	R O U T	I N E =======================================


eff_1389D:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	BYTE [byte_24668], 0
		jnz	short eff_nullsub


; =============== S U B	R O U T	I N E =======================================


eff_138A4:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		shl	ax, 4

loc_138A9:				; CODE XREF: eff_13DEF+5j
		add	[bx], ax
		jb	short loc_138B3
		cmp	word [bx], 13696
		jbe	short loc_138B7

loc_138B3:				; CODE XREF: eff_138A4+7j
		mov	word [bx], 13696

loc_138B7:				; CODE XREF: eff_138A4+Dj
		mov	ax, [bx]
		jmp	WORD [off_245CA]

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_138BD:				; CODE XREF: sub_13623+138j
					; sub_13623+13Ej
		mov	ax, [bx]
		cmp	ax, [word_245DC]
		jnz	short loc_138C7
		xor	ax, ax

loc_138C7:				; CODE XREF: sub_13623+2A0j
		mov	[bx+10h], ax
		mov	ax, [word_245DC]
		mov	[bx], ax
		jmp	sub_137D5
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


eff_138D2:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_138DE
		xor	ah, ah
		shl	ax, 4
		mov	[bx+12h], ax

loc_138DE:				; CODE XREF: eff_138D2+2j eff_139AC+3j ...
		mov	ax, [bx+10h]
		or	ax, ax
		jz	locret_13CF4
		mov	dx, [bx+12h]
		cmp	ax, [bx]
		jb	short loc_138F6
		add	[bx], dx
		cmp	[bx], ax
		jb	short loc_1390B
		jmp	short loc_138FC
; ---------------------------------------------------------------------------

loc_138F6:				; CODE XREF: eff_138D2+1Aj
		sub	[bx], dx
		cmp	ax, [bx]
		jl	short loc_1390B

loc_138FC:				; CODE XREF: eff_138D2+22j
		mov	[bx], ax
		mov	word [bx+10h], 0
		and	byte [bx+17h], 0EFh
		jmp	WORD [off_245CA]
; ---------------------------------------------------------------------------

loc_1390B:				; CODE XREF: eff_138D2+20j
					; eff_138D2+28j
		test	byte [bx+17h], 20h
		jnz	short loc_13917
		mov	ax, [bx]
		jmp	WORD [off_245CA]
; ---------------------------------------------------------------------------

loc_13917:				; CODE XREF: eff_138D2+3Dj
		mov	di, [bx+38h]
		mov	ax, [bx]
		mov	cx, 3Bh	; ';'

loc_1391F:				; CODE XREF: eff_138D2+55j
		cmp	[di], ax
		jbe	short loc_13929
		add	di, 2
		dec	cx
		jnz	short loc_1391F

loc_13929:				; CODE XREF: eff_138D2+4Fj
		mov	ax, [di]
		jmp	WORD [off_245CA]


; =============== S U B	R O U T	I N E =======================================


eff_1392F:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	cl, 3

loc_13931:				; CODE XREF: eff_13E2D+2j
		or	al, al
		jz	short loc_13950
		mov	ch, al
		mov	dl, [bx+0Ch]
		and	al, 0Fh
		jz	short loc_13943
		and	dl, 0F0h
		or	dl, al

loc_13943:				; CODE XREF: eff_1392F+Dj
		and	ch, 0F0h
		jz	short loc_1394D
		and	dl, 0Fh
		or	dl, ch

loc_1394D:				; CODE XREF: eff_1392F+17j
		mov	[bx+0Ch], dl

loc_13950:				; CODE XREF: eff_1392F+4j eff_139B2+5j ...
		mov	al, [bx+0Dh]
		shr	al, 2
		and	ax, 1Fh
		mov	dl, [bx+9]
		and	dl, 3
		jz	short loc_1397B
		shl	al, 3
		cmp	dl, 1
		jz	short loc_1396D
		mov	dl, 0FFh
		jmp	short loc_13981
; ---------------------------------------------------------------------------

loc_1396D:				; CODE XREF: eff_1392F+38j
		mov	dl, al
		test	byte [bx+0Dh], 80h
		jz	short loc_13981
		mov	dl, 0FFh
		sub	dl, al
		jmp	short loc_13981
; ---------------------------------------------------------------------------

loc_1397B:				; CODE XREF: eff_1392F+30j
		mov	di, ax
		mov	dl, [table_251C0+di]

loc_13981:				; CODE XREF: eff_1392F+3Cj
					; eff_1392F+44j ...
		mov	al, [bx+0Ch]
		mov	dh, al
		and	al, 0Fh
		mul	dl
		mov	ch, [flag_playsetttings]
		and	ch, 1
		add	cl, ch
		shr	ax, cl
		test	byte [bx+0Dh], 80h
		jz	short loc_1399D
		neg	ax

loc_1399D:				; CODE XREF: eff_1392F+6Aj
		add	ax, [bx]
		shr	dh, 2
		and	dh, 3Ch
		add	[bx+0Dh], dh
		jmp	WORD [off_245CA]


; =============== S U B	R O U T	I N E =======================================


eff_139AC:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	eff_13AD7
		jmp	loc_138DE


; =============== S U B	R O U T	I N E =======================================


eff_139B2:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	eff_13AD7
		mov	cl, 3
		jmp	short loc_13950


; =============== S U B	R O U T	I N E =======================================


eff_139B9:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_139D8
		mov	cl, al
		mov	dl, [bx+0Eh]
		and	al, 0Fh
		jz	short loc_139CB
		and	dl, 0F0h
		or	dl, al

loc_139CB:				; CODE XREF: eff_139B9+Bj
		and	cl, 0F0h
		jz	short loc_139D5
		and	dl, 0Fh
		or	dl, cl

loc_139D5:				; CODE XREF: eff_139B9+15j
		mov	[bx+0Eh], dl

loc_139D8:				; CODE XREF: eff_139B9+2j
		mov	al, [bx+0Fh]
		shr	al, 2
		and	ax, 1Fh
		mov	dl, [bx+9]
		shr	dl, 4
		and	dl, 3
		jz	short loc_13A06
		shl	al, 3
		cmp	dl, 1
		jz	short loc_139F8
		mov	dl, 0FFh
		jmp	short loc_13A0C
; ---------------------------------------------------------------------------

loc_139F8:				; CODE XREF: eff_139B9+39j
		mov	dl, al
		test	byte [bx+0Fh], 80h
		jz	short loc_13A0C
		mov	dl, 0FFh
		sub	dl, al
		jmp	short loc_13A0C
; ---------------------------------------------------------------------------

loc_13A06:				; CODE XREF: eff_139B9+31j
		mov	di, ax
		mov	dl, [table_251C0+di]

loc_13A0C:				; CODE XREF: eff_139B9+3Dj
					; eff_139B9+45j ...
		mov	al, [bx+0Eh]
		mov	dh, al
		and	al, 0Fh
		mul	dl
		shr	ax, 6
		mov	ah, al
		mov	al, [bx+8]
		test	byte [bx+0Fh], 80h
		jnz	short loc_13A30
		add	al, ah
		cmp	al, [byte_2467D]
		jbe	short loc_13A36
		mov	al, [byte_2467D]
		jmp	short loc_13A36
; ---------------------------------------------------------------------------

loc_13A30:				; CODE XREF: eff_139B9+68j
		sub	al, ah
		jns	short loc_13A36
		xor	al, al

loc_13A36:				; CODE XREF: eff_139B9+70j
					; eff_139B9+75j ...
		shr	dh, 2
		and	dh, 3Ch
		add	[bx+0Fh], dh
		jmp	WORD [off_245CC]


; =============== S U B	R O U T	I N E =======================================


eff_13A43:		; CODE XREF: sub_12AFD+16p
					; sub_13623+196j ...
		cmp	al, 0A4h ; '§'
		jz	short loc_13A5B
		cmp	al, 0A5h ; '•'
		jz	short loc_13A60
		cmp	al, 0A6h ; '¶'
		jz	short loc_13A65
		cmp	al, 80h	; 'Ä'
		ja	short locret_13A5A
		test	BYTE [sndflags_24622], 4

locret_13A5A:				; CODE XREF: eff_13A43+Ej
		retn
; ---------------------------------------------------------------------------

loc_13A5B:				; CODE XREF: eff_13A43+2j
		or	byte [bx+17h], 80h
		retn
; ---------------------------------------------------------------------------

loc_13A60:				; CODE XREF: eff_13A43+6j
		and	byte [bx+17h], 7Fh
		retn
; ---------------------------------------------------------------------------

loc_13A65:				; CODE XREF: eff_13A43+Aj
		xor	byte [bx+17h], 80h
		retn


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


eff_13A94:		; CODE XREF: sub_137D5+16j
					; sub_137D5+2Bp ...
		or	al, al
		jz	short loc_13A9B
		mov	[bx+16h], al

loc_13A9B:				; CODE XREF: eff_13A94+2j
		movzx	eax, byte [bx+16h]
		shl	eax, 8
		cmp	eax, [bx+30h]
		ja	short loc_13AAE
		mov	[bx+4Ch], ax
		retn
; ---------------------------------------------------------------------------

loc_13AAE:				; CODE XREF: eff_13A94+14j
		cmp	BYTE [byte_2461A], 0
		jnz	short loc_13AC6
		call	WORD [off_245CE]
		and	byte [bx+17h], 0FBh
		or	byte [bx+17h], 40h
		mov	byte [bx+3], 0
		retn
; ---------------------------------------------------------------------------

loc_13AC6:				; CODE XREF: eff_13A94+1Fj
		mov	eax, [bx+30h]
		mov	[bx+4Ch], ax
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13ACE:				; CODE XREF: sub_13623+144j
		mov	al, [bx+0Bh]
		call	eff_13A94
		jmp	loc_13791
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


eff_13AD7:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, [bx+8]
		test	al, 0F0h
		jnz	short loc_13AEF

loc_13ADE:				; CODE XREF: eff_13E32+1Ej
					; eff_13E32+36j ...
		and	al, 0Fh

loc_13AE0:				; CODE XREF: eff_13C95+8j
		sub	dl, al
		mov	al, dl
		jnb	short loc_13AE8
		xor	al, al

loc_13AE8:				; CODE XREF: eff_13AD7+Dj
		mov	[bx+8],	al
		jmp	WORD [off_245CC]
; ---------------------------------------------------------------------------

loc_13AEF:				; CODE XREF: eff_13AD7+5j
					; eff_13E32+27j ...
		shr	al, 4

loc_13AF2:				; CODE XREF: eff_13C88+8j
		add	dl, al
		mov	al, dl
		cmp	al, [byte_2467D]
		jbe	short loc_13AFF
		mov	al, [byte_2467D]

loc_13AFF:				; CODE XREF: eff_13AD7+23j
		mov	[bx+8],	al
		jmp	WORD [off_245CC]


; =============== S U B	R O U T	I N E =======================================


eff_13B06:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		dec	ax
		mov	[word_245F0], ax
		inc	ax
		test	BYTE [flag_playsetttings], 4
		jnz	short loc_13B5B
		bt	word [byte_282E8], ax
		jnb	short loc_13B5B
		mov	cx, [word_245FA]
		add	cx, 7
		shr	cx, 3
		jz	short loc_13B34
		xor	di, di

loc_13B29:				; CODE XREF: eff_13B06+2Cj
		cmp	BYTE [byte_282E8+di], 0FFh
		jnz	short loc_13B3E
		inc	di
		dec	cx
		jnz	short loc_13B29

loc_13B34:				; CODE XREF: eff_13B06+1Fj
					; eff_13B06+4Ej
		push	bx
		push	si
		push	es
		call	vlm_141DF
		pop	es
		pop	si
		pop	bx
		retn
; ---------------------------------------------------------------------------

loc_13B3E:				; CODE XREF: eff_13B06+28j
		mov	al, [byte_282E8+di]
		shl	di, 3
		mov	cx, 8

loc_13B48:				; CODE XREF: eff_13B06+48j
		shr	al, 1
		jnb	short loc_13B50
		inc	di
		dec	cx
		jnz	short loc_13B48

loc_13B50:				; CODE XREF: eff_13B06+44j
		cmp	di, [word_245FA]
		jnb	short loc_13B34
		dec	di
		mov	[word_245F0], di

loc_13B5B:				; CODE XREF: eff_13B06+Cj
					; eff_13B06+13j ...
		mov	BYTE [byte_24669], 0
		mov	BYTE [byte_2466A], 1
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13B66:				; CODE XREF: sub_13623+14Aj
		mov	al, [bx+0Bh]
		cmp	al, [byte_2467D]
		jbe	short loc_13B72
		mov	al, [byte_2467D]

loc_13B72:				; CODE XREF: sub_13623+54Aj
		mov	[bx+8],	al
		jmp	loc_13791
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


eff_13B78:		; CODE XREF: sub_137D5+16j
					; sub_137D5+2Bp ...
		cmp	al, [byte_2467D]
		jbe	short loc_13B81
		mov	al, [byte_2467D]

loc_13B81:				; CODE XREF: eff_13B78+4j
		mov	[bx+8],	al
		jmp	WORD [off_245CC]


; =============== S U B	R O U T	I N E =======================================


eff_13B88:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, al
		and	dl, 0Fh
		shr	al, 4
		mov	ah, 0Ah
		mul	ah
		add	al, dl
		cmp	al, 3Fh	; '?'
		ja	short loc_13B5B
		mov	[byte_24669], al
		mov	BYTE [byte_2466A], 1
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13BA3:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	di, ax
		shr	di, 3
		and	di, 1Eh
		and	al, 0Fh
		jmp	WORD [cs:effoff_19026+di]


; =============== S U B	R O U T	I N E =======================================


eff_13BB2:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13BBB
		or	byte [bx+17h], 20h
		retn
; ---------------------------------------------------------------------------

loc_13BBB:				; CODE XREF: eff_13BB2+2j
		and	byte [bx+17h], 0DFh
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13BC0:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	byte [bx+9], 0F0h
		or	[bx+9],	al
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13BC8:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	ax, 0Fh
		mov	di, ax
		cmp	BYTE [byte_2461A], 0
		jnz	short loc_13BE7
		shl	di, 3
		mov	ax, di
		neg	ax
		shl	di, 4
		add	ax, di
		add	ax, word_24998
		mov	[bx+38h], ax
		retn
; ---------------------------------------------------------------------------

loc_13BE7:				; CODE XREF: eff_13BC8+Aj
		shl	di, 1
		mov	ax, [table_246F6+di]
		mov	[bx+14h], dx
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13BF1:				; CODE XREF: sub_13623+151j
		mov	al, [bx+0Bh]
		call	eff_13BC8
		mov	al, [bx+35h]
		call	sub_13826
		mov	[bx], ax
		jmp	loc_13791
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


eff_13C02:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	BYTE [byte_24668], 0
		jnz	locret_13CF4
		or	al, al
		jz	short loc_13C2D
		cmp	byte [bx+3Ch], 0
		jnz	short loc_13C1A
		inc	al
		mov	[bx+3Ch], al

loc_13C1A:				; CODE XREF: eff_13C02+11j
		dec	byte [bx+3Ch]
		jz	locret_13CF4
		mov	al, [bx+3Bh]
		mov	[byte_24669], al
		mov	BYTE [byte_2466B], 1
		retn
; ---------------------------------------------------------------------------

loc_13C2D:				; CODE XREF: eff_13C02+Bj
		mov	ax, [word_245F6]
		mov	[bx+3Bh], al
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13C34:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	byte [bx+9], 0Fh
		shl	al, 4
		or	[bx+9],	al
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13C3F:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	BYTE [byte_24668], 0
		jz	short loc_13C47
		retn
; ---------------------------------------------------------------------------

loc_13C47:				; CODE XREF: eff_13C3F+5j
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:byte_13C54+di]
		jmp	eff_13A43

; ---------------------------------------------------------------------------
byte_13C54	db 0,9,12h,1Bh,24h,2Dh,36h,40h,40h,4Ah,53h,5Ch,65h,6Eh
					; DATA XREF: mtm_module+43r
					; faar_module+55r ...
		db 77h,80h

; =============== S U B	R O U T	I N E =======================================


eff_13C64:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	locret_13CF4
		cmp	BYTE [byte_24668], 0
		jnz	short loc_13C77
		test	byte [bx+3Dh], 8
		jnz	short locret_13CF4

loc_13C77:				; CODE XREF: eff_13C64+Bj
		mov	dl, al
		movzx	ax, BYTE [byte_24668]
		div	dl
		or	ah, ah
		jnz	short locret_13CF4
		jmp	WORD [off_245C8]


; =============== S U B	R O U T	I N E =======================================


eff_13C88:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, [bx+8]
		cmp	BYTE [byte_24668], 0
		jz	loc_13AF2
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13C95:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, [bx+8]
		cmp	BYTE [byte_24668], 0
		jz	loc_13AE0
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13CA2:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	al, [byte_24668]
		jnz	short locret_13CF4
		xor	al, al
		jmp	WORD [off_245CC]

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13CAE:				; CODE XREF: sub_13623+158j
		mov	al, [bx+0Bh]
		and	al, 0Fh
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


eff_13CB3:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	al, [byte_24668]
		jnz	short locret_13CF4
		cmp	word [bx], 0
		jz	short locret_13CF4
		mov	byte [bx+0Ah], 0
		mov	byte [bx+0Bh], 0
		jmp	loc_13791


; =============== S U B	R O U T	I N E =======================================


eff_13CC9:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	BYTE [byte_24668], 0
		jnz	short locret_13CF4
		cmp	BYTE [byte_2466D], 0
		jnz	short locret_13CF4
		inc	al
		mov	[byte_2466C], al
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13CDD:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		test	BYTE [flag_playsetttings], 2
		jnz	short eff_13CE8
		cmp	al, 20h	; ' '
		ja	short sub_13CF6


; =============== S U B	R O U T	I N E =======================================


eff_13CE8:		; CODE XREF: sub_12EBA+6Bp
					; sub_13623+196j ...
		or	al, al
		jz	short locret_13CF5
		mov	[byte_24667], al
		mov	BYTE [byte_24668], 0

locret_13CF4:				; CODE XREF: eff_138D2+11j
					; eff_13C02+5j	...
		retn
; ---------------------------------------------------------------------------

locret_13CF5:				; CODE XREF: eff_13CE8+2j
		retn


; =============== S U B	R O U T	I N E =======================================


sub_13CF6:		; CODE XREF: sub_12EBA+65p
					; eff_13CDD+9j	...

; FUNCTION CHUNK AT 3DB0 SIZE 00000011 BYTES

		xor	ah, ah
		mov	[byte_24666], al
		mov	cx, ax
		mov	dl, 91
		div	dl
		inc	al
		mov	[cs:byte_14F72], al
		mov	[cs:byte_14F73], al
		test	BYTE [sndflags_24622], 4
		jnz	short loc_13D4B
		test	BYTE [sndflags_24622], 10h
		jnz	settimer
		shl	cx, 1
		mov	ax, 5
		mul	WORD [freq1]
		div	cx
		xor	dx, dx
		div	WORD [word_245E8]
		inc	ax
		or	dx, dx
		jnz	short loc_13D36
		dec	ax
		mov	dx, [word_245E8]

loc_13D36:				; CODE XREF: sub_13CF6+39j
		mov	[word_245EA], dx
		mov	[word_245EC], ax
		mov	[word_245EE], ax
		mov	ax, [word_245E8]
		mov	[word_245E4], ax
		mov	[cs:word_14F6C], ax
		retn
; ---------------------------------------------------------------------------

loc_13D4B:				; CODE XREF: sub_13CF6+1Aj
		call	sub_13D95
		mov	ah, al
		pushf
		cli
		mov	dx, [gravis_port]
		sub	dx, 0FBh ; '˚'
		mov	al, 4
		out	dx, al
		inc	dx
		mov	al, 80h	; 'Ä'
		out	dx, al
		xor	al, al
		out	dx, al
		add	dx, 0FAh ; '˙'
		mov	al, 46h	; 'F'
		out	dx, al
		add	dl, 2
		mov	al, ah
		out	dx, al
		sub	dl, 2
		mov	al, 45h	; 'E'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		mov	al, 4
		out	dx, al
		sub	dx, 0FDh ; '˝'
		mov	al, 4
		out	dx, al
		inc	dx
		mov	al, 1
		out	dx, al
		popf
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13D95

loc_13D8D:				; CODE XREF: sub_13D95+10j
		shl	cx, 1
		inc	BYTE [byte_24618]
		jmp	short loc_13D9A
; END OF FUNCTION CHUNK	FOR sub_13D95

; =============== S U B	R O U T	I N E =======================================


sub_13D95:		; CODE XREF: sub_13CF6:loc_13D4Bp

; FUNCTION CHUNK AT 3D8D SIZE 00000008 BYTES

		mov	BYTE [byte_24618], 1

loc_13D9A:				; CODE XREF: sub_13D95-2j
		xor	dx, dx
		mov	ax, 31250
		div	cx
		neg	al
		or	ah, ah
		jnz	short loc_13D8D
		mov	ah, [byte_24618]
		mov	[byte_24619], ah
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13CF6

settimer:				; CODE XREF: sub_13CF6+21j
		xor	ax, ax
		cmp	cx, 45
		jbe	short set_timer
		mov	dx, 2Dh	; '-'
		mov	ax, 8426h
		div	cx
		jmp	short $+2
; END OF FUNCTION CHUNK	FOR sub_13CF6

; =============== S U B	R O U T	I N E =======================================


set_timer:		; CODE XREF: configure_timer+Fp
					; memfill8080+4p ...
		mov	[cs:timer_word_14F6E], ax
		pushf
		cli
		push	ax
		mov	al, 34h	; '4'
		out	43h, al		; Timer	8253-5 (AT: 8254.2).
		pop	ax
		out	40h, al		; Timer	8253-5 (AT: 8254.2).
		mov	al, ah
		out	40h, al		; Timer	8253-5 (AT: 8254.2).
		popf
		retn


; =============== S U B	R O U T	I N E =======================================


clean_timer:	; CODE XREF: clean_int8_mem_timr+Fp
					; midi_sndoff+Fp
		pushf
		cli
		mov	al, 36h	; '6'
		out	43h, al		; Timer	8253-5 (AT: 8254.2).
		xor	al, al
		out	40h, al		; Timer	8253-5 (AT: 8254.2).
		jmp	short $+2
		out	40h, al		; Timer	8253-5 (AT: 8254.2).
		popf
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13DE5:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	sub_14087
		or	ax, ax
		jnz	loc_1388B
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13DEF:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	sub_14087
		or	ax, ax
		jnz	loc_138A9
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13DF9:				; CODE XREF: sub_13623+15Ej
					; sub_13623+164j
		mov	ax, [bx]
		cmp	ax, [word_245DC]
		jnz	short loc_13E03
		xor	ax, ax

loc_13E03:				; CODE XREF: sub_13623+7DCj
		mov	[bx+10h], ax
		mov	ax, [word_245DC]
		mov	[bx], ax
		mov	al, [bx+0Bh]
		or	al, al
		jnz	short loc_13E18
		mov	al, [bx+34h]
		mov	[bx+0Bh], al

loc_13E18:				; CODE XREF: sub_13623+7EDj
		mov	[bx+34h], al
		jmp	sub_137D5
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


eff_13E1E:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13E2A
		xor	ah, ah
		shl	ax, 2
		mov	[bx+12h], ax

loc_13E2A:				; CODE XREF: eff_13E1E+2j eff_13E7F+3j
		jmp	loc_138DE


; =============== S U B	R O U T	I N E =======================================


eff_13E2D:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	cl, 5
		jmp	loc_13931


; =============== S U B	R O U T	I N E =======================================


eff_13E32:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13E39
		mov	[bx+34h], al

loc_13E39:				; CODE XREF: eff_13E32+2j
		mov	al, [bx+34h]
		mov	dl, [bx+8]
		mov	cl, al
		and	cl, 0Fh
		mov	ch, al
		shr	ch, 4
		cmp	cl, 0Fh
		jnz	short loc_13E5E
		or	ch, ch
		jz	loc_13ADE
		cmp	BYTE [byte_24668], 0
		jz	loc_13AEF
		retn
; ---------------------------------------------------------------------------

loc_13E5E:				; CODE XREF: eff_13E32+1Aj
		cmp	ch, 0Fh
		jz	short loc_13E6F
		mov	dl, [bx+8]
		test	al, 0Fh
		jnz	loc_13ADE
		jmp	loc_13AEF
; ---------------------------------------------------------------------------

loc_13E6F:				; CODE XREF: eff_13E32+2Fj
		or	cl, cl
		jz	loc_13AEF
		cmp	BYTE [byte_24668], 0
		jz	loc_13ADE
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13E7F:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	eff_13E32
		jmp	short loc_13E2A


; =============== S U B	R O U T	I N E =======================================


eff_13E84:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	eff_13E32
		mov	cl, 5
		jmp	loc_13950


; =============== S U B	R O U T	I N E =======================================


eff_13E8C:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	sub_13E9B
		mov	[byte_24667], ah
		mov	BYTE [byte_24668], 0
		jmp	sub_13CF6


; =============== S U B	R O U T	I N E =======================================


sub_13E9B:		; CODE XREF: _2stm_module+2Ep
					; eff_13E8Cp
		movzx	di, al
		mov	dx, di
		and	dl, 0Fh
		shr	di, 4
		mov	ax, dx
		mul	BYTE [cs:table_13EC3+di]
		shr	ax, 4
		neg	ax
		add	ax, 31h	; '1'
		mov	dx, ax
		shl	ax, 2
		add	ax, dx
		shr	ax, 1
		mov	dx, di
		mov	ah, dl
		retn

; ---------------------------------------------------------------------------
table_13EC3	db 140,50,25,15,10,7,6,4,3,3,2,2,2,2,1,1 ; DATA	XREF: sub_13E9B+Dr
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13ED3:				; CODE XREF: sub_13623+16Aj
		mov	cl, [bx+0Bh]
		and	cx, 0FFh
		jz	loc_13791
		mov	ax, [bx]
		sub	ax, [word_245DC]
		jns	short loc_13EE8
		neg	ax

loc_13EE8:				; CODE XREF: sub_13623+8C1j
		xor	dx, dx
		div	cx
		mov	[bx+12h], ax
		mov	byte [bx+0Bh], 0
		or	byte [bx+17h], 10h
		mov	ax, [bx]
		mov	[bx+10h], ax
		mov	ax, [word_245DC]
		mov	[bx], ax
		jmp	sub_137D5
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


nullsub_2:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		retn


; =============== S U B	R O U T	I N E =======================================


eff_13F05:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13F0C
		mov	[bx+34h], al

loc_13F0C:				; CODE XREF: eff_13F05+2j
		mov	al, [bx+34h]
		mov	dl, al
		shr	dl, 4
		and	al, 0Fh
		mov	dh, al
		and	ax, 0Fh
		add	al, dl
		jz	locret_13CF4
		mov	cl, al
		movzx	ax, BYTE [byte_24668]
		div	cl
		cmp	ah, dl
		jb	short loc_13F34
		xor	al, al
		jmp	WORD [off_245CC]
; ---------------------------------------------------------------------------

loc_13F34:				; CODE XREF: eff_13F05+27j
		mov	al, [bx+8]
		jmp	WORD [off_245CC]


; =============== S U B	R O U T	I N E =======================================


eff_13F3B:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13F42
		mov	[bx+34h], al

loc_13F42:				; CODE XREF: eff_13F3B+2j
		mov	al, [bx+34h]
		mov	ch, al
		shr	al, 4
		test	al, 7
		jz	short loc_13FB7
		test	al, 8
		jnz	short loc_13F96
		cmp	al, 6
		jz	short loc_13F6D
		cmp	al, 7
		jz	short loc_13F7C
		dec	al
		mov	cl, al
		mov	al, 1
		shl	al, cl
		sub	[bx+8],	al
		jnb	short loc_13FB7
		mov	byte [bx+8], 0
		jmp	short loc_13FB7
; ---------------------------------------------------------------------------

loc_13F6D:				; CODE XREF: eff_13F3B+19j
		movzx	ax, byte [bx+8]
		shl	ax, 1
		mov	dl, 3
		div	dl
		mov	[bx+8],	al
		jmp	short loc_13FB7
; ---------------------------------------------------------------------------

loc_13F7C:				; CODE XREF: eff_13F3B+1Dj
		shr	byte [bx+8], 1
		jmp	short loc_13FB7
; ---------------------------------------------------------------------------

loc_13F81:				; CODE XREF: eff_13F3B+5Fj
		movzx	ax, byte [bx+8]
		mov	dx, ax
		add	ax, dx
		add	ax, dx
		shr	ax, 1
		jmp	short loc_13FAB
; ---------------------------------------------------------------------------

loc_13F8F:				; CODE XREF: eff_13F3B+63j
		mov	al, [bx+8]
		add	al, al
		jmp	short loc_13FAB
; ---------------------------------------------------------------------------

loc_13F96:				; CODE XREF: eff_13F3B+15j
		and	al, 7
		cmp	al, 6
		jz	short loc_13F81
		cmp	al, 7
		jz	short loc_13F8F
		dec	al
		mov	cl, al
		mov	al, 1
		shl	al, cl
		add	al, [bx+8]

loc_13FAB:				; CODE XREF: eff_13F3B+52j
					; eff_13F3B+59j
		cmp	al, [byte_2467D]
		jbe	short loc_13FB4
		mov	al, [byte_2467D]

loc_13FB4:				; CODE XREF: eff_13F3B+74j
		mov	[bx+8],	al

loc_13FB7:				; CODE XREF: eff_13F3B+11j
					; eff_13F3B+2Aj ...
		mov	al, ch
		and	al, 0Fh
		jmp	eff_13C64


; =============== S U B	R O U T	I N E =======================================


eff_13FBE:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jnz	short loc_13FCE
		mov	al, [bx+34h]
		or	al, al
		jz	locret_13CF4
		mov	[bx+0Bh], al

loc_13FCE:				; CODE XREF: eff_13FBE+2j
		mov	[bx+34h], al
		mov	al, [bx+35h]
		mov	dl, al
		and	dl, 0Fh
		jz	locret_13CF4
		dec	dl
		shr	al, 4
		mov	ah, 0Ch
		mul	ah
		add	dl, al
		movzx	ax, BYTE [byte_24668]
		mov	dh, 3
		div	dh
		or	ah, ah
		jz	short loc_1401A
		mov	dh, [bx+0Bh]
		cmp	ah, 2
		jz	short loc_14000
		shr	dh, 4

loc_14000:				; CODE XREF: eff_13FBE+3Dj
		and	dh, 0Fh
		add	dl, dh
		movzx	ax, dl
		mov	dh, 0Ch
		div	dh
		inc	ah
		shl	al, 4
		or	al, ah
		call	sub_13826
		jmp	WORD [off_245CA]
; ---------------------------------------------------------------------------

loc_1401A:				; CODE XREF: eff_13FBE+35j
		mov	ax, [bx]
		jmp	WORD [off_245CA]


; =============== S U B	R O U T	I N E =======================================


eff_14020:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		shl	ax, 2
		push	bx
		push	si
		push	es
		push	cs
		call	near change_amplif
		pop	es
		pop	si
		pop	bx
		retn


; =============== S U B	R O U T	I N E =======================================


eff_14030:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	ax, 0Fh
		mov	di, ax
		mov	al, [cs:table_14057+di]
		mov	[byte_2467B], al

loc_1403D:				; CODE XREF: eff_14067+Ej
					; eff_14067+17j ...
		call far calc_14043
		jmp	sub_13CF6


; =============== S U B	R O U T	I N E =======================================


calc_14043:		; CODE XREF: faar_module+34p
					; eff_14030:loc_1403Dp
		mov	al, [byte_2467B]
		add	al, [byte_2467C]
		and	eax, 0FFh
		lea	ax, [eax+eax*4]
		shr	ax, 1
		retn

; ---------------------------------------------------------------------------
table_14057	db 0FFh,80h,40h,2Ah,20h,19h,15h,12h,10h,0Eh,0Ch,0Bh,0Ah
					; DATA XREF: faar_module+27r
					; eff_14030+5r
		db 9,9,8

; =============== S U B	R O U T	I N E =======================================


eff_14067:		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_14080
		test	al, 0Fh
		jz	short loc_14077
		and	al, 0Fh
		sub	[byte_2467C], al
		jmp	short loc_1403D
; ---------------------------------------------------------------------------

loc_14077:				; CODE XREF: eff_14067+6j
		shr	al, 4
		add	[byte_2467C], al
		jmp	short loc_1403D
; ---------------------------------------------------------------------------

loc_14080:				; CODE XREF: eff_14067+2j
		mov	BYTE [byte_2467C], 0
		jmp	short loc_1403D


; =============== S U B	R O U T	I N E =======================================


sub_14087:		; CODE XREF: eff_13DE5p eff_13DEFp
		xor	ah, ah
		or	al, al
		jz	short loc_14090
		mov	[bx+34h], al

loc_14090:				; CODE XREF: sub_14087+4j
		mov	al, [bx+34h]
		cmp	BYTE [byte_24668], 0
		jz	short loc_140A2
		cmp	al, 0E0h ; '‡'
		jnb	short loc_140B3
		shl	ax, 2
		retn
; ---------------------------------------------------------------------------

loc_140A2:				; CODE XREF: sub_14087+11j
		cmp	al, 0E0h ; '‡'
		jbe	short loc_140B3
		mov	dl, al
		and	al, 0Fh
		cmp	dl, 0F0h ; ''
		jbe	short locret_140B2
		shl	ax, 2

locret_140B2:				; CODE XREF: sub_14087+26j
		retn
; ---------------------------------------------------------------------------

loc_140B3:				; CODE XREF: sub_14087+15j
					; sub_14087+1Dj
		xor	ax, ax
		retn


; =============== S U B	R O U T	I N E =======================================


sub_140B6:		; CODE XREF: gravis_set+1Ep
					; gravis_int+91p ...
		cmp	BYTE [byte_24671], 1
		jz	short locret_140E5
		cmp	BYTE [play_state], 1
		jz	short locret_140E5
		inc	BYTE [byte_24668]
		mov	al, [byte_24668]
		cmp	al, [byte_24667]
		jnb	short loc_140E6
		mov	bx, volume_25908
		mov	cx, [word_245D4]

loc_140D8:				; CODE XREF: sub_140B6+2Dj
		push	bx
		push	cx
		call	sub_13813
		pop	cx
		pop	bx
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_140D8

locret_140E5:				; CODE XREF: sub_140B6+5j sub_140B6+Cj
		retn
; ---------------------------------------------------------------------------

loc_140E6:				; CODE XREF: sub_140B6+19j
		mov	BYTE [byte_24668], 0
		cmp	BYTE [byte_2466D], 0
		jnz	short loc_140F7
		call	sub_135CA
		jmp	short loc_14111
; ---------------------------------------------------------------------------

loc_140F7:				; CODE XREF: sub_140B6+3Aj
		mov	bx, volume_25908
		mov	cx, [word_245D4]

loc_140FE:				; CODE XREF: sub_140B6+53j
		push	bx
		push	cx
		call	sub_13813
		pop	cx
		pop	bx
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_140FE
		mov	si, word [pointer_245B4]
		jmp	short $+2

loc_14111:				; CODE XREF: sub_140B6+3Fj
					; midi_int8p+43p
		cmp	BYTE [byte_2466B], 1
		jz	loc_141BA
		cmp	BYTE [byte_2466A], 1
		jz	short loc_14153
		cmp	BYTE [byte_2466C], 0
		jz	short loc_14131
		xor	al, al
		xchg	al, [byte_2466C]
		mov	[byte_2466D], al

loc_14131:				; CODE XREF: sub_140B6+70j
		cmp	BYTE [byte_2466D], 0
		jz	short loc_1413E
		dec	BYTE [byte_2466D]
		jnz	short loc_14142

loc_1413E:				; CODE XREF: sub_140B6+80j
		inc	WORD [word_245F6]

loc_14142:				; CODE XREF: sub_140B6+86j
		mov	bx, [word_245F0]
		movzx	ax, BYTE [byte_281E8+bx]
		cmp	[word_245F6], ax
		jbe	loc_141DA

loc_14153:				; CODE XREF: sub_140B6+69j
		cmp	BYTE [play_state], 2
		jz	short loc_14184
		inc	WORD [word_245F0]


; =============== S U B	R O U T	I N E =======================================


sub_1415E:		; CODE XREF: sub_12F56+11p
		mov	ax, [word_245FA]
		cmp	[word_245F0], ax
		jb	short loc_14184
		test	BYTE [flag_playsetttings], 4
		jz	short vlm_141DF
		mov	ax, [word_245F8]
		mov	[word_245F0], ax
		or	ax, ax
		jnz	short loc_14184
		mov	al, [byte_2467A]
		call	sub_13CF6
		mov	al, [byte_24679]
		call	eff_13CE8

loc_14184:				; CODE XREF: sub_140B6+A2j
					; sub_1415E+7j	...
		mov	bx, [word_245F0]
		mov	al, [byte_280E8+bx]
		or	al, al
		jz	short loc_141A2
		push	bx
		cmp	al, 0FFh
		jnz	short loc_1419E
		mov	al, [byte_2467A]
		call	sub_13CF6
		mov	al, [byte_24679]

loc_1419E:				; CODE XREF: sub_1415E+35j
		call	eff_13CE8
		pop	bx

loc_141A2:				; CODE XREF: sub_1415E+30j
		bts	word [byte_282E8], bx
		movzx	bx, BYTE [byte_27FE8+bx]
		mov	[my_seg_index],	bx
		shl	bx, 1
		mov	es, [segs_table+bx]
		mov	word [pointer_245B4+2], es

loc_141BA:				; CODE XREF: sub_140B6+60j
		xor	ax, ax
		xchg	al, [byte_24669]
		mov	[word_245F6], ax
		call	sub_11C0C
		mov	BYTE [byte_2466A], 0
		mov	BYTE [byte_2466B], 0
		mov	BYTE [byte_2466C], 0
		mov	BYTE [byte_2466D], 0

loc_141DA:				; CODE XREF: sub_140B6+99j
		mov	word [pointer_245B4], si
		retn


; =============== S U B	R O U T	I N E =======================================


vlm_141DF:		; CODE XREF: eff_13B06+31p
					; sub_1415E+Ej
		push	cs
		call	near volume_12A66
		mov	BYTE [byte_24671], 1
		mov	dl, 1
		mov	bx, 5344h	; DS
		mov	cx, 4D50h	; MP
		mov	ax, 60FFh
		int	2Fh		; IPLAY: get data seg
		retn


; =============== S U B	R O U T	I N E =======================================


snd_initialze:	; CODE XREF: sub_12DA8+78p

; FUNCTION CHUNK AT 526B SIZE 000000DB BYTES

		cmp	BYTE [snd_init], 1
		jz	short loc_1420D
		mov	BYTE [snd_init], 1
		movzx	bx, BYTE [sndcard_type]
		shl	bx, 1
		jmp     sb16_init
; ---------------------------------------------------------------------------

loc_1420D:				; CODE XREF: snd_initialze+5j
					; snd_on+5j ...
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


snd_on:		; CODE XREF: sub_12EBA+87p
		cmp	BYTE [snd_init], 1
		jnz	short loc_1420D
		cmp	BYTE [snd_set_flag],	1
		jz	short loc_1420D
		mov	BYTE [snd_set_flag],	1
		movzx	bx, BYTE [sndcard_type]
		shl	bx, 1
		jmp     sb16_on


; =============== S U B	R O U T	I N E =======================================


snd_off:		; CODE XREF: snd_offx+8p snd_deinit+Cp

; FUNCTION CHUNK AT 0B5A SIZE 000001CC BYTES

		cmp	BYTE [snd_init], 1
		jnz	short loc_1420D
		cmp	BYTE [snd_set_flag],	0
		jz	short loc_1420D
		mov	BYTE [snd_set_flag],	0
		push	cs
		call	near volume_12A66
		movzx	bx, BYTE [sndcard_type]
		shl	bx, 1
		jmp     sb16_off


; =============== S U B	R O U T	I N E =======================================


snd_deinit:		; CODE XREF: deinit_125B9+18p
		cmp	BYTE [snd_init], 1
		jnz	short loc_1420D
		mov	BYTE [snd_init], 0
		call	snd_off
		movzx	bx, BYTE [sndcard_type]
		shl	bx, 1
		jmp     sb16_deinit


; =============== S U B	R O U T	I N E =======================================


 ; sp-analysis failed

; START	OF FUNCTION CHUNK FOR wss_test

loc_14332:				; CODE XREF: proaud_init+22j
					; proaud_init+E2j ...
		stc
		retn
; END OF FUNCTION CHUNK	FOR wss_test

; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
		db 87h,	0DBh

; =============== S U B	R O U T	I N E =======================================


; void __cdecl gravis_int()



; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


; void __cdecl proaud_14700()



; =============== S U B	R O U T	I N E =======================================


 ;	sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


 ;	sp-analysis failed


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
wss_freq_table	dw 5513			; DATA XREF: wss_test+3Er
					; wss_test:loc_149DFr
wss_freq_table2	dw  1,19D7h,0Fh,1F40h, 0,2580h,0Eh,2B11h, 3,3E80h, 2,49D4h
					; DATA XREF: wss_test+51r
		dw  5,5622h, 7,6B25h, 4,7D00h, 6,8133h,0Dh,93A8h, 9,0AC44h
		dw 0Bh,0BB80h,0Ch

; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------

wss_int:				; DATA XREF: wss_set+18o
		push	ax
		push	dx
; ---------------------------------------------------------------------------
		db 0BAh	; ∫
word_14913	dw 536h			; DATA XREF: wss_set+14w
; ---------------------------------------------------------------------------
		xor	al, al
		out	dx, al
		push	ds
		mov	ax, seg003
		mov	ds, ax
		jmp	loc_14E10

; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


sb16_init:		; DATA XREF: seg003:0D08o
		mov	BYTE [sndflags_24622], 9
		mov	BYTE [byte_24623], 1
		mov	BYTE [bit_mode], 16
		call	sb16_detect_port
		mov	dx, aErrorSoundcardN ; "Error: Soundcard	not found!\r\n"
		jb	loc_14332
		mov	al, [irq_number]
		mov	[sb_irq_number], al
		cmp	al, 0FFh
		jnz	short loc_14ABB
		mov	ah, 80h	; 'Ä'
		call	ReadMixerSB
		cmp	al, 0FFh
		jz	short loc_14ABB
		mov	ah, 2
		shr	al, 1
		jb	short loc_14AB3
		mov	ah, 5
		shr	al, 1
		jb	short loc_14AB3
		mov	ah, 7
		shr	al, 1
		jb	short loc_14AB3
		mov	ah, 0Ah

loc_14AB3:				; CODE XREF: sb16_init+30j
					; sb16_init+36j ...
		mov	[sb_irq_number], ah
		mov	[irq_number], ah

loc_14ABB:				; CODE XREF: sb16_init+21j
					; sb16_init+2Aj
		mov	al, [dma_channel]
		mov	[dma_chn_mask],	al
		cmp	al, 0FFh
		jnz	short loc_14AFD
		mov	ah, 81h	; 'Å'
		call	ReadMixerSB
		cmp	al, 0FFh
		jz	short loc_14AFD
		cmp	BYTE [bit_mode], 8
		jz	short loc_14AE7
		mov	ah, 7
		test	al, 80h
		jnz	short loc_14AF5
		mov	ah, 6
		test	al, 40h
		jnz	short loc_14AF5
		mov	ah, 5
		test	al, 20h
		jnz	short loc_14AF5

loc_14AE7:				; CODE XREF: sb16_init+60j
		mov	ah, 3
		test	al, 4
		jnz	short loc_14AF5
		mov	ah, 1
		test	al, 2
		jnz	short loc_14AF5
		mov	ah, 0

loc_14AF5:				; CODE XREF: sb16_init+66j
					; sb16_init+6Cj ...
		mov	[dma_chn_mask],	ah
		mov	[dma_channel], ah

loc_14AFD:				; CODE XREF: sb16_init+50j
					; sb16_init+59j
		call	sb16_sound_on
		mov	eax, 1000h
		mov	cl, [dma_chn_mask]
		call	alloc_dma_buf
		mov	word [dma_buf_pointer], 0
		mov	word [dma_buf_pointer+2], ax
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


sb16_on:		; DATA XREF: seg003:0D1Eo
		call	sub_13017
		mov	BYTE [dma_mode], 58h	; 'X'
		mov	WORD [word_2460E], 1000h
		mov	si, sb_callback ; myfunc
		mov	al, [sb_irq_number]
		call	setsnd_handler
		mov	dx, [sb_base_port]
		add	dl, 0Ch

loc_14B36:				; CODE XREF: sb16_on+21j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B36
		mov	al, 41h	; 'A'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B3E:				; CODE XREF: sb16_on+29j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B3E
		mov	al, byte [freq1+1]
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B47:				; CODE XREF: sb16_on+32j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B47
		mov	al, byte [freq1]
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B50:				; CODE XREF: sb16_on+3Bj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B50
		cmp	BYTE [bit_mode], 16
		jz	short loc_14B6A
		mov	ax, [sb_base_port]
		add	al, 0Eh
		mov	[cs:word_14BBB], ax
		mov	ax, 0C6h ; '∆'
		jmp	short loc_14B76
; ---------------------------------------------------------------------------

loc_14B6A:				; CODE XREF: sb16_on+42j
		mov	ax, [sb_base_port]
		add	al, 0Fh
		mov	[cs:word_14BBB], ax
		mov	ax, 10B6h

loc_14B76:				; CODE XREF: sb16_on+50j
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B77:				; CODE XREF: sb16_on+62j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B77
		mov	al, [byte_24623]
		and	al, 1
		shl	al, 5
		or	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B87:				; CODE XREF: sb16_on+72j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B87
		mov	ax, [word_2460E]
		shr	ax, 2
		mov	cl, [bit_mode]
		shr	cl, 4
		and	cl, 1
		shr	ax, cl
		dec	ax
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14BA0:				; CODE XREF: sb16_on+8Bj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14BA0
		mov	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	cl, [dma_chn_mask]
		call	dma_186E3
		mov	BYTE [byte_2466E], 1
		retn

; ---------------------------------------------------------------------------

; void __cdecl sb_callback()
sb_callback:				; DATA XREF: sb16_on+Eo
		push	ax
		push	dx
; ---------------------------------------------------------------------------
		db 0BAh	; ∫
word_14BBB	dw 22Fh			; DATA XREF: sb16_on+49w sb16_on+57w
; ---------------------------------------------------------------------------
		in	al, dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
		jmp	loc_14E10

; =============== S U B	R O U T	I N E =======================================


sb16_off:		; DATA XREF: seg003:0D34o
		pushf
		cli
		cmp	BYTE [byte_2466E], 1
		jnz	short loc_14BFD
		cli
		mov	dx, [sb_base_port]
		add	dl, 0Ch

loc_14BD8:				; CODE XREF: sb16_off+14j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14BD8
		mov	al, 0DAh ; '⁄'
		cmp	BYTE [bit_mode], 8
		jz	short loc_14BE8
		mov	al, 0D9h ; 'Ÿ'

loc_14BE8:				; CODE XREF: sb16_off+1Dj
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14BE9:				; CODE XREF: sb16_off+25j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14BE9
		call	restore_intvector
		mov	cl, [dma_chn_mask]
		call	set_dmachn_mask
		mov	BYTE [byte_2466E], 0

loc_14BFD:				; CODE XREF: sb16_off+7j
		popf
		retn


; =============== S U B	R O U T	I N E =======================================


sb16_deinit:	; DATA XREF: seg003:0D4Ao
		call	memfree_18A28
		call	sb16_sound_off
		retn


; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sb_set

sbpro_set:				; CODE XREF: sb_set+6j
					; DATA XREF: seg003:0D20o
		call	sub_13017
		mov	BYTE [dma_mode], 58h	; 'X'
		mov	WORD [word_2460E], 1000h
		mov	ax, [sb_base_port]
		add	al, 0Eh
		mov	[cs:word_14CEB], ax
		mov	ah, 0Eh
		call	ReadMixerSB
		mov	[byte_24664], al
		and	al, 0FDh
		cmp	BYTE [byte_24623], 0
		jz	short loc_14C89
		call	WriteMixerSB
		or	al, 22h

loc_14C89:				; CODE XREF: sb_set-F5j
		call	WriteMixerSB
		pushf
		cli
		mov	dx, [sb_base_port]
		add	dl, 0Eh
		in	al, dx		; DMA controller, 8237A-5.
					; Clear	mask registers.
					; Any OUT enables all 4	channels.
		sub	dl, 2

loc_14C99:				; CODE XREF: sb_set-DBj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14C99
		mov	al, 40h	; '@'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CA1:				; CODE XREF: sb_set-D3j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CA1
		mov	al, [sb_timeconst]
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CAA:				; CODE XREF: sb_set-CAj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CAA
		mov	al, 48h	; 'H'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CB2:				; CODE XREF: sb_set-C2j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CB2
		mov	ax, [word_2460E]
		shr	ax, 2
		dec	ax
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CBF:				; CODE XREF: sb_set-B5j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CBF
		mov	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CC7:				; CODE XREF: sb_set-ADj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CC7
		mov	al, 90h	; 'ê'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	BYTE [byte_2466E], 1
		mov	si, loc_14CE8 ; myfunc
		mov	al, [sb_irq_number]
		call	setsnd_handler
		mov	cl, [dma_chn_mask]
		call	dma_186E3
		popf
		retn
; END OF FUNCTION CHUNK	FOR sb_set
; ---------------------------------------------------------------------------

loc_14CE8:				; DATA XREF: sb_set-A3o
		push	ax
		push	dx
; ---------------------------------------------------------------------------
		db 0BAh	; ∫
word_14CEB	dw 22Eh			; DATA XREF: sb_set-108w
; ---------------------------------------------------------------------------
		in	al, dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
		jmp	loc_14E10

; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


	; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


 ; sp-analysis failed

; START	OF FUNCTION CHUNK FOR proaud_14700

loc_14E10:				; CODE XREF: proaud_14700+15j
					; seg000:491Ej	...
		add	WORD [word_24602], 400h
		and	WORD [word_24602], 0FFFh
		inc	BYTE [byte_24620]
		cmp	BYTE [byte_24620], 2
		ja	lc_disable_interpol

loc_14E29:				; CODE XREF: proaud_14700+7BCj
		pushad
		push	es
		push	fs
		push	gs
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		test	byte [config_word+1], 10h
		jz	short loc_14E4D
		inc	BYTE [byte_24621]
		and	BYTE [byte_24621], 3
		jnz	short loc_14E4D
		mov	cl, [dma_channel]
		call	dma_186E3

loc_14E4D:				; CODE XREF: proaud_14700+739j
					; proaud_14700+744j
		mov	bx, 1
		mov	cl, [irq_number]
		shl	bx, cl
		mov	dx, 21h	; '!'
		or	bh, bh
		jz	short loc_14E66
		mov	dx, 0A1h ; '°'
		mov	al, 20h	; ' '
		out	0A0h, al	; PIC 2	 same as 0020 for PIC 1
		mov	bl, bh

loc_14E66:				; CODE XREF: proaud_14700+75Bj
		in	al, dx		; Interrupt Controller #2, 8259A
		or	al, bl
		out	dx, al		; Interrupt Controller #2, 8259A
		sti
		mov	ax, [word_24602]

loc_14E6E:				; CODE XREF: proaud_14700+78Aj
		mov	dx, ax
		cmp	ax, [word_24600]
		ja	short loc_14E79
		add	ax, 1000h

loc_14E79:				; CODE XREF: proaud_14700+774j
		sub	ax, [word_24600]
		cmp	ax, 800h
		jb	short loc_14E8C
		push	dx
		call	sub_16C69
		pop	ax
		add	ax, 10h
		jmp	short loc_14E6E
; ---------------------------------------------------------------------------

loc_14E8C:				; CODE XREF: proaud_14700+780j
		mov	bx, 1
		mov	cl, [irq_number]
		shl	bx, cl
		mov	dx, 21h	; '!'
		or	bh, bh
		jz	short loc_14EA1
		mov	dx, 0A1h ; '°'
		mov	bl, bh

loc_14EA1:				; CODE XREF: proaud_14700+79Aj
		not	bl
		in	al, dx		; Interrupt Controller #2, 8259A
		and	al, bl
		out	dx, al		; Interrupt Controller #2, 8259A
		pop	gs
		pop	fs
		pop	es
		popad
		dec	BYTE [byte_24620]
		pop	ds
		pop	dx
		pop	ax
		iret
; ---------------------------------------------------------------------------

lc_disable_interpol:			; CODE XREF: proaud_14700+725j
		and	BYTE [flag_playsetttings], 0EFh
		jmp	loc_14E29
; END OF FUNCTION CHUNK	FOR proaud_14700
; ---------------------------------------------------------------------------
		mov	al, 20h	; ' '
		cmp	BYTE [irq_number], 7
		jbe	short loc_14ECC
		out	0A0h, al	; PIC 2	 same as 0020 for PIC 1
		jmp	short $+2

loc_14ECC:				; CODE XREF: seg000:4EC6j
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		pop	dx
		pop	ax
		iret

; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


timer_int_end:	; CODE XREF: covox_timer_int+22j
					; covox_timer_int+33j ...
		cmp	BYTE [cs:byte_14F70], 0
		jz	short loc_14F3C
		pushad
		push	ds
		push	es
		push	fs
		push	gs
		mov	ax, seg003
		mov	ds, ax
		mov	ax, [word_245E4]
		mov	[cs:word_14F6C], ax
		sti
		call	sub_16C69
		pop	gs
		pop	fs
		pop	es
		pop	ds
		popad
		iret
; ---------------------------------------------------------------------------

loc_14F3C:				; CODE XREF: timer_int_end+6j
		mov	WORD [cs:word_14F6C], 1
		jmp	FAR [cs:int8addr]

; ---------------------------------------------------------------------------
		dec	BYTE [cs:byte_14F73]
		jz	short loc_14F50
		iret
; ---------------------------------------------------------------------------

loc_14F50:				; CODE XREF: seg000:4F4Dj
		push	ax
		mov	al, [cs:byte_14F72]
		mov	[cs:byte_14F73], al
		mov	ax, [cs:timer_word_14F6E]
		call	set_timer
		pop	ax
		jmp	FAR [cs:int8addr]
; ---------------------------------------------------------------------------
; ---------------------------------------------------------------------------
int8addr	dd 0			; DATA XREF: sub_12DA8+6Aw
					; clean_int8_mem_timr+5r ...
word_14F6C	dw 0			; DATA XREF: configure_timer+1Bw
					; memfill8080+Dw ...
timer_word_14F6E dw 0			; DATA XREF: set_timerw seg000:4F59r
byte_14F70	db 0			; DATA XREF: configure_timer+12w
					; memfill8080+7w ...
byte_14F71	db 0			; DATA XREF: sub_12D35:loc_12D41w
					; sub_12D35:loc_12D4Ew
byte_14F72	db 0			; DATA XREF: sub_13CF6+Dw seg000:4F51r
byte_14F73	db 0			; DATA XREF: sub_13CF6+11w
					; seg000:4F48w	...

; =============== S U B	R O U T	I N E =======================================


covox_init:		; DATA XREF: seg003:0D0Eo
		mov	BYTE [sndflags_24622], 3
		mov	BYTE [byte_24623], 0
		mov	BYTE [bit_mode], 8
		cmp	WORD [snd_base_port], 0FFFFh
		jnz	short loc_14F95
		xor	ax, ax
		mov	es, ax
		mov	ax, [es:408h]
		mov	[snd_base_port], ax

loc_14F95:				; CODE XREF: covox_init+14j
		mov	ax, [snd_base_port]
		mov	[cs:word_14FC8], ax
		pushf
		cli
		mov	dx, covox_timer_int
		call	set_timer_int
		sub	ax, 0F00h
		mov	[cs:word_14FC0], ax
		mov	WORD [cs:word_14FC5], 0F000h
		popf
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


covox_set:		; DATA XREF: seg003:0D24o
		call	configure_timer
		retn

; ---------------------------------------------------------------------------

; =============== S U B	R O U T	I N E =======================================


covox_timer_int:	; DATA XREF: covox_init+2Ao
		push	ax
		push	dx
		push	ds
; ---------------------------------------------------------------------------
		db 0BAh	; ∫		; self moifying
word_14FC0	dw 1000h		; DATA XREF: covox_init+33w
; ---------------------------------------------------------------------------
		mov	ds, dx
; ---------------------------------------------------------------------------
		db 0A0h	; †
word_14FC5	dw 1234h		; DATA XREF: covox_init+37w
					; covox_timer_int+16w ...
		db 0BAh	; ∫
word_14FC8	dw 378h			; DATA XREF: covox_init+24w
; ---------------------------------------------------------------------------
		out	dx, al		; Printer Data Latch:
					; send byte to printer
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		pop	dx
		pop	ax
		inc	WORD [cs:word_14FC5]
		jz	short loc_14FE3
		dec	WORD [cs:word_14F6C]
		jz	near timer_int_end
		iret
; ---------------------------------------------------------------------------

loc_14FE3:				; CODE XREF: covox_timer_int+1Bj
		mov	WORD [cs:word_14FC5], 0F000h
		dec	WORD [cs:word_14F6C]
		jz	near timer_int_end
		iret


; =============== S U B	R O U T	I N E =======================================


covox_sndoff:	; DATA XREF: seg003:0D3Ao
		call	memfill8080
		retn


; =============== S U B	R O U T	I N E =======================================


covox_clean:	; DATA XREF: seg003:0D50o
		call	clean_int8_mem_timr
		retn


; =============== S U B	R O U T	I N E =======================================


stereo_init:	; DATA XREF: seg003:0D10o
		mov	BYTE [sndflags_24622], 3
		mov	BYTE [byte_24623], 1
		mov	BYTE [bit_mode], 8
		cmp	WORD [snd_base_port], -1
		jnz	short loc_1501D
		xor	ax, ax
		mov	es, ax
		mov	ax, [es:408h]
		mov	[snd_base_port], ax

loc_1501D:				; CODE XREF: stereo_init+14j
		mov	ax, [snd_base_port]
		add	ax, 2
		mov	[cs:word_1504D], ax
		pushf
		cli
		mov	dx, stereo_timer_int
		call	set_timer_int
		sub	ax, 0F00h
		mov	word [cs:loc_15047+1], ax
		mov	WORD [cs:word_15056], 0F000h
		popf
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


stereo_set:		; DATA XREF: seg003:0D26o
		call	configure_timer
		retn


; =============== S U B	R O U T	I N E =======================================


stereo_timer_int:	; DATA XREF: stereo_init+2Do
		push	ax
		push	dx
		push	ds

loc_15047:				; DATA XREF: stereo_init+36w
		mov	dx, seg000
		mov	ds, dx
; ---------------------------------------------------------------------------
		db 0BAh
word_1504D	dw 37Ah			; DATA XREF: stereo_init+27w
; ---------------------------------------------------------------------------
		mov	al, 2
		out	dx, al
		sub	dl, 2
; ---------------------------------------------------------------------------
		db 0A1h
word_15056	dw 1234h		; DATA XREF: stereo_init+3Aw
					; stereo_timer_int+28w	...
; ---------------------------------------------------------------------------
		out	dx, al		; Printer Data Latch:
					; send byte to printer
		add	dl, 2
		mov	al, 1
		out	dx, al		; Printer Control Bits:
					; 0: 1 when sending byte
					; 1: 1 causes LF after CR
					; 2: 0 resets the printer
					; 3: 1 selects the printer
					; 4: +IRQ Enable
		sub	dl, 2
		mov	al, ah
		out	dx, al		; Printer Data Latch:
					; send byte to printer
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		pop	dx
		pop	ax
		add	WORD [cs:word_15056], 2
		jb	short loc_1507E
		dec	WORD [cs:word_14F6C]
		jz	near timer_int_end
		iret
; ---------------------------------------------------------------------------

loc_1507E:				; CODE XREF: stereo_timer_int+2Ej
		mov	WORD [cs:word_15056], 0F000h
		dec	WORD [cs:word_14F6C]
		jz	near timer_int_end
		iret


; =============== S U B	R O U T	I N E =======================================


stereo_sndoff:	; DATA XREF: seg003:0D3Co
		call	memfill8080
		retn


; =============== S U B	R O U T	I N E =======================================


stereo_clean:	; DATA XREF: seg003:0D52o
		call	clean_int8_mem_timr
		retn


; =============== S U B	R O U T	I N E =======================================


adlib_init:		; DATA XREF: seg003:0D12o
		mov	BYTE [sndflags_24622], 0Bh
		mov	BYTE [byte_24623], 0
		mov	BYTE [bit_mode], 8
		call	adlib_18389
		mov	ax, 2120h
		call	adlib_18395
		mov	ax, 0F060h
		call	adlib_18395
		mov	ax, 0F080h
		call	adlib_18395
		mov	ax, 1C0h
		call	adlib_18395
		mov	ax, 0E0h ; '‡'
		call	adlib_18395
		mov	ax, 3F43h
		call	adlib_18395
		mov	ax, 0B0h ; '∞'
		call	adlib_18395
		mov	ax, 0A0h ; '†'
		call	adlib_18395
		mov	ax, 8FA0h
		call	adlib_18395
		mov	ax, 2EB0h
		call	adlib_18395
		mov	cx, 4000h

loc_150E8:				; CODE XREF: adlib_init+52j
		dec	cx
		jnz	short loc_150E8
		mov	ax, 20B0h
		call	adlib_18395
		mov	ax, 0A0h ; '†'
		call	adlib_18395
		mov	ax, 40h	; '@'
		call	adlib_18395
		pushf
		cli
		mov	dx, adlib_timer_int
		call	set_timer_int
		sub	ax, 0F00h
		mov	word [cs:loc_15120+1], ax
		mov	WORD [cs:word_15126], 0F000h
		popf
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


adlib_set:		; DATA XREF: seg003:0D28o
		call	configure_timer
		retn

; ---------------------------------------------------------------------------

adlib_timer_int:			; DATA XREF: adlib_init+68o
		push	ax
		push	bx
		push	dx
		push	ds

loc_15120:				; DATA XREF: adlib_init+71w
		mov	ax, 1234h	; self modifying
		mov	ds, ax
; ---------------------------------------------------------------------------
		db 0A0h	; †		; self modifying
word_15126	dw 1234h		; DATA XREF: adlib_init+75w
					; seg000:5135w	...
; ---------------------------------------------------------------------------
		mov	bx, seg003
		mov	ds, bx
		mov	bx, table_24898
		xlat
		mov	dx, 389h
		out	dx, al
		inc	WORD [cs:word_15126]
		jz	short loc_1514E

loc_1513C:				; CODE XREF: seg000:5155j
		pop	ds
		pop	dx
		pop	bx
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ax
		dec	WORD [cs:word_14F6C]
		jz	near timer_int_end
		iret
; ---------------------------------------------------------------------------

loc_1514E:				; CODE XREF: seg000:513Aj
		mov	WORD [cs:word_15126], 0F000h
		jmp	short loc_1513C

; =============== S U B	R O U T	I N E =======================================


adlib_sndoff:	; DATA XREF: seg003:0D3Eo
		call	memfill8080
		retn


; =============== S U B	R O U T	I N E =======================================


adlib_clean:	; DATA XREF: seg003:0D54o
		call	clean_int8_mem_timr
		call	adlib_18389
		retn


; =============== S U B	R O U T	I N E =======================================


pcspeaker_init:	; DATA XREF: seg003:0D14o
		mov	BYTE [sndflags_24622], 3
		mov	BYTE [byte_24623], 0
		mov	BYTE [bit_mode], 8
		pushf
		cli
		mov	al, 90h	; 'ê'
		out	43h, al		; Timer	8253-5 (AT: 8254.2).
		mov	dx, pcspeaker_interrupt
		call	set_timer_int
		sub	ax, 0F00h
		mov	[cs:word_1519B], ax
		mov	WORD [cs:word_151A3], 0F000h
		popf
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


pcspeaker_set:	; DATA XREF: seg003:0D2Ao
		in	al, 61h		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÕÀÕ OR	03H=spkr ON
					; 1: Tmr 2 data	Õº  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		or	al, 3
		out	61h, al		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÕÀÕ OR	03H=spkr ON
					; 1: Tmr 2 data	Õº  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		call	configure_timer
		retn

; ---------------------------------------------------------------------------

pcspeaker_interrupt:			; DATA XREF: pcspeaker_init+15o
		push	bx
		push	ds
; ---------------------------------------------------------------------------
		db 0BBh	; ª
word_1519B	dw 1000h		; DATA XREF: pcspeaker_init+1Ew
; ---------------------------------------------------------------------------
		mov	ds, bx
		xor	bh, bh
; ---------------------------------------------------------------------------
		db  8Ah	; ä
		db  1Eh
word_151A3	dw 1234h		; DATA XREF: pcspeaker_init+22w
					; seg000:51B8w	...
; ---------------------------------------------------------------------------
		mov	bl, [cs:pc_timer_tbl+bx]
		mov	bh, al
		mov	al, bl
		out	42h, al		; Timer	8253-5 (AT: 8254.2).
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		mov	al, bh
		pop	ds
		pop	bx
		inc	WORD [cs:word_151A3]
		jz	short loc_151C9
		dec	WORD [cs:word_14F6C]
		jz	near timer_int_end
		iret
; ---------------------------------------------------------------------------

loc_151C9:				; CODE XREF: seg000:51BDj
		mov	WORD [cs:word_151A3], 0F000h
		dec	WORD [cs:word_14F6C]
		jz	near timer_int_end
		iret

; =============== S U B	R O U T	I N E =======================================


pcspeaker_sndoff:	; DATA XREF: seg003:0D40o
		call	memfill8080
		in	al, 61h		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÕÀÕ OR	03H=spkr ON
					; 1: Tmr 2 data	Õº  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		and	al, 0FCh
		out	61h, al		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÕÀÕ OR	03H=spkr ON
					; 1: Tmr 2 data	Õº  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		retn


; =============== S U B	R O U T	I N E =======================================


pcspeaker_clean:	; DATA XREF: seg003:0D56o
		call	clean_int8_mem_timr
		retn

; ---------------------------------------------------------------------------
pc_timer_tbl	db 40h,40h,40h,40h,40h,40h,40h,40h,40h,40h,3Fh,3Fh,3Fh
					; DATA XREF: seg000:51A5r
		db 3Fh,3Fh,3Fh,3Fh,3Fh,3Fh,3Fh,3Fh,3Fh,3Eh,3Eh,3Eh,3Eh
		db 3Eh,3Eh,3Eh,3Eh,3Eh,3Eh,3Dh,3Dh,3Dh,3Dh,3Dh,3Dh,3Dh
		db 3Dh,3Dh,3Ch,3Ch,3Ch,3Ch,3Ch,3Ch,3Ch,3Ch,3Ch,3Ch,3Bh
		db 3Bh,3Bh,3Bh,3Bh,3Bh,3Bh,3Bh,3Bh,3Bh,3Ah,3Ah,3Ah,3Ah
		db 3Ah,3Ah,3Ah,3Ah,3Ah,3Ah,39h,39h,39h,39h,39h,39h,39h
		db 39h,39h,39h,38h,38h,38h,38h,38h,38h,38h,38h,37h,37h
		db 37h,37h,37h,36h,36h,36h,36h,35h,35h,35h,35h,34h,34h
		db 34h,33h,33h,32h,32h,31h,31h,30h,30h,2Fh,2Eh,2Dh,2Ch
		db 2Bh,2Ah,29h,28h,27h,26h,25h,24h,23h,22h,21h,20h,1Fh
		db 1Eh
; START	OF FUNCTION CHUNK FOR snd_initialze
nn:					; CODE XREF: snd_initialze+13j
		db 1Dh,1Ch,1Bh,1Ah,19h,18h,17h,16h,15h,14h,13h,12h,11h
		db 11h,10h,10h,0Fh,0Fh,0Eh,0Eh,0Dh,0Dh,0Dh,0Ch,0Ch,0Ch
		db 0Ch,0Bh,0Bh,0Bh,0Bh,0Ah,0Ah,0Ah,0Ah,0Ah,9,9,9,9,9,9
		db 9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,6,6,6,6
		db 6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4
		db 4,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1
		db 1,1,1,1,1
; ---------------------------------------------------------------------------

midi_init:				; DATA XREF: seg003:0D16o
		mov	BYTE [sndflags_24622], 12h
		mov	BYTE [byte_24623], 1
		mov	BYTE [bit_mode], 8
		mov	ax, [snd_base_port]
		cmp	ax, 0FFFFh
		jnz	short loc_15302
		mov	ax, 330h

loc_15302:				; CODE XREF: snd_initialze+1107j
		mov	[word_2465C], ax
		mov	[snd_base_port], ax
		mov	WORD [off_245CA], nullsub_4
		mov	WORD [off_245C8], midi_15466
		mov	WORD [off_245CC], midi_154AC
		mov	WORD [off_245CE], midi_1544D
		mov	bx, volume_25908
		mov	ah, 1

loc_15325:				; CODE XREF: snd_initialze+1146j
		mov	al, ah
		and	al, 0Fh
		mov	[bx+18h], al
		and	byte [bx+17h], 0FEh
		mov	byte [bx+35h], 0
		add	bx, 50h	; 'P'
		inc	ah
		cmp	ah, 10h
		jbe	short loc_15325
		call	midi_153C0
		call	midi_153D6
		clc
		retn
; END OF FUNCTION CHUNK	FOR snd_initialze

; =============== S U B	R O U T	I N E =======================================


midi_set:		; DATA XREF: seg003:0D2Co
		mov	bx, midi_int8p
		mov	dx, cs
		mov	al, 8
		call	setint_vect
		retn

; ---------------------------------------------------------------------------

; =============== S U B	R O U T	I N E =======================================


midi_int8p:		; DATA XREF: midi_seto
		pushad
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		push	ds
		push	es
		push	fs
		push	gs
		mov	ax, seg003
		mov	ds, ax
		cmp	BYTE [byte_24671], 1
		jz	short loc_1539A
		inc	BYTE [byte_24668]
		mov	al, [byte_24668]
		cmp	al, [byte_24667]
		jnb	short loc_1538F
		mov	bx, volume_25908
		mov	cx, [word_245D4]

loc_15380:				; CODE XREF: midi_int8p+37j
		push	bx
		push	cx
		call	sub_13813
		pop	cx
		pop	bx
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_15380
		jmp	short loc_1539A
; ---------------------------------------------------------------------------

loc_1538F:				; CODE XREF: midi_int8p+23j
		mov	BYTE [byte_24668], 0
		call	sub_135CA
		call	loc_14111

loc_1539A:				; CODE XREF: midi_int8p+16j
					; midi_int8p+39j
		pop	gs
		pop	fs
		pop	es
		pop	ds
		popad
		iret


; =============== S U B	R O U T	I N E =======================================


midi_sndoff:	; DATA XREF: seg003:0D42o
		mov	dx, word [cs:int8addr+2]
		mov	bx, word [cs:int8addr]
		mov	al, 8
		call	setint_vect
		call	clean_timer
		call	midi_153D6
		retn


; =============== S U B	R O U T	I N E =======================================


midi_clean:		; DATA XREF: seg003:0D58o
		mov	ah, 0FFh
		call	midi_153F1
		retn


; =============== S U B	R O U T	I N E =======================================


midi_153C0:		; CODE XREF: snd_initialze+1148p
		mov	ah, 0FFh
		call	midi_153F1
		mov	cx, 8000h
		call	midi_15442
		mov	ah, 3Fh	; '?'
		call	midi_153F1
		xor	cx, cx
		call	midi_15442
		retn


; =============== S U B	R O U T	I N E =======================================


midi_153D6:		; CODE XREF: snd_initialze+114Bp
					; midi_sndoff+12p
		xor	bl, bl

loc_153D8:				; CODE XREF: midi_153D6+18j
		mov	ah, 0B0h ; '∞'
		or	ah, bl
		call	midi_15413
		mov	ah, 7Bh	; '{'
		call	midi_15413
		xor	ah, ah
		call	midi_15413
		inc	bl
		cmp	bl, 10h
		jb	short loc_153D8
		retn


; =============== S U B	R O U T	I N E =======================================


midi_153F1:		; CODE XREF: midi_clean+2p
					; midi_153C0+2p ...
		mov	dx, [word_2465C]
		inc	dx
		xor	cx, cx

loc_153F8:				; CODE XREF: midi_153F1+Dj
		in	al, dx
		test	al, 40h
		jz	short loc_15401
		dec	cx
		jnz	short loc_153F8
		retn
; ---------------------------------------------------------------------------

loc_15401:				; CODE XREF: midi_153F1+Aj
		mov	al, ah
		out	dx, al
		xor	cx, cx

loc_15406:				; CODE XREF: midi_153F1+1Bj
		in	al, dx
		shl	al, 1
		jnb	short loc_1540E
		dec	cx
		jnz	short loc_15406

loc_1540E:				; CODE XREF: midi_153F1+18j
		dec	dx
		in	al, dx
		cmp	al, 0FEh ; '˛'
		retn


; =============== S U B	R O U T	I N E =======================================


midi_15413:		; CODE XREF: midi_153D6+6p
					; midi_153D6+Bp ...
		or	ah, ah
		jns	short loc_15421
		cmp	ah, [byte_24677]
		jz	short locret_15441
		mov	[byte_24677], ah

loc_15421:				; CODE XREF: midi_15413+2j
		mov	dx, [word_2465C]
		inc	dx
		mov	cl, 0FFh

loc_15428:				; CODE XREF: midi_15413+23j
		in	al, dx
		test	al, 40h
		jz	short loc_15439
		shl	al, 1
		jb	short loc_15434
		dec	dx
		in	al, dx
		inc	dx

loc_15434:				; CODE XREF: midi_15413+1Cj
		dec	cl
		jnz	short loc_15428
		retn
; ---------------------------------------------------------------------------

loc_15439:				; CODE XREF: midi_15413+18j
		dec	dx
		mov	al, ah
		out	dx, al
		sub	[byte_24678], al

locret_15441:				; CODE XREF: midi_15413+8j
		retn


; =============== S U B	R O U T	I N E =======================================


midi_15442:		; CODE XREF: midi_153C0+8p
					; midi_153C0+12p
		mov	dx, [word_2465C]
		inc	dx

loc_15447:				; CODE XREF: midi_15442+7j
		in	al, dx
		dec	cx
		jnz	short loc_15447
		retn


; =============== S U B	R O U T	I N E =======================================


nullsub_4:		; DATA XREF: snd_initialze+1112o
		retn


; =============== S U B	R O U T	I N E =======================================


midi_1544D:		; CODE XREF: midi_15466+6p
					; DATA XREF: snd_initialze+1124o
		and	byte [bx+17h], 0FEh
		call	midi_154DA
		or	ah, 80h
		call	midi_15413
		call	midi_154DE
		call	midi_15413
		mov	ah, 7Fh	; ''
		call	midi_15413
		retn


; =============== S U B	R O U T	I N E =======================================


midi_15466:		; DATA XREF: snd_initialze+1118o
		test	byte [bx+17h], 0FEh
		jz	short loc_1546F
		call	midi_1544D

loc_1546F:				; CODE XREF: midi_15466+4j
		or	byte [bx+17h], 1
		mov	al, [bx+2]
		cmp	al, [bx+3]
		jz	short loc_1548D
		mov	[bx+3],	al
		call	midi_154DA
		or	ah, 0C0h
		call	midi_15413
		mov	ah, [bx+2]
		call	midi_15413

loc_1548D:				; CODE XREF: midi_15466+13j
		mov	al, [bx+8]
		call	midi_154AC
		call	midi_154DA
		or	ah, 90h
		call	midi_15413
		call	midi_154DE
		call	midi_15413
		mov	ah, 7Fh	; ''
		call	midi_15413
		or	byte [bx+17h], 1
		retn


; =============== S U B	R O U T	I N E =======================================


midi_154AC:		; CODE XREF: midi_15466+2Ap
					; DATA XREF: snd_initialze+111Eo
		cmp	al, [byte_2467D]
		jb	short loc_154B5
		mov	al, [byte_2467D]

loc_154B5:				; CODE XREF: midi_154AC+4j
		cmp	al, [bx+1Bh]
		jz	short locret_154D9
		mov	[bx+1Bh], al
		movzx	di, al
		call	midi_154DA
		or	ah, 0B0h
		call	midi_15413
		mov	ah, 7
		call	midi_15413
		mov	al, 80h	; 'Ä'
		add	di, [off_24656]
		mul	byte [di]
		call	midi_15413

locret_154D9:				; CODE XREF: midi_154AC+Cj
		retn


; =============== S U B	R O U T	I N E =======================================


midi_154DA:		; CODE XREF: midi_1544D+4p
					; midi_15466+18p ...
		mov	ah, [bx+18h]
		retn


; =============== S U B	R O U T	I N E =======================================


midi_154DE:		; CODE XREF: midi_1544D+Dp
					; midi_15466+36p
		mov	al, [bx+35h]
		mov	dl, al
		and	dl, 0Fh
		dec	dl
		shr	al, 4
		mov	ah, 0Ch
		mul	ah
		add	al, dl
		mov	ah, al
		retn


; =============== S U B	R O U T	I N E =======================================


sub_154F4:		; CODE XREF: sub_15577+9p sub_1609F+9p
		mov	ax, [word_245E4]
		shr	ax, 4
		mov	[byte_24683], al
		push	bx
		push	si
		mov	bx, [si+26h]
		mov	eax, [si+4]
		shr	eax, 16h
		add	bx, ax
		call	ems_mapmem
		pop	si
		pop	bx
		mov	eax, [si+4]
		shr	eax, 0Ch
		cmp	word [si+26h], 0FFFFh
		jz	short loc_15525
		and	eax, 3FFh

loc_15525:				; CODE XREF: sub_154F4+29j
		add	ax, [si+24h]
		mov	es, ax
		movzx	ebx, byte [si+23h]
		mov	ax, [si+36h]
		mov	[word_24614], ax
		mov	BYTE [byte_24616], 0
		test	BYTE [flag_playsetttings], 10h
		jz	short lc_inerpol_disabld
		cmp	al, ah
		setnz	ah		; dosbox:  setnz sp
		mov	[byte_24616], ah
		movzx	ebx, al

lc_inerpol_disabld:			; CODE XREF: sub_154F4+4Bj
		shl	ebx, 9
		add	bx, vlm_byte_table
		movzx	ebp, word [si+20h]
		mov	ax, bp
		mov	ch, al
		shr	ebp, 8
		mov	esi, [si+4]
		mov	ax, si
		mov	cl, al
		and	esi, 0FFFh
		shr	esi, 8
		retn


; =============== S U B	R O U T	I N E =======================================


sub_15577:		; CODE XREF: sub_16C69:loc_16CB9p
					; sub_16C69+58Ap ...

; FUNCTION CHUNK AT 57F2 SIZE 000000C0 BYTES
; FUNCTION CHUNK AT 58C0 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 58EF SIZE 00000021 BYTES
; FUNCTION CHUNK AT 591E SIZE 00000021 BYTES
; FUNCTION CHUNK AT 594D SIZE 00000021 BYTES
; FUNCTION CHUNK AT 597C SIZE 00000021 BYTES
; FUNCTION CHUNK AT 59AB SIZE 00000021 BYTES
; FUNCTION CHUNK AT 59DA SIZE 00000021 BYTES
; FUNCTION CHUNK AT 5A09 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 5A38 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 5A67 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 5A96 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 5AC5 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 5AF4 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 5B23 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 5B52 SIZE 0000002D BYTES
; FUNCTION CHUNK AT 5E48 SIZE 00000257 BYTES

		test	byte [si+17h], 1
		jz	locret_157BC
		push	si
		call	sub_154F4
		test	BYTE [flag_playsetttings], 10h
		jnz	lc_perfrm_interpol
		cmp	BYTE [byte_24625], 1
		jz	loc_15E48
		xor	edx, edx
		mov	ax, [word_245E4]
		and	eax, 0Fh
		jmp	WORD [cs:offs_noninterp+eax*2]

; START	OF FUNCTION CHUNK FOR sub_1609F

loc_155A8:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_155B8:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_155C8:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_155D8:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_155E8:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_155F8:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15608:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15618:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]

loc_15621:
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15628:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15638:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15648:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15658:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15668:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15678:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15688:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		add	di, 8

loc_15698:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		cmp	BYTE [byte_24683], 0
		jz	loc_1578C

loc_156A1:				; CODE XREF: sub_1609F-917j
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+8],	ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+10h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+18h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+20h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+28h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+30h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+38h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+40h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+48h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+50h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+58h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+60h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+68h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+70h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		add	[di+78h], ax
		add	di, 80h	; 'Ä'
		dec	BYTE [byte_24683]
		jnz	loc_156A1

loc_1578C:				; CODE XREF: sub_1609F-A02j
					; sub_15577+5E0j ...
		mov	eax, esi
		shl	eax, 8
		mov	al, cl
		pop	si
		mov	cx, [word_24614]
		mov	[si+36h], cx
		mov	[si+23h], ch
		mov	edx, [si+4]
		and	dx, 0F000h
		add	eax, edx
		mov	edx, eax
		shr	edx, 8
		cmp	edx, [si+48h]
		ja	short loc_157BD
		mov	[si+4],	eax

locret_157BC:				; CODE XREF: sub_15577+4j
		retn
; ---------------------------------------------------------------------------

loc_157BD:				; CODE XREF: sub_1609F-8E9j
		mov	edx, [si+40h]
		shl	edx, 8
		test	byte [si+19h], 8
		jz	short loc_157E5
		mov	ebx, [si+44h]
		shl	ebx, 8

loc_157D3:				; CODE XREF: sub_1609F-8C4j
		sub	eax, ebx
		jb	short loc_157DD
		cmp	eax, edx
		ja	short loc_157D3

loc_157DD:				; CODE XREF: sub_1609F-8C9j
		add	eax, ebx
		mov	[si+4],	eax
		retn
; ---------------------------------------------------------------------------

loc_157E5:				; CODE XREF: sub_1609F-8D6j
		mov	[si+4],	edx
		and	byte [si+17h], 0FEh
		mov	byte [si+35h], 0
		retn
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_15577

lc_perfrm_interpol:			; CODE XREF: sub_15577+11j
		mov	al, ch
		cmp	al, [cs:byte_158B4]
		jz	short loc_15877
		mov	[cs:byte_158B4], al
		mov	[cs:byte_158E3], al
		mov	[cs:byte_15912], al
		mov	[cs:byte_15941], al
		mov	[cs:byte_15970], al
		mov	[cs:byte_1599F], al
		mov	[cs:byte_159CE], al
		mov	[cs:byte_159FD], al
		mov	[cs:byte_15A2C], al
		mov	[cs:byte_15A5B], al
		mov	[cs:byte_15A8A], al
		mov	[cs:byte_15AB9], al
		mov	[cs:byte_15AE8], al
		mov	[cs:byte_15B17], al
		mov	[cs:byte_15B46], al
		mov	[cs:byte_15B81], al
		mov	[cs:byte_15BAD], al
		mov	[cs:byte_15BDA], al
		mov	[cs:byte_15C07], al
		mov	[cs:byte_15C34], al
		mov	[cs:byte_15C61], al
		mov	[cs:byte_15C8E], al
		mov	[cs:byte_15CBB], al
		mov	[cs:byte_15CE8], al
		mov	[cs:byte_15D15], al
		mov	[cs:byte_15D42], al
		mov	[cs:byte_15D6F], al
		mov	[cs:byte_15D9C], al
		mov	[cs:byte_15DC9], al
		mov	[cs:byte_15DF6], al
		mov	[cs:byte_15E23], al

loc_15877:				; CODE XREF: sub_15577+282j
		and	ecx, 0FFh
		mov	ax, [word_245E4]
		and	eax, 0Fh
		xor	edx, edx
		jmp	WORD [cs:offs_interpol+eax*2]

loc_15891:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_158B4	db 0			; DATA XREF: sub_15577+27Dr
					; sub_15577+284w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_158C0:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_158E3	db 0			; DATA XREF: sub_15577+288w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_158EF:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15912	db 0			; DATA XREF: sub_15577+28Cw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_1591E:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15941	db 0			; DATA XREF: sub_15577+290w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_1594D:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15970	db 0			; DATA XREF: sub_15577+294w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_1597C:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_1599F	db 0			; DATA XREF: sub_15577+298w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_159AB:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_159CE	db 0			; DATA XREF: sub_15577+29Cw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_159DA:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_159FD	db 0			; DATA XREF: sub_15577+2A0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15A09:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15A2C	db 0			; DATA XREF: sub_15577+2A4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15A38:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15A5B	db 0			; DATA XREF: sub_15577+2A8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15A67:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15A8A	db 0			; DATA XREF: sub_15577+2ACw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15A96:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15AB9	db 0			; DATA XREF: sub_15577+2B0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15AC5:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15AE8	db 0			; DATA XREF: sub_15577+2B4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15AF4:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15B17	db 0			; DATA XREF: sub_15577+2B8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15B23:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15B46	db 0			; DATA XREF: sub_15577+2BCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15B52:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		cmp	BYTE [byte_24683], 0
		jz	loc_1578C

loc_15B5B:				; CODE XREF: seg000:5E41j
		xor	edx, edx
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15B81	db 0			; DATA XREF: sub_15577+2C0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15BAD	db 0			; DATA XREF: sub_15577+2C4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+8],	eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15BDA	db 0			; DATA XREF: sub_15577+2C8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+10h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15C07	db 0			; DATA XREF: sub_15577+2CCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+18h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15C34	db 0			; DATA XREF: sub_15577+2D0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+20h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15C61	db 0			; DATA XREF: sub_15577+2D4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+28h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15C8E	db 0			; DATA XREF: sub_15577+2D8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+30h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15CBB	db 0			; DATA XREF: sub_15577+2DCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+38h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15CE8	db 0			; DATA XREF: sub_15577+2E0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+40h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15D15	db 0			; DATA XREF: sub_15577+2E4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+48h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15D42	db 0			; DATA XREF: sub_15577+2E8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+50h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15D6F	db 0			; DATA XREF: sub_15577+2ECw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+58h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15D9C	db 0			; DATA XREF: sub_15577+2F0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+60h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15DC9	db 0			; DATA XREF: sub_15577+2F4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+68h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15DF6	db 0			; DATA XREF: sub_15577+2F8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+70h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_15E23	db 0			; DATA XREF: sub_15577+2FCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+78h], eax
		add	di, 80h	; 'Ä'
		mov	dx, loc_15E3D
		cmp	BYTE [byte_24616], 1
		jz	loc_1690B

loc_15E3D:				; DATA XREF: seg000:5E31o
		dec	BYTE [byte_24683]
		jnz	loc_15B5B
		jmp	loc_1578C
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15E48:				; CODE XREF: sub_15577+1Aj
		xor	edx, edx
		mov	ax, [word_245E4]
		and	eax, 0Fh
		jmp	WORD [cs:off_18E60+eax*2]

loc_15E5B:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15E6E:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15E81:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15E94:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15EA7:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15EBA:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15ECD:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15EE0:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15EF3:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15F06:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15F19:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15F2C:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15F3F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15F52:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15F65:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		add	di, 8

loc_15F78:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		cmp	BYTE [byte_24683], 0
		jz	loc_1578C

loc_15F81:				; CODE XREF: sub_15577+B21j
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+8],	eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+10h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+18h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+20h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+28h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+30h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+38h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+40h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+48h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+50h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+58h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+60h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+68h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+70h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		add	[di+78h], eax
		add	di, 80h	; 'Ä'
		dec	BYTE [byte_24683]
		jnz	loc_15F81
		jmp	loc_1578C
; END OF FUNCTION CHUNK	FOR sub_15577

; =============== S U B	R O U T	I N E =======================================


sub_1609F:		; CODE XREF: sub_16C69+4Bp
					; sub_16C69+594p ...

; FUNCTION CHUNK AT 55A8 SIZE 0000024A BYTES
; FUNCTION CHUNK AT 60E0 SIZE 00000297 BYTES
; FUNCTION CHUNK AT 6385 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 63B4 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 63E3 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 6412 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 6441 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 649F SIZE 00000021 BYTES
; FUNCTION CHUNK AT 64CE SIZE 00000021 BYTES
; FUNCTION CHUNK AT 64FD SIZE 00000021 BYTES
; FUNCTION CHUNK AT 652C SIZE 00000021 BYTES
; FUNCTION CHUNK AT 655B SIZE 00000021 BYTES
; FUNCTION CHUNK AT 658A SIZE 00000021 BYTES
; FUNCTION CHUNK AT 65B9 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 65E8 SIZE 00000021 BYTES
; FUNCTION CHUNK AT 6617 SIZE 0000002D BYTES
; FUNCTION CHUNK AT 6959 SIZE 00000310 BYTES
; FUNCTION CHUNK AT 745C SIZE 00000393 BYTES
; FUNCTION CHUNK AT 7A72 SIZE 000002AE BYTES
; FUNCTION CHUNK AT 8DB0 SIZE 00000005 BYTES
; FUNCTION CHUNK AT 8DB8 SIZE 00000005 BYTES

		test	byte [si+17h], 1
		jz	loc_16BB0
		push	si
		call	sub_154F4
		test	BYTE [flag_playsetttings], 10h
		jnz	lc_perfrm_interpol2
		cmp	BYTE [byte_24625], 1
		jz	loc_16959
		xor	edx, edx
		mov	ax, [word_245E4]
		and	eax, 0Fh
		jmp	WORD [cs:offs_noninterp2+eax*2]


loc_160D0:				; DATA XREF: seg000:8DDEo
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_160E0:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DDCo
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_160F0:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DDAo
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16100:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DD8o
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16110:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DD6o
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16120:				; CODE XREF: sub_137D5+39j
					; eff_139B9+86j ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16130:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DD2o
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16140:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DD0o
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16150:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DCEo
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16160:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DCCo
		mov	dl, [es:si]
		add	cl, ch

loc_16165:				; CODE XREF: snd_initialze+13j
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16170:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DCAo
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16180:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DC8o
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_16190:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DC6o
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_161A0:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DC4o
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_161B0:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DC2o
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		add	di, 8

loc_161C0:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:offs_noninterp2o
		cmp	BYTE [byte_24683], 0
		jz	loc_1578C

loc_161C9:				; CODE XREF: sub_1609F+211j
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+8],	ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+10h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+18h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+20h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+28h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+30h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+38h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+40h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+48h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+50h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+58h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+60h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+68h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+70h], ax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		adc	si, bp
		mov	[di+78h], ax
		add	di, 80h	; 'Ä'
		dec	BYTE [byte_24683]
		jnz	loc_161C9
		jmp	loc_1578C
; ---------------------------------------------------------------------------

lc_perfrm_interpol2:			; CODE XREF: sub_1609F+11j
		mov	al, ch
		cmp	al, [cs:byte_16379]
		jz	short loc_1633C
		mov	[cs:byte_16379], al
		mov	[cs:byte_163A8], al
		mov	[cs:byte_163D7], al
		mov	[cs:byte_16406], al
		mov	[cs:byte_16435], al
		mov	byte [cs:unk_16464], al
		mov	[cs:byte_16493], al
		mov	[cs:byte_164C2], al
		mov	[cs:byte_164F1], al
		mov	[cs:byte_16520], al
		mov	[cs:byte_1654F], al
		mov	[cs:byte_1657E], al
		mov	byte [cs:unk_165AD], al
		mov	[cs:byte_165DC], al
		mov	[cs:byte_1660B], al
		mov	[cs:byte_16646], al
		mov	[cs:byte_16672], al
		mov	[cs:byte_1669F], al
		mov	[cs:byte_166CC], al
		mov	[cs:byte_166F9], al
		mov	[cs:byte_16726], al
		mov	[cs:byte_16753], al
		mov	[cs:byte_16780], al
		mov	[cs:byte_167AD], al
		mov	[cs:byte_167DA], al
		mov	[cs:byte_16807], al
		mov	[cs:byte_16834], al
		mov	[cs:byte_16861], al
		mov	[cs:byte_1688E], al
		mov	[cs:byte_168BB], al
		mov	[cs:byte_168E8], al

loc_1633C:				; CODE XREF: sub_1609F+21Fj
		and	ecx, 0FFh
		mov	ax, [word_245E4]
		and	eax, 0Fh
		xor	edx, edx
		jmp	WORD [cs:offs_interpol2+eax*2]

loc_16356:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DFEo
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]

loc_16369:				; CODE XREF: snd_initialze+13j
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16379	db 0			; DATA XREF: sub_1609F+21Ar
					; sub_1609F+221w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_16385:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_163A8	db 0			; DATA XREF: sub_1609F+225w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_163B4:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_163D7	db 0			; DATA XREF: sub_1609F+229w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_163E3:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16406	db 0			; DATA XREF: sub_1609F+22Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_16412:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16435	db 0			; DATA XREF: sub_1609F+231w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_16441:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db 80h
		db 0C1h	; ¡
unk_16464	db    0			; DATA XREF: sub_1609F+235w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax

loc_1646D:
		add	di, 8

loc_16470:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16493	db 0			; DATA XREF: sub_1609F+239w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_1649F:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_164C2	db 0			; DATA XREF: sub_1609F+23Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_164CE:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_164F1	db 0			; DATA XREF: sub_1609F+241w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_164FD:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16520	db 0			; DATA XREF: sub_1609F+245w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_1652C:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_1654F	db 0			; DATA XREF: sub_1609F+249w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_1655B:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde

loc_16568:
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_1657E	db 0			; DATA XREF: sub_1609F+24Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_1658A:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db 80h
		db 0C1h	; ¡
unk_165AD	db    0			; DATA XREF: sub_1609F+251w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_165B9:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_165DC	db 0			; DATA XREF: sub_1609F+255w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_165E8:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_1660B	db 0			; DATA XREF: sub_1609F+259w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_16617:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		cmp	BYTE [byte_24683], 0
		jz	loc_1578C

loc_16620:				; CODE XREF: seg000:6904j
		xor	edx, edx
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16646	db 0			; DATA XREF: sub_1609F+25Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16672	db 0			; DATA XREF: sub_1609F+261w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+8],	eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde

loc_16689:
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_1669F	db 0			; DATA XREF: sub_1609F+265w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+10h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_166CC	db 0			; DATA XREF: sub_1609F+269w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+18h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_166F9	db 0			; DATA XREF: sub_1609F+26Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+20h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16726	db 0			; DATA XREF: sub_1609F+271w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+28h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16753	db 0			; DATA XREF: sub_1609F+275w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+30h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde

loc_1676A:				; CODE XREF: snd_initialze+13j
					; snd_initialze+13j
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16780	db 0			; DATA XREF: sub_1609F+279w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+38h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_167AD	db 0			; DATA XREF: sub_1609F+27Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+40h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_167DA	db 0			; DATA XREF: sub_1609F+281w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+48h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16807	db 0			; DATA XREF: sub_1609F+285w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+50h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16834	db 0			; DATA XREF: sub_1609F+289w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+58h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_16861	db 0			; DATA XREF: sub_1609F+28Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+60h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_1688E	db 0			; DATA XREF: sub_1609F+291w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+68h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_168BB	db 0			; DATA XREF: sub_1609F+295w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+70h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, word [ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
byte_168E8	db 0			; DATA XREF: sub_1609F+299w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+78h], eax
		add	di, 80h	; 'Ä'
		mov	dx, loc_16900
		cmp	BYTE [byte_24616], 1
		jz	short loc_1690B

loc_16900:				; DATA XREF: seg000:68F6o
		dec	BYTE [byte_24683]
		jnz	loc_16620
		jmp	loc_1578C
; ---------------------------------------------------------------------------

loc_1690B:				; CODE XREF: seg000:5E39j seg000:68FEj
		mov	ax, [word_24614]
		cmp	al, ah
		ja	short loc_16929
		add	al, 4
		cmp	al, ah
		jnb	short loc_16942
		mov	byte [word_24614], al
		movzx	ebx, al
		shl	ebx, 9
		add	bx, vlm_byte_table
		jmp	dx
; ---------------------------------------------------------------------------

loc_16929:				; CODE XREF: seg000:6910j
		sub	al, 4
		jbe	short loc_16942
		cmp	al, ah
		jbe	short loc_16942
		mov	byte [word_24614], al
		movzx	ebx, al
		shl	ebx, 9
		add	bx, vlm_byte_table
		jmp	dx
; ---------------------------------------------------------------------------

loc_16942:				; CODE XREF: seg000:6916j seg000:692Bj ...
		mov	byte [word_24614], ah
		mov	BYTE [byte_24616], 0
		movzx	ebx, ah
		shl	ebx, 9
		add	bx, vlm_byte_table
		jmp	dx
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_16959:				; CODE XREF: sub_1609F+1Aj
		xor	edx, edx
		mov	ax, [word_245E4]
		and	eax, 0Fh

loc_16963:				; CODE XREF: snd_initialze+13j
		jmp	WORD [cs:off_18E00+eax*2]

loc_1696C:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_1697F:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_16992:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_169A5:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_169B8:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_169CB:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_169DE:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_169F1:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_16A04:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_16A17:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_16A2A:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_16A3D:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_16A50:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_16A63:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_16A76:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		add	di, 8

loc_16A89:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj ...
		cmp	BYTE [byte_24683], 0
		jz	loc_1578C

loc_16A92:				; CODE XREF: sub_1609F+B0Aj
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+8],	eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+10h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+18h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+20h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+28h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+30h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+38h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+40h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+48h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+50h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+58h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+60h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+68h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+70h], eax
		mov	dl, [es:si]
		add	cl, ch
		mov	ax, [ebx+edx*2]
		cwde
		adc	si, bp
		mov	[di+78h], eax
		add	di, 80h	; 'Ä'
		dec	BYTE [byte_24683]
		jnz	loc_16A92
		jmp	loc_1578C
; ---------------------------------------------------------------------------

loc_16BB0:				; CODE XREF: sub_1609F+4j
		mov	cx, [word_245E4]
		mov	bx, cx
		shr	cx, 4
		xor	eax, eax
		and	bx, 0Fh
		shl	bx, 1
		jmp	WORD [cs:off_18E80+bx]

loc_16BC6:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16BCC:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16BD2:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16BD8:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16BDE:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16BE4:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16BEA:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16BF0:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16BF6:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16BFC:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16C02:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16C08:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16C0E:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16C14:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16C1A:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	[di], eax
		add	di, 8

loc_16C20:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		jcxz locret_16C68

loc_16C22:				; CODE XREF: sub_1609F:loc_16C66j
		mov	[di], eax
		mov	[di+8],	eax
		mov	[di+10h], eax
		mov	[di+18h], eax
		mov	[di+20h], eax
		mov	[di+28h], eax
		mov	[di+30h], eax
		mov	[di+38h], eax
		mov	[di+40h], eax
		mov	[di+48h], eax
		mov	[di+50h], eax
		mov	[di+58h], eax
		mov	[di+60h], eax
		mov	[di+68h], eax
		mov	[di+70h], eax
		mov	[di+78h], eax
		add	di, 80h	; 'Ä'
		dec	cx

loc_16C66:				; CODE XREF: snd_initialze+13j
		jnz	short loc_16C22

locret_16C68:				; CODE XREF: sub_1609F:loc_16C20j
		retn
; END OF FUNCTION CHUNK	FOR sub_1609F

; =============== S U B	R O U T	I N E =======================================


sub_16C69:		; CODE XREF: sub_13017:loc_13038p
					; proaud_14700+783p ...

; FUNCTION CHUNK AT 71D3 SIZE 0000008C BYTES
; FUNCTION CHUNK AT 77EF SIZE 00000035 BYTES

		call	ems_save_mapctx
		cld
		mov	ax, [word_245E8]
		mov	[word_245E4], ax
		dec	WORD [word_245EE]
		jnz	short loc_16C88
		call	sub_140B6
		mov	ax, [word_245EA]
		mov	[word_245E4], ax
		mov	ax, [word_245EC]
		mov	[word_245EE], ax

loc_16C88:				; CODE XREF: sub_16C69+Ej
		mov	BYTE [byte_24682], 0
		cmp	BYTE [byte_24623], 1
		jz	loc_171D3
		mov	si, volume_25908
		mov	cx, [word_245D4]

loc_16C9D:				; CODE XREF: sub_16C69+59j
		cmp	byte [si+1Dh], 0
		jnz	short loc_16CBE
		push	cx
		push	si
		mov	di, chrin
		test	BYTE [byte_24682], 1
		jnz	short loc_16CB9
		or	BYTE [byte_24682], 1
		call	sub_1609F
		jmp	short loc_16CBC
; ---------------------------------------------------------------------------

loc_16CB9:				; CODE XREF: sub_16C69+44j
		call	sub_15577

loc_16CBC:				; CODE XREF: sub_16C69+4Ej
		pop	si
		pop	cx

loc_16CBE:				; CODE XREF: sub_16C69+38j
		add	si, 50h	; 'P'
		dec	cx
		jnz	short loc_16C9D
		mov	di, [word_24600]
		mov	cx, [word_245E4]
		mov	si, (chrin+1)
		mov	es, word [dma_buf_pointer+2]
		mov	ax, 1000h
		sub	ax, di
		cmp	ax, cx
		ja	short loc_16CEB
		mov	bx, cx
		sub	bx, ax
		mov	cx, ax
		push	bx
		call	sub_16CF6
		pop	cx
		xor	di, di
		jcxz loc_16CEE

loc_16CEB:				; CODE XREF: sub_16C69+71j
		call	sub_16CF6

loc_16CEE:				; CODE XREF: sub_16C69+80j
		mov	[word_24600], di
		call	ems_restore_mapctx
		retn


; =============== S U B	R O U T	I N E =======================================


sub_16CF6:		; CODE XREF: sub_16C69+7Ap
					; sub_16C69:loc_16CEBp
		cmp	BYTE [byte_24625], 1
		jz	loc_16E24
		mov	bx, cx
		and	bx, 0Fh
		shl	bx, 1
		jmp	WORD [cs:off_18EA0+bx]

loc_16D0B:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D16:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D21:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D2C:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D37:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D42:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D4D:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D58:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al

loc_16D5F:
		add	si, 8
		inc	di

loc_16D63:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D6E:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D79:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D84:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D8F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16D9A:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16DA5:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		xor	al, 80h
		mov	[es:di], al
		add	si, 8
		inc	di

loc_16DB0:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		shr	cx, 4
		jz	short locret_16E23
		mov	edx, 80808080h

loc_16DBB:				; CODE XREF: sub_16CF6+12Bj
		mov	al, [si+10h]
		mov	ah, [si+18h]
		shl	eax, 10h
		mov	al, [si]
		mov	ah, [si+8]
		xor	eax, edx
		mov	[es:di], eax
		mov	al, [si+30h]
		mov	ah, [si+38h]
		shl	eax, 10h
		mov	al, [si+20h]
		mov	ah, [si+28h]
		xor	eax, edx
		mov	[es:di+4], eax
		mov	al, [si+50h]
		mov	ah, [si+58h]
		shl	eax, 10h
		mov	al, [si+40h]
		mov	ah, [si+48h]
		xor	eax, edx
		mov	[es:di+8], eax
		mov	al, [si+70h]
		mov	ah, [si+78h]
		shl	eax, 10h
		mov	al, [si+60h]
		mov	ah, [si+68h]
		xor	eax, edx
		mov	[es:di+0Ch], eax
		add	si, 80h	; 'Ä'
		add	di, 10h
		dec	cx
		jnz	short loc_16DBB

locret_16E23:				; CODE XREF: sub_16CF6+BDj
		retn
; ---------------------------------------------------------------------------

loc_16E24:				; CODE XREF: sub_16CF6+5j
		and	si, 0FFFCh
		mov	edx, 7FFFh
		mov	ebp, 0FFFF8000h
		mov	bx, cx
		and	bx, 0Fh
		shl	bx, 1
		jmp	WORD [cs:off_18EC0+bx]

loc_16E3F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16E56
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16E56:				; DATA XREF: sub_16CF6+14Fo
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16E5D:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8		; CODE XREF: sub_137D5+39j
					; eff_139B9+86j ...
		mov	bx, loc_16E74
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16E74:				; DATA XREF: sub_16CF6+16Do
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16E7B:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16E92
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16E92:				; DATA XREF: sub_16CF6+18Bo
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16E99:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16EB0
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16EB0:				; DATA XREF: sub_16CF6+1A9o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16EB7:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16ECE
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16ECE:				; DATA XREF: sub_16CF6+1C7o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16ED5:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16EEC
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16EEC:				; DATA XREF: sub_16CF6+1E5o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16EF3:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16F0A
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16F0A:				; DATA XREF: sub_16CF6+203o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16F11:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16F28
		cmp	eax, ebp

loc_16F1D:				; CODE XREF: snd_initialze+13j
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16F28:				; DATA XREF: sub_16CF6+221o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16F2F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16F46
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16F46:				; DATA XREF: sub_16CF6+23Fo
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16F4D:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16F64
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16F64:				; DATA XREF: sub_16CF6+25Do
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16F6B:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16F82
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16F82:				; DATA XREF: sub_16CF6+27Bo
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16F89:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16FA0
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16FA0:				; DATA XREF: sub_16CF6+299o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16FA7:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16FBE
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16FBE:				; DATA XREF: sub_16CF6+2B7o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16FC5:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16FDC
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16FDC:				; DATA XREF: sub_16CF6+2D5o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_16FE3:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, loc_16FFA
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_16FFA:				; DATA XREF: sub_16CF6+2F3o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_17001:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		shr	cx, 4
		jz	locret_171D2

loc_17008:				; CODE XREF: sub_16CF6+4D8j
		mov	eax, [si]
		mov	bx, loc_1701C
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1701C:				; DATA XREF: sub_16CF6+315o
		xor	ah, 80h
		mov	[es:di], ah
		mov	eax, [si+8]
		mov	bx, loc_17037
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17037:				; DATA XREF: sub_16CF6+330o
		xor	ah, 80h
		mov	[es:di+1], ah
		mov	eax, [si+10h]
		mov	bx, loc_17053
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17053:				; DATA XREF: sub_16CF6+34Co
		xor	ah, 80h
		mov	[es:di+2], ah
		mov	eax, [si+18h]
		mov	bx, loc_1706F
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1706F:				; DATA XREF: sub_16CF6+368o
		xor	ah, 80h
		mov	[es:di+3], ah
		mov	eax, [si+20h]
		mov	bx, loc_1708B
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1708B:				; DATA XREF: sub_16CF6+384o
		xor	ah, 80h
		mov	[es:di+4], ah
		mov	eax, [si+28h]
		mov	bx, loc_170A7
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_170A7:				; DATA XREF: sub_16CF6+3A0o
		xor	ah, 80h
		mov	[es:di+5], ah
		mov	eax, [si+30h]
		mov	bx, loc_170C3
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_170C3:				; DATA XREF: sub_16CF6+3BCo
		xor	ah, 80h
		mov	[es:di+6], ah
		mov	eax, [si+38h]
		mov	bx, loc_170DF
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_170DF:				; DATA XREF: sub_16CF6+3D8o
		xor	ah, 80h
		mov	[es:di+7], ah
		mov	eax, [si+40h]
		mov	bx, loc_170FB
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_170FB:				; DATA XREF: sub_16CF6+3F4o
		xor	ah, 80h
		mov	[es:di+8], ah
		mov	eax, [si+48h]
		mov	bx, loc_17117
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17117:				; DATA XREF: sub_16CF6+410o
		xor	ah, 80h
		mov	[es:di+9], ah
		mov	eax, [si+50h]
		mov	bx, loc_17133
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17133:				; DATA XREF: sub_16CF6+42Co
		xor	ah, 80h
		mov	[es:di+0Ah], ah
		mov	eax, [si+58h]
		mov	bx, loc_1714F
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1714F:				; DATA XREF: sub_16CF6+448o
		xor	ah, 80h
		mov	[es:di+0Bh], ah
		mov	eax, [si+60h]
		mov	bx, loc_1716B
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1716B:				; DATA XREF: sub_16CF6+464o
		xor	ah, 80h
		mov	[es:di+0Ch], ah
		mov	eax, [si+68h]
		mov	bx, loc_17187
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17187:				; DATA XREF: sub_16CF6+480o
		xor	ah, 80h
		mov	[es:di+0Dh], ah
		mov	eax, [si+70h]
		mov	bx, loc_171A3
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_171A3:				; DATA XREF: sub_16CF6+49Co
		xor	ah, 80h
		mov	[es:di+0Eh], ah
		mov	eax, [si+78h]
		mov	bx, loc_171BF
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_171BF:				; DATA XREF: sub_16CF6+4B8o
		xor	ah, 80h
		mov	[es:di+0Fh], ah
		add	si, 80h	; 'Ä'
		add	di, 10h
		dec	cx
		jnz	loc_17008

locret_171D2:				; CODE XREF: sub_16CF6+30Ej
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_16C69

loc_171D3:				; CODE XREF: sub_16C69+29j
		mov	cx, [word_245D4]
		mov	si, volume_25908

loc_171DA:				; CODE XREF: sub_16C69+5B7j
		push	cx
		push	si
		cmp	byte [si+1Dh], 0
		jnz	short loc_1721A
		cmp	byte [si+3Ah], 0
		jz	short loc_17202
		mov	di, [off_245E0]
		test	BYTE [byte_24682], 1
		jz	short loc_171F8
		call	sub_15577
		jmp	short loc_1721A
; ---------------------------------------------------------------------------

loc_171F8:				; CODE XREF: sub_16C69+588j
		or	BYTE [byte_24682], 1
		call	sub_1609F
		jmp	short loc_1721A
; ---------------------------------------------------------------------------

loc_17202:				; CODE XREF: sub_16C69+57Dj
		mov	di, [off_245E2]
		test	BYTE [byte_24682], 2
		jz	short loc_17212
		call	sub_15577
		jmp	short loc_1721A
; ---------------------------------------------------------------------------

loc_17212:				; CODE XREF: sub_16C69+5A2j
		or	BYTE [byte_24682], 2
		call	sub_1609F

loc_1721A:				; CODE XREF: sub_16C69+577j
					; sub_16C69+58Dj ...
		pop	si
		pop	cx
		add	si, 50h	; 'P'
		dec	cx
		jnz	short loc_171DA
		cmp	BYTE [bit_mode], 16
		jz	lc_16bit
		mov	di, [word_24600]
		mov	cx, [word_245E4]
		mov	si, (chrin+1)
		mov	es, word [dma_buf_pointer+2]
		mov	ax, 1000h
		sub	ax, di
		shl	cx, 1
		cmp	ax, cx
		ja	short loc_17254
		mov	bx, cx
		sub	bx, ax
		mov	cx, ax
		push	bx
		call	sub_1725F
		pop	cx
		xor	di, di
		jcxz loc_17257

loc_17254:				; CODE XREF: sub_16C69+5DAj
		call	sub_1725F

loc_17257:				; CODE XREF: sub_16C69+5E9j
		mov	[word_24600], di
		call	ems_restore_mapctx
		retn
; END OF FUNCTION CHUNK	FOR sub_16C69

; =============== S U B	R O U T	I N E =======================================


sub_1725F:		; CODE XREF: sub_16C69+5E3p
					; sub_16C69:loc_17254p
		cmp	BYTE [byte_24625], 1
		jz	loc_17441
		or	si, 1
		mov	edx, 80808080h
		shr	cx, 1
		mov	bx, cx
		and	bx, 0Fh
		shl	bx, 1
		jmp	WORD [cs:off_18EE0+bx]

loc_1727F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_1728F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_1729F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_172AF:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_172BF:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_172CF:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_172DF:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_172EF:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_172FF:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_1730F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_1731F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_1732F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_1733F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_1734F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_1735F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	al, [si]
		mov	ah, [si+4]
		add	si, 8
		xor	ax, dx
		mov	[es:di], ax
		add	di, 2

loc_1736F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		shr	cx, 4
		jz	locret_17440

loc_17376:				; CODE XREF: sub_1725F+1DDj
		mov	al, [si+8]
		mov	bl, [si+18h]
		mov	ah, [si+0Ch]
		mov	bh, [si+1Ch]
		shl	eax, 10h
		shl	ebx, 10h
		mov	al, [si]
		mov	bl, [si+10h]
		mov	ah, [si+4]
		mov	bh, [si+14h]
		xor	eax, edx
		xor	ebx, edx
		mov	[es:di], eax
		mov	[es:di+4], ebx
		mov	al, [si+28h]
		mov	bl, [si+38h]
		mov	ah, [si+2Ch]
		mov	bh, [si+3Ch]
		shl	eax, 10h
		shl	ebx, 10h
		mov	al, [si+20h]
		mov	bl, [si+30h]
		mov	ah, [si+24h]
		mov	bh, [si+34h]
		xor	eax, edx
		xor	ebx, edx
		mov	[es:di+8], eax
		mov	[es:di+0Ch], ebx
		mov	al, [si+48h]
		mov	bl, [si+58h]
		mov	ah, [si+4Ch]
		mov	bh, [si+5Ch]
		shl	eax, 10h
		shl	ebx, 10h
		mov	al, [si+40h]
		mov	bl, [si+50h]
		mov	ah, [si+44h]
		mov	bh, [si+54h]
		xor	eax, edx
		xor	ebx, edx
		mov	[es:di+10h], eax
		mov	[es:di+14h], ebx
		mov	al, [si+68h]
		mov	bl, [si+78h]
		mov	ah, [si+6Ch]
		mov	bh, [si+7Ch]
		shl	eax, 10h
		shl	ebx, 10h
		mov	al, [si+60h]
		mov	bl, [si+70h]
		mov	ah, [si+64h]
		mov	bh, [si+74h]
		xor	eax, edx
		xor	ebx, edx
		mov	[es:di+18h], eax
		mov	[es:di+1Ch], ebx
		add	si, 80h	; 'Ä'
		add	di, 20h	; ' '
		dec	cx
		jnz	loc_17376

locret_17440:				; CODE XREF: sub_1725F+113j
		retn
; ---------------------------------------------------------------------------

loc_17441:				; CODE XREF: sub_1725F+5j
		and	si, 0FFFCh
		mov	edx, 7FFFh
		mov	ebp, 0FFFF8000h
		mov	bx, cx
		and	bx, 0Fh
		shl	bx, 1
		jmp	WORD [cs:off_18F00+bx]

; START	OF FUNCTION CHUNK FOR sub_1609F

loc_1745C:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17473
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17473:				; DATA XREF: sub_1609F+13C3o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_1747A:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17491
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17491:				; DATA XREF: sub_1609F+13E1o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_17498:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_174AF
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_174AF:				; DATA XREF: sub_1609F+13FFo
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_174B6:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_174CD
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_174CD:				; DATA XREF: sub_1609F+141Do
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_174D4:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_174EB
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_174EB:				; DATA XREF: sub_1609F+143Bo
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_174F2:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17509
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17509:				; DATA XREF: sub_1609F+1459o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_17510:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17527
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17527:				; DATA XREF: sub_1609F+1477o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_1752E:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17545
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17545:				; DATA XREF: sub_1609F+1495o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_1754C:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]

loc_1754F:				; CODE XREF: snd_initialze+13j
		add	si, 4
		mov	bx, loc_17563
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17563:				; DATA XREF: sub_1609F+14B3o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_1756A:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17581
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17581:				; DATA XREF: sub_1609F+14D1o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_17588:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_1759F
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1759F:				; DATA XREF: sub_1609F+14EFo
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_175A6:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_175BD
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_175BD:				; DATA XREF: sub_1609F+150Do
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_175C4:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_175DB
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_175DB:				; DATA XREF: sub_1609F+152Bo
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_175E2:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_175F9
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_175F9:				; DATA XREF: sub_1609F+1549o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_17600:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17617
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17617:				; DATA XREF: sub_1609F+1567o
		xor	ah, 80h
		mov	[es:di], ah
		inc	di

loc_1761E:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		shr	cx, 4
		jz	locret_177EE

loc_17625:				; CODE XREF: sub_1609F+174Bj
		mov	eax, [si]
		mov	bx, loc_17639
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17639:				; DATA XREF: sub_1609F+1589o
		xor	ah, 80h
		mov	[es:di], ah
		mov	eax, [si+4]
		mov	bx, loc_17654
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17654:				; DATA XREF: sub_1609F+15A4o
		xor	ah, 80h
		mov	[es:di+1], ah
		mov	eax, [si+8]
		mov	bx, loc_17670
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17670:				; DATA XREF: sub_1609F+15C0o
		xor	ah, 80h
		mov	[es:di+2], ah
		mov	eax, [si+0Ch]
		mov	bx, loc_1768C
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1768C:				; DATA XREF: sub_1609F+15DCo
		xor	ah, 80h
		mov	[es:di+3], ah
		mov	eax, [si+10h]
		mov	bx, loc_176A8
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_176A8:				; DATA XREF: sub_1609F+15F8o
		xor	ah, 80h
		mov	[es:di+4], ah
		mov	eax, [si+14h]
		mov	bx, loc_176C4
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_176C4:				; DATA XREF: sub_1609F+1614o
		xor	ah, 80h
		mov	[es:di+5], ah
		mov	eax, [si+18h]
		mov	bx, loc_176E0
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_176E0:				; DATA XREF: sub_1609F+1630o
		xor	ah, 80h
		mov	[es:di+6], ah
		mov	eax, [si+1Ch]
		mov	bx, loc_176FC
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_176FC:				; DATA XREF: sub_1609F+164Co
		xor	ah, 80h
		mov	[es:di+7], ah
		mov	eax, [si+20h]
		mov	bx, loc_17718
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17718:				; DATA XREF: sub_1609F+1668o
		xor	ah, 80h
		mov	[es:di+8], ah
		mov	eax, [si+24h]
		mov	bx, loc_17734
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17734:				; DATA XREF: sub_1609F+1684o
		xor	ah, 80h
		mov	[es:di+9], ah
		mov	eax, [si+28h]
		mov	bx, loc_17750
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17750:				; DATA XREF: sub_1609F+16A0o
		xor	ah, 80h
		mov	[es:di+0Ah], ah
		mov	eax, [si+2Ch]
		mov	bx, loc_1776C
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1776C:				; DATA XREF: sub_1609F+16BCo
		xor	ah, 80h
		mov	[es:di+0Bh], ah
		mov	eax, [si+30h]
		mov	bx, loc_17788
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17788:				; DATA XREF: sub_1609F+16D8o
		xor	ah, 80h
		mov	[es:di+0Ch], ah
		mov	eax, [si+34h]
		mov	bx, loc_177A4
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_177A4:				; DATA XREF: sub_1609F+16F4o
		xor	ah, 80h
		mov	[es:di+0Dh], ah
		mov	eax, [si+38h]
		mov	bx, loc_177C0
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_177C0:				; DATA XREF: sub_1609F+1710o
		xor	ah, 80h
		mov	[es:di+0Eh], ah
		mov	eax, [si+3Ch]
		mov	bx, loc_177DC
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_177DC:				; DATA XREF: sub_1609F+172Co
		xor	ah, 80h
		mov	[es:di+0Fh], ah
		add	si, 40h	; '@'
		add	di, 10h
		dec	cx
		jnz	loc_17625

locret_177EE:				; CODE XREF: sub_1609F+1582j
		retn
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_16C69

lc_16bit:				; CODE XREF: sub_16C69+5BEj
		mov	di, [word_24600]
		mov	cx, [word_245E4]
		mov	si, chrin
		mov	es, word [dma_buf_pointer+2]
		mov	ax, 1000h
		sub	ax, di
		shr	ax, 2
		cmp	cx, ax
		jbe	short loc_17819
		mov	bx, cx
		sub	bx, ax
		mov	cx, ax
		push	bx
		call	sub_17824
		pop	cx
		xor	di, di
		jcxz loc_1781C

loc_17819:				; CODE XREF: sub_16C69+B9Fj
		call	sub_17824

loc_1781C:				; CODE XREF: sub_16C69+BAEj
		mov	[word_24600], di
		call	ems_restore_mapctx
		retn
; END OF FUNCTION CHUNK	FOR sub_16C69

; =============== S U B	R O U T	I N E =======================================


sub_17824:		; CODE XREF: sub_16C69+BA8p
					; sub_16C69:loc_17819p
		cmp	BYTE [byte_24625], 1
		jz	loc_17A58
		mov	bx, cx
		and	bx, 0Fh
		shl	bx, 1
		jmp	WORD [cs:off_18F20+bx]

loc_17839:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_1784C:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_1785F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_17872:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_17885:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_17898:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_178AB:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_178BE:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_178D1:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_178E4:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_178F7:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_1790A:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_1791D:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_17930:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_17943:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		add	si, 8
		mov	[es:di], eax
		add	di, 4

loc_17956:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		shr	cx, 4
		jz	locret_17A57

loc_1795D:				; CODE XREF: sub_17824+22Fj
		mov	ax, [si+4]
		shl	eax, 10h
		mov	ax, [si]
		mov	[es:di], eax
		mov	ax, [si+0Ch]
		shl	eax, 10h
		mov	ax, [si+8]
		mov	[es:di+4], eax
		mov	ax, [si+14h]
		shl	eax, 10h
		mov	ax, [si+10h]
		mov	[es:di+8], eax
		mov	ax, [si+1Ch]
		shl	eax, 10h
		mov	ax, [si+18h]
		mov	[es:di+0Ch], eax
		mov	ax, [si+24h]
		shl	eax, 10h
		mov	ax, [si+20h]
		mov	[es:di+10h], eax
		mov	ax, [si+2Ch]
		shl	eax, 10h
		mov	ax, [si+28h]
		mov	[es:di+14h], eax
		mov	ax, [si+34h]
		shl	eax, 10h
		mov	ax, [si+30h]
		mov	[es:di+18h], eax
		mov	ax, [si+3Ch]
		shl	eax, 10h
		mov	ax, [si+38h]
		mov	[es:di+1Ch], eax
		mov	ax, [si+44h]
		shl	eax, 10h
		mov	ax, [si+40h]
		mov	[es:di+20h], eax
		mov	ax, [si+4Ch]
		shl	eax, 10h
		mov	ax, [si+48h]
		mov	[es:di+24h], eax
		mov	ax, [si+54h]
		shl	eax, 10h
		mov	ax, [si+50h]
		mov	[es:di+28h], eax
		mov	ax, [si+5Ch]
		shl	eax, 10h
		mov	ax, [si+58h]
		mov	[es:di+2Ch], eax
		mov	ax, [si+64h]
		shl	eax, 10h
		mov	ax, [si+60h]
		mov	[es:di+30h], eax
		mov	ax, [si+6Ch]
		shl	eax, 10h
		mov	ax, [si+68h]
		mov	[es:di+34h], eax
		mov	ax, [si+74h]
		shl	eax, 10h
		mov	ax, [si+70h]
		mov	[es:di+38h], eax
		mov	ax, [si+7Ch]
		shl	eax, 10h
		mov	ax, [si+78h]
		mov	[es:di+3Ch], eax
		add	si, 80h	; 'Ä'
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_1795D

locret_17A57:				; CODE XREF: sub_17824+135j
		retn
; ---------------------------------------------------------------------------

loc_17A58:				; CODE XREF: sub_17824+5j
		mov	edx, 7FFFh
		mov	ebp, 0FFFF8000h
		shl	cx, 1
		mov	bx, cx
		and	bx, 0Fh
		shl	bx, 1
		jmp	WORD [cs:off_18F40+bx]

; START	OF FUNCTION CHUNK FOR sub_1609F

loc_17A72:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17A89
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17A89:				; DATA XREF: sub_1609F+19D9o
		mov	[es:di], ax
		add	di, 2

loc_17A8F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17AA6
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17AA6:				; DATA XREF: sub_1609F+19F6o
		mov	[es:di], ax
		add	di, 2

loc_17AAC:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17AC3
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17AC3:				; DATA XREF: sub_1609F+1A13o
		mov	[es:di], ax
		add	di, 2

loc_17AC9:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17AE0
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17AE0:				; DATA XREF: sub_1609F+1A30o
		mov	[es:di], ax
		add	di, 2

loc_17AE6:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17AFD
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17AFD:				; DATA XREF: sub_1609F+1A4Do
		mov	[es:di], ax
		add	di, 2

loc_17B03:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17B1A
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17B1A:				; DATA XREF: sub_1609F+1A6Ao
		mov	[es:di], ax
		add	di, 2

loc_17B20:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17B37
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17B37:				; DATA XREF: sub_1609F+1A87o
		mov	[es:di], ax
		add	di, 2

loc_17B3D:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17B54
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17B54:				; DATA XREF: sub_1609F+1AA4o
		mov	[es:di], ax
		add	di, 2

loc_17B5A:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17B71
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17B71:				; DATA XREF: sub_1609F+1AC1o
		mov	[es:di], ax
		add	di, 2

loc_17B77:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17B8E
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17B8E:				; DATA XREF: sub_1609F+1ADEo
		mov	[es:di], ax
		add	di, 2

loc_17B94:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17BAB
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17BAB:				; DATA XREF: sub_1609F+1AFBo
		mov	[es:di], ax
		add	di, 2

loc_17BB1:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17BC8
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17BC8:				; DATA XREF: sub_1609F+1B18o
		mov	[es:di], ax
		add	di, 2

loc_17BCE:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17BE5
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17BE5:				; DATA XREF: sub_1609F+1B35o
		mov	[es:di], ax
		add	di, 2

loc_17BEB:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17C02
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C02:				; DATA XREF: sub_1609F+1B52o
		mov	[es:di], ax
		add	di, 2

loc_17C08:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, loc_17C1F
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C1F:				; DATA XREF: sub_1609F+1B6Fo
		mov	[es:di], ax
		add	di, 2

loc_17C25:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		shr	cx, 4
		jz	nullsub_3

loc_17C2C:				; CODE XREF: seg000:7DC1j
		mov	eax, [si]
		mov	bx, loc_17C40
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C40:				; DATA XREF: sub_1609F+1B90o
		mov	[es:di], ax
		mov	eax, [si+4]
		mov	bx, loc_17C58
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C58:				; DATA XREF: sub_1609F+1BA8o
		mov	[es:di+2], ax
		mov	eax, [si+8]
		mov	bx, loc_17C71
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C71:				; DATA XREF: sub_1609F+1BC1o
		mov	[es:di+4], ax
		mov	eax, [si+0Ch]
		mov	bx, loc_17C8A
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C8A:				; DATA XREF: sub_1609F+1BDAo
		mov	[es:di+6], ax
		mov	eax, [si+10h]
		mov	bx, loc_17CA3
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17CA3:				; DATA XREF: sub_1609F+1BF3o
		mov	[es:di+8], ax
		mov	eax, [si+14h]
		mov	bx, loc_17CBC
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17CBC:				; DATA XREF: sub_1609F+1C0Co
		mov	[es:di+0Ah], ax
		mov	eax, [si+18h]
		mov	bx, loc_17CD5
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17CD5:				; DATA XREF: sub_1609F+1C25o
		mov	[es:di+0Ch], ax
		mov	eax, [si+1Ch]
		mov	bx, loc_17CEE
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17CEE:				; DATA XREF: sub_1609F+1C3Eo
		mov	[es:di+0Eh], ax
		mov	eax, [si+20h]
		mov	bx, loc_17D07
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D07:				; DATA XREF: sub_1609F+1C57o
		mov	[es:di+10h], ax
		mov	eax, [si+24h]
		mov	bx, loc_17D20
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8
; END OF FUNCTION CHUNK	FOR sub_1609F

loc_17D20:				; DATA XREF: sub_1609F+1C70o
		mov	[es:di+12h], ax
		mov	eax, [si+28h]
		mov	bx, loc_17D39
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D39:				; DATA XREF: seg000:7D28o
		mov	[es:di+14h], ax
		mov	eax, [si+2Ch]
		mov	bx, loc_17D52
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D52:				; DATA XREF: seg000:7D41o
		mov	[es:di+16h], ax
		mov	eax, [si+30h]
		mov	bx, loc_17D6B
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D6B:				; DATA XREF: seg000:7D5Ao
		mov	[es:di+18h], ax
		mov	eax, [si+34h]
		mov	bx, loc_17D84
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D84:				; DATA XREF: seg000:7D73o
		mov	[es:di+1Ah], ax
		mov	eax, [si+38h]
		mov	bx, loc_17D9D
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D9D:				; DATA XREF: seg000:7D8Co
		mov	[es:di+1Ch], ax
		mov	eax, [si+3Ch]
		mov	bx, loc_17DB6
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17DB6:				; DATA XREF: seg000:7DA5o
		mov	[es:di+1Eh], ax
		add	si, 40h	; '@'
		add	di, 20h	; ' '
		dec	cx
		jnz	loc_17C2C

; =============== S U B	R O U T	I N E =======================================


nullsub_3:		; CODE XREF: sub_1609F+1B89j
		retn


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


 ; sp-analysis failed

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR gravis_17F7D

loc_18077:				; CODE XREF: gravis_17F7D+11j
		stc
		retn
; END OF FUNCTION CHUNK	FOR gravis_17F7D

; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
asc_182C3	db 0,0,1,3,0,2,0,4,0,0,0,5,6,0,0,7 ; DATA XREF:	gravis_18216+5r
					; gravis_18216+Fr
asc_182D3	db 0,1,0,2,0,3,4,5	; DATA XREF: gravis_18216+19r
					; gravis_18216+23r

; =============== S U B	R O U T	I N E =======================================


sub_182DB:		; CODE XREF: sub_1279A+44j
					; sub_1279A+5Ep
		mov	BYTE [dma_mode], 44h	; 'D'
		mov	BYTE [byte_24645], 2
		jmp	short loc_182F7


; =============== S U B	R O U T	I N E =======================================


nongravis_182E7:	; CODE XREF: mod_readfile_11F4E+162p
					; mod_readfile_11F4E+19Dp
		mov	BYTE [dma_mode], 48h	; 'H'
		mov	bl, [byte_24673]
		and	bl, 80h
		mov	[byte_24645], bl

loc_182F7:				; CODE XREF: sub_182DB+Aj
					; nongravis_182E7+15j
		cmp	BYTE [byte_2466E], 1
		jz	short loc_182F7
		mov	WORD [word_24636], 0
		mov	bp, ax
		shl	ax, 2
		mov	[word_2460E], cx
		mov	bx, cx
		shr	cx, 2
		add	cx, ax
		jnb	short loc_18338
		jz	short loc_18338
		neg	ax
		shl	ax, 2
		mov	[word_2460E], ax
		mov	cx, ax
		sub	bx, ax
		mov	[word_24636], bx
		add	ax, word [dma_buf_pointer]
		mov	[word_24634], ax
		shr	cx, 4
		add	cx, bp
		mov	[word_24632], cx

loc_18338:				; CODE XREF: gravis_int+E2p
					; nongravis_182E7+2Dj ...
		pushf
		cli
		push	bp
		mov	cl, [dma_channel_0]
		call	dma_186E3
		pop	bp
		mov	bl, 21h	; '!'
		or	bl, [byte_24645]
		cmp	BYTE [dma_channel_0], 4
		jb	short loc_18360
		or	bl, 4
		mov	ax, bp
		and	ax, 0C000h
		shr	bp, 1
		and	bp, 1FFFh
		or	bp, ax

loc_18360:				; CODE XREF: nongravis_182E7+67j
		mov	dx, [gravis_port]
		mov	al, 41h	; 'A'
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		mov	al, 42h	; 'B'
		out	dx, al
		inc	dx
		mov	ax, bp
		out	dx, ax
		dec	dx
		mov	BYTE [byte_2466E], 1
		mov	al, 41h	; 'A'
		out	dx, al
		add	dl, 2
		mov	al, bl
		out	dx, al
		sub	dl, 2
		popf
		retn


; =============== S U B	R O U T	I N E =======================================


adlib_18389:	; CODE XREF: adlib_init+Fp
					; adlib_clean+3p
		xor	ax, ax

loc_1838B:				; CODE XREF: adlib_18389+9j
		call	adlib_18395
		inc	al
		cmp	al, 0E8h ; 'Ë'
		jbe	short loc_1838B
		retn


; =============== S U B	R O U T	I N E =======================================


adlib_18395:	; CODE XREF: adlib_init+15p
					; adlib_init+1Bp ...
		push	ax
		push	dx
		mov	dx, 388h
		out	dx, al
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		inc	dx
		mov	al, ah
		out	dx, al
		dec	dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		pop	dx
		pop	ax
		retn


; =============== S U B	R O U T	I N E =======================================


sb16_detect_port:	; CODE XREF: useless_12D61+22p
					; sb16_init+Fp	...
		cmp	WORD [snd_base_port], 0FFFFh
		jz	short loc_183DE
		mov	ax, [snd_base_port]
		mov	[sb_base_port],	ax
		call	CheckSB
		jnb	short loc_1842D

loc_183DE:				; CODE XREF: sb16_detect_port+5j
		mov	WORD [sb_base_port],	220h
		call	CheckSB
		jnb	short loc_1842D
		mov	WORD [sb_base_port],	240h
		call	CheckSB
		jnb	short loc_1842D
		mov	WORD [sb_base_port],	210h
		call	CheckSB
		jnb	short loc_1842D
		mov	WORD [sb_base_port],	230h
		call	CheckSB
		jnb	short loc_1842D
		mov	WORD [sb_base_port],	250h
		call	CheckSB
		jnb	short loc_1842D
		mov	WORD [sb_base_port],	260h
		call	CheckSB
		jnb	short loc_1842D
		mov	WORD [sb_base_port],	280h
		call	CheckSB
		jnb	short loc_1842D
		stc
		retn
; ---------------------------------------------------------------------------

loc_1842D:				; CODE XREF: sb16_detect_port+10j
					; sb16_detect_port+1Bj	...
		mov	al, 10h
		call	WriteSB
		mov	al, 80h	; 'Ä'
		call	WriteSB
		mov	al, 0E1h ; '·'
		call	WriteSB
		call	ReadSB
		mov	ah, al
		call	ReadSB
		mov	[word_24654], ax
		clc
		retn


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sb_detect_irq

loc_184C3:				; CODE XREF: sb_detect_irq+18j
					; sb_detect_irq+22j ...
		cmp	BYTE [dma_channel], 0FFh
		jz	short loc_184DC
		mov	al, [dma_channel]
		mov	[dma_chn_mask],	al
		cmp	BYTE [bit_mode], 16
		jz	short sb16_sound_on
		call	sb16_18540
		jnb	short sb16_sound_on

loc_184DC:				; CODE XREF: sb_detect_irq+7Fj
		cmp	BYTE [bit_mode], 8
		jz	short loc_18501
		mov	BYTE [dma_chn_mask],	5
		call	sb16_18540
		jnb	short sb16_sound_on
		mov	BYTE [dma_chn_mask],	6
		call	sb16_18540
		jnb	short sb16_sound_on
		mov	BYTE [dma_chn_mask],	7
		call	sb16_18540
		jnb	short sb16_sound_on

loc_18501:				; CODE XREF: sb_detect_irq+98j
		mov	BYTE [dma_chn_mask],	1
		call	sb16_18540
		jnb	short sb16_sound_on
		mov	BYTE [dma_chn_mask],	3
		call	sb16_18540
		jnb	short sb16_sound_on
		mov	BYTE [dma_chn_mask],	0
		call	sb16_18540
		jnb	short sb16_sound_on
		mov	dx, aErrorCouldNot_1 ; "Error: Could not	find DMA!\r\n"
		stc
		retn
; END OF FUNCTION CHUNK	FOR sb_detect_irq

; =============== S U B	R O U T	I N E =======================================


sb16_sound_on:	; CODE XREF: sb16_init:loc_14AFDp
					; sb_detect_irq+8Cj ...
		call	CheckSB
		mov	al, 0D1h ; '—'
		call	WriteSB
		mov	ax, [sb_base_port]
		mov	[snd_base_port], ax
		mov	al, [sb_irq_number]
		mov	[irq_number], al
		mov	al, [dma_chn_mask]
		mov	[dma_channel], al
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


sb16_18540:		; CODE XREF: sb_detect_irq+8Ep
					; sb_detect_irq+9Fp ...
		mov	BYTE [dma_mode], 48h	; 'H'
		cli
		call	CheckSB
		mov	WORD [word_2460E], 2
		mov	DWORD [dma_buf_pointer], 0
		mov	cl, [dma_chn_mask]
		call	dma_186E3
		mov	BYTE [sb_int_counter], 1
		mov	si, sb16_handler_int ; myfunc
		mov	al, [sb_irq_number]
		call	setsnd_handler
		cmp	BYTE [dma_chn_mask],	4
		jnb	short loc_18591
		mov	al, 40h	; '@'
		call	WriteSB
		mov	al, 0D3h ; '”'
		call	WriteSB
		mov	al, 14h
		call	WriteSB
		mov	ax, [word_2460E]
		dec	ax
		call	WriteSB
		mov	al, ah
		call	WriteSB
		jmp	short loc_185B5
; ---------------------------------------------------------------------------

loc_18591:				; CODE XREF: sb16_18540+32j
		mov	al, 42h	; 'B'
		call	WriteSB
		mov	al, 0ACh ; '¨'
		call	WriteSB
		mov	al, 44h	; 'D'
		call	WriteSB
		mov	al, 0B6h ; '∂'
		call	WriteSB
		mov	al, 30h	; '0'
		call	WriteSB
		mov	ax, [word_2460E]
		call	WriteSB
		mov	al, ah
		call	WriteSB

loc_185B5:				; CODE XREF: sb16_18540+4Fj
		sti
		xor	cx, cx

loc_185B8:				; CODE XREF: sb16_18540+7Fj
		cmp	BYTE [sb_int_counter], 1
		jnz	short loc_185CD
		loop	loc_185B8
		call	restore_intvector
		mov	cl, [dma_chn_mask]
		call	set_dmachn_mask
		stc
		retn
; ---------------------------------------------------------------------------

loc_185CD:				; CODE XREF: sb16_18540+7Dj
		call	restore_intvector
		mov	cl, [dma_chn_mask]
		call	set_dmachn_mask
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


; int sb16_handler_int
sb16_handler_int:	; DATA XREF: sb_test_interrupt+5o
					; sb16_18540+24o
		push	ax
		push	dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	dx, [sb_base_port]
		add	dl, 0Eh
		in	al, dx		; DMA controller, 8237A-5.
					; Clear	mask registers.
					; Any OUT enables all 4	channels.
		inc	BYTE [sb_int_counter]
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		pop	dx
		pop	ax
		iret

; ---------------------------------------------------------------------------
		cmp	cl, 4
		jnb	short loc_18631
		xor	al, al
		out	0Ch, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		cmp	cl, 1
		jz	short loc_18616
		cmp	cl, 2
		jz	short loc_1861F
		cmp	cl, 3
		jz	short loc_18628
		in	al, 1		; DMA controller, 8237A-5.
					; channel 0 current word count
		mov	ah, al
		in	al, 1		; DMA controller, 8237A-5.
					; channel 0 current word count
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_18616:				; CODE XREF: seg000:8601j
		in	al, 3		; DMA controller, 8237A-5.
					; channel 1 current word count
		mov	ah, al
		in	al, 3		; DMA controller, 8237A-5.
					; channel 1 current word count
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_1861F:				; CODE XREF: seg000:8606j
		in	al, 5		; DMA controller, 8237A-5.
					; channel 2 current word count
		mov	ah, al
		in	al, 5		; DMA controller, 8237A-5.
					; channel 2 current word count
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_18628:				; CODE XREF: seg000:860Bj
		in	al, 7		; DMA controller, 8237A-5.
					; channel 3 current word count
		mov	ah, al
		in	al, 7		; DMA controller, 8237A-5.
					; channel 3 current word count
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_18631:				; CODE XREF: seg000:85F8j
		xor	al, al
		out	0D8h, al
		cmp	cl, 5
		jz	short loc_1864D
		cmp	cl, 6
		jz	short loc_18656
		cmp	cl, 7
		jz	short loc_1865F
		in	al, 0C2h	; DMA controller, 8237A-5.
					; channel 1 current address
		mov	ah, al
		in	al, 0C2h	; DMA controller, 8237A-5.
					; channel 1 current address
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_1864D:				; CODE XREF: seg000:8638j
		in	al, 0C6h	; DMA controller, 8237A-5.
					; channel 3 current address
		mov	ah, al
		in	al, 0C6h	; DMA controller, 8237A-5.
					; channel 3 current address
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_18656:				; CODE XREF: seg000:863Dj
		in	al, 0CAh	; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		mov	ah, al
		in	al, 0CAh	; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_1865F:				; CODE XREF: seg000:8642j
		in	al, 0CEh	; DMA controller, 8237A-5.
					; Clear	mask registers.
					; Any OUT enables all 4	channels.
		mov	ah, al
		in	al, 0CEh	; DMA controller, 8237A-5.
					; Clear	mask registers.
					; Any OUT enables all 4	channels.
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------
		cmp	cl, 4
		jnb	short loc_186A4
		xor	al, al
		out	0Ch, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		cmp	cl, 1
		jz	short loc_18689
		cmp	cl, 2
		jz	short loc_18692
		cmp	cl, 3
		jz	short loc_1869B
		in	al, 0
		mov	ah, al
		in	al, 0
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_18689:				; CODE XREF: seg000:8674j
		in	al, 2		; DMA controller, 8237A-5.
					; channel 1 current address
		mov	ah, al
		in	al, 2		; DMA controller, 8237A-5.
					; channel 1 current address
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_18692:				; CODE XREF: seg000:8679j
		in	al, 4		; DMA controller, 8237A-5.
					; channel 2 current address
		mov	ah, al
		in	al, 4		; DMA controller, 8237A-5.
					; channel 2 current address
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_1869B:				; CODE XREF: seg000:867Ej
		in	al, 6		; DMA controller, 8237A-5.
					; channel 3 current address
		mov	ah, al
		in	al, 6		; DMA controller, 8237A-5.
					; channel 3 current address
		xchg	al, ah
		retn
; ---------------------------------------------------------------------------

loc_186A4:				; CODE XREF: seg000:866Bj
		xor	al, al
		out	0D8h, al
		cmp	cl, 5
		jz	short loc_186C2
		cmp	cl, 6
		jz	short loc_186CD
		cmp	cl, 7
		jz	short loc_186D8
		in	al, 0C0h	; DMA controller, 8237A-5.
					; channel 0 current address
		mov	ah, al
		in	al, 0C0h	; DMA controller, 8237A-5.
					; channel 0 current address
		xchg	al, ah
		shl	ax, 1
		retn
; ---------------------------------------------------------------------------

loc_186C2:				; CODE XREF: seg000:86ABj
		in	al, 0C4h	; DMA controller, 8237A-5.
					; channel 2 current address
		mov	ah, al
		in	al, 0C4h	; DMA controller, 8237A-5.
					; channel 2 current address
		xchg	al, ah
		shl	ax, 1
		retn
; ---------------------------------------------------------------------------

loc_186CD:				; CODE XREF: seg000:86B0j
		in	al, 0C8h	; DMA 8237A-5. status register bits:
					; 0-3: channel 0-3 has reached terminal	count
					; 4-7: channel 0-3 has a request pending
		mov	ah, al
		in	al, 0C8h	; DMA 8237A-5. status register bits:
					; 0-3: channel 0-3 has reached terminal	count
					; 4-7: channel 0-3 has a request pending
		xchg	al, ah
		shl	ax, 1
		retn
; ---------------------------------------------------------------------------

loc_186D8:				; CODE XREF: seg000:86B5j
		in	al, 0CCh	; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	ah, al
		in	al, 0CCh	; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		xchg	al, ah
		shl	ax, 1
		retn

; =============== S U B	R O U T	I N E =======================================


dma_186E3:		; CODE XREF: proaud_set+59p
					; wss_set+28p ...
		test	byte [config_word+1], 10h
		jz	short loc_186EF
		and	BYTE [dma_mode], 0EFh

loc_186EF:				; CODE XREF: dma_186E3+5j
		cmp	cl, 1
		jz	short loc_18761
		cmp	cl, 2
		jz	loc_187A6
		cmp	cl, 3
		jz	loc_187EB
		cmp	cl, 4
		jz	loc_18830
		cmp	cl, 5
		jz	loc_18878
		cmp	cl, 6
		jz	loc_188C2
		cmp	cl, 7
		jz	loc_1890C
		mov	al, 4
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		xor	al, al
		out	0Ch, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	al, [dma_mode]
		out	0Bh, al		; DMA 8237A-5. mode register bits:
					; 0-1: channel (00=0; 01=1; 10=2; 11=3)
					; 2-3: transfer	type (00=verify=Nop; 01=write; 10=read)
					; 4: 1=enable auto-initialization
					; 5: 1=address increment; 0=address decrement
					; 6-7: 00=demand mode; 01=single; 10=block; 11=cascade
		mov	dx, word [dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, word [dma_buf_pointer]
		adc	dx, 0
		add	ax, word [dword_24694]
		adc	dx, word [dword_24694+2]
		out	0, al
		mov	al, ah
		out	0, al
		mov	al, dl
		out	87h, al		; DMA page register 74LS612:
					; Channel 0 (address bits 16-23)
		mov	ax, [word_2460E]
		dec	ax
		out	1, al		; DMA controller, 8237A-5.
					; channel 0 base address and word count
		mov	al, ah
		out	1, al		; DMA controller, 8237A-5.
					; channel 0 base address and word count
		xor	al, al
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		retn
; ---------------------------------------------------------------------------

loc_18761:				; CODE XREF: dma_186E3+Fj
		mov	al, 5
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		xor	al, al
		out	0Ch, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	al, [dma_mode]
		or	al, 1
		out	0Bh, al		; DMA 8237A-5. mode register bits:
					; 0-1: channel (00=0; 01=1; 10=2; 11=3)
					; 2-3: transfer	type (00=verify=Nop; 01=write; 10=read)
					; 4: 1=enable auto-initialization
					; 5: 1=address increment; 0=address decrement
					; 6-7: 00=demand mode; 01=single; 10=block; 11=cascade
		mov	dx, word [dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, word [dma_buf_pointer]
		adc	dx, 0
		add	ax, word [dword_24694]
		adc	dx, word [dword_24694+2]
		out	2, al		; DMA controller, 8237A-5.
					; channel 1 base address
					; (also	sets current address)
		mov	al, ah
		out	2, al		; DMA controller, 8237A-5.
					; channel 1 base address
					; (also	sets current address)
		mov	al, dl
		out	83h, al		; DMA page register 74LS612:
					; Channel 1 (address bits 16-23)
		mov	ax, [word_2460E]
		dec	ax
		out	3, al		; DMA controller, 8237A-5.
					; channel 1 base address and word count
		mov	al, ah
		out	3, al		; DMA controller, 8237A-5.
					; channel 1 base address and word count
		mov	al, 1
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		retn
; ---------------------------------------------------------------------------

loc_187A6:				; CODE XREF: dma_186E3+14j
		mov	al, 6
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		xor	al, al
		out	0Ch, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	al, [dma_mode]
		or	al, 2
		out	0Bh, al		; DMA 8237A-5. mode register bits:
					; 0-1: channel (00=0; 01=1; 10=2; 11=3)
					; 2-3: transfer	type (00=verify=Nop; 01=write; 10=read)
					; 4: 1=enable auto-initialization
					; 5: 1=address increment; 0=address decrement
					; 6-7: 00=demand mode; 01=single; 10=block; 11=cascade
		mov	dx, word [dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, word [dma_buf_pointer]
		adc	dx, 0
		add	ax, word [dword_24694]
		adc	dx, word [dword_24694+2]
		out	4, al		; DMA controller, 8237A-5.
					; channel 2 base address
					; (also	sets current address)
		mov	al, ah
		out	4, al		; DMA controller, 8237A-5.
					; channel 2 base address
					; (also	sets current address)
		mov	al, dl
		out	81h, al		; DMA page register 74LS612:
					; Channel 2 (diskette DMA)  (address bits 16-23)
		mov	ax, [word_2460E]
		dec	ax
		out	5, al		; DMA controller, 8237A-5.
					; channel 2 base address and word count
		mov	al, ah
		out	5, al		; DMA controller, 8237A-5.
					; channel 2 base address and word count
		mov	al, 2
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		retn
; ---------------------------------------------------------------------------

loc_187EB:				; CODE XREF: dma_186E3+1Bj
		mov	al, 7
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		xor	al, al
		out	0Ch, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	al, [dma_mode]
		or	al, 3
		out	0Bh, al		; DMA 8237A-5. mode register bits:
					; 0-1: channel (00=0; 01=1; 10=2; 11=3)
					; 2-3: transfer	type (00=verify=Nop; 01=write; 10=read)
					; 4: 1=enable auto-initialization
					; 5: 1=address increment; 0=address decrement
					; 6-7: 00=demand mode; 01=single; 10=block; 11=cascade
		mov	dx, word [dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, word [dma_buf_pointer]
		adc	dx, 0
		add	ax, word [dword_24694]
		adc	dx, word [dword_24694+2]
		out	6, al		; DMA controller, 8237A-5.
					; channel 3 base address
					; (also	sets current address)
		mov	al, ah
		out	6, al		; DMA controller, 8237A-5.
					; channel 3 base address
					; (also	sets current address)
		mov	al, dl
		out	82h, al		; DMA page register 74LS612:
					; Channel 3 (hard disk DMA) (address bits 16-23)
		mov	ax, [word_2460E]
		dec	ax
		out	7, al		; DMA controller, 8237A-5.
					; channel 3 base address and word count
		mov	al, ah
		out	7, al		; DMA controller, 8237A-5.
					; channel 3 base address and word count
		mov	al, 3
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		retn
; ---------------------------------------------------------------------------

loc_18830:				; CODE XREF: dma_186E3+22j
		mov	al, 4
		out	0D4h, al
		xor	al, al
		out	0D8h, al
		mov	al, [dma_mode]
		out	0D6h, al
		movzx	edx, word [dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, word [dma_buf_pointer]
		add	eax, edx
		add	eax, [dword_24694]
		shr	eax, 1
		out	0C0h, al	; DMA controller, 8237A-5.
					; channel 0 base address
					; (also	sets current address)
		mov	al, ah
		out	0C0h, al	; DMA controller, 8237A-5.
					; channel 0 base address
					; (also	sets current address)
		shr	eax, 0Fh
		out	8Fh, al		; DMA page register 74LS612:
					; refresh
		mov	ax, [word_2460E]
		shr	ax, 1
		adc	ax, 0
		dec	ax
		out	0C2h, al	; DMA controller, 8237A-5.
					; channel 1 base address
					; (also	sets current address)
		mov	al, ah
		out	0C2h, al	; DMA controller, 8237A-5.
					; channel 1 base address
					; (also	sets current address)
		xor	al, al
		out	0D4h, al
		retn
; ---------------------------------------------------------------------------

loc_18878:				; CODE XREF: dma_186E3+29j
		mov	al, 5
		out	0D4h, al
		xor	al, al
		out	0D8h, al
		mov	al, [dma_mode]
		or	al, 1
		out	0D6h, al
		movzx	edx, word [dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, word [dma_buf_pointer]
		add	eax, edx
		add	eax, [dword_24694]
		shr	eax, 1
		out	0C4h, al	; DMA controller, 8237A-5.
					; channel 2 base address
					; (also	sets current address)
		mov	al, ah
		out	0C4h, al	; DMA controller, 8237A-5.
					; channel 2 base address
					; (also	sets current address)
		shr	eax, 0Fh
		out	8Bh, al		; DMA page register 74LS612:
					; Channel 5 (address bits 17-23)
		mov	ax, [word_2460E]
		shr	ax, 1
		adc	ax, 0
		dec	ax
		out	0C6h, al	; DMA controller, 8237A-5.
					; channel 3 base address
					; (also	sets current address)
		mov	al, ah
		out	0C6h, al	; DMA controller, 8237A-5.
					; channel 3 base address
					; (also	sets current address)
		mov	al, 1
		out	0D4h, al
		retn
; ---------------------------------------------------------------------------

loc_188C2:				; CODE XREF: dma_186E3+30j
		mov	al, 6
		out	0D4h, al
		xor	al, al
		out	0D8h, al
		mov	al, [dma_mode]
		or	al, 2
		out	0D6h, al
		movzx	edx, word [dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, word [dma_buf_pointer]
		add	eax, edx
		add	eax, [dword_24694]
		shr	eax, 1
		out	0C8h, al	; DMA 8237A-5. cmd reg bits:
					; 0: enable mem-to-mem DMA
					; 1: enable Ch0	address	hold
					; 2: disable controller
					; 3: compressed	timing mode
					; 4: enable rotating priority
					; 5: extended write mode; 0=late write
					; 6: DRQ sensing - active high
					; 7: DACK sensing - active high
		mov	al, ah
		out	0C8h, al	; DMA 8237A-5. cmd reg bits:
					; 0: enable mem-to-mem DMA
					; 1: enable Ch0	address	hold
					; 2: disable controller
					; 3: compressed	timing mode
					; 4: enable rotating priority
					; 5: extended write mode; 0=late write
					; 6: DRQ sensing - active high
					; 7: DACK sensing - active high
		shr	eax, 0Fh
		out	89h, al		; DMA page register 74LS612:
					; Channel 6 (address bits 17-23)
		mov	ax, [word_2460E]
		shr	ax, 1
		adc	ax, 0
		dec	ax
		out	0CAh, al	; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		mov	al, ah
		out	0CAh, al	; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		mov	al, 2
		out	0D4h, al
		retn
; ---------------------------------------------------------------------------

loc_1890C:				; CODE XREF: dma_186E3+37j
		mov	al, 7
		out	0D4h, al
		mov	al, [dma_mode]
		or	al, 3
		out	0D6h, al
		xor	al, al
		out	0D8h, al
		movzx	edx, word [dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, word [dma_buf_pointer]
		add	eax, edx
		add	eax, [dword_24694]
		shr	eax, 1
		out	0CCh, al	; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	al, ah
		out	0CCh, al	; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		shr	eax, 0Fh
		out	8Ah, al		; DMA page register 74LS612:
					; Channel 7 (address bits 17-23)
		mov	ax, [word_2460E]
		shr	ax, 1
		adc	ax, 0
		dec	ax
		out	0CEh, al	; DMA controller, 8237A-5.
					; Clear	mask registers.
					; Any OUT enables all 4	channels.
		mov	al, ah
		out	0CEh, al	; DMA controller, 8237A-5.
					; Clear	mask registers.
					; Any OUT enables all 4	channels.
		mov	al, 3
		out	0D4h, al
		retn


; =============== S U B	R O U T	I N E =======================================


set_dmachn_mask:	; CODE XREF: proaud_sndoff+1Dp
					; wss_sndoff+32p ...
		mov	al, cl
		cmp	al, 4
		jnb	short loc_18961
		or	al, 4
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		retn
; ---------------------------------------------------------------------------

loc_18961:				; CODE XREF: set_dmachn_mask+4j
		and	al, 3
		or	al, 4
		out	0D4h, al
		retn


; =============== S U B	R O U T	I N E =======================================


alloc_dma_buf:	; CODE XREF: mod_readfile_11F4E+92p
					; volume_prep+47p ...
		mov	[dword_24684], eax
		mov	[byte_2469C], cl
		mov	BYTE [memflg_2469A],	0
		mov	BYTE [byte_2469B], 0
		mov	DWORD [dword_24694], 0
		call	getmemallocstrat
		push	ax
		call	setmemalloc2
		mov	ebx, [dword_24684]
		shl	ebx, 1		; bytes
		call	memalloc
		jb	loc_18A22
		mov	[myseg_24698], ax
		mov	dx, ax
		mov	ebx, [dword_24684]
		cmp	BYTE [byte_2469C], 4
		jb	short loc_189DB
		movzx	eax, ax
		shl	eax, 4
		and	eax, 1FFFFh
		add	eax, ebx
		cmp	eax, 20000h
		jbe	short loc_18A0A
		sub	eax, ebx
		neg	eax
		add	eax, 20000h
		add	ebx, eax
		and	dx, 0E000h
		add	dh, 20h	; ' '
		jmp	short loc_18A0A
; ---------------------------------------------------------------------------

loc_189DB:				; CODE XREF: alloc_dma_buf+40j
		movzx	eax, ax
		shl	eax, 4
		and	eax, 0FFFFh
		add	eax, ebx
		cmp	eax, 10000h
		jbe	short loc_18A0A
		sub	eax, ebx
		neg	eax
		add	eax, 10000h
		add	ebx, eax
		and	dx, 0F000h
		add	dh, 10h

loc_18A0A:				; CODE XREF: alloc_dma_buf+59j
					; alloc_dma_buf+71j ...
		mov	[word_2468C], dx
		mov	ax, [myseg_24698]
		call	memrealloc
		pop	ax
		call	setmemallocstrat
		mov	BYTE [memflg_2469A],	1
		mov	ax, [word_2468C]
		clc
		retn
; ---------------------------------------------------------------------------

loc_18A22:				; CODE XREF: alloc_dma_buf+2Dj
		pop	ax
		call	setmemallocstrat
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


memfree_18A28:	; CODE XREF: mod_readfile_11F4E:loc_12117p
					; mod_readfile_11F4E+1E4p ...
		cmp	BYTE [memflg_2469A],	1
		jnz	short loc_18A3B
		mov	BYTE [memflg_2469A],	0
		mov	ax, [myseg_24698]
		call	memfree
		retn
; ---------------------------------------------------------------------------

loc_18A3B:				; CODE XREF: memfree_18A28+5j
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


; int __usercall setsnd_handler<eax>(void (__cdecl *myfunc)()<esi>)
setsnd_handler:	; CODE XREF: gravis_init+C1p
					; proaud_set+14p ...
		pushf
		push	es
		cli
		movzx	cx, al
		in	al, 0A1h	; Interrupt Controller #2, 8259A
		mov	ah, al
		in	al, 21h		; Interrupt controller,	8259A.
		mov	[interrupt_mask], ax
		mov	bx, 0FFFEh
		rol	bx, cl
		cmp	cl, 8
		jb	short loc_18A5C
		and	bl, 0FBh
		add	cl, 60h	; '`'

loc_18A5C:				; CODE XREF: setsnd_handler+17j
		add	cl, 8
		shl	cx, 2
		and	ax, bx
		out	21h, al		; Interrupt controller,	8259A.
		mov	al, ah
		out	0A1h, al	; Interrupt Controller #2, 8259A
		mov	[intvectoffset], cx
		mov	bx, cx
		xor	ax, ax
		mov	es, ax
		les	cx, [es:bx]
		mov	[old_intprocoffset], cx
		mov	[old_intprocseg], es
		mov	es, ax
		mov	[es:bx], si
		mov	word [es:bx+2], cs
		pop	es
		popf
		retn


; =============== S U B	R O U T	I N E =======================================


restore_intvector:	; CODE XREF: gravis_clean+16p
					; useless_1474C+Fp ...
		pushf
		push	es
		cli
		mov	ax, [interrupt_mask]
		out	21h, al		; Interrupt controller,	8259A.
		mov	al, ah
		out	0A1h, al	; Interrupt Controller #2, 8259A
		mov	bx, [intvectoffset]
		xor	ax, ax
		mov	es, ax
		mov	ax, [old_intprocoffset]
		mov	[es:bx], ax
		mov	ax, [old_intprocseg]
		mov	[es:bx+2], ax
		pop	es
		popf
		retn


; =============== S U B	R O U T	I N E =======================================


getint_vect:	; CODE XREF: sub_12DA8+67p
		push	es
		mov	ah, 35h
		int	21h		; DOS -	2+ - GET INTERRUPT VECTOR
					; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	dx, es
		pop	es
		retn


; =============== S U B	R O U T	I N E =======================================


setint_vect:	; CODE XREF: set_timer_int+20p
					; clean_int8_mem_timr+Cp ...
		push	ds
		mov	ds, dx
		mov	dx, bx
		mov	ah, 25h
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds
		retn


; =============== S U B	R O U T	I N E =======================================


; int __usercall memalloc<eax>(int bytes<ebx>)
memalloc:		; CODE XREF: inr_module:loc_11AC0p
					; memalloc12k+6p ...
		add	ebx, 0Fh
		shr	ebx, 4
		cmp	ebx, 10000h
		jnb	short loc_18AD9
		mov	ah, 48h
		int	21h		; DOS -	2+ - ALLOCATE MEMORY
					; BX = number of 16-byte paragraphs desired
		retn
; ---------------------------------------------------------------------------

loc_18AD9:				; CODE XREF: memalloc+Fj
		mov	ax, 8
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


memfree:		; CODE XREF: memfree_125DA+4Fp
					; memfree_125DA+72p ...
		push	es
		mov	es, ax
		mov	ah, 49h
		int	21h		; DOS -	2+ - FREE MEMORY
					; ES = segment address of area to be freed
		pop	es
		retn


; =============== S U B	R O U T	I N E =======================================


memrealloc:		; CODE XREF: mem_reallocx+14p
					; alloc_dma_buf+A9p
		add	ebx, 0Fh
		shr	ebx, 4
		cmp	ebx, 10000h
		jnb	short loc_18AFF
		mov	es, ax
		mov	ah, 4Ah
		int	21h		; DOS -	2+ - ADJUST MEMORY BLOCK SIZE (SETBLOCK)
					; ES = segment address of block	to change
					; BX = new size	in paragraphs
		retn
; ---------------------------------------------------------------------------

loc_18AFF:				; CODE XREF: memrealloc+Fj
		mov	ax, 8
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


setmemallocstrat:	; CODE XREF: deinit_125B9+15p
					; sub_12D35+22p ...
		push	ax
		movzx	bx, al
		mov	ax, 5801h
		int	21h		; DOS -	3+ - GET/SET MEMORY ALLOCATION STRATEGY
					; AL = function	code: set allocation strategy
		pop	bx
		shr	bx, 8
		mov	ax, 5803h
		int	21h		; DOS -	3+ - GET/SET MEMORY ALLOCATION STRATEGY
					; AL = function	code: (DOS 5beta) set UMB link state
		retn


; =============== S U B	R O U T	I N E =======================================


getmemallocstrat:	; CODE XREF: sub_12DA8+7Fp
					; alloc_dma_buf+1Bp
		mov	ax, 5800h
		int	21h		; DOS -	3+ - GET/SET MEMORY ALLOCATION STRATEGY
					; AL = function	code: get allocation strategy
		push	ax
		mov	ax, 5802h
		int	21h		; DOS -	3+ - GET/SET MEMORY ALLOCATION STRATEGY
					; AL = function	code: (DOS 5beta) get UMB link state
		pop	bx
		mov	ah, al
		mov	al, bl
		retn


; =============== S U B	R O U T	I N E =======================================


setmemalloc1:	; CODE XREF: sub_12D35+12p
					; sub_12DA8+85p
		test	byte [config_word],	1
		jz	short setmemalloc2
		mov	ax, 181h
		jmp	short setmemallocstrat


; =============== S U B	R O U T	I N E =======================================


setmemalloc2:	; CODE XREF: alloc_dma_buf+1Fp
					; setmemalloc1+5j
		mov	ax, 1
		jmp	short setmemallocstrat


; =============== S U B	R O U T	I N E =======================================


WriteMixerSB:	; CODE XREF: sb_set-F3p
					; sb_set:loc_14C89p ...
		push	ax
		push	dx
		mov	dx, [sb_base_port]
		add	dl, 4
		xchg	al, ah
		out	dx, al
		jmp	short $+2
		jmp	short $+2
		inc	dx
		mov	al, ah
		out	dx, al
		pop	dx
		pop	ax
		retn


; =============== S U B	R O U T	I N E =======================================


ReadMixerSB:	; CODE XREF: sb16_init+25p
					; sb16_init+54p ...
		push	dx
		mov	dx, [sb_base_port]
		add	dl, 4
		mov	al, ah
		out	dx, al
		jmp	short $+2
		jmp	short $+2
		inc	dx
		in	al, dx
		pop	dx
		retn


; =============== S U B	R O U T	I N E =======================================


WriteSB:		; CODE XREF: sb_set+32p sb_set+38p ...
		push	dx
		push	cx
		push	ax
		mov	dx, [sb_base_port]
		add	dl, 0Ch
		mov	cx, 1000h

loc_18B70:				; CODE XREF: WriteSB+13j
		in	al, dx
		or	al, al
		jns	short loc_18B7C
		dec	cx
		jnz	short loc_18B70
		pop	ax
		pop	cx
		pop	dx
		retn
; ---------------------------------------------------------------------------

loc_18B7C:				; CODE XREF: WriteSB+10j
		pop	ax
		out	dx, al
		pop	cx
		pop	dx
		retn


; =============== S U B	R O U T	I N E =======================================


ReadSB:		; CODE XREF: sb16_detect_port+70p
					; sb16_detect_port+75p	...
		push	dx
		push	cx
		push	ax
		mov	dx, [sb_base_port]
		add	dl, 0Eh
		mov	cx, 1000h

loc_18B8E:				; CODE XREF: ReadSB+13j
		in	al, dx
		or	al, al
		js	short loc_18B9C
		dec	cx
		jnz	short loc_18B8E
		pop	ax
		pop	cx
		pop	dx
		xor	al, al
		retn
; ---------------------------------------------------------------------------

loc_18B9C:				; CODE XREF: ReadSB+10j
		pop	ax
		sub	dl, 4
		in	al, dx
		pop	cx
		pop	dx
		retn


; =============== S U B	R O U T	I N E =======================================


CheckSB:		; CODE XREF: sbpro_sndoff+9p
					; sb16_detect_port+Dp ...
		mov	dx, [sb_base_port]
		add	dl, 6
		mov	al, 1
		out	dx, al
		mov	ax, 400h

loc_18BB1:				; CODE XREF: CheckSB+Ej
		dec	ax
		jnz	short loc_18BB1
		out	dx, al
		call	ReadSB
		cmp	al, 0AAh ; '™'
		jnz	short loc_18BBE
		clc
		retn
; ---------------------------------------------------------------------------

loc_18BBE:				; CODE XREF: CheckSB+16j
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


sb16_sound_off:	; CODE XREF: sb16_deinit+3p
					; sbpro_clean+3p ...
		call	CheckSB
		mov	al, 0D3h ; '”'
		call	WriteSB
		retn


; =============== S U B	R O U T	I N E =======================================


initclockfromrtc:	; CODE XREF: deinit_125B9+1Bp
					; sub_12D35+25p
		mov	ah, 2
		int	1Ah		; CLOCK	- READ REAL TIME CLOCK (AT,XT286,CONV,PS)
					; Return: CH = hours in	BCD
					; CL = minutes in BCD
					; DH = seconds in BCD
		xor	eax, eax
		mov	al, dh
		mov	ah, al
		shr	ah, 4
		and	al, 0Fh
		aad
		mov	ebx, eax
		mov	al, ch
		mov	ah, al
		shr	ah, 4
		and	al, 0Fh
		aad
		imul	edx, eax, 60
		mov	al, cl
		mov	ah, al
		shr	ah, 4
		and	al, 0Fh
		aad
		add	dx, ax
		imul	eax, edx, 60
		add	eax, ebx
		mov	edx, 1193180
		mul	edx
		shrd	eax, edx, 10h
		xor	dx, dx
		mov	es, dx
		mov	[es:46Ch], eax
		retn


; =============== S U B	R O U T	I N E =======================================


u32tox:		; CODE XREF: myasmsprintf+EBp
		ror	eax, 10h
		call	u16tox
		ror	eax, 10h


; =============== S U B	R O U T	I N E =======================================


u16tox:		; CODE XREF: u32tox+4p
					; myasmsprintf+D7p
		xchg	al, ah
		call	u8tox
		mov	al, ah


; =============== S U B	R O U T	I N E =======================================


u8tox:		; CODE XREF: u16tox+2p
					; myasmsprintf+C4p
		push	ax
		shr	al, 4
		call	u4tox
		pop	ax


; =============== S U B	R O U T	I N E =======================================


u4tox:		; CODE XREF: u8tox+4p
		and	al, 0Fh
		or	al, '0'
		cmp	al, '9'
		jbe	short loc_18C3D
		add	al, 7

loc_18C3D:				; CODE XREF: u4tox+6j
		mov	[si], al
		inc	si
		retn


; =============== S U B	R O U T	I N E =======================================


my_i8toa10_0:	; CODE XREF: myasmsprintf+8Ap
		cbw


; =============== S U B	R O U T	I N E =======================================


my_i16toa10_0:	; CODE XREF: myasmsprintf+9Dp
		cwde


; =============== S U B	R O U T	I N E =======================================


my_i32toa10_0:	; CODE XREF: myasmsprintf+B1p
		xor	cx, cx
		or	eax, eax
		jns	short my_i32toa10_1
		mov	dl, '-'
		call	my_putdigit
		neg	eax
		jmp	short my_i32toa10_1


; =============== S U B	R O U T	I N E =======================================


my_u8toa_10:	; CODE XREF: myasmsprintf+53p
		xor	ah, ah


; =============== S U B	R O U T	I N E =======================================


my_u16toa_10:	; CODE XREF: myasmsprintf+65p
		movzx	eax, ax


; =============== S U B	R O U T	I N E =======================================


my_u32toa10_0:	; CODE XREF: myasmsprintf+78p
		xor	cx, cx

my_i32toa10_1:				; CODE XREF: my_i32toa10_0+5j
					; my_i32toa10_0+Fj
		mov	ebx, 10


; =============== S U B	R O U T	I N E =======================================


my_u32toa_0:	; CODE XREF: my_u32toa_0+Dp
		xor	edx, edx
		div	ebx
		or	eax, eax
		jz	short loc_18C75
		push	edx
		call	my_u32toa_0
		pop	edx

loc_18C75:				; CODE XREF: my_u32toa_0+9j
		or	dl, '0'


; =============== S U B	R O U T	I N E =======================================


my_putdigit:	; CODE XREF: my_i32toa10_0+9p
		mov	[si], dl
		inc	si
		inc	cx
		retn

; ---------------------------------------------------------------------------
asmprintf_tbl	dw mysprintf_0_nop ; DATA XREF: myasmsprintf+1Cr
		dw mysprintf_1_offstr
		dw mysprintf_2_off8str
		dw mysprintf_3_off16str
		dw mysprintf_4_u8toa
		dw mysprintf_5_u16toa
		dw mysprintf_6_u32toa
		dw mysprintf_7_i8toa
		dw mysprintf_8_i16toa
		dw mysprintf_9_i32toa
		dw mysprintf_10_u8tox
		dw mysprintf_11_u16tox
		dw mysprintf_12_u32tox

; =============== S U B	R O U T	I N E =======================================


myasmsprintf:	; CODE XREF: sub_12D05+20p
		push	es
		mov	ax, ds
		mov	es, ax
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

loc_18C9F:				; CODE XREF: myasmsprintf+Fj
		mov	[di], al
		inc	di

loc_18CA2:				; CODE XREF: myasmsprintf+5j
					; myasmsprintf+2Dj ...
		mov	al, [si]
		inc	si
		cmp	al, 20h	; ' '
		jnb	short loc_18C9F
		cmp	al, 0Ch
		ja	short mysprintf_0_nop
		inc	si
		mov	bl, al
		xor	bh, bh
		shl	bx, 1
		jmp	WORD [cs:asmprintf_tbl+bx]

mysprintf_0_nop:			; CODE XREF: myasmsprintf+13j
					; DATA XREF: seg000:asmprintf_tblo
		pop	es
		retn
; ---------------------------------------------------------------------------

mysprintf_1_offstr:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C80o
		push	si
		mov	si, [si]
		call	strcpy_count_0
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_2_off8str:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C82o
		mov	bx, [si]
		mov	bl, [bx]
		xor	bh, bh
		jmp	short loc_18CD3
; ---------------------------------------------------------------------------

mysprintf_3_off16str:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C84o
		mov	bx, [si]
		mov	bx, [bx]

loc_18CD3:				; CODE XREF: myasmsprintf+35j
		push	si
		shl	bx, 1
		mov	si, [si+2]
		mov	si, [bx+si]
		call	strcpy_count_0
		pop	si
		add	si, 4
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_4_u8toa:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C86o
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	my_u8toa_10
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_5_u16toa:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C88o
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	my_u16toa_10
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_6_u32toa:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C8Ao
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	my_u32toa10_0
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_7_i8toa:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C8Co
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	my_i8toa10_0
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_8_i16toa:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C8Eo
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	my_i16toa10_0
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_9_i32toa:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C90o
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	my_i32toa10_0
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_10_u8tox:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C92o
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	u8tox
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_11_u16tox:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C94o
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	u16tox
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

mysprintf_12_u32tox:			; CODE XREF: myasmsprintf+1Cj
					; DATA XREF: seg000:8C96o
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	u32tox
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2


; =============== S U B	R O U T	I N E =======================================


mystrlen_0:
		mov	ax, -1
		dec	si

loc_18D93:				; CODE XREF: mystrlen_0+9j
		inc	ax
		inc	si
		cmp	byte [si], 0
		jnz	short loc_18D93
		sub	si, ax
		retn


; =============== S U B	R O U T	I N E =======================================


strcpy_count_0:	; CODE XREF: sub_12D05:loc_12D30p
					; myasmsprintf+26p ...
		xor	cx, cx
		jmp	short loc_18DA6
; ---------------------------------------------------------------------------

loc_18DA1:				; CODE XREF: strcpy_count_0+Ej
		mov	[es:di], al
		inc	si
		inc	di

loc_18DA6:				; CODE XREF: strcpy_count_0+2j
		mov	al, [si]
		inc	cx
		or	al, al
		jnz	short loc_18DA1
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_18DB0:				; CODE XREF: sub_16CF6+155j
					; sub_16CF6+173j ...
		mov	eax, ebp
		jmp	bx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_18DB8:				; CODE XREF: sub_16CF6+15Cj
					; sub_16CF6+17Aj ...
		mov	eax, edx
		jmp	bx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
; ---------------------------------------------------------------------------
offs_noninterp2	dw loc_161C0	; DATA XREF: sub_1609F+28r
		dw loc_161B0
		dw loc_161A0
		dw loc_16190
		dw loc_16180
		dw loc_16170
		dw loc_16160
		dw loc_16150
		dw loc_16140
		dw loc_16130
		dw loc_16120
		dw loc_16110
		dw loc_16100
		dw loc_160F0
		dw loc_160E0
		dw loc_160D0
offs_interpol2	dw loc_16617	; DATA XREF: sub_1609F+2AEr
		dw loc_165E8
		dw loc_165B9
		dw loc_1658A
		dw loc_1655B
		dw loc_1652C
		dw loc_164FD
		dw loc_164CE
		dw loc_1649F
		dw loc_16470
		dw loc_16441
		dw loc_16412
		dw loc_163E3
		dw loc_163B4
		dw loc_16385
		dw loc_16356
off_18E00	dw loc_16A89	; DATA XREF: sub_1609F:loc_16963r
		dw loc_16A76
		dw loc_16A63
		dw loc_16A50
		dw loc_16A3D
		dw loc_16A2A
		dw loc_16A17
		dw loc_16A04
		dw loc_169F1
		dw loc_169DE
		dw loc_169CB
		dw loc_169B8
		dw loc_169A5
		dw loc_16992
		dw loc_1697F
		dw loc_1696C
offs_noninterp	dw loc_15698	; DATA XREF: sub_15577+28r
		dw loc_15688
		dw loc_15678
		dw loc_15668
		dw loc_15658
		dw loc_15648
		dw loc_15638
		dw loc_15628
		dw loc_15618
		dw loc_15608
		dw loc_155F8
		dw loc_155E8
		dw loc_155D8
		dw loc_155C8
		dw loc_155B8
		dw loc_155A8
offs_interpol	dw loc_15B52	; DATA XREF: sub_15577+311r
		dw loc_15B23
		dw loc_15AF4
		dw loc_15AC5
		dw loc_15A96
		dw loc_15A67
		dw loc_15A38
		dw loc_15A09
		dw loc_159DA
		dw loc_159AB
		dw loc_1597C
		dw loc_1594D
		dw loc_1591E
		dw loc_158EF
		dw loc_158C0
		dw loc_15891
off_18E60	dw loc_15F78	; DATA XREF: sub_15577+8DBr
		dw loc_15F65
		dw loc_15F52
		dw loc_15F3F
		dw loc_15F2C
		dw loc_15F19
		dw loc_15F06
		dw loc_15EF3
		dw loc_15EE0
		dw loc_15ECD
		dw loc_15EBA
		dw loc_15EA7
		dw loc_15E94
		dw loc_15E81
		dw loc_15E6E
		dw loc_15E5B
off_18E80	dw loc_16C20	; DATA XREF: sub_1609F+B22r
		dw loc_16C1A
		dw loc_16C14
		dw loc_16C0E
		dw loc_16C08
		dw loc_16C02
		dw loc_16BFC
		dw loc_16BF6
		dw loc_16BF0
		dw loc_16BEA
		dw loc_16BE4
		dw loc_16BDE
		dw loc_16BD8
		dw loc_16BD2
		dw loc_16BCC
		dw loc_16BC6
off_18EA0	dw loc_16DB0	; DATA XREF: sub_16CF6+10r
		dw loc_16DA5
		dw loc_16D9A
		dw loc_16D8F
		dw loc_16D84
		dw loc_16D79
		dw loc_16D6E
		dw loc_16D63
		dw loc_16D58
		dw loc_16D4D
		dw loc_16D42
		dw loc_16D37
		dw loc_16D2C
		dw loc_16D21
		dw loc_16D16
		dw loc_16D0B
off_18EC0	dw loc_17001	; DATA XREF: sub_16CF6+144r
		dw loc_16FE3
		dw loc_16FC5
		dw loc_16FA7
		dw loc_16F89
		dw loc_16F6B
		dw loc_16F4D
		dw loc_16F2F
		dw loc_16F11
		dw loc_16EF3
		dw loc_16ED5
		dw loc_16EB7
		dw loc_16E99
		dw loc_16E7B
		dw loc_16E5D
		dw loc_16E3F
off_18EE0	dw loc_1736F	; DATA XREF: sub_1725F+1Br
		dw loc_1735F
		dw loc_1734F
		dw loc_1733F
		dw loc_1732F
		dw loc_1731F
		dw loc_1730F
		dw loc_172FF
		dw loc_172EF
		dw loc_172DF
		dw loc_172CF
		dw loc_172BF
		dw loc_172AF
		dw loc_1729F
		dw loc_1728F
		dw loc_1727F
off_18F00	dw loc_1761E	; DATA XREF: sub_1725F+1F8r
		dw loc_17600
		dw loc_175E2
		dw loc_175C4
		dw loc_175A6
		dw loc_17588
		dw loc_1756A
		dw loc_1754C
		dw loc_1752E
		dw loc_17510
		dw loc_174F2
		dw loc_174D4
		dw loc_174B6
		dw loc_17498
		dw loc_1747A
		dw loc_1745C
off_18F20	dw loc_17956	; DATA XREF: sub_17824+10r
		dw loc_17943
		dw loc_17930
		dw loc_1791D
		dw loc_1790A
		dw loc_178F7
		dw loc_178E4
		dw loc_178D1
		dw loc_178BE
		dw loc_178AB
		dw loc_17898
		dw loc_17885
		dw loc_17872
		dw loc_1785F
		dw loc_1784C
		dw loc_17839
off_18F40	dw loc_17C25	; DATA XREF: sub_17824+249r
		dw loc_17C08
		dw loc_17BEB
		dw loc_17BCE
		dw loc_17BB1
		dw loc_17B94
		dw loc_17B77
		dw loc_17B5A
		dw loc_17B3D
		dw loc_17B20
		dw loc_17B03
		dw loc_17AE6
		dw loc_17AC9
		dw loc_17AAC
		dw loc_17A8F
		dw loc_17A72
effoff_18F60	dw eff_nullsub	; DATA XREF: sub_137D5+16r
					; sub_137D5+2Br
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_13A43
		dw eff_13A94
		dw eff_nullsub
		dw eff_13B06
		dw eff_13B78
		dw eff_13B88
		dw eff_13BA3
		dw eff_13CDD
		dw eff_13CE8
		dw eff_13DE5
		dw eff_13DEF
		dw eff_nullsub
		dw eff_13E2D
		dw eff_13E32
		dw eff_13E7F
		dw eff_13E84
		dw eff_13E8C
		dw eff_nullsub
		dw nullsub_2
		dw eff_13F05
		dw eff_13F3B
		dw eff_nullsub
		dw eff_14020
		dw eff_14030
		dw eff_14067
effoff_18FA2	dw eff_nullsub	; DATA XREF: sub_13623+196r
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_13A43
		dw eff_nullsub
		dw eff_nullsub
		dw eff_13B06
		dw eff_nullsub
		dw eff_13B88
		dw eff_13BA3
		dw eff_13CDD
		dw eff_13CE8
		dw eff_13DE5
		dw eff_13DEF
		dw eff_nullsub
		dw eff_13E2D
		dw eff_13E32
		dw eff_13E7F
		dw eff_13E84
		dw eff_13E8C
		dw eff_nullsub
		dw nullsub_2
		dw eff_13F05
		dw eff_13F3B
		dw eff_nullsub
		dw eff_14020
		dw eff_14030
		dw eff_14067
effoff_18FE4	dw eff_nullsub	; DATA XREF: sub_13813+Er
		dw eff_13886
		dw eff_138A4
		dw eff_138D2
		dw eff_1392F
		dw eff_139AC
		dw eff_139B2
		dw eff_139B9
		dw eff_nullsub
		dw eff_nullsub
		dw eff_13AD7
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
		dw eff_13BA3
		dw eff_nullsub
		dw eff_nullsub
		dw eff_13DE5
		dw eff_13DEF
		dw eff_13E1E
		dw eff_13E2D
		dw eff_13E32
		dw eff_13E7F
		dw eff_13E84
		dw eff_nullsub
		dw eff_138D2
		dw nullsub_2
		dw eff_13F05
		dw eff_13F3B
		dw eff_13FBE
		dw eff_nullsub
		dw eff_nullsub
		dw eff_nullsub
effoff_19026	dw eff_nullsub	; DATA XREF: eff_13BA3+Ar
		dw eff_1387F
		dw eff_1389D
		dw eff_13BB2
		dw eff_13BC0
		dw eff_13BC8
		dw eff_13C02
		dw eff_13C34
		dw eff_13C3F
		dw eff_13C64
		dw eff_13C88
		dw eff_13C95
		dw eff_13CA2
		dw eff_13CB3
		dw eff_13CC9
		dw eff_nullsub
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0

; ---------------------------------------------------------------------------
; ===========================================================================

; Segment type:	Pure code
SEGMENT	seg001	ALIGN=1	public	CLASS=CODE	use16
; START	OF FUNCTION CHUNK FOR start

loc_19050:				; CODE XREF: start+4Cj
					; DATA XREF: dseg:off_1DE3Co ...
		call	callsubx

loc_19053:
		jb	loc_192B9

loc_19057:				; "\rCurrent Soundcard settings:\r\n\n$"
		mov	dx, aCurrentSoundcard
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	ax, ds
		mov	es, ax
		mov	di, buffer_1 ; 2800h
		call far sub_12D05
		mov	byte [es:di], '$'

loc_1906E:				; 2800h
		mov	dx, buffer_1
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	dx, myendl ; "\r\n$"
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"

loc_1907C:
		call far deinit_125B9
		mov	ax, 4C00h

loc_19084:				; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)
		int	21h		; AL = exit code
; ---------------------------------------------------------------------------

loc_19086:				; CODE XREF: start+57j
		mov	dx, 0
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"

loc_1908D:
		mov	ax, 4C00h

loc_19090:				; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)
		int	21h		; AL = exit code
; END OF FUNCTION CHUNK	FOR start

; =============== S U B	R O U T	I N E =======================================


..start:
start:

; FUNCTION CHUNK AT 0000 SIZE 00000042 BYTES
; FUNCTION CHUNK AT 07D7 SIZE 00000059 BYTES
; FUNCTION CHUNK AT 0D44 SIZE 0000007D BYTES

		mov	ax, dseg

loc_19095:
		mov	ds, ax
		mov	[esseg_atstart], es
		mov	ax, sp
		add	ax, 13h
		mov	cl, 4

loc_190A2:
		shr	ax, cl
		mov	bx, ss
		add	bx, ax
		mov	ax, es
		sub	bx, ax
		mov	ah, 4Ah
		int	21h		; DOS -	2+ - ADJUST MEMORY BLOCK SIZE (SETBLOCK)
					; ES = segment address of block	to change
					; BX = new size	in paragraphs
		cld

loc_190B1:
		xor	dl, dl
		mov	cx, 4D50h	; PM
		mov	bx, 5344h	; DS
		mov	ax, 60FFh

loc_190BC:
		int	2Fh
		cmp	ax, 4F4Bh	; 'KO' check for single instance
		jnz	short loc_190D3
		mov	dx, aCriticalErrorT ; "\r\n\nCritical error: The	player jumped to"...
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		xor	ah, ah
		int	16h		; KEYBOARD - READ CHAR FROM BUFFER, WAIT IF EMPTY
					; Return: AH = scan code, AL = character

loc_190CE:
		mov	ax, 4C02h
		int	21h		; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)
					; AL = exit code
; ---------------------------------------------------------------------------

loc_190D3:				; CODE XREF: start+2Fj
		call	loadcfg
		call	parse_cmdline
		bt	ebp, 8
		jb	loc_19050

loc_190E2:
		test	ebp, 80000080h
		jnz	short loc_19086
		bt	ebp, 0Bh
		jnb	short loc_190F7
		or	byte [configword], 4

loc_190F7:				; CODE XREF: start+5Ej
		bt	ebp, 3
		jnb	short loc_19103
		and	byte [configword], 0FBh

loc_19103:				; CODE XREF: start+6Aj
		bt	ebp, 6
		jnb	short loc_19114
		and	byte [configword+1], 0F1h
		or	byte [configword+1], 2

loc_19114:				; CODE XREF: start+76j
		bt	ebp, 5
		jnb	short loc_19125
		and	byte [configword+1], 0F1h
		or	byte [configword+1], 4

loc_19125:				; CODE XREF: start+87j
		bt	ebp, 13h
		jnb	short loc_19131
		and	byte [configword+1], 0F1h

loc_19131:				; CODE XREF: start+98j
		bt	ebp, 4
		jnb	short loc_1913D
		and	byte [configword], 0FDh

loc_1913D:				; CODE XREF: start+A4j
		bt	ebp, 14h
		jnb	short loc_19149
		and	byte [configword], 0FEh

loc_19149:				; CODE XREF: start+B0j
		bt	ebp, 0Eh
		jnb	short loc_19155
		and	byte [configword], 0BFh

loc_19155:				; CODE XREF: start+BCj
		bt	ebp, 2
		jnb	short loc_19161
		or	byte [configword], 40h

loc_19161:				; CODE XREF: start+C8j
		bt	ebp, 15h
		setb	al
		mov	[byte_1DE86], al
		mov	al, [byte_1DCF8]
		mov	ah, al
		and	al, 0Fh
		mov	[byte_1DE82], al
		shr	ah, 4
		mov	[byte_1DE83], ah

loc_1917D:
		mov	DWORD [videomempointer], 0B8000000h
		mov	ax, 3508h
		int	21h		; DOS -	2+ - GET INTERRUPT VECTOR
					; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	[oint8off_1DE14], bx
		mov	[oint8seg_1DE16], es
		mov	ax, 3509h
		int	21h		; DOS -	2+ - GET INTERRUPT VECTOR
					; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	word [cs:oint9_1C1A4], bx
		mov	word [cs:oint9_1C1A4+2], es

loc_191A2:
		mov	ax, 3524h

loc_191A5:				; DOS -	2+ - GET INTERRUPT VECTOR
		int	21h		; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	word [cs:oint24_1C1AC], bx
		mov	word [cs:oint24_1C1AC+2], es
		mov	ax, 352Fh
		int	21h		; DOS -	2+ - GET INTERRUPT VECTOR
					; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	word [cs:oint2f_1C1B4], bx
		mov	word [cs:oint2f_1C1B4+2], es
		push	ds
		mov	ax, cs
		mov	ds, ax
		mov	dx, int9_keyb
		mov	ax, 2509h
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		mov	dx, int24
		mov	ax, 2524h
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		mov	dx, int2f_checkmyself
		mov	ax, 252Fh

loc_191DB:				; DOS -	SET INTERRUPT VECTOR
		int	21h		; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds
		mov	ah, 34h
		int	21h		; DOS -	2+ internal - RETURN CritSectFlag (InDOS) POINTER
		mov	[critsectpoint_off], bx
		mov	[critsectpoint_seg], es

loc_191EA:
		push	ds
		mov	ax, 5D06h
		int	21h		; DOS -	3.1+ internal -	GET ADDRESS OF DOS SWAPPABLE DATA AREA
					; Return: CF set on error, CF clear if successful
		mov	ax, ds
		pop	ds
		mov	[swapdata_off],	si
		mov	[swapdata_seg],	ax
		mov	BYTE [byte_1DE70], 0FFh
		call	mouse_init
		mov	bl, byte [configword+1]
		shr	bl, 1
		and	bx, 7
		cmp	bl, 5
		jbe	short loc_19212
		xor	bl, bl

loc_19212:				; CODE XREF: start+17Cj
		shl	bx, 1
		mov	ax, [off_1CA8E+bx]
		mov	[off_1DE3C], ax
		cmp	BYTE [buffer_1DB6C],	40h ; '@'
		jz	loc_19D94
		cmp	BYTE [buffer_1DB6C],	20h ; ' '
		jbe	loc_192CA
		mov	WORD [word_1DE4E], 2
		call	find_mods
		jb	short loc_19256
		call	callsubx
		jb	short loc_19256
		call	readallmoules
		jb	short loc_19250

loc_19242:
		cmp	byte [word_1DE50], 1Ch
		jz	loc_192E0
		mov	BYTE [byte_1DE7E], 0

loc_19250:				; CODE XREF: start+1AEj start+5C2j ...
		cli
		call far deinit_125B9

loc_19256:				; CODE XREF: start+1A4j start+1A9j ...
		call	mouse_deinit
		push	ds
		lds	dx, [cs:oint2f_1C1B4]
		mov	ax, 252Fh
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds
		push	ds
		lds	dx, [cs:oint24_1C1AC]
		mov	ax, 2524h
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds
		push	ds
		lds	dx, [cs:oint9_1C1A4]
		mov	ax, 2509h
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds
		mov	ax, 3
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		call	txt_enableblink
		mov	cx, 0
		mov	dx, 124Fh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		call	txt_draw_top_title
		mov	si, hopeyoulike
		les	di, [videomempointer]
		call	write_scr
		mov	dx, 1300h
		xor	bh, bh
		mov	ah, 2
		int	10h		; - VIDEO - SET	CURSOR POSITION
					; DH,DL	= row, column (0,0 = upper left)
					; BH = page number
		cmp	BYTE [byte_1DE7E], 0
		jz	short loc_192C3
		mov	dx, 1400h
		xor	bh, bh
		mov	ah, 2
		int	10h		; - VIDEO - SET	CURSOR POSITION
					; DH,DL	= row, column (0,0 = upper left)
					; BH = page number

loc_192B9:				; CODE XREF: start:loc_19053j
		push	ds
		lds	dx, [messagepointer]
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		pop	ds

loc_192C3:				; CODE XREF: start+21Cj
		mov	ah, 4Ch	; 'L'
		mov	al, [byte_1DE7E]
		int	21h		; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)
					; AL = exit code

loc_192CA:				; CODE XREF: start+197j
		mov	BYTE [byte_1DE7E], 5
		mov	word [messagepointer], aNotEnoughMemor ; "Not enough	memory.\r\n$"
		mov	word [messagepointer+2], ds
		call	callsubx
		jb	loc_19256

loc_192E0:				; CODE XREF: start+1B5j
		mov	si, mystr ; str
		call	dosgetcurdir
		mov	WORD [word_1DE62], 0
		mov	WORD [word_1DE5E], 0
		mov	BYTE [byte_1DE7F], 1

loc_192F7:				; CODE XREF: start+456j start+6F3j ...
		call	setvideomode
		mov	BYTE [byte_1DE70], 1

loc_192FF:				; CODE XREF: start+471j start+4A7j ...
		mov	cx, 0
		mov	dx, 1B4Fh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		call	txt_draw_top_title
		mov	ax, ds
		mov	es, ax
		mov	di, buffer_1 ; 2800h
		call far sub_12D05
		mov	byte [es:di], 0
		sub	di, 16EFh
		and	di, 0FFFEh
		mov	ax, 50h	; 'P'
		sub	ax, di
		add	ax, 320h
		les	di, [videomempointer]
		add	di, ax		; videoptr
		mov	si, buffer_1 ; str
		mov	ah, 78h	; 'x'   ; color
		call	put_message
		mov	cx, 604h
		mov	dx, 84Bh
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame
		mov	ah, 19h
		int	21h		; DOS -	GET DEFAULT DISK NUMBER
		mov	edx, 5C3A41h	; "A:\"
		add	dl, al
		mov	[buffer_1DC6C],	edx
		mov	si, (buffer_1DC6C+3)
		xor	dl, dl
		mov	ah, 47h
		int	21h		; DOS -	2+ - GET CURRENT DIRECTORY
					; DL = drive (0=default, 1=A, etc.)
					; DS:SI	points to 64-byte buffer area
		mov	si, buffer_1DC6C
		call	mystrlen
		shr	ax, 1
		neg	ax
		add	ax, 257h
		shl	ax, 1
		les	di, [videomempointer]
		add	di, ax		; videoptr
		mov	si, buffer_1DC6C	; str
		mov	ah, 7Bh	; '{'   ; color
		call	put_message
		cmp	BYTE [byte_1DE7F], 1
		jnz	short loc_19395
		mov	si, msg	; "Searching directory for modules  "
		mov	ax, 7E0Dh
		call	message_1BE77
		call	modules_search

loc_19395:				; CODE XREF: start+2F5j
		mov	BYTE [byte_1DE7E], 0
		mov	WORD [word_1DE60], 0FFFFh
		mov	cx, 906h
		mov	dx, 1949h
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame

loc_193AE:				; CODE XREF: start+4C8j start+4EAj ...
		call	filelist_198B8
		mov	ax, [word_1DE62]
		mov	bl, 10h
		call	recolortxt

loc_193BC:				; CODE XREF: start+3CBj start+481j ...
		mov	al, [byte_1DE7C]
		xor	al, 1
		mov	[byte_1DE7D], al
		call	mouse_show

loc_193C7:				; CODE XREF: start+373j
		test	BYTE [byte_1DE90], 2
		jnz	loc_19848
		test	BYTE [byte_1DE90], 1
		jnz	loc_19827
		mov	al, [byte_1DE7C]
		cmp	al, [byte_1DE7D]
		jz	short loc_193FF	; keyboard message loop	here
		mov	[byte_1DE7D], al
		les	di, [videomempointer]
		add	di, 104Ah	; videoptr
		mov	ah, 78h	; 'x'   ; color
		mov	si, aHitBackspaceToRe ; "Hit backspace to return	to playmode, F-"...
		cmp	BYTE [byte_1DE7C], 0
		jz	short loc_193FC
		mov	si, aPressF1ForHelpQu ; "		 Press F-1 for help, Qu"...

loc_193FC:				; CODE XREF: start+365j
		call	put_message

loc_193FF:				; CODE XREF: start+34Ej
		mov	ax, [cs:key_code] ; keyboard message loop here
		or	ax, ax
		jnz	short loc_193C77
		hlt
		mov	ax, [cs:key_code] ; keyboard message loop here
		or	ax, ax
		jz	short loc_193C7
loc_193C77:
		push	ax
		call	mouse_hide
		pop	ax
		mov	WORD [cs:key_code], 0
		cmp	al, 1
		jz	loc_1964E
		cmp	al, 48h	; 'H'
		jz	loc_1957F
		cmp	al, 50h	; 'P'
		jz	loc_1953C
		cmp	al, 47h	; 'G'
		jz	loc_195A7
		cmp	al, 4Fh	; 'O'
		jz	loc_195BE
		cmp	al, 49h	; 'I'
		jz	loc_195EA
		cmp	al, 51h	; 'Q'

loc_19439:
		jz	loc_19610
		cmp	al, 0Eh
		jz	loc_19762
		cmp	al, 53h	; 'S'

loc_19445:
		jz	loc_19657
		cmp	al, 3Bh	; ';'
		jz	loc_19788
		cmp	al, 42h	; 'B'
		jz	loc_197D6
		cmp	al, 43h	; 'C'
		jz	loc_197E7
		cmp	al, 1Ch
		jnz	loc_193BC
		mov	ax, [word_1DE62]

loc_19464:				; CODE XREF: seg001:0839j
		add	ax, [word_1DE5E]
		mov	dx, ax
		shl	ax, 1
		add	ax, dx
		add	ax, [word_1DE52]
		mov	fs, ax
		mov	si, 0Ch
		mov	ax, ds
		mov	es, ax
		mov	di, buffer_1DB6C
		mov	dx, di
		cld
		fs movsd
		fs movsd
		fs movsd
		mov	byte [di], 0
		cmp	byte [fs:2], 0
		jz	short loc_194EB
		cmp	byte [fs:2], 1
		jz	short loc_19506
		push	dx

loc_1949E:
		mov	cx, 501h
		mov	dx, 1A4Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7800h
		call	draw_frame
		mov	si, aLoadingModule ; msg
		mov	ax, 7E0Dh
		call	message_1BE77
		pop	dx
		call	read_module

loc_194B9:
		jnb	short loc_194E3
		mov	si, aNotEnoughMemo_0 ; "Not enough memory available to load all"...
		cmp	ax, 0FFFEh
		jz	short loc_194CE
		mov	si, aNotEnoughDram_0 ; "Not enough DRAM on your UltraSound to l"...
		cmp	ax, 0FFFDh
		jz	short loc_194CE
		mov	si, aModuleIsCorrupt ; msg

loc_194CE:				; CODE XREF: start+42Fj start+437j
		mov	ax, 7E0Dh
		call	message_1BE77
		xor	ax, ax
		mov	[cs:key_code], ax

loc_194DA:				; CODE XREF: start+44Fj
		xchg	ax, [cs:key_code]
		or	ax, ax
		jz	short loc_194DA

loc_194E3:				; CODE XREF: start:loc_194B9j
		mov	BYTE [byte_1DE7F], 0
		jmp	loc_192F7
; ---------------------------------------------------------------------------

loc_194EB:				; CODE XREF: start+401j
		mov	BYTE [byte_1DE7F], 1
		mov	dx, buffer_1DB6C
		mov	ah, 3Bh
		int	21h		; DOS -	2+ - CHANGE THE	CURRENT	DIRECTORY (CHDIR)
					; DS:DX	-> ASCIZ directory name	(may include drive)
		mov	WORD [word_1DE62], 0
		mov	WORD [word_1DE5E], 0
		jmp	loc_192FF
; ---------------------------------------------------------------------------

loc_19506:				; CODE XREF: start+409j
		mov	BYTE [byte_1DE7F], 1
		mov	dl, [fs:0Dh]
		sub	dl, 'A'
		jb	loc_193BC
		cmp	dl, 'Z' - 'A' +1
		jnb	loc_193BC
		mov	bl, dl
		inc	bl
		push	dx
		mov	ax, 440Fh
		int	21h		; DOS -	2+ - IOCTL -
		pop	dx
		mov	ah, 0Eh
		int	21h		; DOS -	SELECT DISK
					; DL = new default drive number	(0 = A,	1 = B, etc.)
					; Return: AL = number of logical drives
		mov	WORD [word_1DE62], 0
		mov	WORD [word_1DE5E], 0
		jmp	loc_192FF
; ---------------------------------------------------------------------------

loc_1953C:				; CODE XREF: start+38Fj start+603j ...
		cmp	WORD [word_1DE62], 0Eh
		jnb	short loc_1955D
		mov	bx, [word_1DE54]
		dec	bx
		mov	ax, [word_1DE62]
		cmp	ax, bx
		jnb	loc_193BC
		mov	bl, 70h	; 'p'
		call	recolortxt
		inc	WORD [word_1DE62]
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_1955D:				; CODE XREF: start+4AFj
		cmp	WORD [word_1DE54], 0Fh
		jb	loc_193BC
		mov	ax, [word_1DE54]
		sub	ax, [word_1DE5E]
		jb	loc_193BC
		cmp	ax, 10h
		jb	loc_193BC
		inc	WORD [word_1DE5E]
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_1957F:				; CODE XREF: start+389j
					; DATA XREF: dseg:str_24461o ...
		cmp	WORD [word_1DE62], 0
		jz	short loc_19595
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	recolortxt
		dec	WORD [word_1DE62]
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_19595:				; CODE XREF: start+4F2j
		sub	WORD [word_1DE5E], 1
		jnb	loc_193AE
		mov	WORD [word_1DE5E], 0
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_195A7:				; CODE XREF: start+395j
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	recolortxt
		mov	WORD [word_1DE62], 0
		mov	WORD [word_1DE5E], 0
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_195BE:				; CODE XREF: start+39Bj
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	recolortxt
		mov	ax, [word_1DE54]
		dec	ax
		cmp	ax, 0Fh
		jb	short loc_195DE
		sub	ax, 0Eh
		mov	[word_1DE5E], ax
		mov	WORD [word_1DE62], 0Eh
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_195DE:				; CODE XREF: start+53Bj
		mov	WORD [word_1DE5E], 0
		mov	[word_1DE62], ax
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_195EA:				; CODE XREF: start+3A1j
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	recolortxt
		xor	ax, ax
		xchg	ax, [word_1DE62]
		or	ax, ax
		jnz	loc_193AE
		sub	WORD [word_1DE5E], 0Fh
		jnb	loc_193AE
		mov	WORD [word_1DE5E], 0
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_19610:				; CODE XREF: start:loc_19439j
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	recolortxt
		mov	ax, [word_1DE54]
		dec	ax
		cmp	ax, 0Fh
		jb	short loc_19648
		mov	ax, 0Eh
		xchg	ax, [word_1DE62]
		cmp	ax, 0Eh
		jnz	loc_193AE
		add	WORD [word_1DE5E], 0Fh
		mov	ax, [word_1DE54]
		sub	ax, 0Fh
		cmp	[word_1DE5E], ax
		jbe	loc_193AE
		mov	[word_1DE5E], ax
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_19648:				; CODE XREF: start+58Dj
		mov	[word_1DE62], ax
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_1964E:				; CODE XREF: start+383j
					; DATA XREF: dseg:7CAFo
		mov	si, mystr ; str
		call	doschdir
		jmp	loc_19250
; ---------------------------------------------------------------------------

loc_19657:				; CODE XREF: start:loc_19445j
		mov	ax, [word_1DE5E]
		add	ax, [word_1DE62]
		mov	dx, ax
		shl	ax, 1
		add	ax, dx
		add	ax, [word_1DE52]
		mov	fs, ax
		test	WORD [cs:keyb_switches], 4
		jnz	short loc_196B0
		cmp	byte [fs:2], 2
		jnz	loc_193BC
		mov	WORD [word_1DE60], 0FFFFh
		test	byte [fs:3], 40h
		jnz	short loc_19698
		or	byte [fs:3], 40h
		inc	WORD [word_1DE5C]
		jmp	loc_1953C
; ---------------------------------------------------------------------------

loc_19698:				; CODE XREF: start+5F7j
		and	byte [fs:3], 0BFh
		sub	WORD [word_1DE5C], 1
		jnb	loc_1953C
		mov	WORD [word_1DE5C], 0
		jmp	loc_1953C
; ---------------------------------------------------------------------------

loc_196B0:				; CODE XREF: start+5DFj
		cmp	WORD [word_1DE5C], 0
		jz	loc_193BC
		mov	cx, 602h
		mov	dx, 1A4Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7800h
		call	draw_frame
		mov	si, aDeleteMarkedFil ; "Delete marked files? [Y/N]"
		mov	ax, 7E0Dh
		call	message_1BE77

loc_196D0:				; CODE XREF: start+647j start+649j
		xor	ax, ax
		xchg	ax, [cs:key_code]
		or	ax, ax
		jz	short loc_196D0
		js	short loc_196D0
		mov	BYTE [byte_1DE7F], 0
		cmp	ax, 15h
		jnz	loc_192FF
		mov	fs, [word_1DE52]
		mov	cx, [word_1DE54]

loc_196F1:				; CODE XREF: start+6BAj
		test	byte [fs:3], 40h
		jz	short loc_19744
		cmp	byte [fs:2], 2
		jnz	short loc_19744
		push	cx
		push	fs
		mov	cx, 602h
		mov	dx, 1A4Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7800h
		call	draw_frame
		pop	fs
		push	fs
		mov	eax, [fs:0Ch]
		mov	dword [aFile], eax ; "File"
		mov	eax, [fs:10h]
		mov	dword [aName], eax ; "name"
		mov	eax, [fs:14h]
		mov	dword [a_ext], eax ; ".Ext"
		mov	si, aDeletingFile ; "Deleting file: "
		mov	ax, 7E0Dh
		call	message_1BE77
		mov	dx, aFile ; "File"
		mov	ah, 41h
		int	21h		; DOS -	2+ - DELETE A FILE (UNLINK)
					; DS:DX	-> ASCIZ pathname of file to delete (no	wildcards allowed)
		pop	fs
		pop	cx

loc_19744:				; CODE XREF: start+665j start+66Dj
		mov	ax, fs
		add	ax, 3
		mov	fs, ax
		dec	cx
		jnz	short loc_196F1
		mov	WORD [word_1DE62], 0
		mov	WORD [word_1DE5E], 0
		mov	BYTE [byte_1DE7F], 1
		jmp	loc_192FF
; ---------------------------------------------------------------------------

loc_19762:				; CODE XREF: start+3ADj
					; DATA XREF: dseg:7C8Fo
		cmp	BYTE [byte_1DE7C], 1
		jz	loc_193BC
		mov	cx, 602h
		mov	dx, 1A4Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7800h
		call	draw_frame
		call	WORD [off_1DE3C]
		call	keyb_19EFD
		mov	BYTE [byte_1DE7F], 0
		jmp	loc_192F7
; ---------------------------------------------------------------------------

loc_19788:				; CODE XREF: start+3B9j
		mov	cx, 604h
		mov	dx, 84Bh
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame
		mov	cx, 906h
		mov	dx, 1949h
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame
		les	di, [videomempointer]
		add	di, 1042h
		mov	cx, 4Eh	; 'N'
		mov	ax, 7820h	; 'x'
		cld
		rep stosw
		mov	si, word_1D3B0
		les	di, [videomempointer]
		call	write_scr

loc_197BF:				; CODE XREF: start+733j
		cmp	byte [cs:key_code],	0
		jle	short loc_197BF
		mov	WORD [cs:key_code], 0
		mov	BYTE [byte_1DE7F], 0
		jmp	loc_192F7
; ---------------------------------------------------------------------------

loc_197D6:				; CODE XREF: start+3BFj
		call	mouse_deinit
		call	dosexec
		call	mouse_init
		mov	BYTE [byte_1DE7F], 0
		jmp	loc_192F7
; ---------------------------------------------------------------------------

loc_197E7:				; CODE XREF: start+3C5j
		xor	byte [configword], 20h
		jmp	loc_193BC


; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR start

loc_19827:				; CODE XREF: start+343j
		call	mouse_hide
		and	BYTE [byte_1DE90], 0FEh
		mov	bx, str_24461 ; mystr
		mov	ax, [mousecolumn]
		mov	bp, [mouserow]
		shr	ax, 3
		shr	bp, 3
		call	mouse_1C7CF
		jb	loc_193BC
		jmp	bx
; ---------------------------------------------------------------------------

loc_19848:				; CODE XREF: start+33Aj
		call	mouse_hide
		mov	bx, stru_2448B ;	mystr
		mov	ax, [mousecolumn]
		mov	bp, [mouserow]
		shr	ax, 3
		shr	bp, 3
		call	mouse_1C7CF
		jb	loc_193BC
		push	es
		xor	dx, dx
		mov	es, dx
		mov	edx, [es:46Ch]
		cmp	edx, [dword_1DE88]
		jz	short loc_1987C
		mov	[dword_1DE88], edx
		pop	es
		jmp	bx
; ---------------------------------------------------------------------------

loc_1987C:				; CODE XREF: start+7E0j
		pop	es
		jmp	loc_193BC
; END OF FUNCTION CHUNK	FOR start
; ---------------------------------------------------------------------------

loc_19880:				; DATA XREF: dseg:7C85o
		cmp	bp, 0Eh
		ja	loc_193BC
		mov	ax, bp
		jmp	loc_19464

; =============== S U B	R O U T	I N E =======================================


; void __usercall dosgetcurdir(char *str<esi>)
dosgetcurdir:	; CODE XREF: start+251p dosexec+53p
		push	si
		mov	ah, 19h
		int	21h		; DOS -	GET DEFAULT DISK NUMBER
		pop	si
		mov	[si], al
		mov	byte [si+1], '\'
		add	si, 2
		xor	dl, dl
		mov	ah, 47h
		int	21h		; DOS -	2+ - GET CURRENT DIRECTORY
					; DL = drive (0=default, 1=A, etc.)
					; DS:SI	points to 64-byte buffer area
		retn


; =============== S U B	R O U T	I N E =======================================


; void __usercall doschdir(char	*str<esi>)
doschdir:		; CODE XREF: start+5BFp dosexec+A6p
		mov	dl, [si]
		inc	si
		push	si
		mov	ah, 0Eh
		int	21h		; DOS -	SELECT DISK
					; DL = new default drive number	(0 = A,	1 = B, etc.)
					; Return: AL = number of logical drives
		pop	dx
		mov	ah, 3Bh
		int	21h		; DOS -	2+ - CHANGE THE	CURRENT	DIRECTORY (CHDIR)
					; DS:DX	-> ASCIZ directory name	(may include drive)
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR filelist_198B8

recolortxtx:				; CODE XREF: filelist_198B8+8j
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		jmp	recolortxt
; END OF FUNCTION CHUNK	FOR filelist_198B8

; =============== S U B	R O U T	I N E =======================================


filelist_198B8:	; CODE XREF: start:loc_193AEp

; FUNCTION CHUNK AT 0860 SIZE 00000008 BYTES

		cld
		mov	ax, [word_1DE5E]
		cmp	ax, [word_1DE60]
		jz	short recolortxtx
		mov	[word_1DE60], ax
		mov	cx, [word_1DE54]
		sub	cx, [word_1DE5E]
		cmp	cx, 0Fh
		jb	short loc_198D5
		mov	cx, 0Fh

loc_198D5:				; CODE XREF: filelist_198B8+18j
		mov	ax, [word_1DE5E]
		mov	dx, ax
		shl	ax, 1
		add	ax, dx
		add	ax, [word_1DE52]
		mov	fs, ax
		mov	ax, (80*10+10)*2

loc_198E7:				; CODE XREF: filelist_198B8+13Cj
		push	ax
		push	cx
		les	di, [videomempointer]
		add	di, ax
		mov	bp, di
		mov	ah, 7Eh	; '~'
		cmp	byte [fs:2], 2
		jz	short loc_198FD
		mov	ah, 7Bh	; '{'

loc_198FD:				; CODE XREF: filelist_198B8+41j
		mov	si, 0Ch
		mov	cx, 0Ch

loc_19903:				; CODE XREF: filelist_198B8+5Aj
		mov	al, [fs:si]
		or	al, al
		jz	short loc_19914	; " " fill the space after file	names
		mov	[es:di], ax
		inc	si
		add	di, 2
		dec	cx
		jnz	short loc_19903

loc_19914:				; CODE XREF: filelist_198B8+50j
		mov	ax, 7E20h	; " " fill the space after file	names
		cld
		rep stosw
		cmp	byte [fs:2], 2
		jz	short loc_1992A
		mov	cx, 51

loc_19925:
		rep stosw
		jmp	loc_199E7
; ---------------------------------------------------------------------------

loc_1992A:				; CODE XREF: filelist_198B8+68j
		push	bp
		mov	ax, ds
		mov	es, ax
		mov	di, buffer_1 ; 2800h
		mov	bp, 8		; count
		mov	eax, [fs:8]
		call	my_u32toa_fill

loc_1993D:
		mov	ax, [fs:6]
		and	al, 1Fh
		movzx	eax, al
		mov	bp, 3		; count
		call	my_u32toa_fill
		mov	byte [di], '-'

loc_19950:
		inc	di
		mov	ax, [fs:6]
		shr	ax, 5

loc_19958:
		and	eax, 0Fh
		lea	si, [aJanfebmaraprmayj+eax+eax*2] ; "	JanFebMarAprMayJunJulAugSepOctNovDec"
		cld
		movsw
		movsb
		mov	byte [di], '-'
		inc	di
		movzx	eax, word [fs:6]
		shr	ax, 9
		add	ax, 1980
		mov	bp, 4		; count
		call	my_u32toa_fill
		mov	byte [di], ' '
		inc	di
		mov	ax, [fs:4]
		shr	ax, 0Bh
		mov	dl, 10
		div	dl
		or	ax, '00'
		mov	[di], ax
		mov	byte [di+2], ':'
		mov	ax, [fs:4]
		shr	ax, 5
		and	ax, 3Fh	; '?'
		div	dl
		or	ax, '00'
		mov	[di+3],	ax
		mov	word [di+5], ' '
		pop	bp
		mov	si, buffer_1 ; str
		mov	es, word [videomempointer+2]
		lea	di, [bp+18h]
		mov	ah, 7Fh	; ''
		call	text_1BF69
		test	byte [fs:3], 40h
		jz	short loc_199CF
		mov	si, aMarkedToDelete ; "<Marked to Delete>    "
		mov	ah, 7Fh	; ''
		call	text_1BF69
		jmp	short loc_199E7
; ---------------------------------------------------------------------------

loc_199CF:				; CODE XREF: filelist_198B8+10Bj
		mov	ah, 7Eh	; '~'
		mov	si, 1Ah

loc_199D4:				; CODE XREF: filelist_198B8+12Dj
		mov	al, [fs:si]
		or	al, al
		jz	short loc_199E7
		mov	[es:di], ax
		inc	si
		add	di, 2
		cmp	si, 30h	; '0'
		jb	short loc_199D4

loc_199E7:				; CODE XREF: filelist_198B8+6Fj
					; filelist_198B8+115j ...
		mov	ax, fs
		add	ax, 3
		mov	fs, ax
		pop	cx
		pop	ax
		add	ax, 0A0h ; '†'
		dec	cx
		jnz	loc_198E7
		retn


; =============== S U B	R O U T	I N E =======================================


recolortxt:		; CODE XREF: start+324p start+4C1p ...
		imul	di, ax,	80*2
		add	di, (80*2*10)+(8*2)+1
		mov	cx, 64

loc_19A04:				; CODE XREF: recolortxt+19j
		mov	al, [es:di]
		and	al, 0Fh
		or	al, bl
		mov	[es:di], al
		add	di, 2
		dec	cx
		jnz	short loc_19A04
		retn


; =============== S U B	R O U T	I N E =======================================


cpy_printable:	; CODE XREF: modules_search+230p
		push	si
		push	di

loc_19A17:				; CODE XREF: cpy_printable+Ej
		mov	al, [si]
		inc	si
		cmp	al, ' '
		jb	short loc_19A25
		mov	[es:di], al
		inc	di
		dec	cx
		jnz	short loc_19A17

loc_19A25:				; CODE XREF: cpy_printable+7j
		cld
		mov	al, ' '
		rep stosb
		pop	di
		pop	si
		retn

; ---------------------------------------------------------------------------
		dec	cx
		jz	short locret_19A3E
		mov	al, [es:si]
		inc	si

loc_19A34:				; CODE XREF: seg001:09ECj
		xor	[es:si], al
		mov	al, [es:si]
		inc	si
		dec	cx
		jnz	short loc_19A34

locret_19A3E:				; CODE XREF: seg001:09DEj
		retn
; ---------------------------------------------------------------------------
		dec	cx
		jz	short locret_19A52
		mov	al, [es:si]
		inc	si

loc_19A46:				; CODE XREF: seg001:0A00j
		mov	ah, [es:si]
		xor	[es:si], al
		mov	al, ah
		inc	si
		dec	cx
		jnz	short loc_19A46

locret_19A52:				; CODE XREF: seg001:09F0j
		retn

; =============== S U B	R O U T	I N E =======================================


modules_search:	; CODE XREF: start+300p
		mov	WORD [word_1DE64], 2192
		mov	WORD [word_1DE66], 0
		cmp	WORD [word_1DE52], 0
		jz	short loc_19A6E
		mov	es, [word_1DE52]
		mov	ah, 49h
		int	21h		; DOS -	2+ - FREE MEMORY
					; ES = segment address of area to be freed

loc_19A6E:				; CODE XREF: modules_search+11j
		mov	bx, 1000h
		mov	ah, 48h
		int	21h		; DOS -	2+ - ALLOCATE MEMORY
					; BX = number of 16-byte paragraphs desired
		jb	loc_19250
		mov	[word_1DE52], ax
		mov	es, ax
		xor	di, di
		mov	cx, 4000h
		xor	eax, eax
		cld
		rep stosd
		mov	dword [buffer_1DB6C], 2A2E2Ah ; '*.*'
		mov	WORD [word_1DE5C], 0
		mov	WORD [word_1DE54], 0
		mov	WORD [word_1DE56], 0
		mov	WORD [word_1DE58], 0
		mov	WORD [word_1DE5A], 0
		cld
		mov	WORD [word_1DE4E], 12h
		call	find_mods
		mov	es, [word_1DE52]
		jb	loc_19CA2

loc_19AC3:				; CODE XREF: modules_search+CFj
		lfs	di, [videomempointer]
		add	di, [word_1DE64]
		mov	bx, [word_1DE66]
		mov	ah, 7Fh	; ''
		mov	al, byte [slider+bx] ; "ƒ\\|/ƒ\\|/"
		mov	[fs:di], ax
		inc	WORD [word_1DE66]
		and	WORD [word_1DE66], 7
		test	byte [unk_1DC01], 10h
		jz	short loc_19B1D
		cmp	word [buffer_1DB6C], '.'
		jz	short loc_19B1D
		mov	byte [es:2], 0
		mov	si, buffer_1DB6C
		mov	di, 0Ch
		cld
		movsd
		movsd
		movsd
		movsb
		inc	WORD [word_1DE56]
		mov	ax, es
		add	ax, 3
		mov	es, ax
		inc	WORD [word_1DE54]
		cmp	WORD [word_1DE54], 52Bh
		jnb	loc_19CA2

loc_19B1D:				; CODE XREF: modules_search+94j
					; modules_search+9Bj
		push	es
		call	dosfindnext
		pop	es
		jnb	short loc_19AC3

loc_19B24:				; '*.*'
		mov	dword [buffer_1DB6C], 2A2E2Ah
		mov	WORD [word_1DE4E], 2
		push	es
		call	find_mods
		pop	es
		jb	loc_19CA2

loc_19B3C:				; CODE XREF: modules_search+24Bj
		lfs	di, [videomempointer]
		add	di, [word_1DE64]
		mov	bx, [word_1DE66]
		mov	ah, 7Fh	; ''
		mov	al, byte [slider+bx] ; "ƒ\\|/ƒ\\|/"
		mov	[fs:di], ax
		inc	WORD [word_1DE66]
		and	WORD [word_1DE66], 7
		test	byte [unk_1DC01], 10h
		jnz	loc_19C99
		mov	si, buffer_1DB6C
		mov	cx, 8

loc_19B6A:				; CODE XREF: modules_search+125j
		inc	si
		cmp	byte [si], 0
		jz	loc_19C99
		cmp	byte [si], '.'
		jz	short loc_19B7D
		dec	cx
		jnz	short loc_19B6A
		jmp	loc_19C99
; ---------------------------------------------------------------------------

loc_19B7D:				; CODE XREF: modules_search+122j
		mov	edx, [si]
		mov	si, a_mod_nst_669_s ; ".MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FA"...

loc_19B83:				; CODE XREF: modules_search+13Fj
		mov	eax, [si]
		or	al, al
		jz	loc_19C99
		add	si, 4
		cmp	eax, edx
		jnz	short loc_19B83
		mov	si, buffer_1DB6C
		mov	dx, si
		mov	byte [es:2], 2
		mov	word [es:0], 0
		mov	di, 0Ch
		cld
		movsd
		movsd
		movsd
		movsb
		mov	si, unk_1DC01

loc_19BB4:
		mov	di, 3
		movsb
		and	byte [es:3], 3Fh ; '?'
		movsd
		movsd
		mov	ebp, eax
		inc	WORD [word_1DE58]
		cmp	WORD [cs:key_code], 1
		jnz	short loc_19BDD
		mov	WORD [cs:key_code], 0
		or	byte [configword], 20h

loc_19BDD:				; CODE XREF: modules_search+17Cj
		mov	si, asc_1DA00 ; "		      "
		mov	cx, 16h
		test	byte [configword], 20h
		jnz	loc_19C80
		mov	ax, 3D00h
		int	21h		; DOS -	2+ - OPEN DISK FILE WITH HANDLE
					; DS:DX	-> ASCIZ filename
					; AL = access mode
					; 0 - read
		jb	loc_19C86
		mov	bx, ax
		mov	dx, buffer_1DC6C
		mov	bx, ax
		mov	cx, 80h	; 'Ä'
		mov	ah, 3Fh	; '?'
		push	bx
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	bx
		pushf
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle
		popf
		jb	short loc_19C86
		mov	si, byte_1DC7C
		mov	cx, 16h
		cmp	ebp, 524E492Eh	; .INR
		jz	short loc_19C80
		mov	si, unk_1DC7B
		mov	cx, 16h
		cmp	ebp, 544C552Eh	; .ULT
		jz	short loc_19C80
		mov	si, unk_1DC70
		mov	cx, 16h
		cmp	ebp, 4D544D2Eh	; .MTM
		jz	short loc_19C80
		cmp	ebp, 4D53502Eh	; .PSM
		jz	short loc_19C80
		cmp	ebp, 5241462Eh	; .FAR
		jz	short loc_19C80
		cmp	ebp, 3936362Eh	; .669
		jz	short loc_19C71
		mov	si, byte_1DC7C
		mov	cx, 16h
		cmp	ebp, 5353542Eh	; .TSS
		jz	short loc_19C80
		mov	si, buffer_1DC6C
		mov	cx, 16h
		mov	word [si+14h], '  '
		jmp	short loc_19C80
; ---------------------------------------------------------------------------

loc_19C71:				; CODE XREF: modules_search+200j
		mov	si, (buffer_1DC6C+1)
		mov	cx, 54h	; 'T'

loc_19C77:				; CODE XREF: modules_search+228j
		inc	si
		cmp	byte [si], ' '
		loope	loc_19C77
		mov	cx, 16h

loc_19C80:				; CODE XREF: modules_search+195j
					; modules_search+1C7j ...
		mov	di, 1Ah
		call	cpy_printable

loc_19C86:				; CODE XREF: modules_search+19Ej
					; modules_search+1B8j
		mov	ax, es
		add	ax, 3
		mov	es, ax
		inc	WORD [word_1DE54]
		cmp	WORD [word_1DE54], 52Bh
		jnb	short loc_19CA2

loc_19C99:				; CODE XREF: modules_search+10Dj
					; modules_search+11Bj ...
		push	es
		call	dosfindnext
		pop	es
		jnb	loc_19B3C

loc_19CA2:				; CODE XREF: modules_search+6Cj
					; modules_search+C6j ...
		mov	ah, 19h
		int	21h		; DOS -	GET DEFAULT DISK NUMBER
		push	ax
		xor	dl, dl

loc_19CA9:				; CODE XREF: modules_search+291j
		push	dx
		mov	ah, 0Eh
		int	21h		; DOS -	SELECT DISK
					; DL = new default drive number	(0 = A,	1 = B, etc.)
					; Return: AL = number of logical drives
		mov	ah, 19h
		int	21h		; DOS -	GET DEFAULT DISK NUMBER
		pop	dx
		cmp	al, dl
		jnz	short loc_19CDF
		mov	eax, 5D3A415Bh	; [A:]
		add	ah, dl
		mov	[es:0Ch], eax
		mov	byte [es:10h], 0
		mov	byte [es:2], 1
		inc	WORD [word_1DE5A]
		mov	ax, es
		add	ax, 3
		mov	es, ax
		inc	WORD [word_1DE54]

loc_19CDF:				; CODE XREF: modules_search+262j
		inc	dl

loc_19CE1:
		cmp	dl, 1Ah
		jb	short loc_19CA9
		pop	dx
		mov	ah, 0Eh
		int	21h		; DOS -	SELECT DISK
					; DL = new default drive number	(0 = A,	1 = B, etc.)
					; Return: AL = number of logical drives
		mov	es, [word_1DE52]
		mov	ax, [word_1DE54]
		mov	bx, ax
		shl	ax, 1
		add	bx, ax
		mov	ah, 4Ah
		int	21h		; DOS -	2+ - ADJUST MEMORY BLOCK SIZE (SETBLOCK)
					; ES = segment address of block	to change
					; BX = new size	in paragraphs
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


parse_cmdline:	; CODE XREF: start+44p
		mov	ax, ds
		mov	es, ax
		xor	ebp, ebp
		mov	ds, [esseg_atstart]
		mov	si, 80h	; 'Ä'   ; psp:80h commandline
		mov	di, buffer_1DB6C
		xor	dl, dl
		cld
		lodsb
		movzx	cx, al		; number of bytes on commandline
		stc
		jcxz loc_19D64

loc_19D19:				; CODE XREF: parse_cmdline+29j
					; parse_cmdline+47j ...
		lodsb
		cmp	al, 0Dh
		jz	short loc_19D63
		or	al, al
		jz	short loc_19D63
		cmp	al, ' '
		jnz	short loc_19D4E
		dec	cx
		jnz	short loc_19D19
		stc
		jmp	short loc_19D64
; ---------------------------------------------------------------------------

loc_19D2C:				; CODE XREF: parse_cmdline+52j
		lodsb
		cmp	al, 0Dh
		jz	short loc_19D63
		or	al, al
		jz	short loc_19D63
		cmp	al, '?'
		jz	short loc_19D47
		and	al, 0DFh
		sub	al, 'A'
		movzx	eax, al
		bts	ebp, eax
		jmp	short loc_19D19
; ---------------------------------------------------------------------------

loc_19D47:				; CODE XREF: parse_cmdline+39j
		bts	ebp, 1Fh
		jmp	short loc_19D19
; ---------------------------------------------------------------------------

loc_19D4E:				; CODE XREF: parse_cmdline+26j
					; parse_cmdline+62j
		cmp	al, '/'
		jz	short loc_19D2C
		stosb
		lodsb
		cmp	al, 0Dh
		jz	short loc_19D63
		or	al, al
		jz	short loc_19D63
		cmp	al, ' '
		jz	short loc_19D63
		loop	loc_19D4E
		stosb

loc_19D63:				; CODE XREF: parse_cmdline+1Ej
					; parse_cmdline+22j ...
		clc

loc_19D64:				; CODE XREF: parse_cmdline+19j
					; parse_cmdline+2Cj
		mov	byte [es:di], 0
		mov	ax, es
		mov	ds, ax
		retn


; =============== S U B	R O U T	I N E =======================================


readallmoules:	; CODE XREF: start+1ABp
					; readallmoules+12j ...
		mov	dx, buffer_1DB6C
		call	read_module
		jb	short loc_19D83

loc_19D75:
		cmp	WORD [word_1DE50], 1
		jz	short loc_19D81
		call	dosfindnext
		jnb	short readallmoules

loc_19D81:				; CODE XREF: readallmoules+Dj
		clc
		retn
; ---------------------------------------------------------------------------

loc_19D83:				; CODE XREF: readallmoules+6j
		mov	BYTE [byte_1DE7E], 3
		mov	word [messagepointer], aModuleLoadErro ; "Module load error.\r\n$"
		mov	word [messagepointer+2], ds
		stc
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR start

loc_19D94:				; CODE XREF: start+18Ej
		mov	BYTE [byte_1DE7E], 4
		mov	word [messagepointer], aListFileNotFou ; "List file not found.\r\n$"
		mov	word [messagepointer+2], ds
		mov	dx, (buffer_1DB6C+1)
		mov	ax, 3D00h
		int	21h		; DOS -	2+ - OPEN DISK FILE WITH HANDLE
					; DS:DX	-> ASCIZ filename
					; AL = access mode
					; 0 - read
		jb	loc_19256
		push	ax
		call	callsubx
		pop	bx
		jb	loc_19256

loc_19DB8:				; CODE XREF: start+D4Fj start+D56j ...
		mov	dx, buffer_1DB6C

loc_19DBB:				; CODE XREF: start+D45j
		mov	cx, 1
		mov	ah, 3Fh	; '?'
		push	bx
		push	dx
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	dx
		pop	bx
		mov	di, dx
		jb	short loc_19E03
		or	ax, ax
		jz	short loc_19E03
		inc	dx
		cmp	byte [di], 1Ah
		jz	short loc_19E03
		cmp	byte [di], ' '
		jnb	short loc_19DBB
		mov	byte [di], 0
		cmp	BYTE [buffer_1DB6C],	0
		jz	short loc_19DB8
		cmp	BYTE [buffer_1DB6C],	';'
		jz	short loc_19DB8
		push	bx
		mov	WORD [word_1DE4E], 2
		call	find_mods
		jb	short loc_19DF9
		call	readallmoules

loc_19DF9:				; CODE XREF: start+D62j
		pop	bx
		cmp	WORD [word_1DE50], 1
		jnz	short loc_19DB8
		jmp	short loc_19E09
; ---------------------------------------------------------------------------

loc_19E03:				; CODE XREF: start+D36j start+D3Aj ...
		mov	byte [di], 0
		call	readallmoules

loc_19E09:				; CODE XREF: start+D6Fj
		mov	BYTE [byte_1DE7E], 0
		jmp	loc_19250
; END OF FUNCTION CHUNK	FOR start

; =============== S U B	R O U T	I N E =======================================


read_module:	; CODE XREF: start+424p
					; readallmoules+3p
		mov	BYTE [byte_1DE7E], 3
		mov	word [messagepointer], aModuleLoadErro ; "Module load error.\r\n$"
		mov	word [messagepointer+2], ds
		mov	si, dx

loc_19E22:				; CODE XREF: read_module+16j
		inc	si
		cmp	byte [si-1], 0
		jnz	short loc_19E22
		mov	cx, 0Ch

loc_19E2C:				; CODE XREF: read_module+2Dj
		dec	si
		cmp	byte [si-1], ':'
		jz	short loc_19E41
		cmp	byte [si-1], '\'
		jz	short loc_19E41
		cmp	si, dx
		jbe	short loc_19E41
		dec	cx
		jnz	short loc_19E2C
		dec	si

loc_19E41:				; CODE XREF: read_module+20j
					; read_module+26j ...
		mov	di, aFilename_ext ; "FileName.Ext"
		mov	cx, 0Ch

loc_19E47:				; CODE XREF: read_module+4Bj
		mov	al, [si]
		inc	si
		or	al, al
		jz	short loc_19E5E
		cmp	al, 'a'
		jb	short loc_19E58
		cmp	al, 'z'
		ja	short loc_19E58
		and	al, 0DFh	; upper	case

loc_19E58:				; CODE XREF: read_module+3Fj
					; read_module+43j
		mov	[di], al
		inc	di
		dec	cx
		jnz	short loc_19E47

loc_19E5E:				; CODE XREF: read_module+3Bj
		mov	ax, ds
		mov	es, ax
		mov	al, ' '
		cld
		rep stosb
		call far moduleread
		jb	loc_1A042
		mov	WORD [current_patterns], 0
		mov	BYTE [byte_1DE84], 0
		call far sub_126A9
		mov	dword [module_type_txt], eax ; "	"
		xor	ch, ch
		mov	[amount_of_x], cx
		mov	[byte_1DE73], bl
		call far read_sndsettings
		mov	[outp_freq], bp
		call far sub_1265D
		mov	[byte_1DE78], dl
		mov	al, dh
		and	al, 10h
		shr	al, 4
		mov	[byte_1DE7B], al
		mov	word [segfsbx_1DE28], si
		mov	word [segfsbx_1DE28+2], es
		mov	si, di
		mov	di, asc_1CC2D ; "			      "
		mov	cx, 30

loc_19EBA:				; CODE XREF: read_module+B4j
		mov	al, [es:si]
		or	al, al
		jz	short loc_19EC7
		mov	[di], al
		inc	si
		inc	di
		loop	loc_19EBA

loc_19EC7:				; CODE XREF: read_module+AEj
		mov	cx, 17
		xor	si, si

loc_19ECC:				; CODE XREF: read_module+C3j
		mov	al, [es:si]
		mov	byte [a130295211558+si], al	; "13/02/95 21:15:58"
		inc	si
		loop	loc_19ECC
		call	video_prp_mtr_positn
		xor	edx, edx
		mov	eax, 317
		movzx	ebx, WORD [amount_of_x]
		div	ebx
		mov	[volume_1DE34],	eax
		mov	BYTE [byte_1DE7C], 0
		call far sub_12EBA
		call	WORD [off_1DE3C]


; =============== S U B	R O U T	I N E =======================================


keyb_19EFD:		; CODE XREF: start+6EBp keyb_19EFD+5Aj ...
		call far sub_1265D
		mov	[byte_1DE72], ah
		mov	[byte_1DE74], al
		mov	[byte_1DE75], bh
		mov	[byte_1DE76], ch
		mov	ax, -1
		call far change_volume
		mov	[word_1DE6A], ax
		mov	ax, -1
		call far change_amplif
		mov	[word_1DE6C], ax
		call far get_playsettings
		mov	[flg_play_settings], al
		call	WORD [offs_draw]
		cmp	BYTE [byte_1DE7C], 1
		jz	loc_1A393
		test	BYTE [byte_1DE90], 2
		jnz	loc_1A3C5
		test	BYTE [byte_1DE90], 1
		jnz	loc_1A3A7
		xor	ax, ax
		xchg	ax, [cs:key_code]
		or	ax, ax
		jnz	short keyb_19EFDD
		hlt
		xchg	ax, [cs:key_code]
		or	ax, ax
		jz	short keyb_19EFD
keyb_19EFDD:
		mov	[word_1DE50], ax
		mov	cx, 2
		cmp	ax, 0E04Dh	; gr_right
		jz	l_1A044
		mov	cx, 10
		cmp	ax, 0E048h	; gr_up

loc_19F6C:
		jz	l_1A044
		mov	cx, 2
		cmp	ax, 0E04Bh	; gr_left
		jz	loc_1A070
		mov	ecx, 10
		cmp	ax, 0E050h
		jz	loc_1A070	; gr_down
		cmp	al, 4Dh	; 'M'
		jz	l_right
		cmp	al, 48h	; 'H'
		jz	l_up
		cmp	al, 4Bh	; 'K'
		jz	l_left
		cmp	al, 50h	; 'P'
		jz	l_down
		cmp	al, 4Eh	; 'N'
		jz	l_plus
		cmp	al, 4Ah	; 'J'
		jz	l_minus
		cmp	al, 1Ah
		jz	l_lbracket
		cmp	al, 1Bh
		jz	l_rbracket
		cmp	al, 3Bh	; ';'
		jz	l_f1
		cmp	al, 3Ch	; '<'
		jz	l_f2
		cmp	al, 3Dh	; '='
		jz	l_f3
		cmp	al, 3Eh	; '>'
		jz	l_f4
		cmp	al, 3Fh	; '?'
		jz	l_f5
		cmp	al, 40h	; '@'
		jz	l_f6
		cmp	al, 42h	; 'B'
		jz	l_f8
		cmp	al, 43h	; 'C'
		jz	l_f9
		cmp	al, 44h	; 'D'
		jz	l_f10
		cmp	al, 57h	; 'W'
		jz	l_f11
		cmp	al, 58h	; 'X'
		jz	l_f12
		cmp	al, 26h	; '&'
		jz	l_l
		cmp	al, 32h	; '2'
		jz	l_m
		cmp	al, 13h
		jz	l_r
		cmp	al, 1Fh
		jz	l_s
		cmp	al, 0Fh
		jz	l_tab
		cmp	al, 45h	; 'E'
		jz	l_numlock
		cmp	al, 46h	; 'F'
		jz	l_scrollock
		cmp	al, 4Fh	; 'O'
		jz	l_1_end
		cmp	al, 1Ch
		jz	l_enter
		cmp	al, 1
		jz	l_esc
		jb	keyb_19EFD
		cmp	al, 0Bh
		jbe	loc_1A33E
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

loc_1A042:				; CODE XREF: read_module+5Bj
		stc
		retn
; ---------------------------------------------------------------------------

l_1A044:				; CODE XREF: keyb_19EFD+65j
					; keyb_19EFD:loc_19F6Cj ...
		push	cx
		call far get_12F7C
		and	bx, 3Fh
		movzx	eax, ax
		shl	eax, 6
		or	al, bl
		inc	eax
		mov	bl, al
		and	bl, 3Fh
		shr	eax, 6
		mov	bh, 1
		call far sub_12F56
		pop	cx
		dec	cx
		jnz	short l_1A044
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

loc_1A070:				; CODE XREF: keyb_19EFD+79j
					; keyb_19EFD+86j ...
		push	cx
		call far get_12F7C
		and	bx, 3Fh
		movzx	eax, ax
		shl	eax, 6
		or	al, bl
		sub	eax, 1
		jb	short loc_1A0A0
		mov	bl, al
		and	bl, 3Fh
		shr	eax, 6
		mov	bh, 1
		call far sub_12F56
		pop	cx
		dec	cx
		jnz	short loc_1A070
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

loc_1A0A0:				; CODE XREF: keyb_19EFD+18Aj
		pop	cx
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_up:					; CODE XREF: keyb_19EFD+92j
		sub	BYTE [byte_1DE84], 1
		jnb	keyb_19EFD
		mov	BYTE [byte_1DE84], 0
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_down:					; CODE XREF: keyb_19EFD+9Ej
		inc	BYTE [byte_1DE84]
		mov	ax, [amount_of_x]
		cmp	[byte_1DE84], al
		jb	keyb_19EFD
		dec	al
		mov	[byte_1DE84], al
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_right:				; CODE XREF: keyb_19EFD+8Cj
		lfs	bx, [segfsbx_1DE28]
		mov	al, 50h	; 'P'
		mul	BYTE [byte_1DE84]
		add	bx, ax
		mov	cl, 8
		test	WORD [cs:keyb_switches], 3
		jnz	short loc_1A0E6
		mov	cl, 1

loc_1A0E6:				; CODE XREF: keyb_19EFD+1E5j
		mov	al, [fs:bx+3Ah]
		add	al, cl
		cmp	al, 80h	; 'Ä'
		jbe	short loc_1A0F2
		mov	al, 80h	; 'Ä'

loc_1A0F2:				; CODE XREF: keyb_19EFD+1F1j
					; keyb_19EFD+221j ...
		mov	ch, [byte_1DE84]
		call far sub_12AFD
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_left:					; CODE XREF: keyb_19EFD+98j
		lfs	bx, [segfsbx_1DE28]
		mov	al, 50h	; 'P'
		mul	BYTE [byte_1DE84]
		add	bx, ax
		mov	cl, 8
		test	WORD [cs:keyb_switches], 3
		jnz	short loc_1A118
		mov	cl, 1

loc_1A118:				; CODE XREF: keyb_19EFD+217j
		mov	al, [fs:bx+3Ah]
		sub	al, cl
		jnb	short loc_1A0F2
		mov	al, 0
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_l:					; CODE XREF: keyb_19EFD+FEj
		mov	al, 0
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_m:					; CODE XREF: keyb_19EFD+104j
		mov	al, 64
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_r:					; CODE XREF: keyb_19EFD+10Aj
		mov	al, 128
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_s:					; CODE XREF: keyb_19EFD+110j
		mov	al, 166
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_plus:					; CODE XREF: keyb_19EFD+A4j
		mov	ax, -1
		call far change_volume
		mov	cx, 32
		test	WORD [cs:keyb_switches], 3
		jnz	short loc_1A14B
		mov	cx, 2

loc_1A14B:				; CODE XREF: keyb_19EFD+249j
		add	ax, cx
		cmp	ax, 256
		jb	short loc_1A155
		mov	ax, 256

loc_1A155:				; CODE XREF: keyb_19EFD+253j
		call far change_volume
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_minus:				; CODE XREF: keyb_19EFD+AAj
		mov	ax, -1
		call far change_volume
		mov	cx, 32
		test	WORD [cs:keyb_switches], 3
		jnz	short loc_1A174
		mov	cx, 2

loc_1A174:				; CODE XREF: keyb_19EFD+272j
		sub	ax, cx
		jnb	short loc_1A17A
		xor	ax, ax

loc_1A17A:				; CODE XREF: keyb_19EFD+279j
		call far change_volume
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_rbracket:				; CODE XREF: keyb_19EFD+B6j
		mov	ax, 0FFFFh
		call far change_amplif
		mov	cx, 1
		test	WORD [cs:keyb_switches], 3
		jnz	short loc_1A199
		mov	cx, 0Ah

loc_1A199:				; CODE XREF: keyb_19EFD+297j
		add	ax, cx
		cmp	ax, 2500
		jb	short loc_1A1A3
		mov	ax, 2500

loc_1A1A3:				; CODE XREF: keyb_19EFD+2A1j
		call far change_amplif
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_lbracket:				; CODE XREF: keyb_19EFD+B0j
		mov	ax, -1
		call far change_amplif
		mov	cx, 1
		test	WORD [cs:keyb_switches], 3
		jnz	short loc_1A1C2
		mov	cx, 10

loc_1A1C2:				; CODE XREF: keyb_19EFD+2C0j
		sub	ax, cx
		jnb	short loc_1A1C9
		mov	ax, 50

loc_1A1C9:				; CODE XREF: keyb_19EFD+2C7j
		cmp	ax, 50
		ja	short loc_1A1D1
		mov	ax, 50

loc_1A1D1:				; CODE XREF: keyb_19EFD+2CFj
		call far change_amplif
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f1:					; CODE XREF: keyb_19EFD+BCj
		call	f1_help
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f2:					; CODE XREF: keyb_19EFD+C2j
		call	f2_waves
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f3:					; CODE XREF: keyb_19EFD+C8j
		call	f3_textmetter
		mov	BYTE [byte_1DE85], 0
		test	WORD [cs:keyb_switches], 3
		jz	keyb_19EFD
		mov	BYTE [byte_1DE85], 1
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f4:					; CODE XREF: keyb_19EFD+CEj
		cmp	WORD [offs_draw], f4_draw
		jnz	short loc_1A219
		mov	ax, [word_1DE6E]
		dec	ax
		add	[current_patterns], ax
		mov	ax, [current_patterns]
		cmp	ax, [word_1DE46]
		jb	short loc_1A21F

loc_1A219:				; CODE XREF: keyb_19EFD+309j
		mov	WORD [current_patterns], 0

loc_1A21F:				; CODE XREF: keyb_19EFD+31Aj
		call	f4_patternnae
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f5:					; CODE XREF: keyb_19EFD+D4j
		call	f5_graphspectr
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f6:					; CODE XREF: keyb_19EFD+DAj
		call	f6_undoc
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f8:					; CODE XREF: keyb_19EFD+E0j
		call	WORD [off_1DE42]
		call	dosexec
		mov	BYTE [byte_1DE70], 0FFh
		call	WORD [off_1DE3C]
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f9:					; CODE XREF: keyb_19EFD+E6j
		test	WORD [cs:keyb_switches], 100b
		jnz	short l_f11
		call far get_playsettings
		xor	al, 1
		call far set_playsettings
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f10:					; CODE XREF: keyb_19EFD+ECj
		test	WORD [cs:keyb_switches], 100b
		jnz	short l_f12
		call far get_playsettings
		xor	al, 2
		call far set_playsettings
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f11:					; CODE XREF: keyb_19EFD+F2j
					; keyb_19EFD+34Ej
		call far get_playsettings
		xor	al, 4
		call far set_playsettings
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_f12:					; CODE XREF: keyb_19EFD+F8j
					; keyb_19EFD+366j
		call far get_playsettings

loc_1A288:
		xor	al, 10h
		call far set_playsettings

loc_1A28F:
		xor	byte [configword+1], 1
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_tab:					; CODE XREF: keyb_19EFD+116j
		test	WORD [cs:keyb_switches], 100b
		jnz	short loc_1A2C1

loc_1A2A0:
		test	WORD [cs:keyb_switches], 1000b
		jnz	short loc_1A2D1
		test	WORD [cs:keyb_switches], 11b
		jnz	short loc_1A2E1
		call far get_playsettings
		xor	al, 8
		call far set_playsettings

loc_1A2BE:
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

loc_1A2C1:				; CODE XREF: keyb_19EFD+3A1j
		mov	cx, 0FFh
		xor	bx, bx
		mov	dx, 7D0Fh
		call far sub_12CAD
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

loc_1A2D1:				; CODE XREF: keyb_19EFD+3AAj
		mov	cx, 0FFh
		xor	bx, bx
		mov	dx, 910Fh
		call far sub_12CAD
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

loc_1A2E1:				; CODE XREF: keyb_19EFD+3B3j
		mov	cx, 0FFh
		xor	bx, bx
		mov	dx, 960Fh
		call far sub_12CAD
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_numlock:				; CODE XREF: keyb_19EFD+11Cj
		test	WORD [cs:keyb_switches], 100b
		jz	keyb_19EFD
		mov	al, 0FFh
		call far getset_playstate
		mov	ah, al
		mov	al, 1
		cmp	ah, al
		jnz	short loc_1A30D
		mov	al, 0

loc_1A30D:				; CODE XREF: keyb_19EFD+40Cj
		call far getset_playstate
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_scrollock:				; CODE XREF: keyb_19EFD+122j
		mov	al, 0FFh
		call far getset_playstate
		mov	ah, al
		mov	al, 2
		cmp	ah, al
		jnz	short loc_1A326
		mov	al, 0

loc_1A326:				; CODE XREF: keyb_19EFD+425j
		call far getset_playstate
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_1_end:				; CODE XREF: keyb_19EFD+128j
		mov	cx, 0FFh
		xor	bx, bx
		mov	dx, 0Dh
		call far sub_12CAD
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

loc_1A33E:				; CODE XREF: keyb_19EFD+13Ej
		sub	al, 2
		test	WORD [cs:keyb_switches], 11b
		jz	short loc_1A34B
		add	al, 10

loc_1A34B:				; CODE XREF: keyb_19EFD+44Aj
		test	WORD [cs:keyb_switches], 100b
		jz	short loc_1A356
		add	al, 20

loc_1A356:				; CODE XREF: keyb_19EFD+455j
		cmp	al, byte [amount_of_x]
		jnb	keyb_19EFD
		mov	ch, al
		lfs	bx, [segfsbx_1DE28]
		mov	ah, 80
		mul	ah
		add	bx, ax
		xor	byte [fs:bx+17h], 2
		mov	bx, 0FEh ; '˛'
		xor	cl, cl
		xor	dx, dx
		call far sub_12CAD
		jmp	keyb_19EFD
; ---------------------------------------------------------------------------

l_enter:				; CODE XREF: keyb_19EFD+12Ej
					; DATA XREF: dseg:stru_244ABo
		call	WORD [offs_draw]
		call	WORD [offs_draw2]
		clc
		retn
; ---------------------------------------------------------------------------

l_esc:					; CODE XREF: keyb_19EFD+134j
					; DATA XREF: dseg:stru_244B7o
		mov	BYTE [byte_1DE7C], 1
		and	BYTE [byte_1DE90], 0FDh

loc_1A393:				; CODE XREF: keyb_19EFD+3Bj
		call	WORD [offs_draw]
		call	WORD [offs_draw2]
		call far snd_offx
		call far memfree_125DA
		clc
		retn
; ---------------------------------------------------------------------------

loc_1A3A7:				; CODE XREF: keyb_19EFD+4Dj
		and	BYTE [byte_1DE90], 0FEh
		mov	bx, stru_244AB ;	mystr
		mov	ax, [mousecolumn]
		mov	bp, [mouserow]
		shr	ax, 3
		shr	bp, 3
		call	mouse_1C7CF
		jb	keyb_19EFD
		jmp	bx
; ---------------------------------------------------------------------------

loc_1A3C5:				; CODE XREF: keyb_19EFD+44j
		mov	bx, stru_244B7 ;	mystr
		mov	ax, [mousecolumn]
		mov	bp, [mouserow]
		shr	ax, 3
		shr	bp, 3
		call	mouse_1C7CF
		jb	keyb_19EFD
		push	es
		xor	dx, dx
		mov	es, dx
		mov	edx, [es:46Ch]
		cmp	edx, [dword_1DE88]
		jz	short loc_1A3F6
		mov	[dword_1DE88], edx
		pop	es
		jmp	bx
; ---------------------------------------------------------------------------

loc_1A3F6:				; CODE XREF: keyb_19EFD+4EFj
		pop	es
		jmp	loc_193BC


; =============== S U B	R O U T	I N E =======================================


f1_help:		; CODE XREF: keyb_19EFD:l_f1p
					; DATA XREF: dseg:02A6o
		mov	WORD [off_1DE3C], text_init
		mov	WORD [offs_draw], f1_draw
		mov	WORD [offs_draw2], text_init2
		mov	WORD [off_1DE42], loc_1A4A6
		call	text_init
		retn


; =============== S U B	R O U T	I N E =======================================


f2_waves:		; CODE XREF: keyb_19EFD:l_f2p
					; DATA XREF: dseg:02A0o
		mov	WORD [off_1DE3C], init_vga_waves
		mov	WORD [offs_draw], f2_draw_waves
		mov	WORD [offs_draw2], f2_draw_waves2
		mov	WORD [off_1DE42], init_vga_waves
		call	init_vga_waves
		retn


; =============== S U B	R O U T	I N E =======================================


f3_textmetter:	; CODE XREF: keyb_19EFD:l_f3p
					; DATA XREF: dseg:off_1CA8Eo
		mov	WORD [off_1DE3C], text_init
		mov	WORD [offs_draw], f3_draw
		mov	WORD [offs_draw2], text_init2
		mov	WORD [off_1DE42], loc_1A4A6
		call	text_init
		retn


; =============== S U B	R O U T	I N E =======================================


f4_patternnae:	; CODE XREF: keyb_19EFD:loc_1A21Fp
					; DATA XREF: dseg:02A4o
		mov	WORD [off_1DE3C], text_init
		mov	WORD [offs_draw], f4_draw
		mov	WORD [offs_draw2], text_init2
		mov	WORD [off_1DE42], loc_1A4A6
		call	text_init
		retn


; =============== S U B	R O U T	I N E =======================================


f5_graphspectr:	; CODE XREF: keyb_19EFD:l_f5p
					; DATA XREF: dseg:02A2o
		mov	WORD [off_1DE3C], init_f5_spectr
		mov	WORD [offs_draw], f5_draw_spectr
		mov	WORD [offs_draw2], f5_draw_spectr
		mov	WORD [off_1DE42], init_f5_spectr
		call	init_f5_spectr
		retn


; =============== S U B	R O U T	I N E =======================================


f6_undoc:		; CODE XREF: keyb_19EFD:l_f6p
					; DATA XREF: dseg:02A8o
		mov	WORD [off_1DE3C], text_init
		mov	WORD [offs_draw], f6_draw
		mov	WORD [offs_draw2], text_init2
		mov	WORD [off_1DE42], loc_1A4A6
		call	text_init
		retn


; =============== S U B	R O U T	I N E =======================================


text_init:		; CODE XREF: f1_help+18p
					; f3_textmetter+18p ...
		call	text_init2
		retn

; ---------------------------------------------------------------------------

loc_1A4A6:				; DATA XREF: f1_help+12o
					; f3_textmetter+12o ...
		call	text_init2
		retn

; =============== S U B	R O U T	I N E =======================================


text_init2:		; CODE XREF: text_initp
					; seg001:loc_1A4A6p
					; DATA XREF: ...

; FUNCTION CHUNK AT 14A2 SIZE 0000026B BYTES

		cmp	BYTE [byte_1DE86], 1
		jz	short loc_1A4F2
		cmp	WORD [amount_of_x], 0Ah
		jbe	short loc_1A4F2
		jmp	loc_1A5AB


; =============== S U B	R O U T	I N E =======================================


setvideomode:	; CODE XREF: start:loc_192F7p
					; text_init2:loc_1A4F2p
		cmp	BYTE [byte_1DE70], 0
		jz	short locret_1A4F1
		cmp	BYTE [byte_1DE70], 1
		jz	short locret_1A4F1
		mov	ax, 3
		cmp	BYTE [byte_1DE70], 2
		jnz	short loc_1A4D5
		or	al, 80h

loc_1A4D5:				; CODE XREF: setvideomode+16j
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		call	txt_blinkingoff
		cmp	BYTE [byte_1DE86], 1
		jz	short loc_1A4E8
		mov	ax, 1111h
		xor	bl, bl
		int	10h		; - VIDEO - TEXT-MODE CHARACTER	GENERATOR FUNCTIONS (PS, EGA, VGA)
					; AL = 00h, 10h: load user-specified patterns
					; AL = 01h, 11h: load ROM monochrome patterns (8 by 14)
					; AL = 02h, 12h: load ROM 8 by 8 double-dot patterns
					; AL = 03h: set	block specifier

loc_1A4E8:				; CODE XREF: setvideomode+24j
		mov	dx, 1D00h
		xor	bh, bh
		mov	ah, 2
		int	10h		; - VIDEO - SET	CURSOR POSITION
					; DH,DL	= row, column (0,0 = upper left)
					; BH = page number

locret_1A4F1:				; CODE XREF: setvideomode+5j
					; setvideomode+Cj
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR text_init2

loc_1A4F2:				; CODE XREF: text_init2+5j
					; text_init2+Cj
		call	setvideomode
		cmp	BYTE [byte_1DE86], 1
		jz	short loc_1A55B
		mov	WORD [word_1DE6E], 0Ah
		mov	eax, [videomempointer]
		add	ax, 36*80
		mov	[videopoint_shiftd], eax
		cmp	BYTE [byte_1DE70], 0
		jz	short loc_1A545
		cmp	BYTE [byte_1DE70], 1
		jz	short loc_1A529
		mov	cx, 0
		mov	dx, 1B4Fh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame

loc_1A529:				; CODE XREF: text_init2+6Fj
		mov	cx, 1103h
		mov	dx, 1A25h
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame
		mov	cx, 112Ah
		mov	dx, 1A4Ch
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame

loc_1A545:				; CODE XREF: text_init2+68j
		mov	cx, 501h
		mov	dx, 104Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame
		mov	BYTE [byte_1DE70], 0
		jmp	loc_1A628
; ---------------------------------------------------------------------------

loc_1A55B:				; CODE XREF: text_init2+50j
		mov	WORD [word_1DE6E], 7
		mov	eax, [videomempointer]
		add	ax, 30*80
		mov	[videopoint_shiftd], eax
		mov	cx, 0
		mov	dx, 184Fh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		mov	cx, 0E03h
		mov	dx, 1725h
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame
		mov	cx, 0E2Ah
		mov	dx, 174Ch
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame
		mov	cx, 501h
		mov	dx, 0D4Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame
		mov	BYTE [byte_1DE70], 0
		jmp	short loc_1A628
; ---------------------------------------------------------------------------

loc_1A5AB:				; CODE XREF: text_init2+Ej
		cmp	BYTE [byte_1DE70], 2
		jz	short loc_1A61A
		mov	ax, 3
		cmp	BYTE [byte_1DE70], 1
		jz	short loc_1A5C3
		cmp	BYTE [byte_1DE70], 0
		jnz	short loc_1A5C5

loc_1A5C3:				; CODE XREF: text_init2+110j
		or	al, 80h

loc_1A5C5:				; CODE XREF: text_init2+117j
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		call	txt_blinkingoff
		mov	ax, 1112h
		xor	bl, bl
		int	10h		; - VIDEO - TEXT-MODE CHARACTER	GENERATOR FUNCTIONS (PS, EGA, VGA)
					; AL = 00h, 10h: load user-specified patterns
					; AL = 01h, 11h: load ROM monochrome patterns (8 by 14)
					; AL = 02h, 12h: load ROM 8 by 8 double-dot patterns
					; AL = 03h: set	block specifier
		mov	dx, 3300h
		xor	bh, bh
		mov	ah, 2
		int	10h		; - VIDEO - SET	CURSOR POSITION
					; DH,DL	= row, column (0,0 = upper left)
					; BH = page number
		mov	BYTE [byte_1DE70], 2
		mov	WORD [word_1DE6E], 20h ; ' '
		mov	eax, [videomempointer]
		add	ax, 6400
		mov	[videopoint_shiftd], eax
		mov	cx, 0
		mov	dx, 314Fh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		mov	cx, 2703h
		mov	dx, 3025h
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame
		mov	cx, 272Ah
		mov	dx, 304Ch
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame

loc_1A61A:				; CODE XREF: text_init2+106j
		mov	cx, 501h
		mov	dx, 264Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame

loc_1A628:				; CODE XREF: text_init2+AEj
					; text_init2+FFj
		call	txt_draw_top_title
		mov	ax, ds
		mov	bx, buffer_1 ; 2800h
		shr	bx, 4
		add	ax, bx
		mov	[buffer_1seg], ax
		movzx	si, BYTE [snd_card_type]
		cmp	si, 0Ah
		jb	short loc_1A645
		mov	si, 0Ah

loc_1A645:				; CODE XREF: text_init2+196j
		shl	si, 1
		mov	si, [table_sndcrdname+si] ; str
		les	di, [videopoint_shiftd]
		add	di, 58h	; 'X'   ; videoptr
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		cmp	BYTE [snd_card_type], 0
		jnz	short loc_1A687
		push	di
		push	es
		call far sub_1265D
		pop	es
		pop	di
		mov	word [es:di], 7F20h
		add	di, 2		; videoptr
		movzx	si, dh
		and	si, 1100000b
		shr	si, 3
		add	si, a256	; str
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		mov	si, aKb	; str
		call	put_message

loc_1A687:				; CODE XREF: text_init2+1B2j
		cmp	BYTE [snd_card_type], 0Ah
		jz	short loc_1A6B7
		mov	si, (buffer_1DC6C+2)

loc_1A691:				; ' )'
		mov	word [buffer_1DC6C], 2820h
		xor	dx, dx

loc_1A699:
		mov	ax, [outp_freq]
		mov	cx, 1000
		div	cx

loc_1A6A1:
		call	my_u8toa10
		mov	dword [si],	297A486Bh ; 'kHz('
		mov	byte [si+4], 0
		mov	si, buffer_1DC6C	; str
		mov	ah, 7Fh	; ''   ; color
		call	put_message

loc_1A6B7:				; CODE XREF: text_init2+1E2j
		mov	al, 78h	; 'x'
		cmp	BYTE [byte_1DE7B], 1
		jnz	short loc_1A6C2
		mov	al, 7Ch	; '|'

loc_1A6C2:				; CODE XREF: text_init2+214j
		mov	[byte_1CCEB], al
		les	di, [videopoint_shiftd]
		mov	si, bottom_menu ; str
		call	write_scr
		call far sub_126A9
		mov	word [dword_1DE2C],	si
		mov	word [dword_1DE2C+2], es
		push	cx
		mov	si, buffer_1DC6C
		mov	al, ch
		push	bx
		call	my_u8toa10
		pop	bx
		mov	byte [si], '/'
		inc	si
		movzx	ax, bh
		mov	[word_1DE46], ax
		call	my_u8toa10
		mov	dword [si],	'   '
		mov	si, buffer_1DC6C	; str
		les	di, [videopoint_shiftd]
		add	di, 2AAh	; videoptr
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		pop	cx
		mov	si, buffer_1DC6C
		mov	al, cl
		call	my_u8toa10
		mov	dword [si],	'   '
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 20Ah	; videoptr
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		mov	bx, 0FFFFh
		mov	ah, 48h
		int	21h		; DOS -	2+ - ALLOCATE MEMORY
					; BX = number of 16-byte paragraphs desired
		mov	ax, bx
		shr	ax, 6
		mov	si, buffer_1DC6C
		call	my_u16toa10
		mov	dword [si],	20424Bh	; 'KB '
		cmp	si, (buffer_1DC6C+2)
		jb	short loc_1A74D
		mov	byte [si+2], 0

loc_1A74D:				; CODE XREF: text_init2+29Dj
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 12Eh	; videoptr
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		retn
; END OF FUNCTION CHUNK	FOR text_init2

; =============== S U B	R O U T	I N E =======================================


txt_draw_top_title:	; CODE XREF: start+201p start+27Bp ...
		mov	cx, 102h
		mov	dx, 44Dh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		les	di, [videomempointer]
		mov	si, atop_title ;	str
		call	write_scr
		retn


; =============== S U B	R O U T	I N E =======================================


txt_draw_bottom:	; CODE XREF: seg001:f3_drawp
					; seg001:f4_drawp ...
		mov	si, buffer_1DC6C
		mov	eax, '    '
		mov	[si], eax
		mov	[si+4],	eax
		mov	[si+8],	eax
		mov	[si+0Ch], al
		mov	byte [si+0Dh], 0
		mov	al, [byte_1DE75]
		call	my_u8toa10
		mov	dword [si],	20746120h ; ' at '
		add	si, 4
		mov	al, [byte_1DE76]
		call	my_u8toa10
		mov	word [si], 7062h ; bp
		mov	byte [si+2], 'm'
		mov	si, buffer_1DC6C	; str
		les	di, [videopoint_shiftd]
		add	di, 48Ah	; videoptr
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		mov	si, aPal	; "(PAL) "
		test	BYTE [flg_play_settings], 8
		jnz	short loc_1A7CC
		mov	si, aNtsc ; str

loc_1A7CC:				; CODE XREF: txt_draw_bottom+51j
		les	di, [videopoint_shiftd]
		add	di, 476h	; videoptr
		mov	ah, 7Eh	; '~'   ; color
		call	put_message
		mov	si, buffer_1DC6C
		mov	al, [byte_1DE72]
		inc	al
		call	my_u8toa10
		mov	byte [si], '/'
		inc	si
		mov	al, [byte_1DE73]
		call	my_u8toa10
		mov	dword [si],	'   '
		mov	si, buffer_1DC6C	; str
		les	di, [videopoint_shiftd]
		add	di, 34Ah	; videoptr
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		mov	si, buffer_1DC6C
		mov	al, [byte_1DE74]
		inc	al
		call	my_u8toa10
		mov	dword [si],	2034362Fh ; /64
		mov	word [si+4], ' '
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 3EAh	; videoptr
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		les	di, [videopoint_shiftd]
		add	di, 198h
		mov	ah, 7Ch	; '|'
		test	BYTE [flg_play_settings], 1
		jnz	short loc_1A83E
		mov	ah, 78h	; 'x'

loc_1A83E:				; CODE XREF: txt_draw_bottom+C4j
		mov	al, 0FEh ; '˛'
		mov	[es:di], ax
		les	di, [videopoint_shiftd]
		add	di, 238h
		mov	ah, 7Ch	; '|'
		test	BYTE [flg_play_settings], 2
		jnz	short loc_1A856
		mov	ah, 78h	; 'x'

loc_1A856:				; CODE XREF: txt_draw_bottom+DCj
		mov	al, 0FEh ; '˛'
		mov	[es:di], ax
		les	di, [videopoint_shiftd]
		add	di, 2D8h
		mov	ah, 7Ch	; '|'
		test	BYTE [flg_play_settings], 4
		jnz	short loc_1A86E
		mov	ah, 78h	; 'x'

loc_1A86E:				; CODE XREF: txt_draw_bottom+F4j
		mov	al, 0FEh ; '˛'
		mov	[es:di], ax
		les	di, [videopoint_shiftd]
		add	di, 378h	; interp text offset
		mov	ah, 7Ch	; '|'
		test	BYTE [flg_play_settings], 10h
		jnz	short loc_1A886
		mov	ah, 78h	; 'x'

loc_1A886:				; CODE XREF: txt_draw_bottom+10Cj
		mov	al, 0FEh ; '˛'
		mov	[es:di], ax
		mov	si, buffer_1DC6C
		imul	ax, [word_1DE6A], 100
		mov	al, ah
		call	my_u8toa10
		mov	dword [si],	202025h	; '%  '
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 43Ah	; videoptr
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		mov	si, buffer_1DC6C
		mov	ax, [word_1DE6C]
		call	my_u16toa10
		mov	dword [si],	202025h	; '%  '
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 4DAh	; videoptr
		mov	ah, 7Fh	; ''   ; color
		call	put_message
		mov	al, 0FFh
		call far getset_playstate
		movzx	si, al
		shl	si, 2
		add	si, aPlaypausloop ; "PlayPausLoop"
		les	di, [videopoint_shiftd]
		add	di, 0FCh ; '¸'
		mov	ah, 7Eh	; '~'
		mov	cx, 4

loc_1A8EB:				; CODE XREF: txt_draw_bottom+17Fj
		mov	al, [si]
		mov	[es:di], ax
		inc	si
		add	di, 2
		dec	cx
		jnz	short loc_1A8EB
		retn

; ---------------------------------------------------------------------------

f3_draw:				; DATA XREF: f3_textmetter+6o
		call	txt_draw_bottom
		cmp	BYTE [byte_1DE85], 1
		jz	short loc_1A913
		mov	es, [buffer_1seg]
		xor	di, di
		mov	cx, 50h	; 'P'
		mov	ax, 4001h
		call far volume_prep

loc_1A913:				; CODE XREF: seg001:18B0j
		mov	WORD [buffer_2seg], buffer_1 ; 2800h
		lfs	bx, [segfsbx_1DE28]
		les	di, [videomempointer]
		add	di, 3C4h
		mov	cx, [amount_of_x]
		cmp	cx, [word_1DE6E]
		jbe	short loc_1A934
		mov	cx, [word_1DE6E]

loc_1A934:				; CODE XREF: seg001:18DEj
		inc	BYTE [byte_1DE71]
		xor	ax, ax

loc_1A93A:				; CODE XREF: seg001:1AB8j
		push	ax
		push	cx
		push	di
		mov	dl, al
		add	al, '1'
		cmp	al, '9'
		jbe	short loc_1A947
		add	al, 7

loc_1A947:				; CODE XREF: seg001:18F3j
		mov	ah, 1Eh
		cmp	dl, [byte_1DE84]
		jz	short loc_1A951
		mov	ah, 7Eh	; '~'

loc_1A951:				; CODE XREF: seg001:18FDj
		mov	[es:di+2], ax
		mov	al, ' '
		mov	[es:di], ax
		mov	[es:di+4], ax
		add	di, 6
		movzx	si, byte [fs:bx+35h]
		mov	al, ' '
		test	si, 0Fh
		jz	short loc_1A975
		mov	ax, si
		shr	al, 4
		add	al, '0'

loc_1A975:				; CODE XREF: seg001:191Cj
		mov	ah, 7Fh	; ''
		mov	[es:di+4], ax
		and	si, 0Fh
		shl	si, 1
		mov	al, byte [notes+si]	; "  C-C#D-D#E-F-F#G-G#A-A#B-"
		mov	[es:di], ax
		mov	al, byte [(notes+1)+si]
		mov	[es:di+2], ax
		add	di, 8
		test	byte [fs:bx+17h], 1
		jnz	short loc_1A9AD
		mov	si, aMute ; "<Mute>		  "
		mov	ah, 7Fh	; ''
		test	byte [fs:bx+17h], 2
		jnz	short loc_1A9A8

loc_1A9A5:				; CODE XREF: seg001:1964j
		mov	si, asc_1DA00 ; "		      "

loc_1A9A8:				; CODE XREF: seg001:1953j
		call	put_message
		jmp	short loc_1A9C2
; ---------------------------------------------------------------------------

loc_1A9AD:				; CODE XREF: seg001:1947j
		movzx	eax, byte [fs:bx+2]
		dec	ax
		js	short loc_1A9A5
		shl	ax, 6
		mov	si, ax
		add	si, word [dword_1DE2C]
		call	txt_1ABAE

loc_1A9C2:				; CODE XREF: seg001:195Bj
		add	di, 2
		cmp	BYTE [byte_1DE85], 1
		jnz	short loc_1AA1A
		push	di
		push	es
		mov	ax, ds
		mov	es, ax
		mov	di, buffer_1 ; 2800h
		cld
		movzx	eax, byte [fs:bx+2]
		mov	bp, 2
		call	my_u32toa_fill
		mov	bp, 4
		movzx	eax, byte [fs:bx+22h]
		call	my_u32toa_fill
		mov	bp, 7
		movzx	eax, word [fs:bx+1Eh]
		call	my_u32toa_fill
		mov	ax, ds
		mov	es, ax
		mov	eax, '    '
		mov	cx, 4
		rep stosd
		mov	byte [di], 0
		pop	es
		pop	di
		mov	si, buffer_1 ; 2800h
		mov	ah, 7Eh	; '~'
		call	put_message

loc_1AA17:
		jmp	loc_1AACB
; ---------------------------------------------------------------------------

loc_1AA1A:				; CODE XREF: seg001:197Aj
		cmp	BYTE [snd_card_type], 0Ah
		jz	short loc_1AA62
		mov	si, [buffer_2seg]
		mov	cx, 50h	; 'P'
		xor	eax, eax
		xor	edx, edx

loc_1AA2E:				; CODE XREF: seg001:19EBj
		mov	dl, [si]
		or	dl, dl
		jns	short loc_1AA36
		neg	dl

loc_1AA36:				; CODE XREF: seg001:19E2j
		inc	si
		add	eax, edx
		dec	cx
		jnz	short loc_1AA2E
		mov	[buffer_2seg], si
		xor	edx, edx
		div	DWORD [volume_1DE34]
		cmp	al, 60
		jb	short loc_1AA4F
		mov	al, 60

loc_1AA4F:				; CODE XREF: seg001:19FBj
		cmp	BYTE [byte_1DE83], 0
		jz	short loc_1AA5C
		cmp	al, [fs:bx+1Ah]
		jb	short loc_1AA73

loc_1AA5C:				; CODE XREF: seg001:1A04j
		mov	[fs:bx+1Ah], al
		jmp	short loc_1AA88
; ---------------------------------------------------------------------------

loc_1AA62:				; CODE XREF: seg001:19CFj
		test	byte [fs:bx+17h], 1
		jz	short loc_1AA73
		mov	al, [fs:bx+22h]
		mov	[fs:bx+1Ah], al
		jmp	short loc_1AA88
; ---------------------------------------------------------------------------

loc_1AA73:				; CODE XREF: seg001:1A0Aj seg001:1A17j
					; DATA XREF: ...
		and	BYTE [byte_1DE71], 1Fh
		jnz	short loc_1AA88
		mov	al, [byte_1DE83]
		sub	[fs:bx+1Ah], al
		jns	short loc_1AA88
		mov	byte [fs:bx+1Ah], 0

loc_1AA88:				; CODE XREF: seg001:1A10j seg001:1A21j ...
		movzx	cx, byte [fs:bx+1Ah]
		shr	cx, 1
		mov	dx, 30
		sub	dx, cx
		jcxz volume_endstr
		mov	si, cx
		mov	cx, 0Dh
		cmp	si, cx
		ja	short volume_medium
		mov	cx, si

volume_medium:				; CODE XREF: seg001:1A4Dj
		mov	ax, 7A16h
		cld
		rep stosw
		sub	si, 0Dh
		jbe	short volume_endstr
		mov	cx, 0Ch
		cmp	si, cx
		ja	short volume_higher
		mov	cx, si

volume_higher:				; CODE XREF: seg001:1A61j
		mov	ah, 7Eh	; '~'
		rep stosw
		sub	si, 0Ch
		jbe	short volume_endstr
		mov	cx, si
		mov	ah, 7Ch	; '|'
		rep stosw

volume_endstr:				; CODE XREF: seg001:1A44j seg001:1A5Aj ...
		mov	cx, dx
		mov	ax, 7816h
		rep stosw

loc_1AACB:				; CODE XREF: seg001:loc_1AA17j
		pop	di
		push	di
		add	di, 7Ah	; 'z'
		mov	si, asc_1D6E0 ; "	       "
		mov	al, [fs:bx+0Ah]
		cmp	al, 1Dh
		jz	short loc_1AB0D
		cmp	al, 0Eh
		jnz	short loc_1AAF0
		mov	si, aSetLoopPoint ; "Set	Loop Point "
		mov	al, [fs:bx+0Bh]
		cmp	al, 60h	; '`'
		jz	short loc_1AAF7
		mov	si, aSetFilter ;	"Set Filter	"
		shr	al, 4

loc_1AAF0:				; CODE XREF: seg001:1A8Dj
		xor	ah, ah
		shl	ax, 4
		add	si, ax

loc_1AAF7:				; CODE XREF: seg001:1A98j seg001:1AF2j ...
		mov	ah, 7Eh	; '~'
		call	put_message
		pop	di
		pop	cx
		pop	ax
		add	di, 0A0h ; '†'
		add	bx, 50h	; 'P'
		inc	ax
		dec	cx
		jnz	loc_1A93A
		retn
; ---------------------------------------------------------------------------

loc_1AB0D:				; CODE XREF: seg001:1A89j
		mov	si, aArpeggio ; "Arpeggio       "
		mov	al, [fs:bx+0Bh]
		cmp	al, 37h	; '7'
		jz	short loc_1AB5D	; min
		cmp	al, 47h	; 'G'
		jz	short loc_1AB67	; maj
		cmp	al, 48h	; 'H'
		jz	short loc_1AB53	; puls
		xor	cl, cl
		call	sub_1AB8C
		mov	[si+9],	ax
		mov	cl, [fs:bx+0Bh]
		shr	cl, 4
		call	sub_1AB8C
		mov	[si+0Bh], ax
		mov	cl, [fs:bx+0Bh]
		and	cl, 0Fh
		call	sub_1AB8C
		mov	[si+0Dh], ax
		jmp	short loc_1AAF7
; ---------------------------------------------------------------------------

loc_1AB44:				; CODE XREF: seg001:1B26j seg001:1B2Aj
		mov	dword [si+9], '    '
		mov	word [si+0Dh], '  '
		jmp	short loc_1AAF7
; ---------------------------------------------------------------------------

loc_1AB53:				; CODE XREF: seg001:1ACEj
		mov	dword [si+0Bh], 73756C70h ;	puls
		jmp	short loc_1AB6F
; ---------------------------------------------------------------------------

loc_1AB5D:				; CODE XREF: seg001:1AC6j
		mov	dword [si+0Bh], 206E696Dh ;	min
		jmp	short loc_1AB6F
; ---------------------------------------------------------------------------

loc_1AB67:				; CODE XREF: seg001:1ACAj
		mov	dword [si+0Bh], 206A616Dh ;	maj

loc_1AB6F:				; CODE XREF: seg001:1B0Bj seg001:1B15j
		mov	al, [fs:bx+35h]
		and	ax, 0Fh
		jz	short loc_1AB44
		cmp	al, 0Ch
		ja	short loc_1AB44
		shl	ax, 1
		push	si
		mov	si, ax
		mov	ax, word [notes+si]	; "  C-C#D-D#E-F-F#G-G#A-A#B-"
		pop	si
		mov	[si+9],	ax
		jmp	loc_1AAF7

; =============== S U B	R O U T	I N E =======================================


sub_1AB8C:		; CODE XREF: seg001:1AD2p seg001:1ADFp ...
		mov	al, [fs:bx+35h]
		and	ax, 0Fh
		add	al, cl
		cmp	al, 0Ch
		jbe	short loc_1AB9B
		sub	al, 0Ch

loc_1AB9B:				; CODE XREF: sub_1AB8C+Bj
		shl	ax, 1
		push	si
		mov	si, ax
		mov	ax, word [notes+si]	; "  C-C#D-D#E-F-F#G-G#A-A#B-"
		pop	si
		cmp	ah, 2Dh	; '-'
		jz	short loc_1ABAB
		retn
; ---------------------------------------------------------------------------

loc_1ABAB:				; CODE XREF: sub_1AB8C+1Cj
		mov	ah, 20h	; ' '
		retn


; =============== S U B	R O U T	I N E =======================================


txt_1ABAE:		; CODE XREF: seg001:196Fp
		mov	ah, 7Bh	; '{'
		mov	cx, 16h

loc_1ABB3:				; CODE XREF: txt_1ABAE+10j
		mov	al, [fs:si]
		mov	[es:di], ax
		inc	si
		add	di, 2
		dec	cx
		jnz	short loc_1ABB3
		retn

; ---------------------------------------------------------------------------

f4_draw:				; DATA XREF: keyb_19EFD:l_f4o
					; f4_patternnae+6o
		call	txt_draw_bottom
		les	di, [videomempointer]
		add	di, 3C6h
		mov	si, aSamplename ; "# SampleName	 "
		mov	ah, 7Eh	; '~'
		call	text_1BF69
		mov	di, word [videomempointer]
		add	di, 464h
		lfs	bx, [dword_1DE2C]
		mov	bp, [current_patterns]
		imul	ax, bp,	40h
		add	bx, ax
		mov	dl, byte [word_1DE6E]
		dec	dl

loc_1ABF0:				; CODE XREF: seg001:1CA1j
		cmp	bp, [word_1DE46]
		jnb	locret_1ACF5
		push	bx
		push	dx
		push	bp
		push	di
		mov	ax, ds
		mov	es, ax
		mov	di, buffer_1 ; 2800h
		cld
		movzx	eax, bp
		inc	ax
		mov	bp, 2
		call	my_pnt_u32toa_fill
		mov	dword [di],	7B0220h	;  {
		add	di, 3
		mov	si, bx
		mov	cx, 8
		cld
		fs rep movsd
		test	byte [fs:bx+3Ch], 1
		jnz	short loc_1AC35
		mov	si, unk_1D6C3
		mov	cx, 9
		rep movsb
		jmp	loc_1ACD2
; ---------------------------------------------------------------------------

loc_1AC35:				; CODE XREF: seg001:1BD8j
		mov	eax, [fs:bx+20h]
		mov	bp, 7
		call	my_pnt_u32toa_fill
		movzx	eax, byte [fs:bx+3Dh]
		mov	bp, 3
		call	my_pnt_u32toa_fill
		mov	eax, 363120h	; ' 16'
		test	byte [fs:bx+3Ch], 4
		jnz	short loc_1AC5F
		mov	eax, 382020h	; '  8'

loc_1AC5F:				; CODE XREF: seg001:1C07j
		mov	[di], eax
		mov	al, 1Dh
		test	byte [fs:bx+3Ch], 10h
		jnz	short loc_1AC6D
		mov	al, ' '

loc_1AC6D:				; CODE XREF: seg001:1C19j
		mov	[di+3],	al
		add	di, 4
		movzx	eax, word [fs:bx+36h]
		mov	bp, 6
		call	my_pnt_u32toa_fill
		mov	dword [di],	7A487E02h ;  H
		add	di, 4
		mov	dword [di],	7F0220h	;  square
		add	di, 3
		mov	eax, '    '
		mov	ah, [fs:bx+3Eh]
		and	ah, 0Fh
		test	ah, 8
		jz	short loc_1ACAC
		mov	al, '-'
		neg	ah
		add	ah, 10h

loc_1ACAC:				; CODE XREF: seg001:1C53j
		or	ah, '0'
		mov	[di], eax
		add	di, 4
		test	byte [fs:bx+3Ch], 8
		jz	short loc_1ACD2
		mov	eax, [fs:bx+24h]
		mov	bp, 7
		call	my_pnt_u32toa_fill
		mov	eax, [fs:bx+2Ch]
		mov	bp, 7
		call	my_pnt_u32toa_fill

loc_1ACD2:				; CODE XREF: seg001:1BE2j seg001:1C6Aj
		mov	byte [di], 0
		pop	di
		push	di
		mov	es, word [videomempointer+2]
		mov	si, buffer_1 ; 2800h
		mov	ah, 7Fh	; ''
		call	text_1BF69
		pop	di
		pop	bp
		pop	dx
		pop	bx
		add	bx, 40h	; '@'
		inc	bp
		add	di, 0A0h ; '†'
		dec	dl
		jnz	loc_1ABF0

locret_1ACF5:				; CODE XREF: seg001:1BA4j
		retn

; =============== S U B	R O U T	I N E =======================================


; void __usercall my_pnt_u32toa_fill(int count<ebp>)
my_pnt_u32toa_fill:	; CODE XREF: seg001:1BBCp seg001:1BEDp ...
		mov	word [di], 7F02h
		add	di, 2


; =============== S U B	R O U T	I N E =======================================


; void __usercall my_u32toa_fill(int count<ebp>)
my_u32toa_fill:	; CODE XREF: filelist_198B8+82p
					; filelist_198B8+92p ...
		mov	si, buffer_1DC6C
		push	bx
		push	di
		push	bp
		call	my_u32toa10
		pop	bp
		pop	di
		pop	bx
		cmp	cx, bp
		jb	short loc_1AD0F
		mov	cx, bp

loc_1AD0F:				; CODE XREF: my_u32toa_fill+Ej
		sub	si, cx
		mov	dx, cx
		neg	cx
		add	cx, bp
		mov	al, ' '
		cld
		rep stosb
		mov	cx, dx
		rep movsb
		retn

; ---------------------------------------------------------------------------

f1_draw:				; DATA XREF: f1_help+6o
		call	txt_draw_bottom
		les	di, [videomempointer]
		mov	si, f1_help_text
		call	write_scr
		retn

; =============== S U B	R O U T	I N E =======================================


init_vga_waves:	; CODE XREF: f2_waves+18p
					; DATA XREF: f2_waveso	...

; FUNCTION CHUNK AT 1DDD SIZE 0000008D BYTES

		cmp	BYTE [byte_1DE70], 3
		jz	loc_1AEB2
		mov	BYTE [byte_1DE70], 3
		mov	ax, 12h		; VGA 640x480, 16-color; 80 bytes per line; 1 byte-8 pixels
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		mov	ax, ds
		mov	es, ax
		mov	dx, palette_24404
		mov	ax, 1002h
		int	10h		; - VIDEO - SET	ALL PALETTE REGISTERS (Jr, PS, TANDY 1000, EGA,	VGA)
					; ES:DX	-> 17-byte palette register list
		mov	dx, vga_palette
		mov	cx, 10h
		xor	bx, bx
		mov	ax, 1012h
		int	10h		; - VIDEO - SET	BLOCK OF DAC REGISTERS (EGA, VGA/MCGA)
					; BX = starting	color register,	CX = number of registers to set
					; ES:DX	-> table of 3*CX bytes where each 3 byte group represents one
					; byte each of red, green and blue (0-63)
		mov	si, buffer_1DC6C
		call	getexename
		jb	loc_1AE66
		mov	dx, buffer_1DC6C
		mov	ax, 3D00h
		int	21h		; DOS -	2+ - OPEN DISK FILE WITH HANDLE
					; DS:DX	-> ASCIZ filename
					; AL = access mode
					; 0 - read
		jb	loc_1AE66
		mov	[fhandle_1DE68], ax
		xor	dx, dx
		xor	cx, cx
		mov	bx, [fhandle_1DE68]
		mov	ax, 4202h	; get file size
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from end of file
		jb	loc_1AE5E
		mov	cx, dx
		mov	dx, ax
		sub	dx, 5AB3h	; read from the	end of file - 15AB3h = the size	of picture
		sbb	cx, 1
		mov	bx, [fhandle_1DE68]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		jb	loc_1AE5E
		mov	dx, buffer_1DC6C
		mov	cx, 2
		mov	bx, [fhandle_1DE68]
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		jb	loc_1AE5E
		cmp	ax, 2
		jnz	loc_1AE5E
		cmp	word [buffer_1DC6C], 4453h ; 'SD' check picture signature
		jnz	loc_1AE5E
		call	set_egasequencer
		call	read2buffer
		mov	dx, 3CEh
		mov	ax, 3
		out	dx, ax		; EGA: graph 1 and 2 addr reg:
					; data rotate and function select for write mode 00. Bits:
					; 0-2: set rotate count	for write mode 00
					; 3-4: fn for write modes 00 and 02
					;      00=no change; 01=AND; 10=OR; 11=XOR
		mov	ax, 0FF08h
		out	dx, ax		; EGA: graph 1 and 2 addr reg:
					; unknown register
		mov	ax, 0A000h
		mov	es, ax
		mov	dx, 3C4h
		mov	al, 2
		out	dx, al		; EGA: sequencer address reg
					; map mask: data bits 0-3 enable writes	to bit planes 0-3
		inc	dl
		xor	bx, bx

loc_1ADE0:				; CODE XREF: init_vga_waves+12Aj
		mov	ah, 1

loc_1ADE2:				; CODE XREF: init_vga_waves+121j
		mov	al, ah
		out	dx, al		; EGA port: sequencer data register
		xor	di, di

loc_1ADE7:				; CODE XREF: init_vga_waves+11Aj
		mov	cl, [si]
		inc	si
		cmp	si, buffer_1seg
		jnb	short loc_1AE0C	; WARNING: push	returns	address	to stack

loc_1ADF0:				; DATA XREF: init_vga_waves:loc_1AE0Co
		or	cl, cl
		js	short loc_1AE2D
		inc	cl

loc_1ADF6:				; CODE XREF: init_vga_waves+D9j
		mov	al, [es:bx+di]
		mov	al, [si]
		mov	[es:bx+di], al
		inc	si
		cmp	si, buffer_1seg
		jnb	short loc_1AE11

loc_1AE05:				; DATA XREF: init_vga_waves:loc_1AE11o
		inc	di
		dec	cl
		jnz	short loc_1ADF6
		jmp	short loc_1AE46
; ---------------------------------------------------------------------------

loc_1AE0C:				; CODE XREF: init_vga_waves+BFj
		push	loc_1ADF0 ; WARNING: push returns address to stack
		jmp	short read2buffer
; ---------------------------------------------------------------------------

loc_1AE11:				; CODE XREF: init_vga_waves+D4j
		push	loc_1AE05
		jmp	short read2buffer
; ---------------------------------------------------------------------------

loc_1AE16:				; CODE XREF: init_vga_waves+109j
		push	loc_1AE3A


; =============== S U B	R O U T	I N E =======================================


read2buffer:	; CODE XREF: init_vga_waves+94p
					; init_vga_waves+E0j ...
		pusha
		mov	dx, buffer_1 ; 2800h
		mov	cx, 5000h
		mov	bx, [fhandle_1DE68]
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		popa
		mov	si, buffer_1 ; 2800h
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR init_vga_waves

loc_1AE2D:				; CODE XREF: init_vga_waves+C3j
		neg	cl
		inc	cl
		mov	al, [si]
		inc	si
		cmp	si, buffer_1seg
		jnb	short loc_1AE16

loc_1AE3A:				; CODE XREF: init_vga_waves+115j
					; DATA XREF: init_vga_waves:loc_1AE16o
		test	byte [es:bx+di], 0
		mov	[es:bx+di], al
		inc	di
		dec	cl
		jnz	short loc_1AE3A

loc_1AE46:				; CODE XREF: init_vga_waves+DBj
		cmp	di, 50h	; 'P'
		jb	short loc_1ADE7
		shl	ah, 1
		test	ah, 10h
		jz	short loc_1ADE2
		add	bx, 50h	; 'P'
		cmp	bx, 9600h
		jb	short loc_1ADE0
		call	graph_1C070

loc_1AE5E:				; CODE XREF: init_vga_waves+52j
					; init_vga_waves+6Aj ...
		mov	bx, [fhandle_1DE68]
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle

loc_1AE66:				; CODE XREF: init_vga_waves+32j
					; init_vga_waves+3Ej
		pushf
		cli
		mov	dx, 3C4h
		mov	ax, 802h
		out	dx, ax		; EGA: sequencer address reg
					; unknown register
		mov	dx, 3CEh
		mov	ax, 205h
		out	dx, ax		; EGA: graph 1 and 2 addr reg:
					; unknown register
		mov	ax, 3
		out	dx, ax		; EGA: graph 1 and 2 addr reg:
					; data rotate and function select for write mode 00. Bits:
					; 0-2: set rotate count	for write mode 00
					; 3-4: fn for write modes 00 and 02
					;      00=no change; 01=AND; 10=OR; 11=XOR
		popf
		call	video_prp_mtr_positn

loc_1AE7E:				; CODE XREF: init_vga_waves+189j
					; f2_draw_waves2+69j
		mov	ax, ds
		mov	bx, buffer_1 ; 2800h
		shr	bx, 4
		add	ax, bx
		mov	[buffer_1seg], ax
		add	ax, 280h	; (offset buffer_206E0 - offset	buffer_1DEE0)/16
		mov	[buffer_2seg], ax
		mov	ax, ds
		mov	es, ax
		mov	di, buffer_1 ; 2800h
		mov	cx, 0A00h
		xor	eax, eax
		cld
		rep stosd
		mov	di, buffer_2
		mov	cx, 0A00h
		mov	eax, 1010101h
		rep stosd
		retn
; ---------------------------------------------------------------------------

loc_1AEB2:				; CODE XREF: init_vga_waves+5j
		call	f2_draw_waves2
		call	video_prp_mtr_positn
		jmp	short loc_1AE7E
; END OF FUNCTION CHUNK	FOR init_vga_waves

; =============== S U B	R O U T	I N E =======================================


f2_draw_waves:	; DATA XREF: f2_waves+6o
		mov	es, [buffer_1seg]
		xor	di, di
		mov	cx, 128h
		mov	ax, 0C001h
		call far volume_prep
		mov	ax, 0A000h
		mov	es, ax
		mov	fs, [buffer_1seg]
		mov	gs, [buffer_2seg]
		mov	di, x_storage
		xor	si, si
		mov	cx, [amount_of_x]

lc_next_meter:				; CODE XREF: f2_draw_waves+9Cj
		push	cx
		push	si
		push	di
		mov	bp, [di]	; bp = x * 8
		mov	dx, 3CEh
		mov	al, 8
		out	dx, al		; EGA: graph 1 and 2 addr reg:
					; bit mask
					; Bits 0-7 select bits to be masked in all planes
		mov	al, 10000000b	; bits of display memory which can be modified

lc_nextvideobit:			; CODE XREF: f2_draw_waves+8Fj
		mov	ah, 37		; 37 * 8 = 296 by x
		mov	dx, 3CFh
		out	dx, al		; EGA port: graphics controller	data register
		mov	bx, bp		; reinit (x*8)

lc_next_x8:				; CODE XREF: f2_draw_waves+86j
		movsx	di, byte [gs:si] ; y1
		movsx	dx, byte [fs:si] ; y2
		cmp	di, dx
		jz	short loc_1AF3A
		neg	di
		mov	cx, di
		shl	di, 6
		shl	cx, 4		; multiply by 80 (1 line 80 bytes)
		add	di, cx		; di = y * 80
		lea	cx, [bx+di]
		or	cx, cx		; y * 80 + x
		js	short loc_1AF1E
		cmp	cx, 280*80	; bottom y margin 280
		jnb	short loc_1AF1E
		and	byte [es:bx+di], 111b ; clean previous dot

loc_1AF1E:				; CODE XREF: f2_draw_waves+58j
					; f2_draw_waves+5Ej
		neg	dx
		mov	di, dx
		shl	di, 6
		shl	dx, 4
		add	di, dx
		lea	cx, [bx+di]
		or	cx, cx
		js	short loc_1AF3A
		cmp	cx, 280*80
		jnb	short loc_1AF3A
		or	byte [es:bx+di], 1000b ; set new dot

loc_1AF3A:				; CODE XREF: f2_draw_waves+46j
					; f2_draw_waves+74j ...
		add	si, 8
		inc	bx		; (x*8)++
		dec	ah
		jnz	short lc_next_x8 ; y1
		sub	si, 128h
		inc	si
		shr	al, 1		; next video bit
		jnb	short lc_nextvideobit ;	37 * 8 = 296 by	x
		pop	di
		pop	si
		pop	cx
		add	si, 128h
		add	di, 2		; next x
		dec	cx
		jnz	short lc_next_meter
		mov	ax, [buffer_1seg]
		xchg	ax, [buffer_2seg]
		mov	[buffer_1seg], ax
		retn


; =============== S U B	R O U T	I N E =======================================


f2_draw_waves2:	; CODE XREF: init_vga_waves:loc_1AEB2p
					; DATA XREF: f2_waves+Co
		mov	ax, 0A000h
		mov	es, ax
		mov	fs, [buffer_1seg]
		mov	gs, [buffer_2seg]
		mov	di, x_storage
		xor	si, si
		mov	cx, [amount_of_x]

loc_1AF79:				; CODE XREF: f2_draw_waves2+67j
		push	cx
		push	si
		push	di
		mov	bp, [di]
		mov	dx, 3CEh
		mov	al, 8
		out	dx, al		; EGA: graph 1 and 2 addr reg:
					; bit mask
					; Bits 0-7 select bits to be masked in all planes
		mov	al, 10000000b

loc_1AF86:				; CODE XREF: f2_draw_waves2+5Aj
		mov	ah, 37
		mov	dx, 3CFh
		out	dx, al		; EGA port: graphics controller	data register
		mov	bx, bp

loc_1AF8E:				; CODE XREF: f2_draw_waves2+51j
		movsx	di, byte [gs:si]
		neg	di
		mov	cx, di
		shl	di, 6
		shl	cx, 4
		add	di, cx
		lea	cx, [bx+di]
		or	cx, cx
		js	short loc_1AFAE
		cmp	cx, 22400
		jnb	short loc_1AFAE
		and	byte [es:bx+di], 111b

loc_1AFAE:				; CODE XREF: f2_draw_waves2+3Fj
					; f2_draw_waves2+45j
		add	si, 8
		inc	bx
		dec	ah
		jnz	short loc_1AF8E
		sub	si, 128h
		inc	si
		shr	al, 1
		jnb	short loc_1AF86
		pop	di
		pop	si
		pop	cx
		add	si, 128h
		add	di, 2
		dec	cx
		jnz	short loc_1AF79
		jmp	loc_1AE7E


; =============== S U B	R O U T	I N E =======================================


init_f5_spectr:	; CODE XREF: f5_graphspectr+18p
					; DATA XREF: f5_graphspectro ...
		cmp	BYTE [byte_1DE70], 4
		jz	locret_1B083
		mov	BYTE [byte_1DE70], 4
		mov	ax, 13h
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		call	set_egasequencer
		mov	dx, 3C8h
		xor	al, al
		out	dx, al
		jmp	short $+2
		jmp	short $+2
		inc	dx
		out	dx, al
		jmp	short $+2
		out	dx, al
		jmp	short $+2
		out	dx, al
		jmp	short $+2
		mov	bp, 16Ch
		xor	bx, bx

loc_1AFFE:				; CODE XREF: init_f5_spectr+43j
		mov	al, bh
		out	dx, al
		jmp	short $+2
		mov	al, 3Fh	; '?'
		out	dx, al
		jmp	short $+2
		xor	al, al
		out	dx, al
		jmp	short $+2
		add	bx, bp
		cmp	bh, 40h	; '@'
		jb	short loc_1AFFE

loc_1B014:				; CODE XREF: init_f5_spectr+58j
		sub	bx, bp
		mov	al, 3Fh	; '?'
		out	dx, al
		jmp	short $+2
		mov	al, bh
		out	dx, al
		jmp	short $+2
		xor	al, al
		out	dx, al
		jmp	short $+2
		or	bh, bh
		jns	short loc_1B014
		mov	dx, 3C8h
		mov	al, 0FCh ; '¸'
		out	dx, al
		jmp	short $+2
		jmp	short $+2
		inc	dx
		xor	al, al
		out	dx, al
		jmp	short $+2
		out	dx, al
		jmp	short $+2
		out	dx, al
		jmp	short $+2
		mov	al, 10h
		out	dx, al
		jmp	short $+2
		out	dx, al
		jmp	short $+2
		mov	al, 30h	; '0'
		out	dx, al
		jmp	short $+2
		mov	al, 10h
		out	dx, al
		jmp	short $+2
		out	dx, al
		jmp	short $+2
		out	dx, al
		jmp	short $+2
		mov	al, 3Fh	; '?'
		out	dx, al
		jmp	short $+2
		out	dx, al
		jmp	short $+2
		out	dx, al
		call	graph_1C070
		mov	ax, ds
		mov	es, ax
		mov	di, unk_23EE4
		mov	cx, 0C8h ; '»'
		xor	eax, eax
		cld
		rep stosd
		mov	ax, 200h
		test	byte [configword], 8
		jnz	short loc_1B080
		shr	ax, 1

loc_1B080:				; CODE XREF: init_f5_spectr+ADj
		mov	[word_24524], ax

locret_1B083:				; CODE XREF: init_f5_spectr+5j
		retn


; =============== S U B	R O U T	I N E =======================================


spectr_1B084:
		mov	[word_2450E], di
		mov	al, 1
		cmp	al, 1
		jnz	loc_1B240
		call	spectr_1B406
		mov	ax, [word_24514]
		xor	si, si

loc_1B098:				; CODE XREF: spectr_1B084+1Bj
		add	si, 4
		shr	ax, 1
		test	ax, ax
		jnz	short loc_1B098
		sub	si, 4
		mov	ebx, [tabledword_24526+si]
		mov	[multip_244D0],	ebx
		mov	eax, [tabledword_24562+si]
		mov	[multip_244CC],	eax
		add	eax, 10000h
		mov	[dword_244C8], eax
		mov	[dword_244D4], ebx
		mov	cx, [word_24514]
		shr	cx, 1
		mov	ax, 2

loc_1B0CF:				; CODE XREF: spectr_1B084+1A2j
		push	cx
		push	ax
		shl	ax, 1
		dec	ax
		mov	di, ax
		inc	ax
		neg	ax
		add	ax, 3
		add	ax, [word_24514]
		add	ax, [word_24514]
		mov	si, ax
		mov	eax, [dword_244C8]
		mov	[dword_244F4], eax
		mov	eax, [dword_244D4]
		mov	[dword_244F8], eax
		dec	si
		shl	si, 2
		dec	di

loc_1B0FB:
		shl	di, 2
		add	si, [word_2450E]
		add	di, [word_2450E]
		mov	eax, [di]
		add	eax, [si]
		sar	eax, 1
		mov	[dword_244E4], eax
		mov	eax, [di+4]
		sub	eax, [si+4]
		sar	eax, 1
		mov	[dword_244E8], eax
		mov	eax, [di+4]
		add	eax, [si+4]
		sar	eax, 1
		mov	[dword_244EC], eax
		mov	eax, [si]

loc_1B134:
		sub	eax, [di]
		sar	eax, 1
		mov	[dword_244F0], eax
		mov	ecx, [dword_244F4]
		mov	eax, [dword_244EC]
		imul	ecx
		shrd	eax, edx, 16
		mov	[dword_244FC], eax
		mov	eax, [dword_244F0]
		imul	ecx
		shrd	eax, edx, 16
		mov	[dword_24500], eax
		mov	ecx, [dword_244F8]
		mov	eax, [dword_244EC]
		imul	ecx
		shrd	eax, edx, 16
		mov	[dword_24508], eax
		mov	eax, [dword_244F0]
		imul	ecx
		shrd	eax, edx, 16
		mov	[dword_24504], eax
		mov	eax, [dword_244E4]
		add	eax, [dword_244FC]
		sub	eax, [dword_24504]
		mov	[di], eax
		mov	eax, [dword_244E8]
		add	eax, [dword_24500]
		add	eax, [dword_24508]
		mov	[di+4],	eax
		mov	eax, [dword_244E4]
		sub	eax, [dword_244FC]
		add	eax, [dword_24504]
		mov	[si], eax
		mov	eax, [dword_24500]
		sub	eax, [dword_244E8]
		add	eax, [dword_24508]
		mov	[si+4],	eax
		mov	eax, [dword_244C8]
		mov	dword [unk_244C4], eax
		mov	eax, [multip_244CC]
		imul	DWORD [dword_244C8]
		shrd	eax, edx, 10h
		add	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	DWORD [multip_244D0]
		shrd	eax, edx, 10h
		sub	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	DWORD [multip_244CC]
		shrd	eax, edx, 10h
		add	[dword_244D4], eax
		mov	eax, dword	[unk_244C4]
		imul	DWORD [multip_244D0]
		shrd	eax, edx, 10h
		add	[dword_244D4], eax
		pop	ax
		pop	cx
		inc	ax
		dec	cx
		jnz	loc_1B0CF
		mov	si, [word_2450E]
		mov	eax, [si]
		mov	ebx, [si+4]
		add	[si], ebx
		sub	eax, ebx
		mov	[si+4],	eax
		retn
; ---------------------------------------------------------------------------

loc_1B240:				; CODE XREF: spectr_1B084+8j
		mov	ax, [word_24514]
		xor	si, si

loc_1B245:				; CODE XREF: spectr_1B084+1C8j
		add	si, 4
		shr	ax, 1
		test	ax, ax
		jnz	short loc_1B245
		sub	si, 4
		mov	ebx, [tabledword_24526+si]
		neg	ebx
		mov	[multip_244D0],	ebx
		mov	eax, [tabledword_24562+si]
		neg	eax
		mov	[multip_244CC],	eax
		add	eax, 10000h
		mov	[dword_244C8], eax
		mov	[dword_244D4], ebx
		mov	cx, [word_24514]
		shr	cx, 1
		mov	ax, 2

loc_1B282:				; CODE XREF: spectr_1B084+357j
		push	cx
		push	ax
		shl	ax, 1
		dec	ax
		mov	di, ax
		neg	ax
		add	ax, 3
		add	ax, [word_24514]
		add	ax, [word_24514]
		mov	si, ax
		mov	eax, [dword_244C8]
		mov	[dword_244F4], eax
		mov	eax, [dword_244D4]
		mov	[dword_244F8], eax
		dec	si
		shl	si, 2
		dec	di
		shl	di, 2
		mov	eax, [di]
		add	eax, [si]
		sar	eax, 1
		mov	[dword_244E4], eax
		mov	eax, [di+4]
		sub	eax, [si+4]
		sar	eax, 1
		mov	[dword_244E8], eax
		mov	eax, [di+4]
		add	eax, [si+4]
		neg	eax
		sar	eax, 1
		mov	[dword_244EC], eax
		mov	eax, [di]
		sub	eax, [si]
		sar	eax, 1
		mov	[dword_244F0], eax
		mov	ecx, [dword_244F4]
		mov	eax, [dword_244EC]
		imul	ecx
		shrd	eax, edx, 10h
		mov	[dword_244FC], eax
		mov	eax, [dword_244F0]
		imul	ecx
		shrd	eax, edx, 10h
		mov	[dword_24500], eax
		mov	ecx, [dword_244F8]
		mov	eax, [dword_244EC]
		imul	ecx
		shrd	eax, edx, 10h
		mov	[dword_24508], eax
		mov	eax, [dword_244F0]
		imul	ecx
		shrd	eax, edx, 10h
		mov	[dword_24504], eax
		mov	eax, [dword_244E4]
		add	eax, [dword_244FC]
		sub	eax, [dword_24504]
		mov	[di], eax
		mov	eax, [dword_244E8]
		add	eax, [dword_24500]
		add	eax, [dword_24508]
		mov	[di+4],	eax
		mov	eax, [dword_244E4]
		sub	eax, [dword_244FC]
		add	eax, [dword_24504]
		mov	[si], eax
		mov	eax, [dword_24500]
		sub	eax, [dword_244E8]
		add	eax, [dword_24508]
		mov	[si+4],	eax
		mov	eax, [dword_244C8]
		mov	dword [unk_244C4], eax
		mov	eax, [dword_244C8]
		mov	dword [unk_244C4], eax
		mov	eax, [multip_244CC]
		imul	DWORD [dword_244C8]
		shrd	eax, edx, 10h
		add	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	DWORD [multip_244D0]
		shrd	eax, edx, 10h
		sub	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	DWORD [multip_244CC]
		shrd	eax, edx, 10h
		add	[dword_244D4], eax
		mov	eax, dword	[unk_244C4]
		imul	DWORD [multip_244D0]
		shrd	eax, edx, 10h
		add	[dword_244D4], eax
		pop	ax
		pop	cx
		inc	ax
		dec	cx
		jnz	loc_1B282
		mov	si, [word_2450E]
		mov	eax, [si]
		mov	ebx, [si+4]
		mov	ecx, eax
		add	ecx, ebx
		sar	ecx, 1
		mov	[si], ecx
		mov	ecx, eax
		sub	ecx, ebx
		sar	ecx, 1
		mov	[si], ecx
		call	spectr_1B406
		retn


; =============== S U B	R O U T	I N E =======================================


spectr_1B406:	; CODE XREF: spectr_1B084+Cp
					; spectr_1B084+37Ep ...
		mov	[word_2450E], di
		mov	WORD [word_2450C], 0
		mov	cx, [word_24520]
		shl	cx, 1
		mov	[word_24522], cx
		mov	si, [word_2450E]
		shr	cx, 1
		mov	di, [word_2450E]
		mov	bp, di

loc_1B426:				; CODE XREF: spectr_1B406+5Fj
		push	cx
		cmp	si, di
		jle	short loc_1B440
		mov	edx, [si]
		mov	ebx, [si+4]
		xchg	edx, [di]
		xchg	ebx, [di+4]
		mov	[si], edx
		mov	[si+4],	ebx

loc_1B440:				; CODE XREF: spectr_1B406+23j
		sub	si, bp
		shr	si, 2
		mov	ax, [word_24522]
		shr	ax, 1

loc_1B44A:				; CODE XREF: spectr_1B406+51j
		cmp	ax, 2
		jl	short loc_1B459
		cmp	si, ax
		jl	short loc_1B459
		sub	si, ax
		shr	ax, 1
		jmp	short loc_1B44A
; ---------------------------------------------------------------------------

loc_1B459:				; CODE XREF: spectr_1B406+47j
					; spectr_1B406+4Bj
		add	si, ax
		shl	si, 2
		add	si, bp
		pop	cx
		add	di, 8
		dec	cx
		jnz	short loc_1B426
		mov	WORD [word_24516], 2

loc_1B46D:				; CODE XREF: spectr_1B406+1BEj
		mov	ax, [word_24516]
		cmp	[word_24522], ax
		jle	locret_1B5C7
		shl	ax, 1
		mov	[word_2451C], ax
		mov	si, [word_2450C]
		mov	eax, [tabledword_24526+si]
		mov	[multip_244D0],	eax
		mov	eax, [tabledword_24562+si]
		mov	[multip_244CC],	eax
		add	WORD [word_2450C], 4
		mov	DWORD [dword_244C8], 10000h
		mov	DWORD [dword_244D4], 0
		mov	cx, [word_24516]
		shr	cx, 1
		mov	ax, 1

loc_1B4B3:				; CODE XREF: spectr_1B406+1B4j
		push	cx
		push	ax
		shl	ax, 1
		dec	ax
		mov	[word_24518], ax
		mov	ax, [word_24522]
		sub	ax, [word_24518]
		cwd
		idiv	WORD [word_2451C]
		mov	cx, ax
		inc	cx
		mov	ax, 0

loc_1B4CD:				; CODE XREF: spectr_1B406+156j
		push	cx
		push	ax
		imul	WORD [word_2451C]
		add	ax, [word_24518]
		mov	[word_2451E], ax
		add	ax, [word_24516]
		mov	[word_2451A], ax
		mov	si, [word_2451A]
		dec	si
		shl	si, 2
		add	si, [word_2450E]
		mov	di, [word_2451E]
		dec	di
		shl	di, 2
		add	di, [word_2450E]
		mov	ecx, [dword_244C8]
		mov	ebp, [dword_244D4]
		mov	eax, [si]
		imul	ecx
		shrd	eax, edx, 10h
		mov	ebx, eax
		mov	eax, [si+4]
		imul	ebp
		shrd	eax, edx, 10h
		sub	ebx, eax
		mov	eax, [si+4]
		imul	ecx
		shrd	eax, edx, 10h
		mov	ecx, eax
		mov	eax, [si]
		imul	ebp
		shrd	eax, edx, 10h
		add	ecx, eax
		mov	eax, [di]
		sub	eax, ebx
		mov	[si], eax
		mov	eax, [di+4]
		sub	eax, ecx
		mov	[si+4],	eax
		add	[di], ebx
		add	[di+4],	ecx
		pop	ax
		pop	cx
		inc	ax
		dec	cx
		jnz	loc_1B4CD
		mov	ecx, [multip_244CC]
		mov	ebp, [multip_244D0]
		mov	eax, [dword_244C8]
		mov	dword [unk_244C4], eax
		mov	eax, [dword_244C8]
		imul	ecx
		shrd	eax, edx, 10h
		add	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	ebp
		shrd	eax, edx, 10h
		sub	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	ecx
		shrd	eax, edx, 10h
		add	[dword_244D4], eax
		mov	eax, dword	[unk_244C4]
		imul	ebp
		shrd	eax, edx, 10h
		add	[dword_244D4], eax
		pop	ax
		pop	cx
		inc	ax
		dec	cx
		jnz	loc_1B4B3
		mov	ax, [word_2451C]
		mov	[word_24516], ax
		jmp	loc_1B46D
; ---------------------------------------------------------------------------

locret_1B5C7:				; CODE XREF: spectr_1B406+6Ej
		retn


; =============== S U B	R O U T	I N E =======================================


f5_draw_spectr:	; DATA XREF: f5_graphspectr+6o
					; f5_graphspectr+Co
		mov	ax, ds
		mov	es, ax
		mov	di, buffer_1 ; 2800h
		mov	cx, 200h
		mov	ax, 4001h
		call far volume_prep
		lfs	bx, [segfsbx_1DE28]
		mov	si, buffer_1 ; 2800h
		mov	di, byte_24204
		mov	bp, [amount_of_x]

loc_1B5EC:				; CODE XREF: f5_draw_spectr+2A1j
		mov	cx, bp
		xor	dx, dx
		cmp	byte [fs:bx+3Ah], 64
		ja	short loc_1B5FC
		mov	al, [si]
		cbw
		add	dx, ax

loc_1B5FC:				; CODE XREF: f5_draw_spectr+2Dj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+8Ah], 64
		ja	short loc_1B610
		mov	al, [si+200h]
		cbw
		add	dx, ax

loc_1B610:				; CODE XREF: f5_draw_spectr+3Fj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+0DAh], 64
		ja	short loc_1B624
		mov	al, [si+400h]
		cbw
		add	dx, ax

loc_1B624:				; CODE XREF: f5_draw_spectr+53j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+12Ah], 64
		ja	short loc_1B638
		mov	al, [si+600h]
		cbw
		add	dx, ax

loc_1B638:				; CODE XREF: f5_draw_spectr+67j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+17Ah], 64
		ja	short loc_1B64C
		mov	al, [si+800h]
		cbw
		add	dx, ax

loc_1B64C:				; CODE XREF: f5_draw_spectr+7Bj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+1CAh], 64
		ja	short loc_1B660
		mov	al, [si+0A00h]
		cbw
		add	dx, ax

loc_1B660:				; CODE XREF: f5_draw_spectr+8Fj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+21Ah], 64
		ja	short loc_1B674
		mov	al, [si+0C00h]
		cbw
		add	dx, ax

loc_1B674:				; CODE XREF: f5_draw_spectr+A3j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+26Ah], 64
		ja	short loc_1B688
		mov	al, [si+0E00h]
		cbw
		add	dx, ax

loc_1B688:				; CODE XREF: f5_draw_spectr+B7j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+2BAh], 64
		ja	short loc_1B69C
		mov	al, [si+1000h]
		cbw
		add	dx, ax

loc_1B69C:				; CODE XREF: f5_draw_spectr+CBj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+30Ah], 64
		ja	short loc_1B6B0
		mov	al, [si+1200h]
		cbw
		add	dx, ax

loc_1B6B0:				; CODE XREF: f5_draw_spectr+DFj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+35Ah], 64
		ja	short loc_1B6C4
		mov	al, [si+1400h]
		cbw
		add	dx, ax

loc_1B6C4:				; CODE XREF: f5_draw_spectr+F3j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+3AAh], 64
		ja	short loc_1B6D8
		mov	al, [si+1600h]
		cbw
		add	dx, ax

loc_1B6D8:				; CODE XREF: f5_draw_spectr+107j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+3FAh], 64
		ja	short loc_1B6EC
		mov	al, [si+1800h]
		cbw
		add	dx, ax

loc_1B6EC:				; CODE XREF: f5_draw_spectr+11Bj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+44Ah], 64
		ja	short loc_1B700
		mov	al, [si+1A00h]
		cbw
		add	dx, ax

loc_1B700:				; CODE XREF: f5_draw_spectr+12Fj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+49Ah], 64
		ja	short loc_1B714
		mov	al, [si+1C00h]
		cbw
		add	dx, ax

loc_1B714:				; CODE XREF: f5_draw_spectr+143j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+4EAh], 40h ; '@'
		ja	short loc_1B728
		mov	al, [si+1E00h]
		cbw
		add	dx, ax

loc_1B728:				; CODE XREF: f5_draw_spectr+157j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+53Ah], 40h ; '@'
		ja	short loc_1B73C
		mov	al, [si+2000h]
		cbw
		add	dx, ax

loc_1B73C:				; CODE XREF: f5_draw_spectr+16Bj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+58Ah], 40h ; '@'
		ja	short loc_1B750
		mov	al, [si+2200h]
		cbw
		add	dx, ax

loc_1B750:				; CODE XREF: f5_draw_spectr+17Fj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+5DAh], 40h ; '@'
		ja	short loc_1B764
		mov	al, [si+2400h]
		cbw
		add	dx, ax

loc_1B764:				; CODE XREF: f5_draw_spectr+193j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+62Ah], 40h ; '@'
		ja	short loc_1B778
		mov	al, [si+2600h]
		cbw
		add	dx, ax

loc_1B778:				; CODE XREF: f5_draw_spectr+1A7j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+67Ah], 40h ; '@'
		ja	short loc_1B78C
		mov	al, [si+2800h]
		cbw
		add	dx, ax

loc_1B78C:				; CODE XREF: f5_draw_spectr+1BBj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+6CAh], 40h ; '@'
		ja	short loc_1B7A0
		mov	al, [si+2A00h]
		cbw
		add	dx, ax

loc_1B7A0:				; CODE XREF: f5_draw_spectr+1CFj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+71Ah], 40h ; '@'
		ja	short loc_1B7B4
		mov	al, [si+2C00h]
		cbw
		add	dx, ax

loc_1B7B4:				; CODE XREF: f5_draw_spectr+1E3j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+76Ah], 40h ; '@'
		ja	short loc_1B7C8
		mov	al, [si+2E00h]
		cbw
		add	dx, ax

loc_1B7C8:				; CODE XREF: f5_draw_spectr+1F7j
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+7BAh], 40h ; '@'
		ja	short loc_1B7DC
		mov	al, [si+3000h]
		cbw
		add	dx, ax

loc_1B7DC:				; CODE XREF: f5_draw_spectr+20Bj
		dec	cx
		jz	loc_1B85F
		cmp	byte [fs:bx+80Ah], 40h ; '@'
		ja	short loc_1B7F0
		mov	al, [si+3200h]
		cbw
		add	dx, ax

loc_1B7F0:				; CODE XREF: f5_draw_spectr+21Fj
		dec	cx
		jz	short loc_1B85F
		cmp	byte [fs:bx+85Ah], 40h ; '@'
		ja	short loc_1B802
		mov	al, [si+3400h]
		cbw
		add	dx, ax

loc_1B802:				; CODE XREF: f5_draw_spectr+231j
		dec	cx
		jz	short loc_1B85F
		cmp	byte [fs:bx+8AAh], 40h ; '@'
		ja	short loc_1B814
		mov	al, [si+3600h]
		cbw
		add	dx, ax

loc_1B814:				; CODE XREF: f5_draw_spectr+243j
		dec	cx
		jz	short loc_1B85F
		cmp	byte [fs:bx+8FAh], 40h ; '@'
		ja	short loc_1B826
		mov	al, [si+3800h]
		cbw
		add	dx, ax

loc_1B826:				; CODE XREF: f5_draw_spectr+255j
		dec	cx
		jz	short loc_1B85F
		cmp	byte [fs:bx+94Ah], 40h ; '@'
		ja	short loc_1B838
		mov	al, [si+3A00h]
		cbw
		add	dx, ax

loc_1B838:				; CODE XREF: f5_draw_spectr+267j
		dec	cx
		jz	short loc_1B85F
		cmp	byte [fs:bx+99Ah], 40h ; '@'
		ja	short loc_1B84A
		mov	al, [si+3C00h]
		cbw
		add	dx, ax

loc_1B84A:				; CODE XREF: f5_draw_spectr+279j
		dec	cx
		jz	short loc_1B85F
		cmp	byte [fs:bx+9EAh], 40h ; '@'
		ja	short loc_1B85C
		mov	al, [si+3E00h]
		cbw
		add	dx, ax

loc_1B85C:				; CODE XREF: f5_draw_spectr+28Bj
		dec	cx
		jz	short $+2

loc_1B85F:				; CODE XREF: f5_draw_spectr+35j
					; f5_draw_spectr+49j ...
		sar	dx, 1
		mov	[di], dl
		inc	si
		inc	di
		cmp	si, byte_1E0E0
		jb	loc_1B5EC
		mov	si, byte_24204
		mov	di, byte_22EE4
		mov	cx, 200h

loc_1B876:				; CODE XREF: f5_draw_spectr+2C5j
		movsx	eax, byte [si]
		shl	eax, 10h
		mov	[di], eax
		mov	dword [di+4], 0
		inc	si
		add	di, 8
		loop	loc_1B876
		mov	ax, [word_24524]
		mov	[word_24520], ax
		mov	[word_24514], ax
		mov	di, byte_22EE4
		call	spectr_1B406
		mov	si, byte_22EE4
		mov	di, unk_23EE4
		mov	cx, 64h	; 'd'
		call	spectr_1BBC1
		lfs	bx, [segfsbx_1DE28]
		mov	si, buffer_1 ; 2800h
		mov	di, byte_24204
		mov	bp, [amount_of_x]

loc_1B8BC:				; CODE XREF: f5_draw_spectr+571j
		mov	cx, bp
		xor	dx, dx
		cmp	byte [fs:bx+3Ah], 40h ; '@'
		jb	short loc_1B8CC
		mov	al, [si]
		cbw
		add	dx, ax

loc_1B8CC:				; CODE XREF: f5_draw_spectr+2FDj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+8Ah], 40h ; '@'
		jb	short loc_1B8E0
		mov	al, [si+200h]
		cbw
		add	dx, ax

loc_1B8E0:				; CODE XREF: f5_draw_spectr+30Fj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+0DAh], 40h ; '@'
		jb	short loc_1B8F4
		mov	al, [si+400h]
		cbw
		add	dx, ax

loc_1B8F4:				; CODE XREF: f5_draw_spectr+323j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+12Ah], 40h ; '@'
		jb	short loc_1B908
		mov	al, [si+600h]
		cbw
		add	dx, ax

loc_1B908:				; CODE XREF: f5_draw_spectr+337j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+17Ah], 40h ; '@'
		jb	short loc_1B91C
		mov	al, [si+800h]
		cbw
		add	dx, ax

loc_1B91C:				; CODE XREF: f5_draw_spectr+34Bj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+1CAh], 40h ; '@'
		jb	short loc_1B930
		mov	al, [si+0A00h]
		cbw
		add	dx, ax

loc_1B930:				; CODE XREF: f5_draw_spectr+35Fj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+21Ah], 40h ; '@'
		jb	short loc_1B944
		mov	al, [si+0C00h]
		cbw
		add	dx, ax

loc_1B944:				; CODE XREF: f5_draw_spectr+373j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+26Ah], 40h ; '@'
		jb	short loc_1B958
		mov	al, [si+0E00h]
		cbw
		add	dx, ax

loc_1B958:				; CODE XREF: f5_draw_spectr+387j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+2BAh], 40h ; '@'
		jb	short loc_1B96C
		mov	al, [si+1000h]
		cbw
		add	dx, ax

loc_1B96C:				; CODE XREF: f5_draw_spectr+39Bj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+30Ah], 40h ; '@'
		jb	short loc_1B980
		mov	al, [si+1200h]
		cbw
		add	dx, ax

loc_1B980:				; CODE XREF: f5_draw_spectr+3AFj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+35Ah], 40h ; '@'
		jb	short loc_1B994
		mov	al, [si+1400h]
		cbw
		add	dx, ax

loc_1B994:				; CODE XREF: f5_draw_spectr+3C3j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+3AAh], 40h ; '@'
		jb	short loc_1B9A8
		mov	al, [si+1600h]
		cbw
		add	dx, ax

loc_1B9A8:				; CODE XREF: f5_draw_spectr+3D7j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+3FAh], 40h ; '@'
		jb	short loc_1B9BC
		mov	al, [si+1800h]
		cbw
		add	dx, ax

loc_1B9BC:				; CODE XREF: f5_draw_spectr+3EBj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+44Ah], 40h ; '@'
		jb	short loc_1B9D0
		mov	al, [si+1A00h]
		cbw
		add	dx, ax

loc_1B9D0:				; CODE XREF: f5_draw_spectr+3FFj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+49Ah], 40h ; '@'
		jb	short loc_1B9E4
		mov	al, [si+1C00h]
		cbw
		add	dx, ax

loc_1B9E4:				; CODE XREF: f5_draw_spectr+413j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+4EAh], 40h ; '@'
		jb	short loc_1B9F8
		mov	al, [si+1E00h]
		cbw
		add	dx, ax

loc_1B9F8:				; CODE XREF: f5_draw_spectr+427j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+53Ah], 40h ; '@'
		jb	short loc_1BA0C
		mov	al, [si+2000h]
		cbw
		add	dx, ax

loc_1BA0C:				; CODE XREF: f5_draw_spectr+43Bj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+58Ah], 40h ; '@'
		jb	short loc_1BA20
		mov	al, [si+2200h]
		cbw
		add	dx, ax

loc_1BA20:				; CODE XREF: f5_draw_spectr+44Fj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+5DAh], 40h ; '@'
		jb	short loc_1BA34
		mov	al, [si+2400h]
		cbw
		add	dx, ax

loc_1BA34:				; CODE XREF: f5_draw_spectr+463j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+62Ah], 40h ; '@'
		jb	short loc_1BA48
		mov	al, [si+2600h]
		cbw
		add	dx, ax

loc_1BA48:				; CODE XREF: f5_draw_spectr+477j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+67Ah], 40h ; '@'
		jb	short loc_1BA5C
		mov	al, [si+2800h]
		cbw
		add	dx, ax

loc_1BA5C:				; CODE XREF: f5_draw_spectr+48Bj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+6CAh], 40h ; '@'
		jb	short loc_1BA70
		mov	al, [si+2A00h]
		cbw
		add	dx, ax

loc_1BA70:				; CODE XREF: f5_draw_spectr+49Fj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+71Ah], 40h ; '@'
		jb	short loc_1BA84
		mov	al, [si+2C00h]
		cbw
		add	dx, ax

loc_1BA84:				; CODE XREF: f5_draw_spectr+4B3j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+76Ah], 40h ; '@'
		jb	short loc_1BA98
		mov	al, [si+2E00h]
		cbw
		add	dx, ax

loc_1BA98:				; CODE XREF: f5_draw_spectr+4C7j
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+7BAh], 40h ; '@'
		jb	short loc_1BAAC
		mov	al, [si+3000h]
		cbw
		add	dx, ax

loc_1BAAC:				; CODE XREF: f5_draw_spectr+4DBj
		dec	cx
		jz	loc_1BB2F
		cmp	byte [fs:bx+80Ah], 40h ; '@'
		jb	short loc_1BAC0
		mov	al, [si+3200h]
		cbw
		add	dx, ax

loc_1BAC0:				; CODE XREF: f5_draw_spectr+4EFj
		dec	cx
		jz	short loc_1BB2F
		cmp	byte [fs:bx+85Ah], 40h ; '@'
		jb	short loc_1BAD2
		mov	al, [si+3400h]
		cbw
		add	dx, ax

loc_1BAD2:				; CODE XREF: f5_draw_spectr+501j
		dec	cx
		jz	short loc_1BB2F
		cmp	byte [fs:bx+8AAh], 40h ; '@'
		jb	short loc_1BAE4
		mov	al, [si+3600h]
		cbw
		add	dx, ax

loc_1BAE4:				; CODE XREF: f5_draw_spectr+513j
		dec	cx
		jz	short loc_1BB2F
		cmp	byte [fs:bx+8FAh], 40h ; '@'
		jb	short loc_1BAF6
		mov	al, [si+3800h]
		cbw
		add	dx, ax

loc_1BAF6:				; CODE XREF: f5_draw_spectr+525j
		dec	cx
		jz	short loc_1BB2F
		cmp	byte [fs:bx+94Ah], 40h ; '@'
		jb	short loc_1BB08
		mov	al, [si+3A00h]
		cbw
		add	dx, ax

loc_1BB08:				; CODE XREF: f5_draw_spectr+537j
		dec	cx
		jz	short loc_1BB2F
		cmp	byte [fs:bx+99Ah], 40h ; '@'
		jb	short loc_1BB1A
		mov	al, [si+3C00h]
		cbw
		add	dx, ax

loc_1BB1A:				; CODE XREF: f5_draw_spectr+549j
		dec	cx
		jz	short loc_1BB2F
		cmp	byte [fs:bx+9EAh], 40h ; '@'
		jb	short loc_1BB2C
		mov	al, [si+3E00h]
		cbw
		add	dx, ax

loc_1BB2C:				; CODE XREF: f5_draw_spectr+55Bj
		dec	cx
		jz	short $+2

loc_1BB2F:				; CODE XREF: f5_draw_spectr+305j
					; f5_draw_spectr+319j ...
		sar	dx, 1
		mov	[di], dl
		inc	si
		inc	di
		cmp	si, byte_1E0E0
		jb	loc_1B8BC
		mov	si, byte_24204
		mov	di, byte_22EE4
		mov	cx, 200h

loc_1BB46:				; CODE XREF: f5_draw_spectr+595j
		movsx	eax, byte [si]
		shl	eax, 10h
		mov	[di], eax
		mov	dword [di+4], 0
		inc	si
		add	di, 8
		loop	loc_1BB46
		mov	ax, [word_24524]
		mov	[word_24520], ax
		mov	[word_24514], ax
		mov	di, byte_22EE4
		call	spectr_1B406
		mov	si, byte_22EE4
		mov	di, unk_24074
		mov	cx, 64h	; 'd'
		call	spectr_1BBC1
		mov	ax, 0A000h
		mov	es, ax
		mov	bx, unk_23EE4
		mov	bp, 7BC4h
		call	spectr_1BCE9
		mov	bx, byte_23EE5
		mov	bp, 7BD6h
		call	spectr_1BC2D
		mov	bx, unk_24074
		mov	bp, 0F8C4h
		call	spectr_1BCE9
		mov	bx, byte_24075
		mov	bp, 0F8D6h
		call	spectr_1BC2D
		mov	ax, ds
		mov	es, ax
		mov	si, unk_23EE4
		mov	di, byte_23F48
		mov	cx, 19h
		cld
		rep movsd
		mov	si, unk_24074
		mov	di, byte_240D8
		mov	cx, 19h
		rep movsd
		retn


; =============== S U B	R O U T	I N E =======================================


spectr_1BBC1:	; CODE XREF: f5_draw_spectr+2DFp
					; f5_draw_spectr+5AFp ...
		push	cx
		mov	eax, [si]
		imul	eax
		mov	ebx, eax
		mov	ecx, edx
		mov	eax, [si+4]
		imul	eax
		mov	eax, edx
		add	eax, ebx
		adc	edx, ecx
		mov	eax, edx
		mov	cl, [byte_1DE81]
		sar	eax, cl
		mov	ebx, eax
		call	spectr_1C4F8
		or	ah, ah
		jz	short loc_1BBF4
		mov	al, 0FFh

loc_1BBF4:				; CODE XREF: spectr_1BBC1+2Fj
		cmp	BYTE [byte_1DE82], 0
		jz	short loc_1BC0C
		mov	ah, [di+64h]
		sub	ah, [byte_1DE82]
		jnb	short loc_1BC06
		xor	ah, ah

loc_1BC06:				; CODE XREF: spectr_1BBC1+41j
		cmp	ah, al
		jb	short loc_1BC0C
		mov	al, ah

loc_1BC0C:				; CODE XREF: spectr_1BBC1+38j
					; spectr_1BBC1+47j
		mov	[di], al
		cmp	byte [di+12Ch], 0
		jz	short loc_1BC1B
		cmp	al, [di+0C8h]
		jb	short loc_1BC24

loc_1BC1B:				; CODE XREF: spectr_1BBC1+52j
		mov	[di+0C8h], al
		mov	byte [di+12Ch], 14h

loc_1BC24:				; CODE XREF: spectr_1BBC1+58j
		inc	di
		add	si, 8
		pop	cx
		dec	cx
		jnz	short spectr_1BBC1
		retn


; =============== S U B	R O U T	I N E =======================================


spectr_1BC2D:	; CODE XREF: f5_draw_spectr+5C6p
					; f5_draw_spectr+5D8p
		mov	cx, 99

loc_1BC30:				; CODE XREF: spectr_1BC2D+B7j
		mov	al, [bx]
		cmp	al, 90
		jb	short loc_1BC38
		mov	al, 90

loc_1BC38:				; CODE XREF: spectr_1BC2D+7j
		mov	ah, [bx+64h]
		cmp	ah, 90
		jb	short loc_1BC42
		mov	ah, 90

loc_1BC42:				; CODE XREF: spectr_1BC2D+11j
		cmp	al, ah
		jz	short loc_1BC92
		jb	short loc_1BC70
		movzx	dx, ah
		shl	dx, 6
		mov	di, dx
		shl	dx, 2
		add	di, dx
		neg	di
		add	di, bp
		mov	dl, al
		sub	dl, ah
		mov	al, ah

loc_1BC5F:				; CODE XREF: spectr_1BC2D+3Fj
		mov	[es:di], ax
		inc	al
		inc	ah
		sub	di, 140h
		dec	dl
		jnz	short loc_1BC5F
		jmp	short loc_1BC92
; ---------------------------------------------------------------------------

loc_1BC70:				; CODE XREF: spectr_1BC2D+19j
		movzx	dx, al
		shl	dx, 6
		mov	di, dx
		shl	dx, 2
		add	di, dx
		neg	di
		add	di, bp
		mov	dl, ah
		sub	dl, al
		xor	ax, ax

loc_1BC87:				; CODE XREF: spectr_1BC2D+63j
		mov	[es:di], ax
		sub	di, 140h
		dec	dl
		jnz	short loc_1BC87

loc_1BC92:				; CODE XREF: spectr_1BC2D+17j
					; spectr_1BC2D+41j
		cmp	byte [bx+12Ch], 0
		jz	short loc_1BCDF
		dec	byte [bx+12Ch]
		jnz	short loc_1BCC0
		movzx	dx, byte [bx+0C8h]
		cmp	dl, 5Ah	; 'Z'
		jb	short loc_1BCAB
		mov	dl, 5Ah	; 'Z'

loc_1BCAB:				; CODE XREF: spectr_1BC2D+7Aj
		shl	dx, 6
		mov	di, dx
		shl	dx, 2
		add	di, dx
		neg	di

loc_1BCB7:
		add	di, bp
		mov	word [es:di], 0
		jmp	short loc_1BCDF
; ---------------------------------------------------------------------------

loc_1BCC0:				; CODE XREF: spectr_1BC2D+70j
		movzx	dx, byte [bx+0C8h]
		cmp	dl, 5Ah	; 'Z'
		jb	short loc_1BCCC
		mov	dl, 5Ah	; 'Z'

loc_1BCCC:				; CODE XREF: spectr_1BC2D+9Bj
		shl	dx, 6
		mov	di, dx
		shl	dx, 2
		add	di, dx
		neg	di
		add	di, bp
		mov	word [es:di], 0FEFEh

loc_1BCDF:				; CODE XREF: spectr_1BC2D+6Aj
					; spectr_1BC2D+91j
		inc	bx
		add	bp, 3
		dec	cx
		jnz	loc_1BC30
		retn


; =============== S U B	R O U T	I N E =======================================


spectr_1BCE9:	; CODE XREF: f5_draw_spectr+5BDp
					; f5_draw_spectr+5CFp
		mov	al, [bx]
		cmp	al, 90
		jb	short loc_1BCF1
		mov	al, 90

loc_1BCF1:				; CODE XREF: spectr_1BCE9+4j
		mov	ah, [bx+64h]
		cmp	ah, 90
		jb	short loc_1BCFB
		mov	ah, 90

loc_1BCFB:				; CODE XREF: spectr_1BCE9+Ej
		cmp	al, ah
		jz	short locret_1BD67
		jb	short loc_1BD3E
		movzx	dx, ah
		shl	dx, 6
		mov	di, dx
		shl	dx, 2
		add	di, dx
		neg	di
		add	di, bp
		mov	dl, al
		sub	dl, ah
		shr	ah, 1
		mov	eax, 0FCFCFCFCh
		jnb	short loc_1BD26
		or	eax, 1010101h

loc_1BD26:				; CODE XREF: spectr_1BCE9+35j
					; spectr_1BCE9+52j
		mov	[es:di], eax
		mov	[es:di+4], eax
		sub	di, 140h
		xor	eax, 1010101h
		dec	dl
		jnz	short loc_1BD26
		retn
; ---------------------------------------------------------------------------

loc_1BD3E:				; CODE XREF: spectr_1BCE9+16j
		movzx	dx, al
		shl	dx, 6
		mov	di, dx
		shl	dx, 2
		add	di, dx
		neg	di
		add	di, bp
		mov	dl, ah
		sub	dl, al
		xor	eax, eax

loc_1BD56:				; CODE XREF: spectr_1BCE9+7Cj
		mov	[es:di], eax
		mov	[es:di+4], eax
		sub	di, 140h
		dec	dl
		jnz	short loc_1BD56

locret_1BD67:				; CODE XREF: spectr_1BCE9+14j
		retn

; ---------------------------------------------------------------------------

f6_draw:				; DATA XREF: f6_undoc+6o
		call	txt_draw_bottom
		lfs	bx, [segfsbx_1DE28]
		les	di, [videomempointer]
		add	di, 3C4h
		mov	cx, [amount_of_x]
		cmp	cx, [word_1DE6E]

loc_1BD80:
		jbe	short loc_1BD86
		mov	cx, [word_1DE6E]

loc_1BD86:				; CODE XREF: seg001:loc_1BD80j
		xor	ax, ax

loc_1BD88:				; CODE XREF: seg001:2DDCj
		push	ax
		push	cx
		push	di
		mov	dl, al
		add	al, 31h	; '1'
		cmp	al, 39h	; '9'
		jbe	short loc_1BD95
		add	al, 7

loc_1BD95:				; CODE XREF: seg001:2D41j
		mov	ah, 1Eh
		cmp	dl, [byte_1DE84]
		jz	short loc_1BD9F
		mov	ah, 7Eh	; '~'

loc_1BD9F:				; CODE XREF: seg001:2D4Bj
		mov	[es:di+2], ax
		mov	al, 20h	; ' '
		mov	[es:di], ax
		mov	[es:di+4], ax
		add	di, 6
		mov	si, buffer_1 ; 2800h
		mov	eax, 0C4C4C4C4h
		mov	word [si], 2020h
		mov	[si+2],	eax
		mov	[si+6],	eax
		mov	[si+0Ah], eax
		mov	[si+0Eh], eax
		mov	word [si+12h], 20C4h
		lea	bp, [si+14h]
		mov	al, [fs:bx+3Ah]
		mov	dl, al
		shr	al, 3
		and	ax, 1Fh
		add	si, 2
		add	si, ax
		mov	al, 4Dh	; 'M'
		cmp	dl, 40h	; '@'
		jz	short loc_1BDF2
		mov	al, 4Ch	; 'L'
		jb	short loc_1BDF2
		mov	al, 52h	; 'R'

loc_1BDF2:				; CODE XREF: seg001:2D9Aj seg001:2D9Ej
		mov	[si], al
		mov	si, bp
		mov	dword [si],	20202020h
		cld
		mov	al, [fs:bx+3Ah]
		sub	al, 40h	; '@'
		js	short loc_1BE07
		inc	si

loc_1BE07:				; CODE XREF: seg001:2DB4j
		cmp	al, 0F7h ; '˜'
		jl	short loc_1BE10
		cmp	al, 9
		jg	short loc_1BE10
		inc	si

loc_1BE10:				; CODE XREF: seg001:2DB9j seg001:2DBDj
		push	bx
		call	my_i8toa10
		pop	bx
		mov	byte [si], 0
		mov	si, buffer_1 ; 2800h
		mov	ah, 7Eh	; '~'
		call	put_message
		pop	di
		pop	cx
		pop	ax
		add	di, 0A0h ; '†'
		add	bx, 50h	; 'P'
		inc	ax
		dec	cx
		jnz	loc_1BD88
		retn
; ---------------------------------------------------------------------------
		push	ax
		shr	al, 4
		call	hex_1BE39
		pop	ax

; =============== S U B	R O U T	I N E =======================================


hex_1BE39:		; CODE XREF: seg001:2DE5p
		and	al, 0Fh
		or	al, 30h
		cmp	al, 39h	; '9'
		jbe	short loc_1BE43
		add	al, 7

loc_1BE43:				; CODE XREF: hex_1BE39+6j
		mov	[es:di], ax
		add	di, 2
		retn


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame




; =============== S U B	R O U T	I N E =======================================


; int __usercall message_1BE77<eax>(char *msg<esi>)
message_1BE77:	; CODE XREF: start+2FDp start+420p ...
		push	ax
		push	si
		mov	ch, al
		sub	ch, 2
		mov	dh, al
		add	dh, 2
		mov	ah, 0FFh

loc_1BE85:				; CODE XREF: message_1BE77+15j
		mov	al, [si]
		inc	ah
		inc	si
		or	al, al
		jnz	short loc_1BE85
		mov	cl, 4Eh	; 'N'
		sub	cl, ah
		shr	ah, 1
		mov	dl, 2Ah	; '*'
		add	dl, ah
		mov	al, ch
		inc	al
		mov	ah, 0A0h ; '†'
		mul	ah
		movzx	di, cl
		and	di, 0FFFEh
		add	ax, di
		add	ax, 0A4h ; '§'
		push	ax
		shr	cl, 1
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		pop	ax
		pop	si		; str
		les	di, [videomempointer]
		add	di, ax
		pop	ax
		call	text_1BF69
		retn


; =============== S U B	R O U T	I N E =======================================


draw_frame:		; CODE XREF: start+1FEp start+278p ...
		push	es
		les	bp, [videomempointer]
		movzx	di, cl
		movzx	si, ch
		imul	si, 80
		add	di, si
		shl	di, 1
		add	di, bp
		movzx	bp, dl
		inc	bp
		movzx	si, cl
		sub	bp, si
		jbe	short loc_1BF57
		sub	bp, 2
		jb	short loc_1BF57
		mov	dl, dh
		inc	dl
		sub	dl, ch
		jbe	short loc_1BF57
		xor	dh, dh
		sub	dx, 2
		jb	short loc_1BF57
		cmp	al, 6
		jnb	short loc_1BF57
		movzx	si, al
		imul	si, 6
		add	si, frameborder ; "	€€€€€€…ª»ºÕ∫⁄ø¿Ÿƒ≥÷∑”Ωƒ∫’∏‘æÕ≥"
		mov	al, [si]
		cld
		stosw
		mov	cx, bp
		jcxz loc_1BF11
		mov	al, [si+4]
		rep stosw

loc_1BF11:				; CODE XREF: draw_frame+47j
		xchg	bl, ah
		mov	al, [si+1]
		stosw
		or	dx, dx
		jz	short loc_1BF3A

loc_1BF1B:				; CODE XREF: draw_frame+75j
		xchg	bl, ah
		add	di, 156
		sub	di, bp
		sub	di, bp
		mov	al, [si+5]
		stosw
		mov	cx, bp
		jcxz loc_1BF31
		mov	al, ' '
		rep stosw

loc_1BF31:				; CODE XREF: draw_frame+68j
		xchg	bl, ah
		mov	al, [si+5]
		stosw
		dec	dx
		jnz	short loc_1BF1B

loc_1BF3A:				; CODE XREF: draw_frame+56j
		xchg	bl, ah
		add	di, 156
		sub	di, bp
		sub	di, bp
		mov	al, [si+2]
		stosw
		xchg	bl, ah
		mov	cx, bp
		jcxz loc_1BF53
		mov	al, [si+4]
		rep stosw

loc_1BF53:				; CODE XREF: draw_frame+89j
		mov	al, [si+3]
		stosw

loc_1BF57:				; CODE XREF: draw_frame+1Dj
					; draw_frame+22j ...
		pop	es
		retn


; =============== S U B	R O U T	I N E =======================================


; void __usercall write_scr(char *str<esi>)
write_scr:		; CODE XREF: start+20Bp start+72Ap ...
		mov	bp, di
		add	di, [si]
		add	si, 2
		jmp	short n2_setcolor

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR text_1BF69

n1_movepos:				; CODE XREF: text_1BF69+9j
		mov	di, [si]
		add	di, bp
		add	si, 2
; END OF FUNCTION CHUNK	FOR text_1BF69

; =============== S U B	R O U T	I N E =======================================


; void __usercall text_1BF69(char *str<esi>)
text_1BF69:		; CODE XREF: filelist_198B8+102p
					; filelist_198B8+112p ...

; FUNCTION CHUNK AT 2F12 SIZE 00000007 BYTES

		mov	al, [si]
		inc	si		; str
		or	al, al
		jz	short locret_1BF85
		cmp	al, 1
		jz	short n1_movepos
		cmp	al, 2
		jz	short n2_setcolor
		mov	[es:di], ax
		add	di, 2
		jmp	short text_1BF69
; ---------------------------------------------------------------------------

n2_setcolor:				; CODE XREF: write_scr+7j
					; text_1BF69+Dj
		lodsb
		mov	ah, al
		jmp	short text_1BF69
; ---------------------------------------------------------------------------

locret_1BF85:				; CODE XREF: text_1BF69+5j
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR put_message

loc_1BF86:				; CODE XREF: put_message+4j
		stosw
; END OF FUNCTION CHUNK	FOR put_message

; =============== S U B	R O U T	I N E =======================================


; void __usercall put_message(char color<ah>, char *str<esi>, void *videoptr<edi>)
put_message:	; CODE XREF: start+2A8p start+2EDp ...

; FUNCTION CHUNK AT 2F36 SIZE 00000001 BYTES

		cld
		lodsb
		or	al, al
		jnz	short loc_1BF86
		retn


; =============== S U B	R O U T	I N E =======================================


; void __usercall put_message2(char *str<esi>, void *buf<edi>)
put_message2:	; CODE XREF: put_message2+6j
		stosw
		cld
		fs	lodsb
		or	al, al
		jnz	short put_message2
		retn


; =============== S U B	R O U T	I N E =======================================


loadcfg:		; CODE XREF: start:loc_190D3p
		mov	dx, sIplay_cfg ;	"C:\\IPLAY.CFG"
		mov	ax, 3D00h
		int	21h		; DOS -	2+ - OPEN DISK FILE WITH HANDLE
					; DS:DX	-> ASCIZ filename
					; AL = access mode
					; 0 - read
		jb	short loc_1BFE3
		mov	bx, ax
		mov	dx, cfg_buffer
		mov	cx, 4
		mov	ah, 3Fh	; '?'
		push	bx
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	bx
		jb	short loc_1BFC9
		mov	eax, [dword_1DCEC]
		cmp	eax, dword	[cfg_buffer]
		stc
		jnz	short loc_1BFC9
		mov	dx, snd_card_type
		mov	cx, 0Ch
		mov	ah, 3Fh	; '?'
		push	bx
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	bx

loc_1BFC9:				; CODE XREF: loadcfg+18j loadcfg+24j
		pushf
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle
		popf
		jb	short loc_1BFE3
		mov	si, snd_card_type
		mov	cx, 0Ch
		xor	al, al

loc_1BFD9:				; CODE XREF: loadcfg+45j
		add	al, [si]
		inc	si
		loop	loc_1BFD9
		or	al, al
		jnz	short loc_1BFE3
		retn
; ---------------------------------------------------------------------------

loc_1BFE3:				; CODE XREF: loadcfg+8j loadcfg+38j ...
		mov	ax, cs
		mov	ds, ax
		mov	dx, aConfigFileNotF ; "Config file not found. Run ISETUP	first"...
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	ax, 4C01h
		int	21h		; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)

; ---------------------------------------------------------------------------
aConfigFileNotF	db 'Config file not found. Run ISETUP first',0Dh,0Ah,'$'
					; DATA XREF: loadcfg+50o
		db 0Dh,0Ah,'$'

; =============== S U B	R O U T	I N E =======================================


; char *__usercall getexename<esi>()
getexename:		; CODE XREF: init_vga_waves+2Fp
		mov	es, [esseg_atstart]
		mov	es, word [es:2Ch]
		xor	di, di
		xor	al, al
		cld
		mov	cx, 8000h

loc_1C031:				; CODE XREF: getexename+18j
		repne scasb
		jnz	short loc_1C050
		cmp	[es:di], al
		jnz	short loc_1C031
		mov	cx, [es:di+1]
		jcxz loc_1C050
		add	di, 3

loc_1C043:				; CODE XREF: getexename+2Cj
		mov	al, [es:di]
		mov	[si], al
		inc	di
		inc	si
		or	al, al
		jnz	short loc_1C043
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C050:				; CODE XREF: getexename+13j
					; getexename+1Ej
		stc
		retn


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


set_egasequencer:	; CODE XREF: init_vga_waves+91p
					; init_f5_spectr+13p
		mov	dx, 3C4h
		mov	al, 1
		out	dx, al		; EGA: sequencer address reg
					; clocking mode. Data bits:
					; 0: 1=8 dots/char; 0=9	dots/char
					; 1: CRT bandwidth: 1=low; 0=high
					; 2: 1=shift every char; 0=every 2nd char
					; 3: dot clock:	1=halved
		inc	dl
		in	al, dx		; EGA port: sequencer data register
		or	al, 100000b	; 9 dots/char
					; high bandwidth
					; shift	every 2	char
					; dot clock
					; .
					; dont know
		out	dx, al		; EGA port: sequencer data register
		retn


; =============== S U B	R O U T	I N E =======================================


graph_1C070:	; CODE XREF: init_vga_waves+12Cp
					; init_f5_spectr+91p
		mov	dx, 3C4h
		mov	al, 1
		out	dx, al		; EGA: sequencer address reg
					; clocking mode. Data bits:
					; 0: 1=8 dots/char; 0=9	dots/char
					; 1: CRT bandwidth: 1=low; 0=high
					; 2: 1=shift every char; 0=every 2nd char
					; 3: dot clock:	1=halved
		inc	dl
		in	al, dx		; EGA port: sequencer data register
		and	al, 0DFh
		out	dx, al		; EGA port: sequencer data register
		retn


; =============== S U B	R O U T	I N E =======================================


int9_keyb:		; DATA XREF: start+133o
		cmp	BYTE [cs:byte_1C1B8], 1
		jz	loc_1C11F
		push	ax
		in	al, 60h		; 8042 keyboard	controller data	register
		cmp	al, 0E0h ; '‡'
		jz	l_escaped_scancode
		cmp	al, 0E1h ; '·'
		jz	l_escaped_scancode
		mov	ah, [cs:prev_scan_code]
		or	ah, ah
		jz	short loc_1C0A5
		mov	BYTE [cs:prev_scan_code], 0

loc_1C0A5:				; CODE XREF: int9_keyb+20j
		cmp	al, 36h	; '6'
		jz	short l_rshift
		cmp	al, 0B6h ; '∂'
		jz	short l_rshiftup
		cmp	al, 2Ah	; '*'
		jz	short l_lshift
		cmp	al, 0AAh ; '™'
		jz	short l_lshiftup
		cmp	al, 1Dh
		jz	short l_ctrl
		cmp	al, 9Dh	; 'ù'
		jz	short l_lctrlup
		cmp	al, 38h	; '8'
		jz	short l_alt
		cmp	al, 0B8h ; '∏'
		jz	short l_altup
		mov	[cs:key_code], ax

loc_1C0C9:				; CODE XREF: int9_keyb+62j
					; int9_keyb+6Aj ...
		in	al, 61h		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÕÀÕ OR	03H=spkr ON
					; 1: Tmr 2 data	Õº  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		or	al, 80h
		out	61h, al		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÕÀÕ OR	03H=spkr ON
					; 1: Tmr 2 data	Õº  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		and	al, 7Fh
		out	61h, al		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÕÀÕ OR	03H=spkr ON
					; 1: Tmr 2 data	Õº  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ax
		iret
; ---------------------------------------------------------------------------

l_rshift:				; CODE XREF: int9_keyb+2Aj
		or	WORD [cs:keyb_switches], 1
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_rshiftup:				; CODE XREF: int9_keyb+2Ej
		and	WORD [cs:keyb_switches], ~	1
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_lshift:				; CODE XREF: int9_keyb+32j
		or	WORD [cs:keyb_switches], 10b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_lshiftup:				; CODE XREF: int9_keyb+36j
		and	WORD [cs:keyb_switches], ~	10b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_ctrl:					; CODE XREF: int9_keyb+3Aj
		or	WORD [cs:keyb_switches], 100b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_lctrlup:				; CODE XREF: int9_keyb+3Ej
		and	WORD [cs:keyb_switches], ~	100b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_alt:					; CODE XREF: int9_keyb+42j
		or	WORD [cs:keyb_switches], 1000b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_altup:				; CODE XREF: int9_keyb+46j
		and	WORD [cs:keyb_switches], ~	1000b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_escaped_scancode:			; CODE XREF: int9_keyb+Fj
					; int9_keyb+15j
		mov	[cs:prev_scan_code], al
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

loc_1C11F:				; CODE XREF: int9_keyb+6j
		jmp	FAR [cs:oint9_1C1A4]


; =============== S U B	R O U T	I N E =======================================


get_keybsw:
		push	es
		xor	ax, ax
		mov	es, ax
		mov	ax, [es:17h]
		mov	[cs:keyb_switches], ax
		pop	es
		retn


; =============== S U B	R O U T	I N E =======================================


set_keybsw:
		push	es
		xor	ax, ax
		mov	es, ax
		mov	ax, [cs:keyb_switches]
		mov	[es:17h], ax
		pop	es
		retn

; ---------------------------------------------------------------------------
; ---------------------------------------------------------------------------
key_code	dw 0			; DATA XREF: start:loc_193FFr
					; start+37Aw ...
keyb_switches	dw 0			; DATA XREF: start+5D8r
					; keyb_19EFD+1DEr ...
prev_scan_code	db 0			; DATA XREF: int9_keyb+19r
					; int9_keyb+22w ...

; =============== S U B	R O U T	I N E =======================================


int24:		; DATA XREF: start+13Bo
		mov	al, 3
		test	ah, 8
		jnz	short locret_1C159
		mov	al, 0
		test	ah, 20h
		jnz	short locret_1C159
		mov	al, 1

locret_1C159:				; CODE XREF: int24+5j int24+Cj
		iret


; =============== S U B	R O U T	I N E =======================================


int2f_checkmyself:	; DATA XREF: start+143o
		pushf
		cmp	ax, 60FFh
		jz	short lyesitsme	; DS

loc_1C160:				; CODE XREF: int2f_checkmyself+10j
					; int2f_checkmyself+16j
		popf
		jmp	FAR [cs:oint2f_1C1B4]
; ---------------------------------------------------------------------------

lyesitsme:				; CODE XREF: int2f_checkmyself+4j
		cmp	bx, 5344h	; DS
		jnz	short loc_1C160
		cmp	cx, 4D50h	; PM
		jnz	short loc_1C160
		popf
		cmp	dl, 1
		jz	short loc_1C17C
		mov	ax, 4F4Bh	; KO
		iret
; ---------------------------------------------------------------------------

loc_1C17C:				; CODE XREF: int2f_checkmyself+1Cj
		push	ax
		push	ds
		mov	ax, dseg
		mov	ds, ax
		mov	BYTE [byte_1DE7C], 1
		pop	ds
		pop	ax
		iret


; =============== S U B	R O U T	I N E =======================================


int1a_timer:	; DATA XREF: dosexec+47o
		pushf
		or	ah, ah
		jnz	short loc_1C19C
		pushad
		push	ds
		push	es
		call	rereadrtc_settmr
		pop	es
		pop	ds
		popad

loc_1C19C:				; CODE XREF: int1a_timer+3j
		popf
		jmp	FAR [cs:int1Avect]

; ---------------------------------------------------------------------------
; ---------------------------------------------------------------------------
oint9_1C1A4	dd 0			; DATA XREF: start+106w start+1E0r ...
int1Avect	dd 0			; DATA XREF: int1a_timer+12r
					; dosexec+38w ...
oint24_1C1AC	dd 0			; DATA XREF: start+115w start+1D4r ...
		times	4	db 0
oint2f_1C1B4	dd 0			; DATA XREF: start+124w start+1C8r ...
byte_1C1B8	db 0			; DATA XREF: int9_keybr dosexec+58w ...

; =============== S U B	R O U T	I N E =======================================


dosexec:		; CODE XREF: start+747p
					; keyb_19EFD+338p
		mov	ax, 3
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		call	txt_enableblink
		mov	cx, 0
		mov	dx, 94Fh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		call	txt_draw_top_title
		mov	si, word_1D26D ;	str
		les	di, [videomempointer]
		call	write_scr
		mov	dx, 0A00h
		xor	bh, bh
		mov	ah, 2
		int	10h		; - VIDEO - SET	CURSOR POSITION
					; DH,DL	= row, column (0,0 = upper left)
					; BH = page number
		test	BYTE [byte_1DE78], 2
		jz	short loc_1C209
		mov	ax, 351Ah
		int	21h		; DOS -	2+ - GET INTERRUPT VECTOR
					; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	word [cs:int1Avect], bx
		mov	word [cs:int1Avect+2], es
		push	ds
		mov	ax, cs
		mov	ds, ax
		mov	dx, int1a_timer
		mov	ax, 251Ah
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds

loc_1C209:				; CODE XREF: dosexec+31j
		mov	si, byte_1DD3F ;	str
		call	dosgetcurdir
		mov	al, 1
		mov	[cs:byte_1C1B8], al
		call far sub_12D35
		mov	es, [esseg_atstart]
		mov	ax, [es:2Ch]
		mov	[word_24445], ax
		call	get_comspec
		jb	short loc_1C23E
		mov	dx, di
		push	ds
		mov	ax, ds
		mov	es, ax
		mov	bx, word_24445
		mov	ds, [word_24445]
		mov	ax, 4B00h
		int	21h		; DOS -	2+ - LOAD OR EXECUTE (EXEC)
					; DS:DX	-> ASCIZ filename
					; ES:BX	-> parameter block
					; AL = subfunc:	load & execute program
		pop	ds

loc_1C23E:				; CODE XREF: dosexec+6Fj
		mov	al, 0
		mov	[cs:byte_1C1B8], al
		call far sub_12D35
		test	BYTE [byte_1DE78], 2
		jz	short loc_1C25C
		push	ds
		lds	dx, [cs:int1Avect]
		mov	ax, 251Ah
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds

loc_1C25C:				; CODE XREF: dosexec+95j
		mov	si, byte_1DD3F ;	str
		call	doschdir
		mov	BYTE [byte_1DE70], 0FFh
		retn


; =============== S U B	R O U T	I N E =======================================


get_comspec:	; CODE XREF: dosexec+6Cp
		mov	es, [esseg_atstart]
		mov	es, word [es:2Ch]
		xor	di, di

loc_1C273:				; CODE XREF: get_comspec+2Fj
		cmp	byte [es:di], 0
		stc
		jz	short locret_1C29D
		cmp	dword [es:di], 534D4F43h ; COMSPEC=
		jnz	short loc_1C28F
		cmp	dword [es:di+4], 3D434550h
		jz	short loc_1C299

loc_1C28F:				; CODE XREF: get_comspec+1Aj
					; get_comspec+2Cj
		inc	di
		cmp	byte [es:di], 0
		jnz	short loc_1C28F
		inc	di
		jmp	short loc_1C273
; ---------------------------------------------------------------------------

loc_1C299:				; CODE XREF: get_comspec+25j
		add	di, 8
		clc

locret_1C29D:				; CODE XREF: get_comspec+10j
		retn


; =============== S U B	R O U T	I N E =======================================


find_mods:		; CODE XREF: start+1A1p
					; modules_search+65p ...
		mov	ax, ds
		mov	es, ax
		mov	di, buffer_1DB6C
		mov	si, di
		mov	cx, 120
		xor	al, al
		cld
		repne scasb
		jnz	short loc_1C321
		dec	di
		mov	[word_1DE4A], di

loc_1C2B6:				; CODE XREF: find_mods+2Aj
		mov	al, [di-1]
		or	al, al
		jz	short loc_1C2CA
		cmp	al, '\'
		jz	short loc_1C2CA
		cmp	al, ':'
		jz	short loc_1C2CA
		dec	di
		cmp	si, di
		jb	short loc_1C2B6

loc_1C2CA:				; CODE XREF: find_mods+1Dj
					; find_mods+21j ...
		sub	di, si
		mov	[word_1DE4C], di
		mov	dx, buffer_1DBEC
		mov	ah, 1Ah
		int	21h		; DOS -	SET DISK TRANSFER AREA ADDRESS
					; DS:DX	-> disk	transfer buffer
		mov	dx, buffer_1DB6C
		mov	cx, [word_1DE4E]
		mov	ah, 4Eh
		int	21h		; DOS -	2+ - FIND FIRST	ASCIZ (FINDFIRST)
					; CX = search attributes
					; DS:DX	-> ASCIZ filespec
					; (drive, path,	and wildcards allowed)
		jnb	short loc_1C309
		mov	si, a_mod_nst_669_s ; ".MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FA"...

loc_1C2E7:				; CODE XREF: find_mods+69j
		cmp	byte [si], 0
		jz	short loc_1C321
		mov	di, [word_1DE4A]
		mov	eax, [si]
		mov	[di], eax
		mov	byte [di+4], 0
		add	si, 4
		mov	dx, buffer_1DB6C
		mov	cx, 2
		mov	ah, 4Eh
		int	21h		; DOS -	2+ - FIND FIRST	ASCIZ (FINDFIRST)
					; CX = search attributes
					; DS:DX	-> ASCIZ filespec
					; (drive, path,	and wildcards allowed)
		jb	short loc_1C2E7

loc_1C309:				; CODE XREF: find_mods+44j
					; dosfindnext+Bj
		mov	ax, ds
		mov	es, ax
		mov	si, byte_1DC0A
		mov	di, buffer_1DB6C
		add	di, [word_1DE4C]
		cld
		mov	cx, 3
		rep movsd
		movsb
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C321:				; CODE XREF: find_mods+11j
					; find_mods+4Cj
		mov	BYTE [byte_1DE7E], 2
		mov	word [messagepointer], aModuleNotFound ; "Module not	found.\r\n$"
		mov	word [messagepointer+2], ds
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


dosfindnext:	; CODE XREF: modules_search+CBp
					; modules_search+247p ...
		mov	dx, buffer_1DBEC
		mov	ah, 1Ah
		int	21h		; DOS -	SET DISK TRANSFER AREA ADDRESS
					; DS:DX	-> disk	transfer buffer
		mov	ah, 4Fh
		int	21h		; DOS -	2+ - FIND NEXT ASCIZ (FINDNEXT)
					; [DTA]	= data block from
					; last AH = 4Eh/4Fh call
		jnb	short loc_1C309
		retn


; =============== S U B	R O U T	I N E =======================================


video_prp_mtr_positn: ; CODE XREF: read_module+C5p
					; init_vga_waves+14Cp ...
		pushf
		cli
		mov	BYTE [byte_1DE79], 0
		mov	BYTE [byte_1DE7A], 0
		lfs	bx, [segfsbx_1DE28]
		mov	cx, [amount_of_x]

loc_1C355:				; CODE XREF: video_prp_mtr_positn+2Dj
		mov	al, [fs:bx+3Ah]
		cmp	al, 40h	; '@'
		jb	short loc_1C365
		inc	BYTE [byte_1DE7A]
		cmp	al, 40h	; '@'
		ja	short loc_1C369

loc_1C365:				; CODE XREF: video_prp_mtr_positn+1Bj
		inc	BYTE [byte_1DE79]

loc_1C369:				; CODE XREF: video_prp_mtr_positn+23j
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_1C355
		movzx	ecx, BYTE [byte_1DE79]
		cmp	cl, [byte_1DE7A]
		ja	short loc_1C37F
		mov	cl, [byte_1DE7A]

loc_1C37F:				; CODE XREF: video_prp_mtr_positn+39j
		mov	al, 3
		cmp	cl, 2
		jbe	short loc_1C396
		mov	al, 2
		cmp	cl, 4
		jbe	short loc_1C396
		mov	al, 1
		cmp	cl, 8
		jbe	short loc_1C396
		mov	al, 0

loc_1C396:				; CODE XREF: video_prp_mtr_positn+44j
					; video_prp_mtr_positn+4Bj ...
		add	al, 8
		mov	[byte_1DE81], al
		xor	edx, edx
		mov	eax, 18350080
		jcxz loc_1C3A9
		div	ecx

loc_1C3A9:				; CODE XREF: video_prp_mtr_positn+64j
		mov	ebp, eax
		mov	si, x_storage
		mov	cx, [amount_of_x]
		lfs	bx, [segfsbx_1DE28]
		mov	edi, ebp
		shr	edi, 1
		mov	edx, edi

loc_1C3C1:				; CODE XREF: video_prp_mtr_positn+B5j
		cmp	byte [fs:bx+3Ah], 40h ; '@'
		jz	short loc_1C3EE
		ja	short loc_1C3DC
		mov	eax, edi
		shr	eax, 16
		imul	ax, 80
		add	ax, 1
		add	edi, ebp
		jmp	short loc_1C3EC
; ---------------------------------------------------------------------------

loc_1C3DC:				; CODE XREF: video_prp_mtr_positn+88j
		mov	eax, edx
		shr	eax, 16
		imul	ax, 80
		add	ax, 42
		add	edx, ebp

loc_1C3EC:				; CODE XREF: video_prp_mtr_positn+9Aj
		mov	[si], ax

loc_1C3EE:				; CODE XREF: video_prp_mtr_positn+86j
		add	si, 2
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_1C3C1
		mov	si, x_storage
		mov	cx, [amount_of_x]
		lfs	bx, [segfsbx_1DE28]
		cmp	edi, edx
		ja	short loc_1C40B
		mov	edi, edx

loc_1C40B:				; CODE XREF: video_prp_mtr_positn+C6j
					; video_prp_mtr_positn+EBj
		cmp	byte [fs:bx+3Ah], 40h ; '@'
		jnz	short loc_1C424
		mov	eax, edi
		shr	eax, 16
		imul	ax, 80
		add	ax, 21
		add	edi, ebp
		mov	[si], ax

loc_1C424:				; CODE XREF: video_prp_mtr_positn+D0j
		add	si, 2
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_1C40B
		popf
		retn


; =============== S U B	R O U T	I N E =======================================


callsubx:		; CODE XREF: start:loc_19050p
					; start+1A6p ...
		mov	al, [snd_card_type]
		mov	dx, [snd_base_port_0]
		mov	cl, [irq_number_1]
		mov	ch, [dma_channel_1]
		mov	ah, [freq_1DCF6]
		movzx	di, BYTE [byte_1DCFB]
		mov	si, [configword]
		mov	bl, [byte_1DCF7]
		mov	bh, [byte_1DCF8]
		call far sub_12DA8
		mov	BYTE [byte_1DE7E], 1
		mov	word [messagepointer], dx
		mov	word [messagepointer+2], fs
		jb	short locret_1C4A7
		mov	BYTE [byte_1DE7E], 0
		call far read_sndsettings
		mov	[snd_card_type], al
		mov	[snd_base_port_0], dx
		mov	[irq_number_1],	cl
		mov	[dma_channel_1], ch
		mov	[freq_1DCF6], ah
		mov	[byte_1DCF7], bl
		mov	[byte_1DCF8], bh
		mov	[configword], si
		mov	[outp_freq], bp
		mov	BYTE [byte_1DE7C], 1
		cmp	BYTE [snd_card_type], 0
		jnz	short loc_1C4A6
		mov	byte [cs:loc_1AA73+4], 0Fh

loc_1C4A6:				; CODE XREF: callsubx+6Fj
		clc

locret_1C4A7:				; CODE XREF: callsubx+36j
		retn


; =============== S U B	R O U T	I N E =======================================


rereadrtc_settmr:	; CODE XREF: int1a_timer+9p
		mov	ah, 2
		int	1Ah		; CLOCK	- READ REAL TIME CLOCK (AT,XT286,CONV,PS)
					; Return: CH = hours in	BCD
					; CL = minutes in BCD
					; DH = seconds in BCD
		xor	eax, eax
		mov	al, dh
		mov	ah, al
		shr	ah, 4
		and	al, 0Fh
		aad
		mov	ebx, eax
		mov	al, ch
		mov	ah, al
		shr	ah, 4
		and	al, 0Fh
		aad
		imul	edx, eax, 60
		mov	al, cl
		mov	ah, al
		shr	ah, 4
		and	al, 0Fh
		aad
		add	dx, ax
		imul	eax, edx, 60
		add	eax, ebx
		mov	edx, 1193180
		mul	edx
		shrd	eax, edx, 10h
		xor	dx, dx
		mov	es, dx
		mov	[es:46Ch], eax
		retn


; =============== S U B	R O U T	I N E =======================================


spectr_1C4F8:	; CODE XREF: spectr_1BBC1+2Ap
		xor	eax, eax
		mov	edx, 40000000h

loc_1C501:				; CODE XREF: spectr_1C4F8+21j
		mov	ecx, eax
		add	ecx, edx
		shr	eax, 1
		cmp	ecx, ebx
		jg	short loc_1C515
		sub	ebx, ecx
		add	eax, edx

loc_1C515:				; CODE XREF: spectr_1C4F8+15j
		shr	edx, 2
		jnz	short loc_1C501
		cmp	eax, ebx
		jge	short locret_1C521
		inc	ax

locret_1C521:				; CODE XREF: spectr_1C4F8+26j
		retn


; =============== S U B	R O U T	I N E =======================================


txt_blinkingoff:	; CODE XREF: setvideomode+1Cp
					; text_init2+11Dp
		xor	bl, bl
		mov	ax, 1003h
		int	10h		; - VIDEO - TOGGLE INTENSITY/BLINKING BIT (Jr, PS, TANDY 1000, EGA, VGA)
					; BL = 00h enable background intensity
					; = 01h	enable blink
		retn


; =============== S U B	R O U T	I N E =======================================


txt_enableblink:	; CODE XREF: start+1F0p dosexec+5p
		mov	bl, 1
		mov	ax, 1003h
		int	10h		; - VIDEO - TOGGLE INTENSITY/BLINKING BIT (Jr, PS, TANDY 1000, EGA, VGA)
					; BL = 00h enable background intensity
					; = 01h	enable blink
		retn


; =============== S U B	R O U T	I N E =======================================


my_u32tox:		; CODE XREF: useless_sprint_12+8p
		ror	eax, 10h
		call	my_u16tox
		ror	eax, 10h


; =============== S U B	R O U T	I N E =======================================


my_u16tox:		; CODE XREF: my_u32tox+4p
					; useless_sprint_11+7p
		xchg	al, ah
		call	my_u8tox
		mov	al, ah


; =============== S U B	R O U T	I N E =======================================


my_u8tox:		; CODE XREF: my_u16tox+2p
					; useless_sprint_10+7p
		push	ax
		shr	al, 4
		call	my_u4tox
		pop	ax


; =============== S U B	R O U T	I N E =======================================


my_u4tox:		; CODE XREF: my_u8tox+4p
		and	al, 0Fh
		or	al, '0'
		cmp	al, '9'
		jbe	short loc_1C556
		add	al, 7

loc_1C556:				; CODE XREF: my_u4tox+6j
		mov	[si], al
		inc	si
		retn


; =============== S U B	R O U T	I N E =======================================


my_i8toa10:		; CODE XREF: seg001:2DC1p
					; useless_sprint_7+7p
		cbw

my_i16toa10:				; CODE XREF: useless_sprint_8+7p
		cwde

my_i32toa10:				; CODE XREF: useless_sprint_9+8p
		xor	cx, cx
		or	eax, eax
		jns	short my_i32toa10_
		mov	dl, '-'
		call	myputdigit
		neg	eax
		jmp	short my_i32toa10_


; =============== S U B	R O U T	I N E =======================================


my_u8toa10:		; CODE XREF: text_init2:loc_1A6A1p
					; text_init2+239p ...
		xor	ah, ah


; =============== S U B	R O U T	I N E =======================================


my_u16toa10:	; CODE XREF: text_init2+28Fp
					; txt_draw_bottom+13Ep	...
		movzx	eax, ax


; =============== S U B	R O U T	I N E =======================================


my_u32toa10:	; CODE XREF: my_u32toa_fill+6p
					; useless_sprint_6+8p
		xor	cx, cx

my_i32toa10_:				; CODE XREF: my_i8toa10+8j
					; my_i8toa10+12j
		mov	ebx, 10


; =============== S U B	R O U T	I N E =======================================


my_u32toa:		; CODE XREF: my_u32toa+Dp
		xor	edx, edx
		div	ebx
		or	eax, eax
		jz	short loc_1C58E
		push	edx
		call	my_u32toa
		pop	edx

loc_1C58E:				; CODE XREF: my_u32toa+9j
		or	dl, '0'


; =============== S U B	R O U T	I N E =======================================


myputdigit:		; CODE XREF: my_i8toa10+Cp
		mov	[si], dl
		inc	si
		inc	cx
		retn

; ---------------------------------------------------------------------------

; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


mystrlen:		; CODE XREF: start+2D6p
		mov	ax, -1
		dec	si

loc_1C6AB:				; CODE XREF: mystrlen+9j
		inc	ax
		inc	si
		cmp	byte [si], 0
		jnz	short loc_1C6AB
		sub	si, ax
		retn


; =============== S U B	R O U T	I N E =======================================


strcpy_count:	; CODE XREF: useless_mysprintf+26p
					; useless_mysprintf+43p
		xor	cx, cx
		jmp	short loc_1C6BE
; ---------------------------------------------------------------------------

loc_1C6B9:				; CODE XREF: strcpy_count+Ej
		mov	[es:di], al
		inc	si
		inc	di

loc_1C6BE:				; CODE XREF: strcpy_count+2j
		mov	al, [si]
		inc	cx
		or	al, al
		jnz	short loc_1C6B9
		retn


; =============== S U B	R O U T	I N E =======================================


mouse_init:		; CODE XREF: start+16Dp start+74Ap
		mov	BYTE [mouse_visible], 0
		xor	ax, ax
		mov	es, ax
		cmp	dword [es:0CCh], 0
		jz	short loc_1C708
		mov	ax, 21h	; '!'
		int	33h		; - MS MOUSE - SOFTWARE	RESET
					; Return: AX = FFFFh if	mouse driver installed
					; AX = 0021h if	mouse driver not installed
					; BX = 2 if mouse driver is installed
		cmp	ax, 0FFFFh
		jz	short loc_1C6EF
		xor	ax, ax
		int	33h		; - MS MOUSE - RESET DRIVER AND	READ STATUS
					; Return: AX = status
					; BX = number of buttons
		test	ax, ax
		jz	short loc_1C708
		cmp	ax, 0FFFFh
		jnz	short loc_1C708

loc_1C6EF:				; CODE XREF: mouse_init+1Aj
		mov	BYTE [mouse_exist_flag], 1
		push	es
		mov	ax, seg001
		mov	es, ax
		mov	dx, loc_1C72C
		mov	cx, 1Fh
		mov	ax, 0Ch
		int	33h		; - MS MOUSE - DEFINE INTERRUPT	SUBROUTINE PARAMETERS
					; CX = call mask, ES:DX	-> FAR routine
		pop	es
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C708:				; CODE XREF: mouse_init+10j
					; mouse_init+22j ...
		mov	BYTE [mouse_exist_flag], 0
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


mouse_deinit:	; CODE XREF: start:loc_19256p
					; start:loc_197D6p
		cmp	BYTE [mouse_exist_flag], 1
		jnz	short locret_1C72B
		mov	BYTE [mouse_exist_flag], 0
		mov	BYTE [mouse_visible], 0
		xor	dx, dx
		mov	es, dx
		mov	cx, dx
		mov	ax, 0Ch
		int	33h		; - MS MOUSE - DEFINE INTERRUPT	SUBROUTINE PARAMETERS
					; CX = call mask, ES:DX	-> FAR routine

locret_1C72B:				; CODE XREF: mouse_deinit+5j
		retn

; ---------------------------------------------------------------------------

loc_1C72C:				; DATA XREF: mouse_init+34o
		push	ds
		push	dseg
		pop	ds
		mov	[mousecolumn], cx
		mov	[mouserow], dx
		mov	[byte_1DE90], bl
		pop	ds
		retf

; =============== S U B	R O U T	I N E =======================================


mouse_show:		; CODE XREF: start+332p
		cmp	BYTE [mouse_exist_flag], 1
		jnz	short locret_1C755
		cmp	BYTE [mouse_visible], 1
		jz	short locret_1C755
		mov	BYTE [mouse_visible], 1
		call	mouse_showcur

locret_1C755:				; CODE XREF: mouse_show+5j
					; mouse_show+Cj
		retn


; =============== S U B	R O U T	I N E =======================================


mouse_hide:		; CODE XREF: start+376p
					; start:loc_19827p ...
		cmp	BYTE [mouse_exist_flag], 1
		jnz	short locret_1C76C
		cmp	BYTE [mouse_visible], 0
		jz	short locret_1C76C
		mov	BYTE [mouse_visible], 0
		call	mouse_hide2

locret_1C76C:				; CODE XREF: mouse_hide+5j
					; mouse_hide+Cj
		retn


; =============== S U B	R O U T	I N E =======================================


mouse_getpos:
		cmp	BYTE [mouse_exist_flag], 1
		jnz	short loc_1C783
		mov	ax, 3
		int	33h		; - MS MOUSE - RETURN POSITION AND BUTTON STATUS
					; Return: BX = button status, CX = column, DX =	row
		mov	[mousecolumn], cx
		mov	[mouserow], dx
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C783:				; CODE XREF: mouse_getpos+5j
		xor	bx, bx
		xor	cx, cx
		xor	dx, dx
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


mouse_showcur:	; CODE XREF: mouse_show+13p
		cmp	BYTE [mouse_exist_flag], 1
		jnz	short loc_1C7A7
		mov	ax, 1
		int	33h		; - MS MOUSE - SHOW MOUSE CURSOR
					; SeeAlso: AX=0002h, INT 16/AX=FFFEh
		clc
		retn


; =============== S U B	R O U T	I N E =======================================


mouse_hide2:	; CODE XREF: mouse_hide+13p
		cmp	BYTE [mouse_exist_flag], 1
		jnz	short loc_1C7A7
		mov	ax, 2
		int	33h		; - MS MOUSE - HIDE MOUSE CURSOR
					; SeeAlso: AX=0001h, INT 16/AX=FFFFh
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C7A7:				; CODE XREF: mouse_showcur+5j
					; mouse_hide2+5j
		stc
		retn


; =============== S U B	R O U T	I N E =======================================


mouse_1C7A9:	; CODE XREF: mouse_1C7CF+10p
		cmp	cx, si
		jbe	short loc_1C7AF
		xchg	cx, si

loc_1C7AF:				; CODE XREF: mouse_1C7A9+2j
		cmp	dx, di
		jbe	short loc_1C7B5
		xchg	dx, di

loc_1C7B5:				; CODE XREF: mouse_1C7A9+8j
		cmp	ax, cx
		jb	short loc_1C7CA
		cmp	ax, si
		ja	short loc_1C7CA
		cmp	bp, dx
		jb	short loc_1C7CA
		cmp	bp, di
		ja	short loc_1C7CA
		sub	ax, cx
		sub	bp, dx
		retn
; ---------------------------------------------------------------------------

loc_1C7CA:				; CODE XREF: mouse_1C7A9+Ej
					; mouse_1C7A9+12j ...
		stc
		retn

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR mouse_1C7CF

loc_1C7CC:				; CODE XREF: mouse_1C7CF+13j
		add	bx, 0Ah
; END OF FUNCTION CHUNK	FOR mouse_1C7CF

; =============== S U B	R O U T	I N E =======================================


; void *__usercall mouse_1C7CF<ebx>(struct struct_0 *mystr<ebx>)
mouse_1C7CF:	; CODE XREF: start+7ADp start+7C9p ...

; FUNCTION CHUNK AT 377C SIZE 00000003 BYTES

		mov	cx, [bx]
		cmp	cx, -1
		jz	short loc_1C7E9
		mov	dx, [bx+2]
		mov	si, [bx+4]
		mov	di, [bx+6]
		call	mouse_1C7A9
		jb	short loc_1C7CC
		mov	bx, [bx+8]
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C7E9:				; CODE XREF: mouse_1C7CF+5j
		stc
		retn

; ---------------------------------------------------------------------------
		times	5	db 0

; ===========================================================================

; Segment type:	Pure data
SEGMENT	dseg	ALIGN=16	public	CLASS=DATA	use16
aInertiaPlayerV1_ db 'Inertia Player V1.22 written by Stefan Danes and Ramon van Gorkom'
		db 0Dh,0Ah
		db 0Ah
		db 'Usage: IPLAY [Switches] [FileName.Ext|@FileList.Ext]',0Dh,0Ah
		db 0Ah
		db 'Switches:',0Dh,0Ah
		db ' /?  This help screen',0Dh,0Ah
		db ' /h  This help screen (again???)',0Dh,0Ah
		db ' /i  Display current soundcard settings',0Dh,0Ah
		db ' /l  Loop module when it',27h,'s done',0Dh,0Ah
		db ' /d  Disable module looping',0Dh,0Ah
		db ' /g  Start with graphical scopes [F-2]',0Dh,0Ah
		db ' /t  Start with textmode VU meters [F-3]',0Dh,0Ah
		db ' /f  Start with FastFourier screen [F-5]',0Dh,0Ah
		db ' /e  Disable EMS usage',0Dh,0Ah
		db ' /u  Disable UMB usage',0Dh,0Ah
		db ' /o  Enable GUS Channel Optimize [Use minimum number of voices]',0Dh
		db 0Ah
		db ' /c  Disable GUS Channel Optimize [Always use 32 voices]',0Dh,0Ah
		db ' /v  Desqview mode: Only use 80x25 textmode',0Dh,0Ah,'$'
aCurrentSoundcard db 0Dh,'Current Soundcard settings:',0Dh,0Ah ; DATA XREF: start:loc_19057o
		db 0Ah,'$'
myendl		db 0Dh,0Ah,'$'          ; DATA XREF: start-1Do
off_1CA8E	dw f3_textmetter	; DATA XREF: start+182r
		dw f2_waves
		dw f5_graphspectr
		dw f4_patternnae
		dw f1_help
		dw f6_undoc
table_sndcrdname dw aGravisUltrasou ; DATA XREF:	text_init2+19Dr
					; "Gravis UltraSound"
		dw aProAudioSpectr ; "Pro Audio Spectrum	16"
		dw aWindowsSoundSy ; "Windows Sound System"
		dw aSoundBlaster16 ; "Sound Blaster 16/16ASP"
		dw aSoundBlasterPr ; "Sound Blaster Pro"
		dw aSoundBlaster	; "Sound Blaster"
		dw aCovox	; "Covox"
		dw aStereoOn1	; "Stereo-On-1"
		dw aAdlibSoundcard ; "Adlib SoundCard"
		dw aPcHonker	; "PC Honker"
		dw aGeneralMidi	; "General MIDI"
aGravisUltrasou	db 'Gravis UltraSound',0 ; DATA XREF: dseg:table_sndcrdnameo
aGravisMaxCodec	db 'Gravis MAX Codec',0
aProAudioSpectr	db 'Pro Audio Spectrum 16',0 ; DATA XREF: dseg:02ACo
aWindowsSoundSy	db 'Windows Sound System',0 ; DATA XREF: dseg:02AEo
aSoundBlaster16	db 'Sound Blaster 16/16ASP',0 ; DATA XREF: dseg:02B0o
aSoundBlasterPr	db 'Sound Blaster Pro',0 ; DATA XREF: dseg:02B2o
aSoundBlaster	db 'Sound Blaster',0    ; DATA XREF: dseg:02B4o
aCovox		db 'Covox',0            ; DATA XREF: dseg:02B6o
aStereoOn1	db 'Stereo-On-1',0      ; DATA XREF: dseg:02B8o
aAdlibSoundcard	db 'Adlib SoundCard',0  ; DATA XREF: dseg:02BAo
aPcHonker	db 'PC Honker',0        ; DATA XREF: dseg:02BCo
aGeneralMidi	db 'General MIDI',0     ; DATA XREF: dseg:02BEo
atop_title	dw 152h			; DATA XREF: txt_draw_top_title+12o
		db 7Fh
aInertiaPlayerV1_22A db	'Inertia Player V1.22 Assembly ',27h,'94 CD Edition by Sound Solution'
		db 's'
		db    1
		db 0F4h	; Ù
		db    1
aCopyrightC1994	db 'Copyright (c) 1994,1995 by Stefan Danes and Ramon van Gorkom',0
		db 2
		db  78h	; x
		db    1
		db 0AAh	; ™
		db    1
aShell130295211	db 'Shell: 13/02/95 21:15:58'
		db    1
		db  46h	; F
		db    1
aPlayer13029521	db 'Player: '
a130295211558	db '13/02/95 21:15:58',0 ; DATA XREF: read_module+BEw
bottom_menu	dw 0Ah			; DATA XREF: text_init2+21Fo
		db 7Fh
asc_1CC2D	db '                              ' ; DATA XREF: read_module+A3o
		db    1
		dw 0AAh
		db    2
		db 7Eh
aFilename_0	db 'Filename      : '
		db    2
		db 7Fh
aFilename_ext	db 'FileName.Ext'       ; DATA XREF: read_module:loc_19E41o
		db    1
		dw 14Ah
		db    2
		db 7Eh
aModuleType_0	db 'Module Type   : '
		db    2
		db  7Fh	; 
module_type_txt	db '    '               ; DATA XREF: read_module+6Fw
		db    2
		db  7Eh	; ~
		db    1
		dw 1EAh
aChannels	db 'Channels      :'
		db    1
		dw 28Ah
aSamplesUsed	db 'Samples Used  :'
		db    1
		dw 32Ah
aCurrentTrack	db 'Current Track :'
		db    1
		dw 3CAh
aTrackPosition	db 'Track Position:'
		db    1
		dw 46Ah
aSpeed		db 'Speed'
		db    1
		dw 486h
		db ':'
		db    2
		db  78h	; x
		db    1
		dw 4A4h
aTab		db 'Tab'
		db    1
		dw 0F8h
		db    2
byte_1CCEB	db 78h			; DATA XREF: text_init2:loc_1A6C2w
		db 0FEh	; ˛
		db    2
		db 7Eh
aPlayingInStereoFree db	' Playing in Stereo, Free:'
		db    1
		dw 198h
		db    2
		db  78h	; x
		db 0FEh	; ˛
		db    2
		db 7Eh
aProtracker1_0_0 db ' ProTracker 1.0'
		db    1
		dw 1CEh
		db    2
		db 78h
aF9_4		db 'F-9'
		db    1
		dw 238h
		db    2
		db  78h	; x
		db 0FEh	; ˛
		db    2
		db 7Eh
aIgnoreBpmChanges db ' Ignore BPM changes'
		db    1
		dw 26Eh
		db    2
		db 78h
aF10_1		db 'F-10'
		db    2
		db  7Eh	; ~
		db    1
		dw 2D8h
		db    2
		db  78h	; x
		db 0FEh	; ˛
		db    2
		db 7Eh
aLoopModuleWhenDone db ' Loop Module when done'
		db    1
		dw 30Eh
		db    2
		db 78h
aF11_1		db 'F-11'
		db    2
		db 7Eh
		db    1
		dw 378h
		db    2
		db 78h
		db 0FEh	; ˛
		db    2
		db 7Eh
a24bitInterpolation db ' 24bit Interpolation'
		db    1
		dw 3AEh
		db    2
		db 78h
aF12_1		db 'F-12'
		db    2
		db  7Eh	; ~
		db    1
		dw 418h
aMainVolume	db 'Main Volume   :'
		db 1
		dw 44Eh
		db    2
		db 78h
		db '- +'
		db    2
		db  7Eh	; ~
		db    1
		dw 4B8h
aVolumeAmplify	db 'Volume Amplify:'
		db    1
		dw 4EEh
		db    2
		db  78h	; x
		db '[ ]',0
f1_help_text	dw 3F8h			; DATA XREF: seg001:1CD8o
		db 7Fh
aSoYouWantedSomeHelp db	'So you wanted some help?'
		db    1
		dw 468h
		db    2
		db 7Fh
aF2_0		db 'F-2'
		db    2
		db 7Eh
aGraphicalScopesOneF db	'  Graphical scopes, one for each channel'
		db    1
		dw 508h
		db    2
		db 7Fh
aF3_0		db 'F-3'
		db    2
		db 7Eh
aRealtimeVuMeters db '  Realtime VU meters'
		db    1
		dw 5A8h
		db    2
		db 7Fh
aF4_0		db 'F-4'
		db    2
		db 7Eh
aViewSampleNamesTwic db	'  View sample names (twice for more)'
		db    1
		dw 648h
		db    2
		db 7Fh
aF5_0		db 'F-5'
		db    2
		db 7Eh
aFastfourierFrequenc db	'  FastFourier Frequency Analysis'
		db    1
		dw 6E8h
		db    2
		db 7Fh
aF8_0		db 'F-8'
		db    2
aDosShellTypeEx	db 7Eh
aDosShellTypeExitToR db	'  DOS Shell (Type EXIT to return)'
		db    1
		dw 788h
		db    2
aF9_1		db 7Fh
aF9_2		db 'F-9'
		db    2
aProtracker1_0C	db 7Eh
aProtracker1_0Compat db	'  ProTracker 1.0 compatibility on/off'
		db    1
		dw 828h
		db    2
aF10		db 7Fh
aF10_0		db 'F-10'
		db    2
aDisableBpmOnOf	db 7Eh
aDisableBpmOnOff db ' Disable BPM on/off'
		db    1
		dw 8C8h
		db    2
aF11		db 7Fh
aF11_0		db 'F-11'
		db    2
aLoopModule	db 7Eh
aLoopModule_0	db ' Loop module'
		db    1
		dw 968h
		db    2
aF12		db 7Fh
aF12_0		db 'F-12'
		db    2
aToggle24bitInt	db 7Eh
aToggle24bitInterpol db	' Toggle 24bit Interpolation'
		db    1
		dw 4C4h
		db    2
aGray		db 7Fh
aGray_0		db 'Gray - +'
		db    2
aDecIncVolume	db 7Eh
aDecIncVolume_0	db '  Dec/Inc volume'
		db    1
		dw 56Eh
		db    2
		db 7Fh
		db '[ ]'
		db    2
aDecIncAmplify	db 7Eh
aDecIncAmplify_0 db '  Dec/Inc amplify'
		db    1
		dw 600h
		db    2
aCursor		db 7Fh
aCursor_1	db 'Cursor '
		db  1Ah
		db ' '
		db  18h
		db    2
		db  7Eh	; ~
aFastErForward	db '  Fast(er) forward'
		db    1
		dw 6A0h
		db    2
		db 7Fh
aCursor_0	db 'Cursor ',1Bh,' '
		db  19h
		db    2
		db  7Eh	; ~
aFastErRewind	db '  Fast(er) rewind'
		db    1
		dw 744h
		db    2
		db 7Fh
a1Thru0		db '1 Thru 0'
		db    2
		db  7Eh	; ~
aMuteChannel	db '  Mute channel'
		db    1
		dw 7E0h
		db    2
		db 7Fh
aScrolllock	db 'ScrollLock'
		db    2
		db  7Eh	; ~
aLoopPattern	db '  Loop pattern'
		db    1
		dw 88Ah
		db    2
		db  7Fh	; 
aPause		db 'Pause'
		db    2
		db  7Eh	; ~
aGuess___	db '  Guess...'
		db    1
		dw 92Eh
		db    2
		db 7Fh
aEnd		db 'End'
		db    2
		db  7Eh	; ~
aEndPattern	db '  End pattern'
		db    1
		dw 9CEh
		db    2
		db 7Fh
aTab_0		db 'Tab'
		db    2
		db  7Eh	; ~
aTogglePalNtsc	db '  Toggle PAL/NTSC',0
; char hopeyoulike[1]
hopeyoulike	dw 3C6h			; DATA XREF: start+204o
		db 7Eh
aHopeYouLikedUsingTh db	'Hope you liked using the '
		db    2
		db  7Fh	; 
aInertiaPlayer	db 'Inertia Player'
		db    2
		db  7Eh	; ~
aWhichIsWrittenIn db ' which is written in '
		db    2
		db  7Fh	; 
a100Assembler	db '100% assembler!'
		db    2
		db  7Eh	; ~
		db    1
		dw 50Ch
aIfYouHaveBugReports db	'If you have bug-reports, suggestions or comments send a message t'
		db 'o:'
		db    1
		dw 5ACh
aInternet	db 'Internet : '
		db    2
		db  7Fh	; 
aSdanes@marvels_hack db	'sdanes@marvels.hacktic.nl'
		db    2
		db  7Eh	; ~
		db    1
		dw 64Ch
aFidonet	db 'FidoNet  : '
		db    2
		db  7Fh	; 
a2284116_8	db '2:284/116.8'
		db    2
		db  7Eh	; ~
		db    1
		dw 826h
aSendEmailTo	db 'Send email to '
		db    2
		db  7Fh	; 
aListserver@oliver_s db	'listserver@oliver.sun.ac.za'
		db    2
		db  7Eh	; ~
aToSubscribeToOneOrB db	' to subscribe to one or both of'
		db    1
		dw 8C6h
aThe		db 'the '
		db    2
		db  7Fh	; 
aInertiaMailinglists db	'Inertia Mailinglists'
		db    2
		db  7Eh	; ~
aAndWriteFollowingTe db	' and write following text in your message:'
		db    1
		dw 966h
aToConnectToBinaryIn db	'To connect to Binary Inertia releases: '
		db    2
		db  7Fh	; 
aSubscribeInertiaLis db	'subscribe inertia-list YourRealName'
		db    2
		db  7Eh	; ~
		db    1
		dw 0A06h
aToConnectToDiscussi db	'To connect to Discussion Mailing list: '
		db    2
		db  7Fh	; 
aSubscribeInertiaTal db	'subscribe inertia-talk YourRealName',0
; char word_1D26D
word_1D26D	dw 3F2h			; DATA XREF: dosexec+19o
		db  7Eh	; ~
aShellingToOperating db	'Shelling to Operating System...'
		db    1
		dw 52Ah
aType		db 'Type '
		db    2
		db  7Fh	; 
aExit		db 'EXIT'
		db    2
		db  7Eh	; ~
aToReturnTo	db ' to return to '
		db    2
		db  7Fh	; 
aInertiaPlayer_0 db 'Inertia Player',0
; char msg[]
msg		db 'Searching directory for modules  ',0 ; DATA XREF: start+2F7o
; char aLoadingModule[]
aLoadingModule	db 'Loading module',0   ; DATA XREF: start+41Ao
; char aModuleIsCorrupt[]
aModuleIsCorrupt db 'Module is corrupt!',0 ; DATA XREF: start+439o
aNotEnoughDram_0 db 'Not enough DRAM on your UltraSound to load all samples!',0
					; DATA XREF: start+431o
aNotEnoughMemo_0 db 'Not enough memory available to load all samples!',0
					; DATA XREF: start+429o
; char aDeleteMarkedFil[]
aDeleteMarkedFil db 'Delete marked files? [Y/N]',0 ; DATA XREF: start+635o
; char aDeletingFile[15]
aDeletingFile	db 'Deleting file: '    ; DATA XREF: start+69Fo
aFile		db 'File'               ; DATA XREF: start+689w start+6A8o
aName		db 'name'               ; DATA XREF: start+692w
a_ext		db '.Ext'               ; DATA XREF: start+69Bw
		db 0
aPal		db '(PAL) ',0           ; DATA XREF: txt_draw_bottom+49o
; char aNtsc[]
aNtsc		db '(NTSC)',0           ; DATA XREF: txt_draw_bottom+53o
; char word_1D3B0[1]
word_1D3B0	dw 49Eh			; DATA XREF: start+723o
		db  7Bh	; {
aFileSelectorHelp db 'File Selector Help'
		db    1
		dw 6F2h
		db    2
		db  7Eh	; ~
aUse		db 'Use '
		db    2
		db  7Fh	; 
aHome		db 'Home'
		db    2
		db  7Eh	; ~
		db ','
		db    2
		db  7Fh	; 
aEnd_0		db 'End'
		db    2
		db  7Eh	; ~
		db ','
		db    2
		db  7Fh	; 
aPgup		db 'PgUp'
		db    2
		db  7Eh	; ~
		db ','
		db    2
		db  7Fh	; 
aPgdn		db 'PgDn'
		db    2
		db  7Eh	; ~
		db ','
		db    2
		db  7Fh	; 
		db  18h
		db    2
		db  7Eh	; ~
aAnd		db ' and '
		db    2
		db  7Fh	; 
		db  19h
		db    2
		db  7Eh	; ~
aToMoveTheHighlighte db	' to move the highlighted bar'
		db    1
		dw 792h
aPress		db 'Press '
		db    2
		db  7Fh	; 
aEnter		db 'Enter'
		db    2
		db  7Eh	; ~
aToPlayTheModuleOrSe db	' to play the module or select the drive/directory'
		db    1
		dw 8D2h
		db    2
		db  7Fh	; 
aEsc		db 'ESC'
		db    2
		db  7Eh	; ~
		db    1
		dw 8E6h
aQuitIplay	db 'Quit IPLAY'
		db    1
		dw 972h
		db    2
		db  7Fh	; 
aF1		db 'F-1'
		db    2
		db  7Eh	; ~
		db    1
		dw 986h
aThisHelpScreenButIG db	'This help screen, but I guess you already found it...'
		db    1
		dw 0A12h
		db    2
		db  7Fh	; 
aF8_1		db 'F-8'
		db    2
		db  7Eh	; ~
		db    1
		dw 0A26h
aDosShellTypeExitT_0 db	'DOS Shell (Type EXIT to return)'
		db    1
		dw 0AB2h
		db    2
		db  7Fh	; 
aF9_3		db 'F-9'
		db    2
		db  7Eh	; ~
		db    1
		dw 0AC6h
aToggleQuickreadingO db	'Toggle QuickReading of module name'
		db    1
		dw 0B52h
unk_1D516	db    2
		db  7Fh	; 
aDel		db 'Del'
		db    2
		db  7Eh	; ~
		db    1
		dw 0B66h
aMarkFileToDelete db 'Mark file to delete'
		db    1
		dw 0BF2h
		db    2
		db  7Fh	; 
aCtrlDel	db 'Ctrl Del'
		db    2
		db  7Eh	; ~
		db    1
		dw 0C06h
aDeleteAllFilesWhich db	'Delete all files which are marked to delete'
		db    1
		dw 0C92h
		db    2
		db  7Fh	; 
aBackspace	db 'BackSpace'
		db    2
		db  7Eh	; ~
		db    1
		dw 0CA6h
aReturnToPlaymodeOnl db	'Return to playmode [Only if the music is playing]'
		db    1
		dw 0E86h
		db    2
		db  7Eh	; ~
aPressAnyKeyToReturn db	'Press any key to return to the fileselector',0
; char aPressF1ForHelpQu[11]
aPressF1ForHelpQu db '                 Press F-1 for help, QuickRead='
					; DATA XREF: start+367o
word_1D614	dw 2020h		; DATA XREF: useless_197F2+7w
					; useless_197F2:loc_19810w
byte_1D616	db 20h			; DATA XREF: useless_197F2+Dw
					; useless_197F2+24w
aF9		db ' [F-9]              ',0
aHitBackspaceToRe db 'Hit backspace to return to playmode, F-1 for help, QuickRead='
					; DATA XREF: start+35Do
word_1D669	dw 2020h		; DATA XREF: useless_197F2+12w
					; useless_197F2+29w
byte_1D66B	db 20h			; DATA XREF: useless_197F2+18w
					; useless_197F2+2Fw
aF9_0		db ' [F-9]',0
aSamplename	db '# SampleName   '    ; DATA XREF: seg001:1B7Co
		db    2
aXpressF4ForMor	db 'xPress F-4 for more'
		db    2
aSizeVolModeC2T	db '~   Size Vol Mode  C-2 Tune LoopPos LoopEnd',0
unk_1D6C3	db    2			; DATA XREF: seg001:1BDAo
aUnused256	db ' Unused'
a256		db '256',0              ; DATA XREF: text_init2+1CEo
a512		db '512',0
a768		db '768',0
a1024		db '1024',0
; char aKb[]
aKb		db 'KB',0               ; DATA XREF: text_init2+1D7o
asc_1D6E0	db '               ',0  ; DATA XREF: seg001:1A80o
aPortamentoUp	db 'Portamento Up  ',0
aPortamentoDown	db 'Portamento Down',0
aTonePortamento	db 'Tone Portamento',0
aVibrato	db 'Vibrato        ',0
aPortVolslide	db 'Port + VolSlide',0
aVibrVolslide	db 'Vibr + VolSlide',0
aTremolo	db 'Tremolo        ',0
aFinePanning	db 'Fine Panning   ',0
aSetSampleOfs	db 'Set Sample Ofs ',0
aVolumeSliding	db 'Volume Sliding ',0
aPositionJump	db 'Position Jump  ',0
aVolumeChange	db 'Volume Change  ',0
aPatternBreak	db 'Pattern Break  ',0
aE_command	db 'E_Command      ',0
aSetSpeedBpm	db 'Set Speed/BPM  ',0
aSetSpeed	db 'Set Speed      ',0
aFinePortaUp	db 'Fine Porta Up  ',0
aFinePortaDown	db 'Fine Porta Down',0
aFineTonePorta	db 'Fine Tone Porta',0
aFineVibrato	db 'Fine Vibrato   ',0
aFineVolSlide	db 'Fine Vol Slide ',0
aFinePortVolsl	db 'Fine Port+VolSl',0
aFineVibrVolsl	db 'Fine Vibr+VolSl',0
aSetStmSpeed	db 'Set STM Speed  ',0
aAutoToneporta	db 'Auto TonePorta ',0
aTriller	db 'Triller        ',0
aTremor		db 'Tremor         ',0
aRetrigVolume	db 'Retrig+Volume  ',0
aArpeggio	db 'Arpeggio       ',0  ; DATA XREF: seg001:loc_1AB0Do
aSetAmplify	db 'Set Amplify    ',0
aFarTempo	db 'FAR Tempo      ',0
aFarFineTempo	db 'FAR Fine Tempo ',0
aSetFilter	db 'Set Filter     ',0  ; DATA XREF: seg001:1A9Ao
aFineslideUp	db 'FineSlide Up   ',0
aFineslideDown	db 'FineSlide Down ',0
aGlissandoCtrl	db 'Glissando Ctrl ',0
aVibratoControl	db 'Vibrato Control',0
aSetFinetune	db 'Set FineTune   ',0
aJumpToLoop	db 'Jump To Loop   ',0
aTremoloControl	db 'Tremolo Control',0
aSetPanning	db 'Set Panning    ',0
aRetriggerNote	db 'Retrigger Note ',0
aFinevolumeUp	db 'FineVolume Up  ',0
aFinevolumeDown	db 'FineVolume Down',0
aNoteCut	db 'Note Cut       ',0
aNoteDelay	db 'Note Delay     ',0
aPatternDelay	db 'Pattern Delay  ',0
aInvertLoop	db 'Invert Loop    ',0
aSetLoopPoint	db 'Set Loop Point ',0  ; DATA XREF: seg001:1A8Fo
asc_1DA00	db '                      ',0 ; DATA XREF: modules_search:loc_19BDDo
					; seg001:loc_1A9A5o
aMute		db '<Mute>                ',0 ; DATA XREF: seg001:1949o
; char aMarkedToDelete[]
aMarkedToDelete	db '<Marked to Delete>    ',0 ; DATA XREF: filelist_198B8+10Do
notes		db '  C-C#D-D#E-F-F#G-G#A-A#B-' ; DATA XREF: seg001:1930r
					; seg001:1B31r	...
slider		db 'ƒ\|/ƒ\|/'           ; DATA XREF: modules_search+7Fr
					; modules_search+F8r
aModuleNotFound	db 'Module not found.',0Dh,0Ah,'$' ; DATA XREF: find_mods+88o
aModuleLoadErro	db 'Module load error.',0Dh,0Ah,'$' ; DATA XREF: readallmoules+1Bo
					; read_module+5o
aNotEnoughMemor	db 'Not enough memory.',0Dh,0Ah,'$' ; DATA XREF: start+23Do
aListFileNotFou	db 'List file not found.',0Dh,0Ah,'$' ; DATA XREF: start+D07o
aCriticalErrorT	db 0Dh,0Ah		; DATA XREF: start+31o
		db 0Ah
		db 'Critical error: The player jumped to DOS, and should not be invok'
		db 'ed again.',0Dh,0Ah
		db 'Close this DOS session first with the "EXIT" command.',0Dh,0Ah
		db 0Ah
		db '(Press any key to continue)$'
sIplay_cfg	db 'C:\IPLAY.CFG',0     ; DATA XREF: loadcfgo
buffer_1DB6C	times	128	db 0		; DATA XREF: start+189r start+192r ...
buffer_1DBEC	db 0			; DATA XREF: find_mods+32o
					; dosfindnexto
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
unk_1DC01	db    0			; DATA XREF: modules_search+8Fr
					; modules_search+108r ...
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
byte_1DC0A	times	62h	db 0		; DATA XREF: find_mods+6Fo
; char buffer_1DC6C[]
buffer_1DC6C	dd 0			; DATA XREF: start+2C5w start+2D3o ...
unk_1DC70	db    0			; DATA XREF: modules_search+1D8o
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db 0
unk_1DC7B	db    0			; DATA XREF: modules_search+1C9o
byte_1DC7C	times	70h	db 0		; DATA XREF: modules_search+1BAo
					; modules_search+202o
dword_1DCEC	dd 10524E49h		; DATA XREF: loadcfg+1Ar
cfg_buffer	db    4			; DATA XREF: loadcfg+Co loadcfg+1Er
snd_card_type	db 3			; DATA XREF: text_init2+18Er
					; text_init2+1ADr ...
snd_base_port_0	dw 0FFFFh		; DATA XREF: callsubx+3r callsubx+45w
irq_number_1	db 0FFh			; DATA XREF: callsubx+7r callsubx+49w
dma_channel_1	db 0FFh			; DATA XREF: callsubx+Br callsubx+4Dw
freq_1DCF6	db 2Ch			; DATA XREF: callsubx+Fr callsubx+51w
byte_1DCF7	db 0FFh			; DATA XREF: callsubx+1Cr callsubx+55w
byte_1DCF8	db 14h			; DATA XREF: start+DAr	callsubx+20r ...
configword	dw 218Bh		; DATA XREF: start+60w	start+6Cw ...
byte_1DCFB	db 4Bh			; DATA XREF: callsubx+13r
		db    0
; char mystr[66]
mystr		times	42h	db 0		; DATA XREF: start:loc_192E0o
					; start:loc_1964Eo
; char byte_1DD3F[69]
byte_1DD3F	times	45h	db 0		; DATA XREF: dosexec:loc_1C209o
					; dosexec:loc_1C25Co
a_mod_nst_669_s	db '.MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FAR.ULT.OKT.OCT',0,0,0,0
					; DATA XREF: modules_search+12Do
					; find_mods+46o
aPlaypausloop	db 'PlayPausLoop'       ; DATA XREF: txt_draw_bottom+164o
aJanfebmaraprmayj db '   JanFebMarAprMayJunJulAugSepOctNovDec'
					; DATA XREF: filelist_198B8+A4o
frameborder	db '      €€€€€€…ª»ºÕ∫⁄ø¿Ÿƒ≥÷∑”Ωƒ∫’∏‘æÕ≥',0 ; DATA XREF: draw_frame+3Do
oint8off_1DE14	dw 0			; DATA XREF: start+F9w
oint8seg_1DE16	dw 0			; DATA XREF: start+FDw
critsectpoint_off dw 0			; DATA XREF: start+150w
critsectpoint_seg dw 0			; DATA XREF: start+154w
swapdata_off	dw 0			; DATA XREF: start+161w
swapdata_seg	dw 0			; DATA XREF: start+165w
videomempointer	dd 0			; DATA XREF: start:loc_1917Dw
					; start+207r ...
videopoint_shiftd dd 0			; DATA XREF: text_init2+5Fw
					; text_init2+BEw ...
segfsbx_1DE28	dd 0			; DATA XREF: read_module+99w
					; keyb_19EFD:l_rightr ...
dword_1DE2C	dd 0			; DATA XREF: text_init2+22Aw
					; seg001:196Br	...
messagepointer	dd 0			; DATA XREF: start+228r start+23Dw ...
volume_1DE34	dd 0			; DATA XREF: read_module+DAw
					; seg001:19F4r
outp_freq	dw 0			; DATA XREF: read_module+82w
					; text_init2:loc_1A699r ...
esseg_atstart	dw 0			; DATA XREF: start+5w parse_cmdline+7r ...
off_1DE3C	dw loc_19050	; DATA XREF: start+186w start+6E7r ...
offs_draw	dw loc_19050	; DATA XREF: keyb_19EFD+32r
					; keyb_19EFD:l_f4r ...
offs_draw2	dw loc_19050	; DATA XREF: keyb_19EFD+486r
					; keyb_19EFD+49Ar ...
off_1DE42	dw loc_19050	; DATA XREF: keyb_19EFD:l_f8r
					; f1_help+12w ...
amount_of_x	dw 0			; DATA XREF: read_module+75w
					; read_module+D1r ...
word_1DE46	dw 0			; DATA XREF: keyb_19EFD+316r
					; text_init2+244w ...
current_patterns dw 0			; DATA XREF: read_module+5Fw
					; keyb_19EFD+30Fw ...
word_1DE4A	dw 0			; DATA XREF: find_mods+14w
					; find_mods+4Er
word_1DE4C	dw 0			; DATA XREF: find_mods+2Ew
					; find_mods+75r
word_1DE4E	dw 0			; DATA XREF: start+19Bw
					; modules_search+5Fw ...
word_1DE50	dw 0			; DATA XREF: start:loc_19242r
					; readallmoules:loc_19D75r ...
word_1DE52	dw 0			; DATA XREF: start+3DCr start+5D2r ...
word_1DE54	dw 0			; DATA XREF: start+4B1r
					; start:loc_1955Dr ...
word_1DE56	dw 0			; DATA XREF: modules_search+4Cw
					; modules_search+B1w
word_1DE58	dw 0			; DATA XREF: modules_search+52w
					; modules_search+172w
word_1DE5A	dw 0			; DATA XREF: modules_search+58w
					; modules_search+27Dw
word_1DE5C	dw 0			; DATA XREF: start+5FFw start+60Cw ...
word_1DE5E	dw 0			; DATA XREF: start+25Aw
					; start:loc_19464r ...
word_1DE60	dw 0			; DATA XREF: start+308w start+5EBw ...
word_1DE62	dw 0			; DATA XREF: start+254w start+31Fr ...
word_1DE64	dw 0			; DATA XREF: modules_searchw
					; modules_search+75r ...
word_1DE66	dw 0			; DATA XREF: modules_search+6w
					; modules_search+79r ...
fhandle_1DE68	dw 0			; DATA XREF: init_vga_waves+42w
					; init_vga_waves+49r ...
word_1DE6A	dw 0			; DATA XREF: keyb_19EFD+1Cw
					; txt_draw_bottom+118r
word_1DE6C	dw 0			; DATA XREF: keyb_19EFD+27w
					; txt_draw_bottom+13Br
word_1DE6E	dw 0			; DATA XREF: keyb_19EFD+30Br
					; text_init2+52w ...
byte_1DE70	db 0			; DATA XREF: start+168w start+268w ...
byte_1DE71	db 0			; DATA XREF: seg001:loc_1A934w
					; seg001:loc_1AA73w
byte_1DE72	db 0			; DATA XREF: keyb_19EFD+5w
					; txt_draw_bottom+66r
byte_1DE73	db 0			; DATA XREF: read_module+79w
					; txt_draw_bottom+72r
byte_1DE74	db 0			; DATA XREF: keyb_19EFD+9w
					; txt_draw_bottom+92r
byte_1DE75	db 0			; DATA XREF: keyb_19EFD+Cw
					; txt_draw_bottom+1Br
byte_1DE76	db 0			; DATA XREF: keyb_19EFD+10w
					; txt_draw_bottom+2Br
flg_play_settings db 0			; DATA XREF: keyb_19EFD+2Fw
					; txt_draw_bottom+4Cr ...
byte_1DE78	db 0			; DATA XREF: read_module+8Bw
					; dosexec+2Cr ...
byte_1DE79	db 0			; DATA XREF: video_prp_mtr_positn+2w
					; video_prp_mtr_positn:loc_1C365w ...
byte_1DE7A	db 0			; DATA XREF: video_prp_mtr_positn+7w
					; video_prp_mtr_positn+1Dw ...
byte_1DE7B	db 0			; DATA XREF: read_module+96w
					; text_init2+20Fr
byte_1DE7C	db 0			; DATA XREF: start:loc_193BCr
					; start+347r ...
byte_1DE7D	db 0			; DATA XREF: start+32Fw start+34Ar ...
byte_1DE7E	db 0			; DATA XREF: start+1B9w start+217r ...
byte_1DE7F	db 0			; DATA XREF: start+260w start+2F0r ...
		db    1
byte_1DE81	db 0			; DATA XREF: spectr_1BBC1+20r
					; video_prp_mtr_positn+58w
byte_1DE82	db 0			; DATA XREF: start+E1w
					; spectr_1BBC1:loc_1BBF4r ...
byte_1DE83	db 3			; DATA XREF: start+E7w
					; seg001:loc_1AA4Fr ...
byte_1DE84	db 0			; DATA XREF: read_module+65w
					; keyb_19EFD:l_upw ...
byte_1DE85	db 0			; DATA XREF: keyb_19EFD+2EBw
					; keyb_19EFD+2FBw ...
byte_1DE86	db 0			; DATA XREF: start+D7w	text_init2r ...
		db 0
dword_1DE88	dd 0			; DATA XREF: start+7DBr start+7E2w ...
mousecolumn	dw 0			; DATA XREF: start+7A0r start+7BCr ...
mouserow	dw 0			; DATA XREF: start+7A3r start+7BFr ...
byte_1DE90	db 0			; DATA XREF: start:loc_193C7r
					; start+33Er ...
mouse_exist_flag db 0			; DATA XREF: mouse_init:loc_1C6EFw
					; mouse_init:loc_1C708w ...
mouse_visible	times	0Ah	db 0		; DATA XREF: mouse_initw
					; mouse_deinit+Cw ...
x_storage	dw  0, 0, 0, 0,	0, 0, 0, 0, 0, 0, 0, 0,	0, 0, 0, 0, 0
					; DATA XREF: f2_draw_waves+1Eo
					; f2_draw_waves2+Do ...
		dw  0, 0, 0, 0,	0, 0, 0, 0, 0, 0, 0, 0,	0, 0, 0, 0
		db    0
		align 10h
; char buffer_1[272]
buffer_1	times	200h	db 0		; DATA XREF: start-30o
					; start:loc_1906Eo ...
					; 2800h
byte_1E0E0	times	7BBh	db 0		; DATA XREF: f5_draw_spectr+29Do
					; f5_draw_spectr+56Do
byte_1E89B	times	1E44h	db 0
		align 10h
buffer_2	times	2800h	db 0		; DATA XREF: init_vga_waves+173o
buffer_1seg	dw 0			; DATA XREF: text_init2+18Bw
					; seg001:18B2r	...
buffer_2seg	dw 0			; DATA XREF: seg001:loc_1A913w
					; seg001:19D1r	...
byte_22EE4	times	1000h	db 0		; DATA XREF: f5_draw_spectr+2A8o
					; f5_draw_spectr+2D0o ...
unk_23EE4	db    0			; DATA XREF: init_f5_spectr+98o
					; f5_draw_spectr+2D9o ...
byte_23EE5	times	63h	db 0		; DATA XREF: f5_draw_spectr+5C0o
byte_23F48	times	12Ch	db 0		; DATA XREF: f5_draw_spectr+5E2o
unk_24074	db    0			; DATA XREF: f5_draw_spectr+5A9o
					; f5_draw_spectr+5C9o ...
byte_24075	times	63h	db 0		; DATA XREF: f5_draw_spectr+5D2o
byte_240D8	times	12Ch	db 0		; DATA XREF: f5_draw_spectr+5EFo
byte_24204	times	200h	db 0		; DATA XREF: f5_draw_spectr+1Ao
					; f5_draw_spectr+2A5o ...
palette_24404	db    0			; DATA XREF: init_vga_waves+17o
		db    1
		db    2
		db    3
		db    4
		db    5
		db    6
		db    7
		db    8
		db    9
		db  0Ah
		db  0Bh
		db  0Ch
		db  0Dh
		db  0Eh
		db  0Fh
		db    0
vga_palette	db 0,0,0		; DATA XREF: init_vga_waves+1Fo
		db 2,2,6
		db 4,5,0Dh
		db 7,8,15h
		db 0Ah,0Bh,1Bh
		db 0Dh,0Eh,21h
		db 10h,11h,2Ah
		db 13h,14h,31h
		db 0,2Ah,2Ah
		db 0,2Dh,2Dh
		db 0,30h,30h
		db 0,33h,33h
		db 0,36h,36h
		db 0,39h,39h
		db 0,3Ch,3Ch
		db 0,3Fh,3Fh
word_24445	dw 0			; DATA XREF: dosexec+69w dosexec+78o ...
		dd unk_24453
		dd unk_24456
		dd unk_24456
unk_24453	db    0			; DATA XREF: dseg:7C57o
		db  20h
		db  0Dh
unk_24456	db  20h			; DATA XREF: dseg:7C5Bo dseg:7C5Fo
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
; struct struct_0 str_24461
str_24461: ; DATA XREF: start+79Do
istruc	struct_0
	dw	6
	dw	 9
	dw		49h
	dw	 9
	dw		loc_1957F
iend
		
		istruc	struct_0
			dw	6
			dw	 19h
			dw	 49h
			dw	 19h
			dw	 loc_1953C
		iend
		
		istruc	struct_0
			dw	8
			dw	 0Ah
			dw	 47h
			dw	 18h
			dw	 loc_19880
		iend
		
		istruc	struct_0
			dw	2
			dw	 1
			dw		4Dh
			dw	 4
			dw		loc_19762
		iend
		dw 0FFFFh
; struct struct_0 stru_2448B
stru_2448B: ; DATA XREF: start+7B9o
istruc	struct_0
	dw	6
	dw	 9
	dw		49h
	dw	 9
	dw		loc_1957F
iend
		
		istruc	struct_0
			dw	6
			dw	 19h
			dw	 49h
			dw	 19h
			dw	 loc_1953C
		iend
		
		istruc	struct_0
			dw	2
			dw	 1
			dw		4Dh
			dw	 4
			dw		loc_1964E
		iend
		dw 0FFFFh
; struct struct_0 stru_244AB
stru_244AB:	; DATA XREF: keyb_19EFD+4AFo
istruc	struct_0
	dw	2
	dw	 1
	dw		4Dh
	dw	 4
	dw		l_enter
iend
		dw 0FFFFh
; struct struct_0 stru_244B7
stru_244B7:	; DATA XREF: keyb_19EFD:loc_1A3C5o
istruc	struct_0
	dw	0
	dw	 0
	dw		4Fh
	dw	 31h
	dw	 l_esc
iend
		dw 0FFFFh
		db    0
unk_244C4	db    0			; DATA XREF: spectr_1B084+14Ew
					; spectr_1B084+18Br ...
		db    0
		db    0
		db    0
dword_244C8	dd 0			; DATA XREF: spectr_1B084+39w
					; spectr_1B084+62r ...
multip_244CC	dd 0			; DATA XREF: spectr_1B084+2Fw
					; spectr_1B084+152r ...
multip_244D0	dd 0			; DATA XREF: spectr_1B084+25w
					; spectr_1B084+169r ...
dword_244D4	dd 0			; DATA XREF: spectr_1B084+3Dw
					; spectr_1B084+6Ar ...
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
dword_244E4	dd 0			; DATA XREF: spectr_1B084+8Bw
					; spectr_1B084+104r ...
dword_244E8	dd 0			; DATA XREF: spectr_1B084+9Aw
					; spectr_1B084+115r ...
dword_244EC	dd 0			; DATA XREF: spectr_1B084+A9w
					; spectr_1B084+BFr ...
dword_244F0	dd 0			; DATA XREF: spectr_1B084+B6w
					; spectr_1B084+CFr ...
dword_244F4	dd 0			; DATA XREF: spectr_1B084+66w
					; spectr_1B084+BAr ...
dword_244F8	dd 0			; DATA XREF: spectr_1B084+6Ew
					; spectr_1B084+DFr ...
dword_244FC	dd 0			; DATA XREF: spectr_1B084+CBw
					; spectr_1B084+108r ...
dword_24500	dd 0			; DATA XREF: spectr_1B084+DBw
					; spectr_1B084+119r ...
dword_24504	dd 0			; DATA XREF: spectr_1B084+100w
					; spectr_1B084+10Dr ...
dword_24508	dd 0			; DATA XREF: spectr_1B084+F0w
					; spectr_1B084+11Er ...
word_2450C	dw 0			; DATA XREF: spectr_1B406+4w
					; spectr_1B406+77r ...
word_2450E	dw 0			; DATA XREF: spectr_1B084w
					; spectr_1B084+7Ar ...
		db    0
		db    0
		db    0
		db    0
word_24514	dw 0			; DATA XREF: spectr_1B084+Fr
					; spectr_1B084+42r ...
word_24516	dw 0			; DATA XREF: spectr_1B406+61w
					; spectr_1B406:loc_1B46Dr ...
word_24518	dw 0			; DATA XREF: spectr_1B406+B2w
					; spectr_1B406+B8r ...
word_2451A	dw 0			; DATA XREF: spectr_1B406+D8w
					; spectr_1B406+DBr
word_2451C	dw 0			; DATA XREF: spectr_1B406+74w
					; spectr_1B406+BDr ...
word_2451E	dw 0			; DATA XREF: spectr_1B406+D1w
					; spectr_1B406+E7r
word_24520	dw 0			; DATA XREF: spectr_1B406+Ar
					; f5_draw_spectr+2CAw ...
word_24522	dw 0			; DATA XREF: spectr_1B406+10w
					; spectr_1B406+3Fr ...
word_24524	dw 0			; DATA XREF: init_f5_spectr:loc_1B080w
					; f5_draw_spectr+2C7r ...
tabledword_24526 dd    0,65536,46340,25079,12785,6423,3215,1608, 804, 402
					; DATA XREF: spectr_1B084+20r
					; spectr_1B084+1CDr ...
		dd  201, 100,  50,  25,	 12
tabledword_24562 dd -131072,-65536,-19196,-4989,-1260,-316, -79, -20,  -5
					; DATA XREF: spectr_1B084+2Ar
					; spectr_1B084+1DAr ...
		dd   -2,  -1,  -1,  -1,	 -1,   0
		db    0
		db    0

; ===========================================================================

; Segment type:	Regular
SEGMENT	seg003	ALIGN=1	public	CLASS=UNK	use16
a070295122642	db '07/02/95 12:26:42',0 ; DATA XREF: seg003:off_2462Eo
					; seg003:off_24656o
pointer_245B4	dd 0			; DATA XREF: sub_135CA+1Cr
					; sub_135CA:loc_135FDw	...
dma_buf_pointer	dd 0			; DATA XREF: mod_readfile_11F4E+9Cw
					; mod_readfile_11F4E+144r ...
dword_245BC	dd 0			; DATA XREF: someplaymode+59w
					; sub_13177+1Dr ...
dword_245C0	dd 0			; DATA XREF: someplaymode:loc_12C3Cw
					; sub_13177+31r ...
dword_245C4	dd 0			; DATA XREF: mod_n_t_module:loc_101F4r
					; mod_1024A+33w ...
off_245C8	dw moduleread	; DATA XREF: sub_12DA8+3Ew
					; sub_13623:loc_13791r	...
off_245CA	dw moduleread	; DATA XREF: sub_12DA8+38w
					; sub_135CA+4Dr ...
off_245CC	dw moduleread	; DATA XREF: change_volume+1Ar
					; sub_12DA8+44w ...
off_245CE	dw moduleread	; DATA XREF: volume_12A66+Fr
					; sub_12DA8+4Aw ...
savesp_245D0	dw 0			; DATA XREF: moduleread+15w
					; moduleread+B6r ...
word_245D2	dw 0			; DATA XREF: mod_n_t_module+9w
					; mod_n_t_module+43w ...
word_245D4	dw 0			; DATA XREF: moduleread+81r
					; moduleread+87r ...
word_245D6	dw 0			; DATA XREF: clean_11C43+4Aw
					; sub_12B83+52w ...
word_245D8	dw 0			; DATA XREF: clean_11C43+50w
					; sub_12B83+57w
word_245DA	dw 0			; DATA XREF: clean_11C43+56w
					; sub_12B83+5Cw
word_245DC	dw 0			; DATA XREF: sub_13623+12Dw
					; sub_13623+29Cr ...
freq_245DE	dw 0			; DATA XREF: mod_1024A+40r
					; _2stm_module+26w ...
off_245E0	dw chrin		; DATA XREF: sub_12DA8+E9w
					; sub_16C69+57Fr
off_245E2	dw myin		; DATA XREF: sub_12DA8+EFw
					; sub_16C69:loc_17202r
word_245E4	dw 0			; DATA XREF: configure_timer+18r
					; sub_13CF6+4Dw ...
word_245E8	dw 0			; DATA XREF: sub_12DA8+5Aw
					; sub_12DA8+F9w ...
word_245EA	dw 0			; DATA XREF: sub_13CF6:loc_13D36w
					; sub_16C69+13r
word_245EC	dw 0			; DATA XREF: sub_13CF6+44w
					; sub_16C69+19r
word_245EE	dw 0			; DATA XREF: sub_13CF6+47w
					; sub_16C69+Aw	...
word_245F0	dw 0			; DATA XREF: clean_11C43+21w
					; sub_1265D+46r ...
word_245F2	dw 0			; DATA XREF: mod_n_t_module+12Dr
					; mod_102F5+17w ...
my_seg_index	dw 0			; DATA XREF: psm_module+136r
					; mem_reallocxr ...
word_245F6	dw 0			; DATA XREF: clean_11C43+27w
					; sub_1265D+42r ...
word_245F8	dw 0			; DATA XREF: mod_1021E:loc_10230w
					; faar_module+9Aw ...
word_245FA	dw 0			; DATA XREF: mod_1021E+8w
					; _2stm_module:loc_104F2w ...
volume_245FC	dw 100h			; DATA XREF: sub_1265D+5r
					; change_volume+Bw ...
amplification	dw 100			; DATA XREF: clean_11C43+83w
					; volume_prepare_waves+72r ...
word_24600	dw 0			; DATA XREF: sub_12EBA+2Cw
					; sub_13017+1Bw ...
word_24602	dw 0			; DATA XREF: sub_12EBA+32w
					; proaud_14700:loc_14E10w ...
interrupt_mask	dw 0			; DATA XREF: setsnd_handler+Cw
					; restore_intvector+3r
old_intprocoffset dw 0			; DATA XREF: setsnd_handler+3Aw
					; restore_intvector+14r
old_intprocseg	dw 0			; DATA XREF: setsnd_handler+3Ew
					; restore_intvector+1Ar
intvectoffset	dw 0			; DATA XREF: setsnd_handler+2Dw
					; restore_intvector+Cr
word_2460C	dw 0			; DATA XREF: deinit_125B9+12r
					; sub_12D35+1Fr ...
word_2460E	dw 0			; DATA XREF: gravis_int+D5w
					; proaud_set+8w ...
word_24610	dw 0			; DATA XREF: volume_prep+6w
					; sub_1279A+4r	...
my_size		dw 0			; DATA XREF: volume_prep+9w
					; sub_1279A+Dr	...
word_24614	dw 0			; DATA XREF: sub_154F4+3Ew
					; sub_1609F-909r ...
byte_24616	db 0			; DATA XREF: sub_154F4+41w
					; sub_154F4+52w ...
byte_24617	db 0			; DATA XREF: ems_realloc2w
					; mod_readfile_11F4Ew ...
byte_24618	db 0			; DATA XREF: sub_13D95-6w sub_13D95w ...
byte_24619	db 0			; DATA XREF: sub_13D95+16w
					; gravis_int+7Cw ...
byte_2461A	db 0			; DATA XREF: s3m_module+1Fw
					; useless_writeinr+44r	...
byte_2461B	db 0			; DATA XREF: moduleread:loc_10028w
					; moduleread:loc_1007Br ...
byte_2461C	db 0			; DATA XREF: sub_12B18+14w
					; sub_12B18:loc_12B71w
byte_2461D	db 0			; DATA XREF: sub_12B18+19w
					; sub_12B18+51w
byte_2461E	db 0			; DATA XREF: s3m_module:loc_10652r
					; e669_module+3Cr ...
byte_2461F	db 0			; DATA XREF: s3m_module+C5r
					; e669_module+38r ...
byte_24620	db 0			; DATA XREF: sub_12EBA+38w
					; proaud_14700+71Cw ...
byte_24621	db 0			; DATA XREF: sub_12EBA+3Dw
					; proaud_14700+73Bw ...
sndflags_24622	db 0			; DATA XREF: useless_11787+9r
					; inr_read_118B0+AEr ...
byte_24623	db 0			; DATA XREF: sub_1265D+33r
					; sub_12DA8+50w ...
bit_mode	db 8			; DATA XREF: sub_12DA8+55w
					; sub_12DA8+E2r ...
byte_24625	db 0			; DATA XREF: clean_11C43+89w
					; change_amplif+Ew ...
gravis_port	dw 0			; DATA XREF: volume_prep+61r
					; gravis_13215+49r ...
byte_24628	db 0			; DATA XREF: mod_readfile_11F4E+1BFr
					; sub_1265D+27r ...
byte_24629	db 20h			; DATA XREF: someplaymode+64r
					; gravis_18079:loc_18088w ...
irq_number_0	db 0			; DATA XREF: gravis_init+35w
					; gravis_init+59w ...
byte_2462B	db 0			; DATA XREF: gravis_init+38w
					; gravis_init+61w ...
dma_channel_0	db 0			; DATA XREF: mod_readfile_11F4E+8Er
					; volume_prep+43r ...
byte_2462D	db 0			; DATA XREF: gravis_init+41w
					; gravis_init+6Dw ...
off_2462E	dw a070295122642	; DATA XREF: sub_13044+1Bw
					; sub_13044+2Ew ...
					; "07/02/95 12:26:42"
word_24630	dw 0			; DATA XREF: clean_11C43+32w
					; mod_readfile_11F4E+EDr ...
word_24632	dw 0			; DATA XREF: gravis_int+DEr
					; nongravis_182E7+4Dw
word_24634	dw 0			; DATA XREF: gravis_int+D8r
					; nongravis_182E7+45w
word_24636	dw 0			; DATA XREF: gravis_int+B5r
					; gravis_int+D1w ...
freq2		dw 0			; DATA XREF: read_sndsettings+2Cr
					; gravis_18079+1Dw
		db    0
byte_2463B	db 0			; DATA XREF: gravis_init+Fw
					; gravis_init+1Bw ...
dword_2463C	dd 0			; DATA XREF: someplaymode+8Aw
					; gravis_13215+2Ar
dword_24640	dd 0			; DATA XREF: memfree_125DA+13w
					; volume_prep+4Dw ...
		db    0
byte_24645	db 0			; DATA XREF: sub_182DB+5w
					; nongravis_182E7+Cw ...
word_24646	dw 0			; DATA XREF: proaud_init:loc_145A6w
sound_port	dw 0			; DATA XREF: proaud_init+42w
					; proaud_init+90r ...
byte_2464A	db 0			; DATA XREF: proaud_init+6Aw
					; proaud_init+9Br ...
byte_2464B	db 0			; DATA XREF: proaud_init+64w
					; proaud_set+11r ...
base_port2	dw 0			; DATA XREF: wss_init:loc_147C3w
					; wss_init+75r	...
dma_channel2	db 0			; DATA XREF: wss_init:loc_147DCw
					; wss_init:loc_14801r ...
irq_number2	db 0			; DATA XREF: wss_init:loc_147D0w
					; wss_init+41r	...
byte_24650	db 0			; DATA XREF: wss_set+54w wss_sndoff+4r
byte_24651	db 0			; DATA XREF: wss_set+61w wss_sndoff+Cr
sb_base_port	dw 0			; DATA XREF: sb16_on+17r sb16_on+44r ...
word_24654	dw 0			; DATA XREF: sb16_detect_port+78w
off_24656	dw a070295122642	; DATA XREF: sub_13044+21w
					; sub_13044+34w ...
					; "07/02/95 12:26:42"
dma_chn_mask	db 0			; DATA XREF: sb16_init+4Bw
					; sb16_init:loc_14AF5w	...
sb_irq_number	db 0			; DATA XREF: sb16_init+1Cw
					; sb16_init:loc_14AB3w	...
sb_timeconst	db 0			; DATA XREF: sbpro_init+51w sb_set-D1r ...
word_2465C	dw 0			; DATA XREF: snd_initialze:loc_15302w
					; midi_153F1r ...
freq1		dw 22050		; DATA XREF: volume_prepare_waves+48r
					; someplaymode+49r ...
fhandle_module	dw 0			; DATA XREF: moduleread+19w
					; moduleread:loc_1006Br ...
word_24662	dw 0			; DATA XREF: moduleread:loc_1002Dw
					; moduleread+73w ...
byte_24664	db 0			; DATA XREF: sb_set-FFw
					; sbpro_sndoff+1Dr
byte_24665	db 0			; DATA XREF: moduleread:loc_10064w
					; memfree_125DA:loc_125F6r
byte_24666	db 0			; DATA XREF: sub_1265D+18r
					; sub_13CF6+2w
byte_24667	db 0			; DATA XREF: sub_1265D+1Dr
					; eff_13CE8+4w	...
byte_24668	db 0			; DATA XREF: sub_12EBA+71w
					; sub_12F56+1Aw ...
byte_24669	db 0			; DATA XREF: sub_12EBA+9w sub_12F56+Cw ...
byte_2466A	db 0			; DATA XREF: sub_12EBA+Ew
					; eff_13B06+5Aw ...
byte_2466B	db 0			; DATA XREF: sub_12EBA+13w
					; eff_13C02+25w ...
byte_2466C	db 0			; DATA XREF: sub_12EBA+18w
					; eff_13CC9+10w ...
byte_2466D	db 0			; DATA XREF: sub_12EBA+1Dw
					; eff_13CC9+7r	...
byte_2466E	db 0			; DATA XREF: mod_readfile_11F4E:loc_1212Br
					; volume_prep:loc_1276Cr ...
dma_mode	db 0			; DATA XREF: proaud_set+3w wss_set+3w	...
sb_int_counter	db 0			; DATA XREF: sb_test_interruptw
					; sb_test_interrupt:loc_184B0r	...
byte_24671	db 0			; DATA XREF: sub_1265D+3Ar
					; sub_12EBA+22w ...
flag_playsetttings db 0			; DATA XREF: clean_11C43+68r
					; get_playsettings+6r ...
byte_24673	db 0			; DATA XREF: s3m_module+14w
					; s3m_module+2Bw ...
byte_24674	db 0			; DATA XREF: mod_readfile_11F4E+32w
					; mod_readfile_11F4E+BFw ...
byte_24675	db 0			; DATA XREF: mod_readfile_11F4E+2Aw
					; mod_readfile_11F4E+B7w ...
byte_24676	db 0			; DATA XREF: mod_sub_12220:loc_12228r
					; mod_sub_12220+23w
byte_24677	db 0			; DATA XREF: midi_15413+4r
					; midi_15413+Aw
byte_24678	db 0			; DATA XREF: midi_15413+2Aw
byte_24679	db 0			; DATA XREF: _2stm_module+31w
					; s3m_module+EFw ...
byte_2467A	db 0			; DATA XREF: _2stm_module+35w
					; s3m_module+F5w ...
byte_2467B	db 0			; DATA XREF: faar_module+2Cw
					; sub_12EBA+7Fw ...
byte_2467C	db 0			; DATA XREF: faar_module+2Fw
					; sub_12EBA+82w ...
byte_2467D	db 0			; DATA XREF: sub_13044:loc_1305Aw
					; sub_13044:loc_1306Dw	...
byte_2467E	db 0			; DATA XREF: s3m_module+Fw
					; e669_module+1Fw ...
play_state	db 0			; DATA XREF: getset_playstate+Bw
					; getset_playstate:loc_12CA7r ...
snd_init	db 0			; DATA XREF: sub_12D05+Br
					; snd_initialzer ...
snd_set_flag	db 0			; DATA XREF: sub_12DA8+60w snd_on+7r ...
byte_24682	db 0			; DATA XREF: sub_16C69:loc_16C88w
					; sub_16C69+3Fr ...
byte_24683	db 0			; DATA XREF: sub_154F4+6w
					; sub_1609F:loc_15698r	...
dword_24684	dd 0			; DATA XREF: alloc_dma_bufw
					; alloc_dma_buf+22r ...
		db    0
word_2468C	dw 0			; DATA XREF: alloc_dma_buf:loc_18A0Aw
					; alloc_dma_buf+B5r
		align 10h
		db    0
algn_24691:
dword_24694	dd 0			; DATA XREF: dma_186E3+5Dr
					; dma_186E3+A2r ...
myseg_24698	dw 0			; DATA XREF: alloc_dma_buf+31w
					; alloc_dma_buf+A6r ...
memflg_2469A	db 0			; DATA XREF: alloc_dma_buf+8w
					; alloc_dma_buf+B0w ...
byte_2469B	db 0			; DATA XREF: alloc_dma_buf+Dw
byte_2469C	db 0			; DATA XREF: alloc_dma_buf+4w
					; alloc_dma_buf+3Br
		db 0
ems_pageframe	dw 0			; DATA XREF: useless_11787+3Er
					; ems_init+61w	...
ems_handle	dw 0			; DATA XREF: ems_init+74w
					; ems_release+Dr ...
ems_log_pagenum	dw 0			; DATA XREF: ems_init+7Dw
					; ems_release+15w ...
ems_enabled	db 0			; DATA XREF: ems_initw	ems_init+78w ...
byte_246A5	db 0			; DATA XREF: ems_save_mapctx+1Bw
					; ems_restore_mapctx+7r
word_246A6	dw 0			; DATA XREF: sub_12CAD+9o
					; sub_12CAD+18w
byte_246A8	db 0			; DATA XREF: sub_12CAD+14w
word_246A9	dw 0			; DATA XREF: sub_12CAD+10w
module_type_text dd 20202020h		; DATA XREF: mod_n_t_modulew
					; mod_n_t_module:mod_flt8_modulew ...
; char asc_246B0[32]
asc_246B0	db '                                ' ; DATA XREF: mod_1021E+22o
					; _2stm_module+47o ...
moduleflag_246D0 dw 0			; DATA XREF: mod_n_t_module+3Dw
					; mod_read_10311+12r ...
sndcard_type	db 0			; DATA XREF: mtm_module+2Er
					; faar_module+3Fr ...
snd_base_port	dw 0			; DATA XREF: read_sndsettings+9r
					; useless_12D61+9w ...
irq_number	db 0			; DATA XREF: read_sndsettings+Dr
					; useless_12D61+Cw ...
dma_channel	db 0			; DATA XREF: read_sndsettings+11r
					; useless_12D61+Fw ...
freq_246D7	db 0			; DATA XREF: read_sndsettings+15r
					; sub_12DA8+17w ...
byte_246D8	db 0			; DATA XREF: read_sndsettings+19r
					; useless_12D61+12w ...
byte_246D9	db 0			; DATA XREF: read_sndsettings+1Dr
					; useless_12D61+15w ...
config_word	dw 0			; DATA XREF: ems_init+8r
					; read_sndsettings:loc_12CFFr ...
byte_246DC	db 0			; DATA XREF: sub_12DA8+33w
					; sub_12DA8+88r
word_246DE	dw 6B00h,6500h,5F40h,5A00h,54C0h,5000h,4B80h,4740h,4340h
					; DATA XREF: sub_13826+42o
					; sub_13826:loc_1386Cr
		dw 3F80h,3C00h,38A0h
table_246F6	dw 8363,8422,8482,8543,8604,8667,8730,8794,7901,7954,8007
					; DATA XREF: eff_13BC8+21r
		dw 8062,8116,8191,8231,8305
table_24716	dw 8000h,9000h,0A000h,0A952h,0B000h,0B521h,0B952h,0BCDEh
					; DATA XREF: sub_13044+41o
		dw 0C000h,0C2B5h,0C521h,0C752h,0C952h,0CB29h,0CCDEh,0CE74h
		dw 0D000h,0D164h,0D2B5h,0D3F3h,0D521h,0D640h,0D752h,0D858h
		dw 0D952h,0DA42h,0DB29h,0DC07h,0DCDEh,0DDACh,0DE74h,0DF35h
		dw 0E000h,0E0B5h,0E164h,0E20Fh,0E2B5h,0E356h,0E3F3h,0E48Ch
		dw 0E521h,0E5B2h,0E640h,0E6CBh,0E752h,0E7D6h,0E858h,0E8D6h
		dw 0E952h,0E9CCh,0EA42h,0EAB7h,0EB29h,0EB99h,0EC07h,0EC73h
		dw 0ECDEh,0ED46h,0EDACh,0EE11h,0EE74h,0EED5h,0EF35h,0EF93h
		dw 0EFF0h
table_24798	dw 8000h,9800h,0A000h,0A800h,0B000h,0B400h,0B800h,0BC00h
					; DATA XREF: sub_13044+1Bo
		dw 0C000h,0C200h,0C400h,0C600h,0C800h,0CA00h,0CC00h,0CE00h
		dw 0D000h,0D100h,0D200h,0D300h,0D400h,0D500h,0D600h,0D700h
		dw 0D800h,0D900h,0DA00h,0DB00h,0DC00h,0DD00h,0DE00h,0DF00h
		dw 0E080h,0E100h,0E180h,0E200h,0E280h,0E300h,0E380h,0E400h
		dw 0E480h,0E500h,0E580h,0E600h,0E680h,0E700h,0E780h,0E800h
		dw 0E880h,0E900h,0E980h,0EA00h,0EA80h,0EB00h,0EB80h,0EC00h
		dw 0EC80h,0ED00h,0ED80h,0EE00h,0EE80h,0EF00h,0EF80h,0EFF0h
table_24818	dw 8000h,9800h,0A000h,0A800h,0B000h,0B400h,0B800h,0BC00h
					; DATA XREF: sub_13044+2Eo
		dw 0C000h,0C200h,0C400h,0C600h,0C800h,0CA00h,0CC00h,0CE00h
		dw 0D000h,0D100h,0D200h,0D300h,0D400h,0D500h,0D600h,0D700h
		dw 0D800h,0D900h,0DA00h,0DB00h,0DC00h,0DD00h,0DE00h,0DF00h
		dw 0E080h,0E100h,0E180h,0E200h,0E280h,0E300h,0E380h,0E400h
		dw 0E480h,0E500h,0E580h,0E600h,0E680h,0E700h,0E780h,0E800h
		dw 0E880h,0E900h,0E980h,0EA00h,0EA80h,0EB00h,0EB80h,0EC00h
		dw 0EC80h,0ED00h,0ED80h,0EE00h,0EE80h,0EF00h,0EF80h,0EFF0h
table_24898	db 1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh
					; DATA XREF: seg000:512Do
		db 1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Dh,1Dh,1Dh,1Dh,1Dh,1Dh,1Dh,1Dh,1Dh,1Dh
		db 1Dh,1Dh,1Dh,1Dh,1Dh,1Dh,1Dh,1Dh,1Dh,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch
		db 1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch
		db 1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Ch,1Bh,1Bh,1Bh,1Bh,1Bh,1Bh,1Bh,1Bh,1Bh
		db 1Bh,1Bh,1Bh,1Bh,1Bh,1Bh,1Bh,1Bh,1Bh,1Ah,1Ah,1Ah,1Ah,1Ah,1Ah,1Ah
		db 1Ah,1Ah,19h,19h,19h,19h,19h,19h,19h,18h,18h,18h,18h,17h,17h,17h
		db 17h,16h,16h,15h,15h,14h,14h,13h,13h,13h,12h,12h,11h,11h,10h,10h
		db 0Fh,0Fh,0Eh,0Eh,0Dh,0Dh,0Ch,0Ch,0Bh,0Bh,0Ah,0Ah,0Ah,9,9,8
		db 8,8,8,7,7,7,7,6,6,6,6,6,6,5,5,5
		db 5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4
		db 4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3
		db 3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2
		db 2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2
		db 2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
		db 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
word_24998	dw 6B00h,6500h,5F40h,5A00h,54C0h,5000h,4B80h,4740h,4340h
					; DATA XREF: sub_13623+D2o
					; eff_13BC8+18o
		dw 3F80h,3C00h,38A0h,3580h,3280h,2FA0h,2D00h,2A60h,2800h
		dw 25C0h,23A0h,21A0h,1FC0h,1E00h,1C50h,1AC0h,1940h,17D0h
		dw 1680h,1530h,1400h,12E0h,11D0h,10D0h,0FE0h,0F00h,0E20h
		dw 0D60h,0CA0h,0BE0h,0B40h,0AA0h,0A00h,970h,8F0h,870h
		dw 7F0h,780h,710h,6B0h,650h,5F0h,5A0h,550h,500h,4B0h,470h
		dw 430h,3F0h,3C0h,380h,6A40h,6440h,5EA0h,5960h,5440h,4FA0h
		dw 4B20h,46E0h,42E0h,3F20h,3BA0h,3840h,3520h,3220h,2F50h
		dw 2CB0h,2A20h,27D0h,2590h,2370h,2170h,1F90h,1DD0h,1C20h
		dw 1A90h,1910h,17B0h,1650h,1510h,13E0h,12C0h,11C0h,10C0h
		dw 0FD0h,0EF0h,0E10h,0D50h,0C90h,0BD0h,0B30h,0A90h,9F0h
		dw 960h,8E0h,860h,7E0h,770h,710h,6A0h,640h,5E0h,590h,540h
		dw 4F0h,4B0h,470h,430h,3F0h,3B0h,380h,6980h,6380h,5E00h
		dw 58A0h,53C0h,4F00h,4AA0h,4660h,4280h,3EC0h,3B40h,37E0h
		dw 34C0h,31C0h,2F00h,2C50h,29E0h,2780h,2550h,2330h,2140h
		dw 1F60h,1DA0h,1BF0h,1A60h,18E0h,1780h,1630h,14F0h,13C0h
		dw 12A0h,11A0h,10A0h,0FB0h,0ED0h,0E00h,0D30h,0C70h,0BC0h
		dw 0B10h,0A70h,9E0h,950h,8D0h,850h,7D0h,760h,700h,690h
		dw 630h,5E0h,580h,530h,4F0h,4A0h,460h,420h,3E0h,3B0h,380h
		dw 68C0h,62E0h,5D40h,5800h,5320h,4E80h,4A00h,45E0h,4200h
		dw 3E40h,3AC0h,3780h,3460h,3170h,2EA0h,2C00h,2990h,2740h
		dw 2500h,22F0h,2100h,1F20h,1D60h,1BC0h,1A30h,18B0h,1750h
		dw 1600h,14C0h,13A0h,1280h,1180h,1080h,0F90h,0EB0h,0DE0h
		dw 0D10h,0C60h,0BB0h,0B00h,0A60h,9D0h,940h,8C0h,840h,7D0h
		dw 760h,6F0h,680h,630h,5D0h,580h,530h,4E0h,4A0h,460h,420h
		dw 3E0h,3B0h,370h,6800h,6220h,5CA0h,5760h,5280h,4DE0h
		dw 4980h,4560h,4180h,3DE0h,3A60h,3720h,3400h,3110h,2E50h
		dw 2BB0h,2940h,26F0h,24C0h,22B0h,20C0h,1EF0h,1D30h,1B90h
		dw 1A00h,1880h,1720h,15E0h,14A0h,1380h,1260h,1160h,1060h
		dw 0F70h,0E90h,0DC0h,0D00h,0C40h,0B90h,0AF0h,0A50h,9C0h
		dw 930h,8B0h,830h,7C0h,750h,6E0h,680h,620h,5C0h,570h,520h
		dw 4E0h,490h,450h,410h,3E0h,3A0h,370h,6740h,6160h,5C00h
		dw 56C0h,51E0h,4D60h,4900h,44E0h,4100h,3D60h,39E0h,36A0h
		dw 33A0h,30B0h,2E00h,2B60h,28F0h,26B0h,2480h,2270h,2080h
		dw 1EB0h,1CF0h,1B50h,19D0h,1860h,1700h,15B0h,1480h,1350h
		dw 1240h,1140h,1040h,0F50h,0E80h,0DB0h,0CE0h,0C30h,0B80h
		dw 0AE0h,0A40h,9B0h,920h,8A0h,820h,7B0h,740h,6D0h,670h
		dw 610h,5C0h,570h,520h,4D0h,490h,450h,410h,3D0h,3A0h,360h
		dw 6680h,60C0h,5B40h,5620h,5160h,4CC0h,4880h,4460h,4080h
		dw 3CE0h,3980h,3640h,3340h,3060h,2DA0h,2B10h,28B0h,2660h
		dw 2440h,2230h,2040h,1E70h,1CC0h,1B20h,19A0h,1830h,16D0h
		dw 1590h,1450h,1330h,1220h,1120h,1020h,0F40h,0E60h,0D90h
		dw 0CD0h,0C10h,0B70h,0AC0h,0A30h,9A0h,910h,890h,810h,7A0h
		dw 730h,6D0h,660h,600h,5B0h,560h,510h,4D0h,480h,440h,400h
		dw 3D0h,390h,360h,65C0h,6000h,5AA0h,5580h,50C0h,4C40h
		dw 47E0h,43E0h,4020h,3C80h,3920h,35E0h,32E0h,3000h,2D50h
		dw 2AC0h,2860h,2620h,23F0h,21F0h,2010h,1E40h,1C90h,1AF0h
		dw 1970h,1800h,16B0h,1560h,1430h,1310h,1200h,1100h,1000h
		dw 0F20h,0E40h,0D80h,0CC0h,0C00h,0B50h,0AB0h,0A10h,980h
		dw 900h,880h,800h,790h,720h,6C0h,660h,600h,5A0h,550h,500h
		dw 4C0h,480h,440h,400h,3C0h,390h,360h,7160h,6B00h,6500h
		dw 5F40h,5A00h,54C0h,5000h,4B80h,4740h,4340h,3F80h,3C00h
		dw 38B0h,3580h,3280h,2FA0h,2D00h,2A60h,2800h,25C0h,23A0h
		dw 21A0h,1FC0h,1E00h,1C50h,1AC0h,1940h,17D0h,1680h,1530h
		dw 1400h,12E0h,11D0h,10D0h,0FE0h,0F00h,0E20h,0D60h,0CA0h
		dw 0BE0h,0B40h,0AA0h,0A00h,970h,8F0h,870h,7F0h,780h,710h
		dw 6B0h,650h,5F0h,5A0h,550h,500h,4B0h,470h,430h,3F0h,3C0h
		dw 7080h,6A40h,6440h,5EA0h,5960h,5460h,4F80h,4B20h,46E0h
		dw 42E0h,3F20h,3BA0h,3840h,3520h,3220h,2F50h,2CB0h,2A30h
		dw 27C0h,2590h,2370h,2170h,1F90h,1DD0h,1C20h,1A90h,1910h
		dw 17B0h,1650h,1510h,13E0h,12C0h,11C0h,10C0h,0FD0h,0EE0h
		dw 0E10h,0D40h,0C80h,0BD0h,0B30h,0A90h,9F0h,960h,8E0h
		dw 860h,7E0h,770h,700h,6A0h,640h,5E0h,590h,540h,4F0h,4B0h
		dw 470h,430h,3F0h,3B0h,6FC0h,6980h,6380h,5E00h,58A0h,53C0h
		dw 4F00h,4AA0h,4660h,4280h,3EC0h,3B40h,37E0h,34C0h,31C0h
		dw 2F00h,2C50h,29E0h,2780h,2550h,2330h,2140h,1F60h,1DA0h
		dw 1BF0h,1A60h,18E0h,1780h,1630h,14F0h,13C0h,12A0h,11A0h
		dw 10A0h,0FB0h,0ED0h,0DF0h,0D30h,0C70h,0BC0h,0B10h,0A70h
		dw 9E0h,950h,8D0h,850h,7D0h,760h,6F0h,690h,630h,5E0h,580h
		dw 530h,4F0h,4A0h,460h,420h,3E0h,3B0h,6EE0h,68C0h,62E0h
		dw 5D40h,5800h,5320h,4E80h,4A00h,45E0h,4200h,3E40h,3AC0h
		dw 3770h,3460h,3170h,2EA0h,2C00h,2990h,2740h,2500h,22F0h
		dw 2100h,1F20h,1D60h,1BC0h,1A30h,18B0h,1750h,1600h,14C0h
		dw 13A0h,1280h,1180h,1080h,0F90h,0EB0h,0DE0h,0D10h,0C60h
		dw 0BB0h,0B00h,0A60h,9D0h,940h,8C0h,840h,7D0h,760h,6F0h
		dw 680h,630h,5D0h,580h,530h,4E0h,4A0h,460h,420h,3E0h,3B0h
		dw 6E20h,6800h,6220h,5CA0h,5760h,5280h,4DE0h,4980h,4560h
		dw 4180h,3DC0h,3A60h,3710h,3400h,3110h,2E50h,2BB0h,2940h
		dw 26F0h,24C0h,22B0h,20C0h,1EE0h,1D30h,1B90h,1A00h,1880h
		dw 1720h,15E0h,14A0h,1380h,1260h,1160h,1060h,0F70h,0E90h
		dw 0DC0h,0D00h,0C40h,0B90h,0AF0h,0A50h,9C0h,930h,8B0h
		dw 830h,7B0h,750h,6E0h,680h,620h,5C0h,570h,520h,4E0h,490h
		dw 450h,410h,3D0h,3A0h,6D60h,6740h,6160h,5C00h,56C0h,51E0h
		dw 4D60h,4900h,44E0h,4100h,3D60h,39E0h,36B0h,33A0h,30B0h
		dw 2E00h,2B60h,28F0h,26B0h,2480h,2270h,2080h,1EB0h,1CF0h
		dw 1B50h,19D0h,1860h,1700h,15B0h,1480h,1350h,1240h,1140h
		dw 1040h,0F50h,0E80h,0DB0h,0CE0h,0C30h,0B80h,0AE0h,0A40h
		dw 9B0h,920h,8A0h,820h,7B0h,740h,6D0h,670h,610h,5C0h,570h
		dw 520h,4D0h,490h,450h,410h,3D0h,3A0h,6C80h,6680h,60C0h
		dw 5B40h,5620h,5160h,4CC0h,4880h,4460h,4080h,3CE0h,3980h
		dw 3640h,3340h,3060h,2DA0h,2B10h,28B0h,2660h,2440h,2230h
		dw 2040h,1E70h,1CC0h,1B20h,19A0h,1830h,16D0h,1590h,1450h
		dw 1330h,1220h,1120h,1020h,0F40h,0E60h,0D90h,0CD0h,0C10h
		dw 0B70h,0AC0h,0A30h,9A0h,910h,890h,810h,7A0h,730h,6C0h
		dw 660h,600h,5B0h,560h,510h,4D0h,480h,440h,400h,3D0h,390h
		dw 6BC0h,65C0h,6000h,5AA0h,5580h,50C0h,4C40h,47E0h,43E0h
		dw 4020h,3C80h,3920h,35E0h,32E0h,3000h,2D50h,2AC0h,2860h
		dw 2620h,23F0h,21F0h,2010h,1E40h,1C90h,1AF0h,1970h,1800h
		dw 16B0h,1560h,1430h,1310h,1200h,1100h,1000h,0F20h,0E40h
		dw 0D80h,0CB0h,0C00h,0B50h,0AB0h,0A10h,980h,900h,880h
		dw 800h,790h,720h,6C0h,650h,600h,5A0h,550h,500h,4C0h,480h
		dw 440h,400h,3C0h,390h
table_25118	dw 1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906,856,808,762,720,678,640,604,570,538,508,480,453
					; DATA XREF: mod_read_10311:loc_10399r
		dw 428,404,381,360,339,320,302,285,269,254,240,226,214,202,190,180,170,160,151,143,135,127,120,113
		dw 107,101,95,90,85,80,75,71,67,63,60,56,53,50,47,45,42,40,37,35,33,31,30,28
		dw 26,25,23,22,21,20,18,17,16,15,15,14
table_251C0	db  0,18h,31h,4Ah,61h,78h,8Dh,0A1h,0B4h,0C5h,0D4h,0E0h
					; DATA XREF: eff_1392F+4Er
					; eff_139B9+4Fr
		db 0EBh,0F4h,0FAh,0FDh,0FFh,0FDh,0FAh,0F4h,0EBh,0E0h,0D4h
		db 0C5h,0B4h,0A1h,8Dh,78h,61h,4Ah,31h,18h
table_251E0	db  0,15h,20h,29h,30h,37h,3Dh,44h,49h,4Fh,54h,59h,5Eh
					; DATA XREF: sub_13044+47o
		db 62h,67h,6Bh,6Fh,73h,77h,7Ch,7Fh,83h,86h,8Ah,8Eh,91h
		db 95h,98h,9Bh,9Fh,0A2h,0A5h,0A9h,0ABh,0AFh,0B3h,0B5h
		db 0B8h,0BBh,0BEh,0C1h,0C3h,0C6h,0C9h,0CCh,0CFh,0D1h,0D4h
		db 0D7h,0DAh,0DDh,0DFh,0E2h,0E5h,0E7h,0EAh,0ECh,0EFh,0F1h
		db 0F4h,0F6h,0F9h,0FBh,0FEh,0FFh
table_25221	db  0, 4, 8,0Ch,10h,14h,18h,1Ch,20h,24h,28h,2Ch,30h,34h
					; DATA XREF: sub_13044+21o
		db 38h,3Ch,40h,44h,48h,4Ch,50h,55h,59h,5Dh,61h,65h,69h
		db 6Dh,71h,75h,79h,7Dh,81h,85h,89h,8Dh,91h,95h,99h,9Dh
		db 0A1h,0A5h,0AAh,0AEh,0B2h,0B6h,0BAh,0BEh,0C2h,0C6h,0CAh
		db 0CEh,0D2h,0D6h,0DAh,0DEh,0E2h,0E6h,0EAh,0EEh,0F2h,0F6h
		db 0FAh,0FFh
table_25261	db  0, 4, 8,0Ch,10h,14h,18h,1Ch,20h,24h,28h,2Ch,30h,34h
					; DATA XREF: sub_13044+34o
		db 38h,3Ch,40h,44h,48h,4Ch,50h,54h,58h,5Ch,60h,64h,68h
		db 6Ch,70h,74h,78h,7Ch,80h,84h,88h,8Ch,90h,94h,98h,9Ch
		db 0A0h,0A4h,0A8h,0ACh,0B0h,0B4h,0B8h,0BCh,0C0h,0C4h,0C8h
		db 0CCh,0D0h,0D4h,0D8h,0DCh,0E0h,0E4h,0E8h,0ECh,0F0h,0F4h
		db 0F8h,0FFh, 0
		dw sb16_init
		dw covox_init
		dw stereo_init
		dw adlib_init
		dw pcspeaker_init
		dw midi_init
		dw sb16_on
		dw covox_set
		dw stereo_set
		dw adlib_set
		dw pcspeaker_set
		dw midi_set
		dw sb16_off
		dw covox_sndoff
		dw stereo_sndoff
		dw adlib_sndoff
		dw pcspeaker_sndoff
		dw midi_sndoff
		dw sb16_deinit
		dw covox_clean
		dw stereo_clean
		dw adlib_clean
		dw pcspeaker_clean
		dw midi_clean
snd_cards_offs	dw aGravisUltrasoun ; DATA XREF:	seg003:114Eo
					; seg003:1194o	...
					; "Gravis UltraSound"
		dw aProAudioSpectrum ; "Pro Audio Spectrum 16"
		dw aWindowsSoundSyst ; "Windows Sound System"
		dw aSoundBlaster1616 ; "Sound Blaster 16/16ASP"
		dw aSoundBlasterPro ; "Sound Blaster Pro"
		dw aSoundBlaster_0 ; "Sound Blaster"
		dw aCovox_0	; "Covox"
		dw aStereoOn1_0	; "Stereo-On-1"
		dw aAdlibSoundcard_0 ; "Adlib SoundCard"
		dw aPcHonker_0	; "PC Honker"
		dw aGeneralMidi_0 ; "General MIDI"
		dw sb16_txt
		dw sb16_txt
		dw sb16_txt
		dw sb16_txt
		dw sb16_txt
		dw covox_txt
		dw covox_txt
		dw pcspeaker_text
		dw pcspeaker_text
		dw midi_txt
off_25326	dw inr_module	; DATA XREF: moduleread:loc_10040o
					; INR
		db    0
		db    0
		db 16
aInertiaModule_1 db 'Inertia Module: '
		dw mod_mk_module
		db  38h	; 8
		db    4
		db    4
aM_k_		db 'M.K.'
		dw mod_mk_module
		db  38h	; 8
		db    4
		db    4
a_m_k		db '.M.K'
		dw mod_mk_module
		db  38h	; 8
		db    4
		db    4
aMK		db 'M&K!'
		dw mod_mk_module
		db  38h	; 8
		db    4
		db    4
aMK_0		db 'M!K!'
		dw mod_mk_module
		db  38h	; 8
		db    4
		db    4
aGsft		db 'GSFT'
		dw mod_mk_module
		db  38h	; 8
		db    4
		db    4
aE_g_		db 'E.G.'
		dw mod_mk_module
		db  38h	; 8
		db    4
		db    4
aFlt4		db 'FLT4'
		dw mod_flt8_module ; FLT8
		db  38h	; 8
		db    4
		db    4
aFlt8		db 'FLT8'
		dw mod_cd81_module
		db  38h	; 8
		db    4
		db    4
aCd81		db 'CD81'
		dw mod_cd81_module
		db  38h	; 8
		db    4
		db    4
aOcta		db 'OCTA'
		dw mod_chn_module
		db  39h	; 9
		db    4
		db    3
aChn		db 'CHN'
		dw mod_ch_module
		db  3Ah	; :
		db 4
		db    2
aCh		db 'CH'
		dw mod_tdz_module
		db  38h	; 8
		db    4
		db    3
aTdz		db 'TDZ'
		dw stm_module	; STM
		db  14h
		db    0
		db    8
aScream		db '!Scream!'
		dw _2stm_module	; 2STM
		db  14h
		db    0
		db    8
aBmod2stm	db 'BMOD2STM'
		dw s3m_module	; S3M
		db  2Ch	; ,
		db    0
		db    4
aScrm		db 'SCRM'
		dw mtm_module	; MTM
		db    0
		db    0
		db    3
aMtm		db 'MTM'
		dw psm_module	; PSM
		db    0
		db    0
		db    4
aPsm		db 'PSM˛'
		dw faar_module	; FAR
		db    0
		db    0
		db    4
aFar		db 'FAR˛'
		dw ult_module	; ULT
		db    0
		db    0
		db  0Ch
aMas_utrack_v	db 'MAS_UTrack_V'
		dw _669_module	; 669
		db    0
		db    0
		db    2
aIf		db 'if'
		dw e669_module	; E669
		db    0
		db    0
		db    2
aJn		db 'JN'
eModuleNotFound	db 'Module not found',0Dh,0Ah,0 ; DATA XREF: moduleread+1Co
aNotEnoughMemory db 'Not enough Memory available',0Dh,0Ah,0
					; DATA XREF: moduleread:loc_10099o
aNotEnoughDramOn db 'Not enough DRAM on UltraSound',0Dh,0Ah,0
					; DATA XREF: mod_readfile_11F4E+1CCo
aSomeFunctionsOf db 'Some functions of the UltraSound do not work!',0Dh,0Ah
		db 0Ah
		db 'Probably the AT-BUS Clock Speed is too high.',0Dh,0Ah
		db 'Try changing the AT-BUS Clock in the CMOS Setup.',0Dh,0Ah,0
aCouldNotFindThe db 'Could not find the ULTRASND environment string',0Dh,0Ah,0
					; DATA XREF: gravis_init:loc_1432Fo
aCouldNotFindT_0 db 'Could not find the Gravis UltraSound at the specified port addres'
		db 's',0Dh,0Ah,0
aThisProgramRequ db 'This program requires the soundcards device driver.',0Dh,0Ah,0
aErrorSoundcardN db 'Error: Soundcard not found!',0Dh,0Ah,0
					; DATA XREF: proaud_init:loc_1464Fo
					; wss_test:loc_149ACo ...
aErrorCouldNotFi db 'Error: Could not find IRQ/DMA!',0Dh,0Ah,0
aErrorCouldNot_0 db 'Error: Could not find IRQ!',0Dh,0Ah,0 ; DATA XREF: sb_detect_irq+4Co
aErrorCouldNot_1 db 'Error: Could not find DMA!',0Dh,0Ah,0 ; DATA XREF: sb_detect_irq+D6o
aDeviceNotIniti	db 'Device not initialised!',0 ; DATA XREF: sub_12D05+8o
aAt		db ' at',0              ; DATA XREF: seg003:10BFo seg003:1152o ...
aBasePort	db ' base port ',0      ; DATA XREF: seg003:10C3o seg003:1156o ...
aMixedAt	db ', mixed at ',0      ; DATA XREF: seg003:1173o seg003:11A5o ...
aKhz		db 'kHz',0              ; DATA XREF: seg003:117Bo seg003:11ADo ...
aGravisUltrasoun db 'Gravis UltraSound',0 ; DATA XREF: seg003:snd_cards_offso
					; seg003:10BBo
gravis_txt	db    1			; DATA XREF: seg003:sndcards_text_tblo
		db    0
		dw aGravisUltrasoun ; "Gravis UltraSound"
		db    1
		db    0
		dw aAt		; " at"
		db    1
		db    0
		dw aBasePort	; " base port "
		db  0Bh
		db    0
		dw snd_base_port
aHGf1Irq	db 'h, GF1-IRQ '
		db    4
		db    0
		dw irq_number
aDramDma	db ', DRAM-DMA '
		db    4
		db    0
		dw dma_channel
		db    0
aProAudioSpectrum db 'Pro Audio Spectrum 16',0 ; DATA XREF: seg003:0D5Co
aWindowsSoundSyst db 'Windows Sound System',0 ; DATA XREF: seg003:0D5Eo
aSoundBlaster1616 db 'Sound Blaster 16/16ASP',0 ; DATA XREF: seg003:0D60o
aSoundBlasterPro db 'Sound Blaster Pro',0 ; DATA XREF: seg003:0D62o
aSoundBlaster_0	db 'Sound Blaster',0    ; DATA XREF: seg003:0D64o
sb16_txt	db    2			; DATA XREF: seg003:0D72o seg003:0D74o ...
		db    0
		dw sndcard_type
		dw snd_cards_offs
		db    1
		db    0
		dw aAt		; " at"
		db    1
		db    0
		dw aBasePort	; " base port "
		db 0Bh
		db    0
		dw snd_base_port
aHIrq		db 'h, IRQ '
		db    4
		db    0
		dw irq_number
aDma		db ', DMA '
		db    4
		db    0
		dw dma_channel
		db    1
		db    0
		dw aMixedAt	; ", mixed at "
		db    4
		db    0
		dw freq_246D7
		db    1
		db    0
		dw aKhz		; "kHz"
		db    0
aCovox_0	db 'Covox',0            ; DATA XREF: seg003:0D66o
aStereoOn1_0	db 'Stereo-On-1',0      ; DATA XREF: seg003:0D68o
covox_txt	db    2			; DATA XREF: seg003:0D7Co seg003:0D7Eo
		db    0
		dw sndcard_type
		dw snd_cards_offs
		db    1
		db    0
		dw aAt		; " at"
		db    1
		db    0
		dw aBasePort	; " base port "
		db  0Bh
		db    0
		dw snd_base_port
		db 'h'
		db    1
		db    0
		dw aMixedAt	; ", mixed at "
		db    4
		db    0
		dw freq_246D7
		db    1
		db    0
		dw aKhz		; "kHz"
		db    0
aAdlibSoundcard_0 db 'Adlib SoundCard',0 ; DATA XREF: seg003:0D6Ao
aPcHonker_0	db 'PC Honker',0        ; DATA XREF: seg003:0D6Co
pcspeaker_text	db    2			; DATA XREF: seg003:0D80o seg003:0D82o
		db    0
		dw sndcard_type
		dw snd_cards_offs
		db    1
		db    0
		dw aMixedAt	; ", mixed at "
		db    4
		db    0
		dw freq_246D7
		db    1
		db    0
		dw aKhz		; "kHz"
		db    0
aGeneralMidi_0	db 'General MIDI',0     ; DATA XREF: seg003:0D6Eo
midi_txt	db    2			; DATA XREF: seg003:0D84o
		db    0
		dw sndcard_type
		dw snd_cards_offs
		db    1
		db    0
		dw aAt		; " at"
		db    1
		db    0
		dw aBasePort	; " base port "
		db  0Bh
		db    0
		dw snd_base_port
		db 'h'
		db    0
		db    0
		db    0
dword_257A0	dd 0			; DATA XREF: useless_writeinr+170w
					; inr_read_118B0+82w ...
word_257A4	dw 0			; DATA XREF: useless_writeinr+106w
					; useless_writeinr+111r ...
aInertiaModule	db 'Inertia Module: ',0 ; DATA XREF: useless_writeinr+29o
					; useless_writeinr+80o	...
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db  0Dh
		db  0Ah
		db  1Ah
unk_257D9	db    0
byte_257DA	db 10h			; DATA XREF: useless_writeinr+3Fw
byte_257DB	db 0			; DATA XREF: useless_writeinr+47w
					; inr_module+3Er
byte_257DC	db 0			; DATA XREF: useless_writeinr+4Dw
					; inr_module+44r
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
word_257E6	dw 4			; DATA XREF: useless_writeinr+53w
					; inr_module+4Ar
word_257E8	dw 0			; DATA XREF: useless_writeinr+59w
word_257EA	dw 0			; DATA XREF: useless_writeinr+5Fw
word_257EC	dw 0			; DATA XREF: useless_writeinr+65w
					; inr_module+54r
word_257EE	dw 0			; DATA XREF: useless_writeinr+6Bw
					; inr_module+5Ar
word_257F0	dw 0			; DATA XREF: useless_writeinr+71w
					; inr_module+60r
byte_257F2	db 0			; DATA XREF: useless_writeinr+77w
					; inr_module+66r
byte_257F3	db 0			; DATA XREF: useless_writeinr+7Dw
					; inr_module+6Cr
		db    0
		db    0
aInertiaModule_0 db 'Inertia Module: ',0 ; DATA XREF: useless_writeinr+23o
		times	1Fh	db 0
		db  0Dh
		db  0Ah
		db  1Ah
		db    0
		db  10h
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    4
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
aInertiaSample	db 'Inertia Sample: '   ; DATA XREF: useless_writeinr_118+11o
					; useless_writeinr_118+5Fo ...
asc_25856	db '                                ',0Dh,0Ah,1Ah
					; DATA XREF: useless_writeinr_118+21o
					; inr_read_118B0+26o
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
dword_25886	dd 0			; DATA XREF: useless_writeinr_118+59w
					; inr_read_118B0+64r
		db  10h
byte_2588B	db 0			; DATA XREF: useless_writeinr_118+4Cw
					; inr_read_118B0+58r
byte_2588C	db 0			; DATA XREF: useless_writeinr_118+46w
					; inr_read_118B0+52r
byte_2588D	db 0			; DATA XREF: useless_writeinr_118+52w
					; inr_read_118B0+5Er
word_2588E	dw 0			; DATA XREF: useless_writeinr_118+40w
					; inr_read_118B0+4Cr
		db    0
		db    0
dword_25892	dd 0			; DATA XREF: useless_writeinr_118+31w
					; inr_read_118B0+32r
dword_25896	dd 0			; DATA XREF: useless_writeinr_118+39w
					; inr_read_118B0+3Br
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
unk_258A6	db  49h	; I		; DATA XREF: useless_writeinr_118+Eo
		db  6Eh	; n
		db  65h	; e
		db  72h	; r
		db  74h	; t
		db  69h	; i
		db  61h	; a
		db  20h
		db  53h	; S
		db  61h	; a
		db  6Dh	; m
		db  70h	; p
		db  6Ch	; l
		db  65h	; e
		db  3Ah	; :
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  20h
		db  0Dh
		db  0Ah
		db  1Ah
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db  10h
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
volume_25908	times	0A00h	db 0		; DATA XREF: s3m_module+89o
					; clean_11C43+A2o ...
; char myout[152]
myout		resb 18C0h		; DATA XREF: mod_1024A+3o
					; _2stm_module+53o ...
dword_27BC8	resd	1			; DATA XREF: moduleread+8Eo
					; s3m_module:loc_1065Fw ...
dword_27BCC	resd	1			; DATA XREF: e669_module+4Ew
		resb 18h
segs_table	resw 100h		; DATA XREF: useless_writeinr+13Cr
					; inr_module+10Dw ...
myseg_size	resw 100h		; DATA XREF: useless_writeinr+117r
					; inr_module+116w ...
byte_27FE8	resb 0FFh		; DATA XREF: mod_n_t_module+55o
					; mod_1021E+15o ...
byte_280E7	resb	1			; DATA XREF: s3m_module+1F3w
byte_280E8	resb 100h		; DATA XREF: e669_module+80w
					; e669_module+97r ...
byte_281E8	resb 100h		; DATA XREF: e669_module+88w
					; psm_module+148w ...
byte_282E8	resb 20h		; DATA XREF: clean_11C43+AEo
					; clean_11C43+11Co ...
vlm_byte_table	resb 8200h	; DATA XREF: volume_prepare_waves+8Ao
					; sub_13044:loc_13091o	...
; char chrin[]
chrin		resd	1			; DATA XREF: moduleread:loc_10033o
					; moduleread:loc_10049o ...
; char myin[]
myin		resd	1			; DATA XREF: mtm_module+22o
					; psm_module+3Fo ...
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
word_30515	resw	1			; DATA XREF: ult_module+1Ar
					; ult_module+1Fw ...
; char myin_0
myin_0		resb	1			; DATA XREF: ult_module+3Ao
dword_30518	resd	1			; DATA XREF: ult_module:loc_113F8o
					; ult_module+200o
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
word_30520	resw	1			; DATA XREF: snd_off-3644r
					; snd_off-3543r
byte_30522	resb	1			; DATA XREF: mtm_module+58r
byte_30523	resb	1			; DATA XREF: mtm_module+60r
word_30524	resw	1			; DATA XREF: snd_off-3534r
byte_30526	resb	1			; DATA XREF: mtm_module:loc_10B25r
		resb	1	;
unk_30528	resb	1	;		; DATA XREF: s3m_module+102r
					; s3m_module+1D5r ...
byte_30529	resb	1			; DATA XREF: _2stm_module+38r
word_3052A	resw	1			; DATA XREF: s3m_module+D0r
					; s3m_module+225r ...
word_3052C	resw	1			; DATA XREF: s3m_module+DEr
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
word_30532	resw	1			; DATA XREF: s3m_module+24r
		resb	1	;
		resb	1	;
		resb	1	;
byte_30537	resb	1			; DATA XREF: ult_module+4Cr
; char my_in
my_in		resb	1			; DATA XREF: _2stm_module+50o
					; ult_module+46o ...
; char byte_30539
byte_30539	resb	1			; DATA XREF: s3m_module+ECr
					; ult_module+6Bo ...
byte_3053A	resb	1			; DATA XREF: s3m_module+F2r
byte_3053B	resb	1			; DATA XREF: s3m_module+4Ar
					; s3m_module+53r
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
byte_30548	resb	1			; DATA XREF: s3m_module:loc_10628r
					; s3m_module+BEr
		resb	1	;
unk_3054A	resb	1	;		; DATA XREF: mtm_module+7Bo
byte_3054B	resb	1			; DATA XREF: psm_module+21r
byte_3054C	resb	1			; DATA XREF: psm_module+27r
		resb	1	;
		resb	1	;
		resb	1	;
byte_30550	resb	1			; DATA XREF: psm_module+2Dr
		resb	1	;
word_30552	resw	1			; DATA XREF: psm_module+35r
					; faar_module+1Fr
word_30554	resw	1			; DATA XREF: psm_module+15r
					; faar_module:loc_10F6Ar
word_30556	resw	1			; DATA XREF: psm_module+Fr
		resb	1	;
		resb	1	;
dword_3055A	resd	1			; DATA XREF: psm_module+105r
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
word_30562	resw	1			; DATA XREF: psm_module+10Cr
word_30564	resw	1			; DATA XREF: psm_module+110r
dword_30566	resd	1			; DATA XREF: psm_module+55r
					; s3m_module+FFo ...
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
		resb	1	;
byte_30576	resb	1			; DATA XREF: e669_module+2Ar
byte_30577	resb	1			; DATA XREF: e669_module+32r
		resb	1	;
byte_30579	resb 21h		; DATA XREF: e669_module:loc_1096Fr
byte_3059A	resb 5Fh		; DATA XREF: psm_module+4Bo
					; psm_module+5Co
byte_305F9	resb 40h		; DATA XREF: e669_module+7Cr
byte_30639	resb	1			; DATA XREF: ult_module+169r
byte_3063A	resb	1			; DATA XREF: ult_module+172r
word_3063B	resw	1			; DATA XREF: ult_module+192o
					; ult_module:loc_113E2r ...
dword_3063D	resd	1			; DATA XREF: ult_module+225r
					; ult_read+19w	...
byte_30641	resb 28h		; DATA XREF: ult_module+22Cr
byte_30669	resb	1			; DATA XREF: faar_module+85r
byte_3066A	resb	1			; DATA XREF: faar_module+95r
byte_3066B	resb 0Eh		; DATA XREF: faar_module+AAo
					; faar_module+D9o
byte_30679	resb 65h		; DATA XREF: e669_module+84r
byte_306DE	resb 1E0h		; DATA XREF: mod_n_t_module+15o
byte_308BE	resb 4Ah		; DATA XREF: mod_n_t_module+4Fo
					; mod_n_t_module+F1o
byte_30908	resb 38h		; DATA XREF: ult_module+203o
					; ult_module+255o
byte_30940	resb	1			; DATA XREF: mod_n_t_module:mod_chn_moduler
					; mod_n_t_module+9Cr ...
unk_30941	resb	1	;		; DATA XREF: mod_n_t_module+ACr
		resb	1	;
byte_30943	resb	1			; DATA XREF: mod_n_t_module:mod_tdz_moduler
		resb 0BC4h
; char word_31508[]
word_31508	resw	1			; DATA XREF: mod_read_10311+5o
					; mod_read_10311+1Eo ...
byte_3150A	resb	1			; DATA XREF: psm_module+139r
					; faar_module+130o
		resb	1	;
byte_3150C	resb 7FCh		; DATA XREF: psm_module+150o
					; psm_module+160o
byte_31D08	resb 1800h	; DATA XREF: mod_read_10311+21o
					; mod_read_10311+2Bo
byte_33508	resb 1008h	; DATA XREF: snd_off-3632o
					; snd_off-3625o ...

; ===========================================================================

; Segment type:	Uninitialized
SEGMENT	seg004	ALIGN=1	stack	CLASS=STACK	use16
byte_34510	resb 1000h


		end
