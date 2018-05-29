Ideal
; ---------------------------------------------------------------------------

extrn _start:far
public _deinit_125B9
public sub_12d05
public _MODULEREAD
public SUB_126A9
public _READ_SNDSETTINGS
public SUB_1265D
public SUB_12EBA
public _CHANGE_VOLUME
public _CHANGE_AMPLIF
public _GET_PLAYSETTINGS
public _GET_12F7C
public SUB_12F56
public SUB_12AFD
public _SET_PLAYSETTINGS
public SUB_12CAD
public _GETSET_PLAYSTATE
public _SND_OFFX
public _MEMFREE_125DA
public _VOLUME_PREP
public SUB_12D35
public SUB_12DA8

;extrn dseg:segment

struc		struct_0 ; (sizeof=0xA)
_word_244B7	dw ?
anonymous_0	dw ?
anonymous_1	dw ?
anonymous_2	dw ?
anonymous_3	dw ?			; offset (00019050)
ends		struct_0


;
;
; Input	MD5   :	3ADEF234086ACD44430B68CC52471B0D
; Input	CRC32 :	B294245C

; File Name   :	I:\IPLAY.EXE
; Format      :	MS-DOS executable (EXE)
; Base Address:	1000h Range: 10000h-35510h Loaded length: 16308h
; Entry	Point :	1905:42

		p486

		model large

segment		dseg para public 'DATA' use16
ends		dseg
; ===========================================================================

; Segment type:	Pure code
segment		seg000 byte public 'CODE' use16
		assume cs:seg000
		assume es:nothing, ss:nothing, ds:dseg,	fs:nothing, gs:nothing

; =============== S U B	R O U T	I N E =======================================


proc		_moduleread far		; CODE XREF: _read_module+56P
					; DATA XREF: seg003:off_245C8o	...
		push	ds
		push	dx
		push	cs
		call	near ptr _snd_offx

loc_10006:
		push	cs
		call	near ptr _memfree_125DA
		pop	dx
		mov	ax, 3D00h
		int	21h		; DOS -	2+ - OPEN DISK FILE WITH HANDLE
					; DS:DX	-> ASCIZ filename
					; AL = access mode
					; 0 - read
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		mov	[_savesp_245D0],	sp
		mov	[_fhandle_module], ax
		mov	dx, offset _eModuleNotFound ; "Module not found\r\n"

loc_1001F:
		mov	ax, 0FFFFh
		jb	short _lfreaderr
		call	_ems_save_mapctx
		cld

loc_10028:
		mov	[_byte_2461B], 0

loc_1002D:
		mov	[_word_24662], 0

loc_10033:
		mov	dx, offset _chrin
		mov	cx, 1084
		call	_dosfread
		push	cs

loc_1003D:
		call	near ptr _clean_11C43

loc_10040:
		mov	bx, offset off_25326
		mov	dl, 23

loc_10045:				; CODE XREF: _moduleread+5Fj
		movzx	cx, [byte ptr bx+4]

loc_10049:
		mov	di, offset _chrin
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
		mov	ax, offset _mod_n_t_module ; N.T.

loc_10064:				; CODE XREF: _moduleread+5Bj
		mov	[_byte_24665], 1
		call	ax

loc_1006B:
		mov	bx, [_fhandle_module]
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle
		adc	[_word_24662], 0
		call	_ems_restore_mapctx

loc_1007B:
		movzx	ax, [_byte_2461B]

loc_10080:
		inc	ax
		cmp	ax, [_word_245D4]
		jbe	short loc_1008A
		mov	ax, [_word_245D4]

loc_1008A:				; CODE XREF: _moduleread+85j
		push	cs
		call	near ptr sub_12B83
		mov	si, offset _dword_27BC8
		push	cs

loc_10092:
		call	near ptr sub_12B18
		xor	ax, ax
		pop	ds
		retf
; ---------------------------------------------------------------------------

loc_10099:				; CODE XREF: _mod_n_t_module+6Dj
					; _mod_n_t_module+15Cj ...
		mov	dx, offset _aNotEnoughMemory ; "Not enough Memory available\r\n"
		mov	ax, 0FFFEh

_lfreaderr:				; CODE XREF: _moduleread+22j
					; _dosseek+18j ...
		push	ax
		push	dx
		mov	bx, [_fhandle_module]
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle
		call	_ems_restore_mapctx
		push	cs
		call	near ptr _memfree_125DA
		mov	ax, ds
		mov	fs, ax
		assume fs:seg003
		pop	dx
		pop	ax
		mov	sp, [_savesp_245D0]
		pop	ds
		stc
		retf
endp		_moduleread


; =============== S U B	R O U T	I N E =======================================

; N.T.

proc		_mod_n_t_module near	; DATA XREF: _moduleread+61o
		mov	[_module_type_text], 2E542E4Eh
		mov	[_word_245D2], 0Fh
		mov	[_word_245D4], 4
		mov	si, offset _byte_306DE
		call	_mod_1021E
		call	_mod_102F5
		mov	dx, 258h
		xor	cx, cx
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		adc	[_word_24662], 0
		jmp	loc_101B7
; ---------------------------------------------------------------------------

_mod_flt8_module:			; DATA XREF: seg003:0DDAo
		mov	[_module_type_text], 38544C46h ;	FLT8
		mov	[_moduleflag_246D0], 11b
		mov	[_word_245D2], 1Fh
		mov	[_word_245D4], 8
		mov	si, offset _byte_308BE
		call	_mod_1021E
		mov	si, offset _byte_27FE8
		mov	cx, 80h	; 'Ä'

loc_10118:				; CODE XREF: _mod_n_t_module+5Fj
		shr	[byte ptr si], 1
		inc	si
		dec	cx
		jnz	short loc_10118
		call	_mod_1024A
		call	_mod_102F5
		call	_mod_read_10311
		call	near ptr _mod_readfile_11F4E
		jb	loc_10099
		retn
; ---------------------------------------------------------------------------

_mod_tdz_module:				; DATA XREF: seg003:0E04o
		mov	al, [_byte_30943]
		jmp	short loc_10137
; ---------------------------------------------------------------------------

_mod_chn_module:				; DATA XREF: seg003:0DF5o
		mov	al, [_byte_30940]

loc_10137:				; CODE XREF: _mod_n_t_module+75j
		xor	ah, ah
		inc	[_word_24662]
		sub	al, 30h	; '0'
		jbe	short locret_10154
		cmp	al, 9
		ja	short locret_10154
		dec	[_word_24662]
		mov	[_word_245D2], 1Fh
		mov	[_word_245D4], ax

loc_10152:
		jmp	short loc_101A6
; ---------------------------------------------------------------------------

locret_10154:				; CODE XREF: _mod_n_t_module+82j
					; _mod_n_t_module+86j ...
		retn
; ---------------------------------------------------------------------------

_mod_ch_module:				; DATA XREF: seg003:0DFDo
		inc	[_word_24662]
		movzx	ax, [_byte_30940]
		sub	al, '0'
		jb	short locret_10154
		cmp	al, 9
		ja	short locret_10154
		imul	dx, ax,	10
		mov	al, [byte ptr unk_30941]
		sub	al, '0'
		jb	short locret_10154
		cmp	al, 9
		ja	short locret_10154
		add	ax, dx
		jz	short locret_10154
		cmp	ax, ' '
		ja	short locret_10154
		dec	[_word_24662]
		mov	[_word_245D2], 1Fh
		mov	[_word_245D4], ax
		jmp	short loc_101A6
; ---------------------------------------------------------------------------

_mod_cd81_module:			; DATA XREF: seg003:0DE3o seg003:0DECo
		mov	[_word_245D2], 1Fh
		mov	[_word_245D4], 8
		jmp	short loc_101A6
; ---------------------------------------------------------------------------

_mod_mk_module:				; DATA XREF: seg003:0D9Bo seg003:0DA4o ...
		mov	[_word_245D2], 1Fh
		mov	[_word_245D4], 4

loc_101A6:				; CODE XREF: _mod_n_t_module:loc_10152j
					; _mod_n_t_module+CDj ...
		mov	eax, [dword ptr	_byte_30940]
		mov	[_module_type_text], eax
		mov	si, offset _byte_308BE
		call	_mod_1021E
		call	_mod_102F5

loc_101B7:				; CODE XREF: _mod_n_t_module+31j
		call	_mod_1024A
		cmp	[_module_type_text], 2E4B2E4Dh ;	M.K.
		jnz	short loc_10213
		xor	dx, dx
		xor	cx, cx
		mov	bx, [_fhandle_module]
		mov	ax, 4202h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from end of file
		shl	edx, 10h
		mov	dx, ax
		push	edx
		mov	dx, 1084
		xor	cx, cx
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		pop	edx
		movzx	eax, [_word_245F2]
		shl	eax, 0Bh

loc_101F4:
		add	eax, [_dword_245C4]
		add	eax, 1084
		cmp	eax, edx
		jnz	short loc_10213
		mov	[_word_245D4], 8
		mov	[_module_type_text], 20574F57h ;	WOW

loc_10213:				; CODE XREF: _mod_n_t_module+106j
					; _mod_n_t_module+145j
		call	_mod_read_10311
		call	near ptr _mod_readfile_11F4E
		jb	loc_10099
		retn
endp		_mod_n_t_module ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_mod_1021E near		; CODE XREF: _mod_n_t_module+18p
					; _mod_n_t_module+52p ...
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		cld
		lodsb
		xor	ah, ah
		mov	[_word_245FA], ax
		lodsb
		cmp	al, 78h	; 'x'
		jb	short loc_10230
		xor	al, al

loc_10230:				; CODE XREF: _mod_1021E+Ej
		mov	[_word_245F8], ax
		mov	di, offset _byte_27FE8
		mov	cx, 20h	; ' '
		cld
		rep movsd
		mov	si, offset _chrin ; in
		mov	di, offset asc_246B0 ; out
		mov	cx, 14h		; count
		call	_copy_printable
		retn
endp		_mod_1021E


; =============== S U B	R O U T	I N E =======================================


proc		_mod_1024A near		; CODE XREF: _mod_n_t_module+61p
					; _mod_n_t_module:loc_101B7p
		mov	si, offset _chrin
		mov	di, offset _myout ; out
		mov	cx, [_word_245D2]

loc_10254:				; CODE XREF: _mod_1024A+A6j
		push	cx
		add	si, 20		; in
		mov	cx, 16h		; count
		call	_copy_printable
		sub	si, 20
		pop	cx
		movzx	edx, [word ptr si+2Ah]
		xchg	dl, dh
		shl	edx, 1
		cmp	edx, 100000h
		cmc
		adc	[_word_24662], 0
		mov	[di+20h], edx
		add	[_dword_245C4], edx
		mov	al, [si+2Ch]
		and	al, 0Fh
		mov	[di+3Eh], al
		mov	ax, [_freq_245DE]
		mov	[di+36h], ax
		mov	al, [si+2Dh]
		mov	[di+3Dh], al
		movzx	ebx, [word ptr si+2Eh]
		xchg	bl, bh
		shl	ebx, 1
		movzx	eax, [word ptr si+30h]
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

loc_102C1:				; CODE XREF: _mod_1024A+6Dj
		or	[byte ptr di+3Ch], 8
		add	eax, ebx
		cmp	eax, edx
		jbe	short loc_102DF
		mov	eax, [di+28h]
		shr	eax, 1
		add	eax, ebx
		cmp	eax, edx
		jbe	short loc_102DF

loc_102DC:				; CODE XREF: _mod_1024A+68j
					; _mod_1024A+75j
		mov	eax, edx

loc_102DF:				; CODE XREF: _mod_1024A+81j
					; _mod_1024A+90j
		dec	eax
		mov	[di+2Ch], eax
		mov	[di+24h], ebx
		add	si, 1Eh
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_10254
		retn
endp		_mod_1024A


; =============== S U B	R O U T	I N E =======================================


proc		_mod_102F5 near		; CODE XREF: _mod_n_t_module+1Bp
					; _mod_n_t_module+64p ...
		mov	si, offset _byte_27FE8
		xor	bx, bx
		mov	cx, 80h	; 'Ä'
		cld

loc_102FE:				; CODE XREF: _mod_102F5+13j
		lodsb
		and	al, 7Fh
		cmp	al, bl
		jb	short loc_10307
		mov	bl, al

loc_10307:				; CODE XREF: _mod_102F5+Ej
		dec	cx
		jnz	short loc_102FE
		inc	bl
		mov	[_word_245F2], bx
		retn
endp		_mod_102F5


; =============== S U B	R O U T	I N E =======================================


proc		_mod_read_10311 near	; CODE XREF: _mod_n_t_module+67p
					; _mod_n_t_module:loc_10213p
		mov	cx, [_word_245F2]

loc_10315:				; CODE XREF: _mod_read_10311+D5j
		push	cx
		mov	dx, offset _word_31508
		mov	cx, [_word_245D4]
		shl	cx, 8
		call	_dosfread
		test	[_moduleflag_246D0], 10b
		jz	short loc_1035C
		mov	ax, ds
		mov	es, ax
		mov	si, offset _word_31508
		mov	di, offset _byte_31D08
		mov	cx, 200h
		cld
		rep movsd
		mov	si, offset _byte_31D08
		mov	di, offset _word_31508
		mov	bx, 40h	; '@'

loc_10345:				; CODE XREF: _mod_read_10311+49j
		mov	cx, 4
		rep movsd
		add	si, 3F0h
		mov	cx, 4
		rep movsd
		sub	si, 400h
		dec	bx
		jnz	short loc_10345

loc_1035C:				; CODE XREF: _mod_read_10311+18j
		call	_memalloc12k
		mov	si, offset _word_31508
		mov	cx, 40h	; '@'

loc_10365:				; CODE XREF: _mod_read_10311+CEj
		push	cx
		mov	cx, [_word_245D4]
		xor	ch, ch

loc_1036C:				; CODE XREF: _mod_read_10311+C5j
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

loc_10399:				; CODE XREF: _mod_read_10311+74j
					; _mod_read_10311+7Cj ...
		cmp	ax, [_table_25118+bx]
		jnb	short loc_103A8
		add	bx, 2
		cmp	bx, 166
		jb	short loc_10399

loc_103A8:				; CODE XREF: _mod_read_10311+8Cj
		mov	ax, bx
		shr	ax, 1
		mov	bl, 12
		div	bl
		inc	ah
		shl	al, 4
		or	al, ah
		mov	bl, al

loc_103B9:				; CODE XREF: _mod_read_10311+6Cj
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
		mov	[byte ptr es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	short loc_10365
		call	_mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_10315
		retn
endp		_mod_read_10311


; =============== S U B	R O U T	I N E =======================================

; 2STM

proc		__2stm_module near	; DATA XREF: seg003:0E19o
		mov	[_module_type_text], 4D545332h
		jmp	short loc_103FF
; ---------------------------------------------------------------------------

_stm_module:				; DATA XREF: seg003:0E0Co
		mov	[_module_type_text], 204D5453h ;	STM

loc_103FF:				; CODE XREF: __2stm_module+9j
		mov	[_moduleflag_246D0], 1000b
		mov	[_word_245D4], 4
		mov	[_word_245D2], 1Fh
		mov	[_freq_245DE], 8448
		mov	al, 60h	; '`'
		call	sub_13E9B
		mov	[_byte_24679], ah
		mov	[_byte_2467A], al
		movzx	ax, [_byte_30529]
		mov	[_word_245F2], ax
		mov	ax, ds
		mov	es, ax
		mov	si, offset _chrin ; in
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 14h		; count
		call	_copy_printable
		mov	si, offset _my_in ; in
		mov	di, offset _myout ; out
		mov	cx, [_word_245D2]

loc_10445:				; CODE XREF: __2stm_module+E3j
		push	cx
		mov	cx, 0Ch		; count
		call	_copy_printable
		pop	cx

loc_1044D:
		movzx	eax, [word ptr si+10h]
		mov	edx, eax
		add	eax, 0Fh
		and	al, 0F0h
		cmp	eax, 100000h
		cmc
		adc	[_word_24662], 0

loc_10467:
		mov	[di+20h], eax
		add	[_dword_245C4], eax
		movzx	eax, [word ptr si+0Eh]
		shl	eax, 4
		mov	[di+38h], eax
		mov	ax, [si+18h]
		or	ax, ax
		jnz	short loc_10487
		mov	ax, [_freq_245DE]

loc_10487:				; CODE XREF: __2stm_module+97j
		mov	[di+36h], ax
		mov	al, [si+16h]
		mov	[di+3Dh], al
		movzx	ebx, [word ptr si+12h]
		mov	[di+24h], ebx
		movzx	eax, [word ptr si+14h]
		cmp	ax, 0FFFFh
		jnz	short loc_104B6
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_104C7
; ---------------------------------------------------------------------------

loc_104B6:				; CODE XREF: __2stm_module+B6j
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	[byte ptr di+3Ch], 8

loc_104C7:				; CODE XREF: __2stm_module+C9j
		add	si, 20h	; ' '
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_10445
		mov	dx, offset _byte_27FE8
		mov	cx, 80h	; 'Ä'
		mov	eax, 410h
		call	_dosseek
		mov	si, offset _byte_27FE8
		xor	ax, ax

loc_104E6:				; CODE XREF: __2stm_module+105j
		cmp	[byte ptr si], 63h ; 'c'
		jnb	short loc_104F2
		inc	ax
		inc	si
		cmp	ax, 80h	; 'Ä'
		jb	short loc_104E6

loc_104F2:				; CODE XREF: __2stm_module+FEj
		mov	[_word_245FA], ax
		mov	cx, [_word_245F2]

loc_104F9:				; CODE XREF: __2stm_module+195j
		push	cx
		mov	dx, offset _chrin
		mov	cx, 400h
		call	_dosfread
		call	_memalloc12k
		mov	si, offset _chrin
		mov	cx, 40h	; '@'

loc_1050C:				; CODE XREF: __2stm_module+18Ej
		push	cx
		mov	cx, [_word_245D4]
		xor	ch, ch

loc_10513:				; CODE XREF: __2stm_module+185j
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

loc_1052E:				; CODE XREF: __2stm_module+139j
		mov	bh, [si+1]
		shr	bh, 3
		mov	ax, [si+1]
		and	ax, 0F007h
		shr	ah, 1
		or	al, ah
		cmp	al, 40h	; '@'
		jbe	short loc_10544
		mov	al, 0FFh

loc_10544:				; CODE XREF: __2stm_module+155j
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
		mov	dl, [byte ptr cs:asc_1058C+bx] ; "\x18\v\r\n\x02\x01\x03\x04\a"
		ror	ebx, 10h

loc_10565:				; CODE XREF: __2stm_module+133j
					; __2stm_module+13Dj ...
		call	sub_11BA6
		add	si, 4
		pop	cx
		inc	ch
		cmp	ch, cl
		jb	short loc_10513
		mov	[byte ptr es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	short loc_1050C
		call	_mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_104F9
		call	near ptr _mod_readfile_11F4E
		jb	loc_10099
		retn
endp		__2stm_module ; sp-analysis failed

; ---------------------------------------------------------------------------
asc_1058C	db 0,18h,0Bh,0Dh,0Ah	; DATA XREF: __2stm_module+171r
		db 2,1,3,4,7,0

; =============== S U B	R O U T	I N E =======================================

; S3M

proc		_s3m_module near		; DATA XREF: seg003:0E26o
		mov	[_module_type_text], 204D3353h
		mov	[_moduleflag_246D0], 10000b
		mov	[_byte_2467E], 1
		mov	[_byte_24673], 80h ; 'Ä'
		mov	[_freq_245DE], 8363
		mov	[_byte_2461A], 2
		cmp	[_word_30532], 2
		jnb	short loc_105C7
		mov	[_byte_24673], 0

loc_105C7:				; CODE XREF: _s3m_module+29j
		mov	ax, ds
		mov	es, ax
		mov	si, offset _chrin ; in
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 1Ch		; count
		call	_copy_printable
		test	[byte ptr _config_word+1], 20h
		jz	short loc_1061E
		mov	dx, 64h	; 'd'
		mov	cl, [_byte_3053B]
		and	cx, 7Fh
		jz	short loc_10618
		test	[_byte_3053B], 80h
		jz	short loc_105FF
		mov	ax, 0Bh
		mul	cx
		shrd	ax, dx,	3
		sub	ax, 2
		mov	cx, ax

loc_105FF:				; CODE XREF: _s3m_module+58j
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

loc_10618:				; CODE XREF: _s3m_module+51j
					; _s3m_module+78j ...
		mov	ax, dx
		push	cs
		call	near ptr _change_amplif

loc_1061E:				; CODE XREF: _s3m_module+45j
		xor	si, si
		mov	di, offset _volume_25908
		xor	dx, dx
		mov	cx, 20h	; ' '

loc_10628:				; CODE XREF: _s3m_module+AEj
		mov	al, [_byte_30548+si]
		cmp	al, 0FFh
		jz	short loc_10640
		mov	dx, si
		shr	al, 4
		mov	ah, 1
		cmp	al, 1
		jz	short loc_1063D
		mov	ah, 0

loc_1063D:				; CODE XREF: _s3m_module+A2j
		mov	[di+1Dh], ah

loc_10640:				; CODE XREF: _s3m_module+97j
		inc	si
		add	di, 50h	; 'P'
		dec	cx
		jnz	short loc_10628
		inc	dx
		mov	[_word_245D4], dx
		mov	cx, [_word_245D4]
		xor	si, si

loc_10652:				; CODE XREF: _s3m_module+CEj
		mov	al, [_byte_2461E]
		test	[_byte_30548+si], 8
		jz	short loc_1065F
		mov	al, [_byte_2461F]

loc_1065F:				; CODE XREF: _s3m_module+C3j
		mov	[byte ptr _dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_10652
		mov	ax, [_word_3052A]
		cmp	ax, 63h	; 'c'
		jb	short loc_10672
		mov	ax, 63h	; 'c'

loc_10672:				; CODE XREF: _s3m_module+D6j
		mov	[_word_245D2], ax
		mov	ax, [_word_3052C]
		cmp	ax, 100h
		jb	short loc_10680
		mov	ax, 100h

loc_10680:				; CODE XREF: _s3m_module+E4j
		mov	[_word_245F2], ax
		mov	al, [_byte_30539]
		mov	[_byte_24679], al
		mov	al, [_byte_3053A]
		mov	[_byte_2467A], al
		mov	ax, ds
		mov	es, ax
		mov	di, offset _myout ; out
		mov	bx, (offset _dword_30566+2)
		add	bx, [word ptr unk_30528]
		movzx	ecx, [_word_245D2]

loc_106A3:				; CODE XREF: _s3m_module+1CAj
		push	bx
		push	cx
		mov	dx, offset _word_31508
		mov	cx, 50h	; 'P'
		movzx	eax, [word ptr bx]
		shl	eax, 4
		call	_dosseek
		mov	si, offset _word_31508
		xor	eax, eax
		xor	edx, edx
		cmp	[byte ptr si], 1
		jnz	short loc_106D8
		movzx	eax, [word ptr si+10h]
		mov	edx, eax
		cmp	eax, 100000h
		cmc
		adc	[_word_24662], 0

loc_106D8:				; CODE XREF: _s3m_module+12Bj
		mov	[di+20h], eax
		add	[_dword_245C4], eax
		movzx	eax, [word ptr si+0Eh]
		shl	eax, 4
		mov	[di+38h], eax
		mov	ax, [si+20h]
		or	ax, ax
		jnz	short loc_106F8
		mov	ax, [_freq_245DE]

loc_106F8:				; CODE XREF: _s3m_module+15Cj
		mov	[di+36h], ax
		mov	al, [si+1Ch]
		cmp	al, 3Fh	; '?'
		jb	short loc_10704
		mov	al, 3Fh	; '?'

loc_10704:				; CODE XREF: _s3m_module+169j
		mov	[di+3Dh], al
		test	[byte ptr si+1Fh], 1
		jnz	short loc_10720

loc_1070D:				; CODE XREF: _s3m_module+18Dj
					; _s3m_module+1A0j ...
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_1074F
; ---------------------------------------------------------------------------

loc_10720:				; CODE XREF: _s3m_module+174j
		cmp	[word ptr si+14h], 0FFFFh
		jz	short loc_1070D
		movzx	edx, [word ptr si+14h]
		mov	[di+24h], edx
		movzx	eax, [word ptr si+18h]
		or	eax, eax
		jz	short loc_1070D
		dec	eax
		jz	short loc_1070D
		mov	[di+2Ch], eax
		inc	eax
		sub	eax, [di+24h]
		mov	[di+28h], eax
		or	[byte ptr di+3Ch], 8

loc_1074F:				; CODE XREF: _s3m_module+187j
		add	si, 30h	; '0'   ; in
		mov	cx, 1Ch		; count
		call	_copy_printable
		pop	cx
		pop	bx
		add	di, 40h	; '@'
		add	bx, 2
		dec	cx
		jnz	loc_106A3
		mov	si, (offset _dword_30566+2)
		xor	di, di
		xor	bx, bx
		mov	ax, [word ptr unk_30528]
		cmp	ax, 80h	; 'Ä'
		mov	ah, al
		ja	short loc_1079A
		xor	cl, cl

loc_10778:				; CODE XREF: _s3m_module+1FFj
		mov	al, [si]
		cmp	al, 0F0h ; ''
		jnb	short loc_1078F
		mov	[_byte_27FE8+di], al
		inc	bl
		inc	di
		cmp	cl, 0F0h ; ''
		jb	short loc_1078F
		mov	[_byte_280E7+di], 0FFh

loc_1078F:				; CODE XREF: _s3m_module+1E5j
					; _s3m_module+1F1j
		mov	cl, al
		inc	si
		inc	bh
		cmp	bh, ah
		jb	short loc_10778
		jmp	short loc_107AC
; ---------------------------------------------------------------------------

loc_1079A:				; CODE XREF: _s3m_module+1DDj
					; _s3m_module+213j
		mov	al, [si]
		cmp	al, 0FFh
		jz	short loc_107AC
		mov	[_byte_27FE8+di], al
		inc	bl
		inc	di
		inc	si
		cmp	bl, ah
		jb	short loc_1079A

loc_107AC:				; CODE XREF: _s3m_module+201j
					; _s3m_module+207j
		xor	bh, bh
		mov	[_word_245FA], bx
		xor	ax, ax

loc_107B4:				; CODE XREF: _s3m_module+323j
		push	ax
		mov	bx, (offset _dword_30566+2)
		add	bx, [word ptr unk_30528]
		add	ax, [_word_3052A]
		shl	ax, 1
		add	bx, ax
		mov	dx, offset _word_31508
		mov	cx, 2
		movzx	eax, [word ptr bx]
		or	ax, ax
		jnz	short loc_107E0

loc_107D2:				; CODE XREF: _s3m_module+25Bj
		call	_memalloc12k
		mov	cx, 40h	; '@'
		xor	al, al
		cld
		rep stosb
		jmp	loc_108B1
; ---------------------------------------------------------------------------

loc_107E0:				; CODE XREF: _s3m_module+239j
		shl	eax, 4
		call	_dosseek
		mov	dx, offset _word_31508
		mov	cx, [_word_31508]
		cmp	cx, 308Fh
		jnb	short loc_107D2
		add	cx, 0Fh
		and	cl, 0F0h
		sub	cx, 2
		call	_dosfread
		call	_memalloc12k
		mov	si, offset _word_31508
		mov	cx, 40h	; '@'

loc_10809:				; CODE XREF: _s3m_module+316j
		push	cx
		lodsb
		or	al, al
		jz	loc_108A6

loc_10811:				; CODE XREF: _s3m_module+30Bj
		xor	bx, bx
		mov	ch, al
		test	ch, 20h
		jz	short loc_1082D
		mov	bx, [si]
		add	si, 2
		cmp	bl, 0FEh ; '˛'
		jnb	short loc_10826
		inc	bl

loc_10826:				; CODE XREF: _s3m_module+28Bj
		cmp	bh, 63h	; 'c'
		jbe	short loc_1082D
		xor	bh, bh

loc_1082D:				; CODE XREF: _s3m_module+281j
					; _s3m_module+292j
		mov	cl, 0FFh
		test	ch, 40h
		jz	short loc_1083E
		mov	cl, [si]
		inc	si
		cmp	cl, 40h	; '@'
		jbe	short loc_1083E
		mov	cl, 0FFh

loc_1083E:				; CODE XREF: _s3m_module+29Bj
					; _s3m_module+2A3j
		test	ch, 80h
		jz	short loc_1088D
		mov	dx, [si]
		add	si, 2
		cmp	dl, 19h
		ja	short loc_1088D
		rol	ebx, 10h
		movzx	bx, dl
		mov	dl, [cs:_s3mtable_108D6+bx]
		cmp	dl, 0FFh
		jz	short loc_10885
		cmp	dl, 0Fh
		jz	short loc_10880
		cmp	dl, 0Eh
		jnz	short loc_10887
		mov	bl, dh
		shr	bl, 4
		mov	al, [cs:_s3mtable_108F0+bx]
		cmp	al, 0FFh
		jz	short loc_10885
		shl	al, 4
		and	dh, 0Fh
		or	dh, al
		jmp	short loc_10887
; ---------------------------------------------------------------------------

loc_10880:				; CODE XREF: _s3m_module+2CAj
		cmp	dh, 20h	; ' '
		ja	short loc_10887

loc_10885:				; CODE XREF: _s3m_module+2C5j
					; _s3m_module+2DDj
		xor	dx, dx

loc_10887:				; CODE XREF: _s3m_module+2CFj
					; _s3m_module+2E7j ...
		ror	ebx, 10h
		jmp	short loc_1088F
; ---------------------------------------------------------------------------

loc_1088D:				; CODE XREF: _s3m_module+2AAj
					; _s3m_module+2B4j
		xor	dx, dx

loc_1088F:				; CODE XREF: _s3m_module+2F4j
		and	ch, 1Fh
		cmp	[byte ptr _word_245D4+1], ch
		jnb	short loc_1089C
		mov	[byte ptr _word_245D4+1], ch

loc_1089C:				; CODE XREF: _s3m_module+2FFj
		call	sub_11BA6
		lodsb
		or	al, al
		jnz	loc_10811

loc_108A6:				; CODE XREF: _s3m_module+276j
		mov	[byte ptr es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	loc_10809

loc_108B1:				; CODE XREF: _s3m_module+246j
		call	_mem_reallocx
		pop	ax
		inc	ax
		cmp	ax, [_word_245F2]
		jb	loc_107B4
		mov	ax, [_word_245D4]
		inc	ah
		cmp	al, ah
		jb	short loc_108C9
		mov	al, ah

loc_108C9:				; CODE XREF: _s3m_module+32Ej
		xor	ah, ah
		mov	[_word_245D4], ax
		call	near ptr _mod_readfile_11F4E
		jb	loc_10099
		retn
endp		_s3m_module ; sp-analysis failed

; ---------------------------------------------------------------------------
_s3mtable_108D6	db 0FFh,10h,0Bh,0Dh,15h,12h,11h,13h,14h,1Bh,1Dh,17h,16h
					; DATA XREF: _s3m_module+2BDr
		db 0FFh,0FFh,9,0FFh,1Ch,7,0Eh,0Fh,0FFh,0FFh,0FFh,8,0FFh
_s3mtable_108F0	db 0,3,5,4,7,0FFh,0FFh,0FFh,8,0FFh,0FFh,6,0Ch,0Dh,0FFh
					; DATA XREF: _s3m_module+2D6r
		db 0FFh

; =============== S U B	R O U T	I N E =======================================

; E669

proc		_e669_module near	; DATA XREF: seg003:0E61o
		mov	[_module_type_text], 39363645h
		jmp	short loc_10914
; ---------------------------------------------------------------------------

__669_module:				; DATA XREF: seg003:0E5Ao
		mov	[_module_type_text], 20393636h ;	669

loc_10914:				; CODE XREF: _e669_module+9j
		mov	[_moduleflag_246D0], 100b
		mov	[_byte_24673], 80h ; 'Ä'
		mov	[_byte_2467E], 2
		mov	[_word_245D4], 8
		movzx	ax, [_byte_30576]
		mov	[_word_245D2], ax
		mov	al, [_byte_30577]
		mov	[_word_245F2], ax
		mov	ah, [_byte_2461F]
		mov	al, [_byte_2461E]
		shl	eax, 10h
		mov	ah, [_byte_2461F]
		mov	al, [_byte_2461E]
		mov	[_dword_27BC8], eax
		mov	[_dword_27BCC], eax
		mov	ax, ds
		mov	es, ax
		mov	si, (offset _chrin+1)
		mov	cx, 4Ch	; 'L'

loc_1095C:				; CODE XREF: _e669_module+60j
		inc	si		; in
		cmp	[byte ptr si], 20h ; ' '
		loope	loc_1095C
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 20h	; ' '   ; count
		call	_copy_printable
		xor	si, si
		xor	bh, bh

loc_1096F:				; CODE XREF: _e669_module+91j
		mov	bl, [_byte_30579+si]
		cmp	bl, 0FFh
		jz	short loc_10993
		mov	[_byte_27FE8+si], bl
		mov	al, [_byte_305F9+bx]
		mov	[_byte_280E8+si], al
		mov	al, [_byte_30679+bx]
		mov	[_byte_281E8+si], al
		inc	si
		cmp	si, 80h	; 'Ä'
		jb	short loc_1096F

loc_10993:				; CODE XREF: _e669_module+76j
		mov	[_word_245FA], si
		mov	al, [_byte_280E8]
		mov	[_byte_24679], al
		mov	[_byte_2467A], 50h ; 'P'
		mov	dx, offset _chrin
		imul	cx, [_word_245D2], 25
		mov	eax, 497
		call	_dosseek
		mov	si, offset _chrin ; in
		mov	di, offset _myout ; out
		mov	cx, [_word_245D2]

loc_109BD:				; CODE XREF: _e669_module+127j
		push	cx
		mov	cx, 0Dh		; count
		call	_copy_printable
		pop	cx
		mov	edx, [si+0Dh]
		cmp	edx, 100000h
		cmc
		adc	[_word_24662], 0
		mov	[di+20h], edx
		add	[_dword_245C4], edx
		mov	[byte ptr di+3Dh], 3Fh ; '?'
		mov	[word ptr di+36h], 2100h
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

loc_10A0F:				; CODE XREF: _e669_module+FAj
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	[byte ptr di+3Ch], 8

loc_10A20:				; CODE XREF: _e669_module+10Dj
		add	si, 19h
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_109BD
		mov	cx, [_word_245F2]

loc_10A2D:				; CODE XREF: _e669_module+1C9j
		push	cx
		mov	dx, offset _word_31508
		mov	cx, 600h
		call	_dosfread
		call	_memalloc12k
		mov	si, offset _word_31508
		mov	cx, 40h	; '@'

loc_10A40:				; CODE XREF: _e669_module+1C0j
		push	cx
		mov	cx, [_word_245D4]
		xor	ch, ch

loc_10A47:				; CODE XREF: _e669_module+1B7j
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

loc_10A75:				; CODE XREF: _e669_module+154j
		mov	al, [si+1]
		and	al, 0Fh
		mov	ah, 44h	; 'D'
		mul	ah
		shr	ax, 4
		mov	cl, al

loc_10A83:				; CODE XREF: _e669_module+150j
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

loc_10AAA:				; CODE XREF: _e669_module+192j
					; _e669_module+19Aj ...
		xor	dx, dx

loc_10AAC:				; CODE XREF: _e669_module+196j
					; _e669_module+1A8j
		call	sub_11BA6
		add	si, 3
		pop	cx
		inc	ch
		cmp	ch, cl
		jb	short loc_10A47
		mov	[byte ptr es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	loc_10A40
		call	_mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_10A2D
		call	near ptr _mod_readfile_11F4E
		jb	loc_10099
		retn
endp		_e669_module ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================

; MTM

proc		_mtm_module near		; DATA XREF: seg003:0E2Fo
		mov	[_module_type_text], 204D544Dh
		mov	[_moduleflag_246D0], 100000b
		mov	[_byte_24679], 6
		mov	[_byte_2467A], 7Dh ; '}'
		mov	[_byte_24673], 80h ; 'Ä'
		mov	ax, ds
		mov	es, ax
		mov	si, offset _myin	; in
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 14h		; count
		call	_copy_printable
		cmp	[_sndcard_type],	0
		jnz	short loc_10B25
		xor	si, si
		mov	cx, 10h

loc_10B0F:				; CODE XREF: _mtm_module+4Ej
		mov	al, [byte ptr _word_3052A+si]
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:_byte_13C54+di]
		mov	[byte ptr _dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_10B0F

loc_10B25:				; CODE XREF: _mtm_module+33j
		movzx	ax, [_byte_30526]
		mov	[_word_245D2], ax
		mov	al, [_byte_30522]
		inc	al
		mov	[_word_245F2], ax
		movzx	ax, [_byte_30523]
		inc	ax
		mov	[_word_245FA], ax
		mov	dx, offset _chrin
		imul	cx, [_word_245D2], 25h
		add	cx, 0C2h ; '¬'
		xor	eax, eax
		call	_dosseek
		mov	si, offset unk_3054A
		mov	di, offset _myout
		mov	cx, [_word_245D2]
endp		_mtm_module ; sp-analysis failed

; START	OF FUNCTION CHUNK FOR _snd_off

loc_10B5A:				; CODE XREF: _snd_off-3660j
		push	cx
		mov	cx, 16h		; count
		call	_copy_printable
		pop	cx
		mov	edx, [si+16h]

loc_10B66:				; CODE XREF: _snd_off+1Ej
		cmp	edx, 100000h
		cmc
		adc	[_word_24662], 0
		mov	[di+20h], edx
		add	[_dword_245C4], edx
		mov	al, [si+23h]
		mov	[di+3Dh], al
		mov	al, [si+22h]
		and	al, 0Fh
		mov	[di+3Eh], al
		mov	ax, [_freq_245DE]
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

loc_10BB5:				; CODE XREF: _snd_off-368Dj
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	[byte ptr di+3Ch], 8

loc_10BC6:				; CODE XREF: _snd_off-367Aj
		add	si, 25h	; '%'
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_10B5A
		mov	di, offset _byte_27FE8
		mov	cx, 20h	; ' '
		cld
		rep movsd
		imul	ax, [_word_245D2], 37
		add	ax, 0C2h ; '¬'
		movzx	eax, ax
		mov	[_chrin], eax
		movzx	eax, [_word_30520]
		imul	eax, 192	; CODE XREF: _snd_deinit+16j
		add	eax, [_chrin]
		mov	dx, offset _byte_33508
		mov	cx, [_word_245F2]
		shl	cx, 6
		call	_dosseek
		mov	si, offset _byte_33508
		mov	cx, [_word_245F2]
		mov	ax, 4

loc_10C12:				; CODE XREF: _snd_off-3603j
		mov	bp, 1

loc_10C15:				; CODE XREF: _snd_off-3606j
		cmp	[word ptr si], 0
		jz	short loc_10C20
		cmp	bp, ax
		jb	short loc_10C20
		mov	ax, bp

loc_10C20:				; CODE XREF: _snd_off-3615j
					; _snd_off-3611j
		add	si, 2
		inc	bp
		cmp	bp, 20h	; ' '
		jbe	short loc_10C15
		dec	cx
		jnz	short loc_10C12
		mov	[_word_245D4], ax
		mov	bx, offset _byte_33508
		mov	cx, [_word_245F2]

loc_10C36:				; CODE XREF: _snd_off-354Aj
		push	bx
		push	cx
		mov	si, offset _word_31508
		mov	cx, [_word_245D4]

loc_10C3F:				; CODE XREF: _snd_off-35AFj
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

loc_10C5A:				; CODE XREF: _snd_off-35E7j
		dec	ax
		movzx	eax, ax
		imul	eax, 192
		add	eax, [_chrin]
		mov	dx, si
		mov	cx, 192
		call	_dosseek

loc_10C73:				; CODE XREF: _snd_off-35D5j
		pop	si
		pop	cx
		pop	bx
		add	bx, 2
		add	si, 192
		dec	cx
		jnz	short loc_10C3F
		call	_memalloc12k
		mov	si, offset _word_31508
		mov	cx, 40h	; '@'

loc_10C89:				; CODE XREF: _snd_off-3555j
		push	cx
		push	si
		mov	cx, [_word_245D4]
		xor	ch, ch

loc_10C91:				; CODE XREF: _snd_off-3562j
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

loc_10CAA:				; CODE XREF: _snd_off-3594j
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
		mov	[byte ptr es:di], 0
		inc	di
		pop	si
		pop	cx
		add	si, 3
		dec	cx
		jnz	short loc_10C89
		call	_mem_reallocx
		pop	cx
		pop	bx
		add	bx, 40h	; '@'
		dec	cx
		jnz	loc_10C36
		mov	ax, 192
		mul	[_word_30520]
		mov	cx, dx
		imul	dx, [_word_245D2], 37
		add	dx, 0C2h ; '¬'
		add	dx, [_word_30524]
		adc	cx, 0
		add	dx, ax
		adc	cx, 0
		mov	ax, [_word_245F2]
		shl	ax, 6
		add	dx, ax
		adc	cx, 0
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		adc	[_word_24662], 0
		call	near ptr _mod_readfile_11F4E
		jb	loc_10099
		retn
; END OF FUNCTION CHUNK	FOR _snd_off

; =============== S U B	R O U T	I N E =======================================

; PSM

proc		_psm_module near		; DATA XREF: seg003:0E37o
		mov	[_module_type_text], 204D5350h
		mov	[_moduleflag_246D0], 1000000b
		mov	ax, [_word_30556]
		mov	[_word_245D4], ax
		mov	ax, [_word_30554]
		mov	[_word_245D2], ax
		mov	[_freq_245DE], 8448
		mov	al, [_byte_3054B]
		mov	[_byte_24679], al
		mov	al, [_byte_3054C]
		mov	[_byte_2467A], al
		movzx	ax, [_byte_30550]
		mov	[_word_245FA], ax
		mov	ax, [_word_30552]
		mov	[_word_245F2], ax
		mov	ax, ds
		mov	es, ax
		mov	si, offset _myin	; in
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 30		; count
		call	_copy_printable
		mov	dx, offset _byte_3059A
		mov	cx, [_word_245D2]
		shl	cx, 6
		mov	eax, [_dword_30566]
		call	_dosseek
		mov	si, offset _byte_3059A
		mov	di, offset _myout ; out
		mov	cx, [_word_245D2]

loc_10D8C:				; CODE XREF: _psm_module+FAj
		push	cx
		push	si
		add	si, 0Dh		; in
		mov	cx, 16h		; count
		call	_copy_printable
		pop	si
		pop	cx
		mov	edx, [si+30h]
		cmp	edx, 100000h
		cmc
		adc	[_word_24662], 0
		mov	[di+20h], edx
		add	[_dword_245C4], edx
		mov	[byte ptr di+3Fh], 1
		mov	eax, [si+25h]
		mov	[di+38h], eax
		mov	ax, [si+3Eh]
		jnz	short loc_10DC7
		mov	ax, [_freq_245DE]

loc_10DC7:				; CODE XREF: _psm_module+9Cj
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

loc_10DF0:				; CODE XREF: _psm_module+B5j
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

loc_10E15:				; CODE XREF: _psm_module+DEj
		or	[byte ptr di+3Ch], 8

loc_10E19:				; CODE XREF: _psm_module+C8j
		add	si, 40h	; '@'
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_10D8C
		mov	dx, offset _byte_27FE8
		mov	cx, [_word_245FA]
		mov	eax, [_dword_3055A]
		call	_dosseek
		mov	dx, [_word_30562]
		mov	cx, [_word_30564]
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		adc	[_word_24662], 0
		mov	cx, [_word_245F2]

loc_10E4C:				; CODE XREF: _psm_module+1DCj
		push	cx
		mov	dx, offset _word_31508
		mov	cx, 4
		call	_dosfread
		xor	si, si
		mov	cx, [_word_245FA]
		mov	ax, [_my_seg_index]
		mov	dl, [_byte_3150A]
		dec	dl
		and	dl, 3Fh

loc_10E68:				; CODE XREF: _psm_module+14Ej
		cmp	[_byte_27FE8+si], al
		jnz	short loc_10E72
		mov	[_byte_281E8+si], dl

loc_10E72:				; CODE XREF: _psm_module+146j
		inc	si
		dec	cx
		jnz	short loc_10E68
		mov	dx, offset _byte_3150C
		mov	cx, [_word_31508]
		sub	cx, 4
		call	_dosfread
		call	_memalloc12k
		mov	si, offset _byte_3150C
		mov	cx, 40h	; '@'

loc_10E8C:				; CODE XREF: _psm_module+1D5j
		push	cx
		lodsb
		or	al, al
		jz	short loc_10EF4

loc_10E92:				; CODE XREF: _psm_module+1CCj
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

loc_10EB6:				; CODE XREF: _psm_module+17Cj
		cmp	bh, 63h	; 'c'
		jbe	short loc_10EBD
		xor	bh, bh

loc_10EBD:				; CODE XREF: _psm_module+173j
					; _psm_module+193j
		mov	cl, 0FFh
		test	ch, 40h
		jz	short loc_10ECE
		mov	cl, [si]
		inc	si
		cmp	cl, 40h	; '@'
		jbe	short loc_10ECE
		mov	cl, 0FFh

loc_10ECE:				; CODE XREF: _psm_module+19Cj
					; _psm_module+1A4j
		test	ch, 20h
		jz	short loc_10EDD
		mov	dx, [si]
		add	si, 2
		cmp	dl, 0Fh
		jbe	short loc_10EDF

loc_10EDD:				; CODE XREF: _psm_module+1ABj
		xor	dx, dx

loc_10EDF:				; CODE XREF: _psm_module+1B5j
		and	ch, 1Fh
		cmp	[byte ptr _word_245D4+1], ch
		jnb	short loc_10EEC
		mov	[byte ptr _word_245D4+1], ch

loc_10EEC:				; CODE XREF: _psm_module+1C0j
		call	sub_11BA6
		lodsb
		or	al, al
		jnz	short loc_10E92

loc_10EF4:				; CODE XREF: _psm_module+16Aj
		mov	[byte ptr es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	short loc_10E8C
		call	_mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_10E4C
		mov	ax, [_word_245D4]
		inc	ah
		cmp	al, ah
		jb	short loc_10F11
		mov	al, ah

loc_10F11:				; CODE XREF: _psm_module+1E7j
		xor	ah, ah
		mov	[_word_245D4], ax
		call	near ptr _mod_readfile_11F4E
		jb	loc_10099
		retn
endp		_psm_module ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================

; FAR

proc		_far_module near		; DATA XREF: seg003:0E40o
		mov	[_module_type_text], 20524146h
		mov	[_moduleflag_246D0], 10000000b
		mov	[_byte_24673], 0
		mov	[_byte_2467E], 2
		mov	[_word_245D4], 10h
		mov	al, [byte ptr _word_30552+1]
		and	ax, 0Fh
		mov	di, ax
		mov	al, [cs:_table_14057+di]
		mov	[_byte_2467B], al
		mov	[_byte_2467C], 0
		call	_calc_14043
		mov	[_byte_2467A], al
		mov	[_byte_24679], 4
		cmp	[_sndcard_type],	0
		jnz	short loc_10F80
		xor	si, si
		mov	cx, [_word_245D4]

loc_10F6A:				; CODE XREF: _far_module+60j
		mov	al, [byte ptr _word_30554+si]
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:_byte_13C54+di]
		mov	[byte ptr _dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_10F6A

loc_10F80:				; CODE XREF: _far_module+44j
		mov	ax, ds
		mov	es, ax
		mov	si, offset _myin	; in
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 20h	; ' '   ; count
		call	_copy_printable
		mov	dx, (offset _dword_30566+2)
		mov	cx, 303h
		movzx	eax, [word ptr _dword_30566+2]
		add	eax, 62h ; 'b'
		call	_dosseek
		movzx	ax, [_byte_30669]
		cmp	ax, 100h
		jb	short loc_10FB0
		mov	ax, 100h

loc_10FB0:				; CODE XREF: _far_module+8Dj
		mov	[_word_245FA], ax
		movzx	ax, [_byte_3066A]
		mov	[_word_245F8], ax
		mov	si, (offset _dword_30566+2)
		mov	di, offset _byte_27FE8
		mov	cx, [_word_245FA]
		cld
		rep movsb
		mov	bx, offset _byte_3066B
		xor	ax, ax
		xor	dx, dx

loc_10FCF:				; CODE XREF: _far_module+C0j
		inc	dx
		cmp	[word ptr bx], 0
		jz	short loc_10FD7
		mov	ax, dx

loc_10FD7:				; CODE XREF: _far_module+B5j
		add	bx, 2
		cmp	dx, 100h
		jb	short loc_10FCF
		or	ax, ax
		stc
		jz	loc_10099
		cmp	ax, 100h
		jb	short loc_10FEF
		mov	ax, 100h

loc_10FEF:				; CODE XREF: _far_module+CCj
		mov	[_word_245F2], ax
		mov	[byte ptr _chrin+3], 0
		mov	si, offset _byte_3066B
		mov	cx, [_word_245F2]

loc_10FFE:				; CODE XREF: _far_module+214j
		push	cx
		push	si
		mov	ax, [si]
		or	ax, ax
		jnz	short loc_1100F
		call	_memalloc12k
		mov	cx, 40h	; '@'
		jmp	loc_11120
; ---------------------------------------------------------------------------

loc_1100F:				; CODE XREF: _far_module+E6j
		sub	ax, 2
		shr	ax, 2
		xor	dx, dx
		div	[_word_245D4]
		push	ax
		dec	al
		and	al, 3Fh
		mov	[byte ptr _chrin], al
		xor	di, di
		mov	cx, [_word_245FA]
		mov	ah, [byte ptr _chrin+3]

loc_1102D:				; CODE XREF: _far_module+11Bj
		cmp	ah, [_byte_27FE8+di]
		jnz	short loc_11037
		mov	[_byte_281E8+di], al

loc_11037:				; CODE XREF: _far_module+113j
		inc	di
		dec	cx
		jnz	short loc_1102D
		mov	dx, offset _word_31508
		mov	cx, [si]
		call	_dosfread
		mov	[byte ptr _chrin+1], 0
		call	_memalloc12k
		pop	cx
		xor	ch, ch
		mov	si, offset _byte_3150A

loc_11051:				; CODE XREF: _far_module+1F7j
		push	cx
		mov	cx, [_word_245D4]
		xor	ch, ch

loc_11058:				; CODE XREF: _far_module+1ECj
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

loc_11082:				; CODE XREF: _far_module+143j
					; _far_module+160j
		mov	cl, 0FFh
		mov	al, [si+2]
		or	al, al
		jz	short loc_11094
		dec	al
		and	al, 0Fh
		shl	al, 2
		mov	cl, al

loc_11094:				; CODE XREF: _far_module+16Bj
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

loc_110CB:				; CODE XREF: _far_module+184j
		mov	dl, 19h
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110CF:				; CODE XREF: _far_module+18Ej
		shr	dh, 1
		mov	[byte ptr _chrin+1], dh
		xor	dx, dx
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110D9:				; CODE XREF: _far_module+193j
		shl	dh, 4
		or	dh, [byte ptr _chrin+1]
		mov	dl, 4
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110E4:				; CODE XREF: _far_module+189j
		mov	dl, 0Eh

loc_110E6:
		or	dh, 90h
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110EB:				; CODE XREF: _far_module+1A7j
		mov	dl, 1Fh
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110EF:				; CODE XREF: _far_module+19Dj
		mov	dl, 20h	; ' '
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110F3:				; CODE XREF: _far_module+1A2j
		mov	dl, 20h	; ' '
		shl	dh, 4
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110FA:				; CODE XREF: _far_module+198j
		mov	dl, 0Eh

loc_110FC:
		or	dh, 80h

loc_110FF:				; CODE XREF: _far_module+1ABj
					; _far_module+1AFj ...
		call	sub_11BA6
		add	si, 4
		pop	cx
		inc	ch
		cmp	ch, cl
		jb	loc_11058
		mov	[byte ptr es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	loc_11051
		mov	cx, 3Fh	; '?'
		sub	cl, [byte ptr _chrin]

loc_11120:				; CODE XREF: _far_module+EEj
		xor	al, al
		cld
		rep stosb
		call	_mem_reallocx
		pop	si
		pop	cx
		inc	[byte ptr _chrin+3]
		add	si, 2
		dec	cx
		jnz	loc_10FFE
		mov	ax, ds
		assume es:dseg
		mov	es, ax
		assume es:seg003

loc_1113A:
		mov	dx, offset _myin
		mov	cx, 8
		call	_dosfread
		mov	si, offset _myin
		mov	di, offset _myout

loc_11149:
		xor	ax, ax
		mov	[_word_245D2], ax
		mov	ch, 8

loc_11150:				; CODE XREF: _far_module+305j
		mov	cl, 8

loc_11152:				; CODE XREF: _far_module+2FEj
		inc	ax
		shr	[byte ptr si], 1
		jnb	loc_11217
		push	ax
		push	cx
		push	si
		push	di
		mov	[_word_245D2], ax
		push	di
		mov	dx, offset _word_31508
		mov	cx, 30h	; '0'
		call	_dosfread
		xor	dx, dx
		xor	cx, cx
		mov	bx, [_fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		pop	di		; out
		mov	[di+38h], ax
		mov	[di+3Ah], dx
		mov	si, offset _word_31508 ;	in

loc_11181:
		mov	edx, [si+20h]
		cmp	edx, 100000h
		cmc

loc_1118D:
		adc	[_word_24662], 0
		mov	[di+20h], edx
		add	[_dword_245C4], edx
		mov	al, [si+25h]
		ror	al, 4
		shr	al, 2
		mov	[di+3Dh], al
		mov	ax, [_freq_245DE]
		mov	[di+36h], ax

loc_111AD:
		test	[byte ptr si+2Fh], 8
		jnz	short loc_111C6

loc_111B3:				; CODE XREF: _far_module+2AFj
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_111E8
; ---------------------------------------------------------------------------

loc_111C6:				; CODE XREF: _far_module+293j
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
		or	[byte ptr di+3Ch], 8

loc_111E8:				; CODE XREF: _far_module+2A6j
		mov	cx, 20h	; ' '   ; count
		call	_copy_printable
		test	[byte ptr si+2Eh], 1
		jz	short loc_11204
		or	[byte ptr di+3Ch], 4
		shr	[dword ptr di+24h], 1
		shr	[dword ptr di+2Ch], 1
		shr	[dword ptr di+28h], 1

loc_11204:				; CODE XREF: _far_module+2D4j
		mov	dx, [si+20h]
		mov	cx, [si+22h]
		mov	bx, [_fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		pop	di
		pop	si
		pop	cx
		pop	ax

loc_11217:				; CODE XREF: _far_module+237j
		add	di, 40h	; '@'
		dec	cl
		jnz	loc_11152
		inc	si
		dec	ch
		jnz	loc_11150
		cmp	[_word_245D2], 0
		stc
		jz	loc_10099
		call	near ptr _mod_readfile_11F4E
		jb	loc_10099
		retn
endp		_far_module ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================

; ULT

proc		_ult_module near		; DATA XREF: seg003:0E49o
		mov	[_module_type_text], 20544C55h
		mov	[_moduleflag_246D0], 1000000000b
		mov	[_byte_24673], 0
		mov	[word ptr _chrin], 40h ;	'@'
		mov	ax, [_word_30515]

loc_11256:
		xchg	al, ah
		mov	[_word_30515], ax
		cmp	ax, 3034h
		jb	short loc_11265
		add	[word ptr _chrin], 2

loc_11265:				; CODE XREF: _ult_module+25j
		mov	[_byte_24679], 6
		mov	[_byte_2467A], 7Dh ; '}'

loc_1126F:
		mov	ax, ds
		mov	es, ax
		mov	si, offset _myin_0 ; in
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 20h	; ' '   ; count
		call	_copy_printable
		mov	dx, offset _my_in
		mov	cx, 1
		movzx	eax, [_byte_30537]
		shl	eax, 5
		add	eax, 30h ; '0'
		call	_dosseek
		movzx	ax, [_my_in]
		mov	[_word_245D2], ax
		mul	[word ptr _chrin]
		mov	cx, ax
		mov	dx, offset _byte_30539
		call	_dosfread
		mov	si, offset _byte_30539 ;	in
		mov	di, offset _myout ; out
		mov	cx, [_word_245D2]

loc_112B4:				; CODE XREF: _ult_module+131j
		push	cx
		push	si
		push	di
		mov	edx, [si+38h]
		sub	edx, [si+34h]
		jnb	short loc_112C4
		xor	edx, edx

loc_112C4:				; CODE XREF: _ult_module+86j
		cmp	edx, 100000h
		cmc
		adc	[_word_24662], 0
		mov	[di+20h], edx
		add	[_dword_245C4], edx
		mov	al, [si+3Ch]
		shr	al, 2
		mov	[di+3Dh], al
		mov	ax, [_freq_245DE]
		cmp	[_word_30515], 3034h
		jb	short loc_112F1
		mov	ax, [si+3Eh]

loc_112F1:				; CODE XREF: _ult_module+B3j
		mov	[di+36h], ax
		mov	al, [si+3Dh]
		and	al, 1Ch
		mov	[di+3Ch], al
		test	al, 4
		jz	short loc_11316
		add	[_dword_245C4], edx
		cmp	edx, 80000h
		cmc
		adc	[_word_24662], 0
		shl	[dword ptr di+20h], 1

loc_11316:				; CODE XREF: _ult_module+C5j
		test	al, 8
		jnz	short loc_1132D

loc_1131A:				; CODE XREF: _ult_module+FBj
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_11359
; ---------------------------------------------------------------------------

loc_1132D:				; CODE XREF: _ult_module+DFj
		mov	eax, [si+30h]
		or	eax, eax
		jz	short loc_1131A
		dec	eax
		mov	ebx, [si+2Ch]
		test	[byte ptr di+3Ch], 4
		jz	short loc_11348
		shr	ebx, 1
		shr	eax, 1

loc_11348:				; CODE XREF: _ult_module+107j
		mov	[di+24h], ebx
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax

loc_11359:				; CODE XREF: _ult_module+F2j
		mov	cx, 20h	; ' '   ; count
		call	_copy_printable
		pop	di
		pop	si
		pop	cx
		add	di, 40h	; '@'

loc_11365:
		add	si, [word ptr _chrin]
		dec	cx
		jnz	loc_112B4
		mov	dx, offset _byte_30539
		mov	cx, 102h
		call	_dosfread
		mov	[_word_245F8], 0
		mov	si, offset _byte_30539
		xor	ax, ax

loc_11382:				; CODE XREF: _ult_module+153j
		cmp	[byte ptr si], 0FFh
		jz	short loc_1138E
		inc	ax
		inc	si
		cmp	ax, 100h
		jb	short loc_11382

loc_1138E:				; CODE XREF: _ult_module+14Cj
		mov	[_word_245FA], ax
		mov	ax, ds
		mov	es, ax
		mov	si, offset _byte_30539
		mov	di, offset _byte_27FE8
		mov	cx, [_word_245FA]
		cld
		rep movsb
		movzx	ax, [_byte_30639]
		inc	ax
		mov	[_word_245D4], ax
		movzx	ax, [_byte_3063A]
		inc	ax
		mov	[_word_245F2], ax
		mov	[_byte_2467E], 0
		mov	ax, [_word_30515]
		cmp	ax, 3031h
		jz	short loc_113C6
		mov	[_byte_2467E], 2

loc_113C6:				; CODE XREF: _ult_module+186j
		cmp	ax, 3033h
		jb	short loc_113F8
		mov	dx, offset _word_3063B
		mov	cx, [_word_245D4]
		call	_dosfread
		cmp	[_sndcard_type],	0
		jnz	short loc_113F8
		xor	si, si
		mov	cx, [_word_245D4]

loc_113E2:				; CODE XREF: _ult_module+1BDj
		mov	al, [byte ptr _word_3063B+si]
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:_byte_13C54+di]
		mov	[byte ptr _dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_113E2

loc_113F8:				; CODE XREF: _ult_module+190j
					; _ult_module+1A1j
		mov	si, offset _dword_30518
		mov	cx, [_word_245D4]

loc_113FF:				; CODE XREF: _ult_module+1F9j
		push	cx
		push	si
		xor	dx, dx
		xor	cx, cx
		mov	bx, [_fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		mov	[si], ax
		mov	[si+2],	dx
		mov	cx, [_word_245F2]

loc_11417:				; CODE XREF: _ult_module+1F1j
		push	cx
		mov	[byte ptr _word_3063B+1], 1
		mov	cx, 40h	; '@'

loc_11420:				; CODE XREF: _ult_module+1EDj
		push	cx
		call	_ult_read
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
		mov	cx, [_word_245F2]

loc_11438:				; CODE XREF: _ult_module+2C6j
		push	cx
		mov	si, offset _dword_30518
		mov	di, offset _byte_30908
		mov	cx, [_word_245D4]

loc_11443:				; CODE XREF: _ult_module+250j
		push	cx
		mov	dx, [si]
		mov	cx, [si+2]
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		mov	[byte ptr _word_3063B+1], 1
		mov	cx, 40h	; '@'

loc_1145A:				; CODE XREF: _ult_module+237j
		push	cx
		call	_ult_read
		mov	eax, [_dword_3063D]
		mov	[di], eax
		mov	al, [_byte_30641]
		mov	[di+4],	al
		add	di, 5
		pop	cx
		dec	cx
		jnz	short loc_1145A
		xor	dx, dx
		xor	cx, cx
		mov	bx, [_fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		mov	[si], ax
		mov	[si+2],	dx
		pop	cx
		add	si, 4
		dec	cx
		jnz	short loc_11443
		call	_memalloc12k
		mov	si, offset _byte_30908
		mov	cx, 40h	; '@'

loc_11494:				; CODE XREF: _ult_module+2BFj
		push	cx
		push	si
		mov	cx, [_word_245D4]
		xor	ch, ch

loc_1149C:				; CODE XREF: _ult_module+2B2j
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

loc_114C0:				; CODE XREF: _ult_module+26Aj
					; _ult_module+283j
		mov	cl, 0FFh
		mov	al, [si+2]
		mov	dl, al
		shr	al, 4
		mov	ah, [si+4]
		and	dl, 0Fh
		mov	dh, [si+3]
		call	_ult_1150B
		xchg	ax, dx
		call	_ult_1150B
		cmp	dl, al
		ja	short loc_114DF
		xchg	ax, dx

loc_114DF:				; CODE XREF: _ult_module+2A3j
		call	sub_11BA6
		pop	cx
		add	si, 140h
		inc	ch
		cmp	ch, cl
		jb	short loc_1149C
		mov	[byte ptr es:di], 0
		inc	di
		pop	si
		pop	cx
		add	si, 5
		dec	cx
		jnz	short loc_11494
		call	_mem_reallocx
		pop	cx
		dec	cx
		jnz	loc_11438
		call	near ptr _mod_readfile_11F4E
		jb	loc_10099
		retn
endp		_ult_module ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_ult_1150B near		; CODE XREF: _ult_module+29Ap
					; _ult_module+29Ep
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

loc_11520:				; CODE XREF: _ult_1150B+2j
		xor	ax, ax
		retn
; ---------------------------------------------------------------------------

loc_11523:				; CODE XREF: _ult_1150B+6j
		shr	ah, 2
		and	ah, 33h
		retn
; ---------------------------------------------------------------------------

loc_1152A:				; CODE XREF: _ult_1150B+Aj
		and	ax, 0F00h
		or	ax, 800Eh
		retn
; ---------------------------------------------------------------------------

loc_11531:				; CODE XREF: _ult_1150B+Ej
		mov	cl, ah
		shr	cl, 2
		xor	ax, ax
		retn
; ---------------------------------------------------------------------------

loc_11539:				; CODE XREF: _ult_1150B+12j
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

loc_1154B:				; CODE XREF: _ult_1150B+37j
					; _ult_1150B+3Cj
		mov	dh, ah
		and	dh, 0F0h
		and	ah, 0Fh
		shr	ah, 2
		or	ah, dh
		pop	dx
		retn
endp		_ult_1150B


; =============== S U B	R O U T	I N E =======================================


proc		_ult_read near		; CODE XREF: _ult_module+1E8p
					; _ult_module+222p
		dec	[byte ptr _word_3063B+1]
		jnz	short locret_11584
		mov	dx, offset _word_3063B
		mov	cx, 2
		call	_dosfread
		cmp	[byte ptr _word_3063B], 0FCh ; '¸'
		jz	short loc_11585
		mov	ax, [_word_3063B]
		mov	[word ptr _dword_3063D],	ax
		mov	[byte ptr _word_3063B+1], 1
		mov	dx, (offset _dword_3063D+2)
		mov	cx, 3
		call	_dosfread

locret_11584:				; CODE XREF: _ult_read+4j
		retn
; ---------------------------------------------------------------------------

loc_11585:				; CODE XREF: _ult_read+14j
		mov	dx, offset _dword_3063D
		mov	cx, 5
		call	_dosfread
		retn
endp		_ult_read


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


 ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


proc		_inr_read_118B0 near	; CODE XREF: _inr_module+152p
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	es, ax
		shl	dx, 6
		mov	ax, dx
		add	ax, offset _myout
		push	ax
		mov	cx, 96
		mov	bx, [_fhandle_module]
		mov	dx, offset _aInertiaSample ; "Inertia Sample: "
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	bx
		jb	loc_119B2
		lea	di, [bx]
		mov	si, offset asc_25856 ; "				\r\n\x1A"
		cld
		mov	cx, 8
		rep movsd
		mov	di, bx
		mov	ecx, [_dword_25892]
		mov	[di+24h], ecx
		mov	eax, [_dword_25896]
		mov	[di+2Ch], eax
		sub	eax, ecx
		inc	eax
		mov	[di+28h], eax
		mov	ax, [_word_2588E]
		mov	[di+36h], ax
		mov	al, [_byte_2588C]
		mov	[di+3Eh], al
		mov	al, [_byte_2588B]
		mov	[di+3Dh], al
		mov	al, [_byte_2588D]
		mov	[di+3Ch], al
		mov	eax, [_dword_25886]
		mov	[di+20h], eax

loc_1191C:				; CODE XREF: _inr_read_118B0+FCj
		mov	dx, offset _chrin
		mov	cx, 8
		mov	bx, [_fhandle_module]
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		jb	loc_119B2
		mov	eax, [_myin]
		mov	[_dword_257A0], eax
		xor	cx, cx
		xor	dx, dx
		mov	bx, [_fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		shl	edx, 10h
		mov	dx, ax
		add	[_dword_257A0], edx
		mov	eax, [_chrin]
		cmp	eax, 54414453h	; SDAT
		jnz	short loc_11967	; SAMP
		mov	[di+38h], edx
		test	[_sndflags_24622], 4
		jnz	short loc_11999
		jmp	short loc_11999
; ---------------------------------------------------------------------------

loc_11967:				; CODE XREF: _inr_read_118B0+A8j
		cmp	eax, 504D4153h	; SAMP
		jnz	short loc_11991	; ENDS
		xor	cx, cx
		xor	dx, dx
		mov	bx, [_fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		mov	dx, ax
		mov	cx, dx
		sub	dx, 8
		sub	cx, 0
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		jmp	short loc_119AF
; ---------------------------------------------------------------------------

loc_11991:				; CODE XREF: _inr_read_118B0+BDj
		cmp	eax, 53444E45h	; ENDS
		jz	short loc_119AF

loc_11999:				; CODE XREF: _inr_read_118B0+B3j
					; _inr_read_118B0+B5j
		mov	dx, [word ptr _dword_257A0]
		mov	cx, [word ptr _dword_257A0+2]
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		jb	short loc_119B2
		jmp	loc_1191C
; ---------------------------------------------------------------------------

loc_119AF:				; CODE XREF: _inr_read_118B0+DFj
					; _inr_read_118B0+E7j
		clc
		pop	ds
		retn
; ---------------------------------------------------------------------------

loc_119B2:				; CODE XREF: _inr_read_118B0+20j
					; _inr_read_118B0+7Aj ...
		mov	ax, 0FFFEh
		pop	ds
		retn
endp		_inr_read_118B0


; =============== S U B	R O U T	I N E =======================================


; void __usercall _inr_read_119B7(void *buffer<edi>)
proc		_inr_read_119B7 near	; CODE XREF: _inr_module+B0p
					; _inr_module+C5p ...
		mov	ecx, [_myin]
		mov	bx, [_fhandle_module]
		mov	dx, di
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		retn
endp		_inr_read_119B7


; =============== S U B	R O U T	I N E =======================================

; INR

proc		_inr_module near		; DATA XREF: seg003:off_25326o
		mov	[_module_type_text], 20524E49h
		mov	[_moduleflag_246D0], 100000000b
		mov	[_byte_24673], 0
		mov	[_word_245F2], 0
		mov	[_word_245D2], 0
		mov	ax, ds
		mov	es, ax
		cld
		mov	dx, offset _aInertiaModule ; "Inertia Module: "
		mov	cx, 50h	; 'P'
		xor	eax, eax
		call	_dosseek
		mov	si, (offset _aInertiaModule+10h)
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 8
		cld
		rep movsd
		mov	al, [_byte_257DB]
		mov	[_byte_2461A], al
		mov	al, [_byte_257DC]
		mov	[_byte_2467E], al
		mov	ax, [_word_257E6]
		mov	[_word_245D4], ax
		dec	ax
		mov	[_byte_2461B], al
		mov	ax, [_word_257EC]
		mov	[_freq_245DE], ax
		mov	ax, [_word_257EE]
		mov	[_word_245FA], ax
		mov	ax, [_word_257F0]
		mov	[_word_245F8], ax
		mov	al, [_byte_257F2]
		mov	[_byte_2467A], al
		mov	al, [_byte_257F3]
		mov	[_byte_24679], al

loc_11A39:				; CODE XREF: _inr_module+172j
		mov	cx, 8
		mov	bx, [_fhandle_module]
		mov	dx, offset _chrin
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		jb	loc_11B3D
		mov	eax, [_myin]
		mov	[_dword_257A0], eax
		xor	cx, cx
		xor	dx, dx
		mov	bx, [_fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		add	[word ptr _dword_257A0],	ax
		adc	[word ptr _dword_257A0+2], dx
		mov	eax, [_chrin]
		cmp	eax, 54534C54h	; TLST
		jnz	short loc_11A81	; BLST
		mov	di, offset _byte_280E8 ;	buffer
		call	_inr_read_119B7
		jb	loc_11B3D
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11A81:				; CODE XREF: _inr_module+ABj
		cmp	eax, 54534C42h	; BLST
		jnz	short loc_11A96	; PLST
		mov	di, offset _byte_281E8 ;	buffer
		call	_inr_read_119B7
		jb	loc_11B3D
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11A96:				; CODE XREF: _inr_module+C0j
		cmp	eax, 54534C50h	; PLST
		jnz	short loc_11AAA	; PATT
		mov	di, offset _byte_27FE8 ;	buffer
		call	_inr_read_119B7
		jb	loc_11B3D
		jmp	short loc_11B28
; ---------------------------------------------------------------------------

loc_11AAA:				; CODE XREF: _inr_module+D5j
		cmp	eax, 54544150h	; PATT
		jnz	short loc_11B09	; SAMP
		mov	ebx, [_myin]
		cmp	ebx, 40h ; '@'
		ja	short loc_11AC0
		mov	bx, 40h	; '@'   ; bytes

loc_11AC0:				; CODE XREF: _inr_module+F4j
		call	_memalloc
		jb	short loc_11B3D
		mov	ecx, [_myin]
		mov	di, [_word_245F2]
		inc	[_word_245F2]
		shl	di, 1
		mov	[_segs_table+di], ax
		cmp	cx, 40h	; '@'
		jbe	short loc_11AF3
		mov	[_myseg_size+di], cx
		xor	dx, dx
		mov	bx, [_fhandle_module]
		push	ds
		mov	ds, ax
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	ds
		jb	short loc_11B3D
		jmp	short loc_11B28
; ---------------------------------------------------------------------------

loc_11AF3:				; CODE XREF: _inr_module+114j
		mov	[_myseg_size+di], 40h ; '@'
		xor	di, di
		mov	es, ax
		assume es:nothing
		mov	cx, 10h
		xor	eax, eax
		cld
		rep stosd
		jmp	short loc_11B28
; ---------------------------------------------------------------------------

loc_11B09:				; CODE XREF: _inr_module+E9j
		cmp	eax, 504D4153h	; SAMP
		jnz	short loc_11B20	; ENDM
		mov	dx, [_word_245D2]
		inc	[_word_245D2]
		call	_inr_read_118B0
		jb	short loc_11B3D
		jmp	short loc_11B28
; ---------------------------------------------------------------------------

loc_11B20:				; CODE XREF: _inr_module+148j
		cmp	eax, 4D444E45h	; ENDM
		jz	short loc_11B41

loc_11B28:				; CODE XREF: _inr_module+B7j
					; _inr_module+CCj ...
		mov	dx, [word ptr _dword_257A0]
		mov	cx, [word ptr _dword_257A0+2]
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		jnb	loc_11A39

loc_11B3D:				; CODE XREF: _inr_module+80j
					; _inr_module+B3j ...
		mov	ax, 0FFFEh
		retn
; ---------------------------------------------------------------------------

loc_11B41:				; CODE XREF: _inr_module+15Fj
		call	near ptr _mod_readfile_11F4E
		retn
endp		_inr_module ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_dosseek	near		; CODE XREF: __2stm_module+F3p
					; _s3m_module+11Cp ...
		push	cx
		push	dx
		mov	dx, ax
		shr	eax, 10h
		mov	cx, ax
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		pop	dx
		pop	cx
		mov	ax, 0FFFCh
		jb	_lfreaderr
endp		_dosseek	; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_dosfread near		; CODE XREF: _moduleread+39p
					; _mod_read_10311+Fp ...
		mov	bx, [_fhandle_module]
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		mov	cx, ax
		mov	ax, 0FFFCh
		jb	_lfreaderr	; 1 problem here
		retn
endp		_dosfread


; =============== S U B	R O U T	I N E =======================================


proc		_memalloc12k near	; CODE XREF: _mod_read_10311:loc_1035Cp
					; __2stm_module+118p ...
		mov	ebx, 12352	; bytes
		call	_memalloc
		jb	loc_10099
		mov	es, ax
		xor	di, di
		retn
endp		_memalloc12k


; =============== S U B	R O U T	I N E =======================================


proc		_mem_reallocx near	; CODE XREF: _mod_read_10311+D0p
					; __2stm_module+190p ...
		mov	bx, [_my_seg_index]
		shl	bx, 1
		mov	[_segs_table+bx], es
		mov	[_myseg_size+bx], di
		movzx	ebx, di
		mov	ax, es
		call	_memrealloc
		adc	[_word_24662], 0
		inc	[_my_seg_index]
		retn
endp		_mem_reallocx


; =============== S U B	R O U T	I N E =======================================


proc		sub_11BA6 near		; CODE XREF: _mod_read_10311+BDp
					; __2stm_module:loc_10565p ...
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
		cmp	al, [_byte_2461B]
		ja	short loc_11C04

locret_11C03:				; CODE XREF: sub_11BA6+2Ej
		retn
; ---------------------------------------------------------------------------

loc_11C04:				; CODE XREF: sub_11BA6+5Bj
		mov	[_byte_2461B], al
		retn
; ---------------------------------------------------------------------------

loc_11C08:				; CODE XREF: sub_11BA6+26j
		mov	dl, 1Dh
		jmp	short loc_11BCE
endp		sub_11BA6


; =============== S U B	R O U T	I N E =======================================


proc		sub_11C0C near		; CODE XREF: sub_1415E+65p
		xor	si, si
		or	al, al
		jz	short locret_11C28
		xor	bx, bx

loc_11C14:				; CODE XREF: sub_11C0C+16j
					; sub_11C0C+1Aj
		mov	bl, [cs:_byte_11C29+bx]
		add	si, bx
		mov	bl, [es:si]
		inc	si
		shr	bl, 5
		jnz	short loc_11C14
		dec	al
		jnz	short loc_11C14

locret_11C28:				; CODE XREF: sub_11C0C+4j
		retn
endp		sub_11C0C

; ---------------------------------------------------------------------------
_byte_11C29	db 0			; DATA XREF: sub_11C0C:loc_11C14r
					; sub_13623+1A1r
		db 2, 1, 3, 2, 4, 3, 5

; =============== S U B	R O U T	I N E =======================================


; int __usercall _copy_printable<eax>(char *in<esi>, char *out<edi>, int	count<ecx>)
proc		_copy_printable near	; CODE XREF: _mod_1021E+28p
					; _mod_1024A+11p ...
		push	si
		push	di

loc_11C33:				; CODE XREF: _copy_printable+Dj
		mov	al, [si]
		inc	si
		cmp	al, 20h	; ' '
		jb	short loc_11C40
		mov	[di], al
		inc	di
		dec	cx
		jnz	short loc_11C33

loc_11C40:				; CODE XREF: _copy_printable+7j
		pop	di
		pop	si
		retn
endp		_copy_printable


; =============== S U B	R O U T	I N E =======================================


proc		_clean_11C43 far		; CODE XREF: _moduleread:loc_1003Dp
					; sub_12DA8+75p ...
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	[_byte_24679], 6
		mov	[_byte_2467A], 125
		mov	[_byte_2467E], 0
		mov	[_moduleflag_246D0], 1
		mov	[_my_seg_index],	0
		mov	[_word_245F0], 0
		mov	[_word_245F6], 0
		mov	[_byte_24673], 0
		mov	[_word_24630], 2
		mov	[_word_245FA], 0
		mov	[_word_245F8], 0
		mov	[_word_245D4], 4
		mov	[_word_245D6], 4
		mov	[_word_245D8], 0
		mov	[_word_245DA], 0
		mov	[_word_245D2], 0
		mov	[_freq_245DE], 8287
		test	[_flag_playsetttings], 8
		jnz	short loc_11CB8
		mov	[_freq_245DE], 8363

loc_11CB8:				; CODE XREF: _clean_11C43+6Dj
		mov	[_byte_2461A], 0
		mov	[_dword_245C4], 0
		mov	[_amplification], 100
		mov	[_byte_24625], 0
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		cld
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 8
		mov	eax, '    '
		rep stosd
		mov	di, offset _volume_25908
		xor	eax, eax
		mov	cx, 280h
		rep stosd
		mov	di, offset _byte_282E8
		mov	cx, 8
		rep stosd
		mov	di, offset _dword_27BC8
		mov	ah, [_byte_2461E]
		mov	al, [_byte_2461F]
		shl	eax, 10h
		mov	ah, [_byte_2461F]
		mov	al, [_byte_2461E]
		mov	cx, 8
		rep stosd
		mov	di, offset _myout
		xor	eax, eax
		mov	cx, 630h
		rep stosd
		mov	dx, 63h	; 'c'
		mov	di, offset _myout
		mov	eax, '    '

loc_11D2D:				; CODE XREF: _clean_11C43+FCj
		mov	cx, 8
		rep stosd
		sub	di, 20h	; ' '
		mov	[word ptr di+32h], 0FFFFh
		add	di, 40h	; '@'
		dec	dx
		jnz	short loc_11D2D
		mov	di, offset _segs_table
		mov	cx, 80h	; 'Ä'
		xor	eax, eax
		rep stosd
		mov	di, offset _byte_280E8
		mov	cx, 40h	; '@'
		rep stosd
		mov	di, offset _byte_27FE8
		mov	cx, 40h	; '@'
		rep stosd
		mov	di, offset _byte_282E8
		mov	cx, 8
		rep stosd
		mov	di, offset _byte_281E8
		mov	cx, 40h	; '@'
		mov	eax, 3F3F3F3Fh
		rep stosd
		pop	ds
		retf
endp		_clean_11C43


; =============== S U B	R O U T	I N E =======================================


proc		_ems_init near		; CODE XREF: sub_12DA8+103p
		mov	[_ems_enabled], 0
		mov	ax, 1
		test	[byte ptr _config_word],	2
		jz	short loc_11E00
		xor	ax, ax
		mov	es, ax
		assume es:nothing
		mov	ax, 1
		mov	es, [word ptr es:19Eh]
		assume es:nothing
		cmp	[dword ptr es:0Ah], 584D4D45h ;	EMMX
		jnz	short loc_11E00
		cmp	[dword ptr es:0Eh], 30585858h ;	XXX0
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
		mov	[_ems_pageframe], bx
		mov	ah, 43h	; 'C'
		mov	bx, 1
		int	67h		;  - LIM EMS - GET HANDLE AND ALLOCATE MEMORY
					; BX = number of logical pages to allocate
					; Return: AH = status
		cmp	ah, 0
		mov	ax, 8
		jnz	short loc_11E00
		mov	[_ems_handle], dx
		mov	[_ems_enabled], 1
		mov	[_ems_log_pagenum], 0
		xor	ax, ax
		clc
		retn
; ---------------------------------------------------------------------------

loc_11E00:				; CODE XREF: _ems_init+Dj _ems_init+25j	...
		stc
		retn
endp		_ems_init


; =============== S U B	R O U T	I N E =======================================


proc		_ems_release near	; CODE XREF: _ems_deinit+7p
		cmp	[_ems_enabled], 1
		jnz	short locret_11E1D
		mov	bx, 8000h
		call	_ems_mapmem
		mov	dx, [_ems_handle]
		mov	ah, 45h	; 'E'
		int	67h		;  - LIM EMS - RELEASE HANDLE AND MEMORY
					; DX = EMM handle
					; Return: AH = status
		mov	[_ems_log_pagenum], 0

locret_11E1D:				; CODE XREF: _ems_release+5j
		retn
endp		_ems_release


; =============== S U B	R O U T	I N E =======================================


proc		_ems_realloc near	; CODE XREF: _memfree_125DA+6p
		cmp	[_ems_enabled], 1
		jnz	short locret_11E36
		mov	dx, [_ems_handle]
		mov	bx, 1
		mov	ah, 51h	; 'Q'
		int	67h		;  - LIM EMS 4.0 - REALLOCATE PAGES
					; DX = handle
					; BX = number of pages to be allocated to handle
					; Return: BX = actual number of	pages allocated	to handle
					; AH = status
		mov	[_ems_log_pagenum], 0

locret_11E36:				; CODE XREF: _ems_realloc+5j
		retn
endp		_ems_realloc


; =============== S U B	R O U T	I N E =======================================


proc		_ems_deinit near		; CODE XREF: _deinit_125B9+Fp
		cmp	[_ems_enabled], 1
		jnz	short locret_11E46
		call	_ems_release
		mov	[_ems_enabled], 0

locret_11E46:				; CODE XREF: _ems_deinit+5j
		retn
endp		_ems_deinit


; =============== S U B	R O U T	I N E =======================================


proc		_ems_save_mapctx	near	; CODE XREF: _moduleread+24p
					; _volume_prep+16p ...
		cmp	[_ems_enabled], 1
		jnz	short locret_11E67
		mov	cx, 32h	; '2'

loc_11E51:				; CODE XREF: _ems_save_mapctx+19j
		mov	dx, [_ems_handle]
		mov	ax, 4700h
		int	67h		;  - LIM EMS - SAVE MAPPING CONTEXT
					; DX = handle
					; Return: AH = status
		cmp	ah, 0
		jz	short locret_11E67
		dec	cx
		jnz	short loc_11E51
		mov	[_byte_246A5], 1

locret_11E67:				; CODE XREF: _ems_save_mapctx+5j
					; _ems_save_mapctx+16j
		retn
endp		_ems_save_mapctx


; =============== S U B	R O U T	I N E =======================================


proc		_ems_restore_mapctx near	; CODE XREF: _moduleread+78p
					; _moduleread+A9p ...
		cmp	[_ems_enabled], 1
		jnz	short locret_11E8A
		cmp	[_byte_246A5], 1
		jnz	short locret_11E8A
		mov	cx, 32h	; '2'

loc_11E79:				; CODE XREF: _ems_restore_mapctx+20j
		mov	dx, [_ems_handle]
		mov	ax, 4800h
		int	67h		;  - LIM EMS - RESTORE MAPPING CONTEXT
					; DX = handle
					; Return: AH = status
		cmp	ah, 0
		jz	short locret_11E8A
		dec	cx
		jnz	short loc_11E79

locret_11E8A:				; CODE XREF: _ems_restore_mapctx+5j
					; _ems_restore_mapctx+Cj ...
		retn
endp		_ems_restore_mapctx


; =============== S U B	R O U T	I N E =======================================


proc		_ems_mapmem near		; CODE XREF: _useless_11787+34p
					; _ems_release+Ap ...
		cmp	[_ems_enabled], 1
		jnz	short locret_11EC4
		mov	cx, 32h	; '2'
		cmp	bx, [_ems_log_pagenum]
		jb	short loc_11E9E
		mov	bx, 0FFFFh	; EMS UNMAP

loc_11E9E:				; CODE XREF: _ems_mapmem+Ej
					; _ems_mapmem+37j
		push	bx
		mov	dx, [_ems_handle]
		push	bx
		mov	ax, 4400h
		int	67h		;  - LIM EMS - MAP MEMORY
					; AL = physical	page number (0-3)
					; BX = logical page number, DX = handle
					; Return: AH = status
		pop	bx
		inc	bx
		jz	short loc_11EB3
		cmp	bx, [_ems_log_pagenum]
		jb	short loc_11EB6

loc_11EB3:				; CODE XREF: _ems_mapmem+20j
		mov	bx, 0FFFFh

loc_11EB6:				; CODE XREF: _ems_mapmem+26j
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

locret_11EC4:				; CODE XREF: _ems_mapmem+5j
					; _ems_mapmem+34j
		retn
endp		_ems_mapmem


; =============== S U B	R O U T	I N E =======================================


proc		_ems_mapmem2 near	; CODE XREF: _ems_mapmemx+48p
					; _ems_mapmemx+F4p ...
		cmp	[_ems_enabled], 1
		jnz	short locret_11EFE
		mov	cx, 32h	; '2'
		cmp	bx, [_ems_log_pagenum]
		jb	short loc_11ED8
		mov	bx, 0FFFFh

loc_11ED8:				; CODE XREF: _ems_mapmem2+Ej
					; _ems_mapmem2+37j
		push	bx
		mov	dx, [_ems_handle]
		push	bx
		mov	ax, 4402h
		int	67h		;  - LIM EMS - MAP MEMORY
					; AL = physical	page number (0-3)
					; BX = logical page number, DX = handle
					; Return: AH = status
		pop	bx
		inc	bx
		jz	short loc_11EED
		cmp	bx, [_ems_log_pagenum]
		jb	short loc_11EF0

loc_11EED:				; CODE XREF: _ems_mapmem2+20j
		mov	bx, 0FFFFh

loc_11EF0:				; CODE XREF: _ems_mapmem2+26j
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

locret_11EFE:				; CODE XREF: _ems_mapmem2+5j
					; _ems_mapmem2+34j
		retn
endp		_ems_mapmem2


; =============== S U B	R O U T	I N E =======================================


proc		_ems_realloc2 near	; CODE XREF: _mod_readfile_11F4E+36p
		inc	[_byte_24617]
		cmp	[_ems_enabled], 1
		jnz	short loc_11F3C
		mov	ebx, [di+20h]
		shr	ebx, 4
		add	bx, 102h
		dec	bx
		shr	bx, 0Ah
		inc	bx
		mov	ah, 51h	; 'Q'
		mov	dx, [_ems_handle]
		add	bx, [_ems_log_pagenum]
		push	bx
		int	67h		;  - LIM EMS 4.0 - REALLOCATE PAGES
					; DX = handle
					; BX = number of pages to be allocated to handle
					; Return: BX = actual number of	pages allocated	to handle
					; AH = status
		pop	bx
		cmp	ah, 0
		jnz	short loc_11F3C
		mov	cx, [_ems_log_pagenum]
		mov	[_ems_log_pagenum], bx
		mov	bx, cx
		mov	ax, [_ems_pageframe]
		retn
; ---------------------------------------------------------------------------

loc_11F3C:				; CODE XREF: _ems_realloc2+9j
					; _ems_realloc2+2Dj
		mov	ebx, [di+20h]
		add	ebx, 1020h	; bytes
		call	_memalloc
		mov	cx, 0FFFFh
		retn
endp		_ems_realloc2


; =============== S U B	R O U T	I N E =======================================


proc		_mod_readfile_11F4E far	; CODE XREF: _mod_n_t_module+6Ap
					; _mod_n_t_module+159p ...
		mov	[_byte_24617], 0
		cmp	[_word_24662], 0
		stc
		jnz	short locret_11FD3
		test	[_sndflags_24622], 4
		jnz	short loc_11FD6
		test	[_sndflags_24622], 10h
		jnz	short loc_11FD2
		mov	cx, [_word_245D2]
		mov	di, offset _myout

loc_11F70:				; CODE XREF: _mod_readfile_11F4E+82j
		push	cx
		cmp	[dword ptr di+20h], 0
		jz	short loc_11FCB
		mov	[_byte_24675], 1
		mov	al, [di+3Fh]
		mov	[_byte_24674], al
		push	di
		call	_ems_realloc2
		pop	di
		jb	short loc_11FD4
		mov	[di+30h], ax
		mov	[di+32h], cx
		mov	es, ax
		test	[_moduleflag_246D0], 10111011000b
		jz	short loc_11FA9
		mov	dx, [di+38h]
		mov	cx, [di+3Ah]
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file

loc_11FA9:				; CODE XREF: _mod_readfile_11F4E+4Aj
		mov	bx, [_fhandle_module]
		mov	ecx, [di+20h]
		push	di
		push	es
		mov	dx, [di+32h]
		call	_mod_readfile_12247
		adc	[_word_24662], 0
		pop	es
		assume es:nothing
		pop	di
		mov	ax, es
		push	di
		call	_ems_mapmemx
		pop	di
		or	[byte ptr di+3Ch], 1

loc_11FCB:				; CODE XREF: _mod_readfile_11F4E+28j
		add	di, 40h	; '@'
		pop	cx
		dec	cx
		jnz	short loc_11F70

loc_11FD2:				; CODE XREF: _mod_readfile_11F4E+19j
		clc

locret_11FD3:				; CODE XREF: _mod_readfile_11F4E+Bj
		retn
; ---------------------------------------------------------------------------

loc_11FD4:				; CODE XREF: _mod_readfile_11F4E+3Aj
		pop	cx
		retn
; ---------------------------------------------------------------------------

loc_11FD6:				; CODE XREF: _mod_readfile_11F4E+12j
		mov	eax, 10000h
		mov	cl, [_dma_channel_0]
		call	_alloc_dma_buf
		jb	locret_1221F
		mov	[word ptr _dma_buf_pointer+2], ax
		mov	[word ptr _dma_buf_pointer], 0
		mov	di, offset _myout
		mov	cx, [_word_245D2]

loc_11FF7:				; CODE XREF: _mod_readfile_11F4E+1D9j
		push	cx
		cmp	[dword ptr di+20h], 0
		jz	loc_12106
		inc	[_byte_24617]
		mov	[_byte_24675], 1
		mov	al, [di+3Fh]
		mov	[_byte_24674], al
		test	[_moduleflag_246D0], 10111011000b
		jz	short loc_12027
		mov	dx, [di+38h]
		mov	cx, [di+3Ah]
		mov	bx, [_fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file

loc_12027:				; CODE XREF: _mod_readfile_11F4E+C8j
		test	[byte ptr di+3Ch], 4
		jz	short loc_1206B
		mov	eax, [di+20h]
		add	eax, 1Fh
		and	al, 0E0h
		shr	eax, 2
		mov	bx, [_word_24630]
		shl	bx, 2
		add	ax, bx
		jnb	short loc_12056
		and	[_word_24630], 0C000h
		add	[_word_24630], 4000h
		jb	loc_12117

loc_12056:				; CODE XREF: _mod_readfile_11F4E+F6j
		mov	ax, [_word_24630]
		mov	bx, ax
		and	bx, 0C000h
		and	ax, 3FFFh
		shr	ax, 1
		or	ax, bx		; CODE XREF: _snd_initialze+13j

loc_12066:				; CODE XREF: _snd_initialze+13j
		mov	[di+34h], ax
		jmp	short loc_12071
; ---------------------------------------------------------------------------

loc_1206B:				; CODE XREF: _mod_readfile_11F4E+DDj
		mov	ax, [_word_24630]
		mov	[di+34h], ax

loc_12071:				; CODE XREF: _mod_readfile_11F4E+11Bj
		mov	ecx, [di+20h]

loc_12075:				; CODE XREF: _mod_readfile_11F4E+174j
		cmp	ecx, 8000h
		jbe	short loc_120C4
		sub	ecx, 8000h
		push	ecx
		mov	cx, 8000h
		mov	bx, [_fhandle_module]
		mov	ah, 3Fh	; '?'
		push	di
		push	ds
		lds	dx, [_dma_buf_pointer]
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	ds
		pop	di
		adc	[_word_24662], 0
		les	si, [_dma_buf_pointer]
		assume es:nothing
		mov	cx, 8000h
		call	_mod_sub_12220
		push	di

loc_120AA:
		mov	cx, 8000h
		mov	ax, [_word_24630]
		call	_nongravis_182E7
		xor	[word ptr _dma_buf_pointer], 8000h
		add	[_word_24630], 800h
		pop	di
		pop	ecx
		jmp	short loc_12075
; ---------------------------------------------------------------------------

loc_120C4:				; CODE XREF: _mod_readfile_11F4E+12Ej
		jcxz	short loc_120E7
		mov	bx, [_fhandle_module]
		mov	ah, 3Fh	; '?'
		push	di
		push	cx
		push	ds
		lds	dx, [_dma_buf_pointer]
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	ds
		pop	cx
		pop	di
		push	di
		adc	[_word_24662], 0
		les	si, [_dma_buf_pointer]
		push	cx
		call	_mod_sub_12220
		pop	cx

loc_120E7:				; CODE XREF: _mod_readfile_11F4E:loc_120C4j
		push	cx
		mov	ax, [_word_24630]
		call	_nongravis_182E7
		xor	[word ptr _dma_buf_pointer], 8000h
		pop	ax
		add	ax, 21h	; '!'
		and	al, 0E0h
		shr	ax, 4

loc_120FD:
		add	[_word_24630], ax
		pop	di
		or	[byte ptr di+3Ch], 1

loc_12106:				; CODE XREF: _mod_readfile_11F4E+AFj
		pop	cx
		mov	dx, [_word_24630]
		shr	dx, 1
		mov	al, [_byte_24628]
		shl	ax, 0Dh
		cmp	dx, ax
		jbe	short loc_12123

loc_12117:				; CODE XREF: _mod_readfile_11F4E+104j
		call	_memfree_18A28
		mov	dx, offset _aNotEnoughDramOn ; "Not enough DRAM on UltraSound\r\n"
		mov	ax, 0FFFDh
		jmp	_lfreaderr
; ---------------------------------------------------------------------------

loc_12123:				; CODE XREF: _mod_readfile_11F4E+1C7j
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_11FF7

loc_1212B:				; CODE XREF: _mod_readfile_11F4E+1E2j
		cmp	[_byte_2466E], 1
		jz	short loc_1212B
		call	_memfree_18A28
		mov	di, offset _myout
		mov	cx, [_word_245D2]

loc_1213C:				; CODE XREF: _mod_readfile_11F4E+2CCj
		test	[byte ptr di+3Ch], 1
		jz	loc_12216
		push	cx
		xor	ax, ax
		test	[byte ptr di+3Ch], 4
		jnz	short loc_121B9
		test	[byte ptr di+3Ch], 8
		jz	short loc_1219E
		mov	edx, [di+24h]
		push	edi
		movzx	edi, [word ptr di+34h]
		shl	edi, 4
		add	edi, edx
		inc	edi
		pop	edi
		mov	edx, [di+2Ch]
		push	edi
		movzx	edi, [word ptr di+34h]
		shl	edi, 4
		add	edi, edx
		add	edi, 2
		pop	edi
		mov	edx, [di+24h]
		push	edi
		movzx	edi, [word ptr di+34h]
		shl	edi, 4
		add	edi, edx
		pop	edi

loc_1219E:				; CODE XREF: _mod_readfile_11F4E+203j
		mov	edx, [di+2Ch]
		push	edi
		movzx	edi, [word ptr di+34h]
		shl	edi, 4
		add	edi, edx
		inc	edi
		pop	edi
		jmp	short loc_12215
; ---------------------------------------------------------------------------

loc_121B9:				; CODE XREF: _mod_readfile_11F4E+1FDj
		test	[byte ptr di+3Ch], 8
		jz	short loc_121EE
		mov	edx, [di+24h]
		test	[byte ptr di+3Ch], 10h
		jz	short loc_121CD
		mov	edx, [di+2Ch]

loc_121CD:				; CODE XREF: _mod_readfile_11F4E+279j
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

loc_121EE:				; CODE XREF: _mod_readfile_11F4E+26Fj
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

loc_12215:				; CODE XREF: _mod_readfile_11F4E+269j
		pop	cx

loc_12216:				; CODE XREF: _mod_readfile_11F4E+1F2j
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_1213C
		clc

locret_1221F:				; CODE XREF: _mod_readfile_11F4E+95j
		retn
endp		_mod_readfile_11F4E ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_mod_sub_12220 near	; CODE XREF: _mod_readfile_11F4E+158p
					; _mod_readfile_11F4E+195p ...
		cmp	[_byte_24674], 1
		jz	short loc_12228
		retn
; ---------------------------------------------------------------------------

loc_12228:				; CODE XREF: _mod_sub_12220+5j
		mov	al, [_byte_24676]
		cmp	[_byte_24675], 0
		jz	short loc_12239
		mov	[_byte_24675], 0
		xor	al, al

loc_12239:				; CODE XREF: _mod_sub_12220+10j
					; _mod_sub_12220+21j
		add	al, [es:si]
		mov	[es:si], al
		inc	si
		dec	cx
		jnz	short loc_12239
		mov	[_byte_24676], al
		retn
endp		_mod_sub_12220


; =============== S U B	R O U T	I N E =======================================


proc		_mod_readfile_12247 near	; CODE XREF: _mod_readfile_11F4E+68p
		mov	edi, ecx
		xor	esi, esi
		mov	bp, es

loc_1224F:				; CODE XREF: _mod_readfile_12247+98j
		push	dx
		cmp	dx, 0FFFFh
		jz	short loc_12262
		push	dx
		push	cx
		push	bx
		push	ax
		mov	bx, dx
		call	_ems_mapmem
		pop	ax
		pop	bx
		pop	cx
		pop	dx

loc_12262:				; CODE XREF: _mod_readfile_12247+Cj
		xor	dx, dx
		mov	ecx, 8000h
		cmp	edi, ecx
		ja	short loc_12271
		mov	cx, di

loc_12271:				; CODE XREF: _mod_readfile_12247+26j
		push	bx
		push	esi
		push	edi
		push	bp
		push	es
		push	ds
		mov	ds, bp
		assume ds:nothing
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	ds
		assume ds:seg003
		pushf
		push	ax
		or	ax, ax
		jz	short loc_122B8
		push	ax
		push	bp
		mov	es, bp
		assume es:nothing
		xor	si, si
		mov	cx, ax
		call	_mod_sub_12220
		pop	bp
		pop	ax
		cmp	[_byte_24673], 0
		jz	short loc_122B8
		mov	fs, bp
		assume fs:nothing
		mov	cx, ax
		add	cx, 3
		shr	cx, 2
		jz	short loc_122B8
		mov	edx, 80808080h
		xor	si, si

loc_122AE:				; CODE XREF: _mod_readfile_12247+6Fj
		xor	[fs:si], edx
		add	si, 4
		dec	cx
		jnz	short loc_122AE

loc_122B8:				; CODE XREF: _mod_readfile_12247+3Dj
					; _mod_readfile_12247+51j ...
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

loc_122DA:				; CODE XREF: _mod_readfile_12247+8Bj
		inc	dx
		inc	dx

loc_122DC:				; CODE XREF: _mod_readfile_12247+91j
		sub	edi, eax
		ja	loc_1224F

loc_122E3:				; CODE XREF: _mod_readfile_12247+7Fj
		mov	ecx, esi
		clc

locret_122E7:				; CODE XREF: _mod_readfile_12247+7Bj
		retn
endp		_mod_readfile_12247


; =============== S U B	R O U T	I N E =======================================


proc		_ems_mapmemx near	; CODE XREF: _mod_readfile_11F4E+75p
		test	[byte ptr di+3Ch], 8
		jnz	loc_12386
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		mov	edx, [di+20h]
		add	edx, 800h
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_1234E
		push	eax
		push	ecx
		push	edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem
		pop	edx
		pop	ecx
		pop	eax
		push	eax
		push	ecx
		push	edx
		mov	ebx, edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem2
		pop	edx
		pop	ecx
		pop	eax
		and	ecx, 3FFFh
		and	edx, 3FFFh
		add	edx, 8000h

loc_1234E:				; CODE XREF: _ems_mapmemx+20j
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
		assume es:nothing
		mov	cx, 200h
		cld

loc_1236C:				; CODE XREF: _ems_mapmemx+9Bj
		mov	eax, [es:di]
		mov	[fs:si], eax
		mov	[dword ptr es:di], 0
		add	si, 4
		add	di, 4
		dec	cx
		jnz	short loc_1236C
		retn
; ---------------------------------------------------------------------------

loc_12386:				; CODE XREF: _ems_mapmemx+4j
		push	ax
		push	di
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_123B0
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem
		pop	eax
		pop	ecx
		and	ecx, 3FFFh

loc_123B0:				; CODE XREF: _ems_mapmemx+ADj
		mov	si, cx
		and	si, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	fs, cx
		mov	ecx, [di+20h]
		add	ecx, 800h
		mov	ebx, ecx
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_123EE
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem2
		pop	eax
		pop	ecx
		and	ecx, 3FFFh
		add	cx, 8000h

loc_123EE:				; CODE XREF: _ems_mapmemx+E7j
		mov	bx, cx
		and	bx, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	es, cx
		mov	di, bx
		mov	cx, 200h
		cld
		rep movs [dword	ptr es:di], [dword ptr fs:si]
		pop	di
		pop	ax
		mov	ecx, [di+24h]
		mov	ebx, ecx
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_1242D
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem
		pop	eax
		pop	ecx
		and	ecx, 3FFFh

loc_1242D:				; CODE XREF: _ems_mapmemx+12Aj
		mov	si, cx
		and	si, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	fs, cx
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_12466
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem2
		pop	eax
		pop	ecx
		and	ecx, 3FFFh
		add	cx, 8000h

loc_12466:				; CODE XREF: _ems_mapmemx+15Fj
		mov	bx, cx
		and	bx, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	es, cx
		cmp	[dword ptr di+28h], 800h
		ja	short loc_12497
		mov	edx, [di+28h]
		add	dx, si
		mov	di, bx
		mov	bp, si
		mov	cx, 800h
		cld

loc_1248B:				; CODE XREF: _ems_mapmemx+1ACj
		movs	[byte ptr es:di], [byte	ptr fs:si]
		cmp	si, dx
		jb	short loc_12493
		mov	si, bp

loc_12493:				; CODE XREF: _ems_mapmemx+1A7j
		dec	cx
		jnz	short loc_1248B
		retn
; ---------------------------------------------------------------------------

loc_12497:				; CODE XREF: _ems_mapmemx+193j
		mov	di, bx
		mov	cx, 200h
		cld
		rep movs [dword	ptr es:di], [dword ptr fs:si]
		retn
endp		_ems_mapmemx


; =============== S U B	R O U T	I N E =======================================


proc		_ems_mapmemy near
		test	[byte ptr di+3Ch], 8
		jnz	loc_1253B
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		mov	edx, [di+20h]
		add	edx, 800h
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_12508
		push	eax
		push	ecx
		push	edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem
		pop	edx
		pop	ecx
		pop	eax
		push	eax
		push	ecx
		push	edx
		mov	ebx, edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem2
		pop	edx
		pop	ecx
		pop	eax
		and	ecx, 3FFFh
		and	edx, 3FFFh
		add	edx, 8000h

loc_12508:				; CODE XREF: _ems_mapmemy+20j
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

loc_12529:				; CODE XREF: _ems_mapmemy+96j
		mov	eax, [fs:si]
		mov	[es:di], eax
		add	si, 4
		add	di, 4
		dec	cx
		jnz	short loc_12529
		retn
; ---------------------------------------------------------------------------

loc_1253B:				; CODE XREF: _ems_mapmemy+4j
		mov	ecx, [di+20h]
		add	ecx, 800h
		mov	ebx, ecx
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_12568
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem
		pop	eax
		pop	ecx
		and	ecx, 3FFFh

loc_12568:				; CODE XREF: _ems_mapmemy+ABj
		mov	si, cx
		and	si, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	fs, cx
		mov	ecx, [di+2Ch]
		inc	ecx
		mov	ebx, ecx
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_125A1
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	_ems_mapmem2
		pop	eax
		pop	ecx
		and	ecx, 3FFFh
		add	cx, 8000h

loc_125A1:				; CODE XREF: _ems_mapmemy+E0j
		mov	bx, cx
		and	bx, 0Fh
		shr	ecx, 4
		add	cx, ax
		mov	es, cx
		mov	di, bx
		mov	cx, 200h
		cld
		rep movs [dword	ptr es:di], [dword ptr fs:si]
		retn
endp		_ems_mapmemy


; =============== S U B	R O U T	I N E =======================================


proc		_deinit_125B9 far	; CODE XREF: _start:loc_1907CP
					; _start+1BFP
		pushf
		push	ds
		mov	ax, seg003
		mov	ds, ax
		push	cs
		call	near ptr _snd_offx
		push	cs
		call	near ptr _memfree_125DA
		call	_ems_deinit
		mov	ax, [_word_2460C]
		call	_setmemallocstrat
		call	_snd_deinit
		call	_initclockfromrtc
		pop	ds
		popf
		retf
endp		_deinit_125B9

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		_memfree_125DA far	; CODE XREF: _moduleread+7p
					; _moduleread+ADp ...
		push	ds
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		call	_ems_realloc
		cmp	[word ptr _dword_24640+2], 0
		jz	short loc_125F6
		call	_memfree_18A28
		mov	[_dword_24640], 0

loc_125F6:				; CODE XREF: _memfree_125DA+Ej
		cmp	[_byte_24665], 1
		jnz	short loc_1265B
		test	[_sndflags_24622], 4
		jnz	short loc_1263D
		test	[_sndflags_24622], 10h
		jnz	short loc_1263D
		mov	di, offset _myout
		mov	cx, [_word_245D2]

loc_12612:				; CODE XREF: _memfree_125DA+61j
		push	cx
		test	[byte ptr di+3Ch], 1
		jz	short loc_12636
		cmp	[word ptr di+32h], 0FFFFh
		jnz	short loc_12636
		cmp	[word ptr di+30h], 0
		jz	short loc_12636
		mov	ax, [di+30h]
		push	di
		call	_memfree
		pop	di
		and	[byte ptr di+3Ch], 0FEh
		mov	[word ptr di+30h], 0

loc_12636:				; CODE XREF: _memfree_125DA+3Dj
					; _memfree_125DA+43j ...
		pop	cx
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_12612

loc_1263D:				; CODE XREF: _memfree_125DA+28j
					; _memfree_125DA+2Fj
		mov	di, offset _segs_table
		mov	cx, [_word_245F2]

loc_12644:				; CODE XREF: _memfree_125DA+7Fj
		mov	ax, [di]
		or	ax, ax
		jz	short loc_12655
		push	cx
		push	di
		call	_memfree
		pop	di
		pop	cx
		mov	[word ptr di], 0

loc_12655:				; CODE XREF: _memfree_125DA+6Ej
		add	di, 2
		dec	cx
		jnz	short loc_12644

loc_1265B:				; CODE XREF: _memfree_125DA+21j
		pop	ds
		retf
endp		_memfree_125DA

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		sub_1265D far		; CODE XREF: _read_module+86P
					; _keyb_19EFDP ...
		mov	ax, seg003
		mov	es, ax
		assume es:seg003
		mov	ax, [es:_volume_245FC]
		dec	ax
		mov	cl, al
		mov	si, offset _volume_25908
		mov	di, offset asc_246B0 ; "				"
		movzx	bp, [es:_sndcard_type]
		mov	ch, [es:_byte_24666]
		mov	bh, [es:_byte_24667]
		mov	dl, [es:_sndflags_24622]
		mov	dh, [es:_byte_24628]
		dec	dh
		and	dh, 3
		shl	dh, 1
		or	dh, [es:_byte_24623]
		shl	dh, 1
		or	dh, [es:_byte_24671]
		shl	dh, 3
		mov	al, [byte ptr es:_word_245F6]
		mov	ah, [byte ptr es:_word_245F0]
		retf
endp		sub_1265D


; =============== S U B	R O U T	I N E =======================================


proc		sub_126A9 far		; CODE XREF: _read_module+6AP
					; _text_init2+225P
		mov	ax, seg003
		mov	es, ax
		mov	di, offset asc_246B0 ; "				"
		mov	si, offset _myout
		mov	bl, [byte ptr es:_word_245FA]
		mov	bh, [byte ptr es:_word_245D2]
		mov	cl, [byte ptr es:_word_245D4]
		mov	ch, [es:_byte_24617]
		mov	eax, [es:_module_type_text]
		retf
endp		sub_126A9


; =============== S U B	R O U T	I N E =======================================


proc		_volume_prep far		; CODE XREF: seg001:18BEP
					; _f2_draw_waves+CP ...
		push	ds
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		mov	[_word_24610], ax
		mov	[_my_size], cx
		test	[_sndflags_24622], 4
		jnz	short loc_12702
		push	di
		push	es
		call	_ems_save_mapctx
		pop	es
		assume es:nothing
		pop	di
		mov	si, offset _volume_25908
		mov	dx, [_word_245D4]

loc_126F0:				; CODE XREF: _volume_prep+2Dj
		push	dx
		push	si
		call	_volume_prepare_waves
		pop	si
		pop	dx
		add	si, 50h	; 'P'
		dec	dx
		jnz	short loc_126F0
		call	_ems_restore_mapctx
		pop	ds
		retf
; ---------------------------------------------------------------------------

loc_12702:				; CODE XREF: _volume_prep+12j
		push	di
		push	es
		cmp	[word ptr _dword_24640+2], 0
		jnz	short loc_12721
		mov	eax, 800h
		mov	cl, [_dma_channel_0]
		call	_alloc_dma_buf
		mov	[word ptr _dword_24640+2], ax
		mov	[word ptr _dword_24640],	0

loc_12721:				; CODE XREF: _volume_prep+3Bj
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		cld
		mov	si, offset _volume_25908
		mov	cx, [_word_245D4]

loc_1272D:				; CODE XREF: _volume_prep+87j
		pushf
		cli
		mov	dx, [_gravis_port]
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
		assume es:nothing
		pop	di
		mov	si, offset _volume_25908
		mov	ax, [_word_245D4]

loc_1275F:				; CODE XREF: _volume_prep+C8j
		push	ax
		push	si
		test	[byte ptr si+17h], 1
		jnz	short loc_1276C
		call	_memclean
		jmp	short loc_1278F
; ---------------------------------------------------------------------------

loc_1276C:				; CODE XREF: _volume_prep+97j
					; _volume_prep+A3j
		cmp	[_byte_2466E], 1
		jz	short loc_1276C
		push	si
		push	di
		push	es
		mov	eax, [_dword_24640]
		call	sub_1279A
		pop	es
		pop	di
		pop	si

loc_12780:				; CODE XREF: _volume_prep+B7j
		cmp	[_byte_2466E], 1
		jz	short loc_12780
		lfs	ax, [_dword_24640]
		call	sub_1281A

loc_1278F:				; CODE XREF: _volume_prep+9Cj
		pop	si
		pop	ax
		add	si, 50h	; 'P'
		dec	al
		jnz	short loc_1275F
		pop	ds
		retf
endp		_volume_prep


; =============== S U B	R O U T	I N E =======================================


proc		sub_1279A near		; CODE XREF: _volume_prep+ACp
		mov	[_dma_buf_pointer], eax
		mov	ax, [_word_24610]
		xor	ah, ah
		imul	ax, [si+20h]
		mul	[_my_size]
		shrd	ax, dx,	8
		add	ax, 30h	; '0'
		test	[_word_24610], 8000h
		jz	short loc_127BD
		add	ax, 100h

loc_127BD:				; CODE XREF: sub_1279A+1Ej
		test	[byte ptr si+19h], 4
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
		test	[byte ptr si+19h], 4
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
		cmp	[_byte_2466E], 1
		jz	short loc_127FC
		shr	cx, 1
		push	ds
		lds	di, [_dma_buf_pointer]
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
endp		sub_1279A


; =============== S U B	R O U T	I N E =======================================


proc		sub_1281A near		; CODE XREF: _volume_prep+BEp
		shl	eax, 10h
		mov	ax, [_word_24610]
		xor	ah, ah
		mul	[word ptr si+20h]
		mov	bp, ax
		shr	bp, 8
		mov	dh, al
		xor	dl, dl
		shr	eax, 10h
		jmp	short loc_12898
endp		sub_1281A


; =============== S U B	R O U T	I N E =======================================


proc		_volume_prepare_waves near ; CODE XREF: _volume_prep+24p
		test	[byte ptr si+17h], 1
		jz	_memclean
		test	[_sndflags_24622], 1
		jz	_memclean
		push	di
		push	es
		mov	bx, [si+26h]
		mov	eax, [si+4]
		shr	eax, 22
		add	bx, ax
		push	si
		call	_ems_mapmem
		pop	si
		mov	eax, [si+4]
		mov	bx, ax
		shr	eax, 12
		cmp	[word ptr si+26h], 0FFFFh
		jz	short loc_12870
		and	eax, 3FFh

loc_12870:				; CODE XREF: _volume_prepare_waves+33j
		add	ax, [si+24h]
		mov	fs, ax
		mov	ax, [_word_24610]
		xor	ah, ah
		mul	[word ptr si+20h]
		mul	[_freq1]
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
		movzx	ebx, [byte ptr si+23h]
		mov	si, ax
		test	[_word_24610], 4000h
		jz	short loc_128BB
		cmp	[_amplification], 120
		jbe	short loc_128BB
		mov	ax, 100
		push	dx
		mul	bx
		div	[_amplification]
		pop	dx
		mov	bx, ax

loc_128BB:				; CODE XREF: _volume_prepare_waves+70j
					; _volume_prepare_waves+77j
		shl	ebx, 9
		add	bx, offset _vlm_byte_table
		inc	bx
		mov	cx, [_my_size]
		test	[_word_24610], 8000h
		jz	short loc_1291E
		shl	ecx, 16
		shl	esi, 16
		mov	si, ax
		mov	cx, 100h

loc_128DD:				; CODE XREF: _volume_prepare_waves+DFj
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

loc_12913:				; CODE XREF: _volume_prepare_waves+AFj
					; _volume_prepare_waves+B3j ...
		dec	cx
		jnz	short loc_128DD
		shr	esi, 16

loc_1291A:				; CODE XREF: _volume_prepare_waves+DCj
		shr	ecx, 16

loc_1291E:				; CODE XREF: _volume_prepare_waves+99j
		xor	eax, eax

loc_12921:				; CODE XREF: _volume_prepare_waves+21Cj
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

locret_12A55:				; CODE XREF: _volume_prepare_waves+FCj
					; _volume_prepare_waves+110j ...
		retn
endp		_volume_prepare_waves


; =============== S U B	R O U T	I N E =======================================


proc		_memclean near		; CODE XREF: _volume_prep+99p
					; _volume_prepare_waves+4j ...
		cld
		mov	cx, [_my_size]
		xor	ax, ax
		shr	cx, 1
		rep stosw
		adc	cx, cx
		rep stosb
		retn
endp		_memclean


; =============== S U B	R O U T	I N E =======================================


proc		_volume_12A66 far	; CODE XREF: _vlm_141DF+1p _snd_off+14p
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	cx, [_word_245D4]
		mov	bx, offset _volume_25908

loc_12A73:				; CODE XREF: _volume_12A66+19j
		push	bx
		push	cx
		call	[off_245CE]
		pop	cx
		pop	bx
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_12A73
		pop	ds
		retf
endp		_volume_12A66

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		_change_volume far	; CODE XREF: _keyb_19EFD+17P
					; _keyb_19EFD+23AP ...
		push	ds
		mov	cx, seg003
		mov	ds, cx
		assume ds:seg003
		cmp	ax, -1
		jz	short loc_12AA9
		mov	[_volume_245FC],	ax
		mov	cx, [_word_245D4]
		mov	bx, offset _volume_25908

loc_12A98:				; CODE XREF: _change_volume+24j
		push	bx
		push	cx
		mov	al, [bx+8]
		call	[off_245CC]
		pop	cx
		pop	bx
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_12A98

loc_12AA9:				; CODE XREF: _change_volume+9j
		mov	ax, [_volume_245FC]
		pop	ds
		assume ds:dseg
		retf
endp		_change_volume


; =============== S U B	R O U T	I N E =======================================


proc		_change_amplif far	; CODE XREF: _s3m_module+84p
					; _eff_14020+9p	...
		push	ds
		mov	cx, seg003
		mov	ds, cx
		assume ds:seg003
		cmp	ax, -1
		jz	short loc_12ACE
		mov	[_amplification], ax
		mov	[_byte_24625], 0
		cmp	ax, 100
		jbe	short loc_12ACB
		mov	[_byte_24625], 1

loc_12ACB:				; CODE XREF: _change_amplif+16j
		call	sub_13044

loc_12ACE:				; CODE XREF: _change_amplif+9j
		mov	ax, [_amplification]
		pop	ds
		assume ds:dseg
		retf
endp		_change_amplif


; =============== S U B	R O U T	I N E =======================================


proc		_get_playsettings far	; CODE XREF: _keyb_19EFD+2AP
					; _keyb_19EFD+350P ...
		push	ds
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	al, [_flag_playsetttings]
		pop	ds
		assume ds:dseg
		retf
endp		_get_playsettings


; =============== S U B	R O U T	I N E =======================================


proc		_set_playsettings far	; CODE XREF: _keyb_19EFD+357P
					; _keyb_19EFD+36FP ...
		push	ds
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		mov	[_flag_playsetttings], al
		call	_someplaymode
		and	[byte ptr _config_word+1], 0FEh
		test	[_flag_playsetttings], 10h
		jz	short loc_12AFB
		or	[byte ptr _config_word+1], 1

loc_12AFB:				; CODE XREF: _set_playsettings+16j
		pop	ds
		retf
endp		_set_playsettings


; =============== S U B	R O U T	I N E =======================================


proc		sub_12AFD far		; CODE XREF: _keyb_19EFD+1F9P
		push	ds
		mov	bx, seg003
		mov	ds, bx
		movzx	bx, ch
		cmp	bx, [_word_245D4]
		jnb	short loc_12B16
		imul	bx, 80
		add	bx, offset _volume_25908
		call	_eff_13A43

loc_12B16:				; CODE XREF: sub_12AFD+Dj
		pop	ds
		retf
endp		sub_12AFD


; =============== S U B	R O U T	I N E =======================================


proc		sub_12B18 far		; CODE XREF: _moduleread:loc_10092p
					; sub_12EBA+5Fp
		push	ax
		push	ds
		push	es
		mov	ax, seg003
		mov	es, ax
		assume es:seg003
		mov	di, offset _dword_27BC8
		mov	cx, 8
		cld
		rep movsd
		mov	ds, ax
		mov	[_byte_2461C], 0
		mov	[_byte_2461D], 0
		mov	si, offset _dword_27BC8
		mov	bx, offset _volume_25908
		mov	cx, [_word_245D4]
		xor	al, al

loc_12B42:				; CODE XREF: sub_12B18+65j
		push	ax
		mov	[bx+18h], al
		mov	al, [si]
		mov	[bx+3Ah], al
		test	[_sndflags_24622], 4
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
		inc	[_byte_2461D]
		cmp	al, 80h	; 'Ä'
		jz	short loc_12B75

loc_12B71:				; CODE XREF: sub_12B18+4Fj
		inc	[_byte_2461C]

loc_12B75:				; CODE XREF: sub_12B18+57j
		pop	ax
		add	bx, 80
		inc	si
		inc	al
		dec	cx
		jnz	short loc_12B42
		pop	es
		assume es:nothing
		pop	ds
		pop	ax
		retf
endp		sub_12B18


; =============== S U B	R O U T	I N E =======================================


proc		sub_12B83 far		; CODE XREF: _moduleread+8Bp
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
		mov	[_word_245D4], ax
		mov	di, offset _volume_25908
		mov	cx, [_word_245D4]
		xor	dx, dx
		xor	bx, bx

loc_12BA6:				; CODE XREF: sub_12B83+4Cj
		cmp	[byte ptr di+1Dh], 0
		jnz	short loc_12BB3
		mov	[di+18h], dl
		inc	dl
		jmp	short loc_12BCB
; ---------------------------------------------------------------------------

loc_12BB3:				; CODE XREF: sub_12B83+27j
		cmp	[byte ptr di+1Dh], 1
		jnz	short loc_12BC0
		mov	[di+18h], dh
		inc	dh
		jmp	short loc_12BCB
; ---------------------------------------------------------------------------

loc_12BC0:				; CODE XREF: sub_12B83+34j
		cmp	[byte ptr di+1Dh], 2
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
		mov	[_word_245D6], ax
		mov	al, dh
		mov	[_word_245D8], ax
		mov	al, bl
		mov	[_word_245DA], ax
		test	[_sndflags_24622], 4
		jz	short loc_12BEF
		mov	ax, [_word_245D6]

loc_12BEF:				; CODE XREF: sub_12B83+64j
		call	sub_13044
		call	_someplaymode
		pop	ds
		pop	ax
		retf
endp		sub_12B83


; =============== S U B	R O U T	I N E =======================================


proc		_someplaymode near	; CODE XREF: _set_playsettings+9p
					; sub_12B83+6Fp
		mov	edx, 3
		mov	eax, 1775763456
		mov	ecx, 369D800h
		cmp	[_byte_2461A], 0
		jnz	short loc_12C3C
		mov	edx, 3
		mov	eax, 1643177984
		mov	ecx, 361F0F0h
		test	[_flag_playsetttings], 8
		jnz	short loc_12C3C
		mov	edx, 3
		mov	eax, 1776914432
		mov	ecx, 369E990h

loc_12C3C:				; CODE XREF: _someplaymode+17j
					; _someplaymode+30j
		mov	[_dword_245C0], ecx
		movzx	edi, [_freq1]
		mov	cl, [_byte_2461A]
		shl	edi, cl
		div	edi
		mov	[_dword_245BC], eax
		test	[_sndflags_24622], 4
		jz	short loc_12C86
		movzx	ecx, [_byte_24629]
		mov	eax, 385532977
		test	[_flag_playsetttings], 8
		jnz	short loc_12C75
		mov	eax, 389081954

loc_12C75:				; CODE XREF: _someplaymode+75j
		mul	ecx
		mov	cl, 12
		add	cl, [_byte_2461A]
		shrd	eax, edx, cl
		mov	[_dword_2463C], eax

loc_12C86:				; CODE XREF: _someplaymode+62j
		mov	di, offset _volume_25908
		mov	cx, [_word_245D4]
		xor	ax, ax

loc_12C8F:				; CODE XREF: _someplaymode+9Ej
		mov	[di+3Eh], ax
		add	di, 50h	; 'P'
		dec	cx
		jnz	short loc_12C8F
		retn
endp		_someplaymode

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		_getset_playstate far	; CODE XREF: _keyb_19EFD+401P
					; _keyb_19EFD:loc_1A30DP ...
		push	bx
		push	ds
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		cmp	al, 0FFh
		jz	short loc_12CA7
		mov	[_play_state], al

loc_12CA7:				; CODE XREF: _getset_playstate+9j
		mov	al, [_play_state]
		pop	ds
		assume ds:dseg
		pop	bx
		retf
endp		_getset_playstate


; =============== S U B	R O U T	I N E =======================================


proc		sub_12CAD far		; CODE XREF: _keyb_19EFD+3CCP
					; _keyb_19EFD+3DCP ...
		push	ds
		push	es
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	es, ax
		assume es:seg003
		mov	si, offset _word_246A6
		mov	al, ch
		or	al, 0E0h
		mov	[_word_246A9], bx
		mov	[_byte_246A8], cl
		mov	[_word_246A6], dx
		call	sub_13623
		pop	es
		assume es:nothing
		pop	ds
		retf
endp		sub_12CAD

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		_read_sndsettings far	; CODE XREF: _read_module+7DP
					; _callsubx+3DP
		push	ds
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	al, [_sndcard_type]
		mov	dx, [_snd_base_port]
		mov	cl, [_irq_number]
		mov	ch, [_dma_channel]
		mov	ah, [_freq_246D7]
		mov	bl, [_byte_246D8]
		mov	bh, [_byte_246D9]
		mov	bp, [_freq1]
		test	[_sndflags_24622], 4
		jz	short loc_12CFF
		mov	bp, [_freq2]

loc_12CFF:				; CODE XREF: _read_sndsettings+2Aj
		mov	si, [_config_word]
		pop	ds
		assume ds:dseg
		retf
endp		_read_sndsettings


; =============== S U B	R O U T	I N E =======================================


proc		sub_12D05 far		; CODE XREF: _start-2DP	_start+285P
		push	ds
		push	di
		push	es
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	si, offset _aDeviceNotIniti ; "Device not initialised!"
		cmp	[_snd_init], 1
		jnz	short loc_12D2E
		movzx	si, [_sndcard_type]
		shl	si, 1
		mov	si, offset _covox_txt
		mov	di, offset _chrin
		call	_myasmsprintf
		mov	[byte ptr di], 0
		mov	si, offset _chrin

loc_12D2E:				; CODE XREF: sub_12D05+10j
		pop	es
		assume es:dseg
		pop	di

loc_12D30:
		call	_strcpy_count_0
		pop	ds
		assume ds:dseg
		retf
endp		sub_12D05


; =============== S U B	R O U T	I N E =======================================


proc		sub_12D35 far		; CODE XREF: _dosexec+5CP _dosexec+8BP
		push	ax
		push	bx
		push	ds
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		cmp	al, 1
		jz	short loc_12D4E

loc_12D41:
		mov	[cs:_byte_14F71], 0
		call	_setmemalloc1
		pop	ds
		pop	bx
		pop	ax
		retf
; ---------------------------------------------------------------------------

loc_12D4E:				; CODE XREF: sub_12D35+Aj
		mov	[cs:_byte_14F71], 1
		mov	ax, [_word_2460C]
		call	_setmemallocstrat
		call	_initclockfromrtc
		pop	ds
		pop	bx
		pop	ax
		retf
endp		sub_12D35


; =============== S U B	R O U T	I N E =======================================




		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		sub_12DA8 far		; CODE XREF: _callsubx+24P
		pushf
		cli
		push	ds
		mov	bp, seg003
		mov	ds, bp
		assume ds:seg003
		mov	[_sndcard_type],	al
		mov	[_snd_base_port], dx
		mov	[_irq_number], cl
		mov	[_dma_channel], ch
		mov	[_freq_246D7], ah
		mov	[_byte_246D8], bl
		mov	[_byte_246D9], bh
		movzx	ax, ah
		imul	ax, 1000
		mov	[_freq1], ax
		mov	[_config_word], si
		mov	ax, di
		mov	[_byte_246DC], 4Bh ; 'K'
		mov	[off_245CA], offset sub_13177
		mov	[off_245C8], offset sub_13429
		mov	[off_245CC], offset sub_131EF
		mov	[off_245CE], offset sub_131DA
		mov	[_byte_24623], 0
		mov	[_bit_mode], 8
		mov	[_word_245E8], 400h
		mov	[_snd_set_flag],	0
		mov	al, 8
		call	_getint_vect
		mov	[word ptr cs:_int8addr],	bx
		mov	[word ptr cs:_int8addr+2], dx
		push	cs
		call	near ptr _clean_11C43
		call	_snd_initialze
		jb	loc_12EB2
		call	_getmemallocstrat
		mov	[_word_2460C], ax
		call	_setmemalloc1
		mov	al, [_byte_246DC]
		mov	ah, al
		and	ax, 0F00Fh
		shr	ah, 4
		movzx	di, al
		mov	al, [cs:_byte_13C54+di]
		movzx	di, ah
		mov	ah, [cs:_byte_13C54+di]
		test	[_sndflags_24622], 4
		jnz	short loc_12E55
		mov	ax, 80h	; 'Ä'

loc_12E55:				; CODE XREF: sub_12DA8+A8j
		mov	[_byte_2461E], ah
		mov	[_byte_2461F], al
		push	cs
		call	near ptr _clean_11C43
		mov	al, 0
		test	[byte ptr _config_word+1], 1
		jz	short loc_12E6B
		or	al, 10h

loc_12E6B:				; CODE XREF: sub_12DA8+BFj
		test	[byte ptr _config_word],	4
		jz	short loc_12E74
		or	al, 4

loc_12E74:				; CODE XREF: sub_12DA8+C8j
		test	[byte ptr _config_word],	80h
		jz	short loc_12E7D
		or	al, 8

loc_12E7D:				; CODE XREF: sub_12DA8+D1j
		mov	[_flag_playsetttings], al
		mov	ax, 400h
		mov	cl, [_byte_24623]
		and	cl, 1
		cmp	[_bit_mode], 16
		jnz	short loc_12E9F
		mov	[off_245E0], offset _myin
		mov	[off_245E2], offset _chrin
		inc	cl

loc_12E9F:				; CODE XREF: sub_12DA8+E7j
		shr	ax, cl
		mov	[_word_245E8], ax
		test	[_sndflags_24622], 1
		jz	short loc_12EAE
		call	_ems_init

loc_12EAE:				; CODE XREF: sub_12DA8+101j
		pop	ds
		assume ds:dseg
		popf
		clc
		retf
; ---------------------------------------------------------------------------

loc_12EB2:				; CODE XREF: sub_12DA8+7Bj
		mov	bx, ds
		mov	fs, bx
		assume fs:dseg
		pop	ds
		assume ds:seg003
		popf
		stc
		retf
endp		sub_12DA8

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		sub_12EBA far		; CODE XREF: _read_module+E3P
		pushf
		cli
		push	ds
		push	es
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	[_byte_24669], 0
		mov	[_byte_2466A], 0
		mov	[_byte_2466B], 0
		mov	[_byte_2466C], 0
		mov	[_byte_2466D], 0
		mov	[_byte_24671], 0
		mov	[_play_state], 0
		mov	[_word_24600], 0
		mov	[_word_24602], 0
		mov	[_byte_24620], 0
		mov	[_byte_24621], 0
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		mov	di, offset _volume_25908
		xor	eax, eax
		mov	cx, 280h
		cld
		rep stosd
		xor	ax, ax
		xor	bx, bx
		push	cs
		call	near ptr sub_12F56
		mov	si, offset _dword_27BC8
		push	cs
		call	near ptr sub_12B18
		mov	al, [_byte_2467A]
		call	sub_13CF6
		mov	al, [_byte_24679]
		call	_eff_13CE8
		mov	al, [_byte_24679]
		mov	[_byte_24668], al
		movzx	ax, [_byte_2467A]
		shl	ax, 1
		mov	dl, 5
		div	dl
		mov	[_byte_2467B], al
		mov	[_byte_2467C], 0
		call	_snd_on
		pop	es
		pop	ds
		assume ds:dseg
		popf
		retf
endp		sub_12EBA


; =============== S U B	R O U T	I N E =======================================


proc		_snd_offx far		; CODE XREF: _moduleread+3p
					; _deinit_125B9+8p ...
		pushf
		cli
		push	ds
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		call	_snd_off
		pop	ds
		assume ds:dseg
		popf
		retf
endp		_snd_offx

		assume ds:seg003

; =============== S U B	R O U T	I N E =======================================


proc		sub_12F56 far		; CODE XREF: sub_12EBA+58p
					; _keyb_19EFD+167P ...
		pushf
		cli
		push	ds
		push	es
		mov	cx, seg003
		mov	ds, cx
		mov	[_word_245F0], ax
		mov	[_byte_24669], bl
		push	bx
		call	sub_1415E
		pop	bx
		cmp	bh, 1
		jnz	short loc_12F78
		mov	[_byte_24668], 0
		call	sub_135CA

loc_12F78:				; CODE XREF: sub_12F56+18j
		pop	es
		pop	ds
		popf
		retf
endp		sub_12F56


; =============== S U B	R O U T	I N E =======================================


proc		_get_12F7C far		; CODE XREF: _keyb_19EFD+148P
					; _keyb_19EFD+174P
		pushf
		cli
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	ax, [_word_245F0]
		mov	bx, [_word_245F6]
		pop	ds
		popf
		retf
endp		_get_12F7C


; =============== S U B	R O U T	I N E =======================================


proc		_set_timer_int near	; CODE XREF: _covox_init+2Dp
					; _stereo_init+30p ...
		mov	ebx, 1000h	; bytes
		push	dx		; dx = subrouting offset
		call	_memalloc
		pop	dx
		jb	short locret_12FB3
		mov	[word ptr _dma_buf_pointer], 0
		mov	[word ptr _dma_buf_pointer+2], ax
		push	ax
		push	dx
		call	_memfill8080
		pop	bx
		mov	dx, cs
		mov	al, 8
		call	_setint_vect
		pop	ax
		clc

locret_12FB3:				; CODE XREF: _set_timer_int+Bj
		retn
endp		_set_timer_int


; =============== S U B	R O U T	I N E =======================================


proc		_clean_int8_mem_timr near ; CODE	XREF: _covox_deinitp
					; _stereo_cleanp ...
		mov	dx, [word ptr cs:_int8addr+2]
		mov	bx, [word ptr cs:_int8addr]
		mov	al, 8
		call	_setint_vect
		call	_clean_timer
		mov	ax, [word ptr _dma_buf_pointer+2]
		call	_memfree
		retn
endp		_clean_int8_mem_timr


; =============== S U B	R O U T	I N E =======================================


proc		_configure_timer	near	; CODE XREF: _covox_onp _stereo_setp ...
		call	sub_13017
		pushf
		cli
		mov	dx, 12h
		mov	ax, 34DCh
		div	[_freq1]
		call	_set_timer
		mov	[cs:_byte_14F70], 1
		mov	ax, [_word_245E4]
		mov	[cs:_word_14F6C], ax
		popf
		retn
endp		_configure_timer


; =============== S U B	R O U T	I N E =======================================


proc		_memfill8080 near	; CODE XREF: _set_timer_int+18p
					; _covox_offp ...
		pushf
		cli
		xor	ax, ax
		call	_set_timer
		mov	[cs:_byte_14F70], 0
		mov	[cs:_word_14F6C], 1
		mov	es, [word ptr _dma_buf_pointer+2]
		assume es:nothing
		xor	di, di
		mov	cx, 400h
		mov	eax, 80808080h
		cld
		rep stosd
		popf
		retn
endp		_memfill8080


; =============== S U B	R O U T	I N E =======================================


proc		sub_13017 near		; CODE XREF: _configure_timerp
					; _proaud_setp ...
		mov	di, offset _myout
		mov	cx, [_word_245D2]

loc_1301E:				; CODE XREF: sub_13017+19j
		test	[byte ptr di+3Ch], 8
		jnz	short loc_1302C
		mov	eax, [di+2Ch]
		mov	[di+24h], eax

loc_1302C:				; CODE XREF: sub_13017+Bj
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_1301E
		mov	[_word_24600], 0

loc_13038:				; CODE XREF: sub_13017+2Aj
		call	sub_16C69
		cmp	[_word_24600], 800h
		jbe	short loc_13038
		retn
endp		sub_13017


; =============== S U B	R O U T	I N E =======================================


proc		sub_13044 near		; CODE XREF: _change_amplif:loc_12ACBp
					; sub_12B83:loc_12BEFp
		mov	al, [_byte_2467E]
		cmp	al, 0
		jz	short loc_13080
		cmp	al, 1
		jz	short loc_1305A
		cmp	al, 2
		jz	short loc_1306D
		mov	[_byte_2467E], 0
		jmp	short loc_13080
; ---------------------------------------------------------------------------

loc_1305A:				; CODE XREF: sub_13044+9j
		mov	[_byte_2467D], 3Fh ; '?'
		mov	[off_2462E], offset _table_24798
		mov	[off_24656], offset _table_25221
		jmp	short loc_13091
; ---------------------------------------------------------------------------

loc_1306D:				; CODE XREF: sub_13044+Dj
		mov	[_byte_2467D], 3Fh ; '?'
		mov	[off_2462E], offset _table_24818
		mov	[off_24656], offset _table_25261
		jmp	short loc_13091
; ---------------------------------------------------------------------------

loc_13080:				; CODE XREF: sub_13044+5j
					; sub_13044+14j
		mov	[_byte_2467D], 40h ; '@'
		mov	[off_2462E], offset _table_24716
		mov	[off_24656], offset _table_251E0

loc_13091:				; CODE XREF: sub_13044+27j
					; sub_13044+3Aj
		mov	di, offset _vlm_byte_table
		movzx	eax, [_word_245D6]
		cmp	ax, 2
		ja	short loc_130A2
		mov	ax, 2

loc_130A2:				; CODE XREF: sub_13044+59j
		cmp	[_byte_24623], 1
		jnz	short loc_130AE
		shr	ax, 1
		adc	ax, 0

loc_130AE:				; CODE XREF: sub_13044+63j
		movzx	ebp, ax
		mov	si, [off_24656]
		movzx	cx, [_byte_2467D]
		inc	cx

loc_130BC:				; CODE XREF: sub_13044+122j
		push	cx
		push	ebp
		movzx	eax, [byte ptr si]
		inc	si
		movzx	edx, [_amplification]
		shl	edx, 16
		mul	edx
		mov	ecx, 100
		div	ecx
		xor	edx, edx
		div	ebp
		mov	bp, ax
		shr	eax, 16
		mov	ecx, eax
		cmp	[_byte_24625], 1
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
		mov	[word ptr di], 7FFFh
		jmp	short loc_13131
; ---------------------------------------------------------------------------

loc_13171:				; CODE XREF: sub_13044+112j
		mov	[word ptr di], 8000h
		jmp	short loc_1315A
endp		sub_13044


; =============== S U B	R O U T	I N E =======================================


proc		sub_13177 near		; CODE XREF: sub_13429+4Ap
					; DATA XREF: sub_12DA8+38o
		or	ax, ax
		jz	short locret_131B2
		or	[byte ptr bx+3Dh], 4
		cmp	[byte ptr bx+1Dh], 1
		jz	short loc_131B3
		cmp	ax, [bx+3Eh]
		jz	short locret_131B2
		mov	[bx+3Eh], ax
		movzx	edi, ax
		xor	edx, edx
		mov	eax, [_dword_245BC]
		div	edi
		mov	[bx+20h], ax
		mov	cl, [_byte_2461A]
		shl	edi, cl
		xor	edx, edx
		mov	eax, [_dword_245C0]
		div	edi
		mov	[bx+1Eh], ax

locret_131B2:				; CODE XREF: sub_13177+2j
					; sub_13177+11j
		retn
; ---------------------------------------------------------------------------

loc_131B3:				; CODE XREF: sub_13177+Cj
					; _gravis_13215+Cj
		movzx	edi, ax
		xor	edx, edx
		mov	cl, [_byte_2461A]
		shl	edi, cl
		xor	edx, edx
		mov	eax, [_dword_245C0]
		div	edi
		mov	[bx+1Eh], ax
		retn
endp		sub_13177


; =============== S U B	R O U T	I N E =======================================


proc		_nullsub_5 near		; CODE XREF: sub_131DA+4j
					; _gravis_13272+4j
		retn
endp		_nullsub_5

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_131EF

loc_131D0:				; CODE XREF: sub_131EF+4j
					; _gravis_132A9+4j ...
		xor	ah, ah
		imul	ax, [_volume_245FC]
		xor	al, al
		retn
; END OF FUNCTION CHUNK	FOR sub_131EF

; =============== S U B	R O U T	I N E =======================================


proc		sub_131DA near		; CODE XREF: sub_13429+74j
					; DATA XREF: sub_12DA8+4Ao
		cmp	[byte ptr bx+1Dh], 1
		jz	short _nullsub_5
		test	[byte ptr bx+17h], 1
		jz	short locret_131EE
		and	[byte ptr bx+17h], 0FEh
		mov	[byte ptr bx+35h], 0

locret_131EE:				; CODE XREF: sub_131DA+Aj
		retn
endp		sub_131DA


; =============== S U B	R O U T	I N E =======================================


proc		sub_131EF near		; CODE XREF: sub_13429+4Fp
					; sub_13429+55p
					; DATA XREF: ...

; FUNCTION CHUNK AT 31D0 SIZE 0000000A BYTES

		cmp	[byte ptr bx+1Dh], 1
		jz	short loc_131D0
		and	[byte ptr bx+3Dh], 0BFh
		cmp	al, [_byte_2467D]
		jbe	short loc_13202
		mov	al, [_byte_2467D]

loc_13202:				; CODE XREF: sub_131EF+Ej
		xor	ah, ah
		mov	[bx+22h], al
		mul	[_volume_245FC]
		mov	al, [bx+23h]
		mov	[bx+36h], ax
		mov	[bx+23h], ah
		retn
endp		sub_131EF


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


proc		sub_13429 near		; DATA XREF: sub_12DA8+3Eo
		test	[byte ptr bx+17h], 4
		jz	short locret_13498
		mov	al, [bx+2]
		cmp	al, [bx+3]
		jz	short loc_13471
		mov	[bx+3],	al
		dec	al
		xor	ah, ah
		shl	ax, 6
		mov	di, ax
		add	di, offset _myout
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
		test	[byte ptr bx+17h], 2
		jnz	short loc_13499
		or	[byte ptr bx+17h], 1
		movzx	eax, [word ptr bx+4Ch]
		shl	eax, 8
		mov	[bx+4],	eax

locret_13498:				; CODE XREF: sub_13429+4j
		retn
; ---------------------------------------------------------------------------

loc_13499:				; CODE XREF: sub_13429+5Cj
		test	[byte ptr bx+17h], 1
		jnz	sub_131DA
		retn
endp		sub_13429


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


proc		sub_135CA near		; CODE XREF: sub_12F56+1Fp
					; sub_140B6+3Cp ...
		mov	bx, offset _volume_25908
		mov	cx, [_word_245D4]
		xor	ax, ax

loc_135D3:				; CODE XREF: sub_135CA+1Aj
		mov	[byte ptr bx+3Dh], 0
		test	[byte ptr bx+17h], 10h
		jnz	short loc_135E0
		mov	[bx+0Ah], ax

loc_135E0:				; CODE XREF: sub_135CA+11j
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_135D3
		les	si, [_pointer_245B4]
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
		mov	[word ptr _pointer_245B4], si
		mov	bx, offset _volume_25908
		mov	cx, [_word_245D4]

loc_13608:				; CODE XREF: sub_135CA+56j
		test	[byte ptr bx+17h], 1
		jz	short loc_1361C
		test	[byte ptr bx+3Dh], 0Ch
		jnz	short loc_1361C
		mov	ax, [bx]
		push	cx
		call	[off_245CA]
		pop	cx

loc_1361C:				; CODE XREF: sub_135CA+42j
					; sub_135CA+48j
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_13608
		retn
endp		sub_135CA


; =============== S U B	R O U T	I N E =======================================


proc		sub_13623 near		; CODE XREF: sub_12CAD+1Cp
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
		cmp	ax, [_word_245D4]
		jnb	loc_137BE
		shl	ax, 4
		mov	bx, ax
		shl	ax, 2
		add	bx, ax
		add	bx, offset _volume_25908
		test	dh, 80h
		jz	short loc_13661

loc_13646:
		and	dh, 7Fh
		mov	ax, [es:si]
		add	si, 2
		or	ax, ax
		jz	short loc_13661
		and	[byte ptr bx+17h], 0EFh
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
		cmp	ax, [_word_245D2]
		ja	loc_13718
		dec	ax
		shl	ax, 6
		mov	di, ax
		add	di, offset _myout
		and	[byte ptr bx+17h], 0FBh
		mov	al, [di+3Ch]
		and	al, 1
		shl	al, 2
		or	[bx+17h], al
		or	[byte ptr bx+3Dh], 10h
		mov	[bx+2],	dh
		mov	[word ptr bx+4Ch], 0
		test	[byte ptr bx+17h], 40h
		jz	short loc_136CB
		and	[byte ptr bx+17h], 0BFh
		mov	[byte ptr bx+3], 0

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
		add	ax, offset _word_24998
		mov	[bx+38h], ax
		mov	ax, [_freq_245DE]
		mov	cx, [di+36h]
		jcxz	short loc_13705
		mov	ax, cx

loc_13705:				; CODE XREF: sub_13623+DEj
		mov	[bx+14h], ax
		test	[byte ptr bx+3Dh], 40h
		jnz	short loc_13718
		mov	al, [di+3Dh]
		mov	[bx+8],	al
		or	[byte ptr bx+3Dh], 40h

loc_13718:				; CODE XREF: sub_13623+66j
					; sub_13623+71j ...
		or	dl, dl
		jz	sub_137D5
		cmp	dl, 0FEh ; '˛'
		jz	loc_137CE
		cmp	dl, 0FFh
		jz	sub_137D5
		mov	[bx+35h], dl
		or	[byte ptr bx+3Dh], 8
		test	[_sndflags_24622], 10h
		jnz	short loc_13742
		test	[byte ptr bx+17h], 4
		jz	loc_137CE

loc_13742:				; CODE XREF: sub_13623+115j
		mov	al, [bx+35h]
		call	sub_13826
		xchg	ax, [bx]
		test	[byte ptr bx+3Dh], 80h
		jz	short loc_13791
		mov	[_word_245DC], ax
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
		call	[off_245C8]
		test	[byte ptr bx+9], 4
		jnz	short loc_1379F
		mov	[byte ptr bx+0Dh], 0

loc_1379F:				; CODE XREF: sub_13623+176j
		test	[byte ptr bx+9], 40h
		jnz	short loc_137A9
		mov	[byte ptr bx+0Fh], 0

loc_137A9:				; CODE XREF: sub_13623+180j
		movzx	di, [byte ptr bx+0Ah]
		cmp	di, 32
		ja	_eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		jmp	[cs:_effoff_18FA2+di]
; ---------------------------------------------------------------------------

loc_137BE:				; CODE XREF: sub_13623+Cj
		movzx	di, dh
		shr	di, 5
		mov	al, [cs:_byte_11C29+di]
		xor	ah, ah
		add	si, ax
		retn
; ---------------------------------------------------------------------------

loc_137CE:				; CODE XREF: sub_13623+FEj
					; sub_13623+11Bj
		call	sub_137D5
		jmp	[off_245CE]
endp		sub_13623 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_137D5 near		; CODE XREF: sub_13623+5Aj
					; sub_13623+F7j ...
		test	[byte ptr bx+3Dh], 40h
		jnz	short loc_137F0
		movzx	di, [byte ptr bx+0Ah]
		cmp	di, 32
		ja	_eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		jmp	[cs:_effoff_18F60+di]
; ---------------------------------------------------------------------------

loc_137F0:				; CODE XREF: sub_137D5+4j
		movzx	di, [byte ptr bx+0Ah]
		cmp	di, 32
		ja	_eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		call	[cs:_effoff_18F60+di]
		test	[byte ptr bx+3Dh], 40h
		jz	short locret_13812
		mov	al, [bx+8]
		jmp	[off_245CC]
; ---------------------------------------------------------------------------

locret_13812:				; CODE XREF: sub_137D5+34j
		retn
endp		sub_137D5


; =============== S U B	R O U T	I N E =======================================


proc		sub_13813 near		; CODE XREF: sub_140B6+24p
					; sub_140B6+4Ap ...
		movzx	di, [byte ptr bx+0Ah]
		cmp	di, 32
		ja	short _eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		jmp	[cs:_effoff_18FE4+di]
endp		sub_13813


; =============== S U B	R O U T	I N E =======================================


proc		sub_13826 near		; CODE XREF: sub_13623+122p
					; sub_13623+5D7p ...
		mov	cl, al
		movzx	di, cl
		dec	di
		and	di, 0Fh
		shl	di, 1
		shr	cl, 4
		cmp	[_byte_2461A], 0
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
		sub	di, offset _word_246DE

loc_1386C:				; CODE XREF: sub_13826+13j
		mov	ax, [_word_246DE+di]
		shr	ax, cl
		mov	cx, [bx+14h]
		jcxz	short locret_1387D
		mul	[_freq_245DE]
		div	cx

locret_1387D:				; CODE XREF: sub_13826+4Fj
		retn
endp		sub_13826


; =============== S U B	R O U T	I N E =======================================


proc		_eff_nullsub near	; CODE XREF: sub_13623+18Dj
					; sub_13623+196j ...
		retn
endp		_eff_nullsub


; =============== S U B	R O U T	I N E =======================================


proc		_eff_1387F near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[_byte_24668], 0
		jnz	short _eff_nullsub
endp		_eff_1387F ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13886 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		shl	ax, 4

loc_1388B:				; CODE XREF: _eff_13DE5+5j
		sub	[bx], ax
		cmp	[word ptr bx], 0A0h ; '†'
		jge	short loc_13897
		mov	[word ptr bx], 0A0h ; '†'

loc_13897:				; CODE XREF: _eff_13886+Bj
		mov	ax, [bx]
		jmp	[off_245CA]
endp		_eff_13886


; =============== S U B	R O U T	I N E =======================================


proc		_eff_1389D near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[_byte_24668], 0
		jnz	short _eff_nullsub
endp		_eff_1389D ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		_eff_138A4 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		shl	ax, 4

loc_138A9:				; CODE XREF: _eff_13DEF+5j
		add	[bx], ax
		jb	short loc_138B3
		cmp	[word ptr bx], 13696
		jbe	short loc_138B7

loc_138B3:				; CODE XREF: _eff_138A4+7j
		mov	[word ptr bx], 13696

loc_138B7:				; CODE XREF: _eff_138A4+Dj
		mov	ax, [bx]
		jmp	[off_245CA]
endp		_eff_138A4

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_138BD:				; CODE XREF: sub_13623+138j
					; sub_13623+13Ej
		mov	ax, [bx]
		cmp	ax, [_word_245DC]
		jnz	short loc_138C7
		xor	ax, ax

loc_138C7:				; CODE XREF: sub_13623+2A0j
		mov	[bx+10h], ax
		mov	ax, [_word_245DC]
		mov	[bx], ax
		jmp	sub_137D5
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


proc		_eff_138D2 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_138DE
		xor	ah, ah
		shl	ax, 4
		mov	[bx+12h], ax

loc_138DE:				; CODE XREF: _eff_138D2+2j _eff_139AC+3j ...
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

loc_138F6:				; CODE XREF: _eff_138D2+1Aj
		sub	[bx], dx
		cmp	ax, [bx]
		jl	short loc_1390B

loc_138FC:				; CODE XREF: _eff_138D2+22j
		mov	[bx], ax
		mov	[word ptr bx+10h], 0
		and	[byte ptr bx+17h], 0EFh
		jmp	[off_245CA]
; ---------------------------------------------------------------------------

loc_1390B:				; CODE XREF: _eff_138D2+20j
					; _eff_138D2+28j
		test	[byte ptr bx+17h], 20h
		jnz	short loc_13917
		mov	ax, [bx]
		jmp	[off_245CA]
; ---------------------------------------------------------------------------

loc_13917:				; CODE XREF: _eff_138D2+3Dj
		mov	di, [bx+38h]
		mov	ax, [bx]
		mov	cx, 3Bh	; ';'

loc_1391F:				; CODE XREF: _eff_138D2+55j
		cmp	[di], ax
		jbe	short loc_13929
		add	di, 2
		dec	cx
		jnz	short loc_1391F

loc_13929:				; CODE XREF: _eff_138D2+4Fj
		mov	ax, [di]
		jmp	[off_245CA]
endp		_eff_138D2


; =============== S U B	R O U T	I N E =======================================


proc		_eff_1392F near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	cl, 3

loc_13931:				; CODE XREF: _eff_13E2D+2j
		or	al, al
		jz	short loc_13950
		mov	ch, al
		mov	dl, [bx+0Ch]
		and	al, 0Fh
		jz	short loc_13943
		and	dl, 0F0h
		or	dl, al

loc_13943:				; CODE XREF: _eff_1392F+Dj
		and	ch, 0F0h
		jz	short loc_1394D
		and	dl, 0Fh
		or	dl, ch

loc_1394D:				; CODE XREF: _eff_1392F+17j
		mov	[bx+0Ch], dl

loc_13950:				; CODE XREF: _eff_1392F+4j _eff_139B2+5j ...
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

loc_1396D:				; CODE XREF: _eff_1392F+38j
		mov	dl, al
		test	[byte ptr bx+0Dh], 80h
		jz	short loc_13981
		mov	dl, 0FFh
		sub	dl, al
		jmp	short loc_13981
; ---------------------------------------------------------------------------

loc_1397B:				; CODE XREF: _eff_1392F+30j
		mov	di, ax
		mov	dl, [_table_251C0+di]

loc_13981:				; CODE XREF: _eff_1392F+3Cj
					; _eff_1392F+44j ...
		mov	al, [bx+0Ch]
		mov	dh, al
		and	al, 0Fh
		mul	dl
		mov	ch, [_flag_playsetttings]
		and	ch, 1
		add	cl, ch
		shr	ax, cl
		test	[byte ptr bx+0Dh], 80h
		jz	short loc_1399D
		neg	ax

loc_1399D:				; CODE XREF: _eff_1392F+6Aj
		add	ax, [bx]
		shr	dh, 2
		and	dh, 3Ch
		add	[bx+0Dh], dh
		jmp	[off_245CA]
endp		_eff_1392F


; =============== S U B	R O U T	I N E =======================================


proc		_eff_139AC near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	_eff_13AD7
		jmp	loc_138DE
endp		_eff_139AC


; =============== S U B	R O U T	I N E =======================================


proc		_eff_139B2 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	_eff_13AD7
		mov	cl, 3
		jmp	short loc_13950
endp		_eff_139B2


; =============== S U B	R O U T	I N E =======================================


proc		_eff_139B9 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_139D8
		mov	cl, al
		mov	dl, [bx+0Eh]
		and	al, 0Fh
		jz	short loc_139CB
		and	dl, 0F0h
		or	dl, al

loc_139CB:				; CODE XREF: _eff_139B9+Bj
		and	cl, 0F0h
		jz	short loc_139D5
		and	dl, 0Fh
		or	dl, cl

loc_139D5:				; CODE XREF: _eff_139B9+15j
		mov	[bx+0Eh], dl

loc_139D8:				; CODE XREF: _eff_139B9+2j
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

loc_139F8:				; CODE XREF: _eff_139B9+39j
		mov	dl, al
		test	[byte ptr bx+0Fh], 80h
		jz	short loc_13A0C
		mov	dl, 0FFh
		sub	dl, al
		jmp	short loc_13A0C
; ---------------------------------------------------------------------------

loc_13A06:				; CODE XREF: _eff_139B9+31j
		mov	di, ax
		mov	dl, [_table_251C0+di]

loc_13A0C:				; CODE XREF: _eff_139B9+3Dj
					; _eff_139B9+45j ...
		mov	al, [bx+0Eh]
		mov	dh, al
		and	al, 0Fh
		mul	dl
		shr	ax, 6
		mov	ah, al
		mov	al, [bx+8]
		test	[byte ptr bx+0Fh], 80h
		jnz	short loc_13A30
		add	al, ah
		cmp	al, [_byte_2467D]
		jbe	short loc_13A36
		mov	al, [_byte_2467D]
		jmp	short loc_13A36
; ---------------------------------------------------------------------------

loc_13A30:				; CODE XREF: _eff_139B9+68j
		sub	al, ah
		jns	short loc_13A36
		xor	al, al

loc_13A36:				; CODE XREF: _eff_139B9+70j
					; _eff_139B9+75j ...
		shr	dh, 2
		and	dh, 3Ch
		add	[bx+0Fh], dh
		jmp	[off_245CC]
endp		_eff_139B9


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13A43 near		; CODE XREF: sub_12AFD+16p
					; sub_13623+196j ...
		cmp	al, 0A4h ; '§'
		jz	short loc_13A5B
		cmp	al, 0A5h ; '•'
		jz	short loc_13A60
		cmp	al, 0A6h ; '¶'
		jz	short loc_13A65
		cmp	al, 80h	; 'Ä'
		ja	short locret_13A5A
		test	[_sndflags_24622], 4

locret_13A5A:				; CODE XREF: _eff_13A43+Ej
		retn
; ---------------------------------------------------------------------------

loc_13A5B:				; CODE XREF: _eff_13A43+2j
		or	[byte ptr bx+17h], 80h
		retn
; ---------------------------------------------------------------------------

loc_13A60:				; CODE XREF: _eff_13A43+6j
		and	[byte ptr bx+17h], 7Fh
		retn
; ---------------------------------------------------------------------------

loc_13A65:				; CODE XREF: _eff_13A43+Aj
		xor	[byte ptr bx+17h], 80h
		retn
endp		_eff_13A43


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


proc		_eff_13A94 near		; CODE XREF: sub_137D5+16j
					; sub_137D5+2Bp ...
		or	al, al
		jz	short loc_13A9B
		mov	[bx+16h], al

loc_13A9B:				; CODE XREF: _eff_13A94+2j
		movzx	eax, [byte ptr bx+16h]
		shl	eax, 8
		cmp	eax, [bx+30h]
		ja	short loc_13AAE
		mov	[bx+4Ch], ax
		retn
; ---------------------------------------------------------------------------

loc_13AAE:				; CODE XREF: _eff_13A94+14j
		cmp	[_byte_2461A], 0
		jnz	short loc_13AC6
		call	[off_245CE]
		and	[byte ptr bx+17h], 0FBh
		or	[byte ptr bx+17h], 40h
		mov	[byte ptr bx+3], 0
		retn
; ---------------------------------------------------------------------------

loc_13AC6:				; CODE XREF: _eff_13A94+1Fj
		mov	eax, [bx+30h]
		mov	[bx+4Ch], ax
		retn
endp		_eff_13A94

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13ACE:				; CODE XREF: sub_13623+144j
		mov	al, [bx+0Bh]
		call	_eff_13A94
		jmp	loc_13791
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


proc		_eff_13AD7 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, [bx+8]
		test	al, 0F0h
		jnz	short loc_13AEF

loc_13ADE:				; CODE XREF: _eff_13E32+1Ej
					; _eff_13E32+36j ...
		and	al, 0Fh

loc_13AE0:				; CODE XREF: _eff_13C95+8j
		sub	dl, al
		mov	al, dl
		jnb	short loc_13AE8
		xor	al, al

loc_13AE8:				; CODE XREF: _eff_13AD7+Dj
		mov	[bx+8],	al
		jmp	[off_245CC]
; ---------------------------------------------------------------------------

loc_13AEF:				; CODE XREF: _eff_13AD7+5j
					; _eff_13E32+27j ...
		shr	al, 4

loc_13AF2:				; CODE XREF: _eff_13C88+8j
		add	dl, al
		mov	al, dl
		cmp	al, [_byte_2467D]
		jbe	short loc_13AFF
		mov	al, [_byte_2467D]

loc_13AFF:				; CODE XREF: _eff_13AD7+23j
		mov	[bx+8],	al
		jmp	[off_245CC]
endp		_eff_13AD7


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13B06 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		dec	ax
		mov	[_word_245F0], ax
		inc	ax
		test	[_flag_playsetttings], 4
		jnz	short loc_13B5B
		bt	[word ptr _byte_282E8], ax
		jnb	short loc_13B5B
		mov	cx, [_word_245FA]
		add	cx, 7
		shr	cx, 3
		jz	short loc_13B34
		xor	di, di

loc_13B29:				; CODE XREF: _eff_13B06+2Cj
		cmp	[_byte_282E8+di], 0FFh
		jnz	short loc_13B3E
		inc	di
		dec	cx
		jnz	short loc_13B29

loc_13B34:				; CODE XREF: _eff_13B06+1Fj
					; _eff_13B06+4Ej
		push	bx
		push	si
		push	es
		call	_vlm_141DF
		pop	es
		pop	si
		pop	bx
		retn
; ---------------------------------------------------------------------------

loc_13B3E:				; CODE XREF: _eff_13B06+28j
		mov	al, [_byte_282E8+di]
		shl	di, 3
		mov	cx, 8

loc_13B48:				; CODE XREF: _eff_13B06+48j
		shr	al, 1
		jnb	short loc_13B50
		inc	di
		dec	cx
		jnz	short loc_13B48

loc_13B50:				; CODE XREF: _eff_13B06+44j
		cmp	di, [_word_245FA]
		jnb	short loc_13B34
		dec	di
		mov	[_word_245F0], di

loc_13B5B:				; CODE XREF: _eff_13B06+Cj
					; _eff_13B06+13j ...
		mov	[_byte_24669], 0
		mov	[_byte_2466A], 1
		retn
endp		_eff_13B06

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13B66:				; CODE XREF: sub_13623+14Aj
		mov	al, [bx+0Bh]
		cmp	al, [_byte_2467D]
		jbe	short loc_13B72
		mov	al, [_byte_2467D]

loc_13B72:				; CODE XREF: sub_13623+54Aj
		mov	[bx+8],	al
		jmp	loc_13791
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


proc		_eff_13B78 near		; CODE XREF: sub_137D5+16j
					; sub_137D5+2Bp ...
		cmp	al, [_byte_2467D]
		jbe	short loc_13B81
		mov	al, [_byte_2467D]

loc_13B81:				; CODE XREF: _eff_13B78+4j
		mov	[bx+8],	al
		jmp	[off_245CC]
endp		_eff_13B78


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13B88 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, al
		and	dl, 0Fh
		shr	al, 4
		mov	ah, 0Ah
		mul	ah
		add	al, dl
		cmp	al, 3Fh	; '?'
		ja	short loc_13B5B
		mov	[_byte_24669], al
		mov	[_byte_2466A], 1
		retn
endp		_eff_13B88


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13BA3 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	di, ax
		shr	di, 3
		and	di, 1Eh
		and	al, 0Fh
		jmp	[cs:_effoff_19026+di]
endp		_eff_13BA3


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13BB2 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13BBB
		or	[byte ptr bx+17h], 20h
		retn
; ---------------------------------------------------------------------------

loc_13BBB:				; CODE XREF: _eff_13BB2+2j
		and	[byte ptr bx+17h], 0DFh
		retn
endp		_eff_13BB2


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13BC0 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	[byte ptr bx+9], 0F0h
		or	[bx+9],	al
		retn
endp		_eff_13BC0


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13BC8 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	ax, 0Fh
		mov	di, ax
		cmp	[_byte_2461A], 0
		jnz	short loc_13BE7
		shl	di, 3
		mov	ax, di
		neg	ax
		shl	di, 4
		add	ax, di
		add	ax, offset _word_24998
		mov	[bx+38h], ax
		retn
; ---------------------------------------------------------------------------

loc_13BE7:				; CODE XREF: _eff_13BC8+Aj
		shl	di, 1
		mov	ax, [_table_246F6+di]
		mov	[bx+14h], dx
		retn
endp		_eff_13BC8

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13BF1:				; CODE XREF: sub_13623+151j
		mov	al, [bx+0Bh]
		call	_eff_13BC8
		mov	al, [bx+35h]
		call	sub_13826
		mov	[bx], ax
		jmp	loc_13791
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


proc		_eff_13C02 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[_byte_24668], 0
		jnz	locret_13CF4
		or	al, al
		jz	short loc_13C2D
		cmp	[byte ptr bx+3Ch], 0
		jnz	short loc_13C1A
		inc	al
		mov	[bx+3Ch], al

loc_13C1A:				; CODE XREF: _eff_13C02+11j
		dec	[byte ptr bx+3Ch]
		jz	locret_13CF4
		mov	al, [bx+3Bh]
		mov	[_byte_24669], al
		mov	[_byte_2466B], 1
		retn
; ---------------------------------------------------------------------------

loc_13C2D:				; CODE XREF: _eff_13C02+Bj
		mov	ax, [_word_245F6]
		mov	[bx+3Bh], al
		retn
endp		_eff_13C02


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13C34 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	[byte ptr bx+9], 0Fh
		shl	al, 4
		or	[bx+9],	al
		retn
endp		_eff_13C34


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13C3F near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[_byte_24668], 0
		jz	short loc_13C47
		retn
; ---------------------------------------------------------------------------

loc_13C47:				; CODE XREF: _eff_13C3F+5j
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:_byte_13C54+di]
		jmp	_eff_13A43
endp		_eff_13C3F

; ---------------------------------------------------------------------------
_byte_13C54	db 0,9,12h,1Bh,24h,2Dh,36h,40h,40h,4Ah,53h,5Ch,65h,6Eh
					; DATA XREF: _mtm_module+43r
					; _far_module+55r ...
		db 77h,80h

; =============== S U B	R O U T	I N E =======================================


proc		_eff_13C64 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	locret_13CF4
		cmp	[_byte_24668], 0
		jnz	short loc_13C77
		test	[byte ptr bx+3Dh], 8
		jnz	short locret_13CF4

loc_13C77:				; CODE XREF: _eff_13C64+Bj
		mov	dl, al
		movzx	ax, [_byte_24668]
		div	dl
		or	ah, ah
		jnz	short locret_13CF4
		jmp	[off_245C8]
endp		_eff_13C64


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13C88 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, [bx+8]
		cmp	[_byte_24668], 0
		jz	loc_13AF2
		retn
endp		_eff_13C88


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13C95 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, [bx+8]
		cmp	[_byte_24668], 0
		jz	loc_13AE0
		retn
endp		_eff_13C95


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13CA2 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	al, [_byte_24668]
		jnz	short locret_13CF4
		xor	al, al
		jmp	[off_245CC]
endp		_eff_13CA2

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13CAE:				; CODE XREF: sub_13623+158j
		mov	al, [bx+0Bh]
		and	al, 0Fh
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


proc		_eff_13CB3 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	al, [_byte_24668]
		jnz	short locret_13CF4
		cmp	[word ptr bx], 0
		jz	short locret_13CF4
		mov	[byte ptr bx+0Ah], 0
		mov	[byte ptr bx+0Bh], 0
		jmp	loc_13791
endp		_eff_13CB3


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13CC9 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[_byte_24668], 0
		jnz	short locret_13CF4
		cmp	[_byte_2466D], 0
		jnz	short locret_13CF4
		inc	al
		mov	[_byte_2466C], al
		retn
endp		_eff_13CC9


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13CDD near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		test	[_flag_playsetttings], 2
		jnz	short _eff_13CE8
		cmp	al, 20h	; ' '
		ja	short sub_13CF6
endp		_eff_13CDD ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13CE8 near		; CODE XREF: sub_12EBA+6Bp
					; sub_13623+196j ...
		or	al, al
		jz	short locret_13CF5
		mov	[_byte_24667], al
		mov	[_byte_24668], 0

locret_13CF4:				; CODE XREF: _eff_138D2+11j
					; _eff_13C02+5j	...
		retn
; ---------------------------------------------------------------------------

locret_13CF5:				; CODE XREF: _eff_13CE8+2j
		retn
endp		_eff_13CE8


; =============== S U B	R O U T	I N E =======================================


proc		sub_13CF6 near		; CODE XREF: sub_12EBA+65p
					; _eff_13CDD+9j	...

; FUNCTION CHUNK AT 3DB0 SIZE 00000011 BYTES

		xor	ah, ah
		mov	[_byte_24666], al
		mov	cx, ax
		mov	dl, 91
		div	dl
		inc	al
		mov	[cs:_byte_14F72], al
		mov	[cs:_byte_14F73], al
		test	[_sndflags_24622], 4
		jnz	short loc_13D4B
		test	[_sndflags_24622], 10h
		jnz	_settimer
		shl	cx, 1
		mov	ax, 5
		mul	[_freq1]
		div	cx
		xor	dx, dx
		div	[_word_245E8]
		inc	ax
		or	dx, dx
		jnz	short loc_13D36
		dec	ax
		mov	dx, [_word_245E8]

loc_13D36:				; CODE XREF: sub_13CF6+39j
		mov	[_word_245EA], dx
		mov	[_word_245EC], ax
		mov	[_word_245EE], ax
		mov	ax, [_word_245E8]
		mov	[_word_245E4], ax
		mov	[cs:_word_14F6C], ax
		retn
; ---------------------------------------------------------------------------

loc_13D4B:				; CODE XREF: sub_13CF6+1Aj
		call	sub_13D95
		mov	ah, al
		pushf
		cli
		mov	dx, [_gravis_port]
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
endp		sub_13CF6 ; sp-analysis	failed

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13D95

loc_13D8D:				; CODE XREF: sub_13D95+10j
		shl	cx, 1
		inc	[_byte_24618]
		jmp	short loc_13D9A
; END OF FUNCTION CHUNK	FOR sub_13D95

; =============== S U B	R O U T	I N E =======================================


proc		sub_13D95 near		; CODE XREF: sub_13CF6:loc_13D4Bp

; FUNCTION CHUNK AT 3D8D SIZE 00000008 BYTES

		mov	[_byte_24618], 1

loc_13D9A:				; CODE XREF: sub_13D95-2j
		xor	dx, dx
		mov	ax, 31250
		div	cx
		neg	al
		or	ah, ah
		jnz	short loc_13D8D
		mov	ah, [_byte_24618]
		mov	[_byte_24619], ah
		retn
endp		sub_13D95

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13CF6

_settimer:				; CODE XREF: sub_13CF6+21j
		xor	ax, ax
		cmp	cx, 45
		jbe	short _set_timer
		mov	dx, 2Dh	; '-'
		mov	ax, 8426h
		div	cx
		jmp	short $+2
; END OF FUNCTION CHUNK	FOR sub_13CF6

; =============== S U B	R O U T	I N E =======================================


proc		_set_timer near		; CODE XREF: _configure_timer+Fp
					; _memfill8080+4p ...
		mov	[cs:_timer_word_14F6E], ax
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
endp		_set_timer


; =============== S U B	R O U T	I N E =======================================


proc		_clean_timer near	; CODE XREF: _clean_int8_mem_timr+Fp
					; _midi_sndoff+Fp
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
endp		_clean_timer


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13DE5 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	sub_14087
		or	ax, ax
		jnz	loc_1388B
		retn
endp		_eff_13DE5


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13DEF near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	sub_14087
		or	ax, ax
		jnz	loc_138A9
		retn
endp		_eff_13DEF

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13DF9:				; CODE XREF: sub_13623+15Ej
					; sub_13623+164j
		mov	ax, [bx]
		cmp	ax, [_word_245DC]
		jnz	short loc_13E03
		xor	ax, ax

loc_13E03:				; CODE XREF: sub_13623+7DCj
		mov	[bx+10h], ax
		mov	ax, [_word_245DC]
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


proc		_eff_13E1E near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13E2A
		xor	ah, ah
		shl	ax, 2
		mov	[bx+12h], ax

loc_13E2A:				; CODE XREF: _eff_13E1E+2j _eff_13E7F+3j
		jmp	loc_138DE
endp		_eff_13E1E


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13E2D near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	cl, 5
		jmp	loc_13931
endp		_eff_13E2D


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13E32 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13E39
		mov	[bx+34h], al

loc_13E39:				; CODE XREF: _eff_13E32+2j
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
		cmp	[_byte_24668], 0
		jz	loc_13AEF
		retn
; ---------------------------------------------------------------------------

loc_13E5E:				; CODE XREF: _eff_13E32+1Aj
		cmp	ch, 0Fh
		jz	short loc_13E6F
		mov	dl, [bx+8]
		test	al, 0Fh
		jnz	loc_13ADE
		jmp	loc_13AEF
; ---------------------------------------------------------------------------

loc_13E6F:				; CODE XREF: _eff_13E32+2Fj
		or	cl, cl
		jz	loc_13AEF
		cmp	[_byte_24668], 0
		jz	loc_13ADE
		retn
endp		_eff_13E32


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13E7F near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	_eff_13E32
		jmp	short loc_13E2A
endp		_eff_13E7F


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13E84 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	_eff_13E32
		mov	cl, 5
		jmp	loc_13950
endp		_eff_13E84


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13E8C near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	sub_13E9B
		mov	[_byte_24667], ah
		mov	[_byte_24668], 0
		jmp	sub_13CF6
endp		_eff_13E8C


; =============== S U B	R O U T	I N E =======================================


proc		sub_13E9B near		; CODE XREF: __2stm_module+2Ep
					; _eff_13E8Cp
		movzx	di, al
		mov	dx, di
		and	dl, 0Fh
		shr	di, 4
		mov	ax, dx
		mul	[cs:_table_13EC3+di]
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
endp		sub_13E9B

; ---------------------------------------------------------------------------
_table_13EC3	db 140,50,25,15,10,7,6,4,3,3,2,2,2,2,1,1 ; DATA	XREF: sub_13E9B+Dr
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13ED3:				; CODE XREF: sub_13623+16Aj
		mov	cl, [bx+0Bh]
		and	cx, 0FFh
		jz	loc_13791
		mov	ax, [bx]
		sub	ax, [_word_245DC]
		jns	short loc_13EE8
		neg	ax

loc_13EE8:				; CODE XREF: sub_13623+8C1j
		xor	dx, dx
		div	cx
		mov	[bx+12h], ax
		mov	[byte ptr bx+0Bh], 0
		or	[byte ptr bx+17h], 10h
		mov	ax, [bx]
		mov	[bx+10h], ax
		mov	ax, [_word_245DC]
		mov	[bx], ax
		jmp	sub_137D5
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


proc		_nullsub_2 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		retn
endp		_nullsub_2


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13F05 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13F0C
		mov	[bx+34h], al

loc_13F0C:				; CODE XREF: _eff_13F05+2j
		mov	al, [bx+34h]
		mov	dl, al
		shr	dl, 4
		and	al, 0Fh
		mov	dh, al
		and	ax, 0Fh
		add	al, dl
		jz	locret_13CF4
		mov	cl, al
		movzx	ax, [_byte_24668]
		div	cl
		cmp	ah, dl
		jb	short loc_13F34
		xor	al, al
		jmp	[off_245CC]
; ---------------------------------------------------------------------------

loc_13F34:				; CODE XREF: _eff_13F05+27j
		mov	al, [bx+8]
		jmp	[off_245CC]
endp		_eff_13F05


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13F3B near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13F42
		mov	[bx+34h], al

loc_13F42:				; CODE XREF: _eff_13F3B+2j
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
		mov	[byte ptr bx+8], 0
		jmp	short loc_13FB7
; ---------------------------------------------------------------------------

loc_13F6D:				; CODE XREF: _eff_13F3B+19j
		movzx	ax, [byte ptr bx+8]
		shl	ax, 1
		mov	dl, 3
		div	dl
		mov	[bx+8],	al
		jmp	short loc_13FB7
; ---------------------------------------------------------------------------

loc_13F7C:				; CODE XREF: _eff_13F3B+1Dj
		shr	[byte ptr bx+8], 1
		jmp	short loc_13FB7
; ---------------------------------------------------------------------------

loc_13F81:				; CODE XREF: _eff_13F3B+5Fj
		movzx	ax, [byte ptr bx+8]
		mov	dx, ax
		add	ax, dx
		add	ax, dx
		shr	ax, 1
		jmp	short loc_13FAB
; ---------------------------------------------------------------------------

loc_13F8F:				; CODE XREF: _eff_13F3B+63j
		mov	al, [bx+8]
		add	al, al
		jmp	short loc_13FAB
; ---------------------------------------------------------------------------

loc_13F96:				; CODE XREF: _eff_13F3B+15j
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

loc_13FAB:				; CODE XREF: _eff_13F3B+52j
					; _eff_13F3B+59j
		cmp	al, [_byte_2467D]
		jbe	short loc_13FB4
		mov	al, [_byte_2467D]

loc_13FB4:				; CODE XREF: _eff_13F3B+74j
		mov	[bx+8],	al

loc_13FB7:				; CODE XREF: _eff_13F3B+11j
					; _eff_13F3B+2Aj ...
		mov	al, ch
		and	al, 0Fh
		jmp	_eff_13C64
endp		_eff_13F3B


; =============== S U B	R O U T	I N E =======================================


proc		_eff_13FBE near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jnz	short loc_13FCE
		mov	al, [bx+34h]
		or	al, al
		jz	locret_13CF4
		mov	[bx+0Bh], al

loc_13FCE:				; CODE XREF: _eff_13FBE+2j
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
		movzx	ax, [_byte_24668]
		mov	dh, 3
		div	dh
		or	ah, ah
		jz	short loc_1401A
		mov	dh, [bx+0Bh]
		cmp	ah, 2
		jz	short loc_14000
		shr	dh, 4

loc_14000:				; CODE XREF: _eff_13FBE+3Dj
		and	dh, 0Fh
		add	dl, dh
		movzx	ax, dl
		mov	dh, 0Ch
		div	dh
		inc	ah
		shl	al, 4
		or	al, ah
		call	sub_13826
		jmp	[off_245CA]
; ---------------------------------------------------------------------------

loc_1401A:				; CODE XREF: _eff_13FBE+35j
		mov	ax, [bx]
		jmp	[off_245CA]
endp		_eff_13FBE


; =============== S U B	R O U T	I N E =======================================


proc		_eff_14020 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		shl	ax, 2
		push	bx
		push	si
		push	es
		push	cs
		call	near ptr _change_amplif
		pop	es
		pop	si
		pop	bx
		retn
endp		_eff_14020


; =============== S U B	R O U T	I N E =======================================


proc		_eff_14030 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	ax, 0Fh
		mov	di, ax
		mov	al, [cs:_table_14057+di]
		mov	[_byte_2467B], al

loc_1403D:				; CODE XREF: _eff_14067+Ej
					; _eff_14067+17j ...
		call	_calc_14043
		jmp	sub_13CF6
endp		_eff_14030


; =============== S U B	R O U T	I N E =======================================


proc		_calc_14043 near		; CODE XREF: _far_module+34p
					; _eff_14030:loc_1403Dp
		mov	al, [_byte_2467B]
		add	al, [_byte_2467C]
		and	eax, 0FFh
		lea	ax, [eax+eax*4]
		shr	ax, 1
		retn
endp		_calc_14043

; ---------------------------------------------------------------------------
_table_14057	db 0FFh,80h,40h,2Ah,20h,19h,15h,12h,10h,0Eh,0Ch,0Bh,0Ah
					; DATA XREF: _far_module+27r
					; _eff_14030+5r
		db 9,9,8

; =============== S U B	R O U T	I N E =======================================


proc		_eff_14067 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_14080
		test	al, 0Fh
		jz	short loc_14077
		and	al, 0Fh
		sub	[_byte_2467C], al
		jmp	short loc_1403D
; ---------------------------------------------------------------------------

loc_14077:				; CODE XREF: _eff_14067+6j
		shr	al, 4
		add	[_byte_2467C], al
		jmp	short loc_1403D
; ---------------------------------------------------------------------------

loc_14080:				; CODE XREF: _eff_14067+2j
		mov	[_byte_2467C], 0
		jmp	short loc_1403D
endp		_eff_14067


; =============== S U B	R O U T	I N E =======================================


proc		sub_14087 near		; CODE XREF: _eff_13DE5p _eff_13DEFp
		xor	ah, ah
		or	al, al
		jz	short loc_14090
		mov	[bx+34h], al

loc_14090:				; CODE XREF: sub_14087+4j
		mov	al, [bx+34h]
		cmp	[_byte_24668], 0
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
endp		sub_14087


; =============== S U B	R O U T	I N E =======================================


proc		sub_140B6 near		; CODE XREF: _gravis_set+1Ep
					; _gravis_int+91p ...
		cmp	[_byte_24671], 1
		jz	short locret_140E5
		cmp	[_play_state], 1
		jz	short locret_140E5
		inc	[_byte_24668]
		mov	al, [_byte_24668]
		cmp	al, [_byte_24667]
		jnb	short loc_140E6
		mov	bx, offset _volume_25908
		mov	cx, [_word_245D4]

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
		mov	[_byte_24668], 0
		cmp	[_byte_2466D], 0
		jnz	short loc_140F7
		call	sub_135CA
		jmp	short loc_14111
; ---------------------------------------------------------------------------

loc_140F7:				; CODE XREF: sub_140B6+3Aj
		mov	bx, offset _volume_25908
		mov	cx, [_word_245D4]

loc_140FE:				; CODE XREF: sub_140B6+53j
		push	bx
		push	cx
		call	sub_13813
		pop	cx
		pop	bx
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_140FE
		mov	si, [word ptr _pointer_245B4]
		jmp	short $+2

loc_14111:				; CODE XREF: sub_140B6+3Fj
					; _midi_int8p+43p
		cmp	[_byte_2466B], 1
		jz	loc_141BA
		cmp	[_byte_2466A], 1
		jz	short loc_14153
		cmp	[_byte_2466C], 0
		jz	short loc_14131
		xor	al, al
		xchg	al, [_byte_2466C]
		mov	[_byte_2466D], al

loc_14131:				; CODE XREF: sub_140B6+70j
		cmp	[_byte_2466D], 0
		jz	short loc_1413E
		dec	[_byte_2466D]
		jnz	short loc_14142

loc_1413E:				; CODE XREF: sub_140B6+80j
		inc	[_word_245F6]

loc_14142:				; CODE XREF: sub_140B6+86j
		mov	bx, [_word_245F0]
		movzx	ax, [_byte_281E8+bx]
		cmp	[_word_245F6], ax
		jbe	loc_141DA

loc_14153:				; CODE XREF: sub_140B6+69j
		cmp	[_play_state], 2
		jz	short loc_14184
		inc	[_word_245F0]
endp		sub_140B6 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1415E near		; CODE XREF: sub_12F56+11p
		mov	ax, [_word_245FA]
		cmp	[_word_245F0], ax
		jb	short loc_14184
		test	[_flag_playsetttings], 4
		jz	short _vlm_141DF
		mov	ax, [_word_245F8]
		mov	[_word_245F0], ax
		or	ax, ax
		jnz	short loc_14184
		mov	al, [_byte_2467A]
		call	sub_13CF6
		mov	al, [_byte_24679]
		call	_eff_13CE8

loc_14184:				; CODE XREF: sub_140B6+A2j
					; sub_1415E+7j	...
		mov	bx, [_word_245F0]
		mov	al, [_byte_280E8+bx]
		or	al, al
		jz	short loc_141A2
		push	bx
		cmp	al, 0FFh
		jnz	short loc_1419E
		mov	al, [_byte_2467A]
		call	sub_13CF6
		mov	al, [_byte_24679]

loc_1419E:				; CODE XREF: sub_1415E+35j
		call	_eff_13CE8
		pop	bx

loc_141A2:				; CODE XREF: sub_1415E+30j
		bts	[word ptr _byte_282E8], bx
		movzx	bx, [_byte_27FE8+bx]
		mov	[_my_seg_index],	bx
		shl	bx, 1
		mov	es, [_segs_table+bx]
		mov	[word ptr _pointer_245B4+2], es

loc_141BA:				; CODE XREF: sub_140B6+60j
		xor	ax, ax
		xchg	al, [_byte_24669]
		mov	[_word_245F6], ax
		call	sub_11C0C
		mov	[_byte_2466A], 0
		mov	[_byte_2466B], 0
		mov	[_byte_2466C], 0
		mov	[_byte_2466D], 0

loc_141DA:				; CODE XREF: sub_140B6+99j
		mov	[word ptr _pointer_245B4], si
		retn
endp		sub_1415E


; =============== S U B	R O U T	I N E =======================================


proc		_vlm_141DF near		; CODE XREF: _eff_13B06+31p
					; sub_1415E+Ej
		push	cs
		call	near ptr _volume_12A66
		mov	[_byte_24671], 1
		mov	dl, 1
		mov	bx, 5344h	; DS
		mov	cx, 4D50h	; MP
		mov	ax, 60FFh
		int	2Fh		; IPLAY: get data seg
		retn
endp		_vlm_141DF


; =============== S U B	R O U T	I N E =======================================


proc		_snd_initialze near	; CODE XREF: sub_12DA8+78p

; FUNCTION CHUNK AT 526B SIZE 000000DB BYTES

		cmp	[_snd_init], 1
		jz	short loc_1420D
		mov	[_snd_init], 1
		movzx	bx, [_sndcard_type]
		shl	bx, 1
		jmp     _covox_init
; ---------------------------------------------------------------------------

loc_1420D:				; CODE XREF: _snd_initialze+5j
					; _snd_on+5j ...
		stc
		retn
endp		_snd_initialze ;	sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_snd_on near		; CODE XREF: sub_12EBA+87p
		cmp	[_snd_init], 1
		jnz	short loc_1420D
		cmp	[_snd_set_flag],	1
		jz	short loc_1420D
		mov	[_snd_set_flag],	1
		movzx	bx, [_sndcard_type]
		shl	bx, 1
		jmp     _covox_on
endp		_snd_on


; =============== S U B	R O U T	I N E =======================================


proc		_snd_off	near		; CODE XREF: _snd_offx+8p _snd_deinit+Cp

; FUNCTION CHUNK AT 0B5A SIZE 000001CC BYTES

		cmp	[_snd_init], 1
		jnz	short loc_1420D
		cmp	[_snd_set_flag],	0
		jz	short loc_1420D
		mov	[_snd_set_flag],	0
		push	cs
		call	near ptr _volume_12A66
		movzx	bx, [_sndcard_type]
		shl	bx, 1
		jmp     _covox_off
endp		_snd_off	; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_snd_deinit near		; CODE XREF: _deinit_125B9+18p
		cmp	[_snd_init], 1
		jnz	short loc_1420D
		mov	[_snd_init], 0
		call	_snd_off
		movzx	bx, [_sndcard_type]
		shl	bx, 1
		jmp     _covox_deinit
endp		_snd_deinit


; =============== S U B	R O U T	I N E =======================================


 ; sp-analysis failed

; START	OF FUNCTION CHUNK FOR _wss_test

loc_14332:				; CODE XREF: _proaud_init+22j
					; _proaud_init+E2j ...
		stc
		retn
; END OF FUNCTION CHUNK	FOR _wss_test

; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
		db 87h,	0DBh

; =============== S U B	R O U T	I N E =======================================


; void __cdecl _gravis_int()



; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================


; void __cdecl _proaud_14700()



; =============== S U B	R O U T	I N E =======================================


 ;	sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


 ;	sp-analysis failed


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
_wss_freq_table	dw 5513			; DATA XREF: _wss_test+3Er
					; _wss_test:loc_149DFr
_wss_freq_table2	dw  1,19D7h,0Fh,1F40h, 0,2580h,0Eh,2B11h, 3,3E80h, 2,49D4h
					; DATA XREF: _wss_test+51r
		dw  5,5622h, 7,6B25h, 4,7D00h, 6,8133h,0Dh,93A8h, 9,0AC44h
		dw 0Bh,0BB80h,0Ch

; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------

_wss_int:				; DATA XREF: _wss_set+18o
		push	ax
		push	dx
; ---------------------------------------------------------------------------
		db 0BAh	; ∫
_word_14913	dw 536h			; DATA XREF: _wss_set+14w
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


proc		_sb16_init near		; DATA XREF: seg003:0D08o
		mov	[_sndflags_24622], 9
		mov	[_byte_24623], 1
		mov	[_bit_mode], 16
		call	_sb16_detect_port
		mov	dx, offset _aErrorSoundcardN ; "Error: Soundcard	not found!\r\n"
		jb	loc_14332
		mov	al, [_irq_number]
		mov	[_sb_irq_number], al
		cmp	al, 0FFh
		jnz	short loc_14ABB
		mov	ah, 80h	; 'Ä'
		call	_ReadMixerSB
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

loc_14AB3:				; CODE XREF: _sb16_init+30j
					; _sb16_init+36j ...
		mov	[_sb_irq_number], ah
		mov	[_irq_number], ah

loc_14ABB:				; CODE XREF: _sb16_init+21j
					; _sb16_init+2Aj
		mov	al, [_dma_channel]
		mov	[_dma_chn_mask],	al
		cmp	al, 0FFh
		jnz	short loc_14AFD
		mov	ah, 81h	; 'Å'
		call	_ReadMixerSB
		cmp	al, 0FFh
		jz	short loc_14AFD
		cmp	[_bit_mode], 8
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

loc_14AE7:				; CODE XREF: _sb16_init+60j
		mov	ah, 3
		test	al, 4
		jnz	short loc_14AF5
		mov	ah, 1
		test	al, 2
		jnz	short loc_14AF5
		mov	ah, 0

loc_14AF5:				; CODE XREF: _sb16_init+66j
					; _sb16_init+6Cj ...
		mov	[_dma_chn_mask],	ah
		mov	[_dma_channel], ah

loc_14AFD:				; CODE XREF: _sb16_init+50j
					; _sb16_init+59j
		call	_sb16_sound_on
		mov	eax, 1000h
		mov	cl, [_dma_chn_mask]
		call	_alloc_dma_buf
		mov	[word ptr _dma_buf_pointer], 0
		mov	[word ptr _dma_buf_pointer+2], ax
		clc
		retn
endp		_sb16_init


; =============== S U B	R O U T	I N E =======================================


proc		_sb16_on	near		; DATA XREF: seg003:0D1Eo
		call	sub_13017
		mov	[_dma_mode], 58h	; 'X'
		mov	[_word_2460E], 1000h
		mov	si, offset _sb_callback ; myfunc
		mov	al, [_sb_irq_number]
		call	_setsnd_handler
		mov	dx, [_sb_base_port]
		add	dl, 0Ch

loc_14B36:				; CODE XREF: _sb16_on+21j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B36
		mov	al, 41h	; 'A'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B3E:				; CODE XREF: _sb16_on+29j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B3E
		mov	al, [byte ptr _freq1+1]
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B47:				; CODE XREF: _sb16_on+32j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B47
		mov	al, [byte ptr _freq1]
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B50:				; CODE XREF: _sb16_on+3Bj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B50
		cmp	[_bit_mode], 16
		jz	short loc_14B6A
		mov	ax, [_sb_base_port]
		add	al, 0Eh
		mov	[cs:_word_14BBB], ax
		mov	ax, 0C6h ; '∆'
		jmp	short loc_14B76
; ---------------------------------------------------------------------------

loc_14B6A:				; CODE XREF: _sb16_on+42j
		mov	ax, [_sb_base_port]
		add	al, 0Fh
		mov	[cs:_word_14BBB], ax
		mov	ax, 10B6h

loc_14B76:				; CODE XREF: _sb16_on+50j
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B77:				; CODE XREF: _sb16_on+62j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B77
		mov	al, [_byte_24623]
		and	al, 1
		shl	al, 5
		or	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B87:				; CODE XREF: _sb16_on+72j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B87
		mov	ax, [_word_2460E]
		shr	ax, 2
		mov	cl, [_bit_mode]
		shr	cl, 4
		and	cl, 1
		shr	ax, cl
		dec	ax
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14BA0:				; CODE XREF: _sb16_on+8Bj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14BA0
		mov	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	cl, [_dma_chn_mask]
		call	_dma_186E3
		mov	[_byte_2466E], 1
		retn
endp		_sb16_on

; ---------------------------------------------------------------------------

; void __cdecl _sb_callback()
_sb_callback:				; DATA XREF: _sb16_on+Eo
		push	ax
		push	dx
; ---------------------------------------------------------------------------
		db 0BAh	; ∫
_word_14BBB	dw 22Fh			; DATA XREF: _sb16_on+49w _sb16_on+57w
; ---------------------------------------------------------------------------
		in	al, dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
		jmp	loc_14E10

; =============== S U B	R O U T	I N E =======================================


proc		_sb16_off near		; DATA XREF: seg003:0D34o
		pushf
		cli
		cmp	[_byte_2466E], 1
		jnz	short loc_14BFD
		cli
		mov	dx, [_sb_base_port]
		add	dl, 0Ch

loc_14BD8:				; CODE XREF: _sb16_off+14j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14BD8
		mov	al, 0DAh ; '⁄'
		cmp	[_bit_mode], 8
		jz	short loc_14BE8
		mov	al, 0D9h ; 'Ÿ'

loc_14BE8:				; CODE XREF: _sb16_off+1Dj
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14BE9:				; CODE XREF: _sb16_off+25j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14BE9
		call	_restore_intvector
		mov	cl, [_dma_chn_mask]
		call	_set_dmachn_mask
		mov	[_byte_2466E], 0

loc_14BFD:				; CODE XREF: _sb16_off+7j
		popf
		retn
endp		_sb16_off


; =============== S U B	R O U T	I N E =======================================


proc		_sb16_deinit near	; DATA XREF: seg003:0D4Ao
		call	_memfree_18A28
		call	_sb16_sound_off
		retn
endp		_sb16_deinit


; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR _sb_set

_sbpro_set:				; CODE XREF: _sb_set+6j
					; DATA XREF: seg003:0D20o
		call	sub_13017
		mov	[_dma_mode], 58h	; 'X'
		mov	[_word_2460E], 1000h
		mov	ax, [_sb_base_port]
		add	al, 0Eh
		mov	[cs:_word_14CEB], ax
		mov	ah, 0Eh
		call	_ReadMixerSB
		mov	[_byte_24664], al
		and	al, 0FDh
		cmp	[_byte_24623], 0
		jz	short loc_14C89
		call	_WriteMixerSB
		or	al, 22h

loc_14C89:				; CODE XREF: _sb_set-F5j
		call	_WriteMixerSB
		pushf
		cli
		mov	dx, [_sb_base_port]
		add	dl, 0Eh
		in	al, dx		; DMA controller, 8237A-5.
					; Clear	mask registers.
					; Any OUT enables all 4	channels.
		sub	dl, 2

loc_14C99:				; CODE XREF: _sb_set-DBj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14C99
		mov	al, 40h	; '@'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CA1:				; CODE XREF: _sb_set-D3j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CA1
		mov	al, [_sb_timeconst]
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CAA:				; CODE XREF: _sb_set-CAj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CAA
		mov	al, 48h	; 'H'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CB2:				; CODE XREF: _sb_set-C2j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CB2
		mov	ax, [_word_2460E]
		shr	ax, 2
		dec	ax
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CBF:				; CODE XREF: _sb_set-B5j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CBF
		mov	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CC7:				; CODE XREF: _sb_set-ADj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CC7
		mov	al, 90h	; 'ê'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	[_byte_2466E], 1
		mov	si, offset loc_14CE8 ; myfunc
		mov	al, [_sb_irq_number]
		call	_setsnd_handler
		mov	cl, [_dma_chn_mask]
		call	_dma_186E3
		popf
		retn
; END OF FUNCTION CHUNK	FOR _sb_set
; ---------------------------------------------------------------------------

loc_14CE8:				; DATA XREF: _sb_set-A3o
		push	ax
		push	dx
; ---------------------------------------------------------------------------
		db 0BAh	; ∫
_word_14CEB	dw 22Eh			; DATA XREF: _sb_set-108w
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

; START	OF FUNCTION CHUNK FOR _proaud_14700

loc_14E10:				; CODE XREF: _proaud_14700+15j
					; seg000:491Ej	...
		add	[_word_24602], 400h
		and	[_word_24602], 0FFFh
		inc	[_byte_24620]
		cmp	[_byte_24620], 2
		ja	_lc_disable_interpol

loc_14E29:				; CODE XREF: _proaud_14700+7BCj
		pushad
		push	es
		push	fs
		push	gs
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		test	[byte ptr _config_word+1], 10h
		jz	short loc_14E4D
		inc	[_byte_24621]
		and	[_byte_24621], 3
		jnz	short loc_14E4D
		mov	cl, [_dma_channel]
		call	_dma_186E3

loc_14E4D:				; CODE XREF: _proaud_14700+739j
					; _proaud_14700+744j
		mov	bx, 1
		mov	cl, [_irq_number]
		shl	bx, cl
		mov	dx, 21h	; '!'
		or	bh, bh
		jz	short loc_14E66
		mov	dx, 0A1h ; '°'
		mov	al, 20h	; ' '
		out	0A0h, al	; PIC 2	 same as 0020 for PIC 1
		mov	bl, bh

loc_14E66:				; CODE XREF: _proaud_14700+75Bj
		in	al, dx		; Interrupt Controller #2, 8259A
		or	al, bl
		out	dx, al		; Interrupt Controller #2, 8259A
		sti
		mov	ax, [_word_24602]

loc_14E6E:				; CODE XREF: _proaud_14700+78Aj
		mov	dx, ax
		cmp	ax, [_word_24600]
		ja	short loc_14E79
		add	ax, 1000h

loc_14E79:				; CODE XREF: _proaud_14700+774j
		sub	ax, [_word_24600]
		cmp	ax, 800h
		jb	short loc_14E8C
		push	dx
		call	sub_16C69
		pop	ax
		add	ax, 10h
		jmp	short loc_14E6E
; ---------------------------------------------------------------------------

loc_14E8C:				; CODE XREF: _proaud_14700+780j
		mov	bx, 1
		mov	cl, [_irq_number]
		shl	bx, cl
		mov	dx, 21h	; '!'
		or	bh, bh
		jz	short loc_14EA1
		mov	dx, 0A1h ; '°'
		mov	bl, bh

loc_14EA1:				; CODE XREF: _proaud_14700+79Aj
		not	bl
		in	al, dx		; Interrupt Controller #2, 8259A
		and	al, bl
		out	dx, al		; Interrupt Controller #2, 8259A
		pop	gs
		pop	fs
		pop	es
		popad
		dec	[_byte_24620]
		pop	ds
		pop	dx
		pop	ax
		iret
; ---------------------------------------------------------------------------

_lc_disable_interpol:			; CODE XREF: _proaud_14700+725j
		and	[_flag_playsetttings], 0EFh
		jmp	loc_14E29
; END OF FUNCTION CHUNK	FOR _proaud_14700
; ---------------------------------------------------------------------------
		mov	al, 20h	; ' '
		cmp	[_irq_number], 7
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


proc		_timer_int_end far	; CODE XREF: _covox_timer_int+22j
					; _covox_timer_int+33j ...
		cmp	[cs:_byte_14F70], 0
		jz	short loc_14F3C
		pushad
		push	ds
		push	es
		push	fs
		push	gs
		mov	ax, seg003
		mov	ds, ax
		mov	ax, [_word_245E4]
		mov	[cs:_word_14F6C], ax
		sti
		call	sub_16C69
		pop	gs
		pop	fs
		pop	es
		pop	ds
		popad
		iret
; ---------------------------------------------------------------------------

loc_14F3C:				; CODE XREF: _timer_int_end+6j
		mov	[cs:_word_14F6C], 1
		jmp	[cs:_int8addr]
endp		_timer_int_end

; ---------------------------------------------------------------------------
		dec	[cs:_byte_14F73]
		jz	short loc_14F50
		iret
; ---------------------------------------------------------------------------

loc_14F50:				; CODE XREF: seg000:4F4Dj
		push	ax
		mov	al, [cs:_byte_14F72]
		mov	[cs:_byte_14F73], al
		mov	ax, [cs:_timer_word_14F6E]
		call	_set_timer
		pop	ax
		jmp	[cs:_int8addr]
; ---------------------------------------------------------------------------
; ---------------------------------------------------------------------------
_int8addr	dd 0			; DATA XREF: sub_12DA8+6Aw
					; _clean_int8_mem_timr+5r ...
_word_14F6C	dw 0			; DATA XREF: _configure_timer+1Bw
					; _memfill8080+Dw ...
_timer_word_14F6E dw 0			; DATA XREF: _set_timerw seg000:4F59r
_byte_14F70	db 0			; DATA XREF: _configure_timer+12w
					; _memfill8080+7w ...
_byte_14F71	db 0			; DATA XREF: sub_12D35:loc_12D41w
					; sub_12D35:loc_12D4Ew
_byte_14F72	db 0			; DATA XREF: sub_13CF6+Dw seg000:4F51r
_byte_14F73	db 0			; DATA XREF: sub_13CF6+11w
					; seg000:4F48w	...

; =============== S U B	R O U T	I N E =======================================


proc		_covox_init near		; DATA XREF: seg003:0D0Eo
		mov	[_sndflags_24622], 3
		mov	[_byte_24623], 0
		mov	[_bit_mode], 8
		cmp	[_snd_base_port], 0FFFFh
		jnz	short loc_14F95
		xor	ax, ax
		mov	es, ax
		assume es:nothing
		mov	ax, [es:408h]
		mov	[_snd_base_port], ax

loc_14F95:				; CODE XREF: _covox_init+14j
		mov	ax, [_snd_base_port]
		mov	[cs:_word_14FC8], ax
		pushf
		cli
		mov	dx, offset _covox_timer_int
		call	_set_timer_int
		sub	ax, 0F00h
		mov	[cs:_word_14FC0], ax
		mov	[cs:_word_14FC5], 0F000h
		popf
		clc
		retn
endp		_covox_init


; =============== S U B	R O U T	I N E =======================================


proc		_covox_on near		; DATA XREF: seg003:0D24o
		call	_configure_timer
		retn
endp		_covox_on

; ---------------------------------------------------------------------------

; =============== S U B	R O U T	I N E =======================================


proc		_covox_timer_int	far	; DATA XREF: _covox_init+2Ao
		push	ax
		push	dx
		push	ds
; ---------------------------------------------------------------------------
		db 0BAh	; ∫		; self moifying
_word_14FC0	dw 1000h		; DATA XREF: _covox_init+33w
; ---------------------------------------------------------------------------
		mov	ds, dx
; ---------------------------------------------------------------------------
		assume ds:nothing
		db 0A0h	; †
_word_14FC5	dw 1234h		; DATA XREF: _covox_init+37w
					; _covox_timer_int+16w ...
		db 0BAh	; ∫
_word_14FC8	dw 378h			; DATA XREF: _covox_init+24w
; ---------------------------------------------------------------------------
		out	dx, al		; Printer Data Latch:
					; send byte to printer
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		assume ds:seg003
		pop	dx
		pop	ax
		inc	[cs:_word_14FC5]
		jz	short loc_14FE3
		dec	[cs:_word_14F6C]
		jz	near ptr _timer_int_end
		iret
; ---------------------------------------------------------------------------

loc_14FE3:				; CODE XREF: _covox_timer_int+1Bj
		mov	[cs:_word_14FC5], 0F000h
		dec	[cs:_word_14F6C]
		jz	near ptr _timer_int_end
		iret
endp		_covox_timer_int	; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_covox_off near	; DATA XREF: seg003:0D3Ao
		call	_memfill8080
		retn
endp		_covox_off


; =============== S U B	R O U T	I N E =======================================


proc		_covox_deinit near	; DATA XREF: seg003:0D50o
		call	_clean_int8_mem_timr
		retn
endp		_covox_deinit


; =============== S U B	R O U T	I N E =======================================


proc		_stereo_init near	; DATA XREF: seg003:0D10o
		mov	[_sndflags_24622], 3
		mov	[_byte_24623], 1
		mov	[_bit_mode], 8
		cmp	[_snd_base_port], -1
		jnz	short loc_1501D
		xor	ax, ax
		mov	es, ax
		mov	ax, [es:408h]
		mov	[_snd_base_port], ax

loc_1501D:				; CODE XREF: _stereo_init+14j
		mov	ax, [_snd_base_port]
		add	ax, 2
		mov	[cs:_word_1504D], ax
		pushf
		cli
		mov	dx, offset _stereo_timer_int
		call	_set_timer_int
		sub	ax, 0F00h
		mov	[word ptr cs:loc_15047+1], ax
		mov	[cs:_word_15056], 0F000h
		popf
		clc
		retn
endp		_stereo_init


; =============== S U B	R O U T	I N E =======================================


proc		_stereo_set near		; DATA XREF: seg003:0D26o
		call	_configure_timer
		retn
endp		_stereo_set


; =============== S U B	R O U T	I N E =======================================


proc		_stereo_timer_int far	; DATA XREF: _stereo_init+2Do
		push	ax
		push	dx
		push	ds

loc_15047:				; DATA XREF: _stereo_init+36w
		mov	dx, seg000
		mov	ds, dx
; ---------------------------------------------------------------------------
		assume ds:seg000
		db 0BAh
_word_1504D	dw 37Ah			; DATA XREF: _stereo_init+27w
; ---------------------------------------------------------------------------
		mov	al, 2
		out	dx, al
		sub	dl, 2
; ---------------------------------------------------------------------------
		db 0A1h
_word_15056	dw 1234h		; DATA XREF: _stereo_init+3Aw
					; _stereo_timer_int+28w	...
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
		assume ds:seg003
		pop	dx
		pop	ax
		add	[cs:_word_15056], 2
		jb	short loc_1507E
		dec	[cs:_word_14F6C]
		jz	near ptr _timer_int_end
		iret
; ---------------------------------------------------------------------------

loc_1507E:				; CODE XREF: _stereo_timer_int+2Ej
		mov	[cs:_word_15056], 0F000h
		dec	[cs:_word_14F6C]
		jz	near ptr _timer_int_end
		iret
endp		_stereo_timer_int ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_stereo_sndoff near	; DATA XREF: seg003:0D3Co
		call	_memfill8080
		retn
endp		_stereo_sndoff


; =============== S U B	R O U T	I N E =======================================


proc		_stereo_clean near	; DATA XREF: seg003:0D52o
		call	_clean_int8_mem_timr
		retn
endp		_stereo_clean


; =============== S U B	R O U T	I N E =======================================


proc		_adlib_init near		; DATA XREF: seg003:0D12o
		mov	[_sndflags_24622], 0Bh
		mov	[_byte_24623], 0
		mov	[_bit_mode], 8
		call	_adlib_18389
		mov	ax, 2120h
		call	_adlib_18395
		mov	ax, 0F060h
		call	_adlib_18395
		mov	ax, 0F080h
		call	_adlib_18395
		mov	ax, 1C0h
		call	_adlib_18395
		mov	ax, 0E0h ; '‡'
		call	_adlib_18395
		mov	ax, 3F43h
		call	_adlib_18395
		mov	ax, 0B0h ; '∞'
		call	_adlib_18395
		mov	ax, 0A0h ; '†'
		call	_adlib_18395
		mov	ax, 8FA0h
		call	_adlib_18395
		mov	ax, 2EB0h
		call	_adlib_18395
		mov	cx, 4000h

loc_150E8:				; CODE XREF: _adlib_init+52j
		dec	cx
		jnz	short loc_150E8
		mov	ax, 20B0h
		call	_adlib_18395
		mov	ax, 0A0h ; '†'
		call	_adlib_18395
		mov	ax, 40h	; '@'
		call	_adlib_18395
		pushf
		cli
		mov	dx, offset _adlib_timer_int
		call	_set_timer_int
		sub	ax, 0F00h
		mov	[word ptr cs:loc_15120+1], ax
		mov	[cs:_word_15126], 0F000h
		popf
		clc
		retn
endp		_adlib_init


; =============== S U B	R O U T	I N E =======================================


proc		_adlib_set near		; DATA XREF: seg003:0D28o
		call	_configure_timer
		retn
endp		_adlib_set

; ---------------------------------------------------------------------------

_adlib_timer_int:			; DATA XREF: _adlib_init+68o
		push	ax
		push	bx
		push	dx
		push	ds

loc_15120:				; DATA XREF: _adlib_init+71w
		mov	ax, 1234h	; self modifying
		mov	ds, ax
; ---------------------------------------------------------------------------
		assume ds:nothing
		db 0A0h	; †		; self modifying
_word_15126	dw 1234h		; DATA XREF: _adlib_init+75w
					; seg000:5135w	...
; ---------------------------------------------------------------------------
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		mov	bx, offset _table_24898
		xlat
		mov	dx, 389h
		out	dx, al
		inc	[cs:_word_15126]
		jz	short loc_1514E

loc_1513C:				; CODE XREF: seg000:5155j
		pop	ds
		pop	dx
		pop	bx
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ax
		dec	[cs:_word_14F6C]
		jz	near ptr _timer_int_end
		iret
; ---------------------------------------------------------------------------

loc_1514E:				; CODE XREF: seg000:513Aj
		mov	[cs:_word_15126], 0F000h
		jmp	short loc_1513C

; =============== S U B	R O U T	I N E =======================================


proc		_adlib_sndoff near	; DATA XREF: seg003:0D3Eo
		call	_memfill8080
		retn
endp		_adlib_sndoff


; =============== S U B	R O U T	I N E =======================================


proc		_adlib_clean near	; DATA XREF: seg003:0D54o
		call	_clean_int8_mem_timr
		call	_adlib_18389
		retn
endp		_adlib_clean


; =============== S U B	R O U T	I N E =======================================


proc		_pcspeaker_init near	; DATA XREF: seg003:0D14o
		mov	[_sndflags_24622], 3
		mov	[_byte_24623], 0
		mov	[_bit_mode], 8
		pushf
		cli
		mov	al, 90h	; 'ê'
		out	43h, al		; Timer	8253-5 (AT: 8254.2).
		mov	dx, offset _pcspeaker_interrupt
		call	_set_timer_int
		sub	ax, 0F00h
		mov	[cs:_word_1519B], ax
		mov	[cs:_word_151A3], 0F000h
		popf
		clc
		retn
endp		_pcspeaker_init


; =============== S U B	R O U T	I N E =======================================


proc		_pcspeaker_set near	; DATA XREF: seg003:0D2Ao
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
		call	_configure_timer
		retn
endp		_pcspeaker_set

; ---------------------------------------------------------------------------

_pcspeaker_interrupt:			; DATA XREF: _pcspeaker_init+15o
		push	bx
		push	ds
; ---------------------------------------------------------------------------
		db 0BBh	; ª
_word_1519B	dw 1000h		; DATA XREF: _pcspeaker_init+1Ew
; ---------------------------------------------------------------------------
		mov	ds, bx
		xor	bh, bh
; ---------------------------------------------------------------------------
		db  8Ah	; ä
		db  1Eh
_word_151A3	dw 1234h		; DATA XREF: _pcspeaker_init+22w
					; seg000:51B8w	...
; ---------------------------------------------------------------------------
		mov	bl, [cs:_pc_timer_tbl+bx]
		mov	bh, al
		mov	al, bl
		out	42h, al		; Timer	8253-5 (AT: 8254.2).
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		mov	al, bh
		pop	ds
		pop	bx
		inc	[cs:_word_151A3]
		jz	short loc_151C9
		dec	[cs:_word_14F6C]
		jz	near ptr _timer_int_end
		iret
; ---------------------------------------------------------------------------

loc_151C9:				; CODE XREF: seg000:51BDj
		mov	[cs:_word_151A3], 0F000h
		dec	[cs:_word_14F6C]
		jz	near ptr _timer_int_end
		iret

; =============== S U B	R O U T	I N E =======================================


proc		_pcspeaker_sndoff near	; DATA XREF: seg003:0D40o
		call	_memfill8080
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
endp		_pcspeaker_sndoff


; =============== S U B	R O U T	I N E =======================================


proc		_pcspeaker_clean	near	; DATA XREF: seg003:0D56o
		call	_clean_int8_mem_timr
		retn
endp		_pcspeaker_clean

; ---------------------------------------------------------------------------
_pc_timer_tbl	db 40h,40h,40h,40h,40h,40h,40h,40h,40h,40h,3Fh,3Fh,3Fh
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
; START	OF FUNCTION CHUNK FOR _snd_initialze
nn:					; CODE XREF: _snd_initialze+13j
		db 1Dh,1Ch,1Bh,1Ah,19h,18h,17h,16h,15h,14h,13h,12h,11h
		db 11h,10h,10h,0Fh,0Fh,0Eh,0Eh,0Dh,0Dh,0Dh,0Ch,0Ch,0Ch
		db 0Ch,0Bh,0Bh,0Bh,0Bh,0Ah,0Ah,0Ah,0Ah,0Ah,9,9,9,9,9,9
		db 9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,6,6,6,6
		db 6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4
		db 4,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1
		db 1,1,1,1,1
; ---------------------------------------------------------------------------

_midi_init:				; DATA XREF: seg003:0D16o
		mov	[_sndflags_24622], 12h
		mov	[_byte_24623], 1
		mov	[_bit_mode], 8
		mov	ax, [_snd_base_port]
		cmp	ax, 0FFFFh
		jnz	short loc_15302
		mov	ax, 330h

loc_15302:				; CODE XREF: _snd_initialze+1107j
		mov	[_word_2465C], ax
		mov	[_snd_base_port], ax
		mov	[off_245CA], offset _nullsub_4
		mov	[off_245C8], offset _midi_15466
		mov	[off_245CC], offset _midi_154AC
		mov	[off_245CE], offset _midi_1544D
		mov	bx, offset _volume_25908
		mov	ah, 1

loc_15325:				; CODE XREF: _snd_initialze+1146j
		mov	al, ah
		and	al, 0Fh
		mov	[bx+18h], al
		and	[byte ptr bx+17h], 0FEh
		mov	[byte ptr bx+35h], 0
		add	bx, 50h	; 'P'
		inc	ah
		cmp	ah, 10h
		jbe	short loc_15325
		call	_midi_153C0
		call	_midi_153D6
		clc
		retn
; END OF FUNCTION CHUNK	FOR _snd_initialze

; =============== S U B	R O U T	I N E =======================================


proc		_midi_set near		; DATA XREF: seg003:0D2Co
		mov	bx, offset _midi_int8p
		mov	dx, cs
		mov	al, 8
		call	_setint_vect
		retn
endp		_midi_set

; ---------------------------------------------------------------------------

; =============== S U B	R O U T	I N E =======================================


proc		_midi_int8p far		; DATA XREF: _midi_seto
		pushad
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		push	ds
		push	es
		push	fs
		push	gs
		mov	ax, seg003
		mov	ds, ax
		assume es:nothing
		cmp	[_byte_24671], 1
		jz	short loc_1539A
		inc	[_byte_24668]
		mov	al, [_byte_24668]
		cmp	al, [_byte_24667]
		jnb	short loc_1538F
		mov	bx, offset _volume_25908
		mov	cx, [_word_245D4]

loc_15380:				; CODE XREF: _midi_int8p+37j
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

loc_1538F:				; CODE XREF: _midi_int8p+23j
		mov	[_byte_24668], 0
		call	sub_135CA
		call	loc_14111

loc_1539A:				; CODE XREF: _midi_int8p+16j
					; _midi_int8p+39j
		pop	gs
		pop	fs
		pop	es
		pop	ds
		popad
		iret
endp		_midi_int8p


; =============== S U B	R O U T	I N E =======================================


proc		_midi_sndoff near	; DATA XREF: seg003:0D42o
		mov	dx, [word ptr cs:_int8addr+2]
		mov	bx, [word ptr cs:_int8addr]
		mov	al, 8
		call	_setint_vect
		call	_clean_timer
		call	_midi_153D6
		retn
endp		_midi_sndoff


; =============== S U B	R O U T	I N E =======================================


proc		_midi_clean near		; DATA XREF: seg003:0D58o
		mov	ah, 0FFh
		call	_midi_153F1
		retn
endp		_midi_clean


; =============== S U B	R O U T	I N E =======================================


proc		_midi_153C0 near		; CODE XREF: _snd_initialze+1148p
		mov	ah, 0FFh
		call	_midi_153F1
		mov	cx, 8000h
		call	_midi_15442
		mov	ah, 3Fh	; '?'
		call	_midi_153F1
		xor	cx, cx
		call	_midi_15442
		retn
endp		_midi_153C0


; =============== S U B	R O U T	I N E =======================================


proc		_midi_153D6 near		; CODE XREF: _snd_initialze+114Bp
					; _midi_sndoff+12p
		xor	bl, bl

loc_153D8:				; CODE XREF: _midi_153D6+18j
		mov	ah, 0B0h ; '∞'
		or	ah, bl
		call	_midi_15413
		mov	ah, 7Bh	; '{'
		call	_midi_15413
		xor	ah, ah
		call	_midi_15413
		inc	bl
		cmp	bl, 10h
		jb	short loc_153D8
		retn
endp		_midi_153D6


; =============== S U B	R O U T	I N E =======================================


proc		_midi_153F1 near		; CODE XREF: _midi_clean+2p
					; _midi_153C0+2p ...
		mov	dx, [_word_2465C]
		inc	dx
		xor	cx, cx

loc_153F8:				; CODE XREF: _midi_153F1+Dj
		in	al, dx
		test	al, 40h
		jz	short loc_15401
		dec	cx
		jnz	short loc_153F8
		retn
; ---------------------------------------------------------------------------

loc_15401:				; CODE XREF: _midi_153F1+Aj
		mov	al, ah
		out	dx, al
		xor	cx, cx

loc_15406:				; CODE XREF: _midi_153F1+1Bj
		in	al, dx
		shl	al, 1
		jnb	short loc_1540E
		dec	cx
		jnz	short loc_15406

loc_1540E:				; CODE XREF: _midi_153F1+18j
		dec	dx
		in	al, dx
		cmp	al, 0FEh ; '˛'
		retn
endp		_midi_153F1


; =============== S U B	R O U T	I N E =======================================


proc		_midi_15413 near		; CODE XREF: _midi_153D6+6p
					; _midi_153D6+Bp ...
		or	ah, ah
		jns	short loc_15421
		cmp	ah, [_byte_24677]
		jz	short locret_15441
		mov	[_byte_24677], ah

loc_15421:				; CODE XREF: _midi_15413+2j
		mov	dx, [_word_2465C]
		inc	dx
		mov	cl, 0FFh

loc_15428:				; CODE XREF: _midi_15413+23j
		in	al, dx
		test	al, 40h
		jz	short loc_15439
		shl	al, 1
		jb	short loc_15434
		dec	dx
		in	al, dx
		inc	dx

loc_15434:				; CODE XREF: _midi_15413+1Cj
		dec	cl
		jnz	short loc_15428
		retn
; ---------------------------------------------------------------------------

loc_15439:				; CODE XREF: _midi_15413+18j
		dec	dx
		mov	al, ah
		out	dx, al
		sub	[_byte_24678], al

locret_15441:				; CODE XREF: _midi_15413+8j
		retn
endp		_midi_15413


; =============== S U B	R O U T	I N E =======================================


proc		_midi_15442 near		; CODE XREF: _midi_153C0+8p
					; _midi_153C0+12p
		mov	dx, [_word_2465C]
		inc	dx

loc_15447:				; CODE XREF: _midi_15442+7j
		in	al, dx
		dec	cx
		jnz	short loc_15447
		retn
endp		_midi_15442


; =============== S U B	R O U T	I N E =======================================


proc		_nullsub_4 near		; DATA XREF: _snd_initialze+1112o
		retn
endp		_nullsub_4


; =============== S U B	R O U T	I N E =======================================


proc		_midi_1544D near		; CODE XREF: _midi_15466+6p
					; DATA XREF: _snd_initialze+1124o
		and	[byte ptr bx+17h], 0FEh
		call	_midi_154DA
		or	ah, 80h
		call	_midi_15413
		call	_midi_154DE
		call	_midi_15413
		mov	ah, 7Fh	; ''
		call	_midi_15413
		retn
endp		_midi_1544D


; =============== S U B	R O U T	I N E =======================================


proc		_midi_15466 near		; DATA XREF: _snd_initialze+1118o
		test	[byte ptr bx+17h], 0FEh
		jz	short loc_1546F
		call	_midi_1544D

loc_1546F:				; CODE XREF: _midi_15466+4j
		or	[byte ptr bx+17h], 1
		mov	al, [bx+2]
		cmp	al, [bx+3]
		jz	short loc_1548D
		mov	[bx+3],	al
		call	_midi_154DA
		or	ah, 0C0h
		call	_midi_15413
		mov	ah, [bx+2]
		call	_midi_15413

loc_1548D:				; CODE XREF: _midi_15466+13j
		mov	al, [bx+8]
		call	_midi_154AC
		call	_midi_154DA
		or	ah, 90h
		call	_midi_15413
		call	_midi_154DE
		call	_midi_15413
		mov	ah, 7Fh	; ''
		call	_midi_15413
		or	[byte ptr bx+17h], 1
		retn
endp		_midi_15466


; =============== S U B	R O U T	I N E =======================================


proc		_midi_154AC near		; CODE XREF: _midi_15466+2Ap
					; DATA XREF: _snd_initialze+111Eo
		cmp	al, [_byte_2467D]
		jb	short loc_154B5
		mov	al, [_byte_2467D]

loc_154B5:				; CODE XREF: _midi_154AC+4j
		cmp	al, [bx+1Bh]
		jz	short locret_154D9
		mov	[bx+1Bh], al
		movzx	di, al
		call	_midi_154DA
		or	ah, 0B0h
		call	_midi_15413
		mov	ah, 7
		call	_midi_15413
		mov	al, 80h	; 'Ä'
		add	di, [off_24656]
		mul	[byte ptr di]
		call	_midi_15413

locret_154D9:				; CODE XREF: _midi_154AC+Cj
		retn
endp		_midi_154AC


; =============== S U B	R O U T	I N E =======================================


proc		_midi_154DA near		; CODE XREF: _midi_1544D+4p
					; _midi_15466+18p ...
		mov	ah, [bx+18h]
		retn
endp		_midi_154DA


; =============== S U B	R O U T	I N E =======================================


proc		_midi_154DE near		; CODE XREF: _midi_1544D+Dp
					; _midi_15466+36p
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
endp		_midi_154DE


; =============== S U B	R O U T	I N E =======================================


proc		sub_154F4 near		; CODE XREF: sub_15577+9p sub_1609F+9p
		mov	ax, [_word_245E4]
		shr	ax, 4
		mov	[_byte_24683], al
		push	bx
		push	si
		mov	bx, [si+26h]
		mov	eax, [si+4]
		shr	eax, 16h
		add	bx, ax
		call	_ems_mapmem
		pop	si
		pop	bx
		mov	eax, [si+4]
		shr	eax, 0Ch
		cmp	[word ptr si+26h], 0FFFFh
		jz	short loc_15525
		and	eax, 3FFh

loc_15525:				; CODE XREF: sub_154F4+29j
		add	ax, [si+24h]
		mov	es, ax
		movzx	ebx, [byte ptr si+23h]
		mov	ax, [si+36h]
		mov	[_word_24614], ax
		mov	[_byte_24616], 0
		test	[_flag_playsetttings], 10h
		jz	short _lc_inerpol_disabld
		cmp	al, ah
		setnz	ah		; dosbox:  setnz sp
		mov	[_byte_24616], ah
		movzx	ebx, al

_lc_inerpol_disabld:			; CODE XREF: sub_154F4+4Bj
		shl	ebx, 9
		add	bx, offset _vlm_byte_table
		movzx	ebp, [word ptr si+20h]
		mov	ax, bp
		mov	ch, al
		shr	ebp, 8
		mov	esi, [si+4]
		mov	ax, si
		mov	cl, al
		and	esi, 0FFFh
		shr	esi, 8
		retn
endp		sub_154F4


; =============== S U B	R O U T	I N E =======================================


proc		sub_15577 near		; CODE XREF: sub_16C69:loc_16CB9p
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

		test	[byte ptr si+17h], 1
		jz	locret_157BC
		push	si
		call	sub_154F4
		test	[_flag_playsetttings], 10h
		jnz	_lc_perfrm_interpol
		cmp	[_byte_24625], 1
		jz	loc_15E48
		xor	edx, edx
		mov	ax, [_word_245E4]
		and	eax, 0Fh
		jmp	[cs:_offs_noninterp+eax*2]
endp		sub_15577 ; sp-analysis	failed

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
		cmp	[_byte_24683], 0
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
		dec	[_byte_24683]
		jnz	loc_156A1

loc_1578C:				; CODE XREF: sub_1609F-A02j
					; sub_15577+5E0j ...
		mov	eax, esi
		shl	eax, 8
		mov	al, cl
		pop	si
		mov	cx, [_word_24614]
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
		test	[byte ptr si+19h], 8
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
		and	[byte ptr si+17h], 0FEh
		mov	[byte ptr si+35h], 0
		retn
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_15577

_lc_perfrm_interpol:			; CODE XREF: sub_15577+11j
		mov	al, ch
		cmp	al, [cs:_byte_158B4]
		jz	short loc_15877
		mov	[cs:_byte_158B4], al
		mov	[cs:_byte_158E3], al
		mov	[cs:_byte_15912], al
		mov	[cs:_byte_15941], al
		mov	[cs:_byte_15970], al
		mov	[cs:_byte_1599F], al
		mov	[cs:_byte_159CE], al
		mov	[cs:_byte_159FD], al
		mov	[cs:_byte_15A2C], al
		mov	[cs:_byte_15A5B], al
		mov	[cs:_byte_15A8A], al
		mov	[cs:_byte_15AB9], al
		mov	[cs:_byte_15AE8], al
		mov	[cs:_byte_15B17], al
		mov	[cs:_byte_15B46], al
		mov	[cs:_byte_15B81], al
		mov	[cs:_byte_15BAD], al
		mov	[cs:_byte_15BDA], al
		mov	[cs:_byte_15C07], al
		mov	[cs:_byte_15C34], al
		mov	[cs:_byte_15C61], al
		mov	[cs:_byte_15C8E], al
		mov	[cs:_byte_15CBB], al
		mov	[cs:_byte_15CE8], al
		mov	[cs:_byte_15D15], al
		mov	[cs:_byte_15D42], al
		mov	[cs:_byte_15D6F], al
		mov	[cs:_byte_15D9C], al
		mov	[cs:_byte_15DC9], al
		mov	[cs:_byte_15DF6], al
		mov	[cs:_byte_15E23], al

loc_15877:				; CODE XREF: sub_15577+282j
		and	ecx, 0FFh
		mov	ax, [_word_245E4]
		and	eax, 0Fh
		xor	edx, edx
		jmp	[cs:_offs_interpol+eax*2]

loc_15891:				; CODE XREF: sub_15577+28j
					; sub_1609F+28j ...
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_158B4	db 0			; DATA XREF: sub_15577+27Dr
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_158E3	db 0			; DATA XREF: sub_15577+288w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15912	db 0			; DATA XREF: sub_15577+28Cw
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15941	db 0			; DATA XREF: sub_15577+290w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15970	db 0			; DATA XREF: sub_15577+294w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_1599F	db 0			; DATA XREF: sub_15577+298w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_159CE	db 0			; DATA XREF: sub_15577+29Cw
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_159FD	db 0			; DATA XREF: sub_15577+2A0w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15A2C	db 0			; DATA XREF: sub_15577+2A4w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15A5B	db 0			; DATA XREF: sub_15577+2A8w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15A8A	db 0			; DATA XREF: sub_15577+2ACw
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15AB9	db 0			; DATA XREF: sub_15577+2B0w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15AE8	db 0			; DATA XREF: sub_15577+2B4w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15B17	db 0			; DATA XREF: sub_15577+2B8w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15B46	db 0			; DATA XREF: sub_15577+2BCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15B52:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		cmp	[_byte_24683], 0
		jz	loc_1578C

loc_15B5B:				; CODE XREF: seg000:5E41j
		xor	edx, edx
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15B81	db 0			; DATA XREF: sub_15577+2C0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15BAD	db 0			; DATA XREF: sub_15577+2C4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+8],	eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15BDA	db 0			; DATA XREF: sub_15577+2C8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+10h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15C07	db 0			; DATA XREF: sub_15577+2CCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+18h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15C34	db 0			; DATA XREF: sub_15577+2D0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+20h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15C61	db 0			; DATA XREF: sub_15577+2D4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+28h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15C8E	db 0			; DATA XREF: sub_15577+2D8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+30h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15CBB	db 0			; DATA XREF: sub_15577+2DCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+38h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15CE8	db 0			; DATA XREF: sub_15577+2E0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+40h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15D15	db 0			; DATA XREF: sub_15577+2E4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+48h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15D42	db 0			; DATA XREF: sub_15577+2E8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+50h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15D6F	db 0			; DATA XREF: sub_15577+2ECw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+58h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15D9C	db 0			; DATA XREF: sub_15577+2F0w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+60h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15DC9	db 0			; DATA XREF: sub_15577+2F4w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+68h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15DF6	db 0			; DATA XREF: sub_15577+2F8w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+70h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_15E23	db 0			; DATA XREF: sub_15577+2FCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+78h], eax
		add	di, 80h	; 'Ä'
		mov	dx, offset loc_15E3D
		cmp	[_byte_24616], 1
		jz	loc_1690B

loc_15E3D:				; DATA XREF: seg000:5E31o
		dec	[_byte_24683]
		jnz	loc_15B5B
		jmp	loc_1578C
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15E48:				; CODE XREF: sub_15577+1Aj
		xor	edx, edx
		mov	ax, [_word_245E4]
		and	eax, 0Fh
		jmp	[cs:off_18E60+eax*2]

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
		cmp	[_byte_24683], 0
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
		dec	[_byte_24683]
		jnz	loc_15F81
		jmp	loc_1578C
; END OF FUNCTION CHUNK	FOR sub_15577

; =============== S U B	R O U T	I N E =======================================


proc		sub_1609F near		; CODE XREF: sub_16C69+4Bp
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

		test	[byte ptr si+17h], 1
		jz	loc_16BB0
		push	si
		call	sub_154F4
		test	[_flag_playsetttings], 10h
		jnz	_lc_perfrm_interpol2
		cmp	[_byte_24625], 1
		jz	loc_16959
		xor	edx, edx
		mov	ax, [_word_245E4]
		and	eax, 0Fh
		jmp	[cs:_offs_noninterp2+eax*2]
endp		sub_1609F ; sp-analysis	failed


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
					; _eff_139B9+86j ...
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

loc_16165:				; CODE XREF: _snd_initialze+13j
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
					; DATA XREF: seg000:_offs_noninterp2o
		cmp	[_byte_24683], 0
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
		dec	[_byte_24683]
		jnz	loc_161C9
		jmp	loc_1578C
; ---------------------------------------------------------------------------

_lc_perfrm_interpol2:			; CODE XREF: sub_1609F+11j
		mov	al, ch
		cmp	al, [cs:_byte_16379]
		jz	short loc_1633C
		mov	[cs:_byte_16379], al
		mov	[cs:_byte_163A8], al
		mov	[cs:_byte_163D7], al
		mov	[cs:_byte_16406], al
		mov	[cs:_byte_16435], al
		mov	[byte ptr cs:unk_16464], al
		mov	[cs:_byte_16493], al
		mov	[cs:_byte_164C2], al
		mov	[cs:_byte_164F1], al
		mov	[cs:_byte_16520], al
		mov	[cs:_byte_1654F], al
		mov	[cs:_byte_1657E], al
		mov	[byte ptr cs:unk_165AD], al
		mov	[cs:_byte_165DC], al
		mov	[cs:_byte_1660B], al
		mov	[cs:_byte_16646], al
		mov	[cs:_byte_16672], al
		mov	[cs:_byte_1669F], al
		mov	[cs:_byte_166CC], al
		mov	[cs:_byte_166F9], al
		mov	[cs:_byte_16726], al
		mov	[cs:_byte_16753], al
		mov	[cs:_byte_16780], al
		mov	[cs:_byte_167AD], al
		mov	[cs:_byte_167DA], al
		mov	[cs:_byte_16807], al
		mov	[cs:_byte_16834], al
		mov	[cs:_byte_16861], al
		mov	[cs:_byte_1688E], al
		mov	[cs:_byte_168BB], al
		mov	[cs:_byte_168E8], al

loc_1633C:				; CODE XREF: sub_1609F+21Fj
		and	ecx, 0FFh
		mov	ax, [_word_245E4]
		and	eax, 0Fh
		xor	edx, edx
		jmp	[cs:_offs_interpol2+eax*2]

loc_16356:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DFEo
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]

loc_16369:				; CODE XREF: _snd_initialze+13j
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16379	db 0			; DATA XREF: sub_1609F+21Ar
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_163A8	db 0			; DATA XREF: sub_1609F+225w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_163D7	db 0			; DATA XREF: sub_1609F+229w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16406	db 0			; DATA XREF: sub_1609F+22Dw
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16435	db 0			; DATA XREF: sub_1609F+231w
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
		movsx	edx, [word ptr ebx+edx*2]
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16493	db 0			; DATA XREF: sub_1609F+239w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_164C2	db 0			; DATA XREF: sub_1609F+23Dw
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_164F1	db 0			; DATA XREF: sub_1609F+241w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16520	db 0			; DATA XREF: sub_1609F+245w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_1654F	db 0			; DATA XREF: sub_1609F+249w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_1657E	db 0			; DATA XREF: sub_1609F+24Dw
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
		movsx	edx, [word ptr ebx+edx*2]
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_165DC	db 0			; DATA XREF: sub_1609F+255w
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_1660B	db 0			; DATA XREF: sub_1609F+259w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_16617:				; CODE XREF: sub_1609F+28j
					; sub_1609F+2AEj
					; DATA XREF: ...
		cmp	[_byte_24683], 0
		jz	loc_1578C

loc_16620:				; CODE XREF: seg000:6904j
		xor	edx, edx
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16646	db 0			; DATA XREF: sub_1609F+25Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16672	db 0			; DATA XREF: sub_1609F+261w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+8],	eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde

loc_16689:
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_1669F	db 0			; DATA XREF: sub_1609F+265w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+10h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_166CC	db 0			; DATA XREF: sub_1609F+269w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+18h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_166F9	db 0			; DATA XREF: sub_1609F+26Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+20h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16726	db 0			; DATA XREF: sub_1609F+271w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+28h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16753	db 0			; DATA XREF: sub_1609F+275w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+30h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde

loc_1676A:				; CODE XREF: _snd_initialze+13j
					; _snd_initialze+13j
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16780	db 0			; DATA XREF: sub_1609F+279w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+38h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_167AD	db 0			; DATA XREF: sub_1609F+27Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+40h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_167DA	db 0			; DATA XREF: sub_1609F+281w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+48h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16807	db 0			; DATA XREF: sub_1609F+285w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+50h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16834	db 0			; DATA XREF: sub_1609F+289w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+58h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_16861	db 0			; DATA XREF: sub_1609F+28Dw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+60h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_1688E	db 0			; DATA XREF: sub_1609F+291w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+68h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_168BB	db 0			; DATA XREF: sub_1609F+295w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+70h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; Ä
		db 0C1h	; ¡
_byte_168E8	db 0			; DATA XREF: sub_1609F+299w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+78h], eax
		add	di, 80h	; 'Ä'
		mov	dx, offset loc_16900
		cmp	[_byte_24616], 1
		jz	short loc_1690B

loc_16900:				; DATA XREF: seg000:68F6o
		dec	[_byte_24683]
		jnz	loc_16620
		jmp	loc_1578C
; ---------------------------------------------------------------------------

loc_1690B:				; CODE XREF: seg000:5E39j seg000:68FEj
		mov	ax, [_word_24614]
		cmp	al, ah
		ja	short loc_16929
		add	al, 4
		cmp	al, ah
		jnb	short loc_16942
		mov	[byte ptr _word_24614], al
		movzx	ebx, al
		shl	ebx, 9
		add	bx, offset _vlm_byte_table
		jmp	dx
; ---------------------------------------------------------------------------

loc_16929:				; CODE XREF: seg000:6910j
		sub	al, 4
		jbe	short loc_16942
		cmp	al, ah
		jbe	short loc_16942
		mov	[byte ptr _word_24614], al
		movzx	ebx, al
		shl	ebx, 9
		add	bx, offset _vlm_byte_table
		jmp	dx
; ---------------------------------------------------------------------------

loc_16942:				; CODE XREF: seg000:6916j seg000:692Bj ...
		mov	[byte ptr _word_24614], ah
		mov	[_byte_24616], 0
		movzx	ebx, ah
		shl	ebx, 9
		add	bx, offset _vlm_byte_table
		jmp	dx
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_16959:				; CODE XREF: sub_1609F+1Aj
		xor	edx, edx
		mov	ax, [_word_245E4]
		and	eax, 0Fh

loc_16963:				; CODE XREF: _snd_initialze+13j
		jmp	[cs:off_18E00+eax*2]

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
		cmp	[_byte_24683], 0
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
		dec	[_byte_24683]
		jnz	loc_16A92
		jmp	loc_1578C
; ---------------------------------------------------------------------------

loc_16BB0:				; CODE XREF: sub_1609F+4j
		mov	cx, [_word_245E4]
		mov	bx, cx
		shr	cx, 4
		xor	eax, eax
		and	bx, 0Fh
		shl	bx, 1
		jmp	[cs:off_18E80+bx]

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
		jcxz	short locret_16C68

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

loc_16C66:				; CODE XREF: _snd_initialze+13j
		jnz	short loc_16C22

locret_16C68:				; CODE XREF: sub_1609F:loc_16C20j
		retn
; END OF FUNCTION CHUNK	FOR sub_1609F

; =============== S U B	R O U T	I N E =======================================


proc		sub_16C69 near		; CODE XREF: sub_13017:loc_13038p
					; _proaud_14700+783p ...

; FUNCTION CHUNK AT 71D3 SIZE 0000008C BYTES
; FUNCTION CHUNK AT 77EF SIZE 00000035 BYTES

		call	_ems_save_mapctx
		cld
		mov	ax, [_word_245E8]
		mov	[_word_245E4], ax
		dec	[_word_245EE]
		jnz	short loc_16C88
		call	sub_140B6
		mov	ax, [_word_245EA]
		mov	[_word_245E4], ax
		mov	ax, [_word_245EC]
		mov	[_word_245EE], ax

loc_16C88:				; CODE XREF: sub_16C69+Ej
		mov	[_byte_24682], 0
		cmp	[_byte_24623], 1
		jz	loc_171D3
		mov	si, offset _volume_25908
		mov	cx, [_word_245D4]

loc_16C9D:				; CODE XREF: sub_16C69+59j
		cmp	[byte ptr si+1Dh], 0
		jnz	short loc_16CBE
		push	cx
		push	si
		mov	di, offset _chrin
		test	[_byte_24682], 1
		jnz	short loc_16CB9
		or	[_byte_24682], 1
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
		mov	di, [_word_24600]
		mov	cx, [_word_245E4]
		mov	si, (offset _chrin+1)
		mov	es, [word ptr _dma_buf_pointer+2]
		assume es:nothing
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
		jcxz	short loc_16CEE

loc_16CEB:				; CODE XREF: sub_16C69+71j
		call	sub_16CF6

loc_16CEE:				; CODE XREF: sub_16C69+80j
		mov	[_word_24600], di
		call	_ems_restore_mapctx
		retn
endp		sub_16C69


; =============== S U B	R O U T	I N E =======================================


proc		sub_16CF6 near		; CODE XREF: sub_16C69+7Ap
					; sub_16C69:loc_16CEBp
		cmp	[_byte_24625], 1
		jz	loc_16E24
		mov	bx, cx
		and	bx, 0Fh
		shl	bx, 1
		jmp	[cs:off_18EA0+bx]

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
		jmp	[cs:off_18EC0+bx]

loc_16E3F:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 8
		mov	bx, offset loc_16E56
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
					; _eff_139B9+86j ...
		mov	bx, offset loc_16E74
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
		mov	bx, offset loc_16E92
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
		mov	bx, offset loc_16EB0
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
		mov	bx, offset loc_16ECE
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
		mov	bx, offset loc_16EEC
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
		mov	bx, offset loc_16F0A
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
		mov	bx, offset loc_16F28
		cmp	eax, ebp

loc_16F1D:				; CODE XREF: _snd_initialze+13j
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
		mov	bx, offset loc_16F46
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
		mov	bx, offset loc_16F64
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
		mov	bx, offset loc_16F82
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
		mov	bx, offset loc_16FA0
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
		mov	bx, offset loc_16FBE
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
		mov	bx, offset loc_16FDC
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
		mov	bx, offset loc_16FFA
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
		mov	bx, offset loc_1701C
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1701C:				; DATA XREF: sub_16CF6+315o
		xor	ah, 80h
		mov	[es:di], ah
		mov	eax, [si+8]
		mov	bx, offset loc_17037
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17037:				; DATA XREF: sub_16CF6+330o
		xor	ah, 80h
		mov	[es:di+1], ah
		mov	eax, [si+10h]
		mov	bx, offset loc_17053
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17053:				; DATA XREF: sub_16CF6+34Co
		xor	ah, 80h
		mov	[es:di+2], ah
		mov	eax, [si+18h]
		mov	bx, offset loc_1706F
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1706F:				; DATA XREF: sub_16CF6+368o
		xor	ah, 80h
		mov	[es:di+3], ah
		mov	eax, [si+20h]
		mov	bx, offset loc_1708B
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1708B:				; DATA XREF: sub_16CF6+384o
		xor	ah, 80h
		mov	[es:di+4], ah
		mov	eax, [si+28h]
		mov	bx, offset loc_170A7
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_170A7:				; DATA XREF: sub_16CF6+3A0o
		xor	ah, 80h
		mov	[es:di+5], ah
		mov	eax, [si+30h]
		mov	bx, offset loc_170C3
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_170C3:				; DATA XREF: sub_16CF6+3BCo
		xor	ah, 80h
		mov	[es:di+6], ah
		mov	eax, [si+38h]
		mov	bx, offset loc_170DF
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_170DF:				; DATA XREF: sub_16CF6+3D8o
		xor	ah, 80h
		mov	[es:di+7], ah
		mov	eax, [si+40h]
		mov	bx, offset loc_170FB
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_170FB:				; DATA XREF: sub_16CF6+3F4o
		xor	ah, 80h
		mov	[es:di+8], ah
		mov	eax, [si+48h]
		mov	bx, offset loc_17117
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17117:				; DATA XREF: sub_16CF6+410o
		xor	ah, 80h
		mov	[es:di+9], ah
		mov	eax, [si+50h]
		mov	bx, offset loc_17133
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17133:				; DATA XREF: sub_16CF6+42Co
		xor	ah, 80h
		mov	[es:di+0Ah], ah
		mov	eax, [si+58h]
		mov	bx, offset loc_1714F
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1714F:				; DATA XREF: sub_16CF6+448o
		xor	ah, 80h
		mov	[es:di+0Bh], ah
		mov	eax, [si+60h]
		mov	bx, offset loc_1716B
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1716B:				; DATA XREF: sub_16CF6+464o
		xor	ah, 80h
		mov	[es:di+0Ch], ah
		mov	eax, [si+68h]
		mov	bx, offset loc_17187
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17187:				; DATA XREF: sub_16CF6+480o
		xor	ah, 80h
		mov	[es:di+0Dh], ah
		mov	eax, [si+70h]
		mov	bx, offset loc_171A3
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_171A3:				; DATA XREF: sub_16CF6+49Co
		xor	ah, 80h
		mov	[es:di+0Eh], ah
		mov	eax, [si+78h]
		mov	bx, offset loc_171BF
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
endp		sub_16CF6

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_16C69

loc_171D3:				; CODE XREF: sub_16C69+29j
		mov	cx, [_word_245D4]
		mov	si, offset _volume_25908

loc_171DA:				; CODE XREF: sub_16C69+5B7j
		push	cx
		push	si
		cmp	[byte ptr si+1Dh], 0
		jnz	short loc_1721A
		cmp	[byte ptr si+3Ah], 0
		jz	short loc_17202
		mov	di, [off_245E0]
		test	[_byte_24682], 1
		jz	short loc_171F8
		call	sub_15577
		jmp	short loc_1721A
; ---------------------------------------------------------------------------

loc_171F8:				; CODE XREF: sub_16C69+588j
		or	[_byte_24682], 1
		call	sub_1609F
		jmp	short loc_1721A
; ---------------------------------------------------------------------------

loc_17202:				; CODE XREF: sub_16C69+57Dj
		mov	di, [off_245E2]
		test	[_byte_24682], 2
		jz	short loc_17212
		call	sub_15577
		jmp	short loc_1721A
; ---------------------------------------------------------------------------

loc_17212:				; CODE XREF: sub_16C69+5A2j
		or	[_byte_24682], 2
		call	sub_1609F

loc_1721A:				; CODE XREF: sub_16C69+577j
					; sub_16C69+58Dj ...
		pop	si
		pop	cx
		add	si, 50h	; 'P'
		dec	cx
		jnz	short loc_171DA
		cmp	[_bit_mode], 16
		jz	_lc_16bit
		mov	di, [_word_24600]
		mov	cx, [_word_245E4]
		mov	si, (offset _chrin+1)
		mov	es, [word ptr _dma_buf_pointer+2]
		assume es:nothing
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
		jcxz	short loc_17257

loc_17254:				; CODE XREF: sub_16C69+5DAj
		call	sub_1725F

loc_17257:				; CODE XREF: sub_16C69+5E9j
		mov	[_word_24600], di
		call	_ems_restore_mapctx
		retn
; END OF FUNCTION CHUNK	FOR sub_16C69

; =============== S U B	R O U T	I N E =======================================


proc		sub_1725F near		; CODE XREF: sub_16C69+5E3p
					; sub_16C69:loc_17254p
		cmp	[_byte_24625], 1
		jz	loc_17441
		or	si, 1
		mov	edx, 80808080h
		shr	cx, 1
		mov	bx, cx
		and	bx, 0Fh
		shl	bx, 1
		jmp	[cs:off_18EE0+bx]

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
		jmp	[cs:off_18F00+bx]
endp		sub_1725F ; sp-analysis	failed

; START	OF FUNCTION CHUNK FOR sub_1609F

loc_1745C:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, offset loc_17473
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
		mov	bx, offset loc_17491
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
		mov	bx, offset loc_174AF
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
		mov	bx, offset loc_174CD
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
		mov	bx, offset loc_174EB
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
		mov	bx, offset loc_17509
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
		mov	bx, offset loc_17527
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
		mov	bx, offset loc_17545
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

loc_1754F:				; CODE XREF: _snd_initialze+13j
		add	si, 4
		mov	bx, offset loc_17563
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
		mov	bx, offset loc_17581
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
		mov	bx, offset loc_1759F
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
		mov	bx, offset loc_175BD
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
		mov	bx, offset loc_175DB
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
		mov	bx, offset loc_175F9
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
		mov	bx, offset loc_17617
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
		mov	bx, offset loc_17639
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17639:				; DATA XREF: sub_1609F+1589o
		xor	ah, 80h
		mov	[es:di], ah
		mov	eax, [si+4]
		mov	bx, offset loc_17654
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17654:				; DATA XREF: sub_1609F+15A4o
		xor	ah, 80h
		mov	[es:di+1], ah
		mov	eax, [si+8]
		mov	bx, offset loc_17670
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17670:				; DATA XREF: sub_1609F+15C0o
		xor	ah, 80h
		mov	[es:di+2], ah
		mov	eax, [si+0Ch]
		mov	bx, offset loc_1768C
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1768C:				; DATA XREF: sub_1609F+15DCo
		xor	ah, 80h
		mov	[es:di+3], ah
		mov	eax, [si+10h]
		mov	bx, offset loc_176A8
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_176A8:				; DATA XREF: sub_1609F+15F8o
		xor	ah, 80h
		mov	[es:di+4], ah
		mov	eax, [si+14h]
		mov	bx, offset loc_176C4
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_176C4:				; DATA XREF: sub_1609F+1614o
		xor	ah, 80h
		mov	[es:di+5], ah
		mov	eax, [si+18h]
		mov	bx, offset loc_176E0
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_176E0:				; DATA XREF: sub_1609F+1630o
		xor	ah, 80h
		mov	[es:di+6], ah
		mov	eax, [si+1Ch]
		mov	bx, offset loc_176FC
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_176FC:				; DATA XREF: sub_1609F+164Co
		xor	ah, 80h
		mov	[es:di+7], ah
		mov	eax, [si+20h]
		mov	bx, offset loc_17718
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17718:				; DATA XREF: sub_1609F+1668o
		xor	ah, 80h
		mov	[es:di+8], ah
		mov	eax, [si+24h]
		mov	bx, offset loc_17734
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17734:				; DATA XREF: sub_1609F+1684o
		xor	ah, 80h
		mov	[es:di+9], ah
		mov	eax, [si+28h]
		mov	bx, offset loc_17750
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17750:				; DATA XREF: sub_1609F+16A0o
		xor	ah, 80h
		mov	[es:di+0Ah], ah
		mov	eax, [si+2Ch]
		mov	bx, offset loc_1776C
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_1776C:				; DATA XREF: sub_1609F+16BCo
		xor	ah, 80h
		mov	[es:di+0Bh], ah
		mov	eax, [si+30h]
		mov	bx, offset loc_17788
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17788:				; DATA XREF: sub_1609F+16D8o
		xor	ah, 80h
		mov	[es:di+0Ch], ah
		mov	eax, [si+34h]
		mov	bx, offset loc_177A4
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_177A4:				; DATA XREF: sub_1609F+16F4o
		xor	ah, 80h
		mov	[es:di+0Dh], ah
		mov	eax, [si+38h]
		mov	bx, offset loc_177C0
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_177C0:				; DATA XREF: sub_1609F+1710o
		xor	ah, 80h
		mov	[es:di+0Eh], ah
		mov	eax, [si+3Ch]
		mov	bx, offset loc_177DC
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

_lc_16bit:				; CODE XREF: sub_16C69+5BEj
		mov	di, [_word_24600]
		mov	cx, [_word_245E4]
		mov	si, offset _chrin
		mov	es, [word ptr _dma_buf_pointer+2]
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
		jcxz	short loc_1781C

loc_17819:				; CODE XREF: sub_16C69+B9Fj
		call	sub_17824

loc_1781C:				; CODE XREF: sub_16C69+BAEj
		mov	[_word_24600], di
		call	_ems_restore_mapctx
		retn
; END OF FUNCTION CHUNK	FOR sub_16C69

; =============== S U B	R O U T	I N E =======================================


proc		sub_17824 near		; CODE XREF: sub_16C69+BA8p
					; sub_16C69:loc_17819p
		cmp	[_byte_24625], 1
		jz	loc_17A58
		mov	bx, cx
		and	bx, 0Fh
		shl	bx, 1
		jmp	[cs:off_18F20+bx]

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
		jmp	[cs:off_18F40+bx]
endp		sub_17824 ; sp-analysis	failed

; START	OF FUNCTION CHUNK FOR sub_1609F

loc_17A72:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		mov	eax, [si]
		add	si, 4
		mov	bx, offset loc_17A89
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
		mov	bx, offset loc_17AA6
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
		mov	bx, offset loc_17AC3
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
		mov	bx, offset loc_17AE0
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
		mov	bx, offset loc_17AFD
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
		mov	bx, offset loc_17B1A
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
		mov	bx, offset loc_17B37
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
		mov	bx, offset loc_17B54
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
		mov	bx, offset loc_17B71
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
		mov	bx, offset loc_17B8E
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
		mov	bx, offset loc_17BAB
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
		mov	bx, offset loc_17BC8
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
		mov	bx, offset loc_17BE5
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
		mov	bx, offset loc_17C02
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
		mov	bx, offset loc_17C1F
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
		jz	_nullsub_3

loc_17C2C:				; CODE XREF: seg000:7DC1j
		mov	eax, [si]
		mov	bx, offset loc_17C40
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C40:				; DATA XREF: sub_1609F+1B90o
		mov	[es:di], ax
		mov	eax, [si+4]
		mov	bx, offset loc_17C58
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C58:				; DATA XREF: sub_1609F+1BA8o
		mov	[es:di+2], ax
		mov	eax, [si+8]
		mov	bx, offset loc_17C71
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C71:				; DATA XREF: sub_1609F+1BC1o
		mov	[es:di+4], ax
		mov	eax, [si+0Ch]
		mov	bx, offset loc_17C8A
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17C8A:				; DATA XREF: sub_1609F+1BDAo
		mov	[es:di+6], ax
		mov	eax, [si+10h]
		mov	bx, offset loc_17CA3
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17CA3:				; DATA XREF: sub_1609F+1BF3o
		mov	[es:di+8], ax
		mov	eax, [si+14h]
		mov	bx, offset loc_17CBC
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17CBC:				; DATA XREF: sub_1609F+1C0Co
		mov	[es:di+0Ah], ax
		mov	eax, [si+18h]
		mov	bx, offset loc_17CD5
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17CD5:				; DATA XREF: sub_1609F+1C25o
		mov	[es:di+0Ch], ax
		mov	eax, [si+1Ch]
		mov	bx, offset loc_17CEE
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17CEE:				; DATA XREF: sub_1609F+1C3Eo
		mov	[es:di+0Eh], ax
		mov	eax, [si+20h]
		mov	bx, offset loc_17D07
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D07:				; DATA XREF: sub_1609F+1C57o
		mov	[es:di+10h], ax
		mov	eax, [si+24h]
		mov	bx, offset loc_17D20
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8
; END OF FUNCTION CHUNK	FOR sub_1609F

loc_17D20:				; DATA XREF: sub_1609F+1C70o
		mov	[es:di+12h], ax
		mov	eax, [si+28h]
		mov	bx, offset loc_17D39
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D39:				; DATA XREF: seg000:7D28o
		mov	[es:di+14h], ax
		mov	eax, [si+2Ch]
		mov	bx, offset loc_17D52
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D52:				; DATA XREF: seg000:7D41o
		mov	[es:di+16h], ax
		mov	eax, [si+30h]
		mov	bx, offset loc_17D6B
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D6B:				; DATA XREF: seg000:7D5Ao
		mov	[es:di+18h], ax
		mov	eax, [si+34h]
		mov	bx, offset loc_17D84
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D84:				; DATA XREF: seg000:7D73o
		mov	[es:di+1Ah], ax
		mov	eax, [si+38h]
		mov	bx, offset loc_17D9D
		cmp	eax, ebp
		jl	loc_18DB0
		cmp	eax, edx
		jg	loc_18DB8

loc_17D9D:				; DATA XREF: seg000:7D8Co
		mov	[es:di+1Ch], ax
		mov	eax, [si+3Ch]
		mov	bx, offset loc_17DB6
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


proc		_nullsub_3 near		; CODE XREF: sub_1609F+1B89j
		retn
endp		_nullsub_3


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
; START	OF FUNCTION CHUNK FOR _gravis_17F7D

loc_18077:				; CODE XREF: _gravis_17F7D+11j
		stc
		retn
; END OF FUNCTION CHUNK	FOR _gravis_17F7D

; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
asc_182C3	db 0,0,1,3,0,2,0,4,0,0,0,5,6,0,0,7 ; DATA XREF:	_gravis_18216+5r
					; _gravis_18216+Fr
asc_182D3	db 0,1,0,2,0,3,4,5	; DATA XREF: _gravis_18216+19r
					; _gravis_18216+23r

; =============== S U B	R O U T	I N E =======================================


proc		sub_182DB near		; CODE XREF: sub_1279A+44j
					; sub_1279A+5Ep
		mov	[_dma_mode], 44h	; 'D'
		mov	[_byte_24645], 2
		jmp	short loc_182F7
endp		sub_182DB


; =============== S U B	R O U T	I N E =======================================


proc		_nongravis_182E7	near	; CODE XREF: _mod_readfile_11F4E+162p
					; _mod_readfile_11F4E+19Dp
		mov	[_dma_mode], 48h	; 'H'
		mov	bl, [_byte_24673]
		and	bl, 80h
		mov	[_byte_24645], bl

loc_182F7:				; CODE XREF: sub_182DB+Aj
					; _nongravis_182E7+15j
		cmp	[_byte_2466E], 1
		jz	short loc_182F7
		mov	[_word_24636], 0
		mov	bp, ax
		shl	ax, 2
		mov	[_word_2460E], cx
		mov	bx, cx
		shr	cx, 2
		add	cx, ax
		jnb	short loc_18338
		jz	short loc_18338
		neg	ax
		shl	ax, 2
		mov	[_word_2460E], ax
		mov	cx, ax
		sub	bx, ax
		mov	[_word_24636], bx
		add	ax, [word ptr _dma_buf_pointer]
		mov	[_word_24634], ax
		shr	cx, 4
		add	cx, bp
		mov	[_word_24632], cx

loc_18338:				; CODE XREF: _gravis_int+E2p
					; _nongravis_182E7+2Dj ...
		pushf
		cli
		push	bp
		mov	cl, [_dma_channel_0]
		call	_dma_186E3
		pop	bp
		mov	bl, 21h	; '!'
		or	bl, [_byte_24645]
		cmp	[_dma_channel_0], 4
		jb	short loc_18360
		or	bl, 4
		mov	ax, bp
		and	ax, 0C000h
		shr	bp, 1
		and	bp, 1FFFh
		or	bp, ax

loc_18360:				; CODE XREF: _nongravis_182E7+67j
		mov	dx, [_gravis_port]
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
		mov	[_byte_2466E], 1
		mov	al, 41h	; 'A'
		out	dx, al
		add	dl, 2
		mov	al, bl
		out	dx, al
		sub	dl, 2
		popf
		retn
endp		_nongravis_182E7


; =============== S U B	R O U T	I N E =======================================


proc		_adlib_18389 near	; CODE XREF: _adlib_init+Fp
					; _adlib_clean+3p
		xor	ax, ax

loc_1838B:				; CODE XREF: _adlib_18389+9j
		call	_adlib_18395
		inc	al
		cmp	al, 0E8h ; 'Ë'
		jbe	short loc_1838B
		retn
endp		_adlib_18389


; =============== S U B	R O U T	I N E =======================================


proc		_adlib_18395 near	; CODE XREF: _adlib_init+15p
					; _adlib_init+1Bp ...
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
endp		_adlib_18395


; =============== S U B	R O U T	I N E =======================================


proc		_sb16_detect_port near	; CODE XREF: _useless_12D61+22p
					; _sb16_init+Fp	...
		cmp	[_snd_base_port], 0FFFFh
		jz	short loc_183DE
		mov	ax, [_snd_base_port]
		mov	[_sb_base_port],	ax
		call	_CheckSB
		jnb	short loc_1842D

loc_183DE:				; CODE XREF: _sb16_detect_port+5j
		mov	[_sb_base_port],	220h
		call	_CheckSB
		jnb	short loc_1842D
		mov	[_sb_base_port],	240h
		call	_CheckSB
		jnb	short loc_1842D
		mov	[_sb_base_port],	210h
		call	_CheckSB
		jnb	short loc_1842D
		mov	[_sb_base_port],	230h
		call	_CheckSB
		jnb	short loc_1842D
		mov	[_sb_base_port],	250h
		call	_CheckSB
		jnb	short loc_1842D
		mov	[_sb_base_port],	260h
		call	_CheckSB
		jnb	short loc_1842D
		mov	[_sb_base_port],	280h
		call	_CheckSB
		jnb	short loc_1842D
		stc
		retn
; ---------------------------------------------------------------------------

loc_1842D:				; CODE XREF: _sb16_detect_port+10j
					; _sb16_detect_port+1Bj	...
		mov	al, 10h
		call	_WriteSB
		mov	al, 80h	; 'Ä'
		call	_WriteSB
		mov	al, 0E1h ; '·'
		call	_WriteSB
		call	_ReadSB
		mov	ah, al
		call	_ReadSB
		mov	[_word_24654], ax
		clc
		retn
endp		_sb16_detect_port


; =============== S U B	R O U T	I N E =======================================





; =============== S U B	R O U T	I N E =======================================




; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR _sb_detect_irq

loc_184C3:				; CODE XREF: _sb_detect_irq+18j
					; _sb_detect_irq+22j ...
		cmp	[_dma_channel], 0FFh
		jz	short loc_184DC
		mov	al, [_dma_channel]
		mov	[_dma_chn_mask],	al
		cmp	[_bit_mode], 16
		jz	short _sb16_sound_on
		call	_sb16_18540
		jnb	short _sb16_sound_on

loc_184DC:				; CODE XREF: _sb_detect_irq+7Fj
		cmp	[_bit_mode], 8
		jz	short loc_18501
		mov	[_dma_chn_mask],	5
		call	_sb16_18540
		jnb	short _sb16_sound_on
		mov	[_dma_chn_mask],	6
		call	_sb16_18540
		jnb	short _sb16_sound_on
		mov	[_dma_chn_mask],	7
		call	_sb16_18540
		jnb	short _sb16_sound_on

loc_18501:				; CODE XREF: _sb_detect_irq+98j
		mov	[_dma_chn_mask],	1
		call	_sb16_18540
		jnb	short _sb16_sound_on
		mov	[_dma_chn_mask],	3
		call	_sb16_18540
		jnb	short _sb16_sound_on
		mov	[_dma_chn_mask],	0
		call	_sb16_18540
		jnb	short _sb16_sound_on
		mov	dx, offset _aErrorCouldNot_1 ; "Error: Could not	find DMA!\r\n"
		stc
		retn
; END OF FUNCTION CHUNK	FOR _sb_detect_irq

; =============== S U B	R O U T	I N E =======================================


proc		_sb16_sound_on near	; CODE XREF: _sb16_init:loc_14AFDp
					; _sb_detect_irq+8Cj ...
		call	_CheckSB
		mov	al, 0D1h ; '—'
		call	_WriteSB
		mov	ax, [_sb_base_port]
		mov	[_snd_base_port], ax
		mov	al, [_sb_irq_number]
		mov	[_irq_number], al
		mov	al, [_dma_chn_mask]
		mov	[_dma_channel], al
		clc
		retn
endp		_sb16_sound_on


; =============== S U B	R O U T	I N E =======================================


proc		_sb16_18540 near		; CODE XREF: _sb_detect_irq+8Ep
					; _sb_detect_irq+9Fp ...
		mov	[_dma_mode], 48h	; 'H'
		cli
		call	_CheckSB
		mov	[_word_2460E], 2
		mov	[_dma_buf_pointer], 0
		mov	cl, [_dma_chn_mask]
		call	_dma_186E3
		mov	[_sb_int_counter], 1
		mov	si, offset _sb16_handler_int ; myfunc
		mov	al, [_sb_irq_number]
		call	_setsnd_handler
		cmp	[_dma_chn_mask],	4
		jnb	short loc_18591
		mov	al, 40h	; '@'
		call	_WriteSB
		mov	al, 0D3h ; '”'
		call	_WriteSB
		mov	al, 14h
		call	_WriteSB
		mov	ax, [_word_2460E]
		dec	ax
		call	_WriteSB
		mov	al, ah
		call	_WriteSB
		jmp	short loc_185B5
; ---------------------------------------------------------------------------

loc_18591:				; CODE XREF: _sb16_18540+32j
		mov	al, 42h	; 'B'
		call	_WriteSB
		mov	al, 0ACh ; '¨'
		call	_WriteSB
		mov	al, 44h	; 'D'
		call	_WriteSB
		mov	al, 0B6h ; '∂'
		call	_WriteSB
		mov	al, 30h	; '0'
		call	_WriteSB
		mov	ax, [_word_2460E]
		call	_WriteSB
		mov	al, ah
		call	_WriteSB

loc_185B5:				; CODE XREF: _sb16_18540+4Fj
		sti
		xor	cx, cx

loc_185B8:				; CODE XREF: _sb16_18540+7Fj
		cmp	[_sb_int_counter], 1
		jnz	short loc_185CD
		loop	loc_185B8
		call	_restore_intvector
		mov	cl, [_dma_chn_mask]
		call	_set_dmachn_mask
		stc
		retn
; ---------------------------------------------------------------------------

loc_185CD:				; CODE XREF: _sb16_18540+7Dj
		call	_restore_intvector
		mov	cl, [_dma_chn_mask]
		call	_set_dmachn_mask
		clc
		retn
endp		_sb16_18540


; =============== S U B	R O U T	I N E =======================================


; int _sb16_handler_int
proc		_sb16_handler_int far	; DATA XREF: _sb_test_interrupt+5o
					; _sb16_18540+24o
		push	ax
		push	dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	dx, [_sb_base_port]
		add	dl, 0Eh
		in	al, dx		; DMA controller, 8237A-5.
					; Clear	mask registers.
					; Any OUT enables all 4	channels.
		inc	[_sb_int_counter]
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		pop	dx
		pop	ax
		iret
endp		_sb16_handler_int

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


proc		_dma_186E3 near		; CODE XREF: _proaud_set+59p
					; _wss_set+28p ...
		test	[byte ptr _config_word+1], 10h
		jz	short loc_186EF
		and	[_dma_mode], 0EFh

loc_186EF:				; CODE XREF: _dma_186E3+5j
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
		mov	al, [_dma_mode]
		out	0Bh, al		; DMA 8237A-5. mode register bits:
					; 0-1: channel (00=0; 01=1; 10=2; 11=3)
					; 2-3: transfer	type (00=verify=Nop; 01=write; 10=read)
					; 4: 1=enable auto-initialization
					; 5: 1=address increment; 0=address decrement
					; 6-7: 00=demand mode; 01=single; 10=block; 11=cascade
		mov	dx, [word ptr _dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, [word ptr _dma_buf_pointer]
		adc	dx, 0
		add	ax, [word ptr _dword_24694]
		adc	dx, [word ptr _dword_24694+2]
		out	0, al
		mov	al, ah
		out	0, al
		mov	al, dl
		out	87h, al		; DMA page register 74LS612:
					; Channel 0 (address bits 16-23)
		mov	ax, [_word_2460E]
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

loc_18761:				; CODE XREF: _dma_186E3+Fj
		mov	al, 5
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		xor	al, al
		out	0Ch, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	al, [_dma_mode]
		or	al, 1
		out	0Bh, al		; DMA 8237A-5. mode register bits:
					; 0-1: channel (00=0; 01=1; 10=2; 11=3)
					; 2-3: transfer	type (00=verify=Nop; 01=write; 10=read)
					; 4: 1=enable auto-initialization
					; 5: 1=address increment; 0=address decrement
					; 6-7: 00=demand mode; 01=single; 10=block; 11=cascade
		mov	dx, [word ptr _dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, [word ptr _dma_buf_pointer]
		adc	dx, 0
		add	ax, [word ptr _dword_24694]
		adc	dx, [word ptr _dword_24694+2]
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
		mov	ax, [_word_2460E]
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

loc_187A6:				; CODE XREF: _dma_186E3+14j
		mov	al, 6
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		xor	al, al
		out	0Ch, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	al, [_dma_mode]
		or	al, 2
		out	0Bh, al		; DMA 8237A-5. mode register bits:
					; 0-1: channel (00=0; 01=1; 10=2; 11=3)
					; 2-3: transfer	type (00=verify=Nop; 01=write; 10=read)
					; 4: 1=enable auto-initialization
					; 5: 1=address increment; 0=address decrement
					; 6-7: 00=demand mode; 01=single; 10=block; 11=cascade
		mov	dx, [word ptr _dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, [word ptr _dma_buf_pointer]
		adc	dx, 0
		add	ax, [word ptr _dword_24694]
		adc	dx, [word ptr _dword_24694+2]
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
		mov	ax, [_word_2460E]
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

loc_187EB:				; CODE XREF: _dma_186E3+1Bj
		mov	al, 7
		out	0Ah, al		; DMA controller, 8237A-5.
					; single mask bit register
					; 0-1: select channel (00=0; 01=1; 10=2; 11=3)
					; 2: 1=set mask	for channel; 0=clear mask (enable)
		xor	al, al
		out	0Ch, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	al, [_dma_mode]
		or	al, 3
		out	0Bh, al		; DMA 8237A-5. mode register bits:
					; 0-1: channel (00=0; 01=1; 10=2; 11=3)
					; 2-3: transfer	type (00=verify=Nop; 01=write; 10=read)
					; 4: 1=enable auto-initialization
					; 5: 1=address increment; 0=address decrement
					; 6-7: 00=demand mode; 01=single; 10=block; 11=cascade
		mov	dx, [word ptr _dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, [word ptr _dma_buf_pointer]
		adc	dx, 0
		add	ax, [word ptr _dword_24694]
		adc	dx, [word ptr _dword_24694+2]
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
		mov	ax, [_word_2460E]
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

loc_18830:				; CODE XREF: _dma_186E3+22j
		mov	al, 4
		out	0D4h, al
		xor	al, al
		out	0D8h, al
		mov	al, [_dma_mode]
		out	0D6h, al
		movzx	edx, [word ptr _dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, [word ptr _dma_buf_pointer]
		add	eax, edx
		add	eax, [_dword_24694]
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
		mov	ax, [_word_2460E]
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

loc_18878:				; CODE XREF: _dma_186E3+29j
		mov	al, 5
		out	0D4h, al
		xor	al, al
		out	0D8h, al
		mov	al, [_dma_mode]
		or	al, 1
		out	0D6h, al
		movzx	edx, [word ptr _dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, [word ptr _dma_buf_pointer]
		add	eax, edx
		add	eax, [_dword_24694]
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
		mov	ax, [_word_2460E]
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

loc_188C2:				; CODE XREF: _dma_186E3+30j
		mov	al, 6
		out	0D4h, al
		xor	al, al
		out	0D8h, al
		mov	al, [_dma_mode]
		or	al, 2
		out	0D6h, al
		movzx	edx, [word ptr _dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, [word ptr _dma_buf_pointer]
		add	eax, edx
		add	eax, [_dword_24694]
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
		mov	ax, [_word_2460E]
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

loc_1890C:				; CODE XREF: _dma_186E3+37j
		mov	al, 7
		out	0D4h, al
		mov	al, [_dma_mode]
		or	al, 3
		out	0D6h, al
		xor	al, al
		out	0D8h, al
		movzx	edx, [word ptr _dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, [word ptr _dma_buf_pointer]
		add	eax, edx
		add	eax, [_dword_24694]
		shr	eax, 1
		out	0CCh, al	; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	al, ah
		out	0CCh, al	; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		shr	eax, 0Fh
		out	8Ah, al		; DMA page register 74LS612:
					; Channel 7 (address bits 17-23)
		mov	ax, [_word_2460E]
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
endp		_dma_186E3


; =============== S U B	R O U T	I N E =======================================


proc		_set_dmachn_mask	near	; CODE XREF: _proaud_sndoff+1Dp
					; _wss_sndoff+32p ...
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

loc_18961:				; CODE XREF: _set_dmachn_mask+4j
		and	al, 3
		or	al, 4
		out	0D4h, al
		retn
endp		_set_dmachn_mask


; =============== S U B	R O U T	I N E =======================================


proc		_alloc_dma_buf near	; CODE XREF: _mod_readfile_11F4E+92p
					; _volume_prep+47p ...
		mov	[_dword_24684], eax
		mov	[_byte_2469C], cl
		mov	[_memflg_2469A],	0
		mov	[_byte_2469B], 0
		mov	[_dword_24694], 0
		call	_getmemallocstrat
		push	ax
		call	_setmemalloc2
		mov	ebx, [_dword_24684]
		shl	ebx, 1		; bytes
		call	_memalloc
		jb	loc_18A22
		mov	[_myseg_24698], ax
		mov	dx, ax
		mov	ebx, [_dword_24684]
		cmp	[_byte_2469C], 4
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

loc_189DB:				; CODE XREF: _alloc_dma_buf+40j
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

loc_18A0A:				; CODE XREF: _alloc_dma_buf+59j
					; _alloc_dma_buf+71j ...
		mov	[_word_2468C], dx
		mov	ax, [_myseg_24698]
		call	_memrealloc
		pop	ax
		call	_setmemallocstrat
		mov	[_memflg_2469A],	1
		mov	ax, [_word_2468C]
		clc
		retn
; ---------------------------------------------------------------------------

loc_18A22:				; CODE XREF: _alloc_dma_buf+2Dj
		pop	ax
		call	_setmemallocstrat
		stc
		retn
endp		_alloc_dma_buf


; =============== S U B	R O U T	I N E =======================================


proc		_memfree_18A28 near	; CODE XREF: _mod_readfile_11F4E:loc_12117p
					; _mod_readfile_11F4E+1E4p ...
		cmp	[_memflg_2469A],	1
		jnz	short loc_18A3B
		mov	[_memflg_2469A],	0
		mov	ax, [_myseg_24698]
		call	_memfree
		retn
; ---------------------------------------------------------------------------

loc_18A3B:				; CODE XREF: _memfree_18A28+5j
		clc
		retn
endp		_memfree_18A28


; =============== S U B	R O U T	I N E =======================================


; int __usercall _setsnd_handler<eax>(void (__cdecl *myfunc)()<esi>)
proc		_setsnd_handler near	; CODE XREF: _gravis_init+C1p
					; _proaud_set+14p ...
		pushf
		push	es
		cli
		movzx	cx, al
		in	al, 0A1h	; Interrupt Controller #2, 8259A
		mov	ah, al
		in	al, 21h		; Interrupt controller,	8259A.
		mov	[_interrupt_mask], ax
		mov	bx, 0FFFEh
		rol	bx, cl
		cmp	cl, 8
		jb	short loc_18A5C
		and	bl, 0FBh
		add	cl, 60h	; '`'

loc_18A5C:				; CODE XREF: _setsnd_handler+17j
		add	cl, 8
		shl	cx, 2
		and	ax, bx
		out	21h, al		; Interrupt controller,	8259A.
		mov	al, ah
		out	0A1h, al	; Interrupt Controller #2, 8259A
		mov	[_intvectoffset], cx
		mov	bx, cx
		xor	ax, ax
		mov	es, ax
		assume es:nothing
		les	cx, [es:bx]
		assume es:nothing
		mov	[_old_intprocoffset], cx
		mov	[_old_intprocseg], es
		mov	es, ax
		assume es:nothing
		mov	[es:bx], si
		mov	[word ptr es:bx+2], cs
		pop	es
		assume es:nothing
		popf
		retn
endp		_setsnd_handler


; =============== S U B	R O U T	I N E =======================================


proc		_restore_intvector near	; CODE XREF: _gravis_clean+16p
					; _useless_1474C+Fp ...
		pushf
		push	es
		cli
		mov	ax, [_interrupt_mask]
		out	21h, al		; Interrupt controller,	8259A.
		mov	al, ah
		out	0A1h, al	; Interrupt Controller #2, 8259A
		mov	bx, [_intvectoffset]
		xor	ax, ax
		mov	es, ax
		assume es:nothing
		mov	ax, [_old_intprocoffset]
		mov	[es:bx], ax
		mov	ax, [_old_intprocseg]
		mov	[es:bx+2], ax
		pop	es
		assume es:seg003
		popf
		retn
endp		_restore_intvector


; =============== S U B	R O U T	I N E =======================================


proc		_getint_vect near	; CODE XREF: sub_12DA8+67p
		push	es
		mov	ah, 35h
		int	21h		; DOS -	2+ - GET INTERRUPT VECTOR
					; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	dx, es
		pop	es
		assume es:nothing
		retn
endp		_getint_vect


; =============== S U B	R O U T	I N E =======================================


proc		_setint_vect near	; CODE XREF: _set_timer_int+20p
					; _clean_int8_mem_timr+Cp ...
		push	ds
		mov	ds, dx
		mov	dx, bx
		mov	ah, 25h
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds
		retn
endp		_setint_vect


; =============== S U B	R O U T	I N E =======================================


; int __usercall _memalloc<eax>(int bytes<ebx>)
proc		_memalloc near		; CODE XREF: _inr_module:loc_11AC0p
					; _memalloc12k+6p ...
		add	ebx, 0Fh
		shr	ebx, 4
		cmp	ebx, 10000h
		jnb	short loc_18AD9
		mov	ah, 48h
		int	21h		; DOS -	2+ - ALLOCATE MEMORY
					; BX = number of 16-byte paragraphs desired
		retn
; ---------------------------------------------------------------------------

loc_18AD9:				; CODE XREF: _memalloc+Fj
		mov	ax, 8
		stc
		retn
endp		_memalloc


; =============== S U B	R O U T	I N E =======================================


proc		_memfree	near		; CODE XREF: _memfree_125DA+4Fp
					; _memfree_125DA+72p ...
		push	es
		mov	es, ax
		assume es:nothing
		mov	ah, 49h
		int	21h		; DOS -	2+ - FREE MEMORY
					; ES = segment address of area to be freed
		pop	es
		retn
endp		_memfree


; =============== S U B	R O U T	I N E =======================================


proc		_memrealloc near		; CODE XREF: _mem_reallocx+14p
					; _alloc_dma_buf+A9p
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

loc_18AFF:				; CODE XREF: _memrealloc+Fj
		mov	ax, 8
		stc
		retn
endp		_memrealloc


; =============== S U B	R O U T	I N E =======================================


proc		_setmemallocstrat near	; CODE XREF: _deinit_125B9+15p
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
endp		_setmemallocstrat


; =============== S U B	R O U T	I N E =======================================


proc		_getmemallocstrat near	; CODE XREF: sub_12DA8+7Fp
					; _alloc_dma_buf+1Bp
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
endp		_getmemallocstrat


; =============== S U B	R O U T	I N E =======================================


proc		_setmemalloc1 near	; CODE XREF: sub_12D35+12p
					; sub_12DA8+85p
		test	[byte ptr _config_word],	1
		jz	short _setmemalloc2
		mov	ax, 181h
		jmp	short _setmemallocstrat
endp		_setmemalloc1


; =============== S U B	R O U T	I N E =======================================


proc		_setmemalloc2 near	; CODE XREF: _alloc_dma_buf+1Fp
					; _setmemalloc1+5j
		mov	ax, 1
		jmp	short _setmemallocstrat
endp		_setmemalloc2


; =============== S U B	R O U T	I N E =======================================


proc		_WriteMixerSB near	; CODE XREF: _sb_set-F3p
					; _sb_set:loc_14C89p ...
		push	ax
		push	dx
		mov	dx, [_sb_base_port]
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
endp		_WriteMixerSB


; =============== S U B	R O U T	I N E =======================================


proc		_ReadMixerSB near	; CODE XREF: _sb16_init+25p
					; _sb16_init+54p ...
		push	dx
		mov	dx, [_sb_base_port]
		add	dl, 4
		mov	al, ah
		out	dx, al
		jmp	short $+2
		jmp	short $+2
		inc	dx
		in	al, dx
		pop	dx
		retn
endp		_ReadMixerSB


; =============== S U B	R O U T	I N E =======================================


proc		_WriteSB	near		; CODE XREF: _sb_set+32p _sb_set+38p ...
		push	dx
		push	cx
		push	ax
		mov	dx, [_sb_base_port]
		add	dl, 0Ch
		mov	cx, 1000h

loc_18B70:				; CODE XREF: _WriteSB+13j
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

loc_18B7C:				; CODE XREF: _WriteSB+10j
		pop	ax
		out	dx, al
		pop	cx
		pop	dx
		retn
endp		_WriteSB


; =============== S U B	R O U T	I N E =======================================


proc		_ReadSB near		; CODE XREF: _sb16_detect_port+70p
					; _sb16_detect_port+75p	...
		push	dx
		push	cx
		push	ax
		mov	dx, [_sb_base_port]
		add	dl, 0Eh
		mov	cx, 1000h

loc_18B8E:				; CODE XREF: _ReadSB+13j
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

loc_18B9C:				; CODE XREF: _ReadSB+10j
		pop	ax
		sub	dl, 4
		in	al, dx
		pop	cx
		pop	dx
		retn
endp		_ReadSB


; =============== S U B	R O U T	I N E =======================================


proc		_CheckSB	near		; CODE XREF: _sbpro_sndoff+9p
					; _sb16_detect_port+Dp ...
		mov	dx, [_sb_base_port]
		add	dl, 6
		mov	al, 1
		out	dx, al
		mov	ax, 400h

loc_18BB1:				; CODE XREF: _CheckSB+Ej
		dec	ax
		jnz	short loc_18BB1
		out	dx, al
		call	_ReadSB
		cmp	al, 0AAh ; '™'
		jnz	short loc_18BBE
		clc
		retn
; ---------------------------------------------------------------------------

loc_18BBE:				; CODE XREF: _CheckSB+16j
		stc
		retn
endp		_CheckSB


; =============== S U B	R O U T	I N E =======================================


proc		_sb16_sound_off near	; CODE XREF: _sb16_deinit+3p
					; _sbpro_clean+3p ...
		call	_CheckSB
		mov	al, 0D3h ; '”'
		call	_WriteSB
		retn
endp		_sb16_sound_off


; =============== S U B	R O U T	I N E =======================================


proc		_initclockfromrtc near	; CODE XREF: _deinit_125B9+1Bp
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
		assume es:nothing
		mov	[es:46Ch], eax
		retn
endp		_initclockfromrtc


; =============== S U B	R O U T	I N E =======================================


proc		_u32tox near		; CODE XREF: _myasmsprintf+EBp
		ror	eax, 10h
		call	_u16tox
		ror	eax, 10h
endp		_u32tox ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_u16tox near		; CODE XREF: _u32tox+4p
					; _myasmsprintf+D7p
		xchg	al, ah
		call	_u8tox
		mov	al, ah
endp		_u16tox ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_u8tox near		; CODE XREF: _u16tox+2p
					; _myasmsprintf+C4p
		push	ax
		shr	al, 4
		call	_u4tox
		pop	ax
endp		_u8tox ;	sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_u4tox near		; CODE XREF: _u8tox+4p
		and	al, 0Fh
		or	al, '0'
		cmp	al, '9'
		jbe	short loc_18C3D
		add	al, 7

loc_18C3D:				; CODE XREF: _u4tox+6j
		mov	[si], al
		inc	si
		retn
endp		_u4tox


; =============== S U B	R O U T	I N E =======================================


proc		_my_i8toa10_0 near	; CODE XREF: _myasmsprintf+8Ap
		cbw
endp		_my_i8toa10_0


; =============== S U B	R O U T	I N E =======================================


proc		_my_i16toa10_0 near	; CODE XREF: _myasmsprintf+9Dp
		cwde
endp		_my_i16toa10_0 ;	sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_my_i32toa10_0 near	; CODE XREF: _myasmsprintf+B1p
		xor	cx, cx
		or	eax, eax
		jns	short _my_i32toa10_1
		mov	dl, '-'
		call	_my_putdigit
		neg	eax
		jmp	short _my_i32toa10_1
endp		_my_i32toa10_0


; =============== S U B	R O U T	I N E =======================================


proc		_my_u8toa_10 near	; CODE XREF: _myasmsprintf+53p
		xor	ah, ah
endp		_my_u8toa_10


; =============== S U B	R O U T	I N E =======================================


proc		_my_u16toa_10 near	; CODE XREF: _myasmsprintf+65p
		movzx	eax, ax
endp		_my_u16toa_10 ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_my_u32toa10_0 near	; CODE XREF: _myasmsprintf+78p
		xor	cx, cx

_my_i32toa10_1:				; CODE XREF: _my_i32toa10_0+5j
					; _my_i32toa10_0+Fj
		mov	ebx, 10
endp		_my_u32toa10_0 ;	sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_my_u32toa_0 near	; CODE XREF: _my_u32toa_0+Dp
		xor	edx, edx
		div	ebx
		or	eax, eax
		jz	short loc_18C75
		push	edx
		call	_my_u32toa_0
		pop	edx

loc_18C75:				; CODE XREF: _my_u32toa_0+9j
		or	dl, '0'
endp		_my_u32toa_0 ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		_my_putdigit near	; CODE XREF: _my_i32toa10_0+9p
		mov	[si], dl
		inc	si
		inc	cx
		retn
endp		_my_putdigit

; ---------------------------------------------------------------------------
_asmprintf_tbl	dw offset _mysprintf_0_nop ; DATA XREF: _myasmsprintf+1Cr
		dw offset _mysprintf_1_offstr
		dw offset _mysprintf_2_off8str
		dw offset _mysprintf_3_off16str
		dw offset _mysprintf_4_u8toa
		dw offset _mysprintf_5_u16toa
		dw offset _mysprintf_6_u32toa
		dw offset _mysprintf_7_i8toa
		dw offset _mysprintf_8_i16toa
		dw offset _mysprintf_9_i32toa
		dw offset _mysprintf_10_u8tox
		dw offset _mysprintf_11_u16tox
		dw offset _mysprintf_12_u32tox

; =============== S U B	R O U T	I N E =======================================


proc		_myasmsprintf near	; CODE XREF: sub_12D05+20p
		push	es
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

loc_18C9F:				; CODE XREF: _myasmsprintf+Fj
		mov	[di], al
		inc	di

loc_18CA2:				; CODE XREF: _myasmsprintf+5j
					; _myasmsprintf+2Dj ...
		mov	al, [si]
		inc	si
		cmp	al, 20h	; ' '
		jnb	short loc_18C9F
		cmp	al, 0Ch
		ja	short _mysprintf_0_nop
		inc	si
		mov	bl, al
		xor	bh, bh
		shl	bx, 1
		jmp	[cs:_asmprintf_tbl+bx]

_mysprintf_0_nop:			; CODE XREF: _myasmsprintf+13j
					; DATA XREF: seg000:_asmprintf_tblo
		pop	es
		assume es:dseg
		retn
; ---------------------------------------------------------------------------

_mysprintf_1_offstr:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C80o
		push	si
		mov	si, [si]
		call	_strcpy_count_0
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_2_off8str:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C82o
		mov	bx, [si]
		mov	bl, [bx]
		xor	bh, bh
		jmp	short loc_18CD3
; ---------------------------------------------------------------------------

_mysprintf_3_off16str:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C84o
		mov	bx, [si]
		mov	bx, [bx]

loc_18CD3:				; CODE XREF: _myasmsprintf+35j
		push	si
		shl	bx, 1
		mov	si, [si+2]
		mov	si, [bx+si]
		call	_strcpy_count_0
		pop	si
		add	si, 4
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_4_u8toa:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C86o
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	_my_u8toa_10
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_5_u16toa:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C88o
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	_my_u16toa_10
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_6_u32toa:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C8Ao
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	_my_u32toa10_0
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_7_i8toa:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C8Co
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	_my_i8toa10_0
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_8_i16toa:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C8Eo
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	_my_i16toa10_0
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_9_i32toa:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C90o
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	_my_i32toa10_0
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_10_u8tox:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C92o
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	_u8tox
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_11_u16tox:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C94o
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	_u16tox
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

_mysprintf_12_u32tox:			; CODE XREF: _myasmsprintf+1Cj
					; DATA XREF: seg000:8C96o
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	_u32tox
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
endp		_myasmsprintf


; =============== S U B	R O U T	I N E =======================================


proc		_mystrlen_0 near
		mov	ax, -1
		dec	si

loc_18D93:				; CODE XREF: _mystrlen_0+9j
		inc	ax
		inc	si
		cmp	[byte ptr si], 0
		jnz	short loc_18D93
		sub	si, ax
		retn
endp		_mystrlen_0


; =============== S U B	R O U T	I N E =======================================


proc		_strcpy_count_0 near	; CODE XREF: sub_12D05:loc_12D30p
					; _myasmsprintf+26p ...
		xor	cx, cx
		jmp	short loc_18DA6
; ---------------------------------------------------------------------------

loc_18DA1:				; CODE XREF: _strcpy_count_0+Ej
		mov	[es:di], al
		inc	si
		inc	di

loc_18DA6:				; CODE XREF: _strcpy_count_0+2j
		mov	al, [si]
		inc	cx
		or	al, al
		jnz	short loc_18DA1
		retn
endp		_strcpy_count_0

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
_offs_noninterp2	dw offset loc_161C0	; DATA XREF: sub_1609F+28r
		dw offset loc_161B0
		dw offset loc_161A0
		dw offset loc_16190
		dw offset loc_16180
		dw offset loc_16170
		dw offset loc_16160
		dw offset loc_16150
		dw offset loc_16140
		dw offset loc_16130
		dw offset loc_16120
		dw offset loc_16110
		dw offset loc_16100
		dw offset loc_160F0
		dw offset loc_160E0
		dw offset loc_160D0
_offs_interpol2	dw offset loc_16617	; DATA XREF: sub_1609F+2AEr
		dw offset loc_165E8
		dw offset loc_165B9
		dw offset loc_1658A
		dw offset loc_1655B
		dw offset loc_1652C
		dw offset loc_164FD
		dw offset loc_164CE
		dw offset loc_1649F
		dw offset loc_16470
		dw offset loc_16441
		dw offset loc_16412
		dw offset loc_163E3
		dw offset loc_163B4
		dw offset loc_16385
		dw offset loc_16356
off_18E00	dw offset loc_16A89	; DATA XREF: sub_1609F:loc_16963r
		dw offset loc_16A76
		dw offset loc_16A63
		dw offset loc_16A50
		dw offset loc_16A3D
		dw offset loc_16A2A
		dw offset loc_16A17
		dw offset loc_16A04
		dw offset loc_169F1
		dw offset loc_169DE
		dw offset loc_169CB
		dw offset loc_169B8
		dw offset loc_169A5
		dw offset loc_16992
		dw offset loc_1697F
		dw offset loc_1696C
_offs_noninterp	dw offset loc_15698	; DATA XREF: sub_15577+28r
		dw offset loc_15688
		dw offset loc_15678
		dw offset loc_15668
		dw offset loc_15658
		dw offset loc_15648
		dw offset loc_15638
		dw offset loc_15628
		dw offset loc_15618
		dw offset loc_15608
		dw offset loc_155F8
		dw offset loc_155E8
		dw offset loc_155D8
		dw offset loc_155C8
		dw offset loc_155B8
		dw offset loc_155A8
_offs_interpol	dw offset loc_15B52	; DATA XREF: sub_15577+311r
		dw offset loc_15B23
		dw offset loc_15AF4
		dw offset loc_15AC5
		dw offset loc_15A96
		dw offset loc_15A67
		dw offset loc_15A38
		dw offset loc_15A09
		dw offset loc_159DA
		dw offset loc_159AB
		dw offset loc_1597C
		dw offset loc_1594D
		dw offset loc_1591E
		dw offset loc_158EF
		dw offset loc_158C0
		dw offset loc_15891
off_18E60	dw offset loc_15F78	; DATA XREF: sub_15577+8DBr
		dw offset loc_15F65
		dw offset loc_15F52
		dw offset loc_15F3F
		dw offset loc_15F2C
		dw offset loc_15F19
		dw offset loc_15F06
		dw offset loc_15EF3
		dw offset loc_15EE0
		dw offset loc_15ECD
		dw offset loc_15EBA
		dw offset loc_15EA7
		dw offset loc_15E94
		dw offset loc_15E81
		dw offset loc_15E6E
		dw offset loc_15E5B
off_18E80	dw offset loc_16C20	; DATA XREF: sub_1609F+B22r
		dw offset loc_16C1A
		dw offset loc_16C14
		dw offset loc_16C0E
		dw offset loc_16C08
		dw offset loc_16C02
		dw offset loc_16BFC
		dw offset loc_16BF6
		dw offset loc_16BF0
		dw offset loc_16BEA
		dw offset loc_16BE4
		dw offset loc_16BDE
		dw offset loc_16BD8
		dw offset loc_16BD2
		dw offset loc_16BCC
		dw offset loc_16BC6
off_18EA0	dw offset loc_16DB0	; DATA XREF: sub_16CF6+10r
		dw offset loc_16DA5
		dw offset loc_16D9A
		dw offset loc_16D8F
		dw offset loc_16D84
		dw offset loc_16D79
		dw offset loc_16D6E
		dw offset loc_16D63
		dw offset loc_16D58
		dw offset loc_16D4D
		dw offset loc_16D42
		dw offset loc_16D37
		dw offset loc_16D2C
		dw offset loc_16D21
		dw offset loc_16D16
		dw offset loc_16D0B
off_18EC0	dw offset loc_17001	; DATA XREF: sub_16CF6+144r
		dw offset loc_16FE3
		dw offset loc_16FC5
		dw offset loc_16FA7
		dw offset loc_16F89
		dw offset loc_16F6B
		dw offset loc_16F4D
		dw offset loc_16F2F
		dw offset loc_16F11
		dw offset loc_16EF3
		dw offset loc_16ED5
		dw offset loc_16EB7
		dw offset loc_16E99
		dw offset loc_16E7B
		dw offset loc_16E5D
		dw offset loc_16E3F
off_18EE0	dw offset loc_1736F	; DATA XREF: sub_1725F+1Br
		dw offset loc_1735F
		dw offset loc_1734F
		dw offset loc_1733F
		dw offset loc_1732F
		dw offset loc_1731F
		dw offset loc_1730F
		dw offset loc_172FF
		dw offset loc_172EF
		dw offset loc_172DF
		dw offset loc_172CF
		dw offset loc_172BF
		dw offset loc_172AF
		dw offset loc_1729F
		dw offset loc_1728F
		dw offset loc_1727F
off_18F00	dw offset loc_1761E	; DATA XREF: sub_1725F+1F8r
		dw offset loc_17600
		dw offset loc_175E2
		dw offset loc_175C4
		dw offset loc_175A6
		dw offset loc_17588
		dw offset loc_1756A
		dw offset loc_1754C
		dw offset loc_1752E
		dw offset loc_17510
		dw offset loc_174F2
		dw offset loc_174D4
		dw offset loc_174B6
		dw offset loc_17498
		dw offset loc_1747A
		dw offset loc_1745C
off_18F20	dw offset loc_17956	; DATA XREF: sub_17824+10r
		dw offset loc_17943
		dw offset loc_17930
		dw offset loc_1791D
		dw offset loc_1790A
		dw offset loc_178F7
		dw offset loc_178E4
		dw offset loc_178D1
		dw offset loc_178BE
		dw offset loc_178AB
		dw offset loc_17898
		dw offset loc_17885
		dw offset loc_17872
		dw offset loc_1785F
		dw offset loc_1784C
		dw offset loc_17839
off_18F40	dw offset loc_17C25	; DATA XREF: sub_17824+249r
		dw offset loc_17C08
		dw offset loc_17BEB
		dw offset loc_17BCE
		dw offset loc_17BB1
		dw offset loc_17B94
		dw offset loc_17B77
		dw offset loc_17B5A
		dw offset loc_17B3D
		dw offset loc_17B20
		dw offset loc_17B03
		dw offset loc_17AE6
		dw offset loc_17AC9
		dw offset loc_17AAC
		dw offset loc_17A8F
		dw offset loc_17A72
_effoff_18F60	dw offset _eff_nullsub	; DATA XREF: sub_137D5+16r
					; sub_137D5+2Br
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_13A43
		dw offset _eff_13A94
		dw offset _eff_nullsub
		dw offset _eff_13B06
		dw offset _eff_13B78
		dw offset _eff_13B88
		dw offset _eff_13BA3
		dw offset _eff_13CDD
		dw offset _eff_13CE8
		dw offset _eff_13DE5
		dw offset _eff_13DEF
		dw offset _eff_nullsub
		dw offset _eff_13E2D
		dw offset _eff_13E32
		dw offset _eff_13E7F
		dw offset _eff_13E84
		dw offset _eff_13E8C
		dw offset _eff_nullsub
		dw offset _nullsub_2
		dw offset _eff_13F05
		dw offset _eff_13F3B
		dw offset _eff_nullsub
		dw offset _eff_14020
		dw offset _eff_14030
		dw offset _eff_14067
_effoff_18FA2	dw offset _eff_nullsub	; DATA XREF: sub_13623+196r
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_13A43
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_13B06
		dw offset _eff_nullsub
		dw offset _eff_13B88
		dw offset _eff_13BA3
		dw offset _eff_13CDD
		dw offset _eff_13CE8
		dw offset _eff_13DE5
		dw offset _eff_13DEF
		dw offset _eff_nullsub
		dw offset _eff_13E2D
		dw offset _eff_13E32
		dw offset _eff_13E7F
		dw offset _eff_13E84
		dw offset _eff_13E8C
		dw offset _eff_nullsub
		dw offset _nullsub_2
		dw offset _eff_13F05
		dw offset _eff_13F3B
		dw offset _eff_nullsub
		dw offset _eff_14020
		dw offset _eff_14030
		dw offset _eff_14067
_effoff_18FE4	dw offset _eff_nullsub	; DATA XREF: sub_13813+Er
		dw offset _eff_13886
		dw offset _eff_138A4
		dw offset _eff_138D2
		dw offset _eff_1392F
		dw offset _eff_139AC
		dw offset _eff_139B2
		dw offset _eff_139B9
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_13AD7
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_13BA3
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_13DE5
		dw offset _eff_13DEF
		dw offset _eff_13E1E
		dw offset _eff_13E2D
		dw offset _eff_13E32
		dw offset _eff_13E7F
		dw offset _eff_13E84
		dw offset _eff_nullsub
		dw offset _eff_138D2
		dw offset _nullsub_2
		dw offset _eff_13F05
		dw offset _eff_13F3B
		dw offset _eff_13FBE
		dw offset _eff_nullsub
		dw offset _eff_nullsub
		dw offset _eff_nullsub
_effoff_19026	dw offset _eff_nullsub	; DATA XREF: _eff_13BA3+Ar
		dw offset _eff_1387F
		dw offset _eff_1389D
		dw offset _eff_13BB2
		dw offset _eff_13BC0
		dw offset _eff_13BC8
		dw offset _eff_13C02
		dw offset _eff_13C34
		dw offset _eff_13C3F
		dw offset _eff_13C64
		dw offset _eff_13C88
		dw offset _eff_13C95
		dw offset _eff_13CA2
		dw offset _eff_13CB3
		dw offset _eff_13CC9
		dw offset _eff_nullsub
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
ends		seg000

; ---------------------------------------------------------------------------
; ===========================================================================


; ===========================================================================

; Segment type:	Regular
segment		seg003 byte public 'UNK' use16
		assume cs:seg003
		assume es:nothing, ss:nothing, ds:dseg,	fs:nothing, gs:nothing
_a070295122642	db '07/02/95 12:26:42',0 ; DATA XREF: seg003:off_2462Eo
					; seg003:off_24656o
_pointer_245B4	dd 0			; DATA XREF: sub_135CA+1Cr
					; sub_135CA:loc_135FDw	...
_dma_buf_pointer	dd 0			; DATA XREF: _mod_readfile_11F4E+9Cw
					; _mod_readfile_11F4E+144r ...
_dword_245BC	dd 0			; DATA XREF: _someplaymode+59w
					; sub_13177+1Dr ...
_dword_245C0	dd 0			; DATA XREF: _someplaymode:loc_12C3Cw
					; sub_13177+31r ...
_dword_245C4	dd 0			; DATA XREF: _mod_n_t_module:loc_101F4r
					; _mod_1024A+33w ...
off_245C8	dw offset _moduleread	; DATA XREF: sub_12DA8+3Ew
					; sub_13623:loc_13791r	...
off_245CA	dw offset _moduleread	; DATA XREF: sub_12DA8+38w
					; sub_135CA+4Dr ...
off_245CC	dw offset _moduleread	; DATA XREF: _change_volume+1Ar
					; sub_12DA8+44w ...
off_245CE	dw offset _moduleread	; DATA XREF: _volume_12A66+Fr
					; sub_12DA8+4Aw ...
_savesp_245D0	dw 0			; DATA XREF: _moduleread+15w
					; _moduleread+B6r ...
_word_245D2	dw 0			; DATA XREF: _mod_n_t_module+9w
					; _mod_n_t_module+43w ...
_word_245D4	dw 0			; DATA XREF: _moduleread+81r
					; _moduleread+87r ...
_word_245D6	dw 0			; DATA XREF: _clean_11C43+4Aw
					; sub_12B83+52w ...
_word_245D8	dw 0			; DATA XREF: _clean_11C43+50w
					; sub_12B83+57w
_word_245DA	dw 0			; DATA XREF: _clean_11C43+56w
					; sub_12B83+5Cw
_word_245DC	dw 0			; DATA XREF: sub_13623+12Dw
					; sub_13623+29Cr ...
_freq_245DE	dw 0			; DATA XREF: _mod_1024A+40r
					; __2stm_module+26w ...
off_245E0	dw offset _chrin		; DATA XREF: sub_12DA8+E9w
					; sub_16C69+57Fr
off_245E2	dw offset _myin		; DATA XREF: sub_12DA8+EFw
					; sub_16C69:loc_17202r
_word_245E4	dw 0			; DATA XREF: _configure_timer+18r
					; sub_13CF6+4Dw ...
_word_245E8	dw 0			; DATA XREF: sub_12DA8+5Aw
					; sub_12DA8+F9w ...
_word_245EA	dw 0			; DATA XREF: sub_13CF6:loc_13D36w
					; sub_16C69+13r
_word_245EC	dw 0			; DATA XREF: sub_13CF6+44w
					; sub_16C69+19r
_word_245EE	dw 0			; DATA XREF: sub_13CF6+47w
					; sub_16C69+Aw	...
_word_245F0	dw 0			; DATA XREF: _clean_11C43+21w
					; sub_1265D+46r ...
_word_245F2	dw 0			; DATA XREF: _mod_n_t_module+12Dr
					; _mod_102F5+17w ...
_my_seg_index	dw 0			; DATA XREF: _psm_module+136r
					; _mem_reallocxr ...
_word_245F6	dw 0			; DATA XREF: _clean_11C43+27w
					; sub_1265D+42r ...
_word_245F8	dw 0			; DATA XREF: _mod_1021E:loc_10230w
					; _far_module+9Aw ...
_word_245FA	dw 0			; DATA XREF: _mod_1021E+8w
					; __2stm_module:loc_104F2w ...
_volume_245FC	dw 100h			; DATA XREF: sub_1265D+5r
					; _change_volume+Bw ...
_amplification	dw 100			; DATA XREF: _clean_11C43+83w
					; _volume_prepare_waves+72r ...
_word_24600	dw 0			; DATA XREF: sub_12EBA+2Cw
					; sub_13017+1Bw ...
_word_24602	dw 0			; DATA XREF: sub_12EBA+32w
					; _proaud_14700:loc_14E10w ...
_interrupt_mask	dw 0			; DATA XREF: _setsnd_handler+Cw
					; _restore_intvector+3r
_old_intprocoffset dw 0			; DATA XREF: _setsnd_handler+3Aw
					; _restore_intvector+14r
_old_intprocseg	dw 0			; DATA XREF: _setsnd_handler+3Ew
					; _restore_intvector+1Ar
_intvectoffset	dw 0			; DATA XREF: _setsnd_handler+2Dw
					; _restore_intvector+Cr
_word_2460C	dw 0			; DATA XREF: _deinit_125B9+12r
					; sub_12D35+1Fr ...
_word_2460E	dw 0			; DATA XREF: _gravis_int+D5w
					; _proaud_set+8w ...
_word_24610	dw 0			; DATA XREF: _volume_prep+6w
					; sub_1279A+4r	...
_my_size		dw 0			; DATA XREF: _volume_prep+9w
					; sub_1279A+Dr	...
_word_24614	dw 0			; DATA XREF: sub_154F4+3Ew
					; sub_1609F-909r ...
_byte_24616	db 0			; DATA XREF: sub_154F4+41w
					; sub_154F4+52w ...
_byte_24617	db 0			; DATA XREF: _ems_realloc2w
					; _mod_readfile_11F4Ew ...
_byte_24618	db 0			; DATA XREF: sub_13D95-6w sub_13D95w ...
_byte_24619	db 0			; DATA XREF: sub_13D95+16w
					; _gravis_int+7Cw ...
_byte_2461A	db 0			; DATA XREF: _s3m_module+1Fw
					; _useless_writeinr+44r	...
_byte_2461B	db 0			; DATA XREF: _moduleread:loc_10028w
					; _moduleread:loc_1007Br ...
_byte_2461C	db 0			; DATA XREF: sub_12B18+14w
					; sub_12B18:loc_12B71w
_byte_2461D	db 0			; DATA XREF: sub_12B18+19w
					; sub_12B18+51w
_byte_2461E	db 0			; DATA XREF: _s3m_module:loc_10652r
					; _e669_module+3Cr ...
_byte_2461F	db 0			; DATA XREF: _s3m_module+C5r
					; _e669_module+38r ...
_byte_24620	db 0			; DATA XREF: sub_12EBA+38w
					; _proaud_14700+71Cw ...
_byte_24621	db 0			; DATA XREF: sub_12EBA+3Dw
					; _proaud_14700+73Bw ...
_sndflags_24622	db 0			; DATA XREF: _useless_11787+9r
					; _inr_read_118B0+AEr ...
_byte_24623	db 0			; DATA XREF: sub_1265D+33r
					; sub_12DA8+50w ...
_bit_mode	db 8			; DATA XREF: sub_12DA8+55w
					; sub_12DA8+E2r ...
_byte_24625	db 0			; DATA XREF: _clean_11C43+89w
					; _change_amplif+Ew ...
_gravis_port	dw 0			; DATA XREF: _volume_prep+61r
					; _gravis_13215+49r ...
_byte_24628	db 0			; DATA XREF: _mod_readfile_11F4E+1BFr
					; sub_1265D+27r ...
_byte_24629	db 20h			; DATA XREF: _someplaymode+64r
					; _gravis_18079:loc_18088w ...
_irq_number_0	db 0			; DATA XREF: _gravis_init+35w
					; _gravis_init+59w ...
_byte_2462B	db 0			; DATA XREF: _gravis_init+38w
					; _gravis_init+61w ...
_dma_channel_0	db 0			; DATA XREF: _mod_readfile_11F4E+8Er
					; _volume_prep+43r ...
_byte_2462D	db 0			; DATA XREF: _gravis_init+41w
					; _gravis_init+6Dw ...
off_2462E	dw offset _a070295122642	; DATA XREF: sub_13044+1Bw
					; sub_13044+2Ew ...
					; "07/02/95 12:26:42"
_word_24630	dw 0			; DATA XREF: _clean_11C43+32w
					; _mod_readfile_11F4E+EDr ...
_word_24632	dw 0			; DATA XREF: _gravis_int+DEr
					; _nongravis_182E7+4Dw
_word_24634	dw 0			; DATA XREF: _gravis_int+D8r
					; _nongravis_182E7+45w
_word_24636	dw 0			; DATA XREF: _gravis_int+B5r
					; _gravis_int+D1w ...
_freq2		dw 0			; DATA XREF: _read_sndsettings+2Cr
					; _gravis_18079+1Dw
		db    0
_byte_2463B	db 0			; DATA XREF: _gravis_init+Fw
					; _gravis_init+1Bw ...
_dword_2463C	dd 0			; DATA XREF: _someplaymode+8Aw
					; _gravis_13215+2Ar
_dword_24640	dd 0			; DATA XREF: _memfree_125DA+13w
					; _volume_prep+4Dw ...
		db    0
_byte_24645	db 0			; DATA XREF: sub_182DB+5w
					; _nongravis_182E7+Cw ...
_word_24646	dw 0			; DATA XREF: _proaud_init:loc_145A6w
_sound_port	dw 0			; DATA XREF: _proaud_init+42w
					; _proaud_init+90r ...
_byte_2464A	db 0			; DATA XREF: _proaud_init+6Aw
					; _proaud_init+9Br ...
_byte_2464B	db 0			; DATA XREF: _proaud_init+64w
					; _proaud_set+11r ...
_base_port2	dw 0			; DATA XREF: _wss_init:loc_147C3w
					; _wss_init+75r	...
_dma_channel2	db 0			; DATA XREF: _wss_init:loc_147DCw
					; _wss_init:loc_14801r ...
_irq_number2	db 0			; DATA XREF: _wss_init:loc_147D0w
					; _wss_init+41r	...
_byte_24650	db 0			; DATA XREF: _wss_set+54w _wss_sndoff+4r
_byte_24651	db 0			; DATA XREF: _wss_set+61w _wss_sndoff+Cr
_sb_base_port	dw 0			; DATA XREF: _sb16_on+17r _sb16_on+44r ...
_word_24654	dw 0			; DATA XREF: _sb16_detect_port+78w
off_24656	dw offset _a070295122642	; DATA XREF: sub_13044+21w
					; sub_13044+34w ...
					; "07/02/95 12:26:42"
_dma_chn_mask	db 0			; DATA XREF: _sb16_init+4Bw
					; _sb16_init:loc_14AF5w	...
_sb_irq_number	db 0			; DATA XREF: _sb16_init+1Cw
					; _sb16_init:loc_14AB3w	...
_sb_timeconst	db 0			; DATA XREF: _sbpro_init+51w _sb_set-D1r ...
_word_2465C	dw 0			; DATA XREF: _snd_initialze:loc_15302w
					; _midi_153F1r ...
_freq1		dw 22050		; DATA XREF: _volume_prepare_waves+48r
					; _someplaymode+49r ...
_fhandle_module	dw 0			; DATA XREF: _moduleread+19w
					; _moduleread:loc_1006Br ...
_word_24662	dw 0			; DATA XREF: _moduleread:loc_1002Dw
					; _moduleread+73w ...
_byte_24664	db 0			; DATA XREF: _sb_set-FFw
					; _sbpro_sndoff+1Dr
_byte_24665	db 0			; DATA XREF: _moduleread:loc_10064w
					; _memfree_125DA:loc_125F6r
_byte_24666	db 0			; DATA XREF: sub_1265D+18r
					; sub_13CF6+2w
_byte_24667	db 0			; DATA XREF: sub_1265D+1Dr
					; _eff_13CE8+4w	...
_byte_24668	db 0			; DATA XREF: sub_12EBA+71w
					; sub_12F56+1Aw ...
_byte_24669	db 0			; DATA XREF: sub_12EBA+9w sub_12F56+Cw ...
_byte_2466A	db 0			; DATA XREF: sub_12EBA+Ew
					; _eff_13B06+5Aw ...
_byte_2466B	db 0			; DATA XREF: sub_12EBA+13w
					; _eff_13C02+25w ...
_byte_2466C	db 0			; DATA XREF: sub_12EBA+18w
					; _eff_13CC9+10w ...
_byte_2466D	db 0			; DATA XREF: sub_12EBA+1Dw
					; _eff_13CC9+7r	...
_byte_2466E	db 0			; DATA XREF: _mod_readfile_11F4E:loc_1212Br
					; _volume_prep:loc_1276Cr ...
_dma_mode	db 0			; DATA XREF: _proaud_set+3w _wss_set+3w	...
_sb_int_counter	db 0			; DATA XREF: _sb_test_interruptw
					; _sb_test_interrupt:loc_184B0r	...
_byte_24671	db 0			; DATA XREF: sub_1265D+3Ar
					; sub_12EBA+22w ...
_flag_playsetttings db 0			; DATA XREF: _clean_11C43+68r
					; _get_playsettings+6r ...
_byte_24673	db 0			; DATA XREF: _s3m_module+14w
					; _s3m_module+2Bw ...
_byte_24674	db 0			; DATA XREF: _mod_readfile_11F4E+32w
					; _mod_readfile_11F4E+BFw ...
_byte_24675	db 0			; DATA XREF: _mod_readfile_11F4E+2Aw
					; _mod_readfile_11F4E+B7w ...
_byte_24676	db 0			; DATA XREF: _mod_sub_12220:loc_12228r
					; _mod_sub_12220+23w
_byte_24677	db 0			; DATA XREF: _midi_15413+4r
					; _midi_15413+Aw
_byte_24678	db 0			; DATA XREF: _midi_15413+2Aw
_byte_24679	db 0			; DATA XREF: __2stm_module+31w
					; _s3m_module+EFw ...
_byte_2467A	db 0			; DATA XREF: __2stm_module+35w
					; _s3m_module+F5w ...
_byte_2467B	db 0			; DATA XREF: _far_module+2Cw
					; sub_12EBA+7Fw ...
_byte_2467C	db 0			; DATA XREF: _far_module+2Fw
					; sub_12EBA+82w ...
_byte_2467D	db 0			; DATA XREF: sub_13044:loc_1305Aw
					; sub_13044:loc_1306Dw	...
_byte_2467E	db 0			; DATA XREF: _s3m_module+Fw
					; _e669_module+1Fw ...
_play_state	db 0			; DATA XREF: _getset_playstate+Bw
					; _getset_playstate:loc_12CA7r ...
_snd_init	db 0			; DATA XREF: sub_12D05+Br
					; _snd_initialzer ...
_snd_set_flag	db 0			; DATA XREF: sub_12DA8+60w _snd_on+7r ...
_byte_24682	db 0			; DATA XREF: sub_16C69:loc_16C88w
					; sub_16C69+3Fr ...
_byte_24683	db 0			; DATA XREF: sub_154F4+6w
					; sub_1609F:loc_15698r	...
_dword_24684	dd 0			; DATA XREF: _alloc_dma_bufw
					; _alloc_dma_buf+22r ...
		db    0
_word_2468C	dw 0			; DATA XREF: _alloc_dma_buf:loc_18A0Aw
					; _alloc_dma_buf+B5r
		align 10h
		db    0
algn_24691:
_dword_24694	dd 0			; DATA XREF: _dma_186E3+5Dr
					; _dma_186E3+A2r ...
_myseg_24698	dw 0			; DATA XREF: _alloc_dma_buf+31w
					; _alloc_dma_buf+A6r ...
_memflg_2469A	db 0			; DATA XREF: _alloc_dma_buf+8w
					; _alloc_dma_buf+B0w ...
_byte_2469B	db 0			; DATA XREF: _alloc_dma_buf+Dw
_byte_2469C	db 0			; DATA XREF: _alloc_dma_buf+4w
					; _alloc_dma_buf+3Br
		db 0
_ems_pageframe	dw 0			; DATA XREF: _useless_11787+3Er
					; _ems_init+61w	...
_ems_handle	dw 0			; DATA XREF: _ems_init+74w
					; _ems_release+Dr ...
_ems_log_pagenum	dw 0			; DATA XREF: _ems_init+7Dw
					; _ems_release+15w ...
_ems_enabled	db 0			; DATA XREF: _ems_initw	_ems_init+78w ...
_byte_246A5	db 0			; DATA XREF: _ems_save_mapctx+1Bw
					; _ems_restore_mapctx+7r
_word_246A6	dw 0			; DATA XREF: sub_12CAD+9o
					; sub_12CAD+18w
_byte_246A8	db 0			; DATA XREF: sub_12CAD+14w
_word_246A9	dw 0			; DATA XREF: sub_12CAD+10w
_module_type_text dd 20202020h		; DATA XREF: _mod_n_t_modulew
					; _mod_n_t_module:_mod_flt8_modulew ...
; char asc_246B0[32]
asc_246B0	db '                                ' ; DATA XREF: _mod_1021E+22o
					; __2stm_module+47o ...
_moduleflag_246D0 dw 0			; DATA XREF: _mod_n_t_module+3Dw
					; _mod_read_10311+12r ...
_sndcard_type	db 0			; DATA XREF: _mtm_module+2Er
					; _far_module+3Fr ...
_snd_base_port	dw 0			; DATA XREF: _read_sndsettings+9r
					; _useless_12D61+9w ...
_irq_number	db 0			; DATA XREF: _read_sndsettings+Dr
					; _useless_12D61+Cw ...
_dma_channel	db 0			; DATA XREF: _read_sndsettings+11r
					; _useless_12D61+Fw ...
_freq_246D7	db 0			; DATA XREF: _read_sndsettings+15r
					; sub_12DA8+17w ...
_byte_246D8	db 0			; DATA XREF: _read_sndsettings+19r
					; _useless_12D61+12w ...
_byte_246D9	db 0			; DATA XREF: _read_sndsettings+1Dr
					; _useless_12D61+15w ...
_config_word	dw 0			; DATA XREF: _ems_init+8r
					; _read_sndsettings:loc_12CFFr ...
_byte_246DC	db 0			; DATA XREF: sub_12DA8+33w
					; sub_12DA8+88r
_word_246DE	dw 6B00h,6500h,5F40h,5A00h,54C0h,5000h,4B80h,4740h,4340h
					; DATA XREF: sub_13826+42o
					; sub_13826:loc_1386Cr
		dw 3F80h,3C00h,38A0h
_table_246F6	dw 8363,8422,8482,8543,8604,8667,8730,8794,7901,7954,8007
					; DATA XREF: _eff_13BC8+21r
		dw 8062,8116,8191,8231,8305
_table_24716	dw 8000h,9000h,0A000h,0A952h,0B000h,0B521h,0B952h,0BCDEh
					; DATA XREF: sub_13044+41o
		dw 0C000h,0C2B5h,0C521h,0C752h,0C952h,0CB29h,0CCDEh,0CE74h
		dw 0D000h,0D164h,0D2B5h,0D3F3h,0D521h,0D640h,0D752h,0D858h
		dw 0D952h,0DA42h,0DB29h,0DC07h,0DCDEh,0DDACh,0DE74h,0DF35h
		dw 0E000h,0E0B5h,0E164h,0E20Fh,0E2B5h,0E356h,0E3F3h,0E48Ch
		dw 0E521h,0E5B2h,0E640h,0E6CBh,0E752h,0E7D6h,0E858h,0E8D6h
		dw 0E952h,0E9CCh,0EA42h,0EAB7h,0EB29h,0EB99h,0EC07h,0EC73h
		dw 0ECDEh,0ED46h,0EDACh,0EE11h,0EE74h,0EED5h,0EF35h,0EF93h
		dw 0EFF0h
_table_24798	dw 8000h,9800h,0A000h,0A800h,0B000h,0B400h,0B800h,0BC00h
					; DATA XREF: sub_13044+1Bo
		dw 0C000h,0C200h,0C400h,0C600h,0C800h,0CA00h,0CC00h,0CE00h
		dw 0D000h,0D100h,0D200h,0D300h,0D400h,0D500h,0D600h,0D700h
		dw 0D800h,0D900h,0DA00h,0DB00h,0DC00h,0DD00h,0DE00h,0DF00h
		dw 0E080h,0E100h,0E180h,0E200h,0E280h,0E300h,0E380h,0E400h
		dw 0E480h,0E500h,0E580h,0E600h,0E680h,0E700h,0E780h,0E800h
		dw 0E880h,0E900h,0E980h,0EA00h,0EA80h,0EB00h,0EB80h,0EC00h
		dw 0EC80h,0ED00h,0ED80h,0EE00h,0EE80h,0EF00h,0EF80h,0EFF0h
_table_24818	dw 8000h,9800h,0A000h,0A800h,0B000h,0B400h,0B800h,0BC00h
					; DATA XREF: sub_13044+2Eo
		dw 0C000h,0C200h,0C400h,0C600h,0C800h,0CA00h,0CC00h,0CE00h
		dw 0D000h,0D100h,0D200h,0D300h,0D400h,0D500h,0D600h,0D700h
		dw 0D800h,0D900h,0DA00h,0DB00h,0DC00h,0DD00h,0DE00h,0DF00h
		dw 0E080h,0E100h,0E180h,0E200h,0E280h,0E300h,0E380h,0E400h
		dw 0E480h,0E500h,0E580h,0E600h,0E680h,0E700h,0E780h,0E800h
		dw 0E880h,0E900h,0E980h,0EA00h,0EA80h,0EB00h,0EB80h,0EC00h
		dw 0EC80h,0ED00h,0ED80h,0EE00h,0EE80h,0EF00h,0EF80h,0EFF0h
_table_24898	db 1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh,1Eh
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
_word_24998	dw 6B00h,6500h,5F40h,5A00h,54C0h,5000h,4B80h,4740h,4340h
					; DATA XREF: sub_13623+D2o
					; _eff_13BC8+18o
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
_table_25118	dw 1712,1616,1524,1440,1356,1280,1208,1140,1076,1016,960,906,856,808,762,720,678,640,604,570,538,508,480,453
					; DATA XREF: _mod_read_10311:loc_10399r
		dw 428,404,381,360,339,320,302,285,269,254,240,226,214,202,190,180,170,160,151,143,135,127,120,113
		dw 107,101,95,90,85,80,75,71,67,63,60,56,53,50,47,45,42,40,37,35,33,31,30,28
		dw 26,25,23,22,21,20,18,17,16,15,15,14
_table_251C0	db  0,18h,31h,4Ah,61h,78h,8Dh,0A1h,0B4h,0C5h,0D4h,0E0h
					; DATA XREF: _eff_1392F+4Er
					; _eff_139B9+4Fr
		db 0EBh,0F4h,0FAh,0FDh,0FFh,0FDh,0FAh,0F4h,0EBh,0E0h,0D4h
		db 0C5h,0B4h,0A1h,8Dh,78h,61h,4Ah,31h,18h
_table_251E0	db  0,15h,20h,29h,30h,37h,3Dh,44h,49h,4Fh,54h,59h,5Eh
					; DATA XREF: sub_13044+47o
		db 62h,67h,6Bh,6Fh,73h,77h,7Ch,7Fh,83h,86h,8Ah,8Eh,91h
		db 95h,98h,9Bh,9Fh,0A2h,0A5h,0A9h,0ABh,0AFh,0B3h,0B5h
		db 0B8h,0BBh,0BEh,0C1h,0C3h,0C6h,0C9h,0CCh,0CFh,0D1h,0D4h
		db 0D7h,0DAh,0DDh,0DFh,0E2h,0E5h,0E7h,0EAh,0ECh,0EFh,0F1h
		db 0F4h,0F6h,0F9h,0FBh,0FEh,0FFh
_table_25221	db  0, 4, 8,0Ch,10h,14h,18h,1Ch,20h,24h,28h,2Ch,30h,34h
					; DATA XREF: sub_13044+21o
		db 38h,3Ch,40h,44h,48h,4Ch,50h,55h,59h,5Dh,61h,65h,69h
		db 6Dh,71h,75h,79h,7Dh,81h,85h,89h,8Dh,91h,95h,99h,9Dh
		db 0A1h,0A5h,0AAh,0AEh,0B2h,0B6h,0BAh,0BEh,0C2h,0C6h,0CAh
		db 0CEh,0D2h,0D6h,0DAh,0DEh,0E2h,0E6h,0EAh,0EEh,0F2h,0F6h
		db 0FAh,0FFh
_table_25261	db  0, 4, 8,0Ch,10h,14h,18h,1Ch,20h,24h,28h,2Ch,30h,34h
					; DATA XREF: sub_13044+34o
		db 38h,3Ch,40h,44h,48h,4Ch,50h,54h,58h,5Ch,60h,64h,68h
		db 6Ch,70h,74h,78h,7Ch,80h,84h,88h,8Ch,90h,94h,98h,9Ch
		db 0A0h,0A4h,0A8h,0ACh,0B0h,0B4h,0B8h,0BCh,0C0h,0C4h,0C8h
		db 0CCh,0D0h,0D4h,0D8h,0DCh,0E0h,0E4h,0E8h,0ECh,0F0h,0F4h
		db 0F8h,0FFh, 0
		dw offset _sb16_init
		dw offset _covox_init
		dw offset _stereo_init
		dw offset _adlib_init
		dw offset _pcspeaker_init
		dw offset _midi_init
		dw offset _sb16_on
		dw offset _covox_on
		dw offset _stereo_set
		dw offset _adlib_set
		dw offset _pcspeaker_set
		dw offset _midi_set
		dw offset _sb16_off
		dw offset _covox_off
		dw offset _stereo_sndoff
		dw offset _adlib_sndoff
		dw offset _pcspeaker_sndoff
		dw offset _midi_sndoff
		dw offset _sb16_deinit
		dw offset _covox_deinit
		dw offset _stereo_clean
		dw offset _adlib_clean
		dw offset _pcspeaker_clean
		dw offset _midi_clean
_snd_cards_offs	dw offset _aGravisUltrasoun ; DATA XREF:	seg003:114Eo
					; seg003:1194o	...
					; "Gravis UltraSound"
		dw offset _aProAudioSpectrum ; "Pro Audio Spectrum 16"
		dw offset _aWindowsSoundSyst ; "Windows Sound System"
		dw offset _aSoundBlaster1616 ; "Sound Blaster 16/16ASP"
		dw offset _aSoundBlasterPro ; "Sound Blaster Pro"
		dw offset _aSoundBlaster_0 ; "Sound Blaster"
		dw offset _aCovox_0	; "Covox"
		dw offset _aStereoOn1_0	; "Stereo-On-1"
		dw offset _aAdlibSoundcard_0 ; "Adlib SoundCard"
		dw offset _aPcHonker_0	; "PC Honker"
		dw offset _aGeneralMidi_0 ; "General MIDI"
		dw offset _sb16_txt
		dw offset _sb16_txt
		dw offset _sb16_txt
		dw offset _sb16_txt
		dw offset _sb16_txt
		dw offset _covox_txt
		dw offset _covox_txt
		dw offset _pcspeaker_text
		dw offset _pcspeaker_text
		dw offset _midi_txt
off_25326	dw offset _inr_module	; DATA XREF: _moduleread:loc_10040o
					; INR
		db    0
		db    0
		db 16
_aInertiaModule_1 db 'Inertia Module: '
		dw offset _mod_mk_module
		db  38h	; 8
		db    4
		db    4
_aM_k_		db 'M.K.'
		dw offset _mod_mk_module
		db  38h	; 8
		db    4
		db    4
_a_m_k		db '.M.K'
		dw offset _mod_mk_module
		db  38h	; 8
		db    4
		db    4
_aMK		db 'M&K!'
		dw offset _mod_mk_module
		db  38h	; 8
		db    4
		db    4
_aMK_0		db 'M!K!'
		dw offset _mod_mk_module
		db  38h	; 8
		db    4
		db    4
_aGsft		db 'GSFT'
		dw offset _mod_mk_module
		db  38h	; 8
		db    4
		db    4
_aE_g_		db 'E.G.'
		dw offset _mod_mk_module
		db  38h	; 8
		db    4
		db    4
_aFlt4		db 'FLT4'
		dw offset _mod_flt8_module ; FLT8
		db  38h	; 8
		db    4
		db    4
_aFlt8		db 'FLT8'
		dw offset _mod_cd81_module
		db  38h	; 8
		db    4
		db    4
_aCd81		db 'CD81'
		dw offset _mod_cd81_module
		db  38h	; 8
		db    4
		db    4
_aOcta		db 'OCTA'
		dw offset _mod_chn_module
		db  39h	; 9
		db    4
		db    3
_aChn		db 'CHN'
		dw offset _mod_ch_module
		db  3Ah	; :
		db 4
		db    2
_aCh		db 'CH'
		dw offset _mod_tdz_module
		db  38h	; 8
		db    4
		db    3
_aTdz		db 'TDZ'
		dw offset _stm_module	; STM
		db  14h
		db    0
		db    8
_aScream		db '!Scream!'
		dw offset __2stm_module	; 2STM
		db  14h
		db    0
		db    8
_aBmod2stm	db 'BMOD2STM'
		dw offset _s3m_module	; S3M
		db  2Ch	; ,
		db    0
		db    4
_aScrm		db 'SCRM'
		dw offset _mtm_module	; MTM
		db    0
		db    0
		db    3
_aMtm		db 'MTM'
		dw offset _psm_module	; PSM
		db    0
		db    0
		db    4
_aPsm		db 'PSM˛'
		dw offset _far_module	; FAR
		db    0
		db    0
		db    4
_aFar		db 'FAR˛'
		dw offset _ult_module	; ULT
		db    0
		db    0
		db  0Ch
_aMas_utrack_v	db 'MAS_UTrack_V'
		dw offset __669_module	; 669
		db    0
		db    0
		db    2
_aIf		db 'if'
		dw offset _e669_module	; E669
		db    0
		db    0
		db    2
_aJn		db 'JN'
_eModuleNotFound	db 'Module not found',0Dh,0Ah,0 ; DATA XREF: _moduleread+1Co
_aNotEnoughMemory db 'Not enough Memory available',0Dh,0Ah,0
					; DATA XREF: _moduleread:loc_10099o
_aNotEnoughDramOn db 'Not enough DRAM on UltraSound',0Dh,0Ah,0
					; DATA XREF: _mod_readfile_11F4E+1CCo
_aSomeFunctionsOf db 'Some functions of the UltraSound do not work!',0Dh,0Ah
		db 0Ah
		db 'Probably the AT-BUS Clock Speed is too high.',0Dh,0Ah
		db 'Try changing the AT-BUS Clock in the CMOS Setup.',0Dh,0Ah,0
_aCouldNotFindThe db 'Could not find the ULTRASND environment string',0Dh,0Ah,0
					; DATA XREF: _gravis_init:loc_1432Fo
_aCouldNotFindT_0 db 'Could not find the Gravis UltraSound at the specified port addres'
		db 's',0Dh,0Ah,0
_aThisProgramRequ db 'This program requires the soundcards device driver.',0Dh,0Ah,0
_aErrorSoundcardN db 'Error: Soundcard not found!',0Dh,0Ah,0
					; DATA XREF: _proaud_init:loc_1464Fo
					; _wss_test:loc_149ACo ...
_aErrorCouldNotFi db 'Error: Could not find IRQ/DMA!',0Dh,0Ah,0
_aErrorCouldNot_0 db 'Error: Could not find IRQ!',0Dh,0Ah,0 ; DATA XREF: _sb_detect_irq+4Co
_aErrorCouldNot_1 db 'Error: Could not find DMA!',0Dh,0Ah,0 ; DATA XREF: _sb_detect_irq+D6o
_aDeviceNotIniti	db 'Device not initialised!',0 ; DATA XREF: sub_12D05+8o
_aAt		db ' at',0              ; DATA XREF: seg003:10BFo seg003:1152o ...
_aBasePort	db ' base port ',0      ; DATA XREF: seg003:10C3o seg003:1156o ...
_aMixedAt	db ', mixed at ',0      ; DATA XREF: seg003:1173o seg003:11A5o ...
_aKhz		db 'kHz',0              ; DATA XREF: seg003:117Bo seg003:11ADo ...
_aGravisUltrasoun db 'Gravis UltraSound',0 ; DATA XREF: seg003:_snd_cards_offso
					; seg003:10BBo
_gravis_txt	db    1			; DATA XREF: seg003:_sndcards_text_tblo
		db    0
		dw offset _aGravisUltrasoun ; "Gravis UltraSound"
		db    1
		db    0
		dw offset _aAt		; " at"
		db    1
		db    0
		dw offset _aBasePort	; " base port "
		db  0Bh
		db    0
		dw offset _snd_base_port
_aHGf1Irq	db 'h, GF1-IRQ '
		db    4
		db    0
		dw offset _irq_number
_aDramDma	db ', DRAM-DMA '
		db    4
		db    0
		dw offset _dma_channel
		db    0
_aProAudioSpectrum db 'Pro Audio Spectrum 16',0 ; DATA XREF: seg003:0D5Co
_aWindowsSoundSyst db 'Windows Sound System',0 ; DATA XREF: seg003:0D5Eo
_aSoundBlaster1616 db 'Sound Blaster 16/16ASP',0 ; DATA XREF: seg003:0D60o
_aSoundBlasterPro db 'Sound Blaster Pro',0 ; DATA XREF: seg003:0D62o
_aSoundBlaster_0	db 'Sound Blaster',0    ; DATA XREF: seg003:0D64o
_sb16_txt	db    2			; DATA XREF: seg003:0D72o seg003:0D74o ...
		db    0
		dw offset _sndcard_type
		dw offset _snd_cards_offs
		db    1
		db    0
		dw offset _aAt		; " at"
		db    1
		db    0
		dw offset _aBasePort	; " base port "
		db 0Bh
		db    0
		dw offset _snd_base_port
_aHIrq		db 'h, IRQ '
		db    4
		db    0
		dw offset _irq_number
_aDma		db ', DMA '
		db    4
		db    0
		dw offset _dma_channel
		db    1
		db    0
		dw offset _aMixedAt	; ", mixed at "
		db    4
		db    0
		dw offset _freq_246D7
		db    1
		db    0
		dw offset _aKhz		; "kHz"
		db    0
_aCovox_0	db 'Covox',0            ; DATA XREF: seg003:0D66o
_aStereoOn1_0	db 'Stereo-On-1',0      ; DATA XREF: seg003:0D68o
_covox_txt	db    2			; DATA XREF: seg003:0D7Co seg003:0D7Eo
		db    0
		dw offset _sndcard_type
		dw offset _snd_cards_offs
		db    1
		db    0
		dw offset _aAt		; " at"
		db    1
		db    0
		dw offset _aBasePort	; " base port "
		db  0Bh
		db    0
		dw offset _snd_base_port
		db 'h'
		db    1
		db    0
		dw offset _aMixedAt	; ", mixed at "
		db    4
		db    0
		dw offset _freq_246D7
		db    1
		db    0
		dw offset _aKhz		; "kHz"
		db    0
_aAdlibSoundcard_0 db 'Adlib SoundCard',0 ; DATA XREF: seg003:0D6Ao
_aPcHonker_0	db 'PC Honker',0        ; DATA XREF: seg003:0D6Co
_pcspeaker_text	db    2			; DATA XREF: seg003:0D80o seg003:0D82o
		db    0
		dw offset _sndcard_type
		dw offset _snd_cards_offs
		db    1
		db    0
		dw offset _aMixedAt	; ", mixed at "
		db    4
		db    0
		dw offset _freq_246D7
		db    1
		db    0
		dw offset _aKhz		; "kHz"
		db    0
_aGeneralMidi_0	db 'General MIDI',0     ; DATA XREF: seg003:0D6Eo
_midi_txt	db    2			; DATA XREF: seg003:0D84o
		db    0
		dw offset _sndcard_type
		dw offset _snd_cards_offs
		db    1
		db    0
		dw offset _aAt		; " at"
		db    1
		db    0
		dw offset _aBasePort	; " base port "
		db  0Bh
		db    0
		dw offset _snd_base_port
		db 'h'
		db    0
		db    0
		db    0
_dword_257A0	dd 0			; DATA XREF: _useless_writeinr+170w
					; _inr_read_118B0+82w ...
_word_257A4	dw 0			; DATA XREF: _useless_writeinr+106w
					; _useless_writeinr+111r ...
_aInertiaModule	db 'Inertia Module: ',0 ; DATA XREF: _useless_writeinr+29o
					; _useless_writeinr+80o	...
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
_byte_257DA	db 10h			; DATA XREF: _useless_writeinr+3Fw
_byte_257DB	db 0			; DATA XREF: _useless_writeinr+47w
					; _inr_module+3Er
_byte_257DC	db 0			; DATA XREF: _useless_writeinr+4Dw
					; _inr_module+44r
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
_word_257E6	dw 4			; DATA XREF: _useless_writeinr+53w
					; _inr_module+4Ar
_word_257E8	dw 0			; DATA XREF: _useless_writeinr+59w
_word_257EA	dw 0			; DATA XREF: _useless_writeinr+5Fw
_word_257EC	dw 0			; DATA XREF: _useless_writeinr+65w
					; _inr_module+54r
_word_257EE	dw 0			; DATA XREF: _useless_writeinr+6Bw
					; _inr_module+5Ar
_word_257F0	dw 0			; DATA XREF: _useless_writeinr+71w
					; _inr_module+60r
_byte_257F2	db 0			; DATA XREF: _useless_writeinr+77w
					; _inr_module+66r
_byte_257F3	db 0			; DATA XREF: _useless_writeinr+7Dw
					; _inr_module+6Cr
		db    0
		db    0
_aInertiaModule_0 db 'Inertia Module: ',0 ; DATA XREF: _useless_writeinr+23o
		db 1Fh dup(0)
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
_aInertiaSample	db 'Inertia Sample: '   ; DATA XREF: _useless_writeinr_118+11o
					; _useless_writeinr_118+5Fo ...
asc_25856	db '                                ',0Dh,0Ah,1Ah
					; DATA XREF: _useless_writeinr_118+21o
					; _inr_read_118B0+26o
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
_dword_25886	dd 0			; DATA XREF: _useless_writeinr_118+59w
					; _inr_read_118B0+64r
		db  10h
_byte_2588B	db 0			; DATA XREF: _useless_writeinr_118+4Cw
					; _inr_read_118B0+58r
_byte_2588C	db 0			; DATA XREF: _useless_writeinr_118+46w
					; _inr_read_118B0+52r
_byte_2588D	db 0			; DATA XREF: _useless_writeinr_118+52w
					; _inr_read_118B0+5Er
_word_2588E	dw 0			; DATA XREF: _useless_writeinr_118+40w
					; _inr_read_118B0+4Cr
		db    0
		db    0
_dword_25892	dd 0			; DATA XREF: _useless_writeinr_118+31w
					; _inr_read_118B0+32r
_dword_25896	dd 0			; DATA XREF: _useless_writeinr_118+39w
					; _inr_read_118B0+3Br
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
unk_258A6	db  49h	; I		; DATA XREF: _useless_writeinr_118+Eo
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
_volume_25908	db 0A00h dup(0)		; DATA XREF: _s3m_module+89o
					; _clean_11C43+A2o ...
; char _myout[152]
_myout		db 18C0h dup(?)		; DATA XREF: _mod_1024A+3o
					; __2stm_module+53o ...
_dword_27BC8	dd ?			; DATA XREF: _moduleread+8Eo
					; _s3m_module:loc_1065Fw ...
_dword_27BCC	dd ?			; DATA XREF: _e669_module+4Ew
		db 18h dup(?)
_segs_table	dw 100h	dup( ?)		; DATA XREF: _useless_writeinr+13Cr
					; _inr_module+10Dw ...
_myseg_size	dw 100h	dup( ?)		; DATA XREF: _useless_writeinr+117r
					; _inr_module+116w ...
_byte_27FE8	db 0FFh	dup( ?)		; DATA XREF: _mod_n_t_module+55o
					; _mod_1021E+15o ...
_byte_280E7	db ?			; DATA XREF: _s3m_module+1F3w
_byte_280E8	db 100h	dup( ?)		; DATA XREF: _e669_module+80w
					; _e669_module+97r ...
_byte_281E8	db 100h	dup( ?)		; DATA XREF: _e669_module+88w
					; _psm_module+148w ...
_byte_282E8	db 20h dup( ?)		; DATA XREF: _clean_11C43+AEo
					; _clean_11C43+11Co ...
_vlm_byte_table	db 8200h dup( ?)	; DATA XREF: _volume_prepare_waves+8Ao
					; sub_13044:loc_13091o	...
; char _chrin[]
_chrin		dd ?			; DATA XREF: _moduleread:loc_10033o
					; _moduleread:loc_10049o ...
; char _myin[]
_myin		dd ?			; DATA XREF: _mtm_module+22o
					; _psm_module+3Fo ...
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
_word_30515	dw ?			; DATA XREF: _ult_module+1Ar
					; _ult_module+1Fw ...
; char _myin_0
_myin_0		db ?			; DATA XREF: _ult_module+3Ao
_dword_30518	dd ?			; DATA XREF: _ult_module:loc_113F8o
					; _ult_module+200o
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
_word_30520	dw ?			; DATA XREF: _snd_off-3644r
					; _snd_off-3543r
_byte_30522	db ?			; DATA XREF: _mtm_module+58r
_byte_30523	db ?			; DATA XREF: _mtm_module+60r
_word_30524	dw ?			; DATA XREF: _snd_off-3534r
_byte_30526	db ?			; DATA XREF: _mtm_module:loc_10B25r
		db    ?	;
unk_30528	db    ?	;		; DATA XREF: _s3m_module+102r
					; _s3m_module+1D5r ...
_byte_30529	db ?			; DATA XREF: __2stm_module+38r
_word_3052A	dw ?			; DATA XREF: _s3m_module+D0r
					; _s3m_module+225r ...
_word_3052C	dw ?			; DATA XREF: _s3m_module+DEr
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
_word_30532	dw ?			; DATA XREF: _s3m_module+24r
		db    ?	;
		db    ?	;
		db    ?	;
_byte_30537	db ?			; DATA XREF: _ult_module+4Cr
; char _my_in
_my_in		db ?			; DATA XREF: __2stm_module+50o
					; _ult_module+46o ...
; char _byte_30539
_byte_30539	db ?			; DATA XREF: _s3m_module+ECr
					; _ult_module+6Bo ...
_byte_3053A	db ?			; DATA XREF: _s3m_module+F2r
_byte_3053B	db ?			; DATA XREF: _s3m_module+4Ar
					; _s3m_module+53r
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
_byte_30548	db ?			; DATA XREF: _s3m_module:loc_10628r
					; _s3m_module+BEr
		db    ?	;
unk_3054A	db    ?	;		; DATA XREF: _mtm_module+7Bo
_byte_3054B	db ?			; DATA XREF: _psm_module+21r
_byte_3054C	db ?			; DATA XREF: _psm_module+27r
		db    ?	;
		db    ?	;
		db    ?	;
_byte_30550	db ?			; DATA XREF: _psm_module+2Dr
		db    ?	;
_word_30552	dw ?			; DATA XREF: _psm_module+35r
					; _far_module+1Fr
_word_30554	dw ?			; DATA XREF: _psm_module+15r
					; _far_module:loc_10F6Ar
_word_30556	dw ?			; DATA XREF: _psm_module+Fr
		db    ?	;
		db    ?	;
_dword_3055A	dd ?			; DATA XREF: _psm_module+105r
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
_word_30562	dw ?			; DATA XREF: _psm_module+10Cr
_word_30564	dw ?			; DATA XREF: _psm_module+110r
_dword_30566	dd ?			; DATA XREF: _psm_module+55r
					; _s3m_module+FFo ...
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
_byte_30576	db ?			; DATA XREF: _e669_module+2Ar
_byte_30577	db ?			; DATA XREF: _e669_module+32r
		db    ?	;
_byte_30579	db 21h dup( ?)		; DATA XREF: _e669_module:loc_1096Fr
_byte_3059A	db 5Fh dup( ?)		; DATA XREF: _psm_module+4Bo
					; _psm_module+5Co
_byte_305F9	db 40h dup( ?)		; DATA XREF: _e669_module+7Cr
_byte_30639	db ?			; DATA XREF: _ult_module+169r
_byte_3063A	db ?			; DATA XREF: _ult_module+172r
_word_3063B	dw ?			; DATA XREF: _ult_module+192o
					; _ult_module:loc_113E2r ...
_dword_3063D	dd ?			; DATA XREF: _ult_module+225r
					; _ult_read+19w	...
_byte_30641	db 28h dup( ?)		; DATA XREF: _ult_module+22Cr
_byte_30669	db ?			; DATA XREF: _far_module+85r
_byte_3066A	db ?			; DATA XREF: _far_module+95r
_byte_3066B	db 0Eh dup( ?)		; DATA XREF: _far_module+AAo
					; _far_module+D9o
_byte_30679	db 65h dup( ?)		; DATA XREF: _e669_module+84r
_byte_306DE	db 1E0h	dup( ?)		; DATA XREF: _mod_n_t_module+15o
_byte_308BE	db 4Ah dup( ?)		; DATA XREF: _mod_n_t_module+4Fo
					; _mod_n_t_module+F1o
_byte_30908	db 38h dup( ?)		; DATA XREF: _ult_module+203o
					; _ult_module+255o
_byte_30940	db ?			; DATA XREF: _mod_n_t_module:_mod_chn_moduler
					; _mod_n_t_module+9Cr ...
unk_30941	db    ?	;		; DATA XREF: _mod_n_t_module+ACr
		db    ?	;
_byte_30943	db  ?			; DATA XREF: _mod_n_t_module:_mod_tdz_moduler
		db 0BC4h dup(?)
; char _word_31508[]
_word_31508	dw ?			; DATA XREF: _mod_read_10311+5o
					; _mod_read_10311+1Eo ...
_byte_3150A	db ?			; DATA XREF: _psm_module+139r
					; _far_module+130o
		db    ?	;
_byte_3150C	db 7FCh	dup( ?)		; DATA XREF: _psm_module+150o
					; _psm_module+160o
_byte_31D08	db 1800h dup( ?)	; DATA XREF: _mod_read_10311+21o
					; _mod_read_10311+2Bo
_byte_33508	db 1008h dup( ?)	; DATA XREF: _snd_off-3632o
					; _snd_off-3625o ...
ends		seg003

; ===========================================================================

; Segment type:	Uninitialized
segment		seg004 byte stack 'STACK' use16
		assume cs:seg004
		assume es:nothing, ss:nothing, ds:dseg,	fs:nothing, gs:nothing
_byte_34510	db 1000h dup(?)
ends		seg004


		end
