Ideal
; ---------------------------------------------------------------------------

struc		struct_0 ; (sizeof=0xA)
word_244B7	dw ?
anonymous_0	dw ?
anonymous_1	dw ?
anonymous_2	dw ?
anonymous_3	dw ?			; offset (00019050)
ends		struct_0


;               Tasm source
;
; Input	MD5   :	3ADEF234086ACD44430B68CC52471B0D
; Input	CRC32 :	B294245C

; File Name   :	I:\IPLAY.EXE
; Format      :	MS-DOS executable (EXE)
; Base Address:	1000h Range: 10000h-35510h Loaded length: 16308h
; Entry	Point :	1905:42

		p686
		pmmx
		model large

; ===========================================================================

; Segment type:	Pure code
segment		seg000 byte public 'CODE' use16
		assume cs:seg000
		assume es:nothing, ss:nothing, ds:dseg,	fs:nothing, gs:nothing

; =============== S U B	R O U T	I N E =======================================


proc		moduleread far		; CODE XREF: sub_19E11+56P
					; DATA XREF: seg003:off_245C8o	...
		push	ds
		push	dx
		push	cs
		call	near ptr sub_12F48

loc_10006:
		push	cs
		call	near ptr sub_125DA
		pop	dx
		mov	ax, 3D00h
		int	21h		; DOS -	2+ - OPEN DISK FILE WITH HANDLE
					; DS:DX	-> ASCIZ filename
					; AL = access mode
					; 0 - read
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		mov	[savesp_245D0],	sp
		mov	[fhandle_module], ax
		mov	dx, offset eModuleNotFound ; "Module not found\r\n"

loc_1001F:
		mov	ax, 0FFFFh
		jb	short lfreaderr
		call	sub_11E47
		cld

loc_10028:
		mov	[byte_2461B], 0

loc_1002D:
		mov	[word_24662], 0

loc_10033:
		mov	dx, offset chrin
		mov	cx, 1084
		call	dosfread
		push	cs
		call	near ptr sub_11C43
		mov	bx, offset off_25326
		mov	dl, 23

loc_10045:				; CODE XREF: moduleread+5Fj
		movzx	cx, [byte ptr bx+4]

loc_10049:
		mov	di, offset chrin
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

loc_10061:				; N.T.
		mov	ax, offset sub_100BD

loc_10064:				; CODE XREF: moduleread+5Bj
		mov	[byte_24665], 1
		call	ax

loc_1006B:
		mov	bx, [fhandle_module]
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle
		adc	[word_24662], 0
		call	sub_11E68

loc_1007B:
		movzx	ax, [byte_2461B]

loc_10080:
		inc	ax
		cmp	ax, [word_245D4]
		jbe	short loc_1008A
		mov	ax, [word_245D4]

loc_1008A:				; CODE XREF: moduleread+85j
		push	cs
		call	near ptr sub_12B83
		mov	si, offset dword_27BC8
		push	cs

loc_10092:
		call	near ptr sub_12B18
		xor	ax, ax
		pop	ds
		retf
; ---------------------------------------------------------------------------

loc_10099:				; CODE XREF: sub_100BD+6Dj
					; sub_100BD+15Cj ...
		mov	dx, offset aNotEnoughMemory ; "Not enough Memory available\r\n"
		mov	ax, 0FFFEh

lfreaderr:				; CODE XREF: moduleread+22j
					; dosseek+18j ...
		push	ax
		push	dx
		mov	bx, [fhandle_module]
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle
		call	sub_11E68
		push	cs
		call	near ptr sub_125DA
		mov	ax, ds
		mov	fs, ax
		assume fs:seg003
		pop	dx
		pop	ax
		mov	sp, [savesp_245D0]
		pop	ds
		stc
		retf
endp		moduleread


; =============== S U B	R O U T	I N E =======================================

; N.T.

proc		sub_100BD near		; DATA XREF: moduleread:loc_10061o
		mov	[module_type_text], 2E542E4Eh
		mov	[word_245D2], 0Fh
		mov	[word_245D4], 4
		mov	si, offset byte_306DE
		call	sub_1021E
		call	sub_102F5
		mov	dx, 258h
		xor	cx, cx
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		adc	[word_24662], 0
		jmp	loc_101B7
; ---------------------------------------------------------------------------

mod_flt8_module:			; DATA XREF: seg003:0DDAo
		mov	[module_type_text], 38544C46h ;	FLT8
		mov	[moduleflag_246D0], 11b
		mov	[word_245D2], 1Fh
		mov	[word_245D4], 8
		mov	si, offset byte_308BE
		call	sub_1021E
		mov	si, offset byte_27FE8
		mov	cx, 80h	; '€'

loc_10118:				; CODE XREF: sub_100BD+5Fj
		shr	[byte ptr si], 1
		inc	si
		dec	cx
		jnz	short loc_10118
		call	sub_1024A
		call	sub_102F5
		call	sub_10311
		call	near ptr sub_11F4E
		jb	loc_10099
		retn
; ---------------------------------------------------------------------------

mod_tdz_module:				; DATA XREF: seg003:0E04o
		mov	al, [byte_30943]
		jmp	short loc_10137
; ---------------------------------------------------------------------------

mod_chn_module:				; DATA XREF: seg003:0DF5o
		mov	al, [byte_30940]

loc_10137:				; CODE XREF: sub_100BD+75j
		xor	ah, ah
		inc	[word_24662]
		sub	al, 30h	; '0'
		jbe	short locret_10154
		cmp	al, 9
		ja	short locret_10154
		dec	[word_24662]
		mov	[word_245D2], 1Fh
		mov	[word_245D4], ax

loc_10152:
		jmp	short loc_101A6
; ---------------------------------------------------------------------------

locret_10154:				; CODE XREF: sub_100BD+82j
					; sub_100BD+86j ...
		retn
; ---------------------------------------------------------------------------

mod_ch_module:				; DATA XREF: seg003:0DFDo
		inc	[word_24662]
		movzx	ax, [byte_30940]
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
		dec	[word_24662]
		mov	[word_245D2], 1Fh
		mov	[word_245D4], ax
		jmp	short loc_101A6
; ---------------------------------------------------------------------------

mod_cd81_module:			; DATA XREF: seg003:0DE3o seg003:0DECo
		mov	[word_245D2], 1Fh
		mov	[word_245D4], 8
		jmp	short loc_101A6
; ---------------------------------------------------------------------------

mod_mk_module:				; DATA XREF: seg003:0D9Bo seg003:0DA4o ...
		mov	[word_245D2], 1Fh
		mov	[word_245D4], 4

loc_101A6:				; CODE XREF: sub_100BD:loc_10152j
					; sub_100BD+CDj ...
		mov	eax, [dword ptr	byte_30940]
		mov	[module_type_text], eax
		mov	si, offset byte_308BE
		call	sub_1021E
		call	sub_102F5

loc_101B7:				; CODE XREF: sub_100BD+31j
		call	sub_1024A
		cmp	[module_type_text], 2E4B2E4Dh ;	M.K.
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
		movzx	eax, [word_245F2]
		shl	eax, 0Bh

loc_101F4:
		add	eax, [dword_245C4]
		add	eax, 1084
		cmp	eax, edx
		jnz	short loc_10213
		mov	[word_245D4], 8
		mov	[module_type_text], 20574F57h ;	WOW

loc_10213:				; CODE XREF: sub_100BD+106j
					; sub_100BD+145j
		call	sub_10311
		call	near ptr sub_11F4E
		jb	loc_10099
		retn
endp		sub_100BD ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1021E near		; CODE XREF: sub_100BD+18p
					; sub_100BD+52p ...
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		cld
		lodsb
		xor	ah, ah
		mov	[word_245FA], ax
		lodsb
		cmp	al, 78h	; 'x'
		jb	short loc_10230
		xor	al, al

loc_10230:				; CODE XREF: sub_1021E+Ej
		mov	[word_245F8], ax
		mov	di, offset byte_27FE8
		mov	cx, 20h	; ' '
		cld
		rep movsd
		mov	si, offset chrin ; in
		mov	di, offset asc_246B0 ; out
		mov	cx, 14h		; count
		call	copy_printable
		retn
endp		sub_1021E


; =============== S U B	R O U T	I N E =======================================


proc		sub_1024A near		; CODE XREF: sub_100BD+61p
					; sub_100BD:loc_101B7p
		mov	si, offset chrin
		mov	di, offset myout ; out
		mov	cx, [word_245D2]

loc_10254:				; CODE XREF: sub_1024A+A6j
		push	cx
		add	si, 20		; in
		mov	cx, 16h		; count
		call	copy_printable
		sub	si, 20
		pop	cx
		movzx	edx, [word ptr si+2Ah]
		xchg	dl, dh
		shl	edx, 1
		cmp	edx, 100000h
		cmc
		adc	[word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	al, [si+2Ch]
		and	al, 0Fh
		mov	[di+3Eh], al
		mov	ax, [freq_245DE]
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

loc_102C1:				; CODE XREF: sub_1024A+6Dj
		or	[byte ptr di+3Ch], 8
		add	eax, ebx
		cmp	eax, edx
		jbe	short loc_102DF
		mov	eax, [di+28h]
		shr	eax, 1
		add	eax, ebx
		cmp	eax, edx
		jbe	short loc_102DF

loc_102DC:				; CODE XREF: sub_1024A+68j
					; sub_1024A+75j
		mov	eax, edx

loc_102DF:				; CODE XREF: sub_1024A+81j
					; sub_1024A+90j
		dec	eax
		mov	[di+2Ch], eax
		mov	[di+24h], ebx
		add	si, 1Eh
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_10254
		retn
endp		sub_1024A


; =============== S U B	R O U T	I N E =======================================


proc		sub_102F5 near		; CODE XREF: sub_100BD+1Bp
					; sub_100BD+64p ...
		mov	si, offset byte_27FE8
		xor	bx, bx
		mov	cx, 80h	; '€'
		cld

loc_102FE:				; CODE XREF: sub_102F5+13j
		lodsb
		and	al, 7Fh
		cmp	al, bl
		jb	short loc_10307
		mov	bl, al

loc_10307:				; CODE XREF: sub_102F5+Ej
		dec	cx
		jnz	short loc_102FE
		inc	bl
		mov	[word_245F2], bx
		retn
endp		sub_102F5


; =============== S U B	R O U T	I N E =======================================


proc		sub_10311 near		; CODE XREF: sub_100BD+67p
					; sub_100BD:loc_10213p
		mov	cx, [word_245F2]

loc_10315:				; CODE XREF: sub_10311+D5j
		push	cx
		mov	dx, offset word_31508
		mov	cx, [word_245D4]
		shl	cx, 8
		call	dosfread
		test	[moduleflag_246D0], 10b
		jz	short loc_1035C
		mov	ax, ds
		mov	es, ax
		mov	si, offset word_31508
		mov	di, offset byte_31D08
		mov	cx, 200h
		cld
		rep movsd
		mov	si, offset byte_31D08
		mov	di, offset word_31508
		mov	bx, 40h	; '@'

loc_10345:				; CODE XREF: sub_10311+49j
		mov	cx, 4
		rep movsd
		add	si, 3F0h
		mov	cx, 4
		rep movsd
		sub	si, 400h
		dec	bx
		jnz	short loc_10345

loc_1035C:				; CODE XREF: sub_10311+18j
		call	memalloc12k
		mov	si, offset word_31508
		mov	cx, 40h	; '@'

loc_10365:				; CODE XREF: sub_10311+CEj
		push	cx
		mov	cx, [word_245D4]
		xor	ch, ch

loc_1036C:				; CODE XREF: sub_10311+C5j
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

loc_10399:				; CODE XREF: sub_10311+74j
					; sub_10311+7Cj ...
		cmp	ax, [table_25118+bx]
		jnb	short loc_103A8
		add	bx, 2
		cmp	bx, 166
		jb	short loc_10399

loc_103A8:				; CODE XREF: sub_10311+8Cj
		mov	ax, bx
		shr	ax, 1
		mov	bl, 12
		div	bl
		inc	ah
		shl	al, 4
		or	al, ah
		mov	bl, al

loc_103B9:				; CODE XREF: sub_10311+6Cj
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
		call	sub_11B85
		pop	cx
		dec	cx
		jnz	loc_10315
		retn
endp		sub_10311

; ---------------------------------------------------------------------------

_2stm_module:				; DATA XREF: seg003:0E19o
		mov	[module_type_text], 4D545332h ;	2STM
		jmp	short loc_103FF
; ---------------------------------------------------------------------------

stm_module:				; DATA XREF: seg003:0E0Co
		mov	[module_type_text], 204D5453h ;	STM

loc_103FF:				; CODE XREF: seg000:03F4j
		mov	[moduleflag_246D0], 1000b
		mov	[word_245D4], 4
		mov	[word_245D2], 1Fh
		mov	[freq_245DE], 8448
		mov	al, 60h	; '`'
		call	sub_13E9B
		mov	[byte_24679], ah
		mov	[byte_2467A], al
		movzx	ax, [byte_30529]
		mov	[word_245F2], ax
		mov	ax, ds
		mov	es, ax
		mov	si, offset chrin
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 14h
		call	copy_printable
		mov	si, offset byte_30538
		mov	di, offset myout
		mov	cx, [word_245D2]

loc_10445:				; CODE XREF: seg000:04CEj
		push	cx
		mov	cx, 0Ch
		call	copy_printable
		pop	cx

loc_1044D:
		movzx	eax, [word ptr si+10h]
		mov	edx, eax
		add	eax, 0Fh
		and	al, 0F0h
		cmp	eax, 100000h
		cmc
		adc	[word_24662], 0

loc_10467:
		mov	[di+20h], eax
		add	[dword_245C4], eax
		movzx	eax, [word ptr si+0Eh]
		shl	eax, 4
		mov	[di+38h], eax
		mov	ax, [si+18h]
		or	ax, ax
		jnz	short loc_10487
		mov	ax, [freq_245DE]

loc_10487:				; CODE XREF: seg000:0482j
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

loc_104B6:				; CODE XREF: seg000:04A1j
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	[byte ptr di+3Ch], 8

loc_104C7:				; CODE XREF: seg000:04B4j
		add	si, 20h	; ' '
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_10445
		mov	dx, offset byte_27FE8
		mov	cx, 80h	; '€'
		mov	eax, 410h
		call	dosseek
		mov	si, offset byte_27FE8
		xor	ax, ax

loc_104E6:				; CODE XREF: seg000:04F0j
		cmp	[byte ptr si], 63h ; 'c'
		jnb	short loc_104F2
		inc	ax
		inc	si
		cmp	ax, 80h	; '€'
		jb	short loc_104E6

loc_104F2:				; CODE XREF: seg000:04E9j
		mov	[word_245FA], ax
		mov	cx, [word_245F2]

loc_104F9:				; CODE XREF: seg000:0580j
		push	cx
		mov	dx, offset chrin
		mov	cx, 400h
		call	dosfread
		call	memalloc12k
		mov	si, offset chrin
		mov	cx, 40h	; '@'

loc_1050C:				; CODE XREF: seg000:0579j
		push	cx
		mov	cx, [word_245D4]
		xor	ch, ch

loc_10513:				; CODE XREF: seg000:0570j
		push	cx
		xor	bx, bx
		xor	dx, dx
		xor	cl, cl
		mov	al, [si]
		cmp	al, 0FEh ; 'þ'
		jz	short loc_10565
		mov	cl, 0FFh
		cmp	al, 0FFh
		jz	short loc_1052E
		cmp	al, 0FBh ; 'û'
		jnb	short loc_10565
		inc	al
		mov	bl, al

loc_1052E:				; CODE XREF: seg000:0524j
		mov	bh, [si+1]
		shr	bh, 3
		mov	ax, [si+1]
		and	ax, 0F007h
		shr	ah, 1
		or	al, ah
		cmp	al, 40h	; '@'
		jbe	short loc_10544
		mov	al, 0FFh

loc_10544:				; CODE XREF: seg000:0540j
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

loc_10565:				; CODE XREF: seg000:051Ej seg000:0528j ...
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
		call	sub_11B85
		pop	cx
		dec	cx
		jnz	loc_104F9
		call	near ptr sub_11F4E
		jb	loc_10099
		retn
; ---------------------------------------------------------------------------
asc_1058C	db 0,18h,0Bh,0Dh,0Ah	; DATA XREF: seg000:055Cr
		db 2,1,3,4,7,0

; =============== S U B	R O U T	I N E =======================================

; S3M

proc		s3m_module near		; DATA XREF: seg003:0E26o
		mov	[module_type_text], 204D3353h
		mov	[moduleflag_246D0], 10000b
		mov	[byte_2467E], 1
		mov	[byte_24673], 80h ; '€'
		mov	[freq_245DE], 8363
		mov	[byte_2461A], 2
		cmp	[word_30532], 2
		jnb	short loc_105C7
		mov	[byte_24673], 0

loc_105C7:				; CODE XREF: s3m_module+29j
		mov	ax, ds
		mov	es, ax
		mov	si, offset chrin ; in
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 1Ch		; count
		call	copy_printable
		test	[byte ptr word_246DA+1], 20h
		jz	short loc_1061E
		mov	dx, 64h	; 'd'
		mov	cl, [byte_3053B]
		and	cx, 7Fh
		jz	short loc_10618
		test	[byte_3053B], 80h
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
		call	near ptr change_amplif

loc_1061E:				; CODE XREF: s3m_module+45j
		xor	si, si
		mov	di, offset byte_25908
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
		test	[byte_30548+si], 8
		jz	short loc_1065F
		mov	al, [byte_2461F]

loc_1065F:				; CODE XREF: s3m_module+C3j
		mov	[byte ptr dword_27BC8+si], al
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
		mov	di, offset myout ; out
		mov	bx, (offset dword_30566+2)
		add	bx, [word ptr unk_30528]
		movzx	ecx, [word_245D2]

loc_106A3:				; CODE XREF: s3m_module+1CAj
		push	bx
		push	cx
		mov	dx, offset word_31508
		mov	cx, 50h	; 'P'
		movzx	eax, [word ptr bx]
		shl	eax, 4
		call	dosseek
		mov	si, offset word_31508
		xor	eax, eax
		xor	edx, edx
		cmp	[byte ptr si], 1
		jnz	short loc_106D8
		movzx	eax, [word ptr si+10h]
		mov	edx, eax
		cmp	eax, 100000h
		cmc
		adc	[word_24662], 0

loc_106D8:				; CODE XREF: s3m_module+12Bj
		mov	[di+20h], eax
		add	[dword_245C4], eax
		movzx	eax, [word ptr si+0Eh]
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
		test	[byte ptr si+1Fh], 1
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
		mov	si, (offset dword_30566+2)
		xor	di, di
		xor	bx, bx
		mov	ax, [word ptr unk_30528]
		cmp	ax, 80h	; '€'
		mov	ah, al
		ja	short loc_1079A
		xor	cl, cl

loc_10778:				; CODE XREF: s3m_module+1FFj
		mov	al, [si]
		cmp	al, 0F0h ; 'ð'
		jnb	short loc_1078F
		mov	[byte_27FE8+di], al
		inc	bl
		inc	di
		cmp	cl, 0F0h ; 'ð'
		jb	short loc_1078F
		mov	[byte_280E7+di], 0FFh

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
		mov	[byte_27FE8+di], al
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
		mov	bx, (offset dword_30566+2)
		add	bx, [word ptr unk_30528]
		add	ax, [word_3052A]
		shl	ax, 1
		add	bx, ax
		mov	dx, offset word_31508
		mov	cx, 2
		movzx	eax, [word ptr bx]
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
		mov	dx, offset word_31508
		mov	cx, [word_31508]
		cmp	cx, 308Fh
		jnb	short loc_107D2
		add	cx, 0Fh
		and	cl, 0F0h
		sub	cx, 2
		call	dosfread
		call	memalloc12k
		mov	si, offset word_31508
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
		cmp	bl, 0FEh ; 'þ'
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
		cmp	[byte ptr word_245D4+1], ch
		jnb	short loc_1089C
		mov	[byte ptr word_245D4+1], ch

loc_1089C:				; CODE XREF: s3m_module+2FFj
		call	sub_11BA6
		lodsb
		or	al, al
		jnz	loc_10811

loc_108A6:				; CODE XREF: s3m_module+276j
		mov	[byte ptr es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	loc_10809

loc_108B1:				; CODE XREF: s3m_module+246j
		call	sub_11B85
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
		call	near ptr sub_11F4E
		jb	loc_10099
		retn
endp		s3m_module ; sp-analysis failed

; ---------------------------------------------------------------------------
s3mtable_108D6	db 0FFh,10h,0Bh,0Dh,15h,12h,11h,13h,14h,1Bh,1Dh,17h,16h
					; DATA XREF: s3m_module+2BDr
		db 0FFh,0FFh,9,0FFh,1Ch,7,0Eh,0Fh,0FFh,0FFh,0FFh,8,0FFh
s3mtable_108F0	db 0,3,5,4,7,0FFh,0FFh,0FFh,8,0FFh,0FFh,6,0Ch,0Dh,0FFh
					; DATA XREF: s3m_module+2D6r
		db 0FFh

; =============== S U B	R O U T	I N E =======================================

; E669

proc		e669_module near	; DATA XREF: seg003:0E61o
		mov	[module_type_text], 39363645h
		jmp	short loc_10914
; ---------------------------------------------------------------------------

_669_module:				; DATA XREF: seg003:0E5Ao
		mov	[module_type_text], 20393636h ;	669

loc_10914:				; CODE XREF: e669_module+9j
		mov	[moduleflag_246D0], 100b
		mov	[byte_24673], 80h ; '€'
		mov	[byte_2467E], 2
		mov	[word_245D4], 8
		movzx	ax, [byte_30576]
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
		mov	si, (offset chrin+1)
		mov	cx, 4Ch	; 'L'

loc_1095C:				; CODE XREF: e669_module+60j
		inc	si		; in
		cmp	[byte ptr si], 20h ; ' '
		loope	loc_1095C
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 20h	; ' '   ; count
		call	copy_printable
		xor	si, si
		xor	bh, bh

loc_1096F:				; CODE XREF: e669_module+91j
		mov	bl, [byte_30579+si]
		cmp	bl, 0FFh
		jz	short loc_10993
		mov	[byte_27FE8+si], bl
		mov	al, [byte_305F9+bx]
		mov	[byte_280E8+si], al
		mov	al, [byte_30679+bx]
		mov	[byte_281E8+si], al
		inc	si
		cmp	si, 80h	; '€'
		jb	short loc_1096F

loc_10993:				; CODE XREF: e669_module+76j
		mov	[word_245FA], si
		mov	al, [byte_280E8]
		mov	[byte_24679], al
		mov	[byte_2467A], 50h ; 'P'
		mov	dx, offset chrin
		imul	cx, [word_245D2], 25
		mov	eax, 497
		call	dosseek
		mov	si, offset chrin ; in
		mov	di, offset myout ; out
		mov	cx, [word_245D2]

loc_109BD:				; CODE XREF: e669_module+127j
		push	cx
		mov	cx, 0Dh		; count
		call	copy_printable
		pop	cx
		mov	edx, [si+0Dh]
		cmp	edx, 100000h
		cmc
		adc	[word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
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

loc_10A0F:				; CODE XREF: e669_module+FAj
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	[byte ptr di+3Ch], 8

loc_10A20:				; CODE XREF: e669_module+10Dj
		add	si, 19h
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_109BD
		mov	cx, [word_245F2]

loc_10A2D:				; CODE XREF: e669_module+1C9j
		push	cx
		mov	dx, offset word_31508
		mov	cx, 600h
		call	dosfread
		call	memalloc12k
		mov	si, offset word_31508
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
		cmp	al, 0FEh ; 'þ'
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
		mov	[byte ptr es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	loc_10A40
		call	sub_11B85
		pop	cx
		dec	cx
		jnz	loc_10A2D
		call	near ptr sub_11F4E
		jb	loc_10099
		retn
endp		e669_module ; sp-analysis failed

; ---------------------------------------------------------------------------

mtm_module:				; DATA XREF: seg003:0E2Fo
		mov	[module_type_text], 204D544Dh ;	MTM
		mov	[moduleflag_246D0], 100000b
		mov	[byte_24679], 6
		mov	[byte_2467A], 7Dh ; '}'
		mov	[byte_24673], 80h ; '€'
		mov	ax, ds
		mov	es, ax
		mov	si, offset myin
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 14h
		call	copy_printable
		cmp	[sndcard_type],	0
		jnz	short loc_10B25
		xor	si, si
		mov	cx, 10h

loc_10B0F:				; CODE XREF: seg000:0B23j
		mov	al, [byte ptr word_3052A+si]
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:byte_13C54+di]
		mov	[byte ptr dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_10B0F

loc_10B25:				; CODE XREF: seg000:0B08j
		movzx	ax, [byte_30526]
		mov	[word_245D2], ax
		mov	al, [byte_30522]
		inc	al
		mov	[word_245F2], ax
		movzx	ax, [byte_30523]
		inc	ax
		mov	[word_245FA], ax
		mov	dx, offset chrin
		imul	cx, [word_245D2], 25h
		add	cx, 0C2h ; 'Â'
		xor	eax, eax
		call	dosseek
		mov	si, offset unk_3054A
		mov	di, offset myout
		mov	cx, [word_245D2]
; START	OF FUNCTION CHUNK FOR sub_1422D

loc_10B5A:				; CODE XREF: sub_1422D-3660j
		push	cx
		mov	cx, 16h		; count
		call	copy_printable
		pop	cx
		mov	edx, [si+16h]

loc_10B66:				; CODE XREF: sub_1422D+1Ej
		cmp	edx, 100000h
		cmc
		adc	[word_24662], 0
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

loc_10BB5:				; CODE XREF: sub_1422D-368Dj
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax
		or	[byte ptr di+3Ch], 8

loc_10BC6:				; CODE XREF: sub_1422D-367Aj
		add	si, 25h	; '%'
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_10B5A
		mov	di, offset byte_27FE8
		mov	cx, 20h	; ' '
		cld
		rep movsd
		imul	ax, [word_245D2], 37
		add	ax, 0C2h ; 'Â'
		movzx	eax, ax
		mov	[chrin], eax
		movzx	eax, [word_30520]
		imul	eax, 192	; CODE XREF: sub_1424F+16j
		add	eax, [chrin]
		mov	dx, offset byte_33508
		mov	cx, [word_245F2]
		shl	cx, 6
		call	dosseek
		mov	si, offset byte_33508
		mov	cx, [word_245F2]
		mov	ax, 4

loc_10C12:				; CODE XREF: sub_1422D-3603j
		mov	bp, 1

loc_10C15:				; CODE XREF: sub_1422D-3606j
		cmp	[word ptr si], 0
		jz	short loc_10C20
		cmp	bp, ax
		jb	short loc_10C20
		mov	ax, bp

loc_10C20:				; CODE XREF: sub_1422D-3615j
					; sub_1422D-3611j
		add	si, 2
		inc	bp
		cmp	bp, 20h	; ' '
		jbe	short loc_10C15
		dec	cx
		jnz	short loc_10C12
		mov	[word_245D4], ax
		mov	bx, offset byte_33508
		mov	cx, [word_245F2]

loc_10C36:				; CODE XREF: sub_1422D-354Aj
		push	bx
		push	cx
		mov	si, offset word_31508
		mov	cx, [word_245D4]

loc_10C3F:				; CODE XREF: sub_1422D-35AFj
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

loc_10C5A:				; CODE XREF: sub_1422D-35E7j
		dec	ax
		movzx	eax, ax
		imul	eax, 192
		add	eax, [chrin]
		mov	dx, si
		mov	cx, 192
		call	dosseek

loc_10C73:				; CODE XREF: sub_1422D-35D5j
		pop	si
		pop	cx
		pop	bx
		add	bx, 2
		add	si, 192
		dec	cx
		jnz	short loc_10C3F
		call	memalloc12k
		mov	si, offset word_31508
		mov	cx, 40h	; '@'

loc_10C89:				; CODE XREF: sub_1422D-3555j
		push	cx
		push	si
		mov	cx, [word_245D4]
		xor	ch, ch

loc_10C91:				; CODE XREF: sub_1422D-3562j
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

loc_10CAA:				; CODE XREF: sub_1422D-3594j
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
		call	sub_11B85
		pop	cx
		pop	bx
		add	bx, 40h	; '@'
		dec	cx
		jnz	loc_10C36
		mov	ax, 192
		mul	[word_30520]
		mov	cx, dx
		imul	dx, [word_245D2], 37
		add	dx, 0C2h ; 'Â'
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
		adc	[word_24662], 0
		call	near ptr sub_11F4E
		jb	loc_10099
		retn
; END OF FUNCTION CHUNK	FOR sub_1422D
; ---------------------------------------------------------------------------

psm_module:				; DATA XREF: seg003:0E37o
		mov	[module_type_text], 204D5350h ;	PSM
		mov	[moduleflag_246D0], 1000000b
		mov	ax, [word_30556]
		mov	[word_245D4], ax
		mov	ax, [word_30554]
		mov	[word_245D2], ax
		mov	[freq_245DE], 8448
		mov	al, [byte_3054B]
		mov	[byte_24679], al
		mov	al, [byte_3054C]
		mov	[byte_2467A], al
		movzx	ax, [byte_30550]
		mov	[word_245FA], ax
		mov	ax, [word_30552]
		mov	[word_245F2], ax
		mov	ax, ds
		mov	es, ax
		mov	si, offset myin
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 30
		call	copy_printable
		mov	dx, offset byte_3059A
		mov	cx, [word_245D2]
		shl	cx, 6
		mov	eax, [dword_30566]
		call	dosseek
		mov	si, offset byte_3059A
		mov	di, offset myout
		mov	cx, [word_245D2]

loc_10D8C:				; CODE XREF: seg000:0E20j
		push	cx
		push	si
		add	si, 0Dh
		mov	cx, 16h
		call	copy_printable
		pop	si
		pop	cx
		mov	edx, [si+30h]
		cmp	edx, 100000h
		cmc
		adc	[word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	[byte ptr di+3Fh], 1
		mov	eax, [si+25h]
		mov	[di+38h], eax
		mov	ax, [si+3Eh]
		jnz	short loc_10DC7
		mov	ax, [freq_245DE]

loc_10DC7:				; CODE XREF: seg000:0DC2j
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

loc_10DF0:				; CODE XREF: seg000:0DDBj
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

loc_10E15:				; CODE XREF: seg000:0E04j
		or	[byte ptr di+3Ch], 8

loc_10E19:				; CODE XREF: seg000:0DEEj
		add	si, 40h	; '@'
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_10D8C
		mov	dx, offset byte_27FE8
		mov	cx, [word_245FA]
		mov	eax, [dword_3055A]
		call	dosseek
		mov	dx, [word_30562]
		mov	cx, [word_30564]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		adc	[word_24662], 0
		mov	cx, [word_245F2]

loc_10E4C:				; CODE XREF: seg000:0F02j
		push	cx
		mov	dx, offset word_31508
		mov	cx, 4
		call	dosfread
		xor	si, si
		mov	cx, [word_245FA]
		mov	ax, [word_245F4]
		mov	dl, [byte_3150A]
		dec	dl
		and	dl, 3Fh

loc_10E68:				; CODE XREF: seg000:0E74j
		cmp	[byte_27FE8+si], al
		jnz	short loc_10E72
		mov	[byte_281E8+si], dl

loc_10E72:				; CODE XREF: seg000:0E6Cj
		inc	si
		dec	cx
		jnz	short loc_10E68
		mov	dx, offset byte_3150C
		mov	cx, [word_31508]
		sub	cx, 4
		call	dosfread
		call	memalloc12k
		mov	si, offset byte_3150C
		mov	cx, 40h	; '@'

loc_10E8C:				; CODE XREF: seg000:0EFBj
		push	cx
		lodsb
		or	al, al
		jz	short loc_10EF4

loc_10E92:				; CODE XREF: seg000:0EF2j
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

loc_10EB6:				; CODE XREF: seg000:0EA2j
		cmp	bh, 63h	; 'c'
		jbe	short loc_10EBD
		xor	bh, bh

loc_10EBD:				; CODE XREF: seg000:0E99j seg000:0EB9j
		mov	cl, 0FFh
		test	ch, 40h
		jz	short loc_10ECE
		mov	cl, [si]
		inc	si
		cmp	cl, 40h	; '@'
		jbe	short loc_10ECE
		mov	cl, 0FFh

loc_10ECE:				; CODE XREF: seg000:0EC2j seg000:0ECAj
		test	ch, 20h
		jz	short loc_10EDD
		mov	dx, [si]
		add	si, 2
		cmp	dl, 0Fh
		jbe	short loc_10EDF

loc_10EDD:				; CODE XREF: seg000:0ED1j
		xor	dx, dx

loc_10EDF:				; CODE XREF: seg000:0EDBj
		and	ch, 1Fh
		cmp	[byte ptr word_245D4+1], ch
		jnb	short loc_10EEC
		mov	[byte ptr word_245D4+1], ch

loc_10EEC:				; CODE XREF: seg000:0EE6j
		call	sub_11BA6
		lodsb
		or	al, al
		jnz	short loc_10E92

loc_10EF4:				; CODE XREF: seg000:0E90j
		mov	[byte ptr es:di], 0
		inc	di
		pop	cx
		dec	cx
		jnz	short loc_10E8C
		call	sub_11B85
		pop	cx
		dec	cx
		jnz	loc_10E4C
		mov	ax, [word_245D4]
		inc	ah
		cmp	al, ah
		jb	short loc_10F11
		mov	al, ah

loc_10F11:				; CODE XREF: seg000:0F0Dj
		xor	ah, ah
		mov	[word_245D4], ax
		call	near ptr sub_11F4E
		jb	loc_10099
		retn

; =============== S U B	R O U T	I N E =======================================

; FAR

proc		far_module near		; DATA XREF: seg003:0E40o
		mov	[module_type_text], 20524146h
		mov	[moduleflag_246D0], 10000000b
		mov	[byte_24673], 0
		mov	[byte_2467E], 2
		mov	[word_245D4], 10h
		mov	al, [byte ptr word_30552+1]
		and	ax, 0Fh
		mov	di, ax
		mov	al, [cs:byte_14057+di]
		mov	[byte_2467B], al
		mov	[byte_2467C], 0
		call	sub_14043
		mov	[byte_2467A], al
		mov	[byte_24679], 4
		cmp	[sndcard_type],	0
		jnz	short loc_10F80
		xor	si, si
		mov	cx, [word_245D4]

loc_10F6A:				; CODE XREF: far_module+60j
		mov	al, [byte ptr word_30554+si]
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:byte_13C54+di]
		mov	[byte ptr dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_10F6A

loc_10F80:				; CODE XREF: far_module+44j
		mov	ax, ds
		mov	es, ax
		mov	si, offset myin	; in
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 20h	; ' '   ; count
		call	copy_printable
		mov	dx, (offset dword_30566+2)
		mov	cx, 303h
		movzx	eax, [word ptr dword_30566+2]
		add	eax, 62h ; 'b'
		call	dosseek
		movzx	ax, [byte_30669]
		cmp	ax, 100h
		jb	short loc_10FB0
		mov	ax, 100h

loc_10FB0:				; CODE XREF: far_module+8Dj
		mov	[word_245FA], ax
		movzx	ax, [byte_3066A]
		mov	[word_245F8], ax
		mov	si, (offset dword_30566+2)
		mov	di, offset byte_27FE8
		mov	cx, [word_245FA]
		cld
		rep movsb
		mov	bx, offset byte_3066B
		xor	ax, ax
		xor	dx, dx

loc_10FCF:				; CODE XREF: far_module+C0j
		inc	dx
		cmp	[word ptr bx], 0
		jz	short loc_10FD7
		mov	ax, dx

loc_10FD7:				; CODE XREF: far_module+B5j
		add	bx, 2
		cmp	dx, 100h
		jb	short loc_10FCF
		or	ax, ax
		stc
		jz	loc_10099
		cmp	ax, 100h
		jb	short loc_10FEF
		mov	ax, 100h

loc_10FEF:				; CODE XREF: far_module+CCj
		mov	[word_245F2], ax
		mov	[byte ptr chrin+3], 0
		mov	si, offset byte_3066B
		mov	cx, [word_245F2]

loc_10FFE:				; CODE XREF: far_module+214j
		push	cx
		push	si
		mov	ax, [si]
		or	ax, ax
		jnz	short loc_1100F
		call	memalloc12k
		mov	cx, 40h	; '@'
		jmp	loc_11120
; ---------------------------------------------------------------------------

loc_1100F:				; CODE XREF: far_module+E6j
		sub	ax, 2
		shr	ax, 2
		xor	dx, dx
		div	[word_245D4]
		push	ax
		dec	al
		and	al, 3Fh
		mov	[byte ptr chrin], al
		xor	di, di
		mov	cx, [word_245FA]
		mov	ah, [byte ptr chrin+3]

loc_1102D:				; CODE XREF: far_module+11Bj
		cmp	ah, [byte_27FE8+di]
		jnz	short loc_11037
		mov	[byte_281E8+di], al

loc_11037:				; CODE XREF: far_module+113j
		inc	di
		dec	cx
		jnz	short loc_1102D
		mov	dx, offset word_31508
		mov	cx, [si]
		call	dosfread
		mov	[byte ptr chrin+1], 0
		call	memalloc12k
		pop	cx
		xor	ch, ch
		mov	si, offset byte_3150A

loc_11051:				; CODE XREF: far_module+1F7j
		push	cx
		mov	cx, [word_245D4]
		xor	ch, ch

loc_11058:				; CODE XREF: far_module+1ECj
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

loc_11082:				; CODE XREF: far_module+143j
					; far_module+160j
		mov	cl, 0FFh
		mov	al, [si+2]
		or	al, al
		jz	short loc_11094
		dec	al
		and	al, 0Fh
		shl	al, 2
		mov	cl, al

loc_11094:				; CODE XREF: far_module+16Bj
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

loc_110CB:				; CODE XREF: far_module+184j
		mov	dl, 19h
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110CF:				; CODE XREF: far_module+18Ej
		shr	dh, 1
		mov	[byte ptr chrin+1], dh
		xor	dx, dx
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110D9:				; CODE XREF: far_module+193j
		shl	dh, 4
		or	dh, [byte ptr chrin+1]
		mov	dl, 4
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110E4:				; CODE XREF: far_module+189j
		mov	dl, 0Eh

loc_110E6:
		or	dh, 90h
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110EB:				; CODE XREF: far_module+1A7j
		mov	dl, 1Fh
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110EF:				; CODE XREF: far_module+19Dj
		mov	dl, 20h	; ' '
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110F3:				; CODE XREF: far_module+1A2j
		mov	dl, 20h	; ' '
		shl	dh, 4
		jmp	short loc_110FF
; ---------------------------------------------------------------------------

loc_110FA:				; CODE XREF: far_module+198j
		mov	dl, 0Eh

loc_110FC:
		or	dh, 80h

loc_110FF:				; CODE XREF: far_module+1ABj
					; far_module+1AFj ...
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
		sub	cl, [byte ptr chrin]

loc_11120:				; CODE XREF: far_module+EEj
		xor	al, al
		cld
		rep stosb
		call	sub_11B85
		pop	si
		pop	cx
		inc	[byte ptr chrin+3]
		add	si, 2
		dec	cx
		jnz	loc_10FFE
		mov	ax, ds
		assume es:dseg
		mov	es, ax
		assume es:seg003

loc_1113A:
		mov	dx, offset myin
		mov	cx, 8
		call	dosfread
		mov	si, offset myin
		mov	di, offset myout

loc_11149:
		xor	ax, ax
		mov	[word_245D2], ax
		mov	ch, 8

loc_11150:				; CODE XREF: far_module+305j
		mov	cl, 8

loc_11152:				; CODE XREF: far_module+2FEj
		inc	ax
		shr	[byte ptr si], 1
		jnb	loc_11217
		push	ax
		push	cx
		push	si
		push	di
		mov	[word_245D2], ax
		push	di
		mov	dx, offset word_31508
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
		mov	si, offset word_31508 ;	in

loc_11181:
		mov	edx, [si+20h]
		cmp	edx, 100000h
		cmc

loc_1118D:
		adc	[word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	al, [si+25h]
		ror	al, 4
		shr	al, 2
		mov	[di+3Dh], al
		mov	ax, [freq_245DE]
		mov	[di+36h], ax

loc_111AD:
		test	[byte ptr si+2Fh], 8
		jnz	short loc_111C6

loc_111B3:				; CODE XREF: far_module+2AFj
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_111E8
; ---------------------------------------------------------------------------

loc_111C6:				; CODE XREF: far_module+293j
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

loc_111E8:				; CODE XREF: far_module+2A6j
		mov	cx, 20h	; ' '   ; count
		call	copy_printable
		test	[byte ptr si+2Eh], 1
		jz	short loc_11204
		or	[byte ptr di+3Ch], 4
		shr	[dword ptr di+24h], 1
		shr	[dword ptr di+2Ch], 1
		shr	[dword ptr di+28h], 1

loc_11204:				; CODE XREF: far_module+2D4j
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

loc_11217:				; CODE XREF: far_module+237j
		add	di, 40h	; '@'
		dec	cl
		jnz	loc_11152
		inc	si
		dec	ch
		jnz	loc_11150
		cmp	[word_245D2], 0
		stc
		jz	loc_10099
		call	near ptr sub_11F4E
		jb	loc_10099
		retn
endp		far_module ; sp-analysis failed

; ---------------------------------------------------------------------------

ult_module:				; DATA XREF: seg003:0E49o
		mov	[module_type_text], 20544C55h ;	ULT
		mov	[moduleflag_246D0], 1000000000b
		mov	[byte_24673], 0
		mov	[word ptr chrin], 40h ;	'@'
		mov	ax, [word_30515]

loc_11256:
		xchg	al, ah
		mov	[word_30515], ax
		cmp	ax, 3034h
		jb	short loc_11265
		add	[word ptr chrin], 2

loc_11265:				; CODE XREF: seg000:125Ej
		mov	[byte_24679], 6
		mov	[byte_2467A], 7Dh ; '}'

loc_1126F:
		mov	ax, ds
		mov	es, ax
		mov	si, offset unk_30517
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 20h	; ' '
		call	copy_printable
		mov	dx, offset byte_30538
		mov	cx, 1
		movzx	eax, [byte_30537]
		shl	eax, 5
		add	eax, 30h ; '0'
		call	dosseek
		movzx	ax, [byte_30538]
		mov	[word_245D2], ax
		mul	[word ptr chrin]
		mov	cx, ax
		mov	dx, offset byte_30539
		call	dosfread
		mov	si, offset byte_30539
		mov	di, offset myout
		mov	cx, [word_245D2]

loc_112B4:				; CODE XREF: seg000:136Aj
		push	cx
		push	si
		push	di
		mov	edx, [si+38h]
		sub	edx, [si+34h]
		jnb	short loc_112C4
		xor	edx, edx

loc_112C4:				; CODE XREF: seg000:12BFj
		cmp	edx, 100000h
		cmc
		adc	[word_24662], 0
		mov	[di+20h], edx
		add	[dword_245C4], edx
		mov	al, [si+3Ch]
		shr	al, 2
		mov	[di+3Dh], al
		mov	ax, [freq_245DE]
		cmp	[word_30515], 3034h
		jb	short loc_112F1
		mov	ax, [si+3Eh]

loc_112F1:				; CODE XREF: seg000:12ECj
		mov	[di+36h], ax
		mov	al, [si+3Dh]
		and	al, 1Ch
		mov	[di+3Ch], al
		test	al, 4
		jz	short loc_11316
		add	[dword_245C4], edx
		cmp	edx, 80000h
		cmc
		adc	[word_24662], 0
		shl	[dword ptr di+20h], 1

loc_11316:				; CODE XREF: seg000:12FEj
		test	al, 8
		jnz	short loc_1132D

loc_1131A:				; CODE XREF: seg000:1334j
		xor	eax, eax
		mov	[di+24h], eax
		mov	[di+28h], eax
		dec	edx
		mov	[di+2Ch], edx
		jmp	short loc_11359
; ---------------------------------------------------------------------------

loc_1132D:				; CODE XREF: seg000:1318j
		mov	eax, [si+30h]
		or	eax, eax
		jz	short loc_1131A
		dec	eax
		mov	ebx, [si+2Ch]
		test	[byte ptr di+3Ch], 4
		jz	short loc_11348
		shr	ebx, 1
		shr	eax, 1

loc_11348:				; CODE XREF: seg000:1340j
		mov	[di+24h], ebx
		mov	[di+2Ch], eax
		sub	eax, ebx
		inc	eax
		mov	[di+28h], eax

loc_11359:				; CODE XREF: seg000:132Bj
		mov	cx, 20h	; ' '
		call	copy_printable
		pop	di
		pop	si
		pop	cx
		add	di, 40h	; '@'

loc_11365:
		add	si, [word ptr chrin]
		dec	cx
		jnz	loc_112B4
		mov	dx, offset byte_30539
		mov	cx, 102h
		call	dosfread
		mov	[word_245F8], 0
		mov	si, offset byte_30539
		xor	ax, ax

loc_11382:				; CODE XREF: seg000:138Cj
		cmp	[byte ptr si], 0FFh
		jz	short loc_1138E
		inc	ax
		inc	si
		cmp	ax, 100h
		jb	short loc_11382

loc_1138E:				; CODE XREF: seg000:1385j
		mov	[word_245FA], ax
		mov	ax, ds
		mov	es, ax
		mov	si, offset byte_30539
		mov	di, offset byte_27FE8
		mov	cx, [word_245FA]
		cld
		rep movsb
		movzx	ax, [byte_30639]
		inc	ax
		mov	[word_245D4], ax
		movzx	ax, [byte_3063A]
		inc	ax
		mov	[word_245F2], ax
		mov	[byte_2467E], 0
		mov	ax, [word_30515]
		cmp	ax, 3031h
		jz	short loc_113C6
		mov	[byte_2467E], 2

loc_113C6:				; CODE XREF: seg000:13BFj
		cmp	ax, 3033h
		jb	short loc_113F8
		mov	dx, offset word_3063B
		mov	cx, [word_245D4]
		call	dosfread
		cmp	[sndcard_type],	0
		jnz	short loc_113F8
		xor	si, si
		mov	cx, [word_245D4]

loc_113E2:				; CODE XREF: seg000:13F6j
		mov	al, [byte ptr word_3063B+si]
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:byte_13C54+di]
		mov	[byte ptr dword_27BC8+si], al
		inc	si
		dec	cx
		jnz	short loc_113E2

loc_113F8:				; CODE XREF: seg000:13C9j seg000:13DAj
		mov	si, offset dword_30518
		mov	cx, [word_245D4]

loc_113FF:				; CODE XREF: seg000:1432j
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

loc_11417:				; CODE XREF: seg000:142Aj
		push	cx
		mov	[byte ptr word_3063B+1], 1
		mov	cx, 40h	; '@'

loc_11420:				; CODE XREF: seg000:1426j
		push	cx
		call	sub_1155A
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

loc_11438:				; CODE XREF: seg000:14FFj
		push	cx
		mov	si, offset dword_30518
		mov	di, offset byte_30908
		mov	cx, [word_245D4]

loc_11443:				; CODE XREF: seg000:1489j
		push	cx
		mov	dx, [si]
		mov	cx, [si+2]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		mov	[byte ptr word_3063B+1], 1
		mov	cx, 40h	; '@'

loc_1145A:				; CODE XREF: seg000:1470j
		push	cx
		call	sub_1155A
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
		mov	si, offset byte_30908
		mov	cx, 40h	; '@'

loc_11494:				; CODE XREF: seg000:14F8j
		push	cx
		push	si
		mov	cx, [word_245D4]
		xor	ch, ch

loc_1149C:				; CODE XREF: seg000:14EBj
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

loc_114C0:				; CODE XREF: seg000:14A3j seg000:14BCj
		mov	cl, 0FFh
		mov	al, [si+2]
		mov	dl, al
		shr	al, 4
		mov	ah, [si+4]
		and	dl, 0Fh
		mov	dh, [si+3]
		call	sub_1150B
		xchg	ax, dx
		call	sub_1150B
		cmp	dl, al
		ja	short loc_114DF
		xchg	ax, dx

loc_114DF:				; CODE XREF: seg000:14DCj
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
		call	sub_11B85
		pop	cx
		dec	cx
		jnz	loc_11438
		call	near ptr sub_11F4E
		jb	loc_10099
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_1150B near		; CODE XREF: seg000:14D3p seg000:14D7p
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

loc_11520:				; CODE XREF: sub_1150B+2j
		xor	ax, ax
		retn
; ---------------------------------------------------------------------------

loc_11523:				; CODE XREF: sub_1150B+6j
		shr	ah, 2
		and	ah, 33h
		retn
; ---------------------------------------------------------------------------

loc_1152A:				; CODE XREF: sub_1150B+Aj
		and	ax, 0F00h
		or	ax, 800Eh
		retn
; ---------------------------------------------------------------------------

loc_11531:				; CODE XREF: sub_1150B+Ej
		mov	cl, ah
		shr	cl, 2
		xor	ax, ax
		retn
; ---------------------------------------------------------------------------

loc_11539:				; CODE XREF: sub_1150B+12j
		push	dx
		mov	dx, ax
		shr	dx, 4
		cmp	dl, 0EAh ; 'ê'
		jz	short loc_1154B
		cmp	dl, 0EBh ; 'ë'
		jz	short loc_1154B
		pop	dx
		retn
; ---------------------------------------------------------------------------

loc_1154B:				; CODE XREF: sub_1150B+37j
					; sub_1150B+3Cj
		mov	dh, ah
		and	dh, 0F0h
		and	ah, 0Fh
		shr	ah, 2
		or	ah, dh
		pop	dx
		retn
endp		sub_1150B


; =============== S U B	R O U T	I N E =======================================


proc		sub_1155A near		; CODE XREF: seg000:1421p seg000:145Bp
		dec	[byte ptr word_3063B+1]
		jnz	short locret_11584
		mov	dx, offset word_3063B
		mov	cx, 2
		call	dosfread
		cmp	[byte ptr word_3063B], 0FCh ; 'ü'
		jz	short loc_11585
		mov	ax, [word_3063B]
		mov	[word ptr dword_3063D],	ax
		mov	[byte ptr word_3063B+1], 1
		mov	dx, (offset dword_3063D+2)
		mov	cx, 3
		call	dosfread

locret_11584:				; CODE XREF: sub_1155A+4j
		retn
; ---------------------------------------------------------------------------

loc_11585:				; CODE XREF: sub_1155A+14j
		mov	dx, offset dword_3063D
		mov	cx, 5
		call	dosfread
		retn
endp		sub_1155A


; =============== S U B	R O U T	I N E =======================================


proc		doswrite near		; CODE XREF: createwritefile+B7p
					; createwritefile+E3p ...
		push	dx
		push	ecx
		call	doswrite2
		pop	ecx
		pop	dx
		jb	short locret_115A2
		mov	bx, [fhandle_module]
		mov	ah, 40h
		int	21h		; DOS -	2+ - WRITE TO FILE WITH	HANDLE
					; BX = file handle, CX = number	of bytes to write, DS:DX -> buffer

locret_115A2:				; CODE XREF: doswrite+9j
		retn
endp		doswrite


; =============== S U B	R O U T	I N E =======================================


proc		doswrite2 near		; CODE XREF: doswrite+3p
					; createwritefile+12Cp	...
		mov	[chrin], eax
		mov	[myin],	ecx
		mov	dx, offset chrin
		mov	cx, 8
		mov	bx, [fhandle_module]
		mov	ah, 40h
		int	21h		; DOS -	2+ - WRITE TO FILE WITH	HANDLE
					; BX = file handle, CX = number	of bytes to write, DS:DX -> buffer
		retn
endp		doswrite2


; =============== S U B	R O U T	I N E =======================================


proc		createwritefile	far
		mov	cx, 20h	; ' '
		mov	ah, 3Ch
		int	21h		; DOS -	2+ - CREATE A FILE WITH	HANDLE (CREAT)
					; CX = attributes for file
					; DS:DX	-> ASCIZ filename (may include drive and path)
		mov	bx, ax
		mov	ax, 0FFFFh
		jb	locret_11786
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	es, ax
		mov	[savesp_245D0],	sp
		mov	[fhandle_module], bx
		mov	cx, 14h
		mov	esi, offset aInertiaModule_0 ; "Inertia	Module:	"
		mov	edi, offset aInertiaModule ; "Inertia Module: "
		cld
		rep movsd
		mov	si, offset asc_246B0 ; "				"
		mov	di, (offset aInertiaModule+10h)
		mov	cx, 8
		rep movsd
		mov	[byte_257DA], 10h
		mov	al, [byte_2461A]
		mov	[byte_257DB], al
		mov	al, [byte_2467E]
		mov	[byte_257DC], al
		mov	ax, [word_245D4]
		mov	[word_257E6], ax
		mov	ax, [word_245D2]
		mov	[word_257E8], ax
		mov	ax, [word_245F2]
		mov	[word_257EA], ax
		mov	ax, [freq_245DE]
		mov	[word_257EC], ax
		mov	ax, [word_245FA]
		mov	[word_257EE], ax
		mov	ax, [word_245F8]
		mov	[word_257F0], ax
		mov	al, [byte_2467A]
		mov	[byte_257F2], al
		mov	al, [byte_24679]
		mov	[byte_257F3], al
		mov	dx, offset aInertiaModule ; "Inertia Module: "
		mov	cx, 50h	; 'P'
		mov	bx, [fhandle_module]
		mov	ah, 40h
		int	21h		; DOS -	2+ - WRITE TO FILE WITH	HANDLE
					; BX = file handle, CX = number	of bytes to write, DS:DX -> buffer
		mov	ax, 0FFFEh
		jb	loc_11777
		mov	si, offset byte_280E8
		mov	cx, [word_245FA]
		xor	al, al

loc_11659:				; CODE XREF: createwritefile+A2j
		or	al, [si]
		inc	si
		dec	cx
		jnz	short loc_11659
		or	al, al
		jz	short loc_1167C
		mov	dx, offset byte_280E8
		movzx	ecx, [word_245FA]
		mov	eax, 54534C54h	; TLST
		call	doswrite
		mov	ax, 0FFFEh
		jb	loc_11777

loc_1167C:				; CODE XREF: createwritefile+A6j
		mov	si, offset byte_281E8
		mov	cx, [word_245FA]
		mov	al, 3Fh	; '?'

loc_11685:				; CODE XREF: createwritefile+CEj
		and	al, [si]
		inc	si
		dec	cx
		jnz	short loc_11685
		cmp	al, 3Fh	; '?'
		jz	short loc_116A8
		mov	dx, offset byte_281E8
		movzx	ecx, [word_245FA]
		mov	eax, 54534C42h	; BLST
		call	doswrite
		mov	ax, 0FFFEh
		jb	loc_11777

loc_116A8:				; CODE XREF: createwritefile+D2j
		mov	dx, offset byte_27FE8
		movzx	ecx, [word_245FA]
		mov	eax, 54534C50h	; PLST
		call	doswrite
		mov	ax, 0FFFEh
		jb	loc_11777
		mov	[word_257A4], 0
		mov	cx, [word_245F2]

loc_116CB:				; CODE XREF: createwritefile+156j
		push	cx
		mov	bx, [word_257A4]
		shl	bx, 1
		movzx	ecx, [word_27DE8+bx]
		cmp	cx, 40h	; '@'
		ja	short loc_116E0
		xor	ecx, ecx

loc_116E0:				; CODE XREF: createwritefile+120j
		push	cx
		mov	eax, 54544150h	; PATT
		call	doswrite2
		pop	cx
		jb	loc_11777
		jcxz	short loc_1170B
		mov	bx, [word_257A4]
		shl	bx, 1
		mov	ax, [segs_table+bx]
		xor	dx, dx
		mov	bx, [fhandle_module]
		push	ds
		mov	ds, ax
		mov	ah, 40h
		int	21h		; DOS -	2+ - WRITE TO FILE WITH	HANDLE
					; BX = file handle, CX = number	of bytes to write, DS:DX -> buffer
		pop	ds
		jb	short loc_11777

loc_1170B:				; CODE XREF: createwritefile+134j
		pop	cx
		inc	[word_257A4]
		dec	cx
		jnz	short loc_116CB
		mov	cx, [word_245D2]
		mov	[word_257A4], 0

loc_1171D:				; CODE XREF: createwritefile+1ACj
		push	cx
		xor	cx, cx
		xor	dx, dx
		mov	bx, [fhandle_module]
		mov	ax, 4201h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from present location
		mov	[word ptr dword_257A0],	ax
		mov	[word ptr dword_257A0+2], dx
		mov	ax, [word_257A4]
		shl	ax, 6
		mov	bx, ax
		add	bx, offset myout
		mov	ecx, 78h ; 'x'
		add	ecx, [bx+20h]
		mov	eax, 504D4153h	; SAMP
		call	doswrite2
		jb	short loc_11777
		mov	dx, [word_257A4]
		mov	bx, [fhandle_module]
		push	cs
		call	near ptr sub_1181D
		pop	cx
		jb	short loc_11777
		inc	[word_257A4]
		dec	cx
		jnz	short loc_1171D
		xor	ecx, ecx
		mov	eax, 4D444E45h	; ENDM
		call	doswrite2
		xor	ax, ax

loc_11777:				; CODE XREF: createwritefile+91j
					; createwritefile+BDj ...
		push	ax
		mov	bx, [fhandle_module]
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle
		pop	ax
		mov	sp, [savesp_245D0]
		pop	ds

locret_11786:				; CODE XREF: createwritefile+Cj
		retf
endp		createwritefile	; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_11787 near		; CODE XREF: sub_1181D+82p
		mov	ecx, [di+20h]
		or	ecx, ecx
		jz	short loc_117DC
		test	[sndflags_24622], 4
		jnz	locret_1181C
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_117DE
		mov	bx, [di+32h]

loc_117A2:				; CODE XREF: sub_11787+53j
		mov	eax, ecx
		cmp	eax, 8000h
		jb	short loc_117B3
		mov	eax, 8000h

loc_117B3:				; CODE XREF: sub_11787+24j
		sub	ecx, eax
		push	ecx
		push	ds
		push	bx
		push	ax
		call	sub_11E8B
		pop	cx
		xor	dx, dx
		mov	bx, [fhandle_module]
		mov	ds, [ems_pageframe]
		mov	ah, 40h
		int	21h		; DOS -	2+ - WRITE TO FILE WITH	HANDLE
					; BX = file handle, CX = number	of bytes to write, DS:DX -> buffer
		pop	bx
		pop	ds
		pop	ecx
		jb	short locret_117DD
		add	bx, 2
		cmp	ecx, 0
		jnz	short loc_117A2

loc_117DC:				; CODE XREF: sub_11787+7j
		clc

locret_117DD:				; CODE XREF: sub_11787+4Aj
		retn
; ---------------------------------------------------------------------------

loc_117DE:				; CODE XREF: sub_11787+16j
		mov	ecx, [di+20h]
		mov	dx, [di+30h]

loc_117E5:				; CODE XREF: sub_11787+91j
		mov	eax, ecx
		cmp	eax, 8000h
		jb	short loc_117F6
		mov	eax, 8000h

loc_117F6:				; CODE XREF: sub_11787+67j
		sub	ecx, eax
		push	ecx
		push	ds
		push	dx
		mov	cx, ax
		mov	bx, [fhandle_module]
		mov	ds, dx
		xor	dx, dx
		mov	ah, 40h
		int	21h		; DOS -	2+ - WRITE TO FILE WITH	HANDLE
					; BX = file handle, CX = number	of bytes to write, DS:DX -> buffer
		pop	dx
		pop	ds
		pop	ecx
		jb	short locret_1181B
		add	dx, 800h
		or	ecx, ecx
		jnz	short loc_117E5
		clc

locret_1181B:				; CODE XREF: sub_11787+88j
		retn
; ---------------------------------------------------------------------------

locret_1181C:				; CODE XREF: sub_11787+Ej
		retn
endp		sub_11787


; =============== S U B	R O U T	I N E =======================================


proc		sub_1181D far		; CODE XREF: createwritefile+1A1p
		push	ds
		shl	dx, 6
		mov	ax, seg003
		mov	ds, ax
		mov	es, ax
		mov	cx, 18h
		mov	si, offset unk_258A6
		mov	di, offset aInertiaSample ; "Inertia Sample: "
		cld
		rep movsd
		mov	cx, 8
		mov	si, dx
		add	si, offset myout
		mov	di, offset asc_25856 ; "				\r\n\x1A"
		rep movsd
		add	dx, offset myout
		mov	di, dx
		mov	eax, [di+24h]
		mov	[dword_25892], eax
		mov	eax, [di+2Ch]
		mov	[dword_25896], eax
		mov	ax, [di+36h]
		mov	[word_2588E], ax
		mov	al, [di+3Eh]
		mov	[byte_2588C], al
		mov	al, [di+3Dh]
		mov	[byte_2588B], al
		mov	al, [di+3Ch]
		mov	[byte_2588D], al
		mov	eax, [di+20h]
		mov	[dword_25886], eax
		push	eax
		mov	dx, offset aInertiaSample ; "Inertia Sample: "
		mov	cx, 96
		mov	bx, [fhandle_module]
		mov	ah, 40h
		int	21h		; DOS -	2+ - WRITE TO FILE WITH	HANDLE
					; BX = file handle, CX = number	of bytes to write, DS:DX -> buffer
		mov	ax, 0FFFEh
		pop	ecx
		jb	short loc_118AE
		push	di
		mov	eax, 54414453h	; SDAT
		call	doswrite2
		mov	ax, 0FFFEh
		pop	di
		call	sub_11787
		mov	eax, 53444E45h	; ENDS
		xor	ecx, ecx
		call	doswrite2

loc_118AE:				; CODE XREF: sub_1181D+72j
		pop	ds
		retf
endp		sub_1181D


; =============== S U B	R O U T	I N E =======================================


proc		sub_118B0 near		; CODE XREF: inr_module+152p
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	es, ax
		shl	dx, 6
		mov	ax, dx
		add	ax, offset myout
		push	ax
		mov	cx, 96
		mov	bx, [fhandle_module]
		mov	dx, offset aInertiaSample ; "Inertia Sample: "
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

loc_1191C:				; CODE XREF: sub_118B0+FCj
		mov	dx, offset chrin
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
		test	[sndflags_24622], 4
		jnz	short loc_11999
		jmp	short loc_11999
; ---------------------------------------------------------------------------

loc_11967:				; CODE XREF: sub_118B0+A8j
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

loc_11991:				; CODE XREF: sub_118B0+BDj
		cmp	eax, 53444E45h	; ENDS
		jz	short loc_119AF

loc_11999:				; CODE XREF: sub_118B0+B3j
					; sub_118B0+B5j
		mov	dx, [word ptr dword_257A0]
		mov	cx, [word ptr dword_257A0+2]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file
		jb	short loc_119B2
		jmp	loc_1191C
; ---------------------------------------------------------------------------

loc_119AF:				; CODE XREF: sub_118B0+DFj
					; sub_118B0+E7j
		clc
		pop	ds
		retn
; ---------------------------------------------------------------------------

loc_119B2:				; CODE XREF: sub_118B0+20j
					; sub_118B0+7Aj ...
		mov	ax, 0FFFEh
		pop	ds
		retn
endp		sub_118B0


; =============== S U B	R O U T	I N E =======================================


proc		sub_119B7 near		; CODE XREF: inr_module+B0p
					; inr_module+C5p ...
		mov	ecx, [myin]
		mov	bx, [fhandle_module]
		mov	dx, di
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		retn
endp		sub_119B7


; =============== S U B	R O U T	I N E =======================================

; INR

proc		inr_module near		; DATA XREF: seg003:off_25326o
		mov	[module_type_text], 20524E49h
		mov	[moduleflag_246D0], 100000000b
		mov	[byte_24673], 0
		mov	[word_245F2], 0
		mov	[word_245D2], 0
		mov	ax, ds
		mov	es, ax
		cld
		mov	dx, offset aInertiaModule ; "Inertia Module: "
		mov	cx, 50h	; 'P'
		xor	eax, eax
		call	dosseek
		mov	si, (offset aInertiaModule+10h)
		mov	di, offset asc_246B0 ; "				"
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
		mov	dx, offset chrin
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
		add	[word ptr dword_257A0],	ax
		adc	[word ptr dword_257A0+2], dx
		mov	eax, [chrin]
		cmp	eax, 54534C54h	; TLST
		jnz	short loc_11A81	; BLST
		mov	di, offset byte_280E8
		call	sub_119B7
		jb	loc_11B3D
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11A81:				; CODE XREF: inr_module+ABj
		cmp	eax, 54534C42h	; BLST
		jnz	short loc_11A96	; PLST
		mov	di, offset byte_281E8
		call	sub_119B7
		jb	loc_11B3D
		jmp	loc_11B28
; ---------------------------------------------------------------------------

loc_11A96:				; CODE XREF: inr_module+C0j
		cmp	eax, 54534C50h	; PLST
		jnz	short loc_11AAA	; PATT
		mov	di, offset byte_27FE8
		call	sub_119B7
		jb	loc_11B3D
		jmp	short loc_11B28
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
		inc	[word_245F2]
		shl	di, 1
		mov	[segs_table+di], ax
		cmp	cx, 40h	; '@'
		jbe	short loc_11AF3
		mov	[word_27DE8+di], cx
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
		jmp	short loc_11B28
; ---------------------------------------------------------------------------

loc_11AF3:				; CODE XREF: inr_module+114j
		mov	[word_27DE8+di], 40h ; '@'
		xor	di, di
		mov	es, ax
		assume es:nothing
		mov	cx, 10h
		xor	eax, eax
		cld
		rep stosd
		jmp	short loc_11B28
; ---------------------------------------------------------------------------

loc_11B09:				; CODE XREF: inr_module+E9j
		cmp	eax, 504D4153h	; SAMP
		jnz	short loc_11B20	; ENDM
		mov	dx, [word_245D2]
		inc	[word_245D2]
		call	sub_118B0
		jb	short loc_11B3D
		jmp	short loc_11B28
; ---------------------------------------------------------------------------

loc_11B20:				; CODE XREF: inr_module+148j
		cmp	eax, 4D444E45h	; ENDM
		jz	short loc_11B41

loc_11B28:				; CODE XREF: inr_module+B7j
					; inr_module+CCj ...
		mov	dx, [word ptr dword_257A0]
		mov	cx, [word ptr dword_257A0+2]
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
		call	near ptr sub_11F4E
		retn
endp		inr_module ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		dosseek	near		; CODE XREF: seg000:04DEp
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
endp		dosseek	; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		dosfread near		; CODE XREF: moduleread+39p
					; sub_10311+Fp	...
		mov	bx, [fhandle_module]
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		mov	cx, ax
		mov	ax, 0FFFCh
		jb	lfreaderr	; 1 problem here
		retn
endp		dosfread


; =============== S U B	R O U T	I N E =======================================


proc		memalloc12k near	; CODE XREF: sub_10311:loc_1035Cp
					; seg000:0503p	...
		mov	ebx, 12352	; bytes
		call	memalloc
		jb	loc_10099
		mov	es, ax
		xor	di, di
		retn
endp		memalloc12k


; =============== S U B	R O U T	I N E =======================================


proc		sub_11B85 near		; CODE XREF: sub_10311+D0p
					; seg000:057Bp	...
		mov	bx, [word_245F4]
		shl	bx, 1
		mov	[segs_table+bx], es
		mov	[word_27DE8+bx], di
		movzx	ebx, di
		mov	ax, es
		call	memrealloc
		adc	[word_24662], 0
		inc	[word_245F4]
		retn
endp		sub_11B85


; =============== S U B	R O U T	I N E =======================================


proc		sub_11BA6 near		; CODE XREF: sub_10311+BDp
					; seg000:loc_10565p ...
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
endp		sub_11BA6


; =============== S U B	R O U T	I N E =======================================


proc		sub_11C0C near		; CODE XREF: sub_1415E+65p
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
endp		sub_11C0C

; ---------------------------------------------------------------------------
byte_11C29	db 0			; DATA XREF: sub_11C0C:loc_11C14r
					; sub_13623+1A1r
		db 2, 1, 3, 2, 4, 3, 5

; =============== S U B	R O U T	I N E =======================================


; int __usercall copy_printable<eax>(char *in<esi>, char *out<edi>, int	count<ecx>)
proc		copy_printable near	; CODE XREF: sub_1021E+28p
					; sub_1024A+11p ...
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
endp		copy_printable


; =============== S U B	R O U T	I N E =======================================


proc		sub_11C43 far		; CODE XREF: moduleread+3Dp
					; sub_12DA8+75p ...
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	[byte_24679], 6
		mov	[byte_2467A], 7Dh ; '}'
		mov	[byte_2467E], 0
		mov	[moduleflag_246D0], 1
		mov	[word_245F4], 0
		mov	[word_245F0], 0
		mov	[word_245F6], 0
		mov	[byte_24673], 0
		mov	[word_24630], 2
		mov	[word_245FA], 0
		mov	[word_245F8], 0
		mov	[word_245D4], 4
		mov	[word_245D6], 4
		mov	[word_245D8], 0
		mov	[word_245DA], 0
		mov	[word_245D2], 0
		mov	[freq_245DE], 8287
		test	[byte_24672], 8
		jnz	short loc_11CB8
		mov	[freq_245DE], 8363

loc_11CB8:				; CODE XREF: sub_11C43+6Dj
		mov	[byte_2461A], 0
		mov	[dword_245C4], 0
		mov	[amplification], 100
		mov	[byte_24625], 0
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		cld
		mov	di, offset asc_246B0 ; "				"
		mov	cx, 8
		mov	eax, '    '
		rep stosd
		mov	di, offset byte_25908
		xor	eax, eax
		mov	cx, 280h
		rep stosd
		mov	di, offset byte_282E8
		mov	cx, 8
		rep stosd
		mov	di, offset dword_27BC8
		mov	ah, [byte_2461E]
		mov	al, [byte_2461F]
		shl	eax, 10h
		mov	ah, [byte_2461F]
		mov	al, [byte_2461E]
		mov	cx, 8
		rep stosd
		mov	di, offset myout
		xor	eax, eax
		mov	cx, 630h
		rep stosd
		mov	dx, 63h	; 'c'
		mov	di, offset myout
		mov	eax, '    '

loc_11D2D:				; CODE XREF: sub_11C43+FCj
		mov	cx, 8
		rep stosd
		sub	di, 20h	; ' '
		mov	[word ptr di+32h], 0FFFFh
		add	di, 40h	; '@'
		dec	dx
		jnz	short loc_11D2D
		mov	di, offset segs_table
		mov	cx, 80h	; '€'
		xor	eax, eax
		rep stosd
		mov	di, offset byte_280E8
		mov	cx, 40h	; '@'
		rep stosd
		mov	di, offset byte_27FE8
		mov	cx, 40h	; '@'
		rep stosd
		mov	di, offset byte_282E8
		mov	cx, 8
		rep stosd
		mov	di, offset byte_281E8
		mov	cx, 40h	; '@'
		mov	eax, 3F3F3F3Fh
		rep stosd
		pop	ds
		retf
endp		sub_11C43


; =============== S U B	R O U T	I N E =======================================


proc		ems_init near		; CODE XREF: sub_12DA8+103p
		mov	[ems_supported], 0
		mov	ax, 1
		test	[byte ptr word_246DA], 2
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
		mov	[ems_supported], 1
		mov	[ems_log_pagenum], 0
		xor	ax, ax
		clc
		retn
; ---------------------------------------------------------------------------

loc_11E00:				; CODE XREF: ems_init+Dj ems_init+25j	...
		stc
		retn
endp		ems_init


; =============== S U B	R O U T	I N E =======================================


proc		sub_11E02 near		; CODE XREF: sub_11E37+7p
		cmp	[ems_supported], 1
		jnz	short locret_11E1D
		mov	bx, 8000h
		call	sub_11E8B
		mov	dx, [ems_handle]
		mov	ah, 45h	; 'E'
		int	67h		;  - LIM EMS - RELEASE HANDLE AND MEMORY
					; DX = EMM handle
					; Return: AH = status
		mov	[ems_log_pagenum], 0

locret_11E1D:				; CODE XREF: sub_11E02+5j
		retn
endp		sub_11E02


; =============== S U B	R O U T	I N E =======================================


proc		sub_11E1E near		; CODE XREF: sub_125DA+6p
		cmp	[ems_supported], 1
		jnz	short locret_11E36
		mov	dx, [ems_handle]
		mov	bx, 1
		mov	ah, 51h	; 'Q'
		int	67h		;  - LIM EMS 4.0 - REALLOCATE PAGES
					; DX = handle
					; BX = number of pages to be allocated to handle
					; Return: BX = actual number of	pages allocated	to handle
					; AH = status
		mov	[ems_log_pagenum], 0

locret_11E36:				; CODE XREF: sub_11E1E+5j
		retn
endp		sub_11E1E


; =============== S U B	R O U T	I N E =======================================


proc		sub_11E37 near		; CODE XREF: sub_125B9+Fp
		cmp	[ems_supported], 1
		jnz	short locret_11E46
		call	sub_11E02
		mov	[ems_supported], 0

locret_11E46:				; CODE XREF: sub_11E37+5j
		retn
endp		sub_11E37


; =============== S U B	R O U T	I N E =======================================


proc		sub_11E47 near		; CODE XREF: moduleread+24p
					; volume_prep+16p ...
		cmp	[ems_supported], 1
		jnz	short locret_11E67
		mov	cx, 32h	; '2'

loc_11E51:				; CODE XREF: sub_11E47+19j
		mov	dx, [ems_handle]
		mov	ax, 4700h
		int	67h		;  - LIM EMS - SAVE MAPPING CONTEXT
					; DX = handle
					; Return: AH = status
		cmp	ah, 0
		jz	short locret_11E67
		dec	cx
		jnz	short loc_11E51
		mov	[byte_246A5], 1

locret_11E67:				; CODE XREF: sub_11E47+5j
					; sub_11E47+16j
		retn
endp		sub_11E47


; =============== S U B	R O U T	I N E =======================================


proc		sub_11E68 near		; CODE XREF: moduleread+78p
					; moduleread+A9p ...
		cmp	[ems_supported], 1
		jnz	short locret_11E8A
		cmp	[byte_246A5], 1
		jnz	short locret_11E8A
		mov	cx, 32h	; '2'

loc_11E79:				; CODE XREF: sub_11E68+20j
		mov	dx, [ems_handle]
		mov	ax, 4800h
		int	67h		;  - LIM EMS - RESTORE MAPPING CONTEXT
					; DX = handle
					; Return: AH = status
		cmp	ah, 0
		jz	short locret_11E8A
		dec	cx
		jnz	short loc_11E79

locret_11E8A:				; CODE XREF: sub_11E68+5j sub_11E68+Cj ...
		retn
endp		sub_11E68


; =============== S U B	R O U T	I N E =======================================


proc		sub_11E8B near		; CODE XREF: sub_11787+34p
					; sub_11E02+Ap	...
		cmp	[ems_supported], 1
		jnz	short locret_11EC4
		mov	cx, 32h	; '2'
		cmp	bx, [ems_log_pagenum]
		jb	short loc_11E9E
		mov	bx, 0FFFFh	; EMS UNMAP

loc_11E9E:				; CODE XREF: sub_11E8B+Ej
					; sub_11E8B+37j
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

loc_11EB3:				; CODE XREF: sub_11E8B+20j
		mov	bx, 0FFFFh

loc_11EB6:				; CODE XREF: sub_11E8B+26j
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

locret_11EC4:				; CODE XREF: sub_11E8B+5j
					; sub_11E8B+34j
		retn
endp		sub_11E8B


; =============== S U B	R O U T	I N E =======================================


proc		sub_11EC5 near		; CODE XREF: sub_122E8+48p
					; sub_122E8+F4p ...
		cmp	[ems_supported], 1
		jnz	short locret_11EFE
		mov	cx, 32h	; '2'
		cmp	bx, [ems_log_pagenum]
		jb	short loc_11ED8
		mov	bx, 0FFFFh

loc_11ED8:				; CODE XREF: sub_11EC5+Ej
					; sub_11EC5+37j
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

loc_11EED:				; CODE XREF: sub_11EC5+20j
		mov	bx, 0FFFFh

loc_11EF0:				; CODE XREF: sub_11EC5+26j
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

locret_11EFE:				; CODE XREF: sub_11EC5+5j
					; sub_11EC5+34j
		retn
endp		sub_11EC5


; =============== S U B	R O U T	I N E =======================================


proc		sub_11EFF near		; CODE XREF: sub_11F4E+36p
		inc	[byte_24617]
		cmp	[ems_supported], 1
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

loc_11F3C:				; CODE XREF: sub_11EFF+9j
					; sub_11EFF+2Dj
		mov	ebx, [di+20h]
		add	ebx, 1020h	; bytes
		call	memalloc
		mov	cx, 0FFFFh
		retn
endp		sub_11EFF


; =============== S U B	R O U T	I N E =======================================


proc		sub_11F4E far		; CODE XREF: sub_100BD+6Ap
					; sub_100BD+159p ...
		mov	[byte_24617], 0
		cmp	[word_24662], 0
		stc
		jnz	short locret_11FD3
		test	[sndflags_24622], 4
		jnz	short loc_11FD6
		test	[sndflags_24622], 10h
		jnz	short loc_11FD2
		mov	cx, [word_245D2]
		mov	di, offset myout

loc_11F70:				; CODE XREF: sub_11F4E+82j
		push	cx
		cmp	[dword ptr di+20h], 0
		jz	short loc_11FCB
		mov	[byte_24675], 1
		mov	al, [di+3Fh]
		mov	[byte_24674], al
		push	di
		call	sub_11EFF
		pop	di
		jb	short loc_11FD4
		mov	[di+30h], ax
		mov	[di+32h], cx
		mov	es, ax
		test	[moduleflag_246D0], 10111011000b
		jz	short loc_11FA9
		mov	dx, [di+38h]
		mov	cx, [di+3Ah]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file

loc_11FA9:				; CODE XREF: sub_11F4E+4Aj
		mov	bx, [fhandle_module]
		mov	ecx, [di+20h]
		push	di
		push	es
		mov	dx, [di+32h]
		call	sub_12247
		adc	[word_24662], 0
		pop	es
		assume es:nothing
		pop	di
		mov	ax, es
		push	di
		call	sub_122E8
		pop	di
		or	[byte ptr di+3Ch], 1

loc_11FCB:				; CODE XREF: sub_11F4E+28j
		add	di, 40h	; '@'
		pop	cx
		dec	cx
		jnz	short loc_11F70

loc_11FD2:				; CODE XREF: sub_11F4E+19j
		clc

locret_11FD3:				; CODE XREF: sub_11F4E+Bj
		retn
; ---------------------------------------------------------------------------

loc_11FD4:				; CODE XREF: sub_11F4E+3Aj
		pop	cx
		retn
; ---------------------------------------------------------------------------

loc_11FD6:				; CODE XREF: sub_11F4E+12j
		mov	eax, 10000h
		mov	cl, [byte_2462C]
		call	alloc_dma_buf
		jb	locret_1221F
		mov	[word ptr dma_buf_pointer+2], ax
		mov	[word ptr dma_buf_pointer], 0
		mov	di, offset myout
		mov	cx, [word_245D2]

loc_11FF7:				; CODE XREF: sub_11F4E+1D9j
		push	cx
		cmp	[dword ptr di+20h], 0
		jz	loc_12106
		inc	[byte_24617]
		mov	[byte_24675], 1
		mov	al, [di+3Fh]
		mov	[byte_24674], al
		test	[moduleflag_246D0], 10111011000b
		jz	short loc_12027
		mov	dx, [di+38h]
		mov	cx, [di+3Ah]
		mov	bx, [fhandle_module]
		mov	ax, 4200h
		int	21h		; DOS -	2+ - MOVE FILE READ/WRITE POINTER (LSEEK)
					; AL = method: offset from beginning of	file

loc_12027:				; CODE XREF: sub_11F4E+C8j
		test	[byte ptr di+3Ch], 4
		jz	short loc_1206B
		mov	eax, [di+20h]
		add	eax, 1Fh
		and	al, 0E0h
		shr	eax, 2
		mov	bx, [word_24630]
		shl	bx, 2
		add	ax, bx
		jnb	short loc_12056
		and	[word_24630], 0C000h
		add	[word_24630], 4000h
		jb	loc_12117

loc_12056:				; CODE XREF: sub_11F4E+F6j
		mov	ax, [word_24630]
		mov	bx, ax
		and	bx, 0C000h
		and	ax, 3FFFh
		shr	ax, 1

loc_12064:				; CODE XREF: sub_141F6+13j
		or	ax, bx

loc_12066:				; CODE XREF: sub_141F6+13j
		mov	[di+34h], ax
		jmp	short loc_12071
; ---------------------------------------------------------------------------

loc_1206B:				; CODE XREF: sub_11F4E+DDj
		mov	ax, [word_24630]
		mov	[di+34h], ax

loc_12071:				; CODE XREF: sub_11F4E+11Bj
		mov	ecx, [di+20h]

loc_12075:				; CODE XREF: sub_11F4E+174j
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
		adc	[word_24662], 0
		les	si, [dma_buf_pointer]
		assume es:nothing
		mov	cx, 8000h
		call	sub_12220
		push	di

loc_120AA:
		mov	cx, 8000h
		mov	ax, [word_24630]
		call	sub_182E7
		xor	[word ptr dma_buf_pointer], 8000h
		add	[word_24630], 800h
		pop	di
		pop	ecx
		jmp	short loc_12075
; ---------------------------------------------------------------------------

loc_120C4:				; CODE XREF: sub_11F4E+12Ej
		jcxz	short loc_120E7
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
		adc	[word_24662], 0
		les	si, [dma_buf_pointer]
		push	cx
		call	sub_12220
		pop	cx

loc_120E7:				; CODE XREF: sub_11F4E:loc_120C4j
		push	cx
		mov	ax, [word_24630]
		call	sub_182E7
		xor	[word ptr dma_buf_pointer], 8000h
		pop	ax
		add	ax, 21h	; '!'
		and	al, 0E0h
		shr	ax, 4

loc_120FD:
		add	[word_24630], ax
		pop	di
		or	[byte ptr di+3Ch], 1

loc_12106:				; CODE XREF: sub_11F4E+AFj
		pop	cx
		mov	dx, [word_24630]
		shr	dx, 1
		mov	al, [byte_24628]
		shl	ax, 0Dh
		cmp	dx, ax
		jbe	short loc_12123

loc_12117:				; CODE XREF: sub_11F4E+104j
		call	sub_18A28
		mov	dx, offset aNotEnoughDramOn ; "Not enough DRAM on UltraSound\r\n"
		mov	ax, 0FFFDh
		jmp	lfreaderr
; ---------------------------------------------------------------------------

loc_12123:				; CODE XREF: sub_11F4E+1C7j
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_11FF7

loc_1212B:				; CODE XREF: sub_11F4E+1E2j
		cmp	[byte_2466E], 1
		jz	short loc_1212B
		call	sub_18A28
		mov	di, offset myout
		mov	cx, [word_245D2]

loc_1213C:				; CODE XREF: sub_11F4E+2CCj
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
		call	sub_17DC6
		pop	edi
		mov	edx, [di+2Ch]
		push	edi
		movzx	edi, [word ptr di+34h]
		shl	edi, 4
		add	edi, edx
		add	edi, 2
		call	sub_17DE8
		pop	edi
		mov	edx, [di+24h]
		push	edi
		movzx	edi, [word ptr di+34h]
		shl	edi, 4
		add	edi, edx
		call	sub_17DC6
		pop	edi

loc_1219E:				; CODE XREF: sub_11F4E+203j
		mov	edx, [di+2Ch]
		push	edi
		movzx	edi, [word ptr di+34h]
		shl	edi, 4
		add	edi, edx
		inc	edi
		call	sub_17DE8
		pop	edi
		jmp	short loc_12215
; ---------------------------------------------------------------------------

loc_121B9:				; CODE XREF: sub_11F4E+1FDj
		test	[byte ptr di+3Ch], 8
		jz	short loc_121EE
		mov	edx, [di+24h]
		test	[byte ptr di+3Ch], 10h
		jz	short loc_121CD
		mov	edx, [di+2Ch]

loc_121CD:				; CODE XREF: sub_11F4E+279j
		push	edi
		mov	bx, [di+34h]
		movzx	edi, bx
		and	di, 1FFFh
		and	bx, 0C000h
		shr	bx, 1
		or	di, bx
		shl	edi, 4
		add	edi, edx
		call	sub_17E0E
		pop	edi

loc_121EE:				; CODE XREF: sub_11F4E+26Fj
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
		call	sub_17E49
		pop	edi

loc_12215:				; CODE XREF: sub_11F4E+269j
		pop	cx

loc_12216:				; CODE XREF: sub_11F4E+1F2j
		add	di, 40h	; '@'
		dec	cx
		jnz	loc_1213C
		clc

locret_1221F:				; CODE XREF: sub_11F4E+95j
		retn
endp		sub_11F4E ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_12220 near		; CODE XREF: sub_11F4E+158p
					; sub_11F4E+195p ...
		cmp	[byte_24674], 1
		jz	short loc_12228
		retn
; ---------------------------------------------------------------------------

loc_12228:				; CODE XREF: sub_12220+5j
		mov	al, [byte_24676]
		cmp	[byte_24675], 0
		jz	short loc_12239
		mov	[byte_24675], 0
		xor	al, al

loc_12239:				; CODE XREF: sub_12220+10j
					; sub_12220+21j
		add	al, [es:si]
		mov	[es:si], al
		inc	si
		dec	cx
		jnz	short loc_12239
		mov	[byte_24676], al
		retn
endp		sub_12220


; =============== S U B	R O U T	I N E =======================================


proc		sub_12247 near		; CODE XREF: sub_11F4E+68p
		mov	edi, ecx
		xor	esi, esi
		mov	bp, es

loc_1224F:				; CODE XREF: sub_12247+98j
		push	dx
		cmp	dx, 0FFFFh
		jz	short loc_12262
		push	dx
		push	cx
		push	bx
		push	ax
		mov	bx, dx
		call	sub_11E8B
		pop	ax
		pop	bx
		pop	cx
		pop	dx

loc_12262:				; CODE XREF: sub_12247+Cj
		xor	dx, dx
		mov	ecx, 8000h
		cmp	edi, ecx
		ja	short loc_12271
		mov	cx, di

loc_12271:				; CODE XREF: sub_12247+26j
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
		call	sub_12220
		pop	bp
		pop	ax
		cmp	[byte_24673], 0
		jz	short loc_122B8
		mov	fs, bp
		assume fs:nothing
		mov	cx, ax
		add	cx, 3
		shr	cx, 2
		jz	short loc_122B8
		mov	edx, 80808080h
		xor	si, si

loc_122AE:				; CODE XREF: sub_12247+6Fj
		xor	[fs:si], edx
		add	si, 4
		dec	cx
		jnz	short loc_122AE

loc_122B8:				; CODE XREF: sub_12247+3Dj
					; sub_12247+51j ...
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

loc_122DA:				; CODE XREF: sub_12247+8Bj
		inc	dx
		inc	dx

loc_122DC:				; CODE XREF: sub_12247+91j
		sub	edi, eax
		ja	loc_1224F

loc_122E3:				; CODE XREF: sub_12247+7Fj
		mov	ecx, esi
		clc

locret_122E7:				; CODE XREF: sub_12247+7Bj
		retn
endp		sub_12247


; =============== S U B	R O U T	I N E =======================================


proc		sub_122E8 near		; CODE XREF: sub_11F4E+75p
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
		call	sub_11E8B
		pop	edx
		pop	ecx
		pop	eax
		push	eax
		push	ecx
		push	edx
		mov	ebx, edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	sub_11EC5
		pop	edx
		pop	ecx
		pop	eax
		and	ecx, 3FFFh
		and	edx, 3FFFh
		add	edx, 8000h

loc_1234E:				; CODE XREF: sub_122E8+20j
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

loc_1236C:				; CODE XREF: sub_122E8+9Bj
		mov	eax, [es:di]
		mov	[fs:si], eax
		mov	[dword ptr es:di], 0
		add	si, 4
		add	di, 4
		dec	cx
		jnz	short loc_1236C
		retn
; ---------------------------------------------------------------------------

loc_12386:				; CODE XREF: sub_122E8+4j
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
		call	sub_11E8B
		pop	eax
		pop	ecx
		and	ecx, 3FFFh

loc_123B0:				; CODE XREF: sub_122E8+ADj
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
		call	sub_11EC5
		pop	eax
		pop	ecx
		and	ecx, 3FFFh
		add	cx, 8000h

loc_123EE:				; CODE XREF: sub_122E8+E7j
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
		call	sub_11E8B
		pop	eax
		pop	ecx
		and	ecx, 3FFFh

loc_1242D:				; CODE XREF: sub_122E8+12Aj
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
		call	sub_11EC5
		pop	eax
		pop	ecx
		and	ecx, 3FFFh
		add	cx, 8000h

loc_12466:				; CODE XREF: sub_122E8+15Fj
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

loc_1248B:				; CODE XREF: sub_122E8+1ACj
		movs	[byte ptr es:di], [byte	ptr fs:si]
		cmp	si, dx
		jb	short loc_12493
		mov	si, bp

loc_12493:				; CODE XREF: sub_122E8+1A7j
		dec	cx
		jnz	short loc_1248B
		retn
; ---------------------------------------------------------------------------

loc_12497:				; CODE XREF: sub_122E8+193j
		mov	di, bx
		mov	cx, 200h
		cld
		rep movs [dword	ptr es:di], [dword ptr fs:si]
		retn
endp		sub_122E8

; ---------------------------------------------------------------------------
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
		call	sub_11E8B
		pop	edx
		pop	ecx
		pop	eax
		push	eax
		push	ecx
		push	edx
		mov	ebx, edx
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	sub_11EC5
		pop	edx
		pop	ecx
		pop	eax
		and	ecx, 3FFFh
		and	edx, 3FFFh
		add	edx, 8000h

loc_12508:				; CODE XREF: seg000:24C2j
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

loc_12529:				; CODE XREF: seg000:2538j
		mov	eax, [fs:si]
		mov	[es:di], eax
		add	si, 4
		add	di, 4
		dec	cx
		jnz	short loc_12529
		retn
; ---------------------------------------------------------------------------

loc_1253B:				; CODE XREF: seg000:24A6j
		mov	ecx, [di+20h]
		add	ecx, 800h
		mov	ebx, ecx
		cmp	[word ptr di+32h], 0FFFFh
		jz	short loc_12568
		push	ecx
		push	eax
		shr	ebx, 0Eh
		add	bx, [di+32h]
		call	sub_11E8B
		pop	eax
		pop	ecx
		and	ecx, 3FFFh

loc_12568:				; CODE XREF: seg000:254Dj
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
		call	sub_11EC5
		pop	eax
		pop	ecx
		and	ecx, 3FFFh
		add	cx, 8000h

loc_125A1:				; CODE XREF: seg000:2582j
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

; =============== S U B	R O U T	I N E =======================================


proc		sub_125B9 far		; CODE XREF: start:loc_1907CP
					; start+1BFP
		pushf
		push	ds
		mov	ax, seg003
		mov	ds, ax
		push	cs
		call	near ptr sub_12F48
		push	cs
		call	near ptr sub_125DA
		call	sub_11E37
		mov	ax, [word_2460C]
		call	setmemallocstrat
		call	sub_1424F
		call	initclockfromrtc
		pop	ds
		popf
		retf
endp		sub_125B9

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		sub_125DA far		; CODE XREF: moduleread+7p
					; moduleread+ADp ...
		push	ds
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		call	sub_11E1E
		cmp	[word ptr dword_24640+2], 0
		jz	short loc_125F6
		call	sub_18A28
		mov	[dword_24640], 0

loc_125F6:				; CODE XREF: sub_125DA+Ej
		cmp	[byte_24665], 1
		jnz	short loc_1265B
		test	[sndflags_24622], 4
		jnz	short loc_1263D
		test	[sndflags_24622], 10h
		jnz	short loc_1263D
		mov	di, offset myout
		mov	cx, [word_245D2]

loc_12612:				; CODE XREF: sub_125DA+61j
		push	cx
		test	[byte ptr di+3Ch], 1
		jz	short loc_12636
		cmp	[word ptr di+32h], 0FFFFh
		jnz	short loc_12636
		cmp	[word ptr di+30h], 0
		jz	short loc_12636
		mov	ax, [di+30h]
		push	di
		call	memfree
		pop	di
		and	[byte ptr di+3Ch], 0FEh
		mov	[word ptr di+30h], 0

loc_12636:				; CODE XREF: sub_125DA+3Dj
					; sub_125DA+43j ...
		pop	cx
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_12612

loc_1263D:				; CODE XREF: sub_125DA+28j
					; sub_125DA+2Fj
		mov	di, offset segs_table
		mov	cx, [word_245F2]

loc_12644:				; CODE XREF: sub_125DA+7Fj
		mov	ax, [di]
		or	ax, ax
		jz	short loc_12655
		push	cx
		push	di
		call	memfree
		pop	di
		pop	cx
		mov	[word ptr di], 0

loc_12655:				; CODE XREF: sub_125DA+6Ej
		add	di, 2
		dec	cx
		jnz	short loc_12644

loc_1265B:				; CODE XREF: sub_125DA+21j
		pop	ds
		retf
endp		sub_125DA

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		sub_1265D far		; CODE XREF: sub_19E11+86P sub_19EFDP	...
		mov	ax, seg003
		mov	es, ax
		assume es:seg003
		mov	ax, [es:volume_245FC]
		dec	ax
		mov	cl, al
		mov	si, offset byte_25908
		mov	di, offset asc_246B0 ; "				"
		movzx	bp, [es:sndcard_type]
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
		mov	al, [byte ptr es:word_245F6]
		mov	ah, [byte ptr es:word_245F0]
		retf
endp		sub_1265D


; =============== S U B	R O U T	I N E =======================================


proc		sub_126A9 far		; CODE XREF: sub_19E11+6AP
					; text_init2+225P
		mov	ax, seg003
		mov	es, ax
		mov	di, offset asc_246B0 ; "				"
		mov	si, offset myout
		mov	bl, [byte ptr es:word_245FA]
		mov	bh, [byte ptr es:word_245D2]
		mov	cl, [byte ptr es:word_245D4]
		mov	ch, [es:byte_24617]
		mov	eax, [es:module_type_text]
		retf
endp		sub_126A9


; =============== S U B	R O U T	I N E =======================================


proc		volume_prep far		; CODE XREF: seg001:18BEP seg001:1E76P ...
		push	ds
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		mov	[word_24610], ax
		mov	[word_24612], cx
		test	[sndflags_24622], 4
		jnz	short loc_12702
		push	di
		push	es
		call	sub_11E47
		pop	es
		assume es:nothing
		pop	di
		mov	si, offset byte_25908
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
		call	sub_11E68
		pop	ds
		retf
; ---------------------------------------------------------------------------

loc_12702:				; CODE XREF: volume_prep+12j
		push	di
		push	es
		cmp	[word ptr dword_24640+2], 0
		jnz	short loc_12721
		mov	eax, 800h
		mov	cl, [byte_2462C]
		call	alloc_dma_buf
		mov	[word ptr dword_24640+2], ax
		mov	[word ptr dword_24640],	0

loc_12721:				; CODE XREF: volume_prep+3Bj
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		cld
		mov	si, offset byte_25908
		mov	cx, [word_245D4]

loc_1272D:				; CODE XREF: volume_prep+87j
		pushf
		cli
		mov	dx, [word_24626]
		dec	dx
		mov	al, [si+18h]
		out	dx, al
		inc	dx
		mov	al, 8Ah	; 'Š'
		out	dx, al
		inc	dx
		in	ax, dx
		dec	dx
		and	ah, 1Fh
		shl	eax, 10h
		mov	al, 8Bh	; '‹'
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
		mov	si, offset byte_25908
		mov	ax, [word_245D4]

loc_1275F:				; CODE XREF: volume_prep+C8j
		push	ax
		push	si
		test	[byte ptr si+17h], 1
		jnz	short loc_1276C
		call	sub_12A56
		jmp	short loc_1278F
; ---------------------------------------------------------------------------

loc_1276C:				; CODE XREF: volume_prep+97j
					; volume_prep+A3j
		cmp	[byte_2466E], 1
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
		cmp	[byte_2466E], 1
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
endp		volume_prep


; =============== S U B	R O U T	I N E =======================================


proc		sub_1279A near		; CODE XREF: volume_prep+ACp
		mov	[dma_buf_pointer], eax
		mov	ax, [word_24610]
		xor	ah, ah
		imul	ax, [si+20h]
		mul	[word_24612]
		shrd	ax, dx,	8
		add	ax, 30h	; '0'
		test	[word_24610], 8000h
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
		cmp	[byte_2466E], 1
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
endp		sub_1279A


; =============== S U B	R O U T	I N E =======================================


proc		sub_1281A near		; CODE XREF: volume_prep+BEp
		shl	eax, 10h
		mov	ax, [word_24610]
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


proc		volume_prepare_waves near ; CODE XREF: volume_prep+24p
		test	[byte ptr si+17h], 1
		jz	sub_12A56
		test	[sndflags_24622], 1
		jz	sub_12A56
		push	di
		push	es
		mov	bx, [si+26h]
		mov	eax, [si+4]
		shr	eax, 22
		add	bx, ax
		push	si
		call	sub_11E8B
		pop	si
		mov	eax, [si+4]
		mov	bx, ax
		shr	eax, 12
		cmp	[word ptr si+26h], 0FFFFh
		jz	short loc_12870
		and	eax, 3FFh

loc_12870:				; CODE XREF: volume_prepare_waves+33j
		add	ax, [si+24h]
		mov	fs, ax
		mov	ax, [word_24610]
		xor	ah, ah
		mul	[word ptr si+20h]
		mul	[freq1]
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
		test	[word_24610], 4000h
		jz	short loc_128BB
		cmp	[amplification], 120
		jbe	short loc_128BB
		mov	ax, 100
		push	dx
		mul	bx
		div	[amplification]
		pop	dx
		mov	bx, ax

loc_128BB:				; CODE XREF: volume_prepare_waves+70j
					; volume_prepare_waves+77j
		shl	ebx, 9
		add	bx, offset byte_28308
		inc	bx
		mov	cx, [word_24612]
		test	[word_24610], 8000h
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
endp		volume_prepare_waves


; =============== S U B	R O U T	I N E =======================================


proc		sub_12A56 near		; CODE XREF: volume_prep+99p
					; volume_prepare_waves+4j ...
		cld
		mov	cx, [word_24612]
		xor	ax, ax
		shr	cx, 1
		rep stosw
		adc	cx, cx
		rep stosb
		retn
endp		sub_12A56


; =============== S U B	R O U T	I N E =======================================


proc		sub_12A66 far		; CODE XREF: sub_141DF+1p
					; sub_1422D+14p
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	cx, [word_245D4]
		mov	bx, offset byte_25908

loc_12A73:				; CODE XREF: sub_12A66+19j
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
endp		sub_12A66

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		change_volume far	; CODE XREF: sub_19EFD+17P
					; sub_19EFD+23AP ...
		push	ds
		mov	cx, seg003
		mov	ds, cx
		assume ds:seg003
		cmp	ax, -1
		jz	short loc_12AA9
		mov	[volume_245FC],	ax
		mov	cx, [word_245D4]
		mov	bx, offset byte_25908

loc_12A98:				; CODE XREF: change_volume+24j
		push	bx
		push	cx
		mov	al, [bx+8]
		call	[off_245CC]
		pop	cx
		pop	bx
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_12A98

loc_12AA9:				; CODE XREF: change_volume+9j
		mov	ax, [volume_245FC]
		pop	ds
		assume ds:dseg
		retf
endp		change_volume


; =============== S U B	R O U T	I N E =======================================


proc		change_amplif far	; CODE XREF: s3m_module+84p
					; eff_14020+9p	...
		push	ds
		mov	cx, seg003
		mov	ds, cx
		assume ds:seg003
		cmp	ax, -1
		jz	short loc_12ACE
		mov	[amplification], ax
		mov	[byte_24625], 0
		cmp	ax, 100
		jbe	short loc_12ACB
		mov	[byte_24625], 1

loc_12ACB:				; CODE XREF: change_amplif+16j
		call	sub_13044

loc_12ACE:				; CODE XREF: change_amplif+9j
		mov	ax, [amplification]
		pop	ds
		assume ds:dseg
		retf
endp		change_amplif


; =============== S U B	R O U T	I N E =======================================


proc		sub_12AD3 far		; CODE XREF: sub_19EFD+2AP
					; sub_19EFD+350P ...
		push	ds
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	al, [byte_24672]
		pop	ds
		assume ds:dseg
		retf
endp		sub_12AD3


; =============== S U B	R O U T	I N E =======================================


proc		sub_12ADE far		; CODE XREF: sub_19EFD+357P
					; sub_19EFD+36FP ...
		push	ds
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		mov	[byte_24672], al
		call	sub_12BF8
		and	[byte ptr word_246DA+1], 0FEh
		test	[byte_24672], 10h
		jz	short loc_12AFB
		or	[byte ptr word_246DA+1], 1

loc_12AFB:				; CODE XREF: sub_12ADE+16j
		pop	ds
		retf
endp		sub_12ADE


; =============== S U B	R O U T	I N E =======================================


proc		sub_12AFD far		; CODE XREF: sub_19EFD+1F9P
		push	ds
		mov	bx, seg003
		mov	ds, bx
		movzx	bx, ch
		cmp	bx, [word_245D4]
		jnb	short loc_12B16
		imul	bx, 80
		add	bx, offset byte_25908
		call	eff_13A43

loc_12B16:				; CODE XREF: sub_12AFD+Dj
		pop	ds
		retf
endp		sub_12AFD


; =============== S U B	R O U T	I N E =======================================


proc		sub_12B18 far		; CODE XREF: moduleread:loc_10092p
					; sub_12EBA+5Fp
		push	ax
		push	ds
		push	es
		mov	ax, seg003
		mov	es, ax
		assume es:seg003
		mov	di, offset dword_27BC8
		mov	cx, 8
		cld
		rep movsd
		mov	ds, ax
		mov	[byte_2461C], 0
		mov	[byte_2461D], 0
		mov	si, offset dword_27BC8
		mov	bx, offset byte_25908
		mov	cx, [word_245D4]
		xor	al, al

loc_12B42:				; CODE XREF: sub_12B18+65j
		push	ax
		mov	[bx+18h], al
		mov	al, [si]
		mov	[bx+3Ah], al
		test	[sndflags_24622], 4
		jnz	short loc_12B5F
		cmp	al, 40h	; '@'
		mov	al, 0
		jb	short loc_12B5A
		mov	al, 80h	; '€'

loc_12B5A:				; CODE XREF: sub_12B18+3Ej
		mov	[bx+3Ah], al
		jmp	short loc_12B62
; ---------------------------------------------------------------------------

loc_12B5F:				; CODE XREF: sub_12B18+38j
		call	sub_13A6A

loc_12B62:				; CODE XREF: sub_12B18+45j
		mov	al, [bx+3Ah]
		cmp	al, 0
		jz	short loc_12B71
		inc	[byte_2461D]
		cmp	al, 80h	; '€'
		jz	short loc_12B75

loc_12B71:				; CODE XREF: sub_12B18+4Fj
		inc	[byte_2461C]

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


proc		sub_12B83 far		; CODE XREF: moduleread+8Bp
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
		mov	di, offset byte_25908
		mov	cx, [word_245D4]
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
		mov	[word_245D6], ax
		mov	al, dh
		mov	[word_245D8], ax
		mov	al, bl
		mov	[word_245DA], ax
		test	[sndflags_24622], 4
		jz	short loc_12BEF
		mov	ax, [word_245D6]
		call	sub_18079

loc_12BEF:				; CODE XREF: sub_12B83+64j
		call	sub_13044
		call	sub_12BF8
		pop	ds
		pop	ax
		retf
endp		sub_12B83


; =============== S U B	R O U T	I N E =======================================


proc		sub_12BF8 near		; CODE XREF: sub_12ADE+9p
					; sub_12B83+6Fp
		mov	edx, 3
		mov	eax, 69D80000h
		mov	ecx, 369D800h
		cmp	[byte_2461A], 0
		jnz	short loc_12C3C
		mov	edx, 3
		mov	eax, 61F0E800h
		mov	ecx, 361F0F0h
		test	[byte_24672], 8
		jnz	short loc_12C3C
		mov	edx, 3
		mov	eax, 69E99000h
		mov	ecx, 369E990h

loc_12C3C:				; CODE XREF: sub_12BF8+17j
					; sub_12BF8+30j
		mov	[dword_245C0], ecx
		movzx	edi, [freq1]
		mov	cl, [byte_2461A]
		shl	edi, cl
		div	edi
		mov	[dword_245BC], eax
		test	[sndflags_24622], 4
		jz	short loc_12C86
		movzx	ecx, [byte_24629]
		mov	eax, 385532977
		test	[byte_24672], 8
		jnz	short loc_12C75
		mov	eax, 389081954

loc_12C75:				; CODE XREF: sub_12BF8+75j
		mul	ecx
		mov	cl, 0Ch
		add	cl, [byte_2461A]
		shrd	eax, edx, cl
		mov	[dword_2463C], eax

loc_12C86:				; CODE XREF: sub_12BF8+62j
		mov	di, offset byte_25908
		mov	cx, [word_245D4]
		xor	ax, ax

loc_12C8F:				; CODE XREF: sub_12BF8+9Ej
		mov	[di+3Eh], ax
		add	di, 50h	; 'P'
		dec	cx
		jnz	short loc_12C8F
		retn
endp		sub_12BF8

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		sub_12C99 far		; CODE XREF: sub_19EFD+401P
					; sub_19EFD:loc_1A30DP	...
		push	bx
		push	ds
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		cmp	al, 0FFh
		jz	short loc_12CA7
		mov	[byte_2467F], al

loc_12CA7:				; CODE XREF: sub_12C99+9j
		mov	al, [byte_2467F]
		pop	ds
		assume ds:dseg
		pop	bx
		retf
endp		sub_12C99


; =============== S U B	R O U T	I N E =======================================


proc		sub_12CAD far		; CODE XREF: sub_19EFD+3CCP
					; sub_19EFD+3DCP ...
		push	ds
		push	es
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	es, ax
		assume es:seg003
		mov	si, offset word_246A6
		mov	al, ch
		or	al, 0E0h
		mov	[word_246A9], bx
		mov	[byte_246A8], cl
		mov	[word_246A6], dx
		call	sub_13623
		pop	es
		assume es:nothing
		pop	ds
		retf
endp		sub_12CAD

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		sub_12CCF far		; CODE XREF: sub_19E11+7DP
					; callsubx+3DP
		push	ds
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	al, [sndcard_type]
		mov	dx, [snd_base_port]
		mov	cl, [irq_number]
		mov	ch, [dma_channel]
		mov	ah, [freq_246D7]
		mov	bl, [byte_246D8]
		mov	bh, [byte_246D9]
		mov	bp, [freq1]
		test	[sndflags_24622], 4
		jz	short loc_12CFF
		mov	bp, [freq2]

loc_12CFF:				; CODE XREF: sub_12CCF+2Aj
		mov	si, [word_246DA]
		pop	ds
		assume ds:dseg
		retf
endp		sub_12CCF


; =============== S U B	R O U T	I N E =======================================


proc		sub_12D05 far		; CODE XREF: start-2DP	start+285P
		push	ds
		push	di
		push	es
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	si, offset aDeviceNotIniti ; "Device not initialised!"
		cmp	[byte_24680], 1
		jnz	short loc_12D2E
		movzx	si, [sndcard_type]
		shl	si, 1
		mov	si, [sndcards_table+si]
		mov	di, offset chrin
		call	sub_18C98
		mov	[byte ptr di], 0
		mov	si, offset chrin

loc_12D2E:				; CODE XREF: sub_12D05+10j
		pop	es
		assume es:dseg
		pop	di

loc_12D30:
		call	sub_18D9D
		pop	ds
		assume ds:dseg
		retf
endp		sub_12D05


; =============== S U B	R O U T	I N E =======================================


proc		sub_12D35 far		; CODE XREF: sub_1C1B9+5CP
					; sub_1C1B9+8BP
		push	ax
		push	bx
		push	ds
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		cmp	al, 1
		jz	short loc_12D4E

loc_12D41:
		mov	[cs:byte_14F71], 0
		call	setmemalloc1
		pop	ds
		pop	bx
		pop	ax
		retf
; ---------------------------------------------------------------------------

loc_12D4E:				; CODE XREF: sub_12D35+Aj
		mov	[cs:byte_14F71], 1
		mov	ax, [word_2460C]
		call	setmemallocstrat
		call	initclockfromrtc
		pop	ds
		pop	bx
		pop	ax
		retf
endp		sub_12D35


; =============== S U B	R O U T	I N E =======================================


proc		sub_12D61 near
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	ax, 0FFFFh
		mov	[snd_base_port], ax
		mov	[irq_number], al
		mov	[dma_channel], al
		mov	[byte_246D8], al
		mov	[byte_246D9], al
		mov	[sndcard_type],	0
		call	sub_17EEC
		jnb	short loc_12DA3
		call	sub_183CC
		jb	short loc_12DA3
		mov	[sndcard_type],	3
		cmp	ah, 4
		jnb	short loc_12DA3
		mov	[sndcard_type],	4
		cmp	ah, 3
		jnb	short loc_12DA3
		mov	[sndcard_type],	5
		jmp	short $+2

loc_12DA3:				; CODE XREF: sub_12D61+20j
					; sub_12D61+25j ...
		mov	al, [sndcard_type]
		pop	ds
		retn
endp		sub_12D61

		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


proc		sub_12DA8 far		; CODE XREF: callsubx+24P
		pushf
		cli
		push	ds
		mov	bp, seg003
		mov	ds, bp
		assume ds:seg003
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
		mov	[word_246DA], si
		mov	ax, di
		mov	[byte_246DC], 4Bh ; 'K'
		mov	[off_245CA], offset sub_13177
		mov	[off_245C8], offset loc_13429
		mov	[off_245CC], offset sub_131EF
		mov	[off_245CE], offset loc_131DA
		mov	[byte_24623], 0
		mov	[bit_mode], 8
		mov	[word_245E8], 400h
		mov	[byte_24681], 0
		mov	al, 8
		call	getint_vect
		mov	[word ptr cs:int8addr],	bx
		mov	[word ptr cs:int8addr+2], dx
		push	cs
		call	near ptr sub_11C43
		call	sub_141F6
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
		test	[sndflags_24622], 4
		jnz	short loc_12E55
		mov	ax, 80h	; '€'

loc_12E55:				; CODE XREF: sub_12DA8+A8j
		mov	[byte_2461E], ah
		mov	[byte_2461F], al
		push	cs
		call	near ptr sub_11C43
		mov	al, 0
		test	[byte ptr word_246DA+1], 1
		jz	short loc_12E6B
		or	al, 10h

loc_12E6B:				; CODE XREF: sub_12DA8+BFj
		test	[byte ptr word_246DA], 4
		jz	short loc_12E74
		or	al, 4

loc_12E74:				; CODE XREF: sub_12DA8+C8j
		test	[byte ptr word_246DA], 80h
		jz	short loc_12E7D
		or	al, 8

loc_12E7D:				; CODE XREF: sub_12DA8+D1j
		mov	[byte_24672], al
		mov	ax, 400h
		mov	cl, [byte_24623]
		and	cl, 1
		cmp	[bit_mode], 16
		jnz	short loc_12E9F
		mov	[off_245E0], offset myin
		mov	[off_245E2], offset chrin
		inc	cl

loc_12E9F:				; CODE XREF: sub_12DA8+E7j
		shr	ax, cl
		mov	[word_245E8], ax
		test	[sndflags_24622], 1
		jz	short loc_12EAE
		call	ems_init

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


proc		sub_12EBA far		; CODE XREF: sub_19E11+E3P
		pushf
		cli
		push	ds
		push	es
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		mov	[byte_24669], 0
		mov	[byte_2466A], 0
		mov	[byte_2466B], 0
		mov	[byte_2466C], 0
		mov	[byte_2466D], 0
		mov	[byte_24671], 0
		mov	[byte_2467F], 0
		mov	[word_24600], 0
		mov	[word_24602], 0
		mov	[byte_24620], 0
		mov	[byte_24621], 0
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		mov	di, offset byte_25908
		xor	eax, eax
		mov	cx, 280h
		cld
		rep stosd
		xor	ax, ax
		xor	bx, bx
		push	cs
		call	near ptr sub_12F56
		mov	si, offset dword_27BC8
		push	cs
		call	near ptr sub_12B18
		mov	al, [byte_2467A]
		call	sub_13CF6
		mov	al, [byte_24679]
		call	eff_13CE8
		mov	al, [byte_24679]
		mov	[byte_24668], al
		movzx	ax, [byte_2467A]
		shl	ax, 1
		mov	dl, 5
		div	dl
		mov	[byte_2467B], al
		mov	[byte_2467C], 0
		call	sub_1420F
		pop	es
		pop	ds
		assume ds:dseg
		popf
		retf
endp		sub_12EBA


; =============== S U B	R O U T	I N E =======================================


proc		sub_12F48 far		; CODE XREF: moduleread+3p
					; sub_125B9+8p	...
		pushf
		cli
		push	ds
		mov	ax, seg003
		mov	ds, ax
		assume ds:seg003
		call	sub_1422D
		pop	ds
		assume ds:dseg
		popf
		retf
endp		sub_12F48

		assume ds:seg003

; =============== S U B	R O U T	I N E =======================================


proc		sub_12F56 far		; CODE XREF: sub_12EBA+58p
					; sub_19EFD+167P ...
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
		mov	[byte_24668], 0
		call	sub_135CA

loc_12F78:				; CODE XREF: sub_12F56+18j
		pop	es
		pop	ds
		popf
		retf
endp		sub_12F56


; =============== S U B	R O U T	I N E =======================================


proc		sub_12F7C far		; CODE XREF: sub_19EFD+148P
					; sub_19EFD+174P
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
endp		sub_12F7C


; =============== S U B	R O U T	I N E =======================================


proc		set_timer_int near	; CODE XREF: seg000:4FA1p seg000:502Cp ...
		mov	ebx, 1000h	; bytes
		push	dx		; dx = subrouting offset
		call	memalloc
		pop	dx
		jb	short locret_12FB3
		mov	[word ptr dma_buf_pointer], 0
		mov	[word ptr dma_buf_pointer+2], ax
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
endp		set_timer_int


; =============== S U B	R O U T	I N E =======================================


proc		sub_12FB4 near		; CODE XREF: seg000:covox_cleanp
					; seg000:stereoon_cleanp ...
		mov	dx, [word ptr cs:int8addr+2]
		mov	bx, [word ptr cs:int8addr]
		mov	al, 8
		call	setint_vect
		call	timer_13DD5
		mov	ax, [word ptr dma_buf_pointer+2]
		call	memfree
		retn
endp		sub_12FB4


; =============== S U B	R O U T	I N E =======================================


proc		sub_12FCD near		; CODE XREF: set_covoxp set_stereoonp	...
		call	sub_13017
		pushf
		cli
		mov	dx, 12h
		mov	ax, 34DCh
		div	[freq1]
		call	some_13DC1
		mov	[cs:byte_14F70], 1
		mov	ax, [word_245E4]
		mov	[cs:word_14F6C], ax
		popf
		retn
endp		sub_12FCD


; =============== S U B	R O U T	I N E =======================================


proc		memfill8080 near	; CODE XREF: set_timer_int+18p
					; seg000:covox_sndoffp	...
		pushf
		cli
		xor	ax, ax
		call	some_13DC1
		mov	[cs:byte_14F70], 0
		mov	[cs:word_14F6C], 1
		mov	es, [word ptr dma_buf_pointer+2]
		assume es:nothing
		xor	di, di
		mov	cx, 400h
		mov	eax, 80808080h
		cld
		rep stosd
		popf
		retn
endp		memfill8080


; =============== S U B	R O U T	I N E =======================================


proc		sub_13017 near		; CODE XREF: sub_12FCDp set_proaudp ...
		mov	di, offset myout
		mov	cx, [word_245D2]

loc_1301E:				; CODE XREF: sub_13017+19j
		test	[byte ptr di+3Ch], 8
		jnz	short loc_1302C
		mov	eax, [di+2Ch]
		mov	[di+24h], eax

loc_1302C:				; CODE XREF: sub_13017+Bj
		add	di, 40h	; '@'
		dec	cx
		jnz	short loc_1301E
		mov	[word_24600], 0

loc_13038:				; CODE XREF: sub_13017+2Aj
		call	sub_16C69
		cmp	[word_24600], 800h
		jbe	short loc_13038
		retn
endp		sub_13017


; =============== S U B	R O U T	I N E =======================================


proc		sub_13044 near		; CODE XREF: change_amplif:loc_12ACBp
					; sub_12B83:loc_12BEFp
		mov	al, [byte_2467E]
		cmp	al, 0
		jz	short loc_13080
		cmp	al, 1
		jz	short loc_1305A
		cmp	al, 2
		jz	short loc_1306D
		mov	[byte_2467E], 0
		jmp	short loc_13080
; ---------------------------------------------------------------------------

loc_1305A:				; CODE XREF: sub_13044+9j
		mov	[byte_2467D], 3Fh ; '?'
		mov	[off_2462E], offset table_24798
		mov	[off_24656], offset table_25221
		jmp	short loc_13091
; ---------------------------------------------------------------------------

loc_1306D:				; CODE XREF: sub_13044+Dj
		mov	[byte_2467D], 3Fh ; '?'
		mov	[off_2462E], offset table_24818
		mov	[off_24656], offset table_25261
		jmp	short loc_13091
; ---------------------------------------------------------------------------

loc_13080:				; CODE XREF: sub_13044+5j
					; sub_13044+14j
		mov	[byte_2467D], 40h ; '@'
		mov	[off_2462E], offset table_24716
		mov	[off_24656], offset table_251E0

loc_13091:				; CODE XREF: sub_13044+27j
					; sub_13044+3Aj
		mov	di, offset byte_28308
		movzx	eax, [word_245D6]
		cmp	ax, 2
		ja	short loc_130A2
		mov	ax, 2

loc_130A2:				; CODE XREF: sub_13044+59j
		cmp	[byte_24623], 1
		jnz	short loc_130AE
		shr	ax, 1
		adc	ax, 0

loc_130AE:				; CODE XREF: sub_13044+63j
		movzx	ebp, ax
		mov	si, [off_24656]
		movzx	cx, [byte_2467D]
		inc	cx

loc_130BC:				; CODE XREF: sub_13044+122j
		push	cx
		push	ebp
		movzx	eax, [byte ptr si]
		inc	si
		movzx	edx, [amplification]
		shl	edx, 16
		mul	edx
		mov	ecx, 100
		div	ecx
		xor	edx, edx
		div	ebp
		mov	bp, ax
		shr	eax, 16
		mov	ecx, eax
		cmp	[byte_24625], 1
		jz	short loc_13120
		xor	ax, ax
		xor	dx, dx
		mov	bl, 80h	; '€'

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
		mov	bl, 80h	; '€'

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
		mov	bl, 80h	; '€'

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
		mov	bl, 80h	; '€'

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


proc		sub_13177 near		; CODE XREF: seg000:3473p
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

loc_131B3:				; CODE XREF: sub_13177+Cj sub_13215+Cj
		movzx	edi, ax
		xor	edx, edx
		mov	cl, [byte_2461A]
		shl	edi, cl
		xor	edx, edx
		mov	eax, [dword_245C0]
		div	edi
		mov	[bx+1Eh], ax
		retn
endp		sub_13177

; ---------------------------------------------------------------------------

locret_131CF:				; CODE XREF: seg000:31DEj seg000:3276j
		retn
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_131EF

loc_131D0:				; CODE XREF: sub_131EF+4j sub_132A9+4j ...
		xor	ah, ah
		imul	ax, [volume_245FC]
		xor	al, al
		retn
; END OF FUNCTION CHUNK	FOR sub_131EF
; ---------------------------------------------------------------------------

loc_131DA:				; CODE XREF: seg000:349Dj
					; DATA XREF: sub_12DA8+4Ao
		cmp	[byte ptr bx+1Dh], 1
		jz	short locret_131CF
		test	[byte ptr bx+17h], 1
		jz	short locret_131EE
		and	[byte ptr bx+17h], 0FEh
		mov	[byte ptr bx+35h], 0

locret_131EE:				; CODE XREF: seg000:31E4j
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_131EF near		; CODE XREF: seg000:3478p seg000:347Ep
					; DATA XREF: ...

; FUNCTION CHUNK AT 31D0 SIZE 0000000A BYTES

		cmp	[byte ptr bx+1Dh], 1
		jz	short loc_131D0
		and	[byte ptr bx+3Dh], 0BFh
		cmp	al, [byte_2467D]
		jbe	short loc_13202
		mov	al, [byte_2467D]

loc_13202:				; CODE XREF: sub_131EF+Ej
		xor	ah, ah
		mov	[bx+22h], al
		mul	[volume_245FC]
		mov	al, [bx+23h]
		mov	[bx+36h], ax
		mov	[bx+23h], ah
		retn
endp		sub_131EF


; =============== S U B	R O U T	I N E =======================================


proc		sub_13215 near		; CODE XREF: seg000:358Ap
					; DATA XREF: seg000:4306o
		or	ax, ax
		jz	short locret_13271
		or	[byte ptr bx+3Dh], 4
		cmp	[byte ptr bx+1Dh], 1
		jz	short loc_131B3
		cmp	ax, [bx+3Eh]
		jz	short locret_13271
		mov	[bx+3Eh], ax
		movzx	edi, ax
		xor	edx, edx
		mov	eax, [dword_245BC]
		div	edi
		mov	[bx+20h], ax
		xor	edx, edx
		mov	eax, [dword_2463C]
		div	edi
		mov	cl, [byte_2461A]
		shl	edi, cl
		mov	cx, ax
		xor	edx, edx
		mov	eax, [dword_245C0]
		div	edi
		mov	[bx+1Eh], ax
		pushf
		cli
		mov	dx, [word_24626]
		dec	dx
		mov	al, [bx+18h]
		out	dx, al
		inc	dx
		mov	al, 1
		out	dx, al
		inc	dx
		mov	ax, cx
		out	dx, ax
		dec	dx
		popf

locret_13271:				; CODE XREF: sub_13215+2j
					; sub_13215+11j
		retn
endp		sub_13215

; ---------------------------------------------------------------------------

loc_13272:				; CODE XREF: seg000:35C5j
					; DATA XREF: seg000:4318o
		cmp	[byte ptr bx+1Dh], 1
		jz	locret_131CF
		and	[byte ptr bx+17h], 0FEh
		xor	al, al
		call	sub_13363
		mov	dx, [word_24626]
		dec	dx
		mov	al, [bx+18h]
		pushf
		cli
		out	dx, al
		inc	dx
		mov	al, 0
		out	dx, al
		add	dl, 2
		mov	al, 3
		out	dx, al
		sub	dl, 2
		mov	al, 9
		out	dx, al
		inc	dx
		xor	ax, ax
		out	dx, ax
		dec	dx
		mov	[byte ptr bx+35h], 0
		popf
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_132A9 near		; CODE XREF: seg000:35BCp
					; DATA XREF: seg000:4312o
		cmp	[byte ptr bx+1Dh], 1
		jz	loc_131D0
		and	[byte ptr bx+3Dh], 0BFh
		test	[byte ptr bx+17h], 4
		jz	locret_13355
		cmp	al, [byte_2467D]
		jbe	short loc_132C6
		mov	al, [byte_2467D]

loc_132C6:				; CODE XREF: sub_132A9+18j
		xor	ah, ah
		mov	[bx+22h], al
		mul	[volume_245FC]
		mov	[bx+23h], ah
		push	cx
		push	di
		movzx	di, ah
		shl	di, 1
		add	di, [off_2462E]
		mov	cx, [di]
		mov	ax, cx
		cmp	ax, 8000h
		ja	short loc_132E8
		xor	ax, ax

loc_132E8:				; CODE XREF: sub_132A9+3Bj
		mov	[bx+36h], ax
		pushf
		mov	dx, [word_24626]
		dec	dx
		mov	al, [bx+18h]
		out	dx, al
		inc	dx
		mov	al, 0Dh
		out	dx, al
		add	dl, 2
		mov	al, 3
		out	dx, al
		sub	dl, 2
		mov	al, 89h	; '‰'
		out	dx, al
		inc	dx
		in	ax, dx
		dec	dx
		or	ah, 80h
		cmp	ah, ch
		jz	short loc_13356
		mov	cl, 20h	; ' '
		jb	short loc_13318
		xchg	ah, ch
		or	cl, 40h

loc_13318:				; CODE XREF: sub_132A9+68j
		mov	di, cx
		sub	di, ax
		cmp	di, 300h
		jbe	short loc_13356
		mov	al, 7
		out	dx, al
		add	dl, 2
		mov	al, ah
		out	dx, al
		sub	dl, 2
		mov	al, 8
		out	dx, al
		add	dl, 2
		mov	al, ch
		out	dx, al
		sub	dl, 2
		mov	al, 6
		out	dx, al
		add	dl, 2
		mov	al, 30h	; '0'
		out	dx, al
		sub	dl, 2
		mov	al, 0Dh
		out	dx, al
		add	dl, 2
		mov	al, cl
		out	dx, al
		sub	dl, 2
		popf
		pop	di
		pop	cx

locret_13355:				; CODE XREF: sub_132A9+10j
		retn
; ---------------------------------------------------------------------------

loc_13356:				; CODE XREF: sub_132A9+64j
					; sub_132A9+77j ...
		mov	al, 9
		out	dx, al
		inc	dx
		mov	ax, [bx+36h]
		out	dx, ax
		dec	dx
		popf
		pop	di
		pop	cx
		retn
endp		sub_132A9


; =============== S U B	R O U T	I N E =======================================


proc		sub_13363 near		; CODE XREF: seg000:3280p seg000:34ACp
		cmp	[byte ptr bx+1Dh], 1
		jz	loc_131D0
		and	[byte ptr bx+3Dh], 0BFh
		test	[byte ptr bx+17h], 4
		jz	locret_13428
		cmp	al, [byte_2467D]
		jbe	short loc_13380
		mov	al, [byte_2467D]

loc_13380:				; CODE XREF: sub_13363+18j
		xor	ah, ah
		mov	[bx+22h], al
		mul	[volume_245FC]
		mov	[bx+23h], ah
		push	cx
		push	di
		movzx	di, ah
		shl	di, 1
		add	di, [off_2462E]
		mov	cx, [di]
		mov	ax, cx
		cmp	ax, 8000h
		ja	short loc_133A2
		xor	ax, ax

loc_133A2:				; CODE XREF: sub_13363+3Bj
		mov	[bx+36h], ax
		pushf
		mov	dx, [word_24626]
		dec	dx
		mov	al, [bx+18h]
		out	dx, al
		inc	dx
		mov	al, 0Dh
		out	dx, al
		add	dl, 2
		mov	al, 3
		out	dx, al
		sub	dl, 2
		mov	al, 89h	; '‰'
		out	dx, al
		inc	dx
		in	ax, dx
		dec	dx
		or	ah, 80h
		cmp	ah, ch
		jz	short loc_13356
		mov	cl, 0
		jb	short loc_133D2
		xchg	ah, ch
		or	cl, 40h

loc_133D2:				; CODE XREF: sub_13363+68j
		mov	di, cx
		sub	di, ax
		cmp	di, 300h
		jbe	loc_13356
		mov	al, 7
		out	dx, al
		add	dl, 2
		mov	al, ah
		out	dx, al
		sub	dl, 2
		mov	al, 8
		out	dx, al
		add	dl, 2
		mov	al, ch
		out	dx, al
		sub	dl, 2
		mov	al, 6
		out	dx, al
		add	dl, 2
		mov	al, 30h	; '0'
		out	dx, al
		sub	dl, 2
		mov	al, 0Dh
		out	dx, al
		add	dl, 2
		mov	al, cl
		out	dx, al
		sub	dl, 2

loc_1340E:				; CODE XREF: sub_13363+B7j
		mov	al, 8Dh	; ''
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		shr	al, 1
		jnb	short loc_1340E
		mov	al, 9
		out	dx, al
		inc	dx
		mov	ax, [bx+36h]
		out	dx, ax
		dec	dx
		popf
		pop	di
		pop	cx

locret_13428:				; CODE XREF: sub_13363+10j
		retn
endp		sub_13363

; ---------------------------------------------------------------------------

loc_13429:				; DATA XREF: sub_12DA8+3Eo
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
		add	di, offset myout
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

loc_13471:				; CODE XREF: seg000:3435j
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

locret_13498:				; CODE XREF: seg000:342Dj
		retn
; ---------------------------------------------------------------------------

loc_13499:				; CODE XREF: seg000:3485j
		test	[byte ptr bx+17h], 1
		jnz	loc_131DA
		retn
; ---------------------------------------------------------------------------

loc_134A2:				; DATA XREF: seg000:430Co
		test	[byte ptr bx+17h], 4
		jz	locret_135BF
		xor	al, al
		call	sub_13363
		pushf
		cli
		mov	dx, [word_24626]
		dec	dx
		mov	al, [bx+18h]
		out	dx, al
		inc	dx
		mov	al, 0
		out	dx, al
		add	dl, 2
		mov	al, 3
		out	dx, al
		sub	dl, 2
		and	[byte ptr bx+17h], 0FEh
		mov	al, [bx+2]
		cmp	al, [bx+3]
		jz	loc_1355F
		mov	[bx+3],	al
		dec	al
		xor	ah, ah
		shl	ax, 6
		mov	di, ax
		add	di, offset myout
		mov	eax, [bx+28h]
		mov	[bx+40h], eax
		mov	eax, [bx+2Ch]
		mov	[bx+44h], eax
		mov	eax, [bx+30h]
		mov	[bx+48h], eax
		mov	al, [di+3Ch]
		mov	[bx+19h], al
		movzx	ebp, [word ptr di+34h]
		mov	[bx+24h], bp
		shl	ebp, 0Dh
		mov	edi, [bx+48h]
		test	[byte ptr bx+19h], 8
		jz	short loc_13544
		mov	edi, [bx+40h]
		shl	edi, 9
		add	edi, ebp
		mov	al, 3
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		dec	dx
		shr	edi, 10h
		mov	al, 2
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		dec	dx
		mov	edi, [bx+48h]
		test	[byte ptr bx+19h], 4
		jnz	short loc_13544
		inc	edi

loc_13544:				; CODE XREF: seg000:3517j seg000:3540j
		shl	edi, 9
		add	edi, ebp
		mov	al, 5
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		dec	dx
		shr	edi, 10h
		mov	al, 4
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		dec	dx

loc_1355F:				; CODE XREF: seg000:34D1j
		movzx	edi, [word ptr bx+24h]
		shl	edi, 0Dh
		movzx	eax, [word ptr bx+4Ch]
		shl	eax, 9
		add	edi, eax
		mov	al, 0Bh
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		dec	dx
		shr	edi, 10h
		mov	al, 0Ah
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		dec	dx
		mov	ax, [bx]
		call	sub_13215
		test	[byte ptr bx+17h], 2
		jnz	short loc_135C0
		or	[byte ptr bx+17h], 1
		mov	dx, [word_24626]
		mov	ah, [bx+19h]
		and	ah, 1Ch
		mov	al, ah
		and	al, 8
		shl	al, 2
		xor	al, 20h
		or	ah, al
		mov	al, 0
		out	dx, al
		add	dl, 2
		mov	al, ah
		out	dx, al
		sub	dl, 2
		popf
		mov	al, [bx+8]
		call	sub_132A9

locret_135BF:				; CODE XREF: seg000:34A6j
		retn
; ---------------------------------------------------------------------------

loc_135C0:				; CODE XREF: seg000:3591j
		popf
		test	[byte ptr bx+17h], 1
		jnz	loc_13272
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_135CA near		; CODE XREF: sub_12F56+1Fp
					; sub_140B6+3Cp ...
		mov	bx, offset byte_25908
		mov	cx, [word_245D4]
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
		mov	[word ptr pointer_245B4], si
		mov	bx, offset byte_25908
		mov	cx, [word_245D4]

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
		cmp	ax, [word_245D4]
		jnb	loc_137BE
		shl	ax, 4
		mov	bx, ax
		shl	ax, 2
		add	bx, ax
		add	bx, offset byte_25908
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
		cmp	ax, [word_245D2]
		ja	loc_13718
		dec	ax
		shl	ax, 6
		mov	di, ax
		add	di, offset myout
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
		add	ax, offset word_24998
		mov	[bx+38h], ax
		mov	ax, [freq_245DE]
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
		cmp	dl, 0FEh ; 'þ'
		jz	loc_137CE
		cmp	dl, 0FFh
		jz	sub_137D5
		mov	[bx+35h], dl
		or	[byte ptr bx+3Dh], 8
		test	[sndflags_24622], 10h
		jnz	short loc_13742
		test	[byte ptr bx+17h], 4
		jz	loc_137CE

loc_13742:				; CODE XREF: sub_13623+115j
		mov	al, [bx+35h]
		call	sub_13826
		xchg	ax, [bx]
		test	[byte ptr bx+3Dh], 80h
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
		ja	eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		jmp	[cs:off_18FA2+di]
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
		jmp	[off_245CE]
endp		sub_13623 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_137D5 near		; CODE XREF: sub_13623+5Aj
					; sub_13623+F7j ...
		test	[byte ptr bx+3Dh], 40h
		jnz	short loc_137F0
		movzx	di, [byte ptr bx+0Ah]
		cmp	di, 32
		ja	eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		jmp	[cs:off_18F60+di]
; ---------------------------------------------------------------------------

loc_137F0:				; CODE XREF: sub_137D5+4j
		movzx	di, [byte ptr bx+0Ah]
		cmp	di, 32
		ja	eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		call	[cs:off_18F60+di]
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
		ja	short eff_nullsub
		shl	di, 1
		mov	al, [bx+0Bh]
		jmp	[cs:off_18FE4+di]
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
		cmp	[byte_2461A], 0
		jnz	short loc_1386C
		mov	ch, cl
		xor	cl, cl
		xor	ax, ax
		or	ch, ch
		jz	short loc_13863
		mov	ax, 24
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
		sub	di, offset word_246DE

loc_1386C:				; CODE XREF: sub_13826+13j
		mov	ax, [word_246DE+di]
		shr	ax, cl
		mov	cx, [bx+14h]
		jcxz	short locret_1387D
		mul	[freq_245DE]
		div	cx

locret_1387D:				; CODE XREF: sub_13826+4Fj
		retn
endp		sub_13826


; =============== S U B	R O U T	I N E =======================================


proc		eff_nullsub near	; CODE XREF: sub_13623+18Dj
					; sub_13623+196j ...
		retn
endp		eff_nullsub


; =============== S U B	R O U T	I N E =======================================


proc		eff_1387F near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[byte_24668], 0
		jnz	short eff_nullsub
endp		eff_1387F ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		eff_13886 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		shl	ax, 4

loc_1388B:				; CODE XREF: eff_13DE5+5j
		sub	[bx], ax
		cmp	[word ptr bx], 0A0h ; ' '
		jge	short loc_13897
		mov	[word ptr bx], 0A0h ; ' '

loc_13897:				; CODE XREF: eff_13886+Bj
		mov	ax, [bx]
		jmp	[off_245CA]
endp		eff_13886


; =============== S U B	R O U T	I N E =======================================


proc		eff_1389D near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[byte_24668], 0
		jnz	short eff_nullsub
endp		eff_1389D ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		eff_138A4 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		shl	ax, 4

loc_138A9:				; CODE XREF: eff_13DEF+5j
		add	[bx], ax
		jb	short loc_138B3
		cmp	[word ptr bx], 13696
		jbe	short loc_138B7

loc_138B3:				; CODE XREF: eff_138A4+7j
		mov	[word ptr bx], 13696

loc_138B7:				; CODE XREF: eff_138A4+Dj
		mov	ax, [bx]
		jmp	[off_245CA]
endp		eff_138A4

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


proc		eff_138D2 near		; CODE XREF: sub_13623+196j
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
		mov	[word ptr bx+10h], 0
		and	[byte ptr bx+17h], 0EFh
		jmp	[off_245CA]
; ---------------------------------------------------------------------------

loc_1390B:				; CODE XREF: eff_138D2+20j
					; eff_138D2+28j
		test	[byte ptr bx+17h], 20h
		jnz	short loc_13917
		mov	ax, [bx]
		jmp	[off_245CA]
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
		jmp	[off_245CA]
endp		eff_138D2


; =============== S U B	R O U T	I N E =======================================


proc		eff_1392F near		; CODE XREF: sub_13623+196j
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
		test	[byte ptr bx+0Dh], 80h
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
		mov	ch, [byte_24672]
		and	ch, 1
		add	cl, ch
		shr	ax, cl
		test	[byte ptr bx+0Dh], 80h
		jz	short loc_1399D
		neg	ax

loc_1399D:				; CODE XREF: eff_1392F+6Aj
		add	ax, [bx]
		shr	dh, 2
		and	dh, 3Ch
		add	[bx+0Dh], dh
		jmp	[off_245CA]
endp		eff_1392F


; =============== S U B	R O U T	I N E =======================================


proc		eff_139AC near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	eff_13AD7
		jmp	loc_138DE
endp		eff_139AC


; =============== S U B	R O U T	I N E =======================================


proc		eff_139B2 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	eff_13AD7
		mov	cl, 3
		jmp	short loc_13950
endp		eff_139B2


; =============== S U B	R O U T	I N E =======================================


proc		eff_139B9 near		; CODE XREF: sub_13623+196j
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
		test	[byte ptr bx+0Fh], 80h
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
		test	[byte ptr bx+0Fh], 80h
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
		jmp	[off_245CC]
endp		eff_139B9


; =============== S U B	R O U T	I N E =======================================


proc		eff_13A43 near		; CODE XREF: sub_12AFD+16p
					; sub_13623+196j ...
		cmp	al, 0A4h ; '¤'
		jz	short loc_13A5B
		cmp	al, 0A5h ; '¥'
		jz	short loc_13A60
		cmp	al, 0A6h ; '¦'
		jz	short loc_13A65
		cmp	al, 80h	; '€'
		ja	short locret_13A5A
		test	[sndflags_24622], 4
		jnz	short sub_13A6A

locret_13A5A:				; CODE XREF: eff_13A43+Ej
		retn
; ---------------------------------------------------------------------------

loc_13A5B:				; CODE XREF: eff_13A43+2j
		or	[byte ptr bx+17h], 80h
		retn
; ---------------------------------------------------------------------------

loc_13A60:				; CODE XREF: eff_13A43+6j
		and	[byte ptr bx+17h], 7Fh
		retn
; ---------------------------------------------------------------------------

loc_13A65:				; CODE XREF: eff_13A43+Aj
		xor	[byte ptr bx+17h], 80h
		retn
endp		eff_13A43


; =============== S U B	R O U T	I N E =======================================


proc		sub_13A6A near		; CODE XREF: sub_12B18:loc_12B5Fp
					; eff_13A43+15j
		mov	[bx+3Ah], al
		or	al, al
		jz	short loc_13A78
		dec	al
		shr	al, 3
		and	al, 0Fh

loc_13A78:				; CODE XREF: sub_13A6A+5j
		mov	ah, al
		mov	dx, [word_24626]
		dec	dx
		mov	al, [bx+18h]
		pushf
		cli
		out	dx, al
		inc	dx
		mov	al, 0Ch
		out	dx, al
		add	dl, 2
		mov	al, ah
		out	dx, al
		sub	dl, 2
		popf
		retn
endp		sub_13A6A


; =============== S U B	R O U T	I N E =======================================


proc		eff_13A94 near		; CODE XREF: sub_137D5+16j
					; sub_137D5+2Bp ...
		or	al, al
		jz	short loc_13A9B
		mov	[bx+16h], al

loc_13A9B:				; CODE XREF: eff_13A94+2j
		movzx	eax, [byte ptr bx+16h]
		shl	eax, 8
		cmp	eax, [bx+30h]
		ja	short loc_13AAE
		mov	[bx+4Ch], ax
		retn
; ---------------------------------------------------------------------------

loc_13AAE:				; CODE XREF: eff_13A94+14j
		cmp	[byte_2461A], 0
		jnz	short loc_13AC6
		call	[off_245CE]
		and	[byte ptr bx+17h], 0FBh
		or	[byte ptr bx+17h], 40h
		mov	[byte ptr bx+3], 0
		retn
; ---------------------------------------------------------------------------

loc_13AC6:				; CODE XREF: eff_13A94+1Fj
		mov	eax, [bx+30h]
		mov	[bx+4Ch], ax
		retn
endp		eff_13A94

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13ACE:				; CODE XREF: sub_13623+144j
		mov	al, [bx+0Bh]
		call	eff_13A94
		jmp	loc_13791
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


proc		eff_13AD7 near		; CODE XREF: sub_13623+196j
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
		jmp	[off_245CC]
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
		jmp	[off_245CC]
endp		eff_13AD7


; =============== S U B	R O U T	I N E =======================================


proc		eff_13B06 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		dec	ax
		mov	[word_245F0], ax
		inc	ax
		test	[byte_24672], 4
		jnz	short loc_13B5B
		bt	[word ptr byte_282E8], ax
		jnb	short loc_13B5B
		mov	cx, [word_245FA]
		add	cx, 7
		shr	cx, 3
		jz	short loc_13B34
		xor	di, di

loc_13B29:				; CODE XREF: eff_13B06+2Cj
		cmp	[byte_282E8+di], 0FFh
		jnz	short loc_13B3E
		inc	di
		dec	cx
		jnz	short loc_13B29

loc_13B34:				; CODE XREF: eff_13B06+1Fj
					; eff_13B06+4Ej
		push	bx
		push	si
		push	es
		call	sub_141DF
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
		mov	[byte_24669], 0
		mov	[byte_2466A], 1
		retn
endp		eff_13B06

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


proc		eff_13B78 near		; CODE XREF: sub_137D5+16j
					; sub_137D5+2Bp ...
		cmp	al, [byte_2467D]
		jbe	short loc_13B81
		mov	al, [byte_2467D]

loc_13B81:				; CODE XREF: eff_13B78+4j
		mov	[bx+8],	al
		jmp	[off_245CC]
endp		eff_13B78


; =============== S U B	R O U T	I N E =======================================


proc		eff_13B88 near		; CODE XREF: sub_13623+196j
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
		mov	[byte_2466A], 1
		retn
endp		eff_13B88


; =============== S U B	R O U T	I N E =======================================


proc		eff_13BA3 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	di, ax
		shr	di, 3
		and	di, 1Eh
		and	al, 0Fh
		jmp	[cs:off_19026+di]
endp		eff_13BA3


; =============== S U B	R O U T	I N E =======================================


proc		eff_13BB2 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13BBB
		or	[byte ptr bx+17h], 20h
		retn
; ---------------------------------------------------------------------------

loc_13BBB:				; CODE XREF: eff_13BB2+2j
		and	[byte ptr bx+17h], 0DFh
		retn
endp		eff_13BB2


; =============== S U B	R O U T	I N E =======================================


proc		eff_13BC0 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	[byte ptr bx+9], 0F0h
		or	[bx+9],	al
		retn
endp		eff_13BC0


; =============== S U B	R O U T	I N E =======================================


proc		eff_13BC8 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	ax, 0Fh
		mov	di, ax
		cmp	[byte_2461A], 0
		jnz	short loc_13BE7
		shl	di, 3
		mov	ax, di
		neg	ax
		shl	di, 4
		add	ax, di
		add	ax, offset word_24998
		mov	[bx+38h], ax
		retn
; ---------------------------------------------------------------------------

loc_13BE7:				; CODE XREF: eff_13BC8+Aj
		shl	di, 1
		mov	ax, [table_246F6+di]
		mov	[bx+14h], dx
		retn
endp		eff_13BC8

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


proc		eff_13C02 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[byte_24668], 0
		jnz	locret_13CF4
		or	al, al
		jz	short loc_13C2D
		cmp	[byte ptr bx+3Ch], 0
		jnz	short loc_13C1A
		inc	al
		mov	[bx+3Ch], al

loc_13C1A:				; CODE XREF: eff_13C02+11j
		dec	[byte ptr bx+3Ch]
		jz	locret_13CF4
		mov	al, [bx+3Bh]
		mov	[byte_24669], al
		mov	[byte_2466B], 1
		retn
; ---------------------------------------------------------------------------

loc_13C2D:				; CODE XREF: eff_13C02+Bj
		mov	ax, [word_245F6]
		mov	[bx+3Bh], al
		retn
endp		eff_13C02


; =============== S U B	R O U T	I N E =======================================


proc		eff_13C34 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	[byte ptr bx+9], 0Fh
		shl	al, 4
		or	[bx+9],	al
		retn
endp		eff_13C34


; =============== S U B	R O U T	I N E =======================================


proc		eff_13C3F near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[byte_24668], 0
		jz	short loc_13C47
		retn
; ---------------------------------------------------------------------------

loc_13C47:				; CODE XREF: eff_13C3F+5j
		mov	di, ax
		and	di, 0Fh
		mov	al, [cs:byte_13C54+di]
		jmp	eff_13A43
endp		eff_13C3F

; ---------------------------------------------------------------------------
byte_13C54	db 0,9,12h,1Bh,24h,2Dh,36h,40h,40h,4Ah,53h,5Ch,65h,6Eh
					; DATA XREF: seg000:0B18r
					; far_module+55r ...
		db 77h,80h

; =============== S U B	R O U T	I N E =======================================


proc		eff_13C64 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	locret_13CF4
		cmp	[byte_24668], 0
		jnz	short loc_13C77
		test	[byte ptr bx+3Dh], 8
		jnz	short locret_13CF4

loc_13C77:				; CODE XREF: eff_13C64+Bj
		mov	dl, al
		movzx	ax, [byte_24668]
		div	dl
		or	ah, ah
		jnz	short locret_13CF4
		jmp	[off_245C8]
endp		eff_13C64


; =============== S U B	R O U T	I N E =======================================


proc		eff_13C88 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, [bx+8]
		cmp	[byte_24668], 0
		jz	loc_13AF2
		retn
endp		eff_13C88


; =============== S U B	R O U T	I N E =======================================


proc		eff_13C95 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	dl, [bx+8]
		cmp	[byte_24668], 0
		jz	loc_13AE0
		retn
endp		eff_13C95


; =============== S U B	R O U T	I N E =======================================


proc		eff_13CA2 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	al, [byte_24668]
		jnz	short locret_13CF4
		xor	al, al
		jmp	[off_245CC]
endp		eff_13CA2

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13623

loc_13CAE:				; CODE XREF: sub_13623+158j
		mov	al, [bx+0Bh]
		and	al, 0Fh
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


proc		eff_13CB3 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	al, [byte_24668]
		jnz	short locret_13CF4
		cmp	[word ptr bx], 0
		jz	short locret_13CF4
		mov	[byte ptr bx+0Ah], 0
		mov	[byte ptr bx+0Bh], 0
		jmp	loc_13791
endp		eff_13CB3


; =============== S U B	R O U T	I N E =======================================


proc		eff_13CC9 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		cmp	[byte_24668], 0
		jnz	short locret_13CF4
		cmp	[byte_2466D], 0
		jnz	short locret_13CF4
		inc	al
		mov	[byte_2466C], al
		retn
endp		eff_13CC9


; =============== S U B	R O U T	I N E =======================================


proc		eff_13CDD near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		test	[byte_24672], 2
		jnz	short eff_13CE8
		cmp	al, 20h	; ' '
		ja	short sub_13CF6
endp		eff_13CDD ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		eff_13CE8 near		; CODE XREF: sub_12EBA+6Bp
					; sub_13623+196j ...
		or	al, al
		jz	short locret_13CF5
		mov	[byte_24667], al
		mov	[byte_24668], 0

locret_13CF4:				; CODE XREF: eff_138D2+11j
					; eff_13C02+5j	...
		retn
; ---------------------------------------------------------------------------

locret_13CF5:				; CODE XREF: eff_13CE8+2j
		retn
endp		eff_13CE8


; =============== S U B	R O U T	I N E =======================================


proc		sub_13CF6 near		; CODE XREF: sub_12EBA+65p
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
		test	[sndflags_24622], 4
		jnz	short loc_13D4B
		test	[sndflags_24622], 10h
		jnz	settimer
		shl	cx, 1
		mov	ax, 5
		mul	[freq1]
		div	cx
		xor	dx, dx
		div	[word_245E8]
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
		mov	dx, [word_24626]
		sub	dx, 0FBh ; 'û'
		mov	al, 4
		out	dx, al
		inc	dx
		mov	al, 80h	; '€'
		out	dx, al
		xor	al, al
		out	dx, al
		add	dx, 0FAh ; 'ú'
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
		sub	dx, 0FDh ; 'ý'
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
		inc	[byte_24618]
		jmp	short loc_13D9A
; END OF FUNCTION CHUNK	FOR sub_13D95

; =============== S U B	R O U T	I N E =======================================


proc		sub_13D95 near		; CODE XREF: sub_13CF6:loc_13D4Bp

; FUNCTION CHUNK AT 3D8D SIZE 00000008 BYTES

		mov	[byte_24618], 1

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
endp		sub_13D95

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_13CF6

settimer:				; CODE XREF: sub_13CF6+21j
		xor	ax, ax
		cmp	cx, 45
		jbe	short some_13DC1
		mov	dx, 2Dh	; '-'
		mov	ax, 8426h
		div	cx
		jmp	short $+2
; END OF FUNCTION CHUNK	FOR sub_13CF6

; =============== S U B	R O U T	I N E =======================================


proc		some_13DC1 near		; CODE XREF: sub_12FCD+Fp
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
endp		some_13DC1


; =============== S U B	R O U T	I N E =======================================


proc		timer_13DD5 near	; CODE XREF: sub_12FB4+Fp seg000:53B3p
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
endp		timer_13DD5


; =============== S U B	R O U T	I N E =======================================


proc		eff_13DE5 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	sub_14087
		or	ax, ax
		jnz	loc_1388B
		retn
endp		eff_13DE5


; =============== S U B	R O U T	I N E =======================================


proc		eff_13DEF near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	sub_14087
		or	ax, ax
		jnz	loc_138A9
		retn
endp		eff_13DEF

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


proc		eff_13E1E near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		or	al, al
		jz	short loc_13E2A
		xor	ah, ah
		shl	ax, 2
		mov	[bx+12h], ax

loc_13E2A:				; CODE XREF: eff_13E1E+2j eff_13E7F+3j
		jmp	loc_138DE
endp		eff_13E1E


; =============== S U B	R O U T	I N E =======================================


proc		eff_13E2D near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		mov	cl, 5
		jmp	loc_13931
endp		eff_13E2D


; =============== S U B	R O U T	I N E =======================================


proc		eff_13E32 near		; CODE XREF: sub_13623+196j
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
		cmp	[byte_24668], 0
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
		cmp	[byte_24668], 0
		jz	loc_13ADE
		retn
endp		eff_13E32


; =============== S U B	R O U T	I N E =======================================


proc		eff_13E7F near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	eff_13E32
		jmp	short loc_13E2A
endp		eff_13E7F


; =============== S U B	R O U T	I N E =======================================


proc		eff_13E84 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	eff_13E32
		mov	cl, 5
		jmp	loc_13950
endp		eff_13E84


; =============== S U B	R O U T	I N E =======================================


proc		eff_13E8C near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		call	sub_13E9B
		mov	[byte_24667], ah
		mov	[byte_24668], 0
		jmp	sub_13CF6
endp		eff_13E8C


; =============== S U B	R O U T	I N E =======================================


proc		sub_13E9B near		; CODE XREF: seg000:0419p eff_13E8Cp
		movzx	di, al
		mov	dx, di
		and	dl, 0Fh
		shr	di, 4
		mov	ax, dx
		mul	[cs:byte_13EC3+di]
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
byte_13EC3	db 140,50,25,15,10,7,6,4,3,3,2,2,2,2,1,1 ; DATA	XREF: sub_13E9B+Dr
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
		mov	[byte ptr bx+0Bh], 0
		or	[byte ptr bx+17h], 10h
		mov	ax, [bx]
		mov	[bx+10h], ax
		mov	ax, [word_245DC]
		mov	[bx], ax
		jmp	sub_137D5
; END OF FUNCTION CHUNK	FOR sub_13623

; =============== S U B	R O U T	I N E =======================================


proc		nullsub_2 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		retn
endp		nullsub_2


; =============== S U B	R O U T	I N E =======================================


proc		eff_13F05 near		; CODE XREF: sub_13623+196j
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
		movzx	ax, [byte_24668]
		div	cl
		cmp	ah, dl
		jb	short loc_13F34
		xor	al, al
		jmp	[off_245CC]
; ---------------------------------------------------------------------------

loc_13F34:				; CODE XREF: eff_13F05+27j
		mov	al, [bx+8]
		jmp	[off_245CC]
endp		eff_13F05


; =============== S U B	R O U T	I N E =======================================


proc		eff_13F3B near		; CODE XREF: sub_13623+196j
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
		mov	[byte ptr bx+8], 0
		jmp	short loc_13FB7
; ---------------------------------------------------------------------------

loc_13F6D:				; CODE XREF: eff_13F3B+19j
		movzx	ax, [byte ptr bx+8]
		shl	ax, 1
		mov	dl, 3
		div	dl
		mov	[bx+8],	al
		jmp	short loc_13FB7
; ---------------------------------------------------------------------------

loc_13F7C:				; CODE XREF: eff_13F3B+1Dj
		shr	[byte ptr bx+8], 1
		jmp	short loc_13FB7
; ---------------------------------------------------------------------------

loc_13F81:				; CODE XREF: eff_13F3B+5Fj
		movzx	ax, [byte ptr bx+8]
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
endp		eff_13F3B


; =============== S U B	R O U T	I N E =======================================


proc		eff_13FBE near		; CODE XREF: sub_13623+196j
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
		movzx	ax, [byte_24668]
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
		jmp	[off_245CA]
; ---------------------------------------------------------------------------

loc_1401A:				; CODE XREF: eff_13FBE+35j
		mov	ax, [bx]
		jmp	[off_245CA]
endp		eff_13FBE


; =============== S U B	R O U T	I N E =======================================


proc		eff_14020 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		xor	ah, ah
		shl	ax, 2
		push	bx
		push	si
		push	es
		push	cs
		call	near ptr change_amplif
		pop	es
		pop	si
		pop	bx
		retn
endp		eff_14020


; =============== S U B	R O U T	I N E =======================================


proc		eff_14030 near		; CODE XREF: sub_13623+196j
					; sub_137D5+16j ...
		and	ax, 0Fh
		mov	di, ax
		mov	al, [cs:byte_14057+di]
		mov	[byte_2467B], al

loc_1403D:				; CODE XREF: eff_14067+Ej
					; eff_14067+17j ...
		call	sub_14043
		jmp	sub_13CF6
endp		eff_14030


; =============== S U B	R O U T	I N E =======================================


proc		sub_14043 near		; CODE XREF: far_module+34p
					; eff_14030:loc_1403Dp
		mov	al, [byte_2467B]
		add	al, [byte_2467C]
		and	eax, 0FFh
		lea	ax, [eax+eax*4]
		shr	ax, 1
		retn
endp		sub_14043

; ---------------------------------------------------------------------------
byte_14057	db 0FFh			; DATA XREF: far_module+27r
					; eff_14030+5r
		db  80h	; €
		db  40h	; @
		db  2Ah	; *
		db  20h
		db  19h
		db  15h
		db  12h
		db 10h
		db  0Eh
		db  0Ch
		db  0Bh
		db  0Ah
		db    9
		db    9
		db    8

; =============== S U B	R O U T	I N E =======================================


proc		eff_14067 near		; CODE XREF: sub_13623+196j
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
		mov	[byte_2467C], 0
		jmp	short loc_1403D
endp		eff_14067


; =============== S U B	R O U T	I N E =======================================


proc		sub_14087 near		; CODE XREF: eff_13DE5p eff_13DEFp
		xor	ah, ah
		or	al, al
		jz	short loc_14090
		mov	[bx+34h], al

loc_14090:				; CODE XREF: sub_14087+4j
		mov	al, [bx+34h]
		cmp	[byte_24668], 0
		jz	short loc_140A2
		cmp	al, 0E0h ; 'à'
		jnb	short loc_140B3
		shl	ax, 2
		retn
; ---------------------------------------------------------------------------

loc_140A2:				; CODE XREF: sub_14087+11j
		cmp	al, 0E0h ; 'à'
		jbe	short loc_140B3
		mov	dl, al
		and	al, 0Fh
		cmp	dl, 0F0h ; 'ð'
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


proc		sub_140B6 near		; CODE XREF: set_gravis+1Ep
					; sub_14358+91p ...
		cmp	[byte_24671], 1
		jz	short locret_140E5
		cmp	[byte_2467F], 1
		jz	short locret_140E5
		inc	[byte_24668]
		mov	al, [byte_24668]
		cmp	al, [byte_24667]
		jnb	short loc_140E6
		mov	bx, offset byte_25908
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
		mov	[byte_24668], 0
		cmp	[byte_2466D], 0
		jnz	short loc_140F7
		call	sub_135CA
		jmp	short loc_14111
; ---------------------------------------------------------------------------

loc_140F7:				; CODE XREF: sub_140B6+3Aj
		mov	bx, offset byte_25908
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
		mov	si, [word ptr pointer_245B4]
		jmp	short $+2

loc_14111:				; CODE XREF: sub_140B6+3Fj int8p+43p
		cmp	[byte_2466B], 1
		jz	loc_141BA
		cmp	[byte_2466A], 1
		jz	short loc_14153
		cmp	[byte_2466C], 0
		jz	short loc_14131
		xor	al, al
		xchg	al, [byte_2466C]
		mov	[byte_2466D], al

loc_14131:				; CODE XREF: sub_140B6+70j
		cmp	[byte_2466D], 0
		jz	short loc_1413E
		dec	[byte_2466D]
		jnz	short loc_14142

loc_1413E:				; CODE XREF: sub_140B6+80j
		inc	[word_245F6]

loc_14142:				; CODE XREF: sub_140B6+86j
		mov	bx, [word_245F0]
		movzx	ax, [byte_281E8+bx]
		cmp	[word_245F6], ax
		jbe	loc_141DA

loc_14153:				; CODE XREF: sub_140B6+69j
		cmp	[byte_2467F], 2
		jz	short loc_14184
		inc	[word_245F0]
endp		sub_140B6 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1415E near		; CODE XREF: sub_12F56+11p
		mov	ax, [word_245FA]
		cmp	[word_245F0], ax
		jb	short loc_14184
		test	[byte_24672], 4
		jz	short sub_141DF
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
		bts	[word ptr byte_282E8], bx
		movzx	bx, [byte_27FE8+bx]
		mov	[word_245F4], bx
		shl	bx, 1
		mov	es, [segs_table+bx]
		mov	[word ptr pointer_245B4+2], es

loc_141BA:				; CODE XREF: sub_140B6+60j
		xor	ax, ax
		xchg	al, [byte_24669]
		mov	[word_245F6], ax
		call	sub_11C0C
		mov	[byte_2466A], 0
		mov	[byte_2466B], 0
		mov	[byte_2466C], 0
		mov	[byte_2466D], 0

loc_141DA:				; CODE XREF: sub_140B6+99j
		mov	[word ptr pointer_245B4], si
		retn
endp		sub_1415E


; =============== S U B	R O U T	I N E =======================================


proc		sub_141DF near		; CODE XREF: eff_13B06+31p
					; sub_1415E+Ej
		push	cs
		call	near ptr sub_12A66
		mov	[byte_24671], 1
		mov	dl, 1
		mov	bx, 5344h	; DS
		mov	cx, 4D50h	; MP
		mov	ax, 60FFh
		int	2Fh		; IPLAY: get data seg
		retn
endp		sub_141DF


; =============== S U B	R O U T	I N E =======================================


proc		sub_141F6 near		; CODE XREF: sub_12DA8+78p

; FUNCTION CHUNK AT 526B SIZE 000000DB BYTES

		cmp	[byte_24680], 1
		jz	short loc_1420D
		mov	[byte_24680], 1
		movzx	bx, [sndcard_type]
		shl	bx, 1
		jmp	[off_252A2+bx]
; ---------------------------------------------------------------------------

loc_1420D:				; CODE XREF: sub_141F6+5j sub_1420F+5j ...
		stc
		retn
endp		sub_141F6 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1420F near		; CODE XREF: sub_12EBA+87p
		cmp	[byte_24680], 1
		jnz	short loc_1420D
		cmp	[byte_24681], 1
		jz	short loc_1420D
		mov	[byte_24681], 1
		movzx	bx, [sndcard_type]
		shl	bx, 1
		jmp	[off_252B8+bx]
endp		sub_1420F


; =============== S U B	R O U T	I N E =======================================


proc		sub_1422D near		; CODE XREF: sub_12F48+8p sub_1424F+Cp

; FUNCTION CHUNK AT 0B5A SIZE 000001CC BYTES

		cmp	[byte_24680], 1
		jnz	short loc_1420D
		cmp	[byte_24681], 0
		jz	short loc_1420D
		mov	[byte_24681], 0
		push	cs
		call	near ptr sub_12A66
		movzx	bx, [sndcard_type]
		shl	bx, 1
		jmp	[off_252CE+bx]
endp		sub_1422D ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1424F near		; CODE XREF: sub_125B9+18p
		cmp	[byte_24680], 1
		jnz	short loc_1420D
		mov	[byte_24680], 0
		call	sub_1422D
		movzx	bx, [sndcard_type]
		shl	bx, 1
		jmp	[off_252E4+bx]
endp		sub_1424F

; ---------------------------------------------------------------------------

gravis_check:				; DATA XREF: seg003:off_252A2o
		mov	[sndflags_24622], 24h ;	'$'
		mov	[byte_24623], 1
		mov	[bit_mode], 16
		mov	[byte_2463B], 9
		test	[byte ptr word_246DA], 10h
		jz	short loc_14289
		and	[byte_2463B], 0FEh

loc_14289:				; CODE XREF: seg000:4282j
		mov	ax, [snd_base_port]
		cmp	ax, 0FFFFh
		jz	short loc_142B1
		add	ax, 103h
		mov	[word_24626], ax
		mov	al, [irq_number]
		cmp	al, 0FFh
		jz	short loc_142B1
		mov	[byte_2462A], al
		mov	[byte_2462B], al
		mov	al, [dma_channel]
		mov	[byte_2462C], al
		mov	[byte_2462D], al
		cmp	al, 0FFh
		jnz	short loc_142DA

loc_142B1:				; CODE XREF: seg000:428Fj seg000:429Cj
		call	sub_17F7D
		jb	short loc_1432F
		mov	[snd_base_port], dx
		add	dx, 103h
		mov	[word_24626], dx
		mov	[byte_2462A], bl
		mov	[irq_number], bl
		mov	[byte_2462B], bh
		mov	[byte_2462C], cl
		mov	[dma_channel], cl
		mov	[byte_2462D], ch

loc_142DA:				; CODE XREF: seg000:42AFj
		call	sub_17E86
		mov	dx, 0F7Bh
		jb	short locret_1432E
		mov	al, [byte_246D8]
		cmp	al, 0FFh
		jnz	short loc_142EC
		call	sub_17F30

loc_142EC:				; CODE XREF: seg000:42E7j
		mov	[byte_24628], al
		mov	[byte_246D8], al
		mov	al, 20h	; ' '
		call	sub_18079
		call	sub_18216
		mov	dx, [word_24626]
		sub	dx, 103h
		mov	al, [byte_2463B]
		out	dx, al
		mov	[off_245CA], offset sub_13215
		mov	[off_245C8], offset loc_134A2
		mov	[off_245CC], offset sub_132A9
		mov	[off_245CE], offset loc_13272
		mov	[freq1], 22050
		mov	si, offset sub_14358
		mov	al, [byte_2462A]
		call	setsb_handler
		clc

locret_1432E:				; CODE XREF: seg000:42E0j
		retn
; ---------------------------------------------------------------------------

loc_1432F:				; CODE XREF: seg000:42B4j
		mov	dx, offset aCouldNotFindThe ; "Could not find the ULTRASND environment"...
; START	OF FUNCTION CHUNK FOR sub_14996

loc_14332:				; CODE XREF: proaud_check+22j
					; proaud_check+E2j ...
		stc
		retn
; END OF FUNCTION CHUNK	FOR sub_14996

; =============== S U B	R O U T	I N E =======================================


proc		set_gravis near		; DATA XREF: seg003:off_252B8o
		pushf
		cli
		mov	dx, [word_24626]
		mov	al, 45h	; 'E'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		mov	al, 4
		out	dx, al
		sub	dx, 0FDh ; 'ý'
		mov	al, 4
		out	dx, al
		inc	dx
		mov	al, 1
		out	dx, al
		popf
		call	sub_140B6
		retn
endp		set_gravis

; ---------------------------------------------------------------------------
		db 87h,	0DBh

; =============== S U B	R O U T	I N E =======================================


proc		sub_14358 far		; DATA XREF: seg000:4324o
		push	ax
		push	bx
		push	cx
		push	dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		mov	bx, 1
		mov	cl, [irq_number]
		shl	bx, cl
		mov	dx, 21h	; '!'
		or	bh, bh
		jz	short loc_1437F
		mov	dx, 0A1h ; '¡'
		mov	al, 20h	; ' '
		out	0A0h, al	; PIC 2	 same as 0020 for PIC 1
		mov	bl, bh

loc_1437F:				; CODE XREF: sub_14358+1Cj
		in	al, dx		; Interrupt Controller #2, 8259A
		or	al, bl
		out	dx, al		; Interrupt Controller #2, 8259A
		sti

loc_14384:				; CODE XREF: sub_14358+45j
		mov	dx, [word_24626]
		sub	dx, 0FDh ; 'ý'
		in	al, dx
		test	al, 1100000b
		jnz	loc_1444C

loc_14393:				; CODE XREF: sub_14358+110j
		test	al, 4
		jnz	short loc_143C0

loc_14397:				; CODE XREF: sub_14358+9Ej
		test	al, 80h
		jnz	short loc_143F8

loc_1439B:				; CODE XREF: sub_14358+C1j
					; sub_14358+F1j
		test	al, 0E4h
		jnz	short loc_14384
		mov	bx, 1
		mov	cl, [irq_number]
		shl	bx, cl
		mov	dx, 21h	; '!'
		or	bh, bh
		jz	short loc_143B4
		mov	dx, 0A1h ; '¡'
		mov	bl, bh

loc_143B4:				; CODE XREF: sub_14358+55j
		not	bl
		in	al, dx		; Interrupt Controller #2, 8259A
		and	al, bl
		out	dx, al		; Interrupt Controller #2, 8259A
		pop	ds
		pop	dx
		pop	cx
		pop	bx
		pop	ax
		iret
; ---------------------------------------------------------------------------

loc_143C0:				; CODE XREF: sub_14358+3Dj
		push	ax
		mov	dx, [word_24626]
		pushf
		cli
		mov	al, 45h	; 'E'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		mov	al, 4
		out	dx, al
		popf
		dec	[byte_24619]
		jnz	short loc_143F5
		mov	al, [byte_24618]
		mov	[byte_24619], al
		pushf
		sti
		pushad
		push	es
		push	fs
		push	gs
		call	sub_140B6
		pop	gs
		pop	fs
		assume fs:nothing
		pop	es
		popad
		popf

loc_143F5:				; CODE XREF: sub_14358+80j
		pop	ax
		jmp	short loc_14397
; ---------------------------------------------------------------------------

loc_143F8:				; CODE XREF: sub_14358+41j
		mov	ah, al
		mov	dx, [word_24626]
		pushf
		cli
		mov	al, 41h	; 'A'
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		popf
		mov	al, ah
		cmp	[word_24636], 0
		jnz	short loc_1441C
		mov	[byte_2466E], 0
		jmp	short loc_1439B
; ---------------------------------------------------------------------------

loc_1441C:				; CODE XREF: sub_14358+BAj
		pushad
		push	es
		push	fs
		push	gs
		push	[word ptr dma_buf_pointer]
		xor	ax, ax
		xchg	ax, [word_24636]
		mov	[word_2460E], ax
		mov	ax, [word_24634]
		mov	[word ptr dma_buf_pointer], ax
		mov	bp, [word_24632]
		call	loc_18338
		pop	[word ptr dma_buf_pointer]
		pop	gs
		pop	fs
		pop	es
		popad
		jmp	loc_1439B
; ---------------------------------------------------------------------------

loc_1444C:				; CODE XREF: sub_14358+37j
		push	ax
		push	bx

loc_1444E:				; CODE XREF: sub_14358+142j
					; sub_14358+1D0j ...
		mov	dx, [word_24626]
		mov	al, 8Fh	; ''
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		mov	ah, al
		shl	ah, 1
		jnb	short loc_1449C
		shl	ah, 1
		jnb	short loc_1446B
		pop	bx
		pop	ax
		jmp	loc_14393
; ---------------------------------------------------------------------------

loc_1446B:				; CODE XREF: sub_14358+10Cj
		and	ax, 1Fh
		shl	ax, 4
		mov	bx, ax
		shl	ax, 2
		add	bx, ax
		add	bx, offset byte_25908
		dec	dx
		pushf
		cli
		mov	al, [bx+18h]
		out	dx, al
		inc	dx
		mov	al, 0Dh
		out	dx, al
		add	dl, 2
		mov	al, 3
		out	dx, al
		sub	dl, 2
		mov	al, 9
		out	dx, al
		inc	dx
		mov	ax, [bx+36h]
		out	dx, ax
		dec	dx
		popf
		jmp	short loc_1444E
; ---------------------------------------------------------------------------

loc_1449C:				; CODE XREF: sub_14358+108j
		and	ax, 1Fh
		shl	ax, 4
		mov	bx, ax
		shl	ax, 2
		add	bx, ax
		add	bx, offset byte_25908
		mov	dx, [word_24626]
		dec	dx
		mov	al, [bx+18h]
		pushf
		cli
		out	dx, al
		inc	dx
		mov	al, 80h	; '€'
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		and	al, 3
		jz	short loc_14527
		mov	al, 0
		out	dx, al
		add	dl, 2
		mov	al, 3
		out	dx, al
		sub	dl, 2
		mov	al, 0Dh
		out	dx, al
		add	dl, 2
		mov	al, 3
		out	dx, al
		sub	dl, 2
		and	[byte ptr bx+17h], 0FEh
		mov	[byte ptr bx+35h], 0
		mov	[word ptr bx+36h], 0
		mov	al, 89h	; '‰'
		out	dx, al
		inc	dx
		in	ax, dx
		dec	dx
		cmp	ah, 84h	; '„'
		jbe	short loc_1452B
		mov	al, 7
		out	dx, al
		add	dl, 2
		mov	al, ah
		out	dx, al
		sub	dl, 2
		mov	al, 8
		out	dx, al
		add	dl, 2
		mov	al, 80h	; '€'
		out	dx, al
		sub	dl, 2
		mov	al, 6
		out	dx, al
		add	dl, 2
		mov	al, 3Fh	; '?'
		out	dx, al
		sub	dl, 2
		mov	al, 0Dh
		out	dx, al
		add	dl, 2
		mov	al, 60h	; '`'
		out	dx, al
		sub	dl, 2

loc_14527:				; CODE XREF: sub_14358+16Dj
		popf
		jmp	loc_1444E
; ---------------------------------------------------------------------------

loc_1452B:				; CODE XREF: sub_14358+19Dj
		mov	al, 9
		out	dx, al
		inc	dx
		xor	ax, ax
		out	dx, ax
		dec	dx
		popf
		jmp	loc_1444E
endp		sub_14358


; =============== S U B	R O U T	I N E =======================================


proc		gravis_sndoff near	; DATA XREF: seg003:off_252CEo
		pushf
		cli
		mov	dx, [word_24626]
		mov	al, 45h	; 'E'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		sub	dl, 2
		sub	dx, 0FBh ; 'û'
		mov	al, 4
		out	dx, al
		inc	dx
		mov	al, 81h	; ''
		out	dx, al
		popf
		retn
endp		gravis_sndoff


; =============== S U B	R O U T	I N E =======================================


proc		gravis_clean near	; DATA XREF: seg003:off_252E4o
		mov	al, 20h	; ' '
		call	sub_18079
		and	[byte_2463B], 0FEh
		mov	dx, [word_24626]
		sub	dx, 103h
		mov	al, [byte_2463B]
		out	dx, al
		call	restore_intvector
		retn
endp		gravis_clean


; =============== S U B	R O U T	I N E =======================================


proc		proaud_check near	; DATA XREF: seg003:0D04o
		mov	[sndflags_24622], 9
		mov	[byte_24623], 1
		mov	[bit_mode], 16
		mov	bx, 3F3Fh
		mov	ax, 0BC00h	; Return: if installed,	BX XOR CX XOR DX = 4D56h ('MV')
					; Program: MVSOUND.SYS is a driver for the MediaVision ProAudio	Spectrum family
					;	    of sound boards; its primary programmer was	Bryan Crane
		int	2Fh		; - Multiplex -	Windows	3.0 EGA.SYS - INSTALLATION CHECK
					; Return: AL = 00h not installed, OK to	install
					; AL = 01h not installed, not OK to install
					; AL = FFh installed, BX = 5456h ("TV")
		xor	bx, cx
		xor	bx, dx
		mov	dx, 0FC0h
		cmp	bx, 4D56h	; VM
		jnz	loc_14332
		mov	dx, [snd_base_port]
		cmp	dx, 0FFFFh
		jnz	short loc_145A6
		call	proaud_spectr_14
		jb	loc_1464F

loc_145A6:				; CODE XREF: proaud_check+2Dj
		mov	[word_24646], dx
		mov	[snd_base_port], dx
		xor	dx, 388h
		mov	[sound_port], dx
		mov	ax, 0BC04h	; INT 2F - MediaVision MVSOUND.SYS - GET DMA AND IRQ CHANNELS
					;
					;	  AX = BC04h
					; Return: AX = 4D56h ('MV')
					;	  BL = DMA channel
					;	  CL = IRQ number
		int	2Fh		; - Multiplex -	Windows	3.0 EGA.SYS -
		cmp	[irq_number], 0FFh
		jnz	short loc_145C6
		mov	[irq_number], cl

loc_145C6:				; CODE XREF: proaud_check+50j
		cmp	[dma_channel], 0FFh
		jnz	short loc_145D1
		mov	[dma_channel], bl

loc_145D1:				; CODE XREF: proaud_check+5Bj
		mov	al, [irq_number]
		mov	[byte_2464B], al
		mov	al, [dma_channel]
		mov	[byte_2464A], al
		mov	dx, 12h
		mov	ax, 34DCh
		cmp	[byte_24623], 1
		jnz	short loc_145EE
		shr	dx, 1
		rcr	ax, 1

loc_145EE:				; CODE XREF: proaud_check+78j
		push	ax
		push	dx
		div	[freq1]
		mov	cx, ax
		pop	dx
		pop	ax
		div	cx
		mov	[freq1], ax
		mov	dx, 0B8Bh
		xor	dx, [sound_port]
		in	al, dx
		mov	eax, 1000h
		mov	cl, [byte_2464A]
		call	alloc_dma_buf
		mov	[word ptr dma_buf_pointer], 0
		mov	[word ptr dma_buf_pointer+2], ax
		pushf
		cli
		mov	dx, 0B8Ah
		xor	dx, [sound_port]
		mov	al, 21h	; '!'
		out	dx, al
		mov	dx, 8389h
		xor	dx, [sound_port]
		in	al, dx
		and	al, 0F0h
		or	al, 7
		out	dx, al
		mov	dx, 0F8Ah
		xor	dx, [sound_port]
		mov	al, 0F9h ; 'ù'
		out	dx, al
		mov	dx, 0B89h
		xor	dx, [sound_port]
		out	dx, al
		add	dl, 2
		mov	al, 8
		out	dx, al
		popf
		clc
		retn
; ---------------------------------------------------------------------------

loc_1464F:				; CODE XREF: proaud_check+32j
		mov	dx, offset aErrorSoundcardN ; "Error: Soundcard	not found!\r\n"
		jmp	loc_14332
endp		proaud_check


; =============== S U B	R O U T	I N E =======================================


proc		set_proaud near		; DATA XREF: seg003:0D1Ao
		call	sub_13017
		mov	[dma_mode], 58h	; 'X'
		mov	[word_2460E], 1000h
		mov	si, offset sb_14700 ; myfunc
		mov	al, [byte_2464B]
		call	setsb_handler
		pushf
		cli
		mov	dx, 0B8Bh
		xor	dx, [sound_port]
		mov	al, 8
		out	dx, al
		mov	dx, 12h
		mov	ax, 34DCh
		cmp	[byte_24623], 1
		jnz	short loc_14689
		shr	dx, 1
		rcr	ax, 1

loc_14689:				; CODE XREF: set_proaud+2Ej
		div	[freq1]
		mov	cx, ax
		mov	dx, 138Bh
		xor	dx, [sound_port]
		mov	al, 36h	; '6'
		out	dx, al
		jmp	short $+2
		jmp	short $+2
		sub	dl, 3
		mov	al, cl
		out	dx, al
		jmp	short $+2
		mov	al, ch
		out	dx, al
		jmp	short $+2
		mov	cl, [byte_2464A]
		call	dma_186E3
		mov	cx, 400h
		cmp	[byte_2464A], 4
		jb	short loc_146BD
		shr	cx, 1

loc_146BD:				; CODE XREF: set_proaud+64j
		mov	dx, 138Bh
		xor	dx, [sound_port]
		mov	al, 76h	; 'v'
		out	dx, al
		jmp	short $+2
		jmp	short $+2
		sub	dl, 2
		mov	al, cl
		out	dx, al
		jmp	short $+2
		mov	al, ch
		out	dx, al
		jmp	short $+2
		mov	dx, 0F88h
		xor	dx, [sound_port]
		xor	al, al
		out	dx, al
		mov	dx, 0B8Ah
		xor	dx, [sound_port]
		mov	al, 0E1h ; 'á'
		out	dx, al
		mov	dx, 0F8Ah
		xor	dx, [sound_port]
		mov	al, 0F9h ; 'ù'
		out	dx, al
		and	al, 0DFh
		out	dx, al
		mov	[byte_2466E], 1
		popf
		retn
endp		set_proaud


; =============== S U B	R O U T	I N E =======================================


; void __cdecl sb_14700()
proc		sb_14700 far		; DATA XREF: set_proaud+Eo

; FUNCTION CHUNK AT 4E10 SIZE 000000AF BYTES

		push	ax
		push	dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
		mov	dx, 0B89h
		xor	dx, [sound_port]
		in	al, dx
		jmp	short $+2
		out	dx, al
		test	al, 8
		jnz	loc_14E10
		mov	al, 20h	; ' '
		cmp	[byte_2464B], 8
		jb	short loc_14726
		out	0A0h, al	; PIC 2	 same as 0020 for PIC 1
		jmp	short $+2

loc_14726:				; CODE XREF: sb_14700+20j
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		pop	dx
		pop	ax
		iret
endp		sb_14700


; =============== S U B	R O U T	I N E =======================================


proc		proaud_sndoff near	; DATA XREF: seg003:0D30o
		pushf
		cli
		mov	dx, 0F8Ah
		xor	dx, [sound_port]
		in	al, dx
		and	al, 0BFh
		or	al, 10h
		out	dx, al
		mov	dx, 0B8Bh
		xor	dx, [sound_port]
		xor	al, al
		out	dx, al
		mov	cl, [byte_2464A]
		call	set_dmachn_mask
endp		proaud_sndoff ;	sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1474C near
		mov	dx, 0B8Bh
		xor	dx, [sound_port]
		xor	al, al
		out	dx, al
		mov	[byte_2466E], 0
		call	restore_intvector
		popf
		retn
endp		sub_1474C ; sp-analysis	failed

; ---------------------------------------------------------------------------

proaud_clean:				; DATA XREF: seg003:0D46o
		call	sub_18A28
		retn

; =============== S U B	R O U T	I N E =======================================


proc		proaud_spectr_14 near	; CODE XREF: proaud_check+2Fp
		mov	dx, 0B8Bh
		in	al, dx
		inc	al
		jnz	short loc_1479E
		mov	dx, 0B87h
		in	al, dx
		inc	al
		jnz	short loc_1479E
		mov	dx, 0B8Fh
		in	al, dx
		inc	al
		jnz	short loc_1479E
		mov	dx, 0A8Bh
		in	al, dx
		inc	al
		jnz	short loc_1479E
		mov	dx, 0A83h
		in	al, dx
		inc	al
		jnz	short loc_1479E
		mov	dx, 0A87h
		in	al, dx
		inc	al
		jnz	short loc_1479E
		mov	dx, 0A8Fh
		in	al, dx
		inc	al
		jnz	short loc_1479E
		stc
		retn
; ---------------------------------------------------------------------------

loc_1479E:				; CODE XREF: proaud_spectr_14+6j
					; proaud_spectr_14+Ej ...
		sub	dx, 803h
		clc
		retn
endp		proaud_spectr_14

; ---------------------------------------------------------------------------

check_wss:				; DATA XREF: seg003:0D06o
		mov	[sndflags_24622], 9
		mov	[byte_24623], 1
		mov	[bit_mode], 16
		mov	dx, [snd_base_port]
		cmp	dx, 0FFFFh
		jnz	short loc_147C3
		call	sub_1495F
		jb	loc_149AC

loc_147C3:				; CODE XREF: seg000:47BAj
		mov	[base_port2], dx
		mov	al, [irq_number]
		cmp	al, 0FFh
		jnz	short loc_147D0
		mov	al, 0Ah

loc_147D0:				; CODE XREF: seg000:47CCj
		mov	[irq_number2], al
		mov	al, [dma_channel]
		cmp	al, 0FFh
		jnz	short loc_147DC
		mov	al, 0

loc_147DC:				; CODE XREF: seg000:47D8j
		mov	[dma_channel2],	al
		call	sub_1498A
		call	sub_14996
		mov	al, [irq_number2]
		mov	cl, 8
		cmp	al, 7
		jz	short loc_14801
		mov	cl, 10h
		cmp	al, 9
		jz	short loc_14801
		mov	cl, 18h
		cmp	al, 0Ah
		jz	short loc_14801
		mov	cl, 20h	; ' '
		mov	[irq_number2], 0Bh

loc_14801:				; CODE XREF: seg000:47ECj seg000:47F2j ...
		mov	al, [dma_channel2]
		mov	ah, 1
		cmp	al, 0
		jz	short loc_14817
		mov	ah, 2
		cmp	al, 1
		jz	short loc_14817
		mov	ah, 3
		mov	[dma_channel2],	3

loc_14817:				; CODE XREF: seg000:4808j seg000:480Ej
		or	cl, ah
		mov	dx, [base_port2]
		mov	al, cl
		out	dx, al
		call	sub_1498A
		mov	eax, 1000h
		mov	cl, [dma_channel2]
		call	alloc_dma_buf
		mov	[word ptr dma_buf_pointer], 0
		mov	[word ptr dma_buf_pointer+2], ax
		mov	ax, [base_port2]
		mov	[snd_base_port], ax
		mov	al, [irq_number2]
		mov	[irq_number], al
		mov	al, [dma_channel2]
		mov	[dma_channel], al
		clc
		retn
; ---------------------------------------------------------------------------
freq_tbl	dw 5513			; DATA XREF: sub_14996+3Er
					; sub_14996:loc_149DFr
word_1484F	dw 1			; DATA XREF: sub_14996+51r
		dw 6615
		dw 0Fh
		dw 8000
		dw 0
		dw 9600
		dw 0Eh
		dw 11025
		dw 3
		dw 16000
		dw 2
		dw 18900
		dw 5
		dw 22050
		dw 7
		dw 27429
		dw 4
		dw 32000
		dw 6
		dw 33075
		dw 0Dh
		dw 37800
		dw 9
		dw 44100
		dw 0Bh
		dw 48000
		dw 0Ch

; =============== S U B	R O U T	I N E =======================================


proc		set_wss	near		; DATA XREF: seg003:0D1Co
		call	sub_13017
		mov	[dma_mode], 58h	; 'X'
		mov	[word_2460E], 1000h
		mov	ax, [base_port2]
		add	ax, 6
		mov	[cs:word_14913], ax
		mov	si, offset loc_14910 ; myfunc
		mov	al, [irq_number2]
		call	setsb_handler
		call	sub_1498A
		mov	cl, [dma_channel2]
		call	dma_186E3
		mov	ax, 400h
		mov	cl, [byte_24623]
		shr	ax, cl
		mov	cl, [bit_mode]
		shr	cl, 4
		and	cl, 1
		shr	ax, cl
		dec	ax
		mov	ch, ah
		mov	ah, 0Fh
		call	sub_14A57
		mov	ah, 0Eh
		mov	al, ch
		call	sub_14A57
		mov	ah, 6
		call	sub_14A66
		mov	[byte_24650], al
		and	al, 7Fh
		call	sub_14A57
		mov	ah, 7
		call	sub_14A66
		mov	[byte_24651], al
		and	al, 7Fh
		call	sub_14A57
		mov	ax, 1800h
		call	sub_14A57
		mov	dx, [base_port2]
		add	dx, 6
		xor	al, al
		out	dx, al
		mov	ax, 0A02h
		call	sub_14A57
		mov	ax, 905h
		call	sub_14A57
		mov	[byte_2466E], 1
		retn
endp		set_wss

; ---------------------------------------------------------------------------

loc_14910:				; DATA XREF: set_wss+18o
		push	ax
		push	dx
; ---------------------------------------------------------------------------
		db 0BAh	; º
word_14913	dw 536h			; DATA XREF: set_wss+14w
; ---------------------------------------------------------------------------
		xor	al, al
		out	dx, al
		push	ds
		mov	ax, seg003
		mov	ds, ax
		jmp	loc_14E10

; =============== S U B	R O U T	I N E =======================================


proc		wss_sndoff near		; DATA XREF: seg003:0D32o
		pushf
		cli
		mov	ah, 6
		mov	al, [byte_24650]
		call	sub_14A57
		mov	ah, 7
		mov	al, [byte_24651]
		call	sub_14A57
		mov	ax, 1800h
		call	sub_14A57
		mov	dx, [base_port2]
		add	dx, 6
		xor	al, al
		out	dx, al		; DMA controller, 8237A-5.
					; channel 3 base address
					; (also	sets current address)
		mov	ax, 0A00h
		call	sub_14A57
		mov	ax, 904h
		call	sub_14A57
		mov	cl, [dma_channel2]
		call	set_dmachn_mask
		call	sub_1498A
		popf
		retn
endp		wss_sndoff

; ---------------------------------------------------------------------------

wss_clean:				; DATA XREF: seg003:0D48o
		call	sub_18A28
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_1495F near		; CODE XREF: seg000:47BCp
		mov	dx, 533h
		in	al, dx
		in	al, dx
		inc	al
		jnz	short loc_14985
		mov	dx, 607h
		in	al, dx
		in	al, dx
		inc	al
		jnz	short loc_14985
		mov	dx, 0E83h
		in	al, dx
		in	al, dx
		inc	al
		jnz	short loc_14985
		mov	dx, 0F43h
		in	al, dx
		in	al, dx
		inc	al
		jnz	short loc_14985
		stc
		retn
; ---------------------------------------------------------------------------

loc_14985:				; CODE XREF: sub_1495F+7j
					; sub_1495F+10j ...
		sub	dx, 3
		clc
		retn
endp		sub_1495F


; =============== S U B	R O U T	I N E =======================================


proc		sub_1498A near		; CODE XREF: seg000:47DFp seg000:4820p ...
		mov	dx, [base_port2]
		add	dx, 6
		in	al, dx		; DMA controller, 8237A-5.
					; channel 3 current address
		xor	al, al
		out	dx, al		; DMA controller, 8237A-5.
					; channel 3 base address
					; (also	sets current address)
		retn
endp		sub_1498A


; =============== S U B	R O U T	I N E =======================================


proc		sub_14996 near		; CODE XREF: seg000:47E2p

; FUNCTION CHUNK AT 4332 SIZE 00000002 BYTES

		mov	ecx, 100000h
		mov	dx, [base_port2]
		add	dx, 4

loc_149A3:				; CODE XREF: sub_14996+14j
		in	al, dx		; DMA controller, 8237A-5.
					; channel 2 current address
		test	al, 80h
		jz	short loc_149B2
		dec	ecx
		jnz	short loc_149A3

loc_149AC:				; CODE XREF: seg000:47BFj
		mov	dx, offset aErrorSoundcardN ; "Error: Soundcard	not found!\r\n"
		jmp	loc_14332
; ---------------------------------------------------------------------------

loc_149B2:				; CODE XREF: sub_14996+10j
		mov	al, 49h	; 'I'
		out	dx, al
		inc	dx
		mov	al, 0Ch
		out	dx, al
		dec	dx
		mov	al, 9
		out	dx, al
		mov	ax, 1080h
		call	sub_14A57
		mov	ax, 1101h
		call	sub_14A57
		mov	si, 0FFFCh
		mov	ax, [freq1]
		mov	bl, 0Eh

loc_149D1:				; CODE XREF: sub_14996+47j
		add	si, 4
		cmp	ax, [cs:freq_tbl+si]
		jbe	short loc_149DF
		dec	bl
		jnz	short loc_149D1

loc_149DF:				; CODE XREF: sub_14996+43j
		mov	ax, [cs:freq_tbl+si]
		mov	[freq1], ax
		mov	bx, [cs:word_1484F+si]
		mov	al, [byte_24623]
		mov	ah, [bit_mode]
		and	ax, 1001h
		shl	al, 4
		shl	ah, 2
		or	al, bl
		or	al, ah
		mov	ah, 48h	; 'H'
		call	sub_14A57
		mov	dx, [base_port2]
		add	dx, 5
		in	al, dx		; DMA controller, 8237A-5.
					; channel 2 current word count
		in	al, dx		; DMA controller, 8237A-5.
					; channel 2 current word count
		dec	dx
		mov	ecx, 100000h

loc_14A15:				; CODE XREF: sub_14996+86j
		in	al, dx		; DMA controller, 8237A-5.
					; channel 2 current address
		test	al, 80h
		jz	short loc_14A1E
		dec	ecx
		jnz	short loc_14A15

loc_14A1E:				; CODE XREF: sub_14996+82j
		mov	ecx, 100000h

loc_14A24:				; CODE XREF: sub_14996+98j
		mov	al, 8
		out	dx, al		; DMA controller, 8237A-5.
					; channel 2 base address
					; (also	sets current address)
		in	al, dx		; DMA controller, 8237A-5.
					; channel 2 current address
		cmp	al, 8
		jz	short loc_14A30
		dec	ecx
		jnz	short loc_14A24

loc_14A30:				; CODE XREF: sub_14996+94j
		mov	ecx, 100000h

loc_14A36:				; CODE XREF: sub_14996+AAj
		mov	al, 0Bh
		out	dx, al		; DMA controller, 8237A-5.
					; channel 2 base address
					; (also	sets current address)
		in	al, dx		; DMA controller, 8237A-5.
					; channel 2 current address
		cmp	al, 0Bh
		jz	short loc_14A42
		dec	ecx
		jnz	short loc_14A36

loc_14A42:				; CODE XREF: sub_14996+A6j
		mov	ecx, 100000h

loc_14A48:				; CODE XREF: sub_14996+BEj
		inc	dx
		in	al, dx		; DMA controller, 8237A-5.
					; channel 2 current word count
		dec	dx
		test	al, 20h
		jz	short locret_14A56
		mov	al, 0Bh
		out	dx, al		; DMA controller, 8237A-5.
					; channel 2 base address
					; (also	sets current address)
		dec	ecx
		jnz	short loc_14A48

locret_14A56:				; CODE XREF: sub_14996+B7j
		retn
endp		sub_14996


; =============== S U B	R O U T	I N E =======================================


proc		sub_14A57 near		; CODE XREF: set_wss+45p set_wss+4Cp ...
		mov	dx, [base_port2]
		xchg	al, ah
		add	dx, 4
		out	dx, al		; DMA controller, 8237A-5.
					; channel 2 base address
					; (also	sets current address)
		inc	dx
		xchg	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; channel 2 base address and word count
		retn
endp		sub_14A57


; =============== S U B	R O U T	I N E =======================================


proc		sub_14A66 near		; CODE XREF: set_wss+51p set_wss+5Ep
		mov	dx, [base_port2]
		add	dx, 4
		mov	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; channel 2 base address
					; (also	sets current address)
		inc	dx
		in	al, dx		; DMA controller, 8237A-5.
					; channel 2 current word count
		retn
endp		sub_14A66

; ---------------------------------------------------------------------------

sb16_check:				; DATA XREF: seg003:0D08o
		mov	[sndflags_24622], 9
		mov	[byte_24623], 1
		mov	[bit_mode], 16
		call	sub_183CC
		mov	dx, offset aErrorSoundcardN ; "Error: Soundcard	not found!\r\n"
		jb	loc_14332
		mov	al, [irq_number]
		mov	[irq_number3], al
		cmp	al, 0FFh
		jnz	short loc_14ABB
		mov	ah, 80h	; '€'
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

loc_14AB3:				; CODE XREF: seg000:4AA3j seg000:4AA9j ...
		mov	[irq_number3], ah
		mov	[irq_number], ah

loc_14ABB:				; CODE XREF: seg000:4A94j seg000:4A9Dj
		mov	al, [dma_channel]
		mov	[dma_chn_mask],	al
		cmp	al, 0FFh
		jnz	short loc_14AFD
		mov	ah, 81h	; ''
		call	ReadMixerSB
		cmp	al, 0FFh
		jz	short loc_14AFD
		cmp	[bit_mode], 8
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

loc_14AE7:				; CODE XREF: seg000:4AD3j
		mov	ah, 3
		test	al, 4
		jnz	short loc_14AF5
		mov	ah, 1
		test	al, 2
		jnz	short loc_14AF5
		mov	ah, 0

loc_14AF5:				; CODE XREF: seg000:4AD9j seg000:4ADFj ...
		mov	[dma_chn_mask],	ah
		mov	[dma_channel], ah

loc_14AFD:				; CODE XREF: seg000:4AC3j seg000:4ACCj
		call	sbsound_on
		mov	eax, 1000h
		mov	cl, [dma_chn_mask]
		call	alloc_dma_buf
		mov	[word ptr dma_buf_pointer], 0
		mov	[word ptr dma_buf_pointer+2], ax
		clc
		retn

; =============== S U B	R O U T	I N E =======================================


proc		set_sb16 near		; DATA XREF: seg003:0D1Eo
		call	sub_13017
		mov	[dma_mode], 58h	; 'X'
		mov	[word_2460E], 1000h
		mov	si, offset loc_14BB8 ; myfunc
		mov	al, [irq_number3]
		call	setsb_handler
		mov	dx, [sb_base_port]
		add	dl, 0Ch

loc_14B36:				; CODE XREF: set_sb16+21j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B36
		mov	al, 41h	; 'A'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B3E:				; CODE XREF: set_sb16+29j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B3E
		mov	al, [byte ptr freq1+1]
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B47:				; CODE XREF: set_sb16+32j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B47
		mov	al, [byte ptr freq1]
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B50:				; CODE XREF: set_sb16+3Bj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14B50
		cmp	[bit_mode], 16
		jz	short loc_14B6A
		mov	ax, [sb_base_port]
		add	al, 0Eh
		mov	[cs:word_14BBB], ax
		mov	ax, 0C6h ; 'Æ'
		jmp	short loc_14B76
; ---------------------------------------------------------------------------

loc_14B6A:				; CODE XREF: set_sb16+42j
		mov	ax, [sb_base_port]
		add	al, 0Fh
		mov	[cs:word_14BBB], ax
		mov	ax, 10B6h

loc_14B76:				; CODE XREF: set_sb16+50j
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14B77:				; CODE XREF: set_sb16+62j
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

loc_14B87:				; CODE XREF: set_sb16+72j
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

loc_14BA0:				; CODE XREF: set_sb16+8Bj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14BA0
		mov	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	cl, [dma_chn_mask]
		call	dma_186E3
		mov	[byte_2466E], 1
		retn
endp		set_sb16

; ---------------------------------------------------------------------------

; void __cdecl loc_14BB8()
loc_14BB8:				; DATA XREF: set_sb16+Eo
		push	ax
		push	dx
; ---------------------------------------------------------------------------
		db 0BAh	; º
word_14BBB	dw 22Fh			; DATA XREF: set_sb16+49w set_sb16+57w
; ---------------------------------------------------------------------------
		in	al, dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
		jmp	loc_14E10

; =============== S U B	R O U T	I N E =======================================


proc		sb16_sndoff near	; DATA XREF: seg003:0D34o
		pushf
		cli
		cmp	[byte_2466E], 1
		jnz	short loc_14BFD
		cli
		mov	dx, [sb_base_port]
		add	dl, 0Ch

loc_14BD8:				; CODE XREF: sb16_sndoff+14j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14BD8
		mov	al, 0DAh ; 'Ú'
		cmp	[bit_mode], 8
		jz	short loc_14BE8
		mov	al, 0D9h ; 'Ù'

loc_14BE8:				; CODE XREF: sb16_sndoff+1Dj
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14BE9:				; CODE XREF: sb16_sndoff+25j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14BE9
		call	restore_intvector
		mov	cl, [dma_chn_mask]
		call	set_dmachn_mask
		mov	[byte_2466E], 0

loc_14BFD:				; CODE XREF: sb16_sndoff+7j
		popf
		retn
endp		sb16_sndoff

; ---------------------------------------------------------------------------

sb16_clean:				; DATA XREF: seg003:0D4Ao
		call	sub_18A28
		call	sbsound_off
		retn
; ---------------------------------------------------------------------------

sbpro_check:				; DATA XREF: seg003:0D0Ao
		mov	[sndflags_24622], 9
		mov	[byte_24623], 1
		mov	[bit_mode], 8
		call	sub_18449
		jb	loc_14332
		mov	dx, 0Fh
		mov	ax, 4240h	; 0F4240h SB time constant
		div	[freq1]
		mov	bx, ax
		mov	dx, 0Fh
		mov	ax, 4240h
		div	bx
		mov	[freq1], ax
		mov	eax, 1000h
		mov	cl, [dma_chn_mask]
		call	alloc_dma_buf
		mov	[word ptr dma_buf_pointer], 0
		mov	[word ptr dma_buf_pointer+2], ax
		mov	dx, 0Fh
		mov	ax, 4240h
		div	[freq1]
		shr	al, 1
		neg	al
		mov	[sb_timeconst],	al
		clc
		retn
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR set_sb

set_sbpro:				; CODE XREF: set_sb+6j
					; DATA XREF: seg003:0D20o
		call	sub_13017
		mov	[dma_mode], 58h	; 'X'
		mov	[word_2460E], 1000h
		mov	ax, [sb_base_port]
		add	al, 0Eh
		mov	[cs:word_14CEB], ax
		mov	ah, 0Eh
		call	ReadMixerSB
		mov	[byte_24664], al
		and	al, 0FDh
		cmp	[byte_24623], 0
		jz	short loc_14C89
		call	WriteMixerSB
		or	al, 22h

loc_14C89:				; CODE XREF: set_sb-F5j
		call	WriteMixerSB
		pushf
		cli
		mov	dx, [sb_base_port]
		add	dl, 0Eh
		in	al, dx		; DMA controller, 8237A-5.
					; Clear	mask registers.
					; Any OUT enables all 4	channels.
		sub	dl, 2

loc_14C99:				; CODE XREF: set_sb-DBj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14C99
		mov	al, 40h	; '@'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CA1:				; CODE XREF: set_sb-D3j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CA1
		mov	al, [sb_timeconst]
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CAA:				; CODE XREF: set_sb-CAj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CAA
		mov	al, 48h	; 'H'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CB2:				; CODE XREF: set_sb-C2j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CB2
		mov	ax, [word_2460E]
		shr	ax, 2
		dec	ax
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CBF:				; CODE XREF: set_sb-B5j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CBF
		mov	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14CC7:				; CODE XREF: set_sb-ADj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14CC7
		mov	al, 90h	; ''
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	[byte_2466E], 1
		mov	si, offset loc_14CE8 ; myfunc
		mov	al, [irq_number3]
		call	setsb_handler
		mov	cl, [dma_chn_mask]
		call	dma_186E3
		popf
		retn
; END OF FUNCTION CHUNK	FOR set_sb
; ---------------------------------------------------------------------------

loc_14CE8:				; DATA XREF: set_sb-A3o
		push	ax
		push	dx
; ---------------------------------------------------------------------------
		db 0BAh	; º
word_14CEB	dw 22Eh			; DATA XREF: set_sb-108w
; ---------------------------------------------------------------------------
		in	al, dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
		jmp	loc_14E10

; =============== S U B	R O U T	I N E =======================================


proc		sbpro_sndoff near	; CODE XREF: seg000:4ED8j
					; DATA XREF: seg003:0D36o
		pushf
		cli
		cmp	[byte_2466E], 1
		jnz	short loc_14D1A
		call	CheckSB
		call	restore_intvector
		mov	cl, [dma_chn_mask]
		call	set_dmachn_mask
		mov	[byte_2466E], 0
		mov	ah, 0Eh
		mov	al, [byte_24664]
		call	WriteMixerSB

loc_14D1A:				; CODE XREF: sbpro_sndoff+7j
		popf
		retn
endp		sbpro_sndoff


; =============== S U B	R O U T	I N E =======================================


proc		sbpro_clean near	; DATA XREF: seg003:0D4Co
		call	sub_18A28
		call	sbsound_off
		retn
endp		sbpro_clean


; =============== S U B	R O U T	I N E =======================================


proc		sb_check near		; DATA XREF: seg003:0D0Co
		mov	[sndflags_24622], 9
		mov	[byte_24623], 0
		mov	[bit_mode], 8
		call	sub_18449
		jb	loc_14332
		mov	dx, 0Fh
		mov	ax, 4240h
		div	[freq1]
		mov	bx, ax
		mov	dx, 0Fh
		mov	ax, 4240h
		div	bx
		mov	[freq1], ax
		mov	eax, 1000h
		mov	cl, [dma_chn_mask]
		call	alloc_dma_buf
		mov	[word ptr dma_buf_pointer], 0
endp		sb_check ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_14D63 near
		mov	[word ptr dma_buf_pointer+2], ax
		mov	dx, 0Fh
		mov	ax, 4240h
		div	[freq1]
		neg	al
		mov	[sb_timeconst],	al
		clc
		retn
endp		sub_14D63


; =============== S U B	R O U T	I N E =======================================


proc		set_sb near		; DATA XREF: seg003:0D22o

; FUNCTION CHUNK AT 4C5C SIZE 0000008A BYTES

		cmp	[freq1], 59D8h
		jnb	set_sbpro
		call	sub_13017
		mov	[dma_mode], 58h	; 'X'
		mov	[word_2460E], 1000h
		pushf
		cli
		mov	ax, [sb_base_port]
		add	al, 0Eh
		mov	[cs:word_14DED], ax
		mov	si, offset SBHandler_14DE4 ; myfunc
		mov	al, [irq_number3]
		call	setsb_handler
		mov	dx, [sb_base_port]
		mov	al, 40h	; '@'
		call	WriteSB
		mov	al, [sb_timeconst]
		call	WriteSB
		mov	cl, [dma_chn_mask]
		call	dma_186E3
		mov	dx, [sb_base_port]
		add	dl, 0Ch

loc_14DC0:				; CODE XREF: set_sb+4Cj
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14DC0
		mov	al, 14h
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14DC8:				; CODE XREF: set_sb+54j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14DC8
		mov	ax, [word_2460E]
		shr	ax, 2
		dec	ax
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14DD5:				; CODE XREF: set_sb+61j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14DD5
		mov	al, ah
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		mov	[byte_2466E], 1
		popf
		retn
endp		set_sb


; =============== S U B	R O U T	I N E =======================================


proc		SBHandler_14DE4	near	; DATA XREF: set_sb+23o
		push	ax
		push	dx
		push	ds
		mov	ax, seg003
		mov	ds, ax
; ---------------------------------------------------------------------------
		db 0BAh	; º
word_14DED	dw 22Eh			; DATA XREF: set_sb+1Fw
; ---------------------------------------------------------------------------
		in	al, dx
		sub	dl, 2

loc_14DF3:				; CODE XREF: SBHandler_14DE4+12j
		in	al, dx
		or	al, al
		js	short loc_14DF3
		mov	al, 14h
		out	dx, al

loc_14DFB:				; CODE XREF: SBHandler_14DE4+1Aj
		in	al, dx
		or	al, al
		js	short loc_14DFB
		mov	ax, [word_2460E]
		shr	ax, 2
		dec	ax
		out	dx, al

loc_14E08:				; CODE XREF: SBHandler_14DE4+27j
		in	al, dx
		or	al, al
		js	short loc_14E08
		mov	al, ah
		out	dx, al
endp		SBHandler_14DE4	; sp-analysis failed

; START	OF FUNCTION CHUNK FOR sb_14700

loc_14E10:				; CODE XREF: sb_14700+15j seg000:491Ej ...
		add	[word_24602], 400h
		and	[word_24602], 0FFFh
		inc	[byte_24620]
		cmp	[byte_24620], 2
		ja	loc_14EB7

loc_14E29:				; CODE XREF: sb_14700+7BCj
		pushad
		push	es
		push	fs
		push	gs
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		test	[byte ptr word_246DA+1], 10h
		jz	short loc_14E4D
		inc	[byte_24621]
		and	[byte_24621], 3
		jnz	short loc_14E4D
		mov	cl, [dma_channel]
		call	dma_186E3

loc_14E4D:				; CODE XREF: sb_14700+739j
					; sb_14700+744j
		mov	bx, 1
		mov	cl, [irq_number]
		shl	bx, cl
		mov	dx, 21h	; '!'
		or	bh, bh
		jz	short loc_14E66
		mov	dx, 0A1h ; '¡'
		mov	al, 20h	; ' '
		out	0A0h, al	; PIC 2	 same as 0020 for PIC 1
		mov	bl, bh

loc_14E66:				; CODE XREF: sb_14700+75Bj
		in	al, dx		; Interrupt Controller #2, 8259A
		or	al, bl
		out	dx, al		; Interrupt Controller #2, 8259A
		sti
		mov	ax, [word_24602]

loc_14E6E:				; CODE XREF: sb_14700+78Aj
		mov	dx, ax
		cmp	ax, [word_24600]
		ja	short loc_14E79
		add	ax, 1000h

loc_14E79:				; CODE XREF: sb_14700+774j
		sub	ax, [word_24600]
		cmp	ax, 800h
		jb	short loc_14E8C
		push	dx
		call	sub_16C69
		pop	ax
		add	ax, 10h
		jmp	short loc_14E6E
; ---------------------------------------------------------------------------

loc_14E8C:				; CODE XREF: sb_14700+780j
		mov	bx, 1
		mov	cl, [irq_number]
		shl	bx, cl
		mov	dx, 21h	; '!'
		or	bh, bh
		jz	short loc_14EA1
		mov	dx, 0A1h ; '¡'
		mov	bl, bh

loc_14EA1:				; CODE XREF: sb_14700+79Aj
		not	bl
		in	al, dx		; Interrupt Controller #2, 8259A
		and	al, bl
		out	dx, al		; Interrupt Controller #2, 8259A
		pop	gs
		pop	fs
		pop	es
		popad
		dec	[byte_24620]
		pop	ds
		pop	dx
		pop	ax
		iret
; ---------------------------------------------------------------------------

loc_14EB7:				; CODE XREF: sb_14700+725j
		and	[byte_24672], 0EFh
		jmp	loc_14E29
; END OF FUNCTION CHUNK	FOR sb_14700
; ---------------------------------------------------------------------------
		mov	al, 20h	; ' '
		cmp	[irq_number], 7
		jbe	short loc_14ECC
		out	0A0h, al	; PIC 2	 same as 0020 for PIC 1
		jmp	short $+2

loc_14ECC:				; CODE XREF: seg000:4EC6j
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		pop	dx
		pop	ax
		iret
; ---------------------------------------------------------------------------

sb_sndoff:				; DATA XREF: seg003:0D38o
		cmp	[freq1], 23000
		jnb	sbpro_sndoff
		pushf
		cli
		cmp	[byte_2466E], 1
		jnz	short loc_14F09
		cli
		mov	dx, [sb_base_port]
		add	dl, 0Ch

loc_14EED:				; CODE XREF: seg000:4EF0j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14EED
		mov	al, 0D0h ; 'Ð'
		out	dx, al		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.

loc_14EF5:				; CODE XREF: seg000:4EF8j
		in	al, dx		; DMA controller, 8237A-5.
					; clear	byte pointer flip-flop.
		or	al, al
		js	short loc_14EF5
		call	restore_intvector
		mov	cl, [dma_chn_mask]
		call	set_dmachn_mask
		mov	[byte_2466E], 0

loc_14F09:				; CODE XREF: seg000:4EE3j
		popf
		retn
; ---------------------------------------------------------------------------

sb_clean:				; DATA XREF: seg003:0D4Eo
		call	sub_18A28
		call	sbsound_off
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_14F12 far		; CODE XREF: sub_14FBC+22j
					; sub_14FBC+33j ...
		cmp	[cs:byte_14F70], 0
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

loc_14F3C:				; CODE XREF: sub_14F12+6j
		mov	[cs:word_14F6C], 1
		jmp	[cs:int8addr]
endp		sub_14F12

; ---------------------------------------------------------------------------
		dec	[cs:byte_14F73]
		jz	short loc_14F50
		iret
; ---------------------------------------------------------------------------

loc_14F50:				; CODE XREF: seg000:4F4Dj
		push	ax
		mov	al, [cs:byte_14F72]
		mov	[cs:byte_14F73], al
		mov	ax, [cs:timer_word_14F6E]
		call	some_13DC1
		pop	ax
		jmp	[cs:int8addr]
; ---------------------------------------------------------------------------
; ---------------------------------------------------------------------------
int8addr	dd 0			; DATA XREF: sub_12DA8+6Aw
					; sub_12FB4+5r	...
word_14F6C	dw 0			; DATA XREF: sub_12FCD+1Bw
					; memfill8080+Dw ...
timer_word_14F6E dw 0			; DATA XREF: some_13DC1w seg000:4F59r
byte_14F70	db 0			; DATA XREF: sub_12FCD+12w
					; memfill8080+7w ...
byte_14F71	db 0			; DATA XREF: sub_12D35:loc_12D41w
					; sub_12D35:loc_12D4Ew
byte_14F72	db 0			; DATA XREF: sub_13CF6+Dw seg000:4F51r
byte_14F73	db 0			; DATA XREF: sub_13CF6+11w
					; seg000:4F48w	...
; ---------------------------------------------------------------------------

check_covox:				; DATA XREF: seg003:0D0Eo
		mov	[sndflags_24622], 3
		mov	[byte_24623], 0
		mov	[bit_mode], 8
		cmp	[snd_base_port], 0FFFFh
		jnz	short loc_14F95
		xor	ax, ax
		mov	es, ax
		assume es:nothing
		mov	ax, [es:408h]
		mov	[snd_base_port], ax

loc_14F95:				; CODE XREF: seg000:4F88j
		mov	ax, [snd_base_port]
		mov	[cs:word_14FC8], ax
		pushf
		cli
		mov	dx, offset sub_14FBC
		call	set_timer_int
		sub	ax, 0F00h
		mov	[cs:word_14FC0], ax
		mov	[cs:word_14FC5], 0F000h
		popf
		clc
		retn

; =============== S U B	R O U T	I N E =======================================


proc		set_covox near		; DATA XREF: seg003:0D24o
		call	sub_12FCD
		retn
endp		set_covox

; ---------------------------------------------------------------------------

; =============== S U B	R O U T	I N E =======================================


proc		sub_14FBC far		; DATA XREF: seg000:4F9Eo
		push	ax
		push	dx
		push	ds
; ---------------------------------------------------------------------------
		db 0BAh	; º		; self moifying
word_14FC0	dw 1000h		; DATA XREF: seg000:4FA7w
; ---------------------------------------------------------------------------
		mov	ds, dx
; ---------------------------------------------------------------------------
		assume ds:nothing
		db 0A0h	;  
word_14FC5	dw 1234h		; DATA XREF: seg000:4FABw
					; sub_14FBC+16w ...
		db 0BAh	; º
word_14FC8	dw 378h			; DATA XREF: seg000:4F98w
; ---------------------------------------------------------------------------
		out	dx, al		; Printer Data Latch:
					; send byte to printer
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		assume ds:seg003
		pop	dx
		pop	ax
		inc	[cs:word_14FC5]
		jz	short loc_14FE3
		dec	[cs:word_14F6C]
		jz	near ptr sub_14F12
		iret
; ---------------------------------------------------------------------------

loc_14FE3:				; CODE XREF: sub_14FBC+1Bj
		mov	[cs:word_14FC5], 0F000h
		dec	[cs:word_14F6C]
		jz	near ptr sub_14F12
		iret
endp		sub_14FBC ; sp-analysis	failed

; ---------------------------------------------------------------------------

covox_sndoff:				; DATA XREF: seg003:0D3Ao
		call	memfill8080
		retn
; ---------------------------------------------------------------------------

covox_clean:				; DATA XREF: seg003:0D50o
		call	sub_12FB4
		retn
; ---------------------------------------------------------------------------

check_stereo:				; DATA XREF: seg003:0D10o
		mov	[sndflags_24622], 3
		mov	[byte_24623], 1
		mov	[bit_mode], 8
		cmp	[snd_base_port], 0FFFFh
		jnz	short loc_1501D
		xor	ax, ax
		mov	es, ax
		mov	ax, [es:408h]
		mov	[snd_base_port], ax

loc_1501D:				; CODE XREF: seg000:5010j
		mov	ax, [snd_base_port]
		add	ax, 2
		mov	[cs:word_1504D], ax
		pushf
		cli
		mov	dx, offset sub_15044
		call	set_timer_int
		sub	ax, 0F00h
		mov	[word ptr cs:loc_15047+1], ax
		mov	[cs:word_15056], 0F000h
		popf
		clc
		retn

; =============== S U B	R O U T	I N E =======================================


proc		set_stereoon near	; DATA XREF: seg003:off_252C6o
		call	sub_12FCD
		retn
endp		set_stereoon


; =============== S U B	R O U T	I N E =======================================


proc		sub_15044 far		; DATA XREF: seg000:5029o
		push	ax
		push	dx
		push	ds

loc_15047:				; DATA XREF: seg000:5032w
		mov	dx, seg000
		mov	ds, dx
; ---------------------------------------------------------------------------
		assume ds:seg000
		db 0BAh	; º
word_1504D	dw 37Ah			; DATA XREF: seg000:5023w
; ---------------------------------------------------------------------------
		mov	al, 2
		out	dx, al
		sub	dl, 2
; ---------------------------------------------------------------------------
		db 0A1h	; ¡
word_15056	dw 1234h		; DATA XREF: seg000:5036w
					; sub_15044+28w ...
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
		add	[cs:word_15056], 2
		jb	short loc_1507E
		dec	[cs:word_14F6C]
		jz	near ptr sub_14F12
		iret
; ---------------------------------------------------------------------------

loc_1507E:				; CODE XREF: sub_15044+2Ej
		mov	[cs:word_15056], 0F000h
		dec	[cs:word_14F6C]
		jz	near ptr sub_14F12
		iret
endp		sub_15044 ; sp-analysis	failed

; ---------------------------------------------------------------------------

stereoon_sndoff:			; DATA XREF: seg003:0D3Co
		call	memfill8080
		retn
; ---------------------------------------------------------------------------

stereoon_clean:				; DATA XREF: seg003:0D52o
		call	sub_12FB4
		retn
; ---------------------------------------------------------------------------

adlib_check:				; DATA XREF: seg003:0D12o
		mov	[sndflags_24622], 0Bh
		mov	[byte_24623], 0
		mov	[bit_mode], 8
		call	sub_18389
		mov	ax, 2120h
		call	adlib_18395
		mov	ax, 0F060h
		call	adlib_18395
		mov	ax, 0F080h
		call	adlib_18395
		mov	ax, 1C0h
		call	adlib_18395
		mov	ax, 0E0h ; 'à'
		call	adlib_18395
		mov	ax, 3F43h
		call	adlib_18395
		mov	ax, 0B0h ; '°'
		call	adlib_18395
		mov	ax, 0A0h ; ' '
		call	adlib_18395
		mov	ax, 8FA0h
		call	adlib_18395
		mov	ax, 2EB0h
		call	adlib_18395
		mov	cx, 4000h

loc_150E8:				; CODE XREF: seg000:50E9j
		dec	cx
		jnz	short loc_150E8
		mov	ax, 20B0h
		call	adlib_18395
		mov	ax, 0A0h ; ' '
		call	adlib_18395
		mov	ax, 40h	; '@'
		call	adlib_18395
		pushf
		cli
		mov	dx, offset loc_1511C
		call	set_timer_int
		sub	ax, 0F00h
		mov	[word ptr cs:loc_15120+1], ax
		mov	[cs:word_15126], 0F000h
		popf
		clc
		retn

; =============== S U B	R O U T	I N E =======================================


proc		set_adlib near		; DATA XREF: seg003:0D28o
		call	sub_12FCD
		retn
endp		set_adlib

; ---------------------------------------------------------------------------

loc_1511C:				; DATA XREF: seg000:50FFo
		push	ax
		push	bx
		push	dx
		push	ds

loc_15120:				; DATA XREF: seg000:5108w
		mov	ax, 1234h	; self modifying
		mov	ds, ax
; ---------------------------------------------------------------------------
		assume ds:nothing
		db 0A0h	;  		; self modifying
word_15126	dw 1234h		; DATA XREF: seg000:510Cw seg000:5135w ...
; ---------------------------------------------------------------------------
		mov	bx, seg003
		mov	ds, bx
		assume ds:seg003
		mov	bx, offset table_24898
		xlat
		mov	dx, 389h
		out	dx, al
		inc	[cs:word_15126]
		jz	short loc_1514E

loc_1513C:				; CODE XREF: seg000:5155j
		pop	ds
		pop	dx
		pop	bx
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ax
		dec	[cs:word_14F6C]
		jz	near ptr sub_14F12
		iret
; ---------------------------------------------------------------------------

loc_1514E:				; CODE XREF: seg000:513Aj
		mov	[cs:word_15126], 0F000h
		jmp	short loc_1513C
; ---------------------------------------------------------------------------

adlib_sndoff:				; DATA XREF: seg003:0D3Eo
		call	memfill8080
		retn
; ---------------------------------------------------------------------------

adlib_clean:				; DATA XREF: seg003:0D54o
		call	sub_12FB4
		call	sub_18389
		retn
; ---------------------------------------------------------------------------

check_pc:				; DATA XREF: seg003:0D14o
		mov	[sndflags_24622], 3
		mov	[byte_24623], 0
		mov	[bit_mode], 8
		pushf
		cli
		mov	al, 90h	; ''
		out	43h, al		; Timer	8253-5 (AT: 8254.2).
		mov	dx, offset pc_interrupt
		call	set_timer_int
		sub	ax, 0F00h
		mov	[cs:word_1519B], ax
		mov	[cs:word_151A3], 0F000h
		popf
		clc
		retn

; =============== S U B	R O U T	I N E =======================================


proc		set_pc near		; DATA XREF: seg003:0D2Ao
		in	al, 61h		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÍËÍ OR	03H=spkr ON
					; 1: Tmr 2 data	Í¼  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		or	al, 3
		out	61h, al		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÍËÍ OR	03H=spkr ON
					; 1: Tmr 2 data	Í¼  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		call	sub_12FCD
		retn
endp		set_pc

; ---------------------------------------------------------------------------

pc_interrupt:				; DATA XREF: seg000:5177o
		push	bx
		push	ds
; ---------------------------------------------------------------------------
		db 0BBh	; »
word_1519B	dw 1000h		; DATA XREF: seg000:5180w
; ---------------------------------------------------------------------------
		mov	ds, bx
		xor	bh, bh
; ---------------------------------------------------------------------------
		db  8Ah	; Š
		db  1Eh
word_151A3	dw 1234h		; DATA XREF: seg000:5184w seg000:51B8w ...
; ---------------------------------------------------------------------------
		mov	bl, [cs:byte_151E8+bx]
		mov	bh, al
		mov	al, bl
		out	42h, al		; Timer	8253-5 (AT: 8254.2).
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		mov	al, bh
		pop	ds
		pop	bx
		inc	[cs:word_151A3]
		jz	short loc_151C9
		dec	[cs:word_14F6C]
		jz	near ptr sub_14F12
		iret
; ---------------------------------------------------------------------------

loc_151C9:				; CODE XREF: seg000:51BDj
		mov	[cs:word_151A3], 0F000h
		dec	[cs:word_14F6C]
		jz	near ptr sub_14F12
		iret
; ---------------------------------------------------------------------------

pc_sndoff:				; DATA XREF: seg003:0D40o
		call	memfill8080
		in	al, 61h		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÍËÍ OR	03H=spkr ON
					; 1: Tmr 2 data	Í¼  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		and	al, 0FCh
		out	61h, al		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÍËÍ OR	03H=spkr ON
					; 1: Tmr 2 data	Í¼  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		retn
; ---------------------------------------------------------------------------

pc_clean:				; DATA XREF: seg003:0D56o
		call	sub_12FB4
		retn
; ---------------------------------------------------------------------------
byte_151E8	db 40h			; DATA XREF: seg000:51A5r
		db 40h
		db 40h
		db 40h
		db 40h
		db 40h
		db 40h
		db 40h
		db 40h
		db 40h
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Fh
		db 3Eh
		db  3Eh	; >
		db  3Eh	; >
		db  3Eh	; >
		db  3Eh	; >
		db  3Eh	; >
		db  3Eh	; >
		db  3Eh	; >
		db  3Eh	; >
		db  3Eh	; >
		db  3Dh	; =
		db  3Dh	; =
		db  3Dh	; =
		db 3Dh
		db  3Dh	; =
		db  3Dh	; =
		db 3Dh
		db  3Dh	; =
		db  3Dh	; =
		db 3Ch
		db  3Ch	; <
		db 3Ch
		db  3Ch	; <
		db 3Ch
		db  3Ch	; <
		db 3Ch
		db  3Ch	; <
		db 3Ch
		db  3Ch	; <
		db 3Bh
		db  3Bh	; ;
		db 3Bh
		db  3Bh	; ;
		db 3Bh
		db  3Bh	; ;
		db 3Bh
		db  3Bh	; ;
		db 3Bh
		db  3Bh	; ;
		db 3Ah
		db  3Ah	; :
		db 3Ah
		db  3Ah	; :
		db 3Ah
		db  3Ah	; :
		db 3Ah
		db  3Ah	; :
		db 3Ah
		db  3Ah	; :
		db 39h
		db  39h	; 9
		db 39h
		db  39h	; 9
		db 39h
		db  39h	; 9
		db 39h
		db  39h	; 9
		db 39h
		db  39h	; 9
		db 38h
		db  38h	; 8
		db 38h
		db  38h	; 8
		db 38h
		db  38h	; 8
		db 38h
		db  38h	; 8
		db 37h
		db 37h
		db 37h
		db 37h
		db 37h
		db 36h
		db  36h	; 6
		db  36h	; 6
		db  36h	; 6
		db  35h	; 5
		db  35h	; 5
		db  35h	; 5
		db 35h
		db  34h	; 4
		db  34h	; 4
		db 34h
		db  33h	; 3
		db 33h
		db  32h	; 2
		db 32h
		db  31h	; 1
		db 31h
		db  30h	; 0
		db 30h
		db  2Fh	; /
		db 2Eh
		db  2Dh	; -
		db  2Ch	; ,
		db  2Bh	; +
		db 2Ah
		db  29h	; )
		db 28h
		db  27h	; '
		db 26h
		db  25h	; %
		db  24h	; $
		db  23h	; #
		db 22h
		db  21h	; !
		db 20h
		db  1Fh
		db 1Eh
; START	OF FUNCTION CHUNK FOR sub_141F6
byte_1526B	db 1Dh			; CODE XREF: sub_141F6+13j
		db  1Ch
		db  1Bh
		db 1Ah
		db  19h
		db 18h
		db  17h
		db 16h
		db 15h
		db  14h
		db  13h
		db 12h
		db  11h
		db 11h
		db  10h
		db 10h
		db  0Fh
		db 0Fh
		db  0Eh
		db 0Eh
		db 0Dh
		db  0Dh
		db  0Dh
		db 0Ch
		db  0Ch
		db 0Ch
		db  0Ch
		db 0Bh
		db  0Bh
		db 0Bh
		db  0Bh
		db 0Ah
		db  0Ah
		db 0Ah
		db  0Ah
		db 0Ah
		db    9
		db 9
		db    9
		db 9
		db    9
		db 9
		db    9
		db 9
		db    9
		db 8
		db    8
		db 8
		db    8
		db 8
		db    8
		db 8
		db    8
		db 8
		db    8
		db 8
		db    8
		db 7
		db 7
		db 7
		db 7
		db 7
		db 7
		db 7
		db 6
		db 6
		db 6
		db 6
		db 6
		db 6
		db 6
		db 6
		db 6
		db 6
		db 6
		db 5
		db    5
		db    5
		db 5
		db    5
		db    5
		db 5
		db    5
		db    5
		db 5
		db    4
		db    4
		db 4
		db    4
		db 4
		db    4
		db 4
		db    4
		db 4
		db    4
		db 3
		db    3
		db 3
		db    3
		db 3
		db    3
		db 3
		db    3
		db 3
		db    3
		db 2
		db    2
		db 2
		db    2
		db 2
		db    2
		db 2
		db    2
		db 2
		db    1
		db 1
		db    1
		db 1
		db    1
		db 1
		db    1
		db 1
		db    1
		db 1
		db    1
; ---------------------------------------------------------------------------

check_midi:				; DATA XREF: seg003:0D16o
		mov	[sndflags_24622], 12h
		mov	[byte_24623], 1
		mov	[bit_mode], 8
		mov	ax, [snd_base_port]
		cmp	ax, 0FFFFh
		jnz	short loc_15302
		mov	ax, 330h

loc_15302:				; CODE XREF: sub_141F6+1107j
		mov	[word_2465C], ax
		mov	[snd_base_port], ax
		mov	[off_245CA], offset locret_1544C
		mov	[off_245C8], offset loc_15466
		mov	[off_245CC], offset sub_154AC
		mov	[off_245CE], offset sub_1544D
		mov	bx, offset byte_25908
		mov	ah, 1

loc_15325:				; CODE XREF: sub_141F6+1146j
		mov	al, ah
		and	al, 0Fh
		mov	[bx+18h], al
		and	[byte ptr bx+17h], 0FEh
		mov	[byte ptr bx+35h], 0
		add	bx, 50h	; 'P'
		inc	ah
		cmp	ah, 10h
		jbe	short loc_15325
		call	sub_153C0
		call	sub_153D6
		clc
		retn
; END OF FUNCTION CHUNK	FOR sub_141F6

; =============== S U B	R O U T	I N E =======================================


proc		set_midi near		; DATA XREF: seg003:0D2Co
		mov	bx, offset int8p
		mov	dx, cs
		mov	al, 8
		call	setint_vect
		retn
endp		set_midi

; ---------------------------------------------------------------------------

; =============== S U B	R O U T	I N E =======================================


proc		int8p far		; DATA XREF: set_midio
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
		cmp	[byte_24671], 1
		jz	short loc_1539A
		inc	[byte_24668]
		mov	al, [byte_24668]
		cmp	al, [byte_24667]
		jnb	short loc_1538F
		mov	bx, offset byte_25908
		mov	cx, [word_245D4]

loc_15380:				; CODE XREF: int8p+37j
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

loc_1538F:				; CODE XREF: int8p+23j
		mov	[byte_24668], 0
		call	sub_135CA
		call	loc_14111

loc_1539A:				; CODE XREF: int8p+16j	int8p+39j
		pop	gs
		pop	fs
		pop	es
		pop	ds
		popad
		iret
endp		int8p

; ---------------------------------------------------------------------------

midi_sndoff:				; DATA XREF: seg003:0D42o
		mov	dx, [word ptr cs:int8addr+2]
		mov	bx, [word ptr cs:int8addr]
		mov	al, 8
		call	setint_vect
		call	timer_13DD5
		call	sub_153D6
		retn
; ---------------------------------------------------------------------------

midi_clean:				; DATA XREF: seg003:0D58o
		mov	ah, 0FFh
		call	sub_153F1
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_153C0 near		; CODE XREF: sub_141F6+1148p
		mov	ah, 0FFh
		call	sub_153F1
		mov	cx, 8000h
		call	sub_15442
		mov	ah, 3Fh	; '?'
		call	sub_153F1
		xor	cx, cx
		call	sub_15442
		retn
endp		sub_153C0


; =============== S U B	R O U T	I N E =======================================


proc		sub_153D6 near		; CODE XREF: sub_141F6+114Bp
					; seg000:53B6p
		xor	bl, bl

loc_153D8:				; CODE XREF: sub_153D6+18j
		mov	ah, 0B0h ; '°'
		or	ah, bl
		call	sub_15413
		mov	ah, 7Bh	; '{'
		call	sub_15413
		xor	ah, ah
		call	sub_15413
		inc	bl
		cmp	bl, 10h
		jb	short loc_153D8
		retn
endp		sub_153D6


; =============== S U B	R O U T	I N E =======================================


proc		sub_153F1 near		; CODE XREF: seg000:53BCp sub_153C0+2p ...
		mov	dx, [word_2465C]
		inc	dx
		xor	cx, cx

loc_153F8:				; CODE XREF: sub_153F1+Dj
		in	al, dx
		test	al, 40h
		jz	short loc_15401
		dec	cx
		jnz	short loc_153F8
		retn
; ---------------------------------------------------------------------------

loc_15401:				; CODE XREF: sub_153F1+Aj
		mov	al, ah
		out	dx, al
		xor	cx, cx

loc_15406:				; CODE XREF: sub_153F1+1Bj
		in	al, dx
		shl	al, 1
		jnb	short loc_1540E
		dec	cx
		jnz	short loc_15406

loc_1540E:				; CODE XREF: sub_153F1+18j
		dec	dx
		in	al, dx
		cmp	al, 0FEh ; 'þ'
		retn
endp		sub_153F1


; =============== S U B	R O U T	I N E =======================================


proc		sub_15413 near		; CODE XREF: sub_153D6+6p sub_153D6+Bp ...
		or	ah, ah
		jns	short loc_15421
		cmp	ah, [byte_24677]
		jz	short locret_15441
		mov	[byte_24677], ah

loc_15421:				; CODE XREF: sub_15413+2j
		mov	dx, [word_2465C]
		inc	dx
		mov	cl, 0FFh

loc_15428:				; CODE XREF: sub_15413+23j
		in	al, dx
		test	al, 40h
		jz	short loc_15439
		shl	al, 1
		jb	short loc_15434
		dec	dx
		in	al, dx
		inc	dx

loc_15434:				; CODE XREF: sub_15413+1Cj
		dec	cl
		jnz	short loc_15428
		retn
; ---------------------------------------------------------------------------

loc_15439:				; CODE XREF: sub_15413+18j
		dec	dx
		mov	al, ah
		out	dx, al
		sub	[byte_24678], al

locret_15441:				; CODE XREF: sub_15413+8j
		retn
endp		sub_15413


; =============== S U B	R O U T	I N E =======================================


proc		sub_15442 near		; CODE XREF: sub_153C0+8p
					; sub_153C0+12p
		mov	dx, [word_2465C]
		inc	dx

loc_15447:				; CODE XREF: sub_15442+7j
		in	al, dx
		dec	cx
		jnz	short loc_15447
		retn
endp		sub_15442

; ---------------------------------------------------------------------------

locret_1544C:				; DATA XREF: sub_141F6+1112o
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_1544D near		; CODE XREF: seg000:546Cp
					; DATA XREF: sub_141F6+1124o
		and	[byte ptr bx+17h], 0FEh
		call	sub_154DA
		or	ah, 80h
		call	sub_15413
		call	sub_154DE
		call	sub_15413
		mov	ah, 7Fh	; ''
		call	sub_15413
		retn
endp		sub_1544D

; ---------------------------------------------------------------------------

loc_15466:				; DATA XREF: sub_141F6+1118o
		test	[byte ptr bx+17h], 0FEh
		jz	short loc_1546F
		call	sub_1544D

loc_1546F:				; CODE XREF: seg000:546Aj
		or	[byte ptr bx+17h], 1
		mov	al, [bx+2]
		cmp	al, [bx+3]
		jz	short loc_1548D
		mov	[bx+3],	al
		call	sub_154DA
		or	ah, 0C0h
		call	sub_15413
		mov	ah, [bx+2]
		call	sub_15413

loc_1548D:				; CODE XREF: seg000:5479j
		mov	al, [bx+8]
		call	sub_154AC
		call	sub_154DA
		or	ah, 90h
		call	sub_15413
		call	sub_154DE
		call	sub_15413
		mov	ah, 7Fh	; ''
		call	sub_15413
		or	[byte ptr bx+17h], 1
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_154AC near		; CODE XREF: seg000:5490p
					; DATA XREF: sub_141F6+111Eo
		cmp	al, [byte_2467D]
		jb	short loc_154B5
		mov	al, [byte_2467D]

loc_154B5:				; CODE XREF: sub_154AC+4j
		cmp	al, [bx+1Bh]
		jz	short locret_154D9
		mov	[bx+1Bh], al
		movzx	di, al
		call	sub_154DA
		or	ah, 0B0h
		call	sub_15413
		mov	ah, 7
		call	sub_15413
		mov	al, 80h	; '€'
		add	di, [off_24656]
		mul	[byte ptr di]
		call	sub_15413

locret_154D9:				; CODE XREF: sub_154AC+Cj
		retn
endp		sub_154AC


; =============== S U B	R O U T	I N E =======================================


proc		sub_154DA near		; CODE XREF: sub_1544D+4p seg000:547Ep ...
		mov	ah, [bx+18h]
		retn
endp		sub_154DA


; =============== S U B	R O U T	I N E =======================================


proc		sub_154DE near		; CODE XREF: sub_1544D+Dp seg000:549Cp
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
endp		sub_154DE


; =============== S U B	R O U T	I N E =======================================


proc		sub_154F4 near		; CODE XREF: sub_15577+9p sub_1609F+9p
		mov	ax, [word_245E4]
		shr	ax, 4
		mov	[byte_24683], al
		push	bx
		push	si
		mov	bx, [si+26h]
		mov	eax, [si+4]
		shr	eax, 16h
		add	bx, ax
		call	sub_11E8B
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
		mov	[word_24614], ax
		mov	[byte_24616], 0
		test	[byte_24672], 10h
		jz	short loc_1554E
		cmp	al, ah
		setnz	ah		; dosbox:  setnz sp
		mov	[byte_24616], ah
		movzx	ebx, al

loc_1554E:				; CODE XREF: sub_154F4+4Bj
		shl	ebx, 9
		add	bx, offset byte_28308
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
		test	[byte_24672], 10h
		jnz	loc_157F2
		cmp	[byte_24625], 1
		jz	loc_15E48
		xor	edx, edx
		mov	ax, [word_245E4]
		and	eax, 0Fh
		jmp	[cs:off_18E20+eax*2]
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
		cmp	[byte_24683], 0
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
		add	di, 80h	; '€'
		dec	[byte_24683]
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

loc_157F2:				; CODE XREF: sub_15577+11j
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
		jmp	[cs:off_18E40+eax*2]

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
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_15577
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
byte_15B46	db 0			; DATA XREF: sub_15577+2BCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di], eax
		add	di, 8
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15B52:				; CODE XREF: sub_15577+28j
					; sub_15577+311j ...
		cmp	[byte_24683], 0
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
		db  80h	; €
		db 0C1h	; Á
byte_15B81	db 0			; DATA XREF: sub_15577+2C0w
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
		db  80h	; €
		db 0C1h	; Á
byte_15BAD	db 0			; DATA XREF: sub_15577+2C4w
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
		db  80h	; €
		db 0C1h	; Á
byte_15BDA	db 0			; DATA XREF: sub_15577+2C8w
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
		db  80h	; €
		db 0C1h	; Á
byte_15C07	db 0			; DATA XREF: sub_15577+2CCw
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
		db  80h	; €
		db 0C1h	; Á
byte_15C34	db 0			; DATA XREF: sub_15577+2D0w
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
		db  80h	; €
		db 0C1h	; Á
byte_15C61	db 0			; DATA XREF: sub_15577+2D4w
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
		db  80h	; €
		db 0C1h	; Á
byte_15C8E	db 0			; DATA XREF: sub_15577+2D8w
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
		db  80h	; €
		db 0C1h	; Á
byte_15CBB	db 0			; DATA XREF: sub_15577+2DCw
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
		db  80h	; €
		db 0C1h	; Á
byte_15CE8	db 0			; DATA XREF: sub_15577+2E0w
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
		db  80h	; €
		db 0C1h	; Á
byte_15D15	db 0			; DATA XREF: sub_15577+2E4w
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
		db  80h	; €
		db 0C1h	; Á
byte_15D42	db 0			; DATA XREF: sub_15577+2E8w
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
		db  80h	; €
		db 0C1h	; Á
byte_15D6F	db 0			; DATA XREF: sub_15577+2ECw
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
		db  80h	; €
		db 0C1h	; Á
byte_15D9C	db 0			; DATA XREF: sub_15577+2F0w
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
		db  80h	; €
		db 0C1h	; Á
byte_15DC9	db 0			; DATA XREF: sub_15577+2F4w
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
		db  80h	; €
		db 0C1h	; Á
byte_15DF6	db 0			; DATA XREF: sub_15577+2F8w
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
		db  80h	; €
		db 0C1h	; Á
byte_15E23	db 0			; DATA XREF: sub_15577+2FCw
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		add	[di+78h], eax
		add	di, 80h	; '€'
		mov	dx, offset loc_15E3D
		cmp	[byte_24616], 1
		jz	loc_1690B

loc_15E3D:				; DATA XREF: seg000:5E31o
		dec	[byte_24683]
		jnz	loc_15B5B
		jmp	loc_1578C
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_15577

loc_15E48:				; CODE XREF: sub_15577+1Aj
		xor	edx, edx
		mov	ax, [word_245E4]
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
		cmp	[byte_24683], 0
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
		add	di, 80h	; '€'
		dec	[byte_24683]
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
		test	[byte_24672], 10h
		jnz	loc_162B7
		cmp	[byte_24625], 1
		jz	loc_16959
		xor	edx, edx
		mov	ax, [word_245E4]
		and	eax, 0Fh
		jmp	[cs:off_18DC0+eax*2]
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

loc_16165:				; CODE XREF: sub_141F6+13j
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
					; DATA XREF: seg000:off_18DC0o
		cmp	[byte_24683], 0
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
		add	di, 80h	; '€'
		dec	[byte_24683]
		jnz	loc_161C9
		jmp	loc_1578C
; ---------------------------------------------------------------------------

loc_162B7:				; CODE XREF: sub_1609F+11j
		mov	al, ch
		cmp	al, [cs:byte_16379]
		jz	short loc_1633C
		mov	[cs:byte_16379], al
		mov	[cs:byte_163A8], al
		mov	[cs:byte_163D7], al
		mov	[cs:byte_16406], al
		mov	[cs:byte_16435], al
		mov	[byte ptr cs:unk_16464], al
		mov	[cs:byte_16493], al
		mov	[cs:byte_164C2], al
		mov	[cs:byte_164F1], al
		mov	[cs:byte_16520], al
		mov	[cs:byte_1654F], al
		mov	[cs:byte_1657E], al
		mov	[cs:byte_165AD], al
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
		jmp	[cs:off_18DE0+eax*2]

loc_16356:				; CODE XREF: sub_1609F+28j
					; DATA XREF: seg000:8DFEo
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde
		movsx	edx, [word ptr ebx+edx*2]

loc_16369:				; CODE XREF: sub_141F6+13j
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db 80h
		db 0C1h	; Á
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
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
byte_165AD	db 0			; DATA XREF: sub_1609F+251w
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
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; END OF FUNCTION CHUNK	FOR sub_1609F
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
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
		cmp	[byte_24683], 0
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
		db  80h	; €
		db 0C1h	; Á
byte_16646	db 0			; DATA XREF: sub_1609F+25Dw
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
		db  80h	; €
		db 0C1h	; Á
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
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
byte_1669F	db 0			; DATA XREF: sub_1609F+265w
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
		db  80h	; €
		db 0C1h	; Á
byte_166CC	db 0			; DATA XREF: sub_1609F+269w
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
		db  80h	; €
		db 0C1h	; Á
byte_166F9	db 0			; DATA XREF: sub_1609F+26Dw
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
		db  80h	; €
		db 0C1h	; Á
byte_16726	db 0			; DATA XREF: sub_1609F+271w
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
		db  80h	; €
		db 0C1h	; Á
byte_16753	db 0			; DATA XREF: sub_1609F+275w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+30h], eax
		mov	dl, [es:si]
		mov	ax, [ebx+edx*2]
		mov	dl, [es:si+1]
		cwde

loc_1676A:				; CODE XREF: sub_141F6+13j
					; sub_141F6+13j
		movsx	edx, [word ptr ebx+edx*2]
		sub	edx, eax
		imul	edx, ecx
		sar	edx, 8
		add	eax, edx
; ---------------------------------------------------------------------------
		db  80h	; €
		db 0C1h	; Á
byte_16780	db 0			; DATA XREF: sub_1609F+279w
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
		db  80h	; €
		db 0C1h	; Á
byte_167AD	db 0			; DATA XREF: sub_1609F+27Dw
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
		db  80h	; €
		db 0C1h	; Á
byte_167DA	db 0			; DATA XREF: sub_1609F+281w
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
		db  80h	; €
		db 0C1h	; Á
byte_16807	db 0			; DATA XREF: sub_1609F+285w
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
		db  80h	; €
		db 0C1h	; Á
byte_16834	db 0			; DATA XREF: sub_1609F+289w
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
		db  80h	; €
		db 0C1h	; Á
byte_16861	db 0			; DATA XREF: sub_1609F+28Dw
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
		db  80h	; €
		db 0C1h	; Á
byte_1688E	db 0			; DATA XREF: sub_1609F+291w
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
		db  80h	; €
		db 0C1h	; Á
byte_168BB	db 0			; DATA XREF: sub_1609F+295w
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
		db  80h	; €
		db 0C1h	; Á
byte_168E8	db 0			; DATA XREF: sub_1609F+299w
; ---------------------------------------------------------------------------
		adc	si, bp
		xor	edx, edx
		mov	[di+78h], eax
		add	di, 80h	; '€'
		mov	dx, offset loc_16900
		cmp	[byte_24616], 1
		jz	short loc_1690B

loc_16900:				; DATA XREF: seg000:68F6o
		dec	[byte_24683]
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
		mov	[byte ptr word_24614], al
		movzx	ebx, al
		shl	ebx, 9
		add	bx, offset byte_28308
		jmp	dx
; ---------------------------------------------------------------------------

loc_16929:				; CODE XREF: seg000:6910j
		sub	al, 4
		jbe	short loc_16942
		cmp	al, ah
		jbe	short loc_16942
		mov	[byte ptr word_24614], al
		movzx	ebx, al
		shl	ebx, 9
		add	bx, offset byte_28308
		jmp	dx
; ---------------------------------------------------------------------------

loc_16942:				; CODE XREF: seg000:6916j seg000:692Bj ...
		mov	[byte ptr word_24614], ah
		mov	[byte_24616], 0
		movzx	ebx, ah
		shl	ebx, 9
		add	bx, offset byte_28308
		jmp	dx
; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_1609F

loc_16959:				; CODE XREF: sub_1609F+1Aj
		xor	edx, edx
		mov	ax, [word_245E4]
		and	eax, 0Fh

loc_16963:				; CODE XREF: sub_141F6+13j
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
		cmp	[byte_24683], 0
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
		add	di, 80h	; '€'
		dec	[byte_24683]
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
		add	di, 80h	; '€'
		dec	cx

loc_16C66:				; CODE XREF: sub_141F6+13j
		jnz	short loc_16C22

locret_16C68:				; CODE XREF: sub_1609F:loc_16C20j
		retn
; END OF FUNCTION CHUNK	FOR sub_1609F

; =============== S U B	R O U T	I N E =======================================


proc		sub_16C69 near		; CODE XREF: sub_13017:loc_13038p
					; sb_14700+783p ...

; FUNCTION CHUNK AT 71D3 SIZE 0000008C BYTES
; FUNCTION CHUNK AT 77EF SIZE 00000035 BYTES

		call	sub_11E47
		cld
		mov	ax, [word_245E8]
		mov	[word_245E4], ax
		dec	[word_245EE]
		jnz	short loc_16C88
		call	sub_140B6
		mov	ax, [word_245EA]
		mov	[word_245E4], ax
		mov	ax, [word_245EC]
		mov	[word_245EE], ax

loc_16C88:				; CODE XREF: sub_16C69+Ej
		mov	[byte_24682], 0
		cmp	[byte_24623], 1
		jz	loc_171D3
		mov	si, offset byte_25908
		mov	cx, [word_245D4]

loc_16C9D:				; CODE XREF: sub_16C69+59j
		cmp	[byte ptr si+1Dh], 0
		jnz	short loc_16CBE
		push	cx
		push	si
		mov	di, offset chrin
		test	[byte_24682], 1
		jnz	short loc_16CB9
		or	[byte_24682], 1
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
		mov	si, (offset chrin+1)
		mov	es, [word ptr dma_buf_pointer+2]
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
		mov	[word_24600], di
		call	sub_11E68
		retn
endp		sub_16C69


; =============== S U B	R O U T	I N E =======================================


proc		sub_16CF6 near		; CODE XREF: sub_16C69+7Ap
					; sub_16C69:loc_16CEBp
		cmp	[byte_24625], 1
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
		add	si, 80h	; '€'
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
					; eff_139B9+86j ...
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

loc_16F1D:				; CODE XREF: sub_141F6+13j
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
		add	si, 80h	; '€'
		add	di, 10h
		dec	cx
		jnz	loc_17008

locret_171D2:				; CODE XREF: sub_16CF6+30Ej
		retn
endp		sub_16CF6

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_16C69

loc_171D3:				; CODE XREF: sub_16C69+29j
		mov	cx, [word_245D4]
		mov	si, offset byte_25908

loc_171DA:				; CODE XREF: sub_16C69+5B7j
		push	cx
		push	si
		cmp	[byte ptr si+1Dh], 0
		jnz	short loc_1721A
		cmp	[byte ptr si+3Ah], 0
		jz	short loc_17202
		mov	di, [off_245E0]
		test	[byte_24682], 1
		jz	short loc_171F8
		call	sub_15577
		jmp	short loc_1721A
; ---------------------------------------------------------------------------

loc_171F8:				; CODE XREF: sub_16C69+588j
		or	[byte_24682], 1
		call	sub_1609F
		jmp	short loc_1721A
; ---------------------------------------------------------------------------

loc_17202:				; CODE XREF: sub_16C69+57Dj
		mov	di, [off_245E2]
		test	[byte_24682], 2
		jz	short loc_17212
		call	sub_15577
		jmp	short loc_1721A
; ---------------------------------------------------------------------------

loc_17212:				; CODE XREF: sub_16C69+5A2j
		or	[byte_24682], 2
		call	sub_1609F

loc_1721A:				; CODE XREF: sub_16C69+577j
					; sub_16C69+58Dj ...
		pop	si
		pop	cx
		add	si, 50h	; 'P'
		dec	cx
		jnz	short loc_171DA
		cmp	[bit_mode], 16
		jz	loc_177EF
		mov	di, [word_24600]
		mov	cx, [word_245E4]
		mov	si, (offset chrin+1)
		mov	es, [word ptr dma_buf_pointer+2]
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
		mov	[word_24600], di
		call	sub_11E68
		retn
; END OF FUNCTION CHUNK	FOR sub_16C69

; =============== S U B	R O U T	I N E =======================================


proc		sub_1725F near		; CODE XREF: sub_16C69+5E3p
					; sub_16C69:loc_17254p
		cmp	[byte_24625], 1
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
		add	si, 80h	; '€'
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

loc_1754F:				; CODE XREF: sub_141F6+13j
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

loc_177EF:				; CODE XREF: sub_16C69+5BEj
		mov	di, [word_24600]
		mov	cx, [word_245E4]
		mov	si, offset chrin
		mov	es, [word ptr dma_buf_pointer+2]
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
		mov	[word_24600], di
		call	sub_11E68
		retn
; END OF FUNCTION CHUNK	FOR sub_16C69

; =============== S U B	R O U T	I N E =======================================


proc		sub_17824 near		; CODE XREF: sub_16C69+BA8p
					; sub_16C69:loc_17819p
		cmp	[byte_24625], 1
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
		add	si, 80h	; '€'
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
		jz	nullsub_3

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


proc		nullsub_3 near		; CODE XREF: sub_1609F+1B89j
		retn
endp		nullsub_3


; =============== S U B	R O U T	I N E =======================================


proc		sub_17DC6 near		; CODE XREF: sub_11F4E+219p
					; sub_11F4E+24Bp ...
		pushf
		cli
		mov	dx, [word_24626]
		mov	al, 43h	; 'C'
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		dec	dx
		mov	al, 44h	; 'D'
		out	dx, al
		add	dl, 2
		mov	eax, edi
		shr	eax, 10h
		out	dx, al
		add	dl, 2
		in	al, dx
		popf
		retn
endp		sub_17DC6


; =============== S U B	R O U T	I N E =======================================


proc		sub_17DE8 near		; CODE XREF: sub_11F4E+234p
					; sub_11F4E+264p ...
		pushf
		cli
		mov	dx, [word_24626]
		mov	ch, al
		mov	al, 43h	; 'C'
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		dec	dx
		mov	al, 44h	; 'D'
		out	dx, al
		add	dl, 2
		mov	eax, edi
		shr	eax, 10h
		out	dx, al
		add	dl, 2
		mov	al, ch
		out	dx, al
		popf
		retn
endp		sub_17DE8


; =============== S U B	R O U T	I N E =======================================


proc		sub_17E0E near		; CODE XREF: sub_11F4E+29Bp
		pushf
		cli
		shl	edi, 1
		mov	dx, [word_24626]
		mov	al, 43h	; 'C'
		out	dx, al
		inc	dx
		mov	ax, di
		inc	ax
		out	dx, ax
		dec	dx
		mov	al, 44h	; 'D'
		out	dx, al
		add	dl, 2
		mov	eax, edi
		shr	eax, 10h
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dx, 4
		mov	ch, al
		mov	al, 43h	; 'C'
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		add	dx, 3
		in	al, dx
		mov	ah, ch
		shr	edi, 1
		popf
		retn
endp		sub_17E0E


; =============== S U B	R O U T	I N E =======================================


proc		sub_17E49 near		; CODE XREF: sub_11F4E+2C2p
		pushf
		cli
		shl	edi, 1
		mov	dx, [word_24626]
		mov	cx, ax
		mov	al, 43h	; 'C'
		out	dx, al
		inc	dx
		mov	ax, di
		out	dx, ax
		dec	dx
		mov	al, 44h	; 'D'
		out	dx, al
		add	dl, 2
		mov	eax, edi
		shr	eax, 10h
		out	dx, al
		add	dl, 2
		mov	al, cl
		out	dx, al
		sub	dx, 4
		mov	al, 43h	; 'C'
		out	dx, al
		inc	dx
		mov	ax, di
		inc	ax
		out	dx, ax
		add	dx, 3
		mov	al, ch
		out	dx, al
		shr	edi, 1
		popf
		retn
endp		sub_17E49


; =============== S U B	R O U T	I N E =======================================


proc		sub_17E86 near		; CODE XREF: seg000:loc_142DAp
					; sub_17EEC+6p	...
		mov	dx, [word_24626]
		mov	al, 4Ch	; 'L'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		sub	dl, 2
		add	dl, 4
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
		sub	dl, 4
		mov	al, 4Ch	; 'L'
		out	dx, al
		add	dl, 2
		mov	al, 1
		out	dx, al
		sub	dl, 2
		xor	edi, edi
		mov	al, 0AAh ; 'ª'
		call	sub_17DE8
		mov	edi, 10000h
		mov	al, 55h	; 'U'
		call	sub_17DE8
		xor	edi, edi
		call	sub_17DC6
		push	ax
		xor	al, al
		call	sub_17DE8
		mov	dx, [word_24626]
		mov	al, 4Ch	; 'L'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		sub	dl, 2
		pop	ax
		cmp	al, 0AAh ; 'ª'
		jz	short locret_17EEB
		stc

locret_17EEB:				; CODE XREF: sub_17E86+62j
		retn
endp		sub_17E86


; =============== S U B	R O U T	I N E =======================================


proc		sub_17EEC near		; CODE XREF: sub_12D61+1Dp
		mov	[word_24626], 323h
		call	sub_17E86
		jnb	short locret_17F2F
		mov	[word_24626], 343h
		call	sub_17E86
		jnb	short locret_17F2F
		mov	[word_24626], 313h
		call	sub_17E86
		jnb	short locret_17F2F
		mov	[word_24626], 333h
		call	sub_17E86
		jnb	short locret_17F2F
		mov	[word_24626], 353h
		call	sub_17E86
		jnb	short locret_17F2F
		mov	[word_24626], 363h
		call	sub_17E86
		jnb	short locret_17F2F
		stc

locret_17F2F:				; CODE XREF: sub_17EEC+9j
					; sub_17EEC+14j ...
		retn
endp		sub_17EEC


; =============== S U B	R O U T	I N E =======================================


proc		sub_17F30 near		; CODE XREF: seg000:42E9p
		mov	dx, [word_24626]
		mov	al, 4Ch	; 'L'
		out	dx, al
		add	dl, 2
		mov	al, 1
		out	dx, al
		sub	dl, 2
		xor	edi, edi
		mov	al, 0AAh ; 'ª'

loc_17F45:				; CODE XREF: sub_17F30+2Dj
		call	sub_17DE8
		call	sub_17DC6
		cmp	al, 0AAh ; 'ª'
		jnz	short loc_17F65
		add	edi, 40000h
		cmp	edi, 100000h
		jbe	short loc_17F45
		mov	edi, 100000h

loc_17F65:				; CODE XREF: sub_17F30+1Dj
		mov	dx, [word_24626]
		mov	al, 4Ch	; 'L'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		sub	dl, 2
		mov	eax, edi
		shr	eax, 12h
		retn
endp		sub_17F30


; =============== S U B	R O U T	I N E =======================================


proc		sub_17F7D near		; CODE XREF: seg000:loc_142B1p

; FUNCTION CHUNK AT 8077 SIZE 00000002 BYTES

		mov	ah, 62h
		int	21h		; DOS -	3+ - GET PSP ADDRESS
		mov	es, bx
		mov	es, [word ptr es:2Ch]
		xor	di, di

loc_17F8A:				; CODE XREF: sub_17F7D+32j
					; sub_17F7D+41j ...
		cmp	[byte ptr es:di], 0
		jz	loc_18077
		cmp	[dword ptr es:di], 52544C55h
		jnz	short loc_17FA7
		cmp	[dword ptr es:di+4], 444E5341h
		jz	short loc_17FB1

loc_17FA7:				; CODE XREF: sub_17F7D+1Dj
					; sub_17F7D+2Fj
		inc	di

loc_17FA8:				; CODE XREF: sub_17F7D+45j
					; sub_17F7D+75j ...
		cmp	[byte ptr es:di], 0
		jnz	short loc_17FA7
		inc	di
		jmp	short loc_17F8A
; ---------------------------------------------------------------------------

loc_17FB1:				; CODE XREF: sub_17F7D+28j
		add	di, 8

loc_17FB4:				; CODE XREF: sub_17F7D+3Dj
		mov	al, [es:di]
		inc	di
		cmp	al, 20h	; ' '
		jz	short loc_17FB4
		or	al, al
		jz	short loc_17F8A
		cmp	al, 3Dh	; '='
		jnz	short loc_17FA8

loc_17FC4:				; CODE XREF: sub_17F7D+53j
		mov	al, [es:di]
		or	al, al
		jz	short loc_17F8A
		cmp	al, 20h	; ' '
		jnz	short loc_17FD2
		inc	di
		jmp	short loc_17FC4
; ---------------------------------------------------------------------------

loc_17FD2:				; CODE XREF: sub_17F7D+50j
		call	sub_18062
		mov	dh, al
		call	sub_18062
		mov	dl, al
		shl	dl, 4
		call	sub_18062
		or	dl, al

loc_17FE4:				; CODE XREF: sub_17F7D+6Dj
		mov	al, [es:di]
		inc	di
		cmp	al, 20h	; ' '
		jz	short loc_17FE4
		or	al, al
		jz	short loc_17F8A
		cmp	al, 2Ch	; ','
		jnz	short loc_17FA8
		call	sub_18062
		mov	cl, al

loc_17FF9:				; CODE XREF: sub_17F7D+82j
		mov	al, [es:di]
		inc	di
		cmp	al, 20h	; ' '
		jz	short loc_17FF9
		or	al, al
		jz	short loc_17F8A
		cmp	al, 2Ch	; ','
		jnz	short loc_17FA8
		call	sub_18062
		mov	ch, al

loc_1800E:				; CODE XREF: sub_17F7D+97j
		mov	al, [es:di]
		inc	di
		cmp	al, 20h	; ' '
		jz	short loc_1800E
		or	al, al
		jz	loc_17F8A
		cmp	al, 2Ch	; ','
		jnz	short loc_17FA8
		call	sub_18062
		mov	bl, al
		cmp	[byte ptr es:di], 2Ch ;	','
		jz	short loc_18036
		mov	al, 0Ah
		mul	bl
		mov	bl, al
		call	sub_18062
		add	bl, al

loc_18036:				; CODE XREF: sub_17F7D+ACj
					; sub_17F7D+BFj
		mov	al, [es:di]
		inc	di
		cmp	al, 20h	; ' '
		jz	short loc_18036
		or	al, al
		jz	loc_17F8A
		cmp	al, 2Ch	; ','
		jnz	loc_17FA8
		call	sub_18062
		mov	bh, al
		cmp	[byte ptr es:di], 0
		jz	short loc_18060
		mov	al, 0Ah
		mul	bh
		mov	bh, al
		call	sub_18062
		add	bh, al

loc_18060:				; CODE XREF: sub_17F7D+D6j
		clc
		retn
endp		sub_17F7D


; =============== S U B	R O U T	I N E =======================================


proc		sub_18062 near		; CODE XREF: sub_17F7D:loc_17FD2p
					; sub_17F7D+5Ap ...
		mov	al, [es:di]
		inc	di
		or	al, al
		jz	short loc_18073
		sub	al, 30h	; '0'
		jb	short loc_18073
		cmp	al, 9
		ja	short loc_18073
		retn
; ---------------------------------------------------------------------------

loc_18073:				; CODE XREF: sub_18062+6j sub_18062+Aj ...
		pop	ax
		jmp	loc_17F8A
endp		sub_18062 ; sp-analysis	failed

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_17F7D

loc_18077:				; CODE XREF: sub_17F7D+11j
		stc
		retn
; END OF FUNCTION CHUNK	FOR sub_17F7D

; =============== S U B	R O U T	I N E =======================================


proc		sub_18079 near		; CODE XREF: sub_12B83+69p
					; seg000:42F4p	...
		test	[byte ptr word_246DA], 40h
		jz	short loc_18082
		mov	al, 20h	; ' '

loc_18082:				; CODE XREF: sub_18079+5j
		cmp	al, 0Eh
		ja	short loc_18088
		mov	al, 0Eh

loc_18088:				; CODE XREF: sub_18079+Bj
		mov	[byte_24629], al
		movzx	cx, al
		mov	dx, 9
		mov	ax, 6BB8h
		div	cx
		mov	[freq2], ax
		pushf
		cli
		mov	dx, [word_24626]
		mov	al, 4Ch	; 'L'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		sub	dl, 2
		mov	cx, 10h
		call	sub_18201
		mov	al, 4Ch	; 'L'
		out	dx, al
		add	dl, 2
		mov	al, 1
		out	dx, al
		sub	dl, 2
		mov	cx, 10h
		call	sub_18201
		sub	dx, 3
		mov	al, 3
		out	dx, al
		mov	cx, 10h
		call	sub_18201
		xor	al, al
		out	dx, al
		add	dx, 3
		mov	al, 41h	; 'A'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		sub	dl, 2
		mov	al, 45h	; 'E'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		sub	dl, 2
		mov	al, 49h	; 'I'
		out	dx, al
		add	dl, 2
		xor	al, al
		out	dx, al
		sub	dl, 2
		mov	ah, [byte_24629]
		dec	ah
		and	ah, 1Fh
		or	ah, 0C0h
		mov	al, 0Eh
		out	dx, al
		add	dl, 2
		mov	al, ah
		out	dx, al
		sub	dl, 2
		sub	dx, 0FDh ; 'ý'
		in	al, dx
		add	dx, 0FDh ; 'ý'
		mov	al, 41h	; 'A'
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		mov	al, 49h	; 'I'
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		mov	al, 8Fh	; ''
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		xor	bl, bl

loc_1813A:				; CODE XREF: sub_18079+14Fj
		dec	dx
		mov	al, bl
		out	dx, al
		inc	dx
		mov	al, 0
		out	dx, al
		add	dl, 2
		mov	al, 3
		out	dx, al
		sub	dl, 2
		mov	al, 0Dh
		out	dx, al
		add	dl, 2
		mov	al, 3
		out	dx, al
		sub	dl, 2
		mov	cx, 8
		call	sub_18201
		mov	al, 1
		out	dx, al
		inc	dx
		mov	ax, 400h
		out	dx, ax
		dec	dx
		mov	al, 2
		out	dx, al
		inc	dx
		xor	ax, ax
		out	dx, ax
		dec	dx
		mov	al, 3
		out	dx, al
		inc	dx
		xor	ax, ax
		out	dx, ax
		dec	dx
		mov	al, 4
		out	dx, al
		inc	dx
		xor	ax, ax
		out	dx, ax
		dec	dx
		mov	al, 5
		out	dx, al
		inc	dx
		xor	ax, ax
		out	dx, ax
		dec	dx
		mov	al, 6
		out	dx, al
		add	dl, 2
		mov	al, 30h	; '0'
		out	dx, al
		sub	dl, 2
		mov	al, 7
		out	dx, al
		add	dl, 2
		mov	al, 10h
		out	dx, al
		sub	dl, 2
		mov	al, 8
		out	dx, al
		add	dl, 2
		mov	al, 0E0h ; 'à'
		out	dx, al
		sub	dl, 2
		mov	al, 9
		out	dx, al
		inc	dx
		xor	ax, ax
		out	dx, ax
		dec	dx
		mov	al, 0Ah
		out	dx, al
		inc	dx
		xor	ax, ax
		out	dx, ax
		dec	dx
		mov	al, 0Bh
		out	dx, al
		inc	dx
		xor	ax, ax
		out	dx, ax
		dec	dx
		inc	bl
		cmp	bl, [byte_24629]
		jb	loc_1813A
		sub	dx, 0FDh ; 'ý'
		in	al, dx
		add	dx, 0FDh ; 'ý'
		mov	al, 41h	; 'A'
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		mov	al, 49h	; 'I'
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		mov	al, 8Fh	; ''
		out	dx, al
		add	dl, 2
		in	al, dx
		sub	dl, 2
		mov	al, 4Ch	; 'L'
		out	dx, al
		add	dl, 2
		mov	al, 7
		out	dx, al
		sub	dl, 2
		popf
		retn
endp		sub_18079


; =============== S U B	R O U T	I N E =======================================


proc		sub_18201 near		; CODE XREF: sub_18079+35p
					; sub_18079+47p ...
		push	dx
		mov	dx, [word_24626]
		add	dx, 4

loc_18209:				; CODE XREF: sub_18201+11j
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		in	al, dx
		dec	cx
		jnz	short loc_18209
		pop	dx
		retn
endp		sub_18201


; =============== S U B	R O U T	I N E =======================================


proc		sub_18216 near		; CODE XREF: seg000:42F7p
		movzx	si, [byte_2462A]
		mov	bl, [byte ptr cs:asc_182C3+si] ; "\x01\x03\x02\x04\x05\x06\a"
		movzx	si, [byte_2462B]
		mov	bh, [byte ptr cs:asc_182C3+si] ; "\x01\x03\x02\x04\x05\x06\a"
		movzx	si, [byte_2462C]
		mov	cl, [byte ptr cs:asc_182D3+si] ; "\x01\x02\x03\x04\x05"
		movzx	si, [byte_2462D]
		mov	ch, [byte ptr cs:asc_182D3+si] ; "\x01\x02\x03\x04\x05"
		cmp	bl, bh
		jnz	short loc_18244
		mov	bh, 8

loc_18244:				; CODE XREF: sub_18216+2Aj
		shl	bh, 3
		or	bl, bh
		cmp	cl, ch
		jnz	short loc_1824F
		mov	ch, 8

loc_1824F:				; CODE XREF: sub_18216+35j
		shl	ch, 3
		or	cl, ch
		mov	ah, [byte_2463B]
		and	ah, 0AFh
		pushf
		cli
		mov	dx, [word_24626]
		sub	dx, 103h
		mov	si, dx
		lea	di, [si+0Bh]
		lea	dx, [si+0Fh]
		mov	al, 5
		out	dx, al
		mov	dx, si
		mov	al, ah
		out	dx, al
		mov	dx, di
		xor	al, al
		out	dx, al
		lea	dx, [si+0Fh]
		xor	al, al
		out	dx, al
		mov	dx, si
		mov	al, ah
		out	dx, al
		mov	dx, di
		mov	al, cl
		or	al, 80h
		out	dx, al
		mov	dx, si
		mov	al, ah
		or	al, 40h
		out	dx, al
		mov	dx, di
		mov	al, bl
		out	dx, al
		mov	dx, si
		mov	al, ah
		out	dx, al
		mov	dx, di
		mov	al, cl
		out	dx, al
		mov	dx, si
		mov	al, ah
		or	al, 40h
		out	dx, al
		mov	dx, di
		mov	al, bl
		out	dx, al
		lea	dx, [si+102h]
		xor	al, al
		out	dx, al
		mov	dx, si
		mov	al, ah
		out	dx, al
		lea	dx, [si+102h]
		xor	al, al
		out	dx, al
		popf
		retn
endp		sub_18216

; ---------------------------------------------------------------------------
asc_182C3	db 0,0,1,3,0,2,0,4,0,0,0,5,6,0,0,7 ; DATA XREF:	sub_18216+5r
					; sub_18216+Fr
asc_182D3	db 0,1,0,2,0,3,4,5	; DATA XREF: sub_18216+19r
					; sub_18216+23r

; =============== S U B	R O U T	I N E =======================================


proc		sub_182DB near		; CODE XREF: sub_1279A+44j
					; sub_1279A+5Ep
		mov	[dma_mode], 44h	; 'D'
		mov	[byte_24645], 2
		jmp	short loc_182F7
endp		sub_182DB


; =============== S U B	R O U T	I N E =======================================


proc		sub_182E7 near		; CODE XREF: sub_11F4E+162p
					; sub_11F4E+19Dp
		mov	[dma_mode], 48h	; 'H'
		mov	bl, [byte_24673]
		and	bl, 80h
		mov	[byte_24645], bl

loc_182F7:				; CODE XREF: sub_182DB+Aj
					; sub_182E7+15j
		cmp	[byte_2466E], 1
		jz	short loc_182F7
		mov	[word_24636], 0
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
		add	ax, [word ptr dma_buf_pointer]
		mov	[word_24634], ax
		shr	cx, 4
		add	cx, bp
		mov	[word_24632], cx

loc_18338:				; CODE XREF: sub_14358+E2p
					; sub_182E7+2Dj ...
		pushf
		cli
		push	bp
		mov	cl, [byte_2462C]
		call	dma_186E3
		pop	bp
		mov	bl, 21h	; '!'
		or	bl, [byte_24645]
		cmp	[byte_2462C], 4
		jb	short loc_18360
		or	bl, 4
		mov	ax, bp
		and	ax, 0C000h
		shr	bp, 1
		and	bp, 1FFFh
		or	bp, ax

loc_18360:				; CODE XREF: sub_182E7+67j
		mov	dx, [word_24626]
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
		mov	[byte_2466E], 1
		mov	al, 41h	; 'A'
		out	dx, al
		add	dl, 2
		mov	al, bl
		out	dx, al
		sub	dl, 2
		popf
		retn
endp		sub_182E7


; =============== S U B	R O U T	I N E =======================================


proc		sub_18389 near		; CODE XREF: seg000:50A6p seg000:515Ep
		xor	ax, ax

loc_1838B:				; CODE XREF: sub_18389+9j
		call	adlib_18395
		inc	al
		cmp	al, 0E8h ; 'è'
		jbe	short loc_1838B
		retn
endp		sub_18389


; =============== S U B	R O U T	I N E =======================================


proc		adlib_18395 near	; CODE XREF: seg000:50ACp seg000:50B2p ...
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
endp		adlib_18395


; =============== S U B	R O U T	I N E =======================================


proc		sub_183CC near		; CODE XREF: sub_12D61+22p
					; seg000:4A82p	...
		cmp	[snd_base_port], 0FFFFh
		jz	short loc_183DE
		mov	ax, [snd_base_port]
		mov	[sb_base_port],	ax
		call	CheckSB
		jnb	short loc_1842D

loc_183DE:				; CODE XREF: sub_183CC+5j
		mov	[sb_base_port],	220h
		call	CheckSB
		jnb	short loc_1842D
		mov	[sb_base_port],	240h
		call	CheckSB
		jnb	short loc_1842D
		mov	[sb_base_port],	210h
		call	CheckSB
		jnb	short loc_1842D
		mov	[sb_base_port],	230h
		call	CheckSB
		jnb	short loc_1842D
		mov	[sb_base_port],	250h
		call	CheckSB
		jnb	short loc_1842D
		mov	[sb_base_port],	260h
		call	CheckSB
		jnb	short loc_1842D
		mov	[sb_base_port],	280h
		call	CheckSB
		jnb	short loc_1842D
		stc
		retn
; ---------------------------------------------------------------------------

loc_1842D:				; CODE XREF: sub_183CC+10j
					; sub_183CC+1Bj ...
		mov	al, 10h
		call	WriteSB
		mov	al, 80h	; '€'
		call	WriteSB
		mov	al, 0E1h ; 'á'
		call	WriteSB
		call	ReadSB
		mov	ah, al
		call	ReadSB
		mov	[word_24654], ax
		clc
		retn
endp		sub_183CC


; =============== S U B	R O U T	I N E =======================================


proc		sub_18449 near		; CODE XREF: seg000:4C15p sb_check+Fp

; FUNCTION CHUNK AT 84C3 SIZE 00000061 BYTES

		call	sub_183CC
		mov	dx, 0FF6h
		jb	short loc_18498
		cmp	[irq_number], 0FFh
		jz	short loc_18463
		mov	al, [irq_number]
		mov	[irq_number3], al
		call	sub_1849A
		jnb	short loc_184C3

loc_18463:				; CODE XREF: sub_18449+Dj
		mov	[irq_number3], 7
		call	sub_1849A
		jnb	short loc_184C3
		mov	[irq_number3], 5
		call	sub_1849A
		jnb	short loc_184C3
		mov	[irq_number3], 3
		call	sub_1849A
		jnb	short loc_184C3
		mov	[irq_number3], 0Ah
		call	sub_1849A
		jnb	short loc_184C3
		mov	[irq_number3], 9
		call	sub_1849A
		jnb	short loc_184C3
		mov	dx, offset aErrorCouldNot_0 ; "Error: Could not	find IRQ!\r\n"

loc_18498:				; CODE XREF: sub_18449+6j
		stc
		retn
endp		sub_18449


; =============== S U B	R O U T	I N E =======================================


proc		sub_1849A near		; CODE XREF: sub_18449+15p
					; sub_18449+1Fp ...
		mov	[byte_24670], 0
		mov	si, offset sbhandler_185D9 ; myfunc
		mov	al, [irq_number3]
		call	setsb_handler
		mov	al, 0F2h ; 'ò'
		call	WriteSB
		sti
		xor	cx, cx

loc_184B0:				; CODE XREF: sub_1849A+1Dj
		cmp	[byte_24670], 0
		jnz	short loc_184BE
		loop	loc_184B0
		call	restore_intvector
		stc
		retn
; ---------------------------------------------------------------------------

loc_184BE:				; CODE XREF: sub_1849A+1Bj
		call	restore_intvector
		clc
		retn
endp		sub_1849A

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_18449

loc_184C3:				; CODE XREF: sub_18449+18j
					; sub_18449+22j ...
		cmp	[dma_channel], 0FFh
		jz	short loc_184DC
		mov	al, [dma_channel]
		mov	[dma_chn_mask],	al
		cmp	[bit_mode], 16
		jz	short sbsound_on
		call	sub_18540
		jnb	short sbsound_on

loc_184DC:				; CODE XREF: sub_18449+7Fj
		cmp	[bit_mode], 8
		jz	short loc_18501
		mov	[dma_chn_mask],	5
		call	sub_18540
		jnb	short sbsound_on
		mov	[dma_chn_mask],	6
		call	sub_18540
		jnb	short sbsound_on
		mov	[dma_chn_mask],	7
		call	sub_18540
		jnb	short sbsound_on

loc_18501:				; CODE XREF: sub_18449+98j
		mov	[dma_chn_mask],	1
		call	sub_18540
		jnb	short sbsound_on
		mov	[dma_chn_mask],	3
		call	sub_18540
		jnb	short sbsound_on
		mov	[dma_chn_mask],	0
		call	sub_18540
		jnb	short sbsound_on
		mov	dx, offset aErrorCouldNot_1 ; "Error: Could not	find DMA!\r\n"
		stc
		retn
; END OF FUNCTION CHUNK	FOR sub_18449

; =============== S U B	R O U T	I N E =======================================


proc		sbsound_on near		; CODE XREF: seg000:loc_14AFDp
					; sub_18449+8Cj ...
		call	CheckSB
		mov	al, 0D1h ; 'Ñ'
		call	WriteSB
		mov	ax, [sb_base_port]
		mov	[snd_base_port], ax
		mov	al, [irq_number3]
		mov	[irq_number], al
		mov	al, [dma_chn_mask]
		mov	[dma_channel], al
		clc
		retn
endp		sbsound_on


; =============== S U B	R O U T	I N E =======================================


proc		sub_18540 near		; CODE XREF: sub_18449+8Ep
					; sub_18449+9Fp ...
		mov	[dma_mode], 48h	; 'H'
		cli
		call	CheckSB
		mov	[word_2460E], 2
		mov	[dma_buf_pointer], 0
		mov	cl, [dma_chn_mask]
		call	dma_186E3
		mov	[byte_24670], 1
		mov	si, offset sbhandler_185D9 ; myfunc
		mov	al, [irq_number3]
		call	setsb_handler
		cmp	[dma_chn_mask],	4
		jnb	short loc_18591
		mov	al, 40h	; '@'
		call	WriteSB
		mov	al, 0D3h ; 'Ó'
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

loc_18591:				; CODE XREF: sub_18540+32j
		mov	al, 42h	; 'B'
		call	WriteSB
		mov	al, 0ACh ; '¬'
		call	WriteSB
		mov	al, 44h	; 'D'
		call	WriteSB
		mov	al, 0B6h ; '¶'
		call	WriteSB
		mov	al, 30h	; '0'
		call	WriteSB
		mov	ax, [word_2460E]
		call	WriteSB
		mov	al, ah
		call	WriteSB

loc_185B5:				; CODE XREF: sub_18540+4Fj
		sti
		xor	cx, cx

loc_185B8:				; CODE XREF: sub_18540+7Fj
		cmp	[byte_24670], 1
		jnz	short loc_185CD
		loop	loc_185B8
		call	restore_intvector
		mov	cl, [dma_chn_mask]
		call	set_dmachn_mask
		stc
		retn
; ---------------------------------------------------------------------------

loc_185CD:				; CODE XREF: sub_18540+7Dj
		call	restore_intvector
		mov	cl, [dma_chn_mask]
		call	set_dmachn_mask
		clc
		retn
endp		sub_18540


; =============== S U B	R O U T	I N E =======================================


; int sbhandler_185D9
proc		sbhandler_185D9	far	; DATA XREF: sub_1849A+5o
					; sub_18540+24o
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
		inc	[byte_24670]
		mov	al, 20h	; ' '
		out	20h, al		; Interrupt controller,	8259A.
		pop	ds
		pop	dx
		pop	ax
		iret
endp		sbhandler_185D9

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


proc		dma_186E3 near		; CODE XREF: set_proaud+59p
					; set_wss+28p ...
		test	[byte ptr word_246DA+1], 10h
		jz	short loc_186EF
		and	[dma_mode], 0EFh

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
		mov	dx, [word ptr dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, [word ptr dma_buf_pointer]
		adc	dx, 0
		add	ax, [word ptr dword_24694]
		adc	dx, [word ptr dword_24694+2]
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
		mov	dx, [word ptr dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, [word ptr dma_buf_pointer]
		adc	dx, 0
		add	ax, [word ptr dword_24694]
		adc	dx, [word ptr dword_24694+2]
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
		mov	dx, [word ptr dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, [word ptr dma_buf_pointer]
		adc	dx, 0
		add	ax, [word ptr dword_24694]
		adc	dx, [word ptr dword_24694+2]
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
		mov	dx, [word ptr dma_buf_pointer+2]
		rol	dx, 4
		mov	ax, dx
		and	al, 0F0h
		and	dx, 0Fh
		add	ax, [word ptr dma_buf_pointer]
		adc	dx, 0
		add	ax, [word ptr dword_24694]
		adc	dx, [word ptr dword_24694+2]
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
		movzx	edx, [word ptr dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, [word ptr dma_buf_pointer]
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
		movzx	edx, [word ptr dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, [word ptr dma_buf_pointer]
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
		movzx	edx, [word ptr dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, [word ptr dma_buf_pointer]
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
		movzx	edx, [word ptr dma_buf_pointer+2]
		shl	edx, 4
		movzx	eax, [word ptr dma_buf_pointer]
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
endp		dma_186E3


; =============== S U B	R O U T	I N E =======================================


proc		set_dmachn_mask	near	; CODE XREF: proaud_sndoff+1Dp
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
endp		set_dmachn_mask


; =============== S U B	R O U T	I N E =======================================


proc		alloc_dma_buf near	; CODE XREF: sub_11F4E+92p
					; volume_prep+47p ...
		mov	[dword_24684], eax
		mov	[byte_2469C], cl
		mov	[byte_2469A], 0
		mov	[byte_2469B], 0
		mov	[dword_24694], 0
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
		cmp	[byte_2469C], 4
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
		mov	[byte_2469A], 1
		mov	ax, [word_2468C]
		clc
		retn
; ---------------------------------------------------------------------------

loc_18A22:				; CODE XREF: alloc_dma_buf+2Dj
		pop	ax
		call	setmemallocstrat
		stc
		retn
endp		alloc_dma_buf


; =============== S U B	R O U T	I N E =======================================


proc		sub_18A28 near		; CODE XREF: sub_11F4E:loc_12117p
					; sub_11F4E+1E4p ...
		cmp	[byte_2469A], 1
		jnz	short loc_18A3B
		mov	[byte_2469A], 0
		mov	ax, [myseg_24698]
		call	memfree
		retn
; ---------------------------------------------------------------------------

loc_18A3B:				; CODE XREF: sub_18A28+5j
		clc
		retn
endp		sub_18A28


; =============== S U B	R O U T	I N E =======================================


; int __usercall setsb_handler<eax>(void (__cdecl *myfunc)()<esi>)
proc		setsb_handler near	; CODE XREF: seg000:432Ap
					; set_proaud+14p ...
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

loc_18A5C:				; CODE XREF: setsb_handler+17j
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
		assume es:nothing
		les	cx, [es:bx]
		assume es:nothing
		mov	[old_intprocoffset], cx
		mov	[old_intprocseg], es
		mov	es, ax
		assume es:nothing
		mov	[es:bx], si
		mov	[word ptr es:bx+2], cs
		pop	es
		assume es:nothing
		popf
		retn
endp		setsb_handler


; =============== S U B	R O U T	I N E =======================================


proc		restore_intvector near	; CODE XREF: gravis_clean+16p
					; sub_1474C+Fp	...
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
		assume es:nothing
		mov	ax, [old_intprocoffset]
		mov	[es:bx], ax
		mov	ax, [old_intprocseg]
		mov	[es:bx+2], ax
		pop	es
		assume es:seg003
		popf
		retn
endp		restore_intvector


; =============== S U B	R O U T	I N E =======================================


proc		getint_vect near	; CODE XREF: sub_12DA8+67p
		push	es
		mov	ah, 35h
		int	21h		; DOS -	2+ - GET INTERRUPT VECTOR
					; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	dx, es
		pop	es
		assume es:nothing
		retn
endp		getint_vect


; =============== S U B	R O U T	I N E =======================================


proc		setint_vect near	; CODE XREF: set_timer_int+20p
					; sub_12FB4+Cp	...
		push	ds
		mov	ds, dx
		mov	dx, bx
		mov	ah, 25h
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds
		retn
endp		setint_vect


; =============== S U B	R O U T	I N E =======================================


; int __usercall memalloc<eax>(int bytes<ebx>)
proc		memalloc near		; CODE XREF: inr_module:loc_11AC0p
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
endp		memalloc


; =============== S U B	R O U T	I N E =======================================


proc		memfree	near		; CODE XREF: sub_125DA+4Fp
					; sub_125DA+72p ...
		push	es
		mov	es, ax
		assume es:nothing
		mov	ah, 49h
		int	21h		; DOS -	2+ - FREE MEMORY
					; ES = segment address of area to be freed
		pop	es
		retn
endp		memfree


; =============== S U B	R O U T	I N E =======================================


proc		memrealloc near		; CODE XREF: sub_11B85+14p
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
endp		memrealloc


; =============== S U B	R O U T	I N E =======================================


proc		setmemallocstrat near	; CODE XREF: sub_125B9+15p
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
endp		setmemallocstrat


; =============== S U B	R O U T	I N E =======================================


proc		getmemallocstrat near	; CODE XREF: sub_12DA8+7Fp
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
endp		getmemallocstrat


; =============== S U B	R O U T	I N E =======================================


proc		setmemalloc1 near	; CODE XREF: sub_12D35+12p
					; sub_12DA8+85p
		test	[byte ptr word_246DA], 1
		jz	short setmemalloc2
		mov	ax, 181h
		jmp	short setmemallocstrat
endp		setmemalloc1


; =============== S U B	R O U T	I N E =======================================


proc		setmemalloc2 near	; CODE XREF: alloc_dma_buf+1Fp
					; setmemalloc1+5j
		mov	ax, 1
		jmp	short setmemallocstrat
endp		setmemalloc2


; =============== S U B	R O U T	I N E =======================================


proc		WriteMixerSB near	; CODE XREF: set_sb-F3p
					; set_sb:loc_14C89p ...
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
endp		WriteMixerSB


; =============== S U B	R O U T	I N E =======================================


proc		ReadMixerSB near	; CODE XREF: seg000:4A98p seg000:4AC7p ...
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
endp		ReadMixerSB


; =============== S U B	R O U T	I N E =======================================


proc		WriteSB	near		; CODE XREF: set_sb+32p set_sb+38p ...
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
endp		WriteSB


; =============== S U B	R O U T	I N E =======================================


proc		ReadSB near		; CODE XREF: sub_183CC+70p
					; sub_183CC+75p ...
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
endp		ReadSB


; =============== S U B	R O U T	I N E =======================================


proc		CheckSB	near		; CODE XREF: sbpro_sndoff+9p
					; sub_183CC+Dp	...
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
		cmp	al, 0AAh ; 'ª'
		jnz	short loc_18BBE
		clc
		retn
; ---------------------------------------------------------------------------

loc_18BBE:				; CODE XREF: CheckSB+16j
		stc
		retn
endp		CheckSB


; =============== S U B	R O U T	I N E =======================================


proc		sbsound_off near	; CODE XREF: seg000:4C02p
					; sbpro_clean+3p ...
		call	CheckSB
		mov	al, 0D3h ; 'Ó'
		call	WriteSB
		retn
endp		sbsound_off


; =============== S U B	R O U T	I N E =======================================


proc		initclockfromrtc near	; CODE XREF: sub_125B9+1Bp
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
endp		initclockfromrtc


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C19 near		; CODE XREF: sub_18C98+EBp
		ror	eax, 10h
		call	itox
		ror	eax, 10h
endp		sub_18C19 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		itox near		; CODE XREF: sub_18C19+4p
					; sub_18C98+D7p
		xchg	al, ah
		call	sub_18C2B
		mov	al, ah
endp		itox ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C2B near		; CODE XREF: itox+2p sub_18C98+C4p
		push	ax
		shr	al, 4
		call	dtox
		pop	ax
endp		sub_18C2B ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		dtox near		; CODE XREF: sub_18C2B+4p
		and	al, 0Fh
		or	al, '0'
		cmp	al, '9'
		jbe	short loc_18C3D
		add	al, 7

loc_18C3D:				; CODE XREF: dtox+6j
		mov	[si], al
		inc	si
		retn
endp		dtox


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C41 near		; CODE XREF: sub_18C98+8Ap
		cbw
endp		sub_18C41


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C42 near		; CODE XREF: sub_18C98+9Dp
		cwde
endp		sub_18C42 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C44 near		; CODE XREF: sub_18C98+B1p
		xor	cx, cx
		or	eax, eax
		jns	short loc_18C5D
		mov	dl, 2Dh	; '-'
		call	sub_18C78
		neg	eax
		jmp	short loc_18C5D
endp		sub_18C44


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C55 near		; CODE XREF: sub_18C98+53p
		xor	ah, ah
endp		sub_18C55


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C57 near		; CODE XREF: sub_18C98+65p
		movzx	eax, ax
endp		sub_18C57 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C5B near		; CODE XREF: sub_18C98+78p
		xor	cx, cx

loc_18C5D:				; CODE XREF: sub_18C44+5j sub_18C44+Fj
		mov	ebx, 0Ah
endp		sub_18C5B ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C63 near		; CODE XREF: sub_18C63+Dp
		xor	edx, edx
		div	ebx
		or	eax, eax
		jz	short loc_18C75
		push	edx
		call	sub_18C63
		pop	edx

loc_18C75:				; CODE XREF: sub_18C63+9j
		or	dl, 30h
endp		sub_18C63 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_18C78 near		; CODE XREF: sub_18C44+9p
		mov	[si], dl
		inc	si
		inc	cx
		retn
endp		sub_18C78

; ---------------------------------------------------------------------------
asmprintf_tbl	dw offset loc_18CB9	; DATA XREF: sub_18C98+1Cr
		dw offset loc_18CBB
		dw offset loc_18CC7
		dw offset loc_18CCF
		dw offset loc_18CE4
		dw offset loc_18CF6
		dw offset loc_18D08
		dw offset loc_18D1B
		dw offset loc_18D2E
		dw offset loc_18D41
		dw offset loc_18D55
		dw offset loc_18D68
		dw offset loc_18D7B

; =============== S U B	R O U T	I N E =======================================


proc		sub_18C98 near		; CODE XREF: sub_12D05+20p
		push	es
		mov	ax, ds
		mov	es, ax
		assume es:seg003
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

loc_18C9F:				; CODE XREF: sub_18C98+Fj
		mov	[di], al
		inc	di

loc_18CA2:				; CODE XREF: sub_18C98+5j
					; sub_18C98+2Dj ...
		mov	al, [si]
		inc	si
		cmp	al, 20h	; ' '
		jnb	short loc_18C9F
		cmp	al, 0Ch
		ja	short loc_18CB9
		inc	si
		mov	bl, al
		xor	bh, bh
		shl	bx, 1
		jmp	[cs:asmprintf_tbl+bx]

loc_18CB9:				; CODE XREF: sub_18C98+13j
					; DATA XREF: seg000:asmprintf_tblo
		pop	es
		assume es:dseg
		retn
; ---------------------------------------------------------------------------

loc_18CBB:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C80o
		push	si
		mov	si, [si]
		call	sub_18D9D
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

loc_18CC7:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C82o
		mov	bx, [si]
		mov	bl, [bx]
		xor	bh, bh
		jmp	short loc_18CD3
; ---------------------------------------------------------------------------

loc_18CCF:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C84o
		mov	bx, [si]
		mov	bx, [bx]

loc_18CD3:				; CODE XREF: sub_18C98+35j
		push	si
		shl	bx, 1
		mov	si, [si+2]
		mov	si, [bx+si]
		call	sub_18D9D
		pop	si
		add	si, 4
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

loc_18CE4:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C86o
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	sub_18C55
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

loc_18CF6:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C88o
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	sub_18C57
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

loc_18D08:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C8Ao
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	sub_18C5B
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_18CA2
; ---------------------------------------------------------------------------

loc_18D1B:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C8Co
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	sub_18C41
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

loc_18D2E:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C8Eo
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	sub_18C42
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

loc_18D41:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C90o
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	sub_18C44
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

loc_18D55:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C92o
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	sub_18C2B
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

loc_18D68:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C94o
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	itox
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
; ---------------------------------------------------------------------------

loc_18D7B:				; CODE XREF: sub_18C98+1Cj
					; DATA XREF: seg000:8C96o
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	sub_18C19
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_18CA2
endp		sub_18C98

; ---------------------------------------------------------------------------
		mov	ax, 0FFFFh
		dec	si

loc_18D93:				; CODE XREF: seg000:8D98j
		inc	ax
		inc	si
		cmp	[byte ptr si], 0
		jnz	short loc_18D93
		sub	si, ax
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_18D9D near		; CODE XREF: sub_12D05:loc_12D30p
					; sub_18C98+26p ...
		xor	cx, cx
		jmp	short loc_18DA6
; ---------------------------------------------------------------------------

loc_18DA1:				; CODE XREF: sub_18D9D+Ej
		mov	[es:di], al
		inc	si
		inc	di

loc_18DA6:				; CODE XREF: sub_18D9D+2j
		mov	al, [si]
		inc	cx
		or	al, al
		jnz	short loc_18DA1
		retn
endp		sub_18D9D

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
off_18DC0	dw offset loc_161C0	; DATA XREF: sub_1609F+28r
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
off_18DE0	dw offset loc_16617	; DATA XREF: sub_1609F+2AEr
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
off_18E20	dw offset loc_15698	; DATA XREF: sub_15577+28r
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
off_18E40	dw offset loc_15B52	; DATA XREF: sub_15577+311r
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
off_18F60	dw offset eff_nullsub	; DATA XREF: sub_137D5+16r
					; sub_137D5+2Br
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_13A43
		dw offset eff_13A94
		dw offset eff_nullsub
		dw offset eff_13B06
		dw offset eff_13B78
		dw offset eff_13B88
		dw offset eff_13BA3
		dw offset eff_13CDD
		dw offset eff_13CE8
		dw offset eff_13DE5
		dw offset eff_13DEF
		dw offset eff_nullsub
		dw offset eff_13E2D
		dw offset eff_13E32
		dw offset eff_13E7F
		dw offset eff_13E84
		dw offset eff_13E8C
		dw offset eff_nullsub
		dw offset nullsub_2
		dw offset eff_13F05
		dw offset eff_13F3B
		dw offset eff_nullsub
		dw offset eff_14020
		dw offset eff_14030
		dw offset eff_14067
off_18FA2	dw offset eff_nullsub	; DATA XREF: sub_13623+196r
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_13A43
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_13B06
		dw offset eff_nullsub
		dw offset eff_13B88
		dw offset eff_13BA3
		dw offset eff_13CDD
		dw offset eff_13CE8
		dw offset eff_13DE5
		dw offset eff_13DEF
		dw offset eff_nullsub
		dw offset eff_13E2D
		dw offset eff_13E32
		dw offset eff_13E7F
		dw offset eff_13E84
		dw offset eff_13E8C
		dw offset eff_nullsub
		dw offset nullsub_2
		dw offset eff_13F05
		dw offset eff_13F3B
		dw offset eff_nullsub
		dw offset eff_14020
		dw offset eff_14030
		dw offset eff_14067
off_18FE4	dw offset eff_nullsub	; DATA XREF: sub_13813+Er
		dw offset eff_13886
		dw offset eff_138A4
		dw offset eff_138D2
		dw offset eff_1392F
		dw offset eff_139AC
		dw offset eff_139B2
		dw offset eff_139B9
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_13AD7
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_13BA3
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_13DE5
		dw offset eff_13DEF
		dw offset eff_13E1E
		dw offset eff_13E2D
		dw offset eff_13E32
		dw offset eff_13E7F
		dw offset eff_13E84
		dw offset eff_nullsub
		dw offset eff_138D2
		dw offset nullsub_2
		dw offset eff_13F05
		dw offset eff_13F3B
		dw offset eff_13FBE
		dw offset eff_nullsub
		dw offset eff_nullsub
		dw offset eff_nullsub
off_19026	dw offset eff_nullsub	; DATA XREF: eff_13BA3+Ar
		dw offset eff_1387F
		dw offset eff_1389D
		dw offset eff_13BB2
		dw offset eff_13BC0
		dw offset eff_13BC8
		dw offset eff_13C02
		dw offset eff_13C34
		dw offset eff_13C3F
		dw offset eff_13C64
		dw offset eff_13C88
		dw offset eff_13C95
		dw offset eff_13CA2
		dw offset eff_13CB3
		dw offset eff_13CC9
		dw offset eff_nullsub
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

; Segment type:	Pure code
segment		seg001 byte public 'CODE' use16
		assume cs:seg001
; START	OF FUNCTION CHUNK FOR start
		assume es:nothing, ss:nothing, ds:dseg,	fs:nothing, gs:nothing

loc_19050:				; CODE XREF: start+4Cj
					; DATA XREF: dseg:off_1DE3Co ...
		call	callsubx

loc_19053:
		jb	loc_192B9

loc_19057:				; "\rCurrent Soundcard settings:\r\n\n$"
		mov	dx, offset aCurrentSoundcard
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		mov	di, offset buffer_1 ; 2800h
		call	sub_12D05
		mov	[byte ptr es:di], '$'

loc_1906E:				; 2800h
		mov	dx, offset buffer_1
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	dx, offset myendl ; "\r\n$"
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"

loc_1907C:
		call	sub_125B9
		mov	ax, 4C00h

loc_19084:				; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)
		int	21h		; AL = exit code
; ---------------------------------------------------------------------------

loc_19086:				; CODE XREF: start+57j
		mov	dx, 0
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	ax, 4C00h
		int	21h		; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)
; END OF FUNCTION CHUNK	FOR start	; AL = exit code
		assume ss:seg004, ds:nothing

; =============== S U B	R O U T	I N E =======================================


proc		start near

; FUNCTION CHUNK AT 0000 SIZE 00000042 BYTES
; FUNCTION CHUNK AT 07D7 SIZE 00000059 BYTES
; FUNCTION CHUNK AT 0D44 SIZE 0000007D BYTES

		mov	ax, dseg

loc_19095:
		mov	ds, ax
		assume ds:dseg
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
		mov	dx, offset aCriticalErrorT ; "\r\n\nCritical error: The	player jumped to"...
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
		or	[byte ptr configword], 4

loc_190F7:				; CODE XREF: start+5Ej
		bt	ebp, 3
		jnb	short loc_19103
		and	[byte ptr configword], 0FBh

loc_19103:				; CODE XREF: start+6Aj
		bt	ebp, 6
		jnb	short loc_19114
		and	[byte ptr configword+1], 0F1h
		or	[byte ptr configword+1], 2

loc_19114:				; CODE XREF: start+76j
		bt	ebp, 5
		jnb	short loc_19125
		and	[byte ptr configword+1], 0F1h
		or	[byte ptr configword+1], 4

loc_19125:				; CODE XREF: start+87j
		bt	ebp, 13h
		jnb	short loc_19131
		and	[byte ptr configword+1], 0F1h

loc_19131:				; CODE XREF: start+98j
		bt	ebp, 4
		jnb	short loc_1913D
		and	[byte ptr configword], 0FDh

loc_1913D:				; CODE XREF: start+A4j
		bt	ebp, 14h
		jnb	short loc_19149
		and	[byte ptr configword], 0FEh

loc_19149:				; CODE XREF: start+B0j
		bt	ebp, 0Eh
		jnb	short loc_19155
		and	[byte ptr configword], 0BFh

loc_19155:				; CODE XREF: start+BCj
		bt	ebp, 2
		jnb	short loc_19161
		or	[byte ptr configword], 40h

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
		mov	[videomempointer], 0B8000000h
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
		mov	[word ptr cs:oint9_1C1A4], bx
		mov	[word ptr cs:oint9_1C1A4+2], es

loc_191A2:
		mov	ax, 3524h

loc_191A5:				; DOS -	2+ - GET INTERRUPT VECTOR
		int	21h		; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	[word ptr cs:oint24_1C1AC], bx
		mov	[word ptr cs:oint24_1C1AC+2], es
		mov	ax, 352Fh
		int	21h		; DOS -	2+ - GET INTERRUPT VECTOR
					; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	[word ptr cs:oint2f_1C1B4], bx
		mov	[word ptr cs:oint2f_1C1B4+2], es
		push	ds
		mov	ax, cs
		mov	ds, ax
		assume ds:seg001
		mov	dx, offset int9
		mov	ax, 2509h
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		mov	dx, offset int24
		mov	ax, 2524h
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		mov	dx, offset int2f
		mov	ax, 252Fh

loc_191DB:				; DOS -	SET INTERRUPT VECTOR
		int	21h		; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds
		assume ds:dseg
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
		mov	[byte_1DE70], 0FFh
		call	mouseinit
		mov	bl, [byte ptr configword+1]
		shr	bl, 1
		and	bx, 7
		cmp	bl, 5
		jbe	short loc_19212
		xor	bl, bl

loc_19212:				; CODE XREF: start+17Cj
		shl	bx, 1
		mov	ax, [off_1CA8E+bx]
		mov	[off_1DE3C], ax
		cmp	[byte_1DB6C], 40h ; '@'
		jz	loc_19D94
		cmp	[byte_1DB6C], 20h ; ' '
		jbe	loc_192CA
		mov	[word_1DE4E], 2
		call	sub_1C29E
		jb	short loc_19256
		call	callsubx
		jb	short loc_19256
		call	sub_19D6D
		jb	short loc_19250

loc_19242:
		cmp	[byte ptr word_1DE50], 1Ch
		jz	loc_192E0
		mov	[byte_1DE7E], 0

loc_19250:				; CODE XREF: start+1AEj start+5C2j ...
		cli
		call	sub_125B9

loc_19256:				; CODE XREF: start+1A4j start+1A9j ...
		call	sub_1C70F
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
		call	enableblink
		mov	cx, 0
		mov	dx, 124Fh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		call	sub_1A75D
		mov	si, offset hopeyoulike ; "Æ"
		les	di, [videomempointer]
		assume es:nothing
		call	write_scr
		mov	dx, 1300h
		xor	bh, bh
		mov	ah, 2
		int	10h		; - VIDEO - SET	CURSOR POSITION
					; DH,DL	= row, column (0,0 = upper left)
					; BH = page number
		cmp	[byte_1DE7E], 0
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
		mov	[byte_1DE7E], 5
		mov	[word ptr messagepointer], offset aNotEnoughMemor ; "Not enough	memory.\r\n$"
		mov	[word ptr messagepointer+2], ds
		call	callsubx
		jb	loc_19256

loc_192E0:				; CODE XREF: start+1B5j
		mov	si, offset unk_1DCFD
		call	sub_1988C
		mov	[word_1DE62], 0
		mov	[word_1DE5E], 0
		mov	[byte_1DE7F], 1

loc_192F7:				; CODE XREF: start+456j start+6F3j ...
		call	setvideomode
		mov	[byte_1DE70], 1

loc_192FF:				; CODE XREF: start+471j start+4A7j ...
		mov	cx, 0
		mov	dx, 1B4Fh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		call	sub_1A75D
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		mov	di, offset buffer_1 ; 2800h
		call	sub_12D05
		mov	[byte ptr es:di], 0
		sub	di, 16EFh
		and	di, 0FFFEh
		mov	ax, 50h	; 'P'
		sub	ax, di
		add	ax, 320h
		les	di, [videomempointer]
		assume es:nothing
		add	di, ax		; buf
		mov	si, offset buffer_1 ; str
		mov	ah, 78h	; 'x'
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
		mov	si, (offset buffer_1DC6C+3)
		xor	dl, dl
		mov	ah, 47h
		int	21h		; DOS -	2+ - GET CURRENT DIRECTORY
					; DL = drive (0=default, 1=A, etc.)
					; DS:SI	points to 64-byte buffer area
		mov	si, offset buffer_1DC6C
		call	sub_1C6A7
		shr	ax, 1
		neg	ax
		add	ax, 257h
		shl	ax, 1
		les	di, [videomempointer]
		add	di, ax		; buf
		mov	si, offset buffer_1DC6C	; str
		mov	ah, 7Bh	; '{'
		call	put_message
		cmp	[byte_1DE7F], 1
		jnz	short loc_19395
		mov	si, offset msg	; "Searching directory for modules  "
		mov	ax, 7E0Dh
		call	message_1BE77
		call	modules_search

loc_19395:				; CODE XREF: start+2F5j
		mov	[byte_1DE7E], 0
		mov	[word_1DE60], 0FFFFh
		mov	cx, 906h
		mov	dx, 1949h
		mov	bl, 7Fh	; ''
		mov	ax, 7803h
		call	draw_frame

loc_193AE:				; CODE XREF: start+4C8j start+4EAj ...
		call	filelist_198B8
		mov	ax, [word_1DE62]
		mov	bl, 10h
		call	sub_199F9
		call	sub_197F2

loc_193BC:				; CODE XREF: start+3CBj start+481j ...
		mov	al, [byte_1DE7C]
		xor	al, 1
		mov	[byte_1DE7D], al
		call	mouse_1C73F

loc_193C7:				; CODE XREF: start+373j
		test	[byte_1DE90], 2
		jnz	loc_19848
		test	[byte_1DE90], 1
		jnz	loc_19827
		mov	al, [byte_1DE7C]
		cmp	al, [byte_1DE7D]
		jz	short loc_193FF	; keyboard message loop	here
		mov	[byte_1DE7D], al
		les	di, [videomempointer]
		add	di, 104Ah	; buf
		mov	ah, 78h	; 'x'
		mov	si, offset aHitBackspaceToRe ; "Hit backspace to return	to playmode, F-"...
		cmp	[byte_1DE7C], 0
		jz	short loc_193FC
		mov	si, offset aPressF1ForHelpQu ; "		 Press F-1 for help, Qu"...

loc_193FC:				; CODE XREF: start+365j
		call	put_message

loc_193FF:				; CODE XREF: start+34Ej
		mov	ax, [cs:key_code] ; keyboard message loop here
		or	ax, ax
		jz	short loc_193C7
		push	ax
		call	sub_1C756
		pop	ax
		mov	[cs:key_code], 0
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
		assume es:dseg
		mov	di, offset byte_1DB6C
		mov	dx, di
		cld
		movs	[dword ptr es:di], [dword ptr fs:si]
		movs	[dword ptr es:di], [dword ptr fs:si]
		movs	[dword ptr es:di], [dword ptr fs:si]
		mov	[byte ptr di], 0
		cmp	[byte ptr fs:2], 0
		jz	short loc_194EB
		cmp	[byte ptr fs:2], 1
		jz	short loc_19506
		push	dx

loc_1949E:
		mov	cx, 501h
		mov	dx, 1A4Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7800h
		call	draw_frame
		mov	si, offset aLoadingModule ; msg
		mov	ax, 7E0Dh
		call	message_1BE77
		pop	dx
		call	sub_19E11

loc_194B9:
		jnb	short loc_194E3
		mov	si, offset aNotEnoughMemo_0 ; "Not enough memory available to load all"...
		cmp	ax, 0FFFEh
		jz	short loc_194CE
		mov	si, offset aNotEnoughDram_0 ; "Not enough DRAM on your UltraSound to l"...
		cmp	ax, 0FFFDh
		jz	short loc_194CE
		mov	si, offset aModuleIsCorrupt ; msg

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
		mov	[byte_1DE7F], 0
		jmp	loc_192F7
; ---------------------------------------------------------------------------

loc_194EB:				; CODE XREF: start+401j
		mov	[byte_1DE7F], 1
		mov	dx, offset byte_1DB6C
		mov	ah, 3Bh
		int	21h		; DOS -	2+ - CHANGE THE	CURRENT	DIRECTORY (CHDIR)
					; DS:DX	-> ASCIZ directory name	(may include drive)
		mov	[word_1DE62], 0
		mov	[word_1DE5E], 0
		jmp	loc_192FF
; ---------------------------------------------------------------------------

loc_19506:				; CODE XREF: start+409j
		mov	[byte_1DE7F], 1
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
		mov	[word_1DE62], 0
		mov	[word_1DE5E], 0
		jmp	loc_192FF
; ---------------------------------------------------------------------------

loc_1953C:				; CODE XREF: start+38Fj start+603j ...
		cmp	[word_1DE62], 0Eh
		jnb	short loc_1955D
		mov	bx, [word_1DE54]
		dec	bx
		mov	ax, [word_1DE62]
		cmp	ax, bx
		jnb	loc_193BC
		mov	bl, 70h	; 'p'
		call	sub_199F9
		inc	[word_1DE62]
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_1955D:				; CODE XREF: start+4AFj
		cmp	[word_1DE54], 0Fh
		jb	loc_193BC
		mov	ax, [word_1DE54]
		sub	ax, [word_1DE5E]
		jb	loc_193BC
		cmp	ax, 10h
		jb	loc_193BC
		inc	[word_1DE5E]
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_1957F:				; CODE XREF: start+389j
					; DATA XREF: dseg:str_24461o ...
		cmp	[word_1DE62], 0
		jz	short loc_19595
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	sub_199F9
		dec	[word_1DE62]
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_19595:				; CODE XREF: start+4F2j
		sub	[word_1DE5E], 1
		jnb	loc_193AE
		mov	[word_1DE5E], 0
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_195A7:				; CODE XREF: start+395j
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	sub_199F9
		mov	[word_1DE62], 0
		mov	[word_1DE5E], 0
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_195BE:				; CODE XREF: start+39Bj
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	sub_199F9
		mov	ax, [word_1DE54]
		dec	ax
		cmp	ax, 0Fh
		jb	short loc_195DE
		sub	ax, 0Eh
		mov	[word_1DE5E], ax
		mov	[word_1DE62], 0Eh
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_195DE:				; CODE XREF: start+53Bj
		mov	[word_1DE5E], 0
		mov	[word_1DE62], ax
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_195EA:				; CODE XREF: start+3A1j
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	sub_199F9
		xor	ax, ax
		xchg	ax, [word_1DE62]
		or	ax, ax
		jnz	loc_193AE
		sub	[word_1DE5E], 0Fh
		jnb	loc_193AE
		mov	[word_1DE5E], 0
		jmp	loc_193AE
; ---------------------------------------------------------------------------

loc_19610:				; CODE XREF: start:loc_19439j
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		call	sub_199F9
		mov	ax, [word_1DE54]
		dec	ax
		cmp	ax, 0Fh
		jb	short loc_19648
		mov	ax, 0Eh
		xchg	ax, [word_1DE62]
		cmp	ax, 0Eh
		jnz	loc_193AE
		add	[word_1DE5E], 0Fh
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
		mov	si, offset unk_1DCFD ; str
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
		test	[cs:keyb_switches], 4
		jnz	short loc_196B0
		cmp	[byte ptr fs:2], 2
		jnz	loc_193BC
		mov	[word_1DE60], 0FFFFh
		test	[byte ptr fs:3], 40h
		jnz	short loc_19698
		or	[byte ptr fs:3], 40h
		inc	[word_1DE5C]
		jmp	loc_1953C
; ---------------------------------------------------------------------------

loc_19698:				; CODE XREF: start+5F7j
		and	[byte ptr fs:3], 0BFh
		sub	[word_1DE5C], 1
		jnb	loc_1953C
		mov	[word_1DE5C], 0
		jmp	loc_1953C
; ---------------------------------------------------------------------------

loc_196B0:				; CODE XREF: start+5DFj
		cmp	[word_1DE5C], 0
		jz	loc_193BC
		mov	cx, 602h
		mov	dx, 1A4Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7800h
		call	draw_frame
		mov	si, offset aDeleteMarkedFil ; "Delete marked files? [Y/N]"
		mov	ax, 7E0Dh
		call	message_1BE77

loc_196D0:				; CODE XREF: start+647j start+649j
		xor	ax, ax
		xchg	ax, [cs:key_code]
		or	ax, ax
		jz	short loc_196D0
		js	short loc_196D0
		mov	[byte_1DE7F], 0
		cmp	ax, 15h
		jnz	loc_192FF
		mov	fs, [word_1DE52]
		mov	cx, [word_1DE54]

loc_196F1:				; CODE XREF: start+6BAj
		test	[byte ptr fs:3], 40h
		jz	short loc_19744
		cmp	[byte ptr fs:2], 2
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
		mov	[dword ptr aFile], eax ; "File"
		mov	eax, [fs:10h]
		mov	[dword ptr aName], eax ; "name"
		mov	eax, [fs:14h]
		mov	[dword ptr a_ext], eax ; ".Ext"
		mov	si, offset aDeletingFile ; "Deleting file: "
		mov	ax, 7E0Dh
		call	message_1BE77
		mov	dx, offset aFile ; "File"
		mov	ah, 41h
		int	21h		; DOS -	2+ - DELETE A FILE (UNLINK)
					; DS:DX	-> ASCIZ pathname of file to delete (no	wildcards allowed)
		pop	fs
		pop	cx

loc_19744:				; CODE XREF: start+665j start+66Dj
		mov	ax, fs
		add	ax, 3
		mov	fs, ax
		assume fs:nothing
		dec	cx
		jnz	short loc_196F1
		mov	[word_1DE62], 0
		mov	[word_1DE5E], 0
		mov	[byte_1DE7F], 1
		jmp	loc_192FF
; ---------------------------------------------------------------------------

loc_19762:				; CODE XREF: start+3ADj
					; DATA XREF: dseg:7C8Fo
		cmp	[byte_1DE7C], 1
		jz	loc_193BC
		mov	cx, 602h
		mov	dx, 1A4Eh
		mov	bl, 7Fh	; ''
		mov	ax, 7800h
		call	draw_frame
		call	[off_1DE3C]
		call	sub_19EFD
		mov	[byte_1DE7F], 0
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
		assume es:nothing
		add	di, 1042h
		mov	cx, 4Eh	; 'N'
		mov	ax, 7820h	; 'x'
		cld
		rep stosw
		mov	si, offset aU	; "ž"
		les	di, [videomempointer]
		call	write_scr

loc_197BF:				; CODE XREF: start+733j
		cmp	[byte ptr cs:key_code],	0
		jle	short loc_197BF
		mov	[cs:key_code], 0
		mov	[byte_1DE7F], 0
		jmp	loc_192F7
; ---------------------------------------------------------------------------

loc_197D6:				; CODE XREF: start+3BFj
		call	sub_1C70F
		call	sub_1C1B9
		call	mouseinit
		mov	[byte_1DE7F], 0
		jmp	loc_192F7
; ---------------------------------------------------------------------------

loc_197E7:				; CODE XREF: start+3C5j
		xor	[byte ptr configword], 20h
		call	sub_197F2
		jmp	loc_193BC
endp		start


; =============== S U B	R O U T	I N E =======================================


proc		sub_197F2 near		; CODE XREF: start+327p start+75Ap
		test	[byte ptr configword], 20h
		jnz	short loc_19810
		mov	[word_1D614], 664Fh
		mov	[byte_1D616], 66h ; 'f'
		mov	[word_1D669], 664Fh
		mov	[byte_1D66B], 66h ; 'f'
		retn
; ---------------------------------------------------------------------------

loc_19810:				; CODE XREF: sub_197F2+5j
		mov	[word_1D614], 6E4Fh
		mov	[byte_1D616], 20h ; ' '
		mov	[word_1D669], 6E4Fh
		mov	[byte_1D66B], 20h ; ' '
		retn
endp		sub_197F2

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR start

loc_19827:				; CODE XREF: start+343j
		call	sub_1C756
		and	[byte_1DE90], 0FEh
		mov	bx, offset str_24461 ; mystr
		mov	ax, [mousecolumn]
		mov	bp, [mouserow]
		shr	ax, 3
		shr	bp, 3
		call	sub_1C7CF
		jb	loc_193BC
		jmp	bx
; ---------------------------------------------------------------------------

loc_19848:				; CODE XREF: start+33Aj
		call	sub_1C756
		mov	bx, offset stru_2448B ;	mystr
		mov	ax, [mousecolumn]
		mov	bp, [mouserow]
		shr	ax, 3
		shr	bp, 3
		call	sub_1C7CF
		jb	loc_193BC
		push	es
		xor	dx, dx
		mov	es, dx
		assume es:nothing
		mov	edx, [es:46Ch]
		cmp	edx, [dword_1DE88]
		jz	short loc_1987C
		mov	[dword_1DE88], edx
		pop	es
		assume es:nothing
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


proc		sub_1988C near		; CODE XREF: start+251p sub_1C1B9+53p
		push	si
		mov	ah, 19h
		int	21h		; DOS -	GET DEFAULT DISK NUMBER
		pop	si
		mov	[si], al
		mov	[byte ptr si+1], '\'
		add	si, 2
		xor	dl, dl
		mov	ah, 47h
		int	21h		; DOS -	2+ - GET CURRENT DIRECTORY
					; DL = drive (0=default, 1=A, etc.)
					; DS:SI	points to 64-byte buffer area
		retn
endp		sub_1988C


; =============== S U B	R O U T	I N E =======================================


; void __usercall doschdir(char	*str<esi>)
proc		doschdir near		; CODE XREF: start+5BFp sub_1C1B9+A6p
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
endp		doschdir

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR filelist_198B8

loc_198B0:				; CODE XREF: filelist_198B8+8j
		mov	ax, [word_1DE62]
		mov	bl, 70h	; 'p'
		jmp	sub_199F9
; END OF FUNCTION CHUNK	FOR filelist_198B8

; =============== S U B	R O U T	I N E =======================================


proc		filelist_198B8 near	; CODE XREF: start:loc_193AEp

; FUNCTION CHUNK AT 0860 SIZE 00000008 BYTES

		cld
		mov	ax, [word_1DE5E]
		cmp	ax, [word_1DE60]
		jz	short loc_198B0
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
		assume fs:nothing
		mov	ax, 654h

loc_198E7:				; CODE XREF: filelist_198B8+13Cj
		push	ax
		push	cx
		les	di, [videomempointer]
		add	di, ax
		mov	bp, di
		mov	ah, 7Eh	; '~'
		cmp	[byte ptr fs:2], 2
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
		cmp	[byte ptr fs:2], 2
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
		assume es:dseg
		mov	di, offset buffer_1 ; 2800h
		mov	bp, 8
		mov	eax, [fs:8]
		call	sub_1ACFD

loc_1993D:
		mov	ax, [fs:6]
		and	al, 1Fh
		movzx	eax, al
		mov	bp, 3
		call	sub_1ACFD
		mov	[byte ptr di], '-'

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
		mov	[byte ptr di], '-'
		inc	di
		movzx	eax, [word ptr fs:6]
		shr	ax, 9
		add	ax, 1980
		mov	bp, 4
		call	sub_1ACFD
		mov	[byte ptr di], ' '
		inc	di
		mov	ax, [fs:4]
		shr	ax, 0Bh
		mov	dl, 10
		div	dl
		or	ax, '00'
		mov	[di], ax
		mov	[byte ptr di+2], ':'
		mov	ax, [fs:4]
		shr	ax, 5
		and	ax, 3Fh	; '?'
		div	dl
		or	ax, '00'
		mov	[di+3],	ax
		mov	[word ptr di+5], ' '
		pop	bp
		mov	si, offset buffer_1 ; str
		mov	es, [word ptr videomempointer+2]
		assume es:nothing
		lea	di, [bp+18h]
		mov	ah, 7Fh	; ''
		call	text_1BF69
		test	[byte ptr fs:3], 40h
		jz	short loc_199CF
		mov	si, offset aMarkedToDelete ; "<Marked to Delete>    "
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
		assume fs:nothing
		pop	cx
		pop	ax
		add	ax, 0A0h ; ' '
		dec	cx
		jnz	loc_198E7
		retn
endp		filelist_198B8


; =============== S U B	R O U T	I N E =======================================


proc		sub_199F9 near		; CODE XREF: start+324p start+4C1p ...
		imul	di, ax,	160
		add	di, 1617
		mov	cx, 64

loc_19A04:				; CODE XREF: sub_199F9+19j
		mov	al, [es:di]
		and	al, 0Fh
		or	al, bl
		mov	[es:di], al
		add	di, 2
		dec	cx
		jnz	short loc_19A04
		retn
endp		sub_199F9


; =============== S U B	R O U T	I N E =======================================


proc		sub_19A15 near		; CODE XREF: modules_search+230p
		push	si
		push	di

loc_19A17:				; CODE XREF: sub_19A15+Ej
		mov	al, [si]
		inc	si
		cmp	al, ' '
		jb	short loc_19A25
		mov	[es:di], al
		inc	di
		dec	cx
		jnz	short loc_19A17

loc_19A25:				; CODE XREF: sub_19A15+7j
		cld
		mov	al, ' '
		rep stosb
		pop	di
		pop	si
		retn
endp		sub_19A15

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


proc		modules_search near	; CODE XREF: start+300p
		mov	[word_1DE64], 2192
		mov	[word_1DE66], 0
		cmp	[word_1DE52], 0
		jz	short loc_19A6E
		mov	es, [word_1DE52]
		assume es:nothing
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
		assume es:nothing
		xor	di, di
		mov	cx, 4000h
		xor	eax, eax
		cld
		rep stosd
		mov	[dword ptr byte_1DB6C],	2A2E2Ah	; '*.*'
		mov	[word_1DE5C], 0
		mov	[word_1DE54], 0
		mov	[word_1DE56], 0
		mov	[word_1DE58], 0
		mov	[word_1DE5A], 0
		cld
		mov	[word_1DE4E], 12h
		call	sub_1C29E
		mov	es, [word_1DE52]
		jb	loc_19CA2

loc_19AC3:				; CODE XREF: modules_search+CFj
		lfs	di, [videomempointer]
		assume fs:nothing
		add	di, [word_1DE64]
		mov	bx, [word_1DE66]
		mov	ah, 7Fh	; ''
		mov	al, [byte ptr slider+bx] ; "Ä\\|/Ä\\|/"
		mov	[fs:di], ax
		inc	[word_1DE66]
		and	[word_1DE66], 7
		test	[byte ptr unk_1DC01], 10h
		jz	short loc_19B1D
		cmp	[word ptr byte_1DB6C], '.'
		jz	short loc_19B1D
		mov	[byte ptr es:2], 0
		mov	si, offset byte_1DB6C
		mov	di, 0Ch
		cld
		movsd
		movsd
		movsd
		movsb
		inc	[word_1DE56]
		mov	ax, es
		add	ax, 3
		mov	es, ax
		assume es:nothing
		inc	[word_1DE54]
		cmp	[word_1DE54], 52Bh
		jnb	loc_19CA2

loc_19B1D:				; CODE XREF: modules_search+94j
					; modules_search+9Bj
		push	es
		call	sub_1C332
		pop	es
		assume es:nothing
		jnb	short loc_19AC3

loc_19B24:				; '*.*'
		mov	[dword ptr byte_1DB6C],	2A2E2Ah
		mov	[word_1DE4E], 2
		push	es
		call	sub_1C29E
		pop	es
		assume es:nothing
		jb	loc_19CA2

loc_19B3C:				; CODE XREF: modules_search+24Bj
		lfs	di, [videomempointer]
		add	di, [word_1DE64]
		mov	bx, [word_1DE66]
		mov	ah, 7Fh	; ''
		mov	al, [byte ptr slider+bx] ; "Ä\\|/Ä\\|/"
		mov	[fs:di], ax
		inc	[word_1DE66]
		and	[word_1DE66], 7
		test	[byte ptr unk_1DC01], 10h
		jnz	loc_19C99
		mov	si, offset byte_1DB6C
		mov	cx, 8

loc_19B6A:				; CODE XREF: modules_search+125j
		inc	si
		cmp	[byte ptr si], 0
		jz	loc_19C99
		cmp	[byte ptr si], '.'
		jz	short loc_19B7D
		dec	cx
		jnz	short loc_19B6A
		jmp	loc_19C99
; ---------------------------------------------------------------------------

loc_19B7D:				; CODE XREF: modules_search+122j
		mov	edx, [si]
		mov	si, offset a_mod_nst_669_s ; ".MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FA"...

loc_19B83:				; CODE XREF: modules_search+13Fj
		mov	eax, [si]
		or	al, al
		jz	loc_19C99
		add	si, 4
		cmp	eax, edx
		jnz	short loc_19B83
		mov	si, offset byte_1DB6C
		mov	dx, si
		mov	[byte ptr es:2], 2
		mov	[word ptr es:0], 0
		mov	di, 0Ch
		cld
		movsd
		movsd
		movsd
		movsb
		mov	si, offset unk_1DC01

loc_19BB4:
		mov	di, 3
		movsb
		and	[byte ptr es:3], 3Fh ; '?'
		movsd
		movsd
		mov	ebp, eax
		inc	[word_1DE58]
		cmp	[cs:key_code], 1
		jnz	short loc_19BDD
		mov	[cs:key_code], 0
		or	[byte ptr configword], 20h

loc_19BDD:				; CODE XREF: modules_search+17Cj
		mov	si, offset asc_1DA00 ; "		      "
		mov	cx, 16h
		test	[byte ptr configword], 20h
		jnz	loc_19C80
		mov	ax, 3D00h
		int	21h		; DOS -	2+ - OPEN DISK FILE WITH HANDLE
					; DS:DX	-> ASCIZ filename
					; AL = access mode
					; 0 - read
		jb	loc_19C86
		mov	bx, ax
		mov	dx, offset buffer_1DC6C
		mov	bx, ax
		mov	cx, 80h	; '€'
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
		mov	si, offset byte_1DC7C
		mov	cx, 16h
		cmp	ebp, 524E492Eh	; .INR
		jz	short loc_19C80
		mov	si, offset unk_1DC7B
		mov	cx, 16h
		cmp	ebp, 544C552Eh	; .ULT
		jz	short loc_19C80
		mov	si, offset unk_1DC70
		mov	cx, 16h
		cmp	ebp, 4D544D2Eh	; .MTM
		jz	short loc_19C80
		cmp	ebp, 4D53502Eh	; .PSM
		jz	short loc_19C80
		cmp	ebp, 5241462Eh	; .FAR
		jz	short loc_19C80
		cmp	ebp, 3936362Eh	; .669
		jz	short loc_19C71
		mov	si, offset byte_1DC7C
		mov	cx, 16h
		cmp	ebp, 5353542Eh	; .TSS
		jz	short loc_19C80
		mov	si, offset buffer_1DC6C
		mov	cx, 16h
		mov	[word ptr si+14h], '  '
		jmp	short loc_19C80
; ---------------------------------------------------------------------------

loc_19C71:				; CODE XREF: modules_search+200j
		mov	si, (offset buffer_1DC6C+1)
		mov	cx, 54h	; 'T'

loc_19C77:				; CODE XREF: modules_search+228j
		inc	si
		cmp	[byte ptr si], ' '
		loope	loc_19C77
		mov	cx, 16h

loc_19C80:				; CODE XREF: modules_search+195j
					; modules_search+1C7j ...
		mov	di, 1Ah
		call	sub_19A15

loc_19C86:				; CODE XREF: modules_search+19Ej
					; modules_search+1B8j
		mov	ax, es
		add	ax, 3
		mov	es, ax
		assume es:nothing
		inc	[word_1DE54]
		cmp	[word_1DE54], 52Bh
		jnb	short loc_19CA2

loc_19C99:				; CODE XREF: modules_search+10Dj
					; modules_search+11Bj ...
		push	es
		call	sub_1C332
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
		mov	[byte ptr es:10h], 0
		mov	[byte ptr es:2], 1
		inc	[word_1DE5A]
		mov	ax, es
		add	ax, 3
		mov	es, ax
		assume es:nothing
		inc	[word_1DE54]

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
		assume es:nothing
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
endp		modules_search


; =============== S U B	R O U T	I N E =======================================


proc		parse_cmdline near	; CODE XREF: start+44p
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		xor	ebp, ebp
		mov	ds, [esseg_atstart]
		assume ds:nothing
		mov	si, 80h	; '€'   ; psp:80h commandline
		mov	di, offset byte_1DB6C
		xor	dl, dl
		cld
		lodsb
		movzx	cx, al		; number of bytes on commandline
		stc
		jcxz	short loc_19D64

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
		mov	[byte ptr es:di], 0
		mov	ax, es
		mov	ds, ax
		assume ds:dseg
		retn
endp		parse_cmdline


; =============== S U B	R O U T	I N E =======================================


proc		sub_19D6D near		; CODE XREF: start+1ABp sub_19D6D+12j	...
		mov	dx, offset byte_1DB6C
		call	sub_19E11
		jb	short loc_19D83

loc_19D75:
		cmp	[word_1DE50], 1
		jz	short loc_19D81
		call	sub_1C332
		jnb	short sub_19D6D

loc_19D81:				; CODE XREF: sub_19D6D+Dj
		clc
		retn
; ---------------------------------------------------------------------------

loc_19D83:				; CODE XREF: sub_19D6D+6j
		mov	[byte_1DE7E], 3
		mov	[word ptr messagepointer], offset aModuleLoadErro ; "Module load error.\r\n$"
		mov	[word ptr messagepointer+2], ds
		stc
		retn
endp		sub_19D6D

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR start

loc_19D94:				; CODE XREF: start+18Ej
		mov	[byte_1DE7E], 4
		mov	[word ptr messagepointer], offset aListFileNotFou ; "List file not found.\r\n$"
		mov	[word ptr messagepointer+2], ds
		mov	dx, (offset byte_1DB6C+1)
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
		mov	dx, offset byte_1DB6C

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
		cmp	[byte ptr di], 1Ah
		jz	short loc_19E03
		cmp	[byte ptr di], ' '
		jnb	short loc_19DBB
		mov	[byte ptr di], 0
		cmp	[byte_1DB6C], 0
		jz	short loc_19DB8
		cmp	[byte_1DB6C], ';'
		jz	short loc_19DB8
		push	bx
		mov	[word_1DE4E], 2
		call	sub_1C29E
		jb	short loc_19DF9
		call	sub_19D6D

loc_19DF9:				; CODE XREF: start+D62j
		pop	bx
		cmp	[word_1DE50], 1
		jnz	short loc_19DB8
		jmp	short loc_19E09
; ---------------------------------------------------------------------------

loc_19E03:				; CODE XREF: start+D36j start+D3Aj ...
		mov	[byte ptr di], 0
		call	sub_19D6D

loc_19E09:				; CODE XREF: start+D6Fj
		mov	[byte_1DE7E], 0
		jmp	loc_19250
; END OF FUNCTION CHUNK	FOR start

; =============== S U B	R O U T	I N E =======================================


proc		sub_19E11 near		; CODE XREF: start+424p sub_19D6D+3p
		mov	[byte_1DE7E], 3
		mov	[word ptr messagepointer], offset aModuleLoadErro ; "Module load error.\r\n$"
		mov	[word ptr messagepointer+2], ds
		mov	si, dx

loc_19E22:				; CODE XREF: sub_19E11+16j
		inc	si
		cmp	[byte ptr si-1], 0
		jnz	short loc_19E22
		mov	cx, 0Ch

loc_19E2C:				; CODE XREF: sub_19E11+2Dj
		dec	si
		cmp	[byte ptr si-1], ':'
		jz	short loc_19E41
		cmp	[byte ptr si-1], '\'
		jz	short loc_19E41
		cmp	si, dx
		jbe	short loc_19E41
		dec	cx
		jnz	short loc_19E2C
		dec	si

loc_19E41:				; CODE XREF: sub_19E11+20j
					; sub_19E11+26j ...
		mov	di, (offset aFilename_ext+1)
		mov	cx, 0Ch

loc_19E47:				; CODE XREF: sub_19E11+4Bj
		mov	al, [si]
		inc	si
		or	al, al
		jz	short loc_19E5E
		cmp	al, 'a'
		jb	short loc_19E58
		cmp	al, 'z'
		ja	short loc_19E58
		and	al, 0DFh

loc_19E58:				; CODE XREF: sub_19E11+3Fj
					; sub_19E11+43j
		mov	[di], al
		inc	di
		dec	cx
		jnz	short loc_19E47

loc_19E5E:				; CODE XREF: sub_19E11+3Bj
		mov	ax, ds
		mov	es, ax
		mov	al, ' '
		cld
		rep stosb
		call	moduleread
		jb	loc_1A042
		mov	[current_patterns], 0
		mov	[byte_1DE84], 0
		call	sub_126A9
		mov	[dword ptr asc_1CC85], eax ; "	  "
		xor	ch, ch
		mov	[word_1DE44], cx
		mov	[byte_1DE73], bl
		call	sub_12CCF
		mov	[outp_freq], bp
		call	sub_1265D
		mov	[byte_1DE78], dl
		mov	al, dh
		and	al, 10h
		shr	al, 4
		mov	[byte_1DE7B], al
		mov	[word ptr segfsbx_1DE28], si
		mov	[word ptr segfsbx_1DE28+2], es
		mov	si, di
		mov	di, (offset asc_1CC2C+1)
		mov	cx, 30

loc_19EBA:				; CODE XREF: sub_19E11+B4j
		mov	al, [es:si]
		or	al, al
		jz	short loc_19EC7
		mov	[di], al
		inc	si
		inc	di
		loop	loc_19EBA

loc_19EC7:				; CODE XREF: sub_19E11+AEj
		mov	cx, 17
		xor	si, si

loc_19ECC:				; CODE XREF: sub_19E11+C3j
		mov	al, [es:si]
		mov	[byte ptr a130295211558+si], al	; "13/02/95 21:15:58"
		inc	si
		loop	loc_19ECC
		call	video_1C340
		xor	edx, edx
		mov	eax, 317
		movzx	ebx, [word_1DE44]
		div	ebx
		mov	[volume_1DE34],	eax
		mov	[byte_1DE7C], 0
		call	sub_12EBA
		call	[off_1DE3C]
endp		sub_19E11 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_19EFD near		; CODE XREF: start+6EBp sub_19EFD+5Aj	...
		call	sub_1265D
		mov	[byte_1DE72], ah
		mov	[byte_1DE74], al
		mov	[byte_1DE75], bh
		mov	[byte_1DE76], ch
		mov	ax, 0FFFFh
		call	change_volume
		mov	[word_1DE6A], ax
		mov	ax, 0FFFFh
		call	change_amplif
		mov	[word_1DE6C], ax
		call	sub_12AD3
		mov	[byte_1DE77], al
		call	[offs_draw]
		cmp	[byte_1DE7C], 1
		jz	loc_1A393
		test	[byte_1DE90], 2
		jnz	loc_1A3C5
		test	[byte_1DE90], 1
		jnz	loc_1A3A7
		xor	ax, ax
		xchg	ax, [cs:key_code]
		or	ax, ax
		jz	short sub_19EFD
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
		jb	sub_19EFD
		cmp	al, 0Bh
		jbe	loc_1A33E
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

loc_1A042:				; CODE XREF: sub_19E11+5Bj
		stc
		retn
; ---------------------------------------------------------------------------

l_1A044:				; CODE XREF: sub_19EFD+65j
					; sub_19EFD:loc_19F6Cj	...
		push	cx
		call	sub_12F7C
		and	bx, 3Fh
		movzx	eax, ax
		shl	eax, 6
		or	al, bl
		inc	eax
		mov	bl, al
		and	bl, 3Fh
		shr	eax, 6
		mov	bh, 1
		call	sub_12F56
		pop	cx
		dec	cx
		jnz	short l_1A044
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

loc_1A070:				; CODE XREF: sub_19EFD+79j
					; sub_19EFD+86j ...
		push	cx
		call	sub_12F7C
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
		call	sub_12F56
		pop	cx
		dec	cx
		jnz	short loc_1A070
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

loc_1A0A0:				; CODE XREF: sub_19EFD+18Aj
		pop	cx
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_up:					; CODE XREF: sub_19EFD+92j
		sub	[byte_1DE84], 1
		jnb	sub_19EFD
		mov	[byte_1DE84], 0
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_down:					; CODE XREF: sub_19EFD+9Ej
		inc	[byte_1DE84]
		mov	ax, [word_1DE44]
		cmp	[byte_1DE84], al
		jb	sub_19EFD
		dec	al
		mov	[byte_1DE84], al
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_right:				; CODE XREF: sub_19EFD+8Cj
		lfs	bx, [segfsbx_1DE28]
		mov	al, 50h	; 'P'
		mul	[byte_1DE84]
		add	bx, ax
		mov	cl, 8
		test	[cs:keyb_switches], 3
		jnz	short loc_1A0E6
		mov	cl, 1

loc_1A0E6:				; CODE XREF: sub_19EFD+1E5j
		mov	al, [fs:bx+3Ah]
		add	al, cl
		cmp	al, 80h	; '€'
		jbe	short loc_1A0F2
		mov	al, 80h	; '€'

loc_1A0F2:				; CODE XREF: sub_19EFD+1F1j
					; sub_19EFD+221j ...
		mov	ch, [byte_1DE84]
		call	sub_12AFD
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_left:					; CODE XREF: sub_19EFD+98j
		lfs	bx, [segfsbx_1DE28]
		mov	al, 50h	; 'P'
		mul	[byte_1DE84]
		add	bx, ax
		mov	cl, 8
		test	[cs:keyb_switches], 3
		jnz	short loc_1A118
		mov	cl, 1

loc_1A118:				; CODE XREF: sub_19EFD+217j
		mov	al, [fs:bx+3Ah]
		sub	al, cl
		jnb	short loc_1A0F2
		mov	al, 0
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_l:					; CODE XREF: sub_19EFD+FEj
		mov	al, 0
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_m:					; CODE XREF: sub_19EFD+104j
		mov	al, 64
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_r:					; CODE XREF: sub_19EFD+10Aj
		mov	al, 128
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_s:					; CODE XREF: sub_19EFD+110j
		mov	al, 166
		jmp	short loc_1A0F2
; ---------------------------------------------------------------------------

l_plus:					; CODE XREF: sub_19EFD+A4j
		mov	ax, -1
		call	change_volume
		mov	cx, 32
		test	[cs:keyb_switches], 3
		jnz	short loc_1A14B
		mov	cx, 2

loc_1A14B:				; CODE XREF: sub_19EFD+249j
		add	ax, cx
		cmp	ax, 256
		jb	short loc_1A155
		mov	ax, 256

loc_1A155:				; CODE XREF: sub_19EFD+253j
		call	change_volume
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_minus:				; CODE XREF: sub_19EFD+AAj
		mov	ax, -1
		call	change_volume
		mov	cx, 32
		test	[cs:keyb_switches], 3
		jnz	short loc_1A174
		mov	cx, 2

loc_1A174:				; CODE XREF: sub_19EFD+272j
		sub	ax, cx
		jnb	short loc_1A17A
		xor	ax, ax

loc_1A17A:				; CODE XREF: sub_19EFD+279j
		call	change_volume
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_rbracket:				; CODE XREF: sub_19EFD+B6j
		mov	ax, 0FFFFh
		call	change_amplif
		mov	cx, 1
		test	[cs:keyb_switches], 3
		jnz	short loc_1A199
		mov	cx, 0Ah

loc_1A199:				; CODE XREF: sub_19EFD+297j
		add	ax, cx
		cmp	ax, 2500
		jb	short loc_1A1A3
		mov	ax, 2500

loc_1A1A3:				; CODE XREF: sub_19EFD+2A1j
		call	change_amplif
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_lbracket:				; CODE XREF: sub_19EFD+B0j
		mov	ax, -1
		call	change_amplif
		mov	cx, 1
		test	[cs:keyb_switches], 3
		jnz	short loc_1A1C2
		mov	cx, 10

loc_1A1C2:				; CODE XREF: sub_19EFD+2C0j
		sub	ax, cx
		jnb	short loc_1A1C9
		mov	ax, 50

loc_1A1C9:				; CODE XREF: sub_19EFD+2C7j
		cmp	ax, 50
		ja	short loc_1A1D1
		mov	ax, 50

loc_1A1D1:				; CODE XREF: sub_19EFD+2CFj
		call	change_amplif
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f1:					; CODE XREF: sub_19EFD+BCj
		call	f1_help
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f2:					; CODE XREF: sub_19EFD+C2j
		call	f2_equal
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f3:					; CODE XREF: sub_19EFD+C8j
		call	f3_textmetter
		mov	[byte_1DE85], 0
		test	[cs:keyb_switches], 3
		jz	sub_19EFD
		mov	[byte_1DE85], 1
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f4:					; CODE XREF: sub_19EFD+CEj
		cmp	[offs_draw], offset f4_draw
		jnz	short loc_1A219
		mov	ax, [word_1DE6E]
		dec	ax
		add	[current_patterns], ax
		mov	ax, [current_patterns]
		cmp	ax, [word_1DE46]
		jb	short loc_1A21F

loc_1A219:				; CODE XREF: sub_19EFD+309j
		mov	[current_patterns], 0

loc_1A21F:				; CODE XREF: sub_19EFD+31Aj
		call	f4_patternnae
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f5:					; CODE XREF: sub_19EFD+D4j
		call	f5_graphspectr
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f6:					; CODE XREF: sub_19EFD+DAj
		call	f6_undoc
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f8:					; CODE XREF: sub_19EFD+E0j
		call	[off_1DE42]
		call	sub_1C1B9
		mov	[byte_1DE70], 0FFh
		call	[off_1DE3C]
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f9:					; CODE XREF: sub_19EFD+E6j
		test	[cs:keyb_switches], 100b
		jnz	short l_f11
		call	sub_12AD3
		xor	al, 1
		call	sub_12ADE
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f10:					; CODE XREF: sub_19EFD+ECj
		test	[cs:keyb_switches], 100b
		jnz	short l_f12
		call	sub_12AD3
		xor	al, 2
		call	sub_12ADE
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f11:					; CODE XREF: sub_19EFD+F2j
					; sub_19EFD+34Ej
		call	sub_12AD3
		xor	al, 4
		call	sub_12ADE
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_f12:					; CODE XREF: sub_19EFD+F8j
					; sub_19EFD+366j
		call	sub_12AD3

loc_1A288:
		xor	al, 10h
		call	sub_12ADE

loc_1A28F:
		xor	[byte ptr configword+1], 1
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_tab:					; CODE XREF: sub_19EFD+116j
		test	[cs:keyb_switches], 100b
		jnz	short loc_1A2C1

loc_1A2A0:
		test	[cs:keyb_switches], 1000b
		jnz	short loc_1A2D1
		test	[cs:keyb_switches], 11b
		jnz	short loc_1A2E1
		call	sub_12AD3
		xor	al, 8
		call	sub_12ADE

loc_1A2BE:
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

loc_1A2C1:				; CODE XREF: sub_19EFD+3A1j
		mov	cx, 0FFh
		xor	bx, bx
		mov	dx, 7D0Fh
		call	sub_12CAD
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

loc_1A2D1:				; CODE XREF: sub_19EFD+3AAj
		mov	cx, 0FFh
		xor	bx, bx
		mov	dx, 910Fh
		call	sub_12CAD
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

loc_1A2E1:				; CODE XREF: sub_19EFD+3B3j
		mov	cx, 0FFh
		xor	bx, bx
		mov	dx, 960Fh
		call	sub_12CAD
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_numlock:				; CODE XREF: sub_19EFD+11Cj
		test	[cs:keyb_switches], 100b
		jz	sub_19EFD
		mov	al, 0FFh
		call	sub_12C99
		mov	ah, al
		mov	al, 1
		cmp	ah, al
		jnz	short loc_1A30D
		mov	al, 0

loc_1A30D:				; CODE XREF: sub_19EFD+40Cj
		call	sub_12C99
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_scrollock:				; CODE XREF: sub_19EFD+122j
		mov	al, 0FFh
		call	sub_12C99
		mov	ah, al
		mov	al, 2
		cmp	ah, al
		jnz	short loc_1A326
		mov	al, 0

loc_1A326:				; CODE XREF: sub_19EFD+425j
		call	sub_12C99
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_1_end:				; CODE XREF: sub_19EFD+128j
		mov	cx, 0FFh
		xor	bx, bx
		mov	dx, 0Dh
		call	sub_12CAD
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

loc_1A33E:				; CODE XREF: sub_19EFD+13Ej
		sub	al, 2
		test	[cs:keyb_switches], 11b
		jz	short loc_1A34B
		add	al, 10

loc_1A34B:				; CODE XREF: sub_19EFD+44Aj
		test	[cs:keyb_switches], 100b
		jz	short loc_1A356
		add	al, 20

loc_1A356:				; CODE XREF: sub_19EFD+455j
		cmp	al, [byte ptr word_1DE44]
		jnb	sub_19EFD
		mov	ch, al
		lfs	bx, [segfsbx_1DE28]
		mov	ah, 80
		mul	ah
		add	bx, ax
		xor	[byte ptr fs:bx+17h], 2
		mov	bx, 0FEh ; 'þ'
		xor	cl, cl
		xor	dx, dx
		call	sub_12CAD
		jmp	sub_19EFD
; ---------------------------------------------------------------------------

l_enter:				; CODE XREF: sub_19EFD+12Ej
					; DATA XREF: dseg:stru_244ABo
		call	[offs_draw]
		call	[off_1DE40]
		clc
		retn
; ---------------------------------------------------------------------------

l_esc:					; CODE XREF: sub_19EFD+134j
					; DATA XREF: dseg:stru_244B7o
		mov	[byte_1DE7C], 1
		and	[byte_1DE90], 0FDh

loc_1A393:				; CODE XREF: sub_19EFD+3Bj
		call	[offs_draw]
		call	[off_1DE40]
		call	sub_12F48
		call	sub_125DA
		clc
		retn
; ---------------------------------------------------------------------------

loc_1A3A7:				; CODE XREF: sub_19EFD+4Dj
		and	[byte_1DE90], 0FEh
		mov	bx, offset stru_244AB ;	mystr
		mov	ax, [mousecolumn]
		mov	bp, [mouserow]
		shr	ax, 3
		shr	bp, 3
		call	sub_1C7CF
		jb	sub_19EFD
		jmp	bx
; ---------------------------------------------------------------------------

loc_1A3C5:				; CODE XREF: sub_19EFD+44j
		mov	bx, offset stru_244B7 ;	mystr
		mov	ax, [mousecolumn]
		mov	bp, [mouserow]
		shr	ax, 3
		shr	bp, 3
		call	sub_1C7CF
		jb	sub_19EFD
		push	es
		xor	dx, dx
		mov	es, dx
		assume es:nothing
		mov	edx, [es:46Ch]
		cmp	edx, [dword_1DE88]
		jz	short loc_1A3F6
		mov	[dword_1DE88], edx
		pop	es
		assume es:nothing
		jmp	bx
; ---------------------------------------------------------------------------

loc_1A3F6:				; CODE XREF: sub_19EFD+4EFj
		pop	es
		jmp	loc_193BC
endp		sub_19EFD


; =============== S U B	R O U T	I N E =======================================


proc		f1_help	near		; CODE XREF: sub_19EFD:l_f1p
					; DATA XREF: dseg:02A6o
		mov	[off_1DE3C], offset text_init
		mov	[offs_draw], offset f1_draw
		mov	[off_1DE40], offset text_init2
		mov	[off_1DE42], offset loc_1A4A6
		call	text_init
		retn
endp		f1_help


; =============== S U B	R O U T	I N E =======================================


proc		f2_equal near		; CODE XREF: sub_19EFD:l_f2p
					; DATA XREF: dseg:02A0o
		mov	[off_1DE3C], offset init_vga_equalizr
		mov	[offs_draw], offset f2_draw_metters
		mov	[off_1DE40], offset video_1AF63
		mov	[off_1DE42], offset init_vga_equalizr
		call	init_vga_equalizr
		retn
endp		f2_equal


; =============== S U B	R O U T	I N E =======================================


proc		f3_textmetter near	; CODE XREF: sub_19EFD:l_f3p
					; DATA XREF: dseg:off_1CA8Eo
		mov	[off_1DE3C], offset text_init
		mov	[offs_draw], offset f3_draw
		mov	[off_1DE40], offset text_init2
		mov	[off_1DE42], offset loc_1A4A6
		call	text_init
		retn
endp		f3_textmetter


; =============== S U B	R O U T	I N E =======================================


proc		f4_patternnae near	; CODE XREF: sub_19EFD:loc_1A21Fp
					; DATA XREF: dseg:02A4o
		mov	[off_1DE3C], offset text_init
		mov	[offs_draw], offset f4_draw
		mov	[off_1DE40], offset text_init2
		mov	[off_1DE42], offset loc_1A4A6
		call	text_init
		retn
endp		f4_patternnae


; =============== S U B	R O U T	I N E =======================================


proc		f5_graphspectr near	; CODE XREF: sub_19EFD:l_f5p
					; DATA XREF: dseg:02A2o
		mov	[off_1DE3C], offset init_f5_spectr
		mov	[offs_draw], offset f5_draw
		mov	[off_1DE40], offset f5_draw
		mov	[off_1DE42], offset init_f5_spectr
		call	init_f5_spectr
		retn
endp		f5_graphspectr


; =============== S U B	R O U T	I N E =======================================


proc		f6_undoc near		; CODE XREF: sub_19EFD:l_f6p
					; DATA XREF: dseg:02A8o
		mov	[off_1DE3C], offset text_init
		mov	[offs_draw], offset f6_draw
		mov	[off_1DE40], offset text_init2
		mov	[off_1DE42], offset loc_1A4A6
		call	text_init
		retn
endp		f6_undoc


; =============== S U B	R O U T	I N E =======================================


proc		text_init near		; CODE XREF: f1_help+18p
					; f3_textmetter+18p ...
		call	text_init2
		retn
endp		text_init

; ---------------------------------------------------------------------------

loc_1A4A6:				; DATA XREF: f1_help+12o
					; f3_textmetter+12o ...
		call	text_init2
		retn

; =============== S U B	R O U T	I N E =======================================


proc		text_init2 near		; CODE XREF: text_initp
					; seg001:loc_1A4A6p
					; DATA XREF: ...

; FUNCTION CHUNK AT 14A2 SIZE 0000026B BYTES

		cmp	[byte_1DE86], 1
		jz	short loc_1A4F2
		cmp	[word_1DE44], 0Ah
		jbe	short loc_1A4F2
		jmp	loc_1A5AB
endp		text_init2


; =============== S U B	R O U T	I N E =======================================


proc		setvideomode near	; CODE XREF: start:loc_192F7p
					; text_init2:loc_1A4F2p
		cmp	[byte_1DE70], 0
		jz	short locret_1A4F1
		cmp	[byte_1DE70], 1
		jz	short locret_1A4F1
		mov	ax, 3
		cmp	[byte_1DE70], 2
		jnz	short loc_1A4D5
		or	al, 80h

loc_1A4D5:				; CODE XREF: setvideomode+16j
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		call	blinkingoff
		cmp	[byte_1DE86], 1
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
endp		setvideomode

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR text_init2

loc_1A4F2:				; CODE XREF: text_init2+5j
					; text_init2+Cj
		call	setvideomode
		cmp	[byte_1DE86], 1
		jz	short loc_1A55B
		mov	[word_1DE6E], 0Ah
		mov	eax, [videomempointer]
		add	ax, 36*80
		mov	[videopoint_shiftd], eax
		cmp	[byte_1DE70], 0
		jz	short loc_1A545
		cmp	[byte_1DE70], 1
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
		mov	[byte_1DE70], 0
		jmp	loc_1A628
; ---------------------------------------------------------------------------

loc_1A55B:				; CODE XREF: text_init2+50j
		mov	[word_1DE6E], 7
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
		mov	[byte_1DE70], 0
		jmp	short loc_1A628
; ---------------------------------------------------------------------------

loc_1A5AB:				; CODE XREF: text_init2+Ej
		cmp	[byte_1DE70], 2
		jz	short loc_1A61A
		mov	ax, 3
		cmp	[byte_1DE70], 1
		jz	short loc_1A5C3
		cmp	[byte_1DE70], 0
		jnz	short loc_1A5C5

loc_1A5C3:				; CODE XREF: text_init2+110j
		or	al, 80h

loc_1A5C5:				; CODE XREF: text_init2+117j
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		call	blinkingoff
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
		mov	[byte_1DE70], 2
		mov	[word_1DE6E], 20h ; ' '
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
		call	sub_1A75D
		mov	ax, ds
		mov	bx, offset buffer_1 ; 2800h
		shr	bx, 4
		add	ax, bx
		mov	[buffer_1seg], ax
		movzx	si, [snd_card_type]
		cmp	si, 0Ah
		jb	short loc_1A645
		mov	si, 0Ah

loc_1A645:				; CODE XREF: text_init2+196j
		shl	si, 1
		mov	si, [table_sndcrdname+si] ; str
		les	di, [videopoint_shiftd]
		add	di, 58h	; 'X'   ; buf
		mov	ah, 7Fh	; ''
		call	put_message
		cmp	[snd_card_type], 0
		jnz	short loc_1A687
		push	di
		push	es
		call	sub_1265D
		pop	es
		pop	di
		mov	[word ptr es:di], 7F20h
		add	di, 2		; buf
		movzx	si, dh
		and	si, 1100000b
		shr	si, 3
		add	si, offset a256	; str
		mov	ah, 7Fh	; ''
		call	put_message
		mov	si, offset aKb	; str
		call	put_message

loc_1A687:				; CODE XREF: text_init2+1B2j
		cmp	[snd_card_type], 0Ah
		jz	short loc_1A6B7
		mov	si, (offset buffer_1DC6C+2)

loc_1A691:				; ' )'
		mov	[word ptr buffer_1DC6C], 2820h
		xor	dx, dx

loc_1A699:
		mov	ax, [outp_freq]
		mov	cx, 1000
		div	cx

loc_1A6A1:
		call	my_i8toa
		mov	[dword ptr si],	297A486Bh ; 'kHz('
		mov	[byte ptr si+4], 0
		mov	si, offset buffer_1DC6C	; str
		mov	ah, 7Fh	; ''
		call	put_message

loc_1A6B7:				; CODE XREF: text_init2+1E2j
		mov	al, 78h	; 'x'
		cmp	[byte_1DE7B], 1
		jnz	short loc_1A6C2
		mov	al, 7Ch	; '|'

loc_1A6C2:				; CODE XREF: text_init2+214j
		mov	[byte_1CCEB], al
		les	di, [videopoint_shiftd]
		mov	si, offset asc_1CC2A ; str
		call	write_scr
		call	sub_126A9
		mov	[word ptr dword_1DE2C],	si
		mov	[word ptr dword_1DE2C+2], es
		push	cx
		mov	si, offset buffer_1DC6C
		mov	al, ch
		push	bx
		call	my_i8toa
		pop	bx
		mov	[byte ptr si], '/'
		inc	si
		movzx	ax, bh
		mov	[word_1DE46], ax
		call	my_i8toa
		mov	[dword ptr si],	'   '
		mov	si, offset buffer_1DC6C	; str
		les	di, [videopoint_shiftd]
		add	di, 2AAh	; buf
		mov	ah, 7Fh	; ''
		call	put_message
		pop	cx
		mov	si, offset buffer_1DC6C
		mov	al, cl
		call	my_i8toa
		mov	[dword ptr si],	'   '
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 20Ah	; buf
		mov	ah, 7Fh	; ''
		call	put_message
		mov	bx, 0FFFFh
		mov	ah, 48h
		int	21h		; DOS -	2+ - ALLOCATE MEMORY
					; BX = number of 16-byte paragraphs desired
		mov	ax, bx
		shr	ax, 6
		mov	si, offset buffer_1DC6C
		call	my_i16toa
		mov	[dword ptr si],	20424Bh	; 'KB '
		cmp	si, (offset buffer_1DC6C+2)
		jb	short loc_1A74D
		mov	[byte ptr si+2], 0

loc_1A74D:				; CODE XREF: text_init2+29Dj
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 12Eh	; buf
		mov	ah, 7Fh	; ''
		call	put_message
		retn
; END OF FUNCTION CHUNK	FOR text_init2

; =============== S U B	R O U T	I N E =======================================


proc		sub_1A75D near		; CODE XREF: start+201p start+27Bp ...
		mov	cx, 102h
		mov	dx, 44Dh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		les	di, [videomempointer]
		mov	si, offset word_1CB6E ;	str
		call	write_scr
		retn
endp		sub_1A75D


; =============== S U B	R O U T	I N E =======================================


proc		draw_text_bottom near	; CODE XREF: seg001:f3_drawp
					; seg001:f4_drawp ...
		mov	si, offset buffer_1DC6C
		mov	eax, '    '
		mov	[si], eax
		mov	[si+4],	eax
		mov	[si+8],	eax
		mov	[si+0Ch], al
		mov	[byte ptr si+0Dh], 0
		mov	al, [byte_1DE75]
		call	my_i8toa
		mov	[dword ptr si],	20746120h ; ' at '
		add	si, 4
		mov	al, [byte_1DE76]
		call	my_i8toa
		mov	[word ptr si], 7062h ; bp
		mov	[byte ptr si+2], 'm'
		mov	si, offset buffer_1DC6C	; str
		les	di, [videopoint_shiftd]
		add	di, 48Ah	; buf
		mov	ah, 7Fh	; ''
		call	put_message
		mov	si, offset aPal	; "(PAL) "
		test	[byte_1DE77], 8
		jnz	short loc_1A7CC
		mov	si, offset aNtsc ; str

loc_1A7CC:				; CODE XREF: draw_text_bottom+51j
		les	di, [videopoint_shiftd]
		add	di, 476h	; buf
		mov	ah, 7Eh	; '~'
		call	put_message
		mov	si, offset buffer_1DC6C
		mov	al, [byte_1DE72]
		inc	al
		call	my_i8toa
		mov	[byte ptr si], '/'
		inc	si
		mov	al, [byte_1DE73]
		call	my_i8toa
		mov	[dword ptr si],	'   '
		mov	si, offset buffer_1DC6C	; str
		les	di, [videopoint_shiftd]
		add	di, 34Ah	; buf
		mov	ah, 7Fh	; ''
		call	put_message
		mov	si, offset buffer_1DC6C
		mov	al, [byte_1DE74]
		inc	al
		call	my_i8toa
		mov	[dword ptr si],	2034362Fh ; /64
		mov	[word ptr si+4], ' '
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 3EAh	; buf
		mov	ah, 7Fh	; ''
		call	put_message
		les	di, [videopoint_shiftd]
		add	di, 198h
		mov	ah, 7Ch	; '|'
		test	[byte_1DE77], 1
		jnz	short loc_1A83E
		mov	ah, 78h	; 'x'

loc_1A83E:				; CODE XREF: draw_text_bottom+C4j
		mov	al, 0FEh ; 'þ'
		mov	[es:di], ax
		les	di, [videopoint_shiftd]
		add	di, 238h
		mov	ah, 7Ch	; '|'
		test	[byte_1DE77], 2
		jnz	short loc_1A856
		mov	ah, 78h	; 'x'

loc_1A856:				; CODE XREF: draw_text_bottom+DCj
		mov	al, 0FEh ; 'þ'
		mov	[es:di], ax
		les	di, [videopoint_shiftd]
		add	di, 2D8h
		mov	ah, 7Ch	; '|'
		test	[byte_1DE77], 4
		jnz	short loc_1A86E
		mov	ah, 78h	; 'x'

loc_1A86E:				; CODE XREF: draw_text_bottom+F4j
		mov	al, 0FEh ; 'þ'
		mov	[es:di], ax
		les	di, [videopoint_shiftd]
		add	di, 378h
		mov	ah, 7Ch	; '|'
		test	[byte_1DE77], 10h
		jnz	short loc_1A886
		mov	ah, 78h	; 'x'

loc_1A886:				; CODE XREF: draw_text_bottom+10Cj
		mov	al, 0FEh ; 'þ'
		mov	[es:di], ax
		mov	si, offset buffer_1DC6C
		imul	ax, [word_1DE6A], 100
		mov	al, ah
		call	my_i8toa
		mov	[dword ptr si],	202025h	; '%  '
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 43Ah	; buf
		mov	ah, 7Fh	; ''
		call	put_message
		mov	si, offset buffer_1DC6C
		mov	ax, [word_1DE6C]
		call	my_i16toa
		mov	[dword ptr si],	202025h	; '%  '
		sub	si, cx		; str
		les	di, [videopoint_shiftd]
		add	di, 4DAh	; buf
		mov	ah, 7Fh	; ''
		call	put_message
		mov	al, 0FFh
		call	sub_12C99
		movzx	si, al
		shl	si, 2
		add	si, offset aPlaypausloop ; "PlayPausLoop"
		les	di, [videopoint_shiftd]
		add	di, 0FCh ; 'ü'
		mov	ah, 7Eh	; '~'
		mov	cx, 4

loc_1A8EB:				; CODE XREF: draw_text_bottom+17Fj
		mov	al, [si]
		mov	[es:di], ax
		inc	si
		add	di, 2
		dec	cx
		jnz	short loc_1A8EB
		retn
endp		draw_text_bottom

; ---------------------------------------------------------------------------

f3_draw:				; DATA XREF: f3_textmetter+6o
		call	draw_text_bottom
		cmp	[byte_1DE85], 1
		jz	short loc_1A913
		mov	es, [buffer_1seg]
		assume es:nothing
		xor	di, di
		mov	cx, 50h	; 'P'
		mov	ax, 4001h
		call	volume_prep

loc_1A913:				; CODE XREF: seg001:18B0j
		mov	[buffer_2seg], offset buffer_1 ; 2800h
		lfs	bx, [segfsbx_1DE28]
		les	di, [videomempointer]
		assume es:nothing
		add	di, 3C4h
		mov	cx, [word_1DE44]
		cmp	cx, [word_1DE6E]
		jbe	short loc_1A934
		mov	cx, [word_1DE6E]

loc_1A934:				; CODE XREF: seg001:18DEj
		inc	[byte_1DE71]
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
		movzx	si, [byte ptr fs:bx+35h]
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
		mov	al, [byte ptr notes+si]	; "  C-C#D-D#E-F-F#G-G#A-A#B-"
		mov	[es:di], ax
		mov	al, [byte ptr (notes+1)+si]
		mov	[es:di+2], ax
		add	di, 8
		test	[byte ptr fs:bx+17h], 1
		jnz	short loc_1A9AD
		mov	si, offset aMute ; "<Mute>		  "
		mov	ah, 7Fh	; ''
		test	[byte ptr fs:bx+17h], 2
		jnz	short loc_1A9A8

loc_1A9A5:				; CODE XREF: seg001:1964j
		mov	si, offset asc_1DA00 ; "		      "

loc_1A9A8:				; CODE XREF: seg001:1953j
		call	put_message
		jmp	short loc_1A9C2
; ---------------------------------------------------------------------------

loc_1A9AD:				; CODE XREF: seg001:1947j
		movzx	eax, [byte ptr fs:bx+2]
		dec	ax
		js	short loc_1A9A5
		shl	ax, 6
		mov	si, ax
		add	si, [word ptr dword_1DE2C]
		call	sub_1ABAE

loc_1A9C2:				; CODE XREF: seg001:195Bj
		add	di, 2
		cmp	[byte_1DE85], 1
		jnz	short loc_1AA1A
		push	di
		push	es
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		mov	di, offset buffer_1 ; 2800h
		cld
		movzx	eax, [byte ptr fs:bx+2]
		mov	bp, 2
		call	sub_1ACFD
		mov	bp, 4
		movzx	eax, [byte ptr fs:bx+22h]
		call	sub_1ACFD
		mov	bp, 7
		movzx	eax, [word ptr fs:bx+1Eh]
		call	sub_1ACFD
		mov	ax, ds
		mov	es, ax
		mov	eax, '    '
		mov	cx, 4
		rep stosd
		mov	[byte ptr di], 0
		pop	es
		assume es:nothing
		pop	di
		mov	si, offset buffer_1 ; 2800h
		mov	ah, 7Eh	; '~'
		call	put_message

loc_1AA17:
		jmp	loc_1AACB
; ---------------------------------------------------------------------------

loc_1AA1A:				; CODE XREF: seg001:197Aj
		cmp	[snd_card_type], 0Ah
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
		div	[volume_1DE34]
		cmp	al, 60
		jb	short loc_1AA4F
		mov	al, 60

loc_1AA4F:				; CODE XREF: seg001:19FBj
		cmp	[byte_1DE83], 0
		jz	short loc_1AA5C
		cmp	al, [fs:bx+1Ah]
		jb	short loc_1AA73

loc_1AA5C:				; CODE XREF: seg001:1A04j
		mov	[fs:bx+1Ah], al
		jmp	short loc_1AA88
; ---------------------------------------------------------------------------

loc_1AA62:				; CODE XREF: seg001:19CFj
		test	[byte ptr fs:bx+17h], 1
		jz	short loc_1AA73
		mov	al, [fs:bx+22h]
		mov	[fs:bx+1Ah], al
		jmp	short loc_1AA88
; ---------------------------------------------------------------------------

loc_1AA73:				; CODE XREF: seg001:1A0Aj seg001:1A17j
					; DATA XREF: ...
		and	[byte_1DE71], 1Fh
		jnz	short loc_1AA88
		mov	al, [byte_1DE83]
		sub	[fs:bx+1Ah], al
		jns	short loc_1AA88
		mov	[byte ptr fs:bx+1Ah], 0

loc_1AA88:				; CODE XREF: seg001:1A10j seg001:1A21j ...
		movzx	cx, [byte ptr fs:bx+1Ah]
		shr	cx, 1
		mov	dx, 30
		sub	dx, cx
		jcxz	short volume_endstr
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
		mov	si, offset asc_1D6E0 ; "	       "
		mov	al, [fs:bx+0Ah]
		cmp	al, 1Dh
		jz	short loc_1AB0D
		cmp	al, 0Eh
		jnz	short loc_1AAF0
		mov	si, offset aSetLoopPoint ; "Set	Loop Point "
		mov	al, [fs:bx+0Bh]
		cmp	al, 60h	; '`'
		jz	short loc_1AAF7
		mov	si, offset aSetFilter ;	"Set Filter	"
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
		add	di, 0A0h ; ' '
		add	bx, 50h	; 'P'
		inc	ax
		dec	cx
		jnz	loc_1A93A
		retn
; ---------------------------------------------------------------------------

loc_1AB0D:				; CODE XREF: seg001:1A89j
		mov	si, offset aArpeggio ; "Arpeggio       "
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
		mov	[dword ptr si+9], '    '
		mov	[word ptr si+0Dh], '  '
		jmp	short loc_1AAF7
; ---------------------------------------------------------------------------

loc_1AB53:				; CODE XREF: seg001:1ACEj
		mov	[dword ptr si+0Bh], 73756C70h ;	puls
		jmp	short loc_1AB6F
; ---------------------------------------------------------------------------

loc_1AB5D:				; CODE XREF: seg001:1AC6j
		mov	[dword ptr si+0Bh], 206E696Dh ;	min
		jmp	short loc_1AB6F
; ---------------------------------------------------------------------------

loc_1AB67:				; CODE XREF: seg001:1ACAj
		mov	[dword ptr si+0Bh], 206A616Dh ;	maj

loc_1AB6F:				; CODE XREF: seg001:1B0Bj seg001:1B15j
		mov	al, [fs:bx+35h]
		and	ax, 0Fh
		jz	short loc_1AB44
		cmp	al, 0Ch
		ja	short loc_1AB44
		shl	ax, 1
		push	si
		mov	si, ax
		mov	ax, [word ptr notes+si]	; "  C-C#D-D#E-F-F#G-G#A-A#B-"
		pop	si
		mov	[si+9],	ax
		jmp	loc_1AAF7

; =============== S U B	R O U T	I N E =======================================


proc		sub_1AB8C near		; CODE XREF: seg001:1AD2p seg001:1ADFp ...
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
		mov	ax, [word ptr notes+si]	; "  C-C#D-D#E-F-F#G-G#A-A#B-"
		pop	si
		cmp	ah, 2Dh	; '-'
		jz	short loc_1ABAB
		retn
; ---------------------------------------------------------------------------

loc_1ABAB:				; CODE XREF: sub_1AB8C+1Cj
		mov	ah, 20h	; ' '
		retn
endp		sub_1AB8C


; =============== S U B	R O U T	I N E =======================================


proc		sub_1ABAE near		; CODE XREF: seg001:196Fp
		mov	ah, 7Bh	; '{'
		mov	cx, 16h

loc_1ABB3:				; CODE XREF: sub_1ABAE+10j
		mov	al, [fs:si]
		mov	[es:di], ax
		inc	si
		add	di, 2
		dec	cx
		jnz	short loc_1ABB3
		retn
endp		sub_1ABAE

; ---------------------------------------------------------------------------

f4_draw:				; DATA XREF: sub_19EFD:l_f4o
					; f4_patternnae+6o
		call	draw_text_bottom
		les	di, [videomempointer]
		add	di, 3C6h
		mov	si, offset aSamplename ; "# SampleName	 "
		mov	ah, 7Eh	; '~'
		call	text_1BF69
		mov	di, [word ptr videomempointer]
		add	di, 464h
		lfs	bx, [dword_1DE2C]
		mov	bp, [current_patterns]
		imul	ax, bp,	40h
		add	bx, ax
		mov	dl, [byte ptr word_1DE6E]
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
		assume es:dseg
		mov	di, offset buffer_1 ; 2800h
		cld
		movzx	eax, bp
		inc	ax
		mov	bp, 2
		call	sub_1ACF6
		mov	[dword ptr di],	7B0220h
		add	di, 3
		mov	si, bx
		mov	cx, 8
		cld
		rep movs [dword	ptr es:di], [dword ptr fs:si]
		test	[byte ptr fs:bx+3Ch], 1
		jnz	short loc_1AC35
		mov	si, offset unk_1D6C3
		mov	cx, 9
		rep movsb
		jmp	loc_1ACD2
; ---------------------------------------------------------------------------

loc_1AC35:				; CODE XREF: seg001:1BD8j
		mov	eax, [fs:bx+20h]
		mov	bp, 7
		call	sub_1ACF6
		movzx	eax, [byte ptr fs:bx+3Dh]
		mov	bp, 3
		call	sub_1ACF6
		mov	eax, 363120h	; ' 16'
		test	[byte ptr fs:bx+3Ch], 4
		jnz	short loc_1AC5F
		mov	eax, 382020h	; '  8'

loc_1AC5F:				; CODE XREF: seg001:1C07j
		mov	[di], eax
		mov	al, 1Dh
		test	[byte ptr fs:bx+3Ch], 10h
		jnz	short loc_1AC6D
		mov	al, ' '

loc_1AC6D:				; CODE XREF: seg001:1C19j
		mov	[di+3],	al
		add	di, 4
		movzx	eax, [word ptr fs:bx+36h]
		mov	bp, 6
		call	sub_1ACF6
		mov	[dword ptr di],	7A487E02h
		add	di, 4
		mov	[dword ptr di],	7F0220h
		add	di, 3
		mov	eax, '    '
		mov	ah, [fs:bx+3Eh]
		and	ah, 0Fh
		test	ah, 8
		jz	short loc_1ACAC
		mov	al, 2Dh	; '-'
		neg	ah
		add	ah, 10h

loc_1ACAC:				; CODE XREF: seg001:1C53j
		or	ah, 30h
		mov	[di], eax
		add	di, 4
		test	[byte ptr fs:bx+3Ch], 8
		jz	short loc_1ACD2
		mov	eax, [fs:bx+24h]
		mov	bp, 7
		call	sub_1ACF6
		mov	eax, [fs:bx+2Ch]
		mov	bp, 7
		call	sub_1ACF6

loc_1ACD2:				; CODE XREF: seg001:1BE2j seg001:1C6Aj
		mov	[byte ptr di], 0
		pop	di
		push	di
		mov	es, [word ptr videomempointer+2]
		assume es:nothing
		mov	si, offset buffer_1 ; 2800h
		mov	ah, 7Fh	; ''
		call	text_1BF69
		pop	di
		pop	bp
		pop	dx
		pop	bx
		add	bx, 40h	; '@'
		inc	bp
		add	di, 0A0h ; ' '
		dec	dl
		jnz	loc_1ABF0

locret_1ACF5:				; CODE XREF: seg001:1BA4j
		retn

; =============== S U B	R O U T	I N E =======================================


proc		sub_1ACF6 near		; CODE XREF: seg001:1BBCp seg001:1BEDp ...
		mov	[word ptr di], 7F02h
		add	di, 2
endp		sub_1ACF6 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1ACFD near		; CODE XREF: filelist_198B8+82p
					; filelist_198B8+92p ...
		mov	si, offset buffer_1DC6C
		push	bx
		push	di
		push	bp
		call	my_i32toa
		pop	bp
		pop	di
		pop	bx
		cmp	cx, bp
		jb	short loc_1AD0F
		mov	cx, bp

loc_1AD0F:				; CODE XREF: sub_1ACFD+Ej
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
endp		sub_1ACFD

; ---------------------------------------------------------------------------

f1_draw:				; DATA XREF: f1_help+6o
		call	draw_text_bottom
		les	di, [videomempointer]
		assume es:nothing
		mov	si, offset f1_help_text
		call	write_scr
		retn

; =============== S U B	R O U T	I N E =======================================


proc		init_vga_equalizr near	; CODE XREF: f2_equal+18p
					; DATA XREF: f2_equalo	...

; FUNCTION CHUNK AT 1DDD SIZE 0000008D BYTES

		cmp	[byte_1DE70], 3
		jz	loc_1AEB2
		mov	[byte_1DE70], 3
		mov	ax, 12h
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		mov	dx, offset palette_24404
		mov	ax, 1002h
		int	10h		; - VIDEO - SET	ALL PALETTE REGISTERS (Jr, PS, TANDY 1000, EGA,	VGA)
					; ES:DX	-> 17-byte palette register list
		mov	dx, offset vga_palette
		mov	cx, 10h
		xor	bx, bx
		mov	ax, 1012h
		int	10h		; - VIDEO - SET	BLOCK OF DAC REGISTERS (EGA, VGA/MCGA)
					; BX = starting	color register,	CX = number of registers to set
					; ES:DX	-> table of 3*CX bytes where each 3 byte group represents one
					; byte each of red, green and blue (0-63)
		mov	si, offset buffer_1DC6C
		call	getexename
		jb	loc_1AE66
		mov	dx, offset buffer_1DC6C
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
		mov	dx, offset buffer_1DC6C
		mov	cx, 2
		mov	bx, [fhandle_1DE68]
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		jb	loc_1AE5E
		cmp	ax, 2
		jnz	loc_1AE5E
		cmp	[word ptr buffer_1DC6C], 4453h ; 'SD' check picture signature
		jnz	loc_1AE5E
		call	set_egavga
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
		assume es:nothing
		mov	dx, 3C4h
		mov	al, 2
		out	dx, al		; EGA: sequencer address reg
					; map mask: data bits 0-3 enable writes	to bit planes 0-3
		inc	dl
		xor	bx, bx

loc_1ADE0:				; CODE XREF: init_vga_equalizr+12Aj
		mov	ah, 1

loc_1ADE2:				; CODE XREF: init_vga_equalizr+121j
		mov	al, ah
		out	dx, al		; EGA port: sequencer data register
		xor	di, di

loc_1ADE7:				; CODE XREF: init_vga_equalizr+11Aj
		mov	cl, [si]
		inc	si
		cmp	si, offset buffer_1seg
		jnb	short loc_1AE0C	; WARNING: push	returns	address	to stack

loc_1ADF0:				; DATA XREF: init_vga_equalizr:loc_1AE0Co
		or	cl, cl
		js	short loc_1AE2D
		inc	cl

loc_1ADF6:				; CODE XREF: init_vga_equalizr+D9j
		mov	al, [es:bx+di]
		mov	al, [si]
		mov	[es:bx+di], al
		inc	si
		cmp	si, offset buffer_1seg
		jnb	short loc_1AE11

loc_1AE05:				; DATA XREF: init_vga_equalizr:loc_1AE11o
		inc	di
		dec	cl
		jnz	short loc_1ADF6
		jmp	short loc_1AE46
; ---------------------------------------------------------------------------

loc_1AE0C:				; CODE XREF: init_vga_equalizr+BFj
		push	offset loc_1ADF0 ; WARNING: push returns address to stack
		jmp	short read2buffer
; ---------------------------------------------------------------------------

loc_1AE11:				; CODE XREF: init_vga_equalizr+D4j
		push	offset loc_1AE05
		jmp	short read2buffer
; ---------------------------------------------------------------------------

loc_1AE16:				; CODE XREF: init_vga_equalizr+109j
		push	offset loc_1AE3A
endp		init_vga_equalizr ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		read2buffer near	; CODE XREF: init_vga_equalizr+94p
					; init_vga_equalizr+E0j ...
		pusha
		mov	dx, offset buffer_1 ; 2800h
		mov	cx, 5000h
		mov	bx, [fhandle_1DE68]
		mov	ah, 3Fh
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		popa
		mov	si, offset buffer_1 ; 2800h
		retn
endp		read2buffer

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR init_vga_equalizr

loc_1AE2D:				; CODE XREF: init_vga_equalizr+C3j
		neg	cl
		inc	cl
		mov	al, [si]
		inc	si
		cmp	si, offset buffer_1seg
		jnb	short loc_1AE16

loc_1AE3A:				; CODE XREF: init_vga_equalizr+115j
					; DATA XREF: init_vga_equalizr:loc_1AE16o
		test	[byte ptr es:bx+di], 0
		mov	[es:bx+di], al
		inc	di
		dec	cl
		jnz	short loc_1AE3A

loc_1AE46:				; CODE XREF: init_vga_equalizr+DBj
		cmp	di, 50h	; 'P'
		jb	short loc_1ADE7
		shl	ah, 1
		test	ah, 10h
		jz	short loc_1ADE2
		add	bx, 50h	; 'P'
		cmp	bx, 9600h
		jb	short loc_1ADE0
		call	graph_1C070

loc_1AE5E:				; CODE XREF: init_vga_equalizr+52j
					; init_vga_equalizr+6Aj ...
		mov	bx, [fhandle_1DE68]
		mov	ah, 3Eh
		int	21h		; DOS -	2+ - CLOSE A FILE WITH HANDLE
					; BX = file handle

loc_1AE66:				; CODE XREF: init_vga_equalizr+32j
					; init_vga_equalizr+3Ej
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
		call	video_1C340

loc_1AE7E:				; CODE XREF: init_vga_equalizr+189j
					; video_1AF63+69j
		mov	ax, ds
		mov	bx, offset buffer_1 ; 2800h
		shr	bx, 4
		add	ax, bx
		mov	[buffer_1seg], ax
		add	ax, 280h	; (offset buffer_206E0 - offset	buffer_1DEE0)/16
		mov	[buffer_2seg], ax
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		mov	di, offset buffer_1 ; 2800h
		mov	cx, 0A00h
		xor	eax, eax
		cld
		rep stosd
		mov	di, offset buffer_2
		mov	cx, 0A00h
		mov	eax, 1010101h
		rep stosd
		retn
; ---------------------------------------------------------------------------

loc_1AEB2:				; CODE XREF: init_vga_equalizr+5j
		call	video_1AF63
		call	video_1C340
		jmp	short loc_1AE7E
; END OF FUNCTION CHUNK	FOR init_vga_equalizr
; ---------------------------------------------------------------------------

f2_draw_metters:			; DATA XREF: f2_equal+6o
		mov	es, [buffer_1seg]
		assume es:nothing
		xor	di, di
		mov	cx, 128h
		mov	ax, 0C001h
		call	volume_prep
		mov	ax, 0A000h
		mov	es, ax
		assume es:nothing
		mov	fs, [buffer_1seg]
		mov	gs, [buffer_2seg]
		mov	di, offset byte_1DE9C
		xor	si, si
		mov	cx, [word_1DE44]

loc_1AEE1:				; CODE XREF: seg001:1F06j
		push	cx
		push	si
		push	di
		mov	bp, [di]
		mov	dx, 3CEh
		mov	al, 8
		out	dx, al		; EGA: graph 1 and 2 addr reg:
					; bit mask
					; Bits 0-7 select bits to be masked in all planes
		mov	al, 80h	; '€'

loc_1AEEE:				; CODE XREF: seg001:1EF9j
		mov	ah, 25h	; '%'
		mov	dx, 3CFh
		out	dx, al		; EGA port: graphics controller	data register
		mov	bx, bp

loc_1AEF6:				; CODE XREF: seg001:1EF0j
		movsx	di, [byte ptr gs:si]
		movsx	dx, [byte ptr fs:si]
		cmp	di, dx
		jz	short loc_1AF3A
		neg	di
		mov	cx, di
		shl	di, 6
		shl	cx, 4
		add	di, cx
		lea	cx, [bx+di]
		or	cx, cx
		js	short loc_1AF1E
		cmp	cx, 5780h
		jnb	short loc_1AF1E
		and	[byte ptr es:bx+di], 7

loc_1AF1E:				; CODE XREF: seg001:1EC2j seg001:1EC8j
		neg	dx
		mov	di, dx
		shl	di, 6
		shl	dx, 4
		add	di, dx
		lea	cx, [bx+di]
		or	cx, cx
		js	short loc_1AF3A
		cmp	cx, 5780h
		jnb	short loc_1AF3A
		or	[byte ptr es:bx+di], 8

loc_1AF3A:				; CODE XREF: seg001:1EB0j seg001:1EDEj ...
		add	si, 8
		inc	bx
		dec	ah
		jnz	short loc_1AEF6
		sub	si, 128h
		inc	si
		shr	al, 1
		jnb	short loc_1AEEE
		pop	di
		pop	si
		pop	cx
		add	si, 128h
		add	di, 2
		dec	cx
		jnz	short loc_1AEE1
		mov	ax, [buffer_1seg]
		xchg	ax, [buffer_2seg]
		mov	[buffer_1seg], ax
		retn

; =============== S U B	R O U T	I N E =======================================


proc		video_1AF63 near	; CODE XREF: init_vga_equalizr:loc_1AEB2p
					; DATA XREF: f2_equal+Co
		mov	ax, 0A000h
		mov	es, ax
		mov	fs, [buffer_1seg]
		mov	gs, [buffer_2seg]
		mov	di, offset byte_1DE9C
		xor	si, si
		mov	cx, [word_1DE44]

loc_1AF79:				; CODE XREF: video_1AF63+67j
		push	cx
		push	si
		push	di
		mov	bp, [di]
		mov	dx, 3CEh
		mov	al, 8
		out	dx, al		; EGA: graph 1 and 2 addr reg:
					; bit mask
					; Bits 0-7 select bits to be masked in all planes
		mov	al, 80h	; '€'

loc_1AF86:				; CODE XREF: video_1AF63+5Aj
		mov	ah, 25h	; '%'
		mov	dx, 3CFh
		out	dx, al		; EGA port: graphics controller	data register
		mov	bx, bp

loc_1AF8E:				; CODE XREF: video_1AF63+51j
		movsx	di, [byte ptr gs:si]
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
		and	[byte ptr es:bx+di], 7

loc_1AFAE:				; CODE XREF: video_1AF63+3Fj
					; video_1AF63+45j
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
endp		video_1AF63


; =============== S U B	R O U T	I N E =======================================


proc		init_f5_spectr near	; CODE XREF: f5_graphspectr+18p
					; DATA XREF: f5_graphspectro ...
		cmp	[byte_1DE70], 4
		jz	locret_1B083
		mov	[byte_1DE70], 4
		mov	ax, 13h
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		call	set_egavga
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
		mov	al, 0FCh ; 'ü'
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
		assume es:dseg
		mov	di, offset unk_23EE4
		mov	cx, 0C8h ; 'È'
		xor	eax, eax
		cld
		rep stosd
		mov	ax, 200h
		test	[byte ptr configword], 8
		jnz	short loc_1B080
		shr	ax, 1

loc_1B080:				; CODE XREF: init_f5_spectr+ADj
		mov	[word_24524], ax

locret_1B083:				; CODE XREF: init_f5_spectr+5j
		retn
endp		init_f5_spectr


; =============== S U B	R O U T	I N E =======================================


proc		sub_1B084 near
		mov	[word_2450E], di
		mov	al, 1
		cmp	al, 1
		jnz	loc_1B240
		call	sub_1B406
		mov	ax, [word_24514]
		xor	si, si

loc_1B098:				; CODE XREF: sub_1B084+1Bj
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

loc_1B0CF:				; CODE XREF: sub_1B084+1A2j
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
		mov	[dword ptr unk_244C4], eax
		mov	eax, [multip_244CC]
		imul	[dword_244C8]
		shrd	eax, edx, 10h
		add	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	[multip_244D0]
		shrd	eax, edx, 10h
		sub	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	[multip_244CC]
		shrd	eax, edx, 10h
		add	[dword_244D4], eax
		mov	eax, [dword ptr	unk_244C4]
		imul	[multip_244D0]
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

loc_1B240:				; CODE XREF: sub_1B084+8j
		mov	ax, [word_24514]
		xor	si, si

loc_1B245:				; CODE XREF: sub_1B084+1C8j
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

loc_1B282:				; CODE XREF: sub_1B084+357j
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
		mov	[dword ptr unk_244C4], eax
		mov	eax, [dword_244C8]
		mov	[dword ptr unk_244C4], eax
		mov	eax, [multip_244CC]
		imul	[dword_244C8]
		shrd	eax, edx, 10h
		add	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	[multip_244D0]
		shrd	eax, edx, 10h
		sub	[dword_244C8], eax
		mov	eax, [dword_244D4]
		imul	[multip_244CC]
		shrd	eax, edx, 10h
		add	[dword_244D4], eax
		mov	eax, [dword ptr	unk_244C4]
		imul	[multip_244D0]
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
		call	sub_1B406
		retn
endp		sub_1B084


; =============== S U B	R O U T	I N E =======================================


proc		sub_1B406 near		; CODE XREF: sub_1B084+Cp
					; sub_1B084+37Ep ...
		mov	[word_2450E], di
		mov	[word_2450C], 0
		mov	cx, [word_24520]
		shl	cx, 1
		mov	[word_24522], cx
		mov	si, [word_2450E]
		shr	cx, 1
		mov	di, [word_2450E]
		mov	bp, di

loc_1B426:				; CODE XREF: sub_1B406+5Fj
		push	cx
		cmp	si, di
		jle	short loc_1B440
		mov	edx, [si]
		mov	ebx, [si+4]
		xchg	edx, [di]
		xchg	ebx, [di+4]
		mov	[si], edx
		mov	[si+4],	ebx

loc_1B440:				; CODE XREF: sub_1B406+23j
		sub	si, bp
		shr	si, 2
		mov	ax, [word_24522]
		shr	ax, 1

loc_1B44A:				; CODE XREF: sub_1B406+51j
		cmp	ax, 2
		jl	short loc_1B459
		cmp	si, ax
		jl	short loc_1B459
		sub	si, ax
		shr	ax, 1
		jmp	short loc_1B44A
; ---------------------------------------------------------------------------

loc_1B459:				; CODE XREF: sub_1B406+47j
					; sub_1B406+4Bj
		add	si, ax
		shl	si, 2
		add	si, bp
		pop	cx
		add	di, 8
		dec	cx
		jnz	short loc_1B426
		mov	[word_24516], 2

loc_1B46D:				; CODE XREF: sub_1B406+1BEj
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
		add	[word_2450C], 4
		mov	[dword_244C8], 10000h
		mov	[dword_244D4], 0
		mov	cx, [word_24516]
		shr	cx, 1
		mov	ax, 1

loc_1B4B3:				; CODE XREF: sub_1B406+1B4j
		push	cx
		push	ax
		shl	ax, 1
		dec	ax
		mov	[word_24518], ax
		mov	ax, [word_24522]
		sub	ax, [word_24518]
		cwd
		idiv	[word_2451C]
		mov	cx, ax
		inc	cx
		mov	ax, 0

loc_1B4CD:				; CODE XREF: sub_1B406+156j
		push	cx
		push	ax
		imul	[word_2451C]
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
		mov	[dword ptr unk_244C4], eax
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
		mov	eax, [dword ptr	unk_244C4]
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

locret_1B5C7:				; CODE XREF: sub_1B406+6Ej
		retn
endp		sub_1B406


; =============== S U B	R O U T	I N E =======================================


proc		f5_draw	near		; DATA XREF: f5_graphspectr+6o
					; f5_graphspectr+Co
		mov	ax, ds
		mov	es, ax
		mov	di, offset buffer_1 ; 2800h
		mov	cx, 200h
		mov	ax, 4001h
		call	volume_prep
		lfs	bx, [segfsbx_1DE28]
		mov	si, offset buffer_1 ; 2800h
		mov	di, offset byte_24204
		mov	bp, [word_1DE44]

loc_1B5EC:				; CODE XREF: f5_draw+2A1j
		mov	cx, bp
		xor	dx, dx
		cmp	[byte ptr fs:bx+3Ah], 40h ; '@'
		ja	short loc_1B5FC
		mov	al, [si]
		cbw
		add	dx, ax

loc_1B5FC:				; CODE XREF: f5_draw+2Dj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+8Ah], 40h ; '@'
		ja	short loc_1B610
		mov	al, [si+200h]
		cbw
		add	dx, ax

loc_1B610:				; CODE XREF: f5_draw+3Fj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+0DAh], 40h ; '@'
		ja	short loc_1B624
		mov	al, [si+400h]
		cbw
		add	dx, ax

loc_1B624:				; CODE XREF: f5_draw+53j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+12Ah], 40h ; '@'
		ja	short loc_1B638
		mov	al, [si+600h]
		cbw
		add	dx, ax

loc_1B638:				; CODE XREF: f5_draw+67j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+17Ah], 40h ; '@'
		ja	short loc_1B64C
		mov	al, [si+800h]
		cbw
		add	dx, ax

loc_1B64C:				; CODE XREF: f5_draw+7Bj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+1CAh], 40h ; '@'
		ja	short loc_1B660
		mov	al, [si+0A00h]
		cbw
		add	dx, ax

loc_1B660:				; CODE XREF: f5_draw+8Fj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+21Ah], 40h ; '@'
		ja	short loc_1B674
		mov	al, [si+0C00h]
		cbw
		add	dx, ax

loc_1B674:				; CODE XREF: f5_draw+A3j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+26Ah], 40h ; '@'
		ja	short loc_1B688
		mov	al, [si+0E00h]
		cbw
		add	dx, ax

loc_1B688:				; CODE XREF: f5_draw+B7j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+2BAh], 40h ; '@'
		ja	short loc_1B69C
		mov	al, [si+1000h]
		cbw
		add	dx, ax

loc_1B69C:				; CODE XREF: f5_draw+CBj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+30Ah], 40h ; '@'
		ja	short loc_1B6B0
		mov	al, [si+1200h]
		cbw
		add	dx, ax

loc_1B6B0:				; CODE XREF: f5_draw+DFj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+35Ah], 40h ; '@'
		ja	short loc_1B6C4
		mov	al, [si+1400h]
		cbw
		add	dx, ax

loc_1B6C4:				; CODE XREF: f5_draw+F3j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+3AAh], 40h ; '@'
		ja	short loc_1B6D8
		mov	al, [si+1600h]
		cbw
		add	dx, ax

loc_1B6D8:				; CODE XREF: f5_draw+107j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+3FAh], 40h ; '@'
		ja	short loc_1B6EC
		mov	al, [si+1800h]
		cbw
		add	dx, ax

loc_1B6EC:				; CODE XREF: f5_draw+11Bj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+44Ah], 40h ; '@'
		ja	short loc_1B700
		mov	al, [si+1A00h]
		cbw
		add	dx, ax

loc_1B700:				; CODE XREF: f5_draw+12Fj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+49Ah], 40h ; '@'
		ja	short loc_1B714
		mov	al, [si+1C00h]
		cbw
		add	dx, ax

loc_1B714:				; CODE XREF: f5_draw+143j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+4EAh], 40h ; '@'
		ja	short loc_1B728
		mov	al, [si+1E00h]
		cbw
		add	dx, ax

loc_1B728:				; CODE XREF: f5_draw+157j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+53Ah], 40h ; '@'
		ja	short loc_1B73C
		mov	al, [si+2000h]
		cbw
		add	dx, ax

loc_1B73C:				; CODE XREF: f5_draw+16Bj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+58Ah], 40h ; '@'
		ja	short loc_1B750
		mov	al, [si+2200h]
		cbw
		add	dx, ax

loc_1B750:				; CODE XREF: f5_draw+17Fj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+5DAh], 40h ; '@'
		ja	short loc_1B764
		mov	al, [si+2400h]
		cbw
		add	dx, ax

loc_1B764:				; CODE XREF: f5_draw+193j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+62Ah], 40h ; '@'
		ja	short loc_1B778
		mov	al, [si+2600h]
		cbw
		add	dx, ax

loc_1B778:				; CODE XREF: f5_draw+1A7j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+67Ah], 40h ; '@'
		ja	short loc_1B78C
		mov	al, [si+2800h]
		cbw
		add	dx, ax

loc_1B78C:				; CODE XREF: f5_draw+1BBj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+6CAh], 40h ; '@'
		ja	short loc_1B7A0
		mov	al, [si+2A00h]
		cbw
		add	dx, ax

loc_1B7A0:				; CODE XREF: f5_draw+1CFj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+71Ah], 40h ; '@'
		ja	short loc_1B7B4
		mov	al, [si+2C00h]
		cbw
		add	dx, ax

loc_1B7B4:				; CODE XREF: f5_draw+1E3j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+76Ah], 40h ; '@'
		ja	short loc_1B7C8
		mov	al, [si+2E00h]
		cbw
		add	dx, ax

loc_1B7C8:				; CODE XREF: f5_draw+1F7j
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+7BAh], 40h ; '@'
		ja	short loc_1B7DC
		mov	al, [si+3000h]
		cbw
		add	dx, ax

loc_1B7DC:				; CODE XREF: f5_draw+20Bj
		dec	cx
		jz	loc_1B85F
		cmp	[byte ptr fs:bx+80Ah], 40h ; '@'
		ja	short loc_1B7F0
		mov	al, [si+3200h]
		cbw
		add	dx, ax

loc_1B7F0:				; CODE XREF: f5_draw+21Fj
		dec	cx
		jz	short loc_1B85F
		cmp	[byte ptr fs:bx+85Ah], 40h ; '@'
		ja	short loc_1B802
		mov	al, [si+3400h]
		cbw
		add	dx, ax

loc_1B802:				; CODE XREF: f5_draw+231j
		dec	cx
		jz	short loc_1B85F
		cmp	[byte ptr fs:bx+8AAh], 40h ; '@'
		ja	short loc_1B814
		mov	al, [si+3600h]
		cbw
		add	dx, ax

loc_1B814:				; CODE XREF: f5_draw+243j
		dec	cx
		jz	short loc_1B85F
		cmp	[byte ptr fs:bx+8FAh], 40h ; '@'
		ja	short loc_1B826
		mov	al, [si+3800h]
		cbw
		add	dx, ax

loc_1B826:				; CODE XREF: f5_draw+255j
		dec	cx
		jz	short loc_1B85F
		cmp	[byte ptr fs:bx+94Ah], 40h ; '@'
		ja	short loc_1B838
		mov	al, [si+3A00h]
		cbw
		add	dx, ax

loc_1B838:				; CODE XREF: f5_draw+267j
		dec	cx
		jz	short loc_1B85F
		cmp	[byte ptr fs:bx+99Ah], 40h ; '@'
		ja	short loc_1B84A
		mov	al, [si+3C00h]
		cbw
		add	dx, ax

loc_1B84A:				; CODE XREF: f5_draw+279j
		dec	cx
		jz	short loc_1B85F
		cmp	[byte ptr fs:bx+9EAh], 40h ; '@'
		ja	short loc_1B85C
		mov	al, [si+3E00h]
		cbw
		add	dx, ax

loc_1B85C:				; CODE XREF: f5_draw+28Bj
		dec	cx
		jz	short $+2

loc_1B85F:				; CODE XREF: f5_draw+35j f5_draw+49j ...
		sar	dx, 1
		mov	[di], dl
		inc	si
		inc	di
		cmp	si, offset byte_1E0E0
		jb	loc_1B5EC
		mov	si, offset byte_24204
		mov	di, offset byte_22EE4
		mov	cx, 200h

loc_1B876:				; CODE XREF: f5_draw+2C5j
		movsx	eax, [byte ptr si]
		shl	eax, 10h
		mov	[di], eax
		mov	[dword ptr di+4], 0
		inc	si
		add	di, 8
		loop	loc_1B876
		mov	ax, [word_24524]
		mov	[word_24520], ax
		mov	[word_24514], ax
		mov	di, offset byte_22EE4
		call	sub_1B406
		mov	si, offset byte_22EE4
		mov	di, offset unk_23EE4
		mov	cx, 64h	; 'd'
		call	sub_1BBC1
		lfs	bx, [segfsbx_1DE28]
		mov	si, offset buffer_1 ; 2800h
		mov	di, offset byte_24204
		mov	bp, [word_1DE44]

loc_1B8BC:				; CODE XREF: f5_draw+571j
		mov	cx, bp
		xor	dx, dx
		cmp	[byte ptr fs:bx+3Ah], 40h ; '@'
		jb	short loc_1B8CC
		mov	al, [si]
		cbw
		add	dx, ax

loc_1B8CC:				; CODE XREF: f5_draw+2FDj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+8Ah], 40h ; '@'
		jb	short loc_1B8E0
		mov	al, [si+200h]
		cbw
		add	dx, ax

loc_1B8E0:				; CODE XREF: f5_draw+30Fj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+0DAh], 40h ; '@'
		jb	short loc_1B8F4
		mov	al, [si+400h]
		cbw
		add	dx, ax

loc_1B8F4:				; CODE XREF: f5_draw+323j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+12Ah], 40h ; '@'
		jb	short loc_1B908
		mov	al, [si+600h]
		cbw
		add	dx, ax

loc_1B908:				; CODE XREF: f5_draw+337j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+17Ah], 40h ; '@'
		jb	short loc_1B91C
		mov	al, [si+800h]
		cbw
		add	dx, ax

loc_1B91C:				; CODE XREF: f5_draw+34Bj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+1CAh], 40h ; '@'
		jb	short loc_1B930
		mov	al, [si+0A00h]
		cbw
		add	dx, ax

loc_1B930:				; CODE XREF: f5_draw+35Fj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+21Ah], 40h ; '@'
		jb	short loc_1B944
		mov	al, [si+0C00h]
		cbw
		add	dx, ax

loc_1B944:				; CODE XREF: f5_draw+373j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+26Ah], 40h ; '@'
		jb	short loc_1B958
		mov	al, [si+0E00h]
		cbw
		add	dx, ax

loc_1B958:				; CODE XREF: f5_draw+387j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+2BAh], 40h ; '@'
		jb	short loc_1B96C
		mov	al, [si+1000h]
		cbw
		add	dx, ax

loc_1B96C:				; CODE XREF: f5_draw+39Bj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+30Ah], 40h ; '@'
		jb	short loc_1B980
		mov	al, [si+1200h]
		cbw
		add	dx, ax

loc_1B980:				; CODE XREF: f5_draw+3AFj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+35Ah], 40h ; '@'
		jb	short loc_1B994
		mov	al, [si+1400h]
		cbw
		add	dx, ax

loc_1B994:				; CODE XREF: f5_draw+3C3j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+3AAh], 40h ; '@'
		jb	short loc_1B9A8
		mov	al, [si+1600h]
		cbw
		add	dx, ax

loc_1B9A8:				; CODE XREF: f5_draw+3D7j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+3FAh], 40h ; '@'
		jb	short loc_1B9BC
		mov	al, [si+1800h]
		cbw
		add	dx, ax

loc_1B9BC:				; CODE XREF: f5_draw+3EBj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+44Ah], 40h ; '@'
		jb	short loc_1B9D0
		mov	al, [si+1A00h]
		cbw
		add	dx, ax

loc_1B9D0:				; CODE XREF: f5_draw+3FFj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+49Ah], 40h ; '@'
		jb	short loc_1B9E4
		mov	al, [si+1C00h]
		cbw
		add	dx, ax

loc_1B9E4:				; CODE XREF: f5_draw+413j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+4EAh], 40h ; '@'
		jb	short loc_1B9F8
		mov	al, [si+1E00h]
		cbw
		add	dx, ax

loc_1B9F8:				; CODE XREF: f5_draw+427j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+53Ah], 40h ; '@'
		jb	short loc_1BA0C
		mov	al, [si+2000h]
		cbw
		add	dx, ax

loc_1BA0C:				; CODE XREF: f5_draw+43Bj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+58Ah], 40h ; '@'
		jb	short loc_1BA20
		mov	al, [si+2200h]
		cbw
		add	dx, ax

loc_1BA20:				; CODE XREF: f5_draw+44Fj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+5DAh], 40h ; '@'
		jb	short loc_1BA34
		mov	al, [si+2400h]
		cbw
		add	dx, ax

loc_1BA34:				; CODE XREF: f5_draw+463j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+62Ah], 40h ; '@'
		jb	short loc_1BA48
		mov	al, [si+2600h]
		cbw
		add	dx, ax

loc_1BA48:				; CODE XREF: f5_draw+477j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+67Ah], 40h ; '@'
		jb	short loc_1BA5C
		mov	al, [si+2800h]
		cbw
		add	dx, ax

loc_1BA5C:				; CODE XREF: f5_draw+48Bj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+6CAh], 40h ; '@'
		jb	short loc_1BA70
		mov	al, [si+2A00h]
		cbw
		add	dx, ax

loc_1BA70:				; CODE XREF: f5_draw+49Fj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+71Ah], 40h ; '@'
		jb	short loc_1BA84
		mov	al, [si+2C00h]
		cbw
		add	dx, ax

loc_1BA84:				; CODE XREF: f5_draw+4B3j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+76Ah], 40h ; '@'
		jb	short loc_1BA98
		mov	al, [si+2E00h]
		cbw
		add	dx, ax

loc_1BA98:				; CODE XREF: f5_draw+4C7j
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+7BAh], 40h ; '@'
		jb	short loc_1BAAC
		mov	al, [si+3000h]
		cbw
		add	dx, ax

loc_1BAAC:				; CODE XREF: f5_draw+4DBj
		dec	cx
		jz	loc_1BB2F
		cmp	[byte ptr fs:bx+80Ah], 40h ; '@'
		jb	short loc_1BAC0
		mov	al, [si+3200h]
		cbw
		add	dx, ax

loc_1BAC0:				; CODE XREF: f5_draw+4EFj
		dec	cx
		jz	short loc_1BB2F
		cmp	[byte ptr fs:bx+85Ah], 40h ; '@'
		jb	short loc_1BAD2
		mov	al, [si+3400h]
		cbw
		add	dx, ax

loc_1BAD2:				; CODE XREF: f5_draw+501j
		dec	cx
		jz	short loc_1BB2F
		cmp	[byte ptr fs:bx+8AAh], 40h ; '@'
		jb	short loc_1BAE4
		mov	al, [si+3600h]
		cbw
		add	dx, ax

loc_1BAE4:				; CODE XREF: f5_draw+513j
		dec	cx
		jz	short loc_1BB2F
		cmp	[byte ptr fs:bx+8FAh], 40h ; '@'
		jb	short loc_1BAF6
		mov	al, [si+3800h]
		cbw
		add	dx, ax

loc_1BAF6:				; CODE XREF: f5_draw+525j
		dec	cx
		jz	short loc_1BB2F
		cmp	[byte ptr fs:bx+94Ah], 40h ; '@'
		jb	short loc_1BB08
		mov	al, [si+3A00h]
		cbw
		add	dx, ax

loc_1BB08:				; CODE XREF: f5_draw+537j
		dec	cx
		jz	short loc_1BB2F
		cmp	[byte ptr fs:bx+99Ah], 40h ; '@'
		jb	short loc_1BB1A
		mov	al, [si+3C00h]
		cbw
		add	dx, ax

loc_1BB1A:				; CODE XREF: f5_draw+549j
		dec	cx
		jz	short loc_1BB2F
		cmp	[byte ptr fs:bx+9EAh], 40h ; '@'
		jb	short loc_1BB2C
		mov	al, [si+3E00h]
		cbw
		add	dx, ax

loc_1BB2C:				; CODE XREF: f5_draw+55Bj
		dec	cx
		jz	short $+2

loc_1BB2F:				; CODE XREF: f5_draw+305j f5_draw+319j ...
		sar	dx, 1
		mov	[di], dl
		inc	si
		inc	di
		cmp	si, offset byte_1E0E0
		jb	loc_1B8BC
		mov	si, offset byte_24204
		mov	di, offset byte_22EE4
		mov	cx, 200h

loc_1BB46:				; CODE XREF: f5_draw+595j
		movsx	eax, [byte ptr si]
		shl	eax, 10h
		mov	[di], eax
		mov	[dword ptr di+4], 0
		inc	si
		add	di, 8
		loop	loc_1BB46
		mov	ax, [word_24524]
		mov	[word_24520], ax
		mov	[word_24514], ax
		mov	di, offset byte_22EE4
		call	sub_1B406
		mov	si, offset byte_22EE4
		mov	di, offset unk_24074
		mov	cx, 64h	; 'd'
		call	sub_1BBC1
		mov	ax, 0A000h
		mov	es, ax
		assume es:nothing
		mov	bx, offset unk_23EE4
		mov	bp, 7BC4h
		call	sub_1BCE9
		mov	bx, offset byte_23EE5
		mov	bp, 7BD6h
		call	sub_1BC2D
		mov	bx, offset unk_24074
		mov	bp, 0F8C4h
		call	sub_1BCE9
		mov	bx, offset byte_24075
		mov	bp, 0F8D6h
		call	sub_1BC2D
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		mov	si, offset unk_23EE4
		mov	di, offset byte_23F48
		mov	cx, 19h
		cld
		rep movsd
		mov	si, offset unk_24074
		mov	di, offset byte_240D8
		mov	cx, 19h
		rep movsd
		retn
endp		f5_draw


; =============== S U B	R O U T	I N E =======================================


proc		sub_1BBC1 near		; CODE XREF: f5_draw+2DFp f5_draw+5AFp ...
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
		call	sub_1C4F8
		or	ah, ah
		jz	short loc_1BBF4
		mov	al, 0FFh

loc_1BBF4:				; CODE XREF: sub_1BBC1+2Fj
		cmp	[byte_1DE82], 0
		jz	short loc_1BC0C
		mov	ah, [di+64h]
		sub	ah, [byte_1DE82]
		jnb	short loc_1BC06
		xor	ah, ah

loc_1BC06:				; CODE XREF: sub_1BBC1+41j
		cmp	ah, al
		jb	short loc_1BC0C
		mov	al, ah

loc_1BC0C:				; CODE XREF: sub_1BBC1+38j
					; sub_1BBC1+47j
		mov	[di], al
		cmp	[byte ptr di+12Ch], 0
		jz	short loc_1BC1B
		cmp	al, [di+0C8h]
		jb	short loc_1BC24

loc_1BC1B:				; CODE XREF: sub_1BBC1+52j
		mov	[di+0C8h], al
		mov	[byte ptr di+12Ch], 14h

loc_1BC24:				; CODE XREF: sub_1BBC1+58j
		inc	di
		add	si, 8
		pop	cx
		dec	cx
		jnz	short sub_1BBC1
		retn
endp		sub_1BBC1


; =============== S U B	R O U T	I N E =======================================


proc		sub_1BC2D near		; CODE XREF: f5_draw+5C6p f5_draw+5D8p
		mov	cx, 63h	; 'c'

loc_1BC30:				; CODE XREF: sub_1BC2D+B7j
		mov	al, [bx]
		cmp	al, 5Ah	; 'Z'
		jb	short loc_1BC38
		mov	al, 5Ah	; 'Z'

loc_1BC38:				; CODE XREF: sub_1BC2D+7j
		mov	ah, [bx+64h]
		cmp	ah, 5Ah	; 'Z'
		jb	short loc_1BC42
		mov	ah, 5Ah	; 'Z'

loc_1BC42:				; CODE XREF: sub_1BC2D+11j
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

loc_1BC5F:				; CODE XREF: sub_1BC2D+3Fj
		mov	[es:di], ax
		inc	al
		inc	ah
		sub	di, 140h
		dec	dl
		jnz	short loc_1BC5F
		jmp	short loc_1BC92
; ---------------------------------------------------------------------------

loc_1BC70:				; CODE XREF: sub_1BC2D+19j
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

loc_1BC87:				; CODE XREF: sub_1BC2D+63j
		mov	[es:di], ax
		sub	di, 140h
		dec	dl
		jnz	short loc_1BC87

loc_1BC92:				; CODE XREF: sub_1BC2D+17j
					; sub_1BC2D+41j
		cmp	[byte ptr bx+12Ch], 0
		jz	short loc_1BCDF
		dec	[byte ptr bx+12Ch]
		jnz	short loc_1BCC0
		movzx	dx, [byte ptr bx+0C8h]
		cmp	dl, 5Ah	; 'Z'
		jb	short loc_1BCAB
		mov	dl, 5Ah	; 'Z'

loc_1BCAB:				; CODE XREF: sub_1BC2D+7Aj
		shl	dx, 6
		mov	di, dx
		shl	dx, 2
		add	di, dx
		neg	di

loc_1BCB7:
		add	di, bp
		mov	[word ptr es:di], 0
		jmp	short loc_1BCDF
; ---------------------------------------------------------------------------

loc_1BCC0:				; CODE XREF: sub_1BC2D+70j
		movzx	dx, [byte ptr bx+0C8h]
		cmp	dl, 5Ah	; 'Z'
		jb	short loc_1BCCC
		mov	dl, 5Ah	; 'Z'

loc_1BCCC:				; CODE XREF: sub_1BC2D+9Bj
		shl	dx, 6
		mov	di, dx
		shl	dx, 2
		add	di, dx
		neg	di
		add	di, bp
		mov	[word ptr es:di], 0FEFEh

loc_1BCDF:				; CODE XREF: sub_1BC2D+6Aj
					; sub_1BC2D+91j
		inc	bx
		add	bp, 3
		dec	cx
		jnz	loc_1BC30
		retn
endp		sub_1BC2D


; =============== S U B	R O U T	I N E =======================================


proc		sub_1BCE9 near		; CODE XREF: f5_draw+5BDp f5_draw+5CFp
		mov	al, [bx]
		cmp	al, 5Ah	; 'Z'
		jb	short loc_1BCF1
		mov	al, 5Ah	; 'Z'

loc_1BCF1:				; CODE XREF: sub_1BCE9+4j
		mov	ah, [bx+64h]
		cmp	ah, 5Ah	; 'Z'
		jb	short loc_1BCFB
		mov	ah, 5Ah	; 'Z'

loc_1BCFB:				; CODE XREF: sub_1BCE9+Ej
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

loc_1BD26:				; CODE XREF: sub_1BCE9+35j
					; sub_1BCE9+52j
		mov	[es:di], eax
		mov	[es:di+4], eax
		sub	di, 140h
		xor	eax, 1010101h
		dec	dl
		jnz	short loc_1BD26
		retn
; ---------------------------------------------------------------------------

loc_1BD3E:				; CODE XREF: sub_1BCE9+16j
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

loc_1BD56:				; CODE XREF: sub_1BCE9+7Cj
		mov	[es:di], eax
		mov	[es:di+4], eax
		sub	di, 140h
		dec	dl
		jnz	short loc_1BD56

locret_1BD67:				; CODE XREF: sub_1BCE9+14j
		retn
endp		sub_1BCE9

; ---------------------------------------------------------------------------

f6_draw:				; DATA XREF: f6_undoc+6o
		call	draw_text_bottom
		lfs	bx, [segfsbx_1DE28]
		les	di, [videomempointer]
		assume es:nothing
		add	di, 3C4h
		mov	cx, [word_1DE44]
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
		mov	si, offset buffer_1 ; 2800h
		mov	eax, 0C4C4C4C4h
		mov	[word ptr si], 2020h
		mov	[si+2],	eax
		mov	[si+6],	eax
		mov	[si+0Ah], eax
		mov	[si+0Eh], eax
		mov	[word ptr si+12h], 20C4h
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
		mov	[dword ptr si],	20202020h
		cld
		mov	al, [fs:bx+3Ah]
		sub	al, 40h	; '@'
		js	short loc_1BE07
		inc	si

loc_1BE07:				; CODE XREF: seg001:2DB4j
		cmp	al, 0F7h ; '÷'
		jl	short loc_1BE10
		cmp	al, 9
		jg	short loc_1BE10
		inc	si

loc_1BE10:				; CODE XREF: seg001:2DB9j seg001:2DBDj
		push	bx
		call	sub_1C55A
		pop	bx
		mov	[byte ptr si], 0
		mov	si, offset buffer_1 ; 2800h
		mov	ah, 7Eh	; '~'
		call	put_message
		pop	di
		pop	cx
		pop	ax
		add	di, 0A0h ; ' '
		add	bx, 50h	; 'P'
		inc	ax
		dec	cx
		jnz	loc_1BD88
		retn
; ---------------------------------------------------------------------------
		push	ax
		shr	al, 4
		call	sub_1BE39
		pop	ax

; =============== S U B	R O U T	I N E =======================================


proc		sub_1BE39 near		; CODE XREF: seg001:2DE5p
		and	al, 0Fh
		or	al, 30h
		cmp	al, 39h	; '9'
		jbe	short loc_1BE43
		add	al, 7

loc_1BE43:				; CODE XREF: sub_1BE39+6j
		mov	[es:di], ax
		add	di, 2
		retn
endp		sub_1BE39


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

proc		strange_1BE4A near
		mov	bp, sp
		xchg	si, [bp+0]
		les	di, [videomempointer]
		add	di, [cs:si]
		mov	ah, [cs:si+2]
		add	si, 3
		mov	cl, 70h	; 'p'
		xor	al, al

loc_1BE61:				; CODE XREF: strange_1BE4A+27j
		add	cl, al
		mov	al, [cs:si]
		inc	si
		xor	al, cl
		jz	short loc_1BE73
		mov	[es:di], ax
		add	di, 2
		jmp	short loc_1BE61
; ---------------------------------------------------------------------------

loc_1BE73:				; CODE XREF: strange_1BE4A+1Fj
		xchg	si, [bp+0]
		retn
endp		strange_1BE4A


; =============== S U B	R O U T	I N E =======================================


; int __usercall message_1BE77<eax>(char *msg<esi>)
proc		message_1BE77 near	; CODE XREF: start+2FDp start+420p ...
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
		mov	ah, 0A0h ; ' '
		mul	ah
		movzx	di, cl
		and	di, 0FFFEh
		add	ax, di
		add	ax, 0A4h ; '¤'
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
endp		message_1BE77


; =============== S U B	R O U T	I N E =======================================


proc		draw_frame near		; CODE XREF: start+1FEp start+278p ...
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
		add	si, offset frameborder ; "	ÛÛÛÛÛÛÉ»È¼ÍºÚ¿ÀÙÄ³Ö·Ó½ÄºÕ¸Ô¾Í³"
		mov	al, [si]
		cld
		stosw
		mov	cx, bp
		jcxz	short loc_1BF11
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
		jcxz	short loc_1BF31
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
		jcxz	short loc_1BF53
		mov	al, [si+4]
		rep stosw

loc_1BF53:				; CODE XREF: draw_frame+89j
		mov	al, [si+3]
		stosw

loc_1BF57:				; CODE XREF: draw_frame+1Dj
					; draw_frame+22j ...
		pop	es
		retn
endp		draw_frame


; =============== S U B	R O U T	I N E =======================================


; void __usercall write_scr(char *str<esi>)
proc		write_scr near		; CODE XREF: start+20Bp start+72Ap ...
		mov	bp, di
		add	di, [si]
		add	si, 2
		jmp	short n2_setcolor
endp		write_scr

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR text_1BF69

n1_movepos:				; CODE XREF: text_1BF69+9j
		mov	di, [si]
		add	di, bp
		add	si, 2
; END OF FUNCTION CHUNK	FOR text_1BF69

; =============== S U B	R O U T	I N E =======================================


; void __usercall text_1BF69(char *str<esi>)
proc		text_1BF69 near		; CODE XREF: filelist_198B8+102p
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
endp		text_1BF69 ; sp-analysis failed

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR put_message

loc_1BF86:				; CODE XREF: put_message+4j
		stosw
; END OF FUNCTION CHUNK	FOR put_message

; =============== S U B	R O U T	I N E =======================================


; void __usercall put_message(char *str<esi>, void *buf<edi>)
proc		put_message near	; CODE XREF: start+2A8p start+2EDp ...

; FUNCTION CHUNK AT 2F36 SIZE 00000001 BYTES

		cld
		lodsb
		or	al, al
		jnz	short loc_1BF86
		retn
endp		put_message ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


; void __usercall put_message2(char *str<esi>, void *buf<edi>)
proc		put_message2 near	; CODE XREF: put_message2+6j
		stosw
		cld
		lods	[byte ptr fs:si]
		or	al, al
		jnz	short put_message2
		retn
endp		put_message2


; =============== S U B	R O U T	I N E =======================================


proc		loadcfg	near		; CODE XREF: start:loc_190D3p
		mov	dx, offset sIplay_cfg ;	"C:\\IPLAY.CFG"
		mov	ax, 3D00h
		int	21h		; DOS -	2+ - OPEN DISK FILE WITH HANDLE
					; DS:DX	-> ASCIZ filename
					; AL = access mode
					; 0 - read
		jb	short loc_1BFE3
		mov	bx, ax
		mov	dx, offset cfg_buffer
		mov	cx, 4
		mov	ah, 3Fh	; '?'
		push	bx
		int	21h		; DOS -	2+ - READ FROM FILE WITH HANDLE
					; BX = file handle, CX = number	of bytes to read
					; DS:DX	-> buffer
		pop	bx
		jb	short loc_1BFC9
		mov	eax, [dword_1DCEC]
		cmp	eax, [dword ptr	cfg_buffer]
		stc
		jnz	short loc_1BFC9
		mov	dx, offset snd_card_type
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
		mov	si, offset snd_card_type
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
		assume ds:seg001
		mov	dx, offset aConfigFileNotF ; "Config file not found. Run ISETUP	first"...
		mov	ah, 9
		int	21h		; DOS -	PRINT STRING
					; DS:DX	-> string terminated by	"$"
		mov	ax, 4C01h
		int	21h		; DOS -	2+ - QUIT WITH EXIT CODE (EXIT)
endp		loadcfg			; AL = exit code

; ---------------------------------------------------------------------------
aConfigFileNotF	db 'Config file not found. Run ISETUP first',0Dh,0Ah,'$'
					; DATA XREF: loadcfg+50o
		db 0Dh,0Ah,'$'
		assume ds:dseg

; =============== S U B	R O U T	I N E =======================================


; char *__usercall getexename<esi>()
proc		getexename near		; CODE XREF: init_vga_equalizr+2Fp
		mov	es, [esseg_atstart]
		mov	es, [word ptr es:2Ch]
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
		jcxz	short loc_1C050
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
endp		getexename


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C052 near
		mov	ah, al
		mov	dx, 3CEh
		mov	al, 5
		out	dx, al		; EGA: graph 1 and 2 addr reg:
					; mode register.Data bits:
					; 0-1: Write mode 0-2
					; 2: test condition
					; 3: read mode:	1=color	compare, 0=direct
					; 4: 1=use odd/even RAM	addressing
					; 5: 1=use CGA mid-res map (2-bits/pixel)
		inc	dl
		in	al, dx		; EGA port: graphics controller	data register
		and	al, 0FCh
		or	al, ah
		out	dx, al		; EGA port: graphics controller	data register
		retn
endp		sub_1C052


; =============== S U B	R O U T	I N E =======================================


proc		set_egavga near		; CODE XREF: init_vga_equalizr+91p
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
		or	al, 20h
		out	dx, al		; EGA port: sequencer data register
		retn
endp		set_egavga


; =============== S U B	R O U T	I N E =======================================


proc		graph_1C070 near	; CODE XREF: init_vga_equalizr+12Cp
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
endp		graph_1C070

		assume ds:seg003

; =============== S U B	R O U T	I N E =======================================


proc		int9 far		; DATA XREF: start+133o
		cmp	[cs:byte_1C1B8], 1
		jz	loc_1C11F
		push	ax
		in	al, 60h		; 8042 keyboard	controller data	register
		cmp	al, 0E0h ; 'à'
		jz	l_escaped_scancode
		cmp	al, 0E1h ; 'á'
		jz	l_escaped_scancode
		mov	ah, [cs:prev_scan_code]
		or	ah, ah
		jz	short loc_1C0A5
		mov	[cs:prev_scan_code], 0

loc_1C0A5:				; CODE XREF: int9+20j
		cmp	al, 36h	; '6'
		jz	short l_rshift
		cmp	al, 0B6h ; '¶'
		jz	short l_rshiftup
		cmp	al, 2Ah	; '*'
		jz	short l_lshift
		cmp	al, 0AAh ; 'ª'
		jz	short l_lshiftup
		cmp	al, 1Dh
		jz	short l_ctrl
		cmp	al, 9Dh	; ''
		jz	short l_lctrlup
		cmp	al, 38h	; '8'
		jz	short l_alt
		cmp	al, 0B8h ; '¸'
		jz	short l_altup
		mov	[cs:key_code], ax

loc_1C0C9:				; CODE XREF: int9+62j int9+6Aj ...
		in	al, 61h		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÍËÍ OR	03H=spkr ON
					; 1: Tmr 2 data	Í¼  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		or	al, 80h
		out	61h, al		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÍËÍ OR	03H=spkr ON
					; 1: Tmr 2 data	Í¼  AND	0fcH=spkr OFF
					; 3: 1=read high switches
					; 4: 0=enable RAM parity checking
					; 5: 0=enable I/O channel check
					; 6: 0=hold keyboard clock low
					; 7: 0=enable kbrd
		and	al, 7Fh
		out	61h, al		; PC/XT	PPI port B bits:
					; 0: Tmr 2 gate	ÍËÍ OR	03H=spkr ON
					; 1: Tmr 2 data	Í¼  AND	0fcH=spkr OFF
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

l_rshift:				; CODE XREF: int9+2Aj
		or	[cs:keyb_switches], 1
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_rshiftup:				; CODE XREF: int9+2Ej
		and	[cs:keyb_switches], not	1
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_lshift:				; CODE XREF: int9+32j
		or	[cs:keyb_switches], 10b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_lshiftup:				; CODE XREF: int9+36j
		and	[cs:keyb_switches], not	10b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_ctrl:					; CODE XREF: int9+3Aj
		or	[cs:keyb_switches], 100b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_lctrlup:				; CODE XREF: int9+3Ej
		and	[cs:keyb_switches], not	100b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------
		assume ds:dseg

l_alt:					; CODE XREF: int9+42j
		or	[cs:keyb_switches], 1000b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_altup:				; CODE XREF: int9+46j
		and	[cs:keyb_switches], not	1000b
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

l_escaped_scancode:			; CODE XREF: int9+Fj int9+15j
		mov	[cs:prev_scan_code], al
		jmp	short loc_1C0C9
; ---------------------------------------------------------------------------

loc_1C11F:				; CODE XREF: int9+6j
		jmp	[cs:oint9_1C1A4]
endp		int9


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C124 near
		push	es
		xor	ax, ax
		mov	es, ax
		assume es:nothing
		mov	ax, [es:17h]
		mov	[cs:keyb_switches], ax
		pop	es
		assume es:nothing
		retn
endp		sub_1C124


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C133 near
		push	es
		xor	ax, ax
		mov	es, ax
		assume es:nothing
		mov	ax, [cs:keyb_switches]
		mov	[es:17h], ax
		pop	es
		assume es:nothing
		retn
endp		sub_1C133

; ---------------------------------------------------------------------------
; ---------------------------------------------------------------------------
key_code	dw 0			; DATA XREF: start:loc_193FFr
					; start+37Aw ...
keyb_switches	dw 0			; DATA XREF: start+5D8r sub_19EFD+1DEr ...
prev_scan_code	db 0			; DATA XREF: int9+19r int9+22w ...

; =============== S U B	R O U T	I N E =======================================


proc		int24 far		; DATA XREF: start+13Bo
		mov	al, 3
		test	ah, 8
		jnz	short locret_1C159
		mov	al, 0
		test	ah, 20h
		jnz	short locret_1C159
		mov	al, 1

locret_1C159:				; CODE XREF: int24+5j int24+Cj
		iret
endp		int24


; =============== S U B	R O U T	I N E =======================================


proc		int2f far		; DATA XREF: start+143o
		pushf
		cmp	ax, 60FFh
		jz	short lyesitsme	; DS

loc_1C160:				; CODE XREF: int2f+10j	int2f+16j
		popf
		jmp	[cs:oint2f_1C1B4]
; ---------------------------------------------------------------------------

lyesitsme:				; CODE XREF: int2f+4j
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

loc_1C17C:				; CODE XREF: int2f+1Cj
		push	ax
		push	ds
		mov	ax, dseg
		mov	ds, ax
		mov	[byte_1DE7C], 1
		pop	ds
		pop	ax
		iret
endp		int2f


; =============== S U B	R O U T	I N E =======================================


proc		int1a near		; DATA XREF: sub_1C1B9+47o
		pushf
		or	ah, ah
		jnz	short loc_1C19C
		pushad
		push	ds
		push	es
		call	rereadrtc_set
		pop	es
		pop	ds
		popad

loc_1C19C:				; CODE XREF: int1a+3j
		popf
		jmp	[cs:int1Avect]
endp		int1a

; ---------------------------------------------------------------------------
		db 87h,	0DBh
oint9_1C1A4	dd 0			; DATA XREF: start+106w start+1E0r ...
int1Avect	dd 0			; DATA XREF: int1a+12r	sub_1C1B9+38w ...
oint24_1C1AC	dd 0			; DATA XREF: start+115w start+1D4r ...
		db 4 dup(0)
oint2f_1C1B4	dd 0			; DATA XREF: start+124w start+1C8r ...
byte_1C1B8	db 0			; DATA XREF: int9r sub_1C1B9+58w ...

; =============== S U B	R O U T	I N E =======================================


proc		sub_1C1B9 near		; CODE XREF: start+747p sub_19EFD+338p
		mov	ax, 3
		int	10h		; - VIDEO - SET	VIDEO MODE
					; AL = mode
		call	enableblink
		mov	cx, 0
		mov	dx, 94Fh
		mov	bl, 78h	; 'x'
		mov	ax, 7F03h
		call	draw_frame
		call	sub_1A75D
		mov	si, offset byte_1D26D ;	str
		les	di, [videomempointer]
		call	write_scr
		mov	dx, 0A00h
		xor	bh, bh
		mov	ah, 2
		int	10h		; - VIDEO - SET	CURSOR POSITION
					; DH,DL	= row, column (0,0 = upper left)
					; BH = page number
		test	[byte_1DE78], 2
		jz	short loc_1C209
		mov	ax, 351Ah
		int	21h		; DOS -	2+ - GET INTERRUPT VECTOR
					; AL = interrupt number
					; Return: ES:BX	= value	of interrupt vector
		mov	[word ptr cs:int1Avect], bx
		mov	[word ptr cs:int1Avect+2], es
		push	ds
		mov	ax, cs
		mov	ds, ax
		assume ds:seg001
		mov	dx, offset int1a
		mov	ax, 251Ah
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds
		assume ds:dseg

loc_1C209:				; CODE XREF: sub_1C1B9+31j
		mov	si, offset byte_1DD3F
		call	sub_1988C
		mov	al, 1
		mov	[cs:byte_1C1B8], al
		call	sub_12D35
		mov	es, [esseg_atstart]
		mov	ax, [es:2Ch]
		mov	[word_24445], ax
		call	sub_1C268
		jb	short loc_1C23E
		mov	dx, di
		push	ds
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		mov	bx, offset word_24445
		mov	ds, [word_24445]
		mov	ax, 4B00h
		int	21h		; DOS -	2+ - LOAD OR EXECUTE (EXEC)
					; DS:DX	-> ASCIZ filename
					; ES:BX	-> parameter block
					; AL = subfunc:	load & execute program
		pop	ds

loc_1C23E:				; CODE XREF: sub_1C1B9+6Fj
		mov	al, 0
		mov	[cs:byte_1C1B8], al
		call	sub_12D35
		test	[byte_1DE78], 2
		jz	short loc_1C25C
		push	ds
		lds	dx, [cs:int1Avect]
		mov	ax, 251Ah
		int	21h		; DOS -	SET INTERRUPT VECTOR
					; AL = interrupt number
					; DS:DX	= new vector to	be used	for specified interrupt
		pop	ds

loc_1C25C:				; CODE XREF: sub_1C1B9+95j
		mov	si, offset byte_1DD3F ;	str
		call	doschdir
		mov	[byte_1DE70], 0FFh
		retn
endp		sub_1C1B9


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C268 near		; CODE XREF: sub_1C1B9+6Cp
		mov	es, [esseg_atstart]
		assume es:nothing
		mov	es, [word ptr es:2Ch]
		xor	di, di

loc_1C273:				; CODE XREF: sub_1C268+2Fj
		cmp	[byte ptr es:di], 0
		stc
		jz	short locret_1C29D
		cmp	[dword ptr es:di], 534D4F43h ; COMSPEC=
		jnz	short loc_1C28F
		cmp	[dword ptr es:di+4], 3D434550h
		jz	short loc_1C299

loc_1C28F:				; CODE XREF: sub_1C268+1Aj
					; sub_1C268+2Cj
		inc	di
		cmp	[byte ptr es:di], 0
		jnz	short loc_1C28F
		inc	di
		jmp	short loc_1C273
; ---------------------------------------------------------------------------

loc_1C299:				; CODE XREF: sub_1C268+25j
		add	di, 8
		clc

locret_1C29D:				; CODE XREF: sub_1C268+10j
		retn
endp		sub_1C268


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C29E near		; CODE XREF: start+1A1p
					; modules_search+65p ...
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		mov	di, offset byte_1DB6C
		mov	si, di
		mov	cx, 120
		xor	al, al
		cld
		repne scasb
		jnz	short loc_1C321
		dec	di
		mov	[word_1DE4A], di

loc_1C2B6:				; CODE XREF: sub_1C29E+2Aj
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

loc_1C2CA:				; CODE XREF: sub_1C29E+1Dj
					; sub_1C29E+21j ...
		sub	di, si
		mov	[word_1DE4C], di
		mov	dx, offset byte_1DBEC
		mov	ah, 1Ah
		int	21h		; DOS -	SET DISK TRANSFER AREA ADDRESS
					; DS:DX	-> disk	transfer buffer
		mov	dx, offset byte_1DB6C
		mov	cx, [word_1DE4E]
		mov	ah, 4Eh
		int	21h		; DOS -	2+ - FIND FIRST	ASCIZ (FINDFIRST)
					; CX = search attributes
					; DS:DX	-> ASCIZ filespec
					; (drive, path,	and wildcards allowed)
		jnb	short loc_1C309
		mov	si, offset a_mod_nst_669_s ; ".MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FA"...

loc_1C2E7:				; CODE XREF: sub_1C29E+69j
		cmp	[byte ptr si], 0
		jz	short loc_1C321
		mov	di, [word_1DE4A]
		mov	eax, [si]
		mov	[di], eax
		mov	[byte ptr di+4], 0
		add	si, 4
		mov	dx, offset byte_1DB6C
		mov	cx, 2
		mov	ah, 4Eh
		int	21h		; DOS -	2+ - FIND FIRST	ASCIZ (FINDFIRST)
					; CX = search attributes
					; DS:DX	-> ASCIZ filespec
					; (drive, path,	and wildcards allowed)
		jb	short loc_1C2E7

loc_1C309:				; CODE XREF: sub_1C29E+44j
					; sub_1C332+Bj
		mov	ax, ds
		mov	es, ax
		mov	si, offset byte_1DC0A
		mov	di, offset byte_1DB6C
		add	di, [word_1DE4C]
		cld
		mov	cx, 3
		rep movsd
		movsb
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C321:				; CODE XREF: sub_1C29E+11j
					; sub_1C29E+4Cj
		mov	[byte_1DE7E], 2
		mov	[word ptr messagepointer], offset aModuleNotFound ; "Module not	found.\r\n$"
		mov	[word ptr messagepointer+2], ds
		stc
		retn
endp		sub_1C29E


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C332 near		; CODE XREF: modules_search+CBp
					; modules_search+247p ...
		mov	dx, offset byte_1DBEC
		mov	ah, 1Ah
		int	21h		; DOS -	SET DISK TRANSFER AREA ADDRESS
					; DS:DX	-> disk	transfer buffer
		mov	ah, 4Fh
		int	21h		; DOS -	2+ - FIND NEXT ASCIZ (FINDNEXT)
					; [DTA]	= data block from
					; last AH = 4Eh/4Fh call
		jnb	short loc_1C309
		retn
endp		sub_1C332


; =============== S U B	R O U T	I N E =======================================


proc		video_1C340 near	; CODE XREF: sub_19E11+C5p
					; init_vga_equalizr+14Cp ...
		pushf
		cli
		mov	[byte_1DE79], 0
		mov	[byte_1DE7A], 0
		lfs	bx, [segfsbx_1DE28]
		mov	cx, [word_1DE44]

loc_1C355:				; CODE XREF: video_1C340+2Dj
		mov	al, [fs:bx+3Ah]
		cmp	al, 40h	; '@'
		jb	short loc_1C365
		inc	[byte_1DE7A]
		cmp	al, 40h	; '@'
		ja	short loc_1C369

loc_1C365:				; CODE XREF: video_1C340+1Bj
		inc	[byte_1DE79]

loc_1C369:				; CODE XREF: video_1C340+23j
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_1C355
		movzx	ecx, [byte_1DE79]
		cmp	cl, [byte_1DE7A]
		ja	short loc_1C37F
		mov	cl, [byte_1DE7A]

loc_1C37F:				; CODE XREF: video_1C340+39j
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

loc_1C396:				; CODE XREF: video_1C340+44j
					; video_1C340+4Bj ...
		add	al, 8
		mov	[byte_1DE81], al
		xor	edx, edx
		mov	eax, 18350080
		jcxz	short loc_1C3A9
		div	ecx

loc_1C3A9:				; CODE XREF: video_1C340+64j
		mov	ebp, eax
		mov	si, offset byte_1DE9C
		mov	cx, [word_1DE44]
		lfs	bx, [segfsbx_1DE28]
		mov	edi, ebp
		shr	edi, 1
		mov	edx, edi

loc_1C3C1:				; CODE XREF: video_1C340+B5j
		cmp	[byte ptr fs:bx+3Ah], 40h ; '@'
		jz	short loc_1C3EE
		ja	short loc_1C3DC
		mov	eax, edi
		shr	eax, 10h
		imul	ax, 80
		add	ax, 1
		add	edi, ebp
		jmp	short loc_1C3EC
; ---------------------------------------------------------------------------

loc_1C3DC:				; CODE XREF: video_1C340+88j
		mov	eax, edx
		shr	eax, 10h
		imul	ax, 80
		add	ax, 2Ah	; '*'
		add	edx, ebp

loc_1C3EC:				; CODE XREF: video_1C340+9Aj
		mov	[si], ax

loc_1C3EE:				; CODE XREF: video_1C340+86j
		add	si, 2
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_1C3C1
		mov	si, offset byte_1DE9C
		mov	cx, [word_1DE44]
		lfs	bx, [segfsbx_1DE28]
		cmp	edi, edx
		ja	short loc_1C40B
		mov	edi, edx

loc_1C40B:				; CODE XREF: video_1C340+C6j
					; video_1C340+EBj
		cmp	[byte ptr fs:bx+3Ah], 40h ; '@'
		jnz	short loc_1C424
		mov	eax, edi
		shr	eax, 16
		imul	ax, 80
		add	ax, 21
		add	edi, ebp
		mov	[si], ax

loc_1C424:				; CODE XREF: video_1C340+D0j
		add	si, 2
		add	bx, 50h	; 'P'
		dec	cx
		jnz	short loc_1C40B
		popf
		retn
endp		video_1C340


; =============== S U B	R O U T	I N E =======================================


proc		callsubx near		; CODE XREF: start:loc_19050p
					; start+1A6p ...
		mov	al, [snd_card_type]
		mov	dx, [word_1DCF2]
		mov	cl, [byte_1DCF4]
		mov	ch, [byte_1DCF5]
		mov	ah, [byte_1DCF6]
		movzx	di, [byte_1DCFB]
		mov	si, [configword]
		mov	bl, [byte_1DCF7]
		mov	bh, [byte_1DCF8]
		call	sub_12DA8
		mov	[byte_1DE7E], 1
		mov	[word ptr messagepointer], dx
		mov	[word ptr messagepointer+2], fs
		jb	short locret_1C4A7
		mov	[byte_1DE7E], 0
		call	sub_12CCF
		mov	[snd_card_type], al
		mov	[word_1DCF2], dx
		mov	[byte_1DCF4], cl
		mov	[byte_1DCF5], ch
		mov	[byte_1DCF6], ah
		mov	[byte_1DCF7], bl
		mov	[byte_1DCF8], bh
		mov	[configword], si
		mov	[outp_freq], bp
		mov	[byte_1DE7C], 1
		cmp	[snd_card_type], 0
		jnz	short loc_1C4A6
		mov	[byte ptr cs:loc_1AA73+4], 0Fh

loc_1C4A6:				; CODE XREF: callsubx+6Fj
		clc

locret_1C4A7:				; CODE XREF: callsubx+36j
		retn
endp		callsubx


; =============== S U B	R O U T	I N E =======================================


proc		rereadrtc_set near	; CODE XREF: int1a+9p
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
endp		rereadrtc_set


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C4F8 near		; CODE XREF: sub_1BBC1+2Ap
		xor	eax, eax
		mov	edx, 40000000h

loc_1C501:				; CODE XREF: sub_1C4F8+21j
		mov	ecx, eax
		add	ecx, edx
		shr	eax, 1
		cmp	ecx, ebx
		jg	short loc_1C515
		sub	ebx, ecx
		add	eax, edx

loc_1C515:				; CODE XREF: sub_1C4F8+15j
		shr	edx, 2
		jnz	short loc_1C501
		cmp	eax, ebx
		jge	short locret_1C521
		inc	ax

locret_1C521:				; CODE XREF: sub_1C4F8+26j
		retn
endp		sub_1C4F8


; =============== S U B	R O U T	I N E =======================================


proc		blinkingoff near	; CODE XREF: setvideomode+1Cp
					; text_init2+11Dp
		xor	bl, bl
		mov	ax, 1003h
		int	10h		; - VIDEO - TOGGLE INTENSITY/BLINKING BIT (Jr, PS, TANDY 1000, EGA, VGA)
					; BL = 00h enable background intensity
					; = 01h	enable blink
		retn
endp		blinkingoff


; =============== S U B	R O U T	I N E =======================================


proc		enableblink near	; CODE XREF: start+1F0p sub_1C1B9+5p
		mov	bl, 1
		mov	ax, 1003h
		int	10h		; - VIDEO - TOGGLE INTENSITY/BLINKING BIT (Jr, PS, TANDY 1000, EGA, VGA)
					; BL = 00h enable background intensity
					; = 01h	enable blink
		retn
endp		enableblink


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C532 near		; CODE XREF: seg001:364Bp
		ror	eax, 10h
		call	sub_1C53D
		ror	eax, 10h
endp		sub_1C532 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C53D near		; CODE XREF: sub_1C532+4p seg001:3637p
		xchg	al, ah
		call	sub_1C544
		mov	al, ah
endp		sub_1C53D ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C544 near		; CODE XREF: sub_1C53D+2p seg001:3624p
		push	ax
		shr	al, 4
		call	sub_1C54C
		pop	ax
endp		sub_1C544 ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C54C near		; CODE XREF: sub_1C544+4p
		and	al, 0Fh
		or	al, '0'
		cmp	al, '9'
		jbe	short loc_1C556
		add	al, 7

loc_1C556:				; CODE XREF: sub_1C54C+6j
		mov	[si], al
		inc	si
		retn
endp		sub_1C54C


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C55A near		; CODE XREF: seg001:2DC1p seg001:35EAp
		cbw

loc_1C55B:				; CODE XREF: seg001:35FDp
		cwde

loc_1C55D:				; CODE XREF: seg001:3611p
		xor	cx, cx
		or	eax, eax
		jns	short loc_1C576
		mov	dl, 2Dh	; '-'
		call	sub_1C591
		neg	eax
		jmp	short loc_1C576
endp		sub_1C55A


; =============== S U B	R O U T	I N E =======================================


proc		my_i8toa near		; CODE XREF: text_init2:loc_1A6A1p
					; text_init2+239p ...
		xor	ah, ah
endp		my_i8toa


; =============== S U B	R O U T	I N E =======================================


proc		my_i16toa near		; CODE XREF: text_init2+28Fp
					; draw_text_bottom+13Ep ...
		movzx	eax, ax
endp		my_i16toa ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		my_i32toa near		; CODE XREF: sub_1ACFD+6p seg001:35D8p
		xor	cx, cx

loc_1C576:				; CODE XREF: sub_1C55A+8j
					; sub_1C55A+12j
		mov	ebx, 10
endp		my_i32toa ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C57C near		; CODE XREF: sub_1C57C+Dp
		xor	edx, edx
		div	ebx
		or	eax, eax
		jz	short loc_1C58E
		push	edx
		call	sub_1C57C
		pop	edx

loc_1C58E:				; CODE XREF: sub_1C57C+9j
		or	dl, '0'
endp		sub_1C57C ; sp-analysis	failed


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C591 near		; CODE XREF: sub_1C55A+Cp
		mov	[si], dl
		inc	si
		inc	cx
		retn
endp		sub_1C591

; ---------------------------------------------------------------------------
off_1C596	dw offset loc_1C5D1	; DATA XREF: sub_1C5B0+1Cr
		dw offset loc_1C5D3
		dw offset loc_1C5DF
		dw offset loc_1C5E7
		dw offset loc_1C5FC
		dw offset loc_1C60E
		dw offset loc_1C620
		dw offset loc_1C633
		dw offset loc_1C646
		dw offset loc_1C659
		dw offset loc_1C66D
		dw offset loc_1C680
		dw offset loc_1C693

; =============== S U B	R O U T	I N E =======================================


proc		sub_1C5B0 near
		push	es
		mov	ax, ds
		mov	es, ax
		assume es:dseg
		jmp	short loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C5B7:				; CODE XREF: sub_1C5B0+Fj
		mov	[di], al
		inc	di

loc_1C5BA:				; CODE XREF: sub_1C5B0+5j
					; sub_1C5B0+2Dj ...
		mov	al, [si]
		inc	si
		cmp	al, 20h	; ' '
		jnb	short loc_1C5B7
		cmp	al, 0Ch
		ja	short loc_1C5D1
		inc	si
		mov	bl, al
		xor	bh, bh
		shl	bx, 1
		jmp	[cs:off_1C596+bx]

loc_1C5D1:				; CODE XREF: sub_1C5B0+13j
					; DATA XREF: seg001:off_1C596o
		pop	es
		assume es:nothing
		retn
; ---------------------------------------------------------------------------

loc_1C5D3:				; CODE XREF: sub_1C5B0+1Cj
					; DATA XREF: seg001:3548o
		push	si
		mov	si, [si]
		call	sub_1C6B5
		pop	si
		add	si, 2
		jmp	short loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C5DF:				; CODE XREF: sub_1C5B0+1Cj
					; DATA XREF: seg001:354Ao
		mov	bx, [si]
		mov	bl, [bx]
		xor	bh, bh
		jmp	short loc_1C5EB
; ---------------------------------------------------------------------------

loc_1C5E7:				; CODE XREF: sub_1C5B0+1Cj
					; DATA XREF: seg001:354Co
		mov	bx, [si]
		mov	bx, [bx]

loc_1C5EB:				; CODE XREF: sub_1C5B0+35j
		push	si
		shl	bx, 1
		mov	si, [si+2]
		mov	si, [bx+si]
		call	sub_1C6B5
		pop	si
		add	si, 4
		jmp	short loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C5FC:				; CODE XREF: sub_1C5B0+1Cj
					; DATA XREF: seg001:354Eo
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	my_i8toa
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C60E:				; CODE XREF: sub_1C5B0+1Cj
					; DATA XREF: seg001:3550o
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	my_i16toa
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_1C5BA
endp		sub_1C5B0

; ---------------------------------------------------------------------------

loc_1C620:				; DATA XREF: seg001:3552o
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	my_i32toa
		mov	di, si
		pop	si
		add	si, 2
		jmp	short loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C633:				; DATA XREF: seg001:3554o
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	sub_1C55A
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C646:				; DATA XREF: seg001:3556o
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	loc_1C55B
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C659:				; DATA XREF: seg001:3558o
		push	si
		mov	si, [si]
		mov	eax, [si]
		mov	si, di
		call	loc_1C55D
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C66D:				; DATA XREF: seg001:355Ao
		push	si
		mov	si, [si]
		mov	al, [si]
		mov	si, di
		call	sub_1C544
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C680:				; DATA XREF: seg001:355Co
		push	si
		mov	si, [si]
		mov	ax, [si]
		mov	si, di
		call	sub_1C53D
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_1C5BA
; ---------------------------------------------------------------------------

loc_1C693:				; DATA XREF: seg001:355Eo
		push	si
		mov	si, [si]

loc_1C696:
		mov	eax, [si]
		mov	si, di
		call	sub_1C532
		mov	di, si
		pop	si
		add	si, 2
		jmp	loc_1C5BA

; =============== S U B	R O U T	I N E =======================================


proc		sub_1C6A7 near		; CODE XREF: start+2D6p
		mov	ax, 0FFFFh
		dec	si

loc_1C6AB:				; CODE XREF: sub_1C6A7+9j
		inc	ax
		inc	si
		cmp	[byte ptr si], 0
		jnz	short loc_1C6AB
		sub	si, ax
		retn
endp		sub_1C6A7


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C6B5 near		; CODE XREF: sub_1C5B0+26p
					; sub_1C5B0+43p
		xor	cx, cx
		jmp	short loc_1C6BE
; ---------------------------------------------------------------------------

loc_1C6B9:				; CODE XREF: sub_1C6B5+Ej
		mov	[es:di], al
		inc	si
		inc	di

loc_1C6BE:				; CODE XREF: sub_1C6B5+2j
		mov	al, [si]
		inc	cx
		or	al, al
		jnz	short loc_1C6B9
		retn
endp		sub_1C6B5


; =============== S U B	R O U T	I N E =======================================


proc		mouseinit near		; CODE XREF: start+16Dp start+74Ap
		mov	[byte_1DE92], 0
		xor	ax, ax
		mov	es, ax
		assume es:nothing
		cmp	[dword ptr es:0CCh], 0
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

loc_1C6EF:				; CODE XREF: mouseinit+1Aj
		mov	[mouse_exist_flag], 1
		push	es
		mov	ax, seg001
		mov	es, ax
		assume es:seg001
		mov	dx, offset loc_1C72C
		mov	cx, 1Fh
		mov	ax, 0Ch
		int	33h		; - MS MOUSE - DEFINE INTERRUPT	SUBROUTINE PARAMETERS
					; CX = call mask, ES:DX	-> FAR routine
		pop	es
		assume es:nothing
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C708:				; CODE XREF: mouseinit+10j
					; mouseinit+22j ...
		mov	[mouse_exist_flag], 0
		stc
		retn
endp		mouseinit


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C70F near		; CODE XREF: start:loc_19256p
					; start:loc_197D6p
		cmp	[mouse_exist_flag], 1
		jnz	short locret_1C72B
		mov	[mouse_exist_flag], 0
		mov	[byte_1DE92], 0
		xor	dx, dx
		mov	es, dx
		assume es:nothing
		mov	cx, dx
		mov	ax, 0Ch
		int	33h		; - MS MOUSE - DEFINE INTERRUPT	SUBROUTINE PARAMETERS
					; CX = call mask, ES:DX	-> FAR routine

locret_1C72B:				; CODE XREF: sub_1C70F+5j
		retn
endp		sub_1C70F

; ---------------------------------------------------------------------------

loc_1C72C:				; DATA XREF: mouseinit+34o
		push	ds
		push	dseg
		pop	ds
		mov	[mousecolumn], cx
		mov	[mouserow], dx
		mov	[byte_1DE90], bl
		pop	ds
		retf

; =============== S U B	R O U T	I N E =======================================


proc		mouse_1C73F near	; CODE XREF: start+332p
		cmp	[mouse_exist_flag], 1
		jnz	short locret_1C755
		cmp	[byte_1DE92], 1
		jz	short locret_1C755
		mov	[byte_1DE92], 1
		call	mouseshowcur

locret_1C755:				; CODE XREF: mouse_1C73F+5j
					; mouse_1C73F+Cj
		retn
endp		mouse_1C73F


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C756 near		; CODE XREF: start+376p
					; start:loc_19827p ...
		cmp	[mouse_exist_flag], 1
		jnz	short locret_1C76C
		cmp	[byte_1DE92], 0
		jz	short locret_1C76C
		mov	[byte_1DE92], 0
		call	mousehide

locret_1C76C:				; CODE XREF: sub_1C756+5j sub_1C756+Cj
		retn
endp		sub_1C756


; =============== S U B	R O U T	I N E =======================================


proc		getmousepos near
		cmp	[mouse_exist_flag], 1
		jnz	short loc_1C783
		mov	ax, 3
		int	33h		; - MS MOUSE - RETURN POSITION AND BUTTON STATUS
					; Return: BX = button status, CX = column, DX =	row
		mov	[mousecolumn], cx
		mov	[mouserow], dx
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C783:				; CODE XREF: getmousepos+5j
		xor	bx, bx
		xor	cx, cx
		xor	dx, dx
		stc
		retn
endp		getmousepos


; =============== S U B	R O U T	I N E =======================================


proc		mouseshowcur near	; CODE XREF: mouse_1C73F+13p
		cmp	[mouse_exist_flag], 1
		jnz	short loc_1C7A7
		mov	ax, 1
		int	33h		; - MS MOUSE - SHOW MOUSE CURSOR
					; SeeAlso: AX=0002h, INT 16/AX=FFFEh
		clc
		retn
endp		mouseshowcur


; =============== S U B	R O U T	I N E =======================================


proc		mousehide near		; CODE XREF: sub_1C756+13p
		cmp	[mouse_exist_flag], 1
		jnz	short loc_1C7A7
		mov	ax, 2
		int	33h		; - MS MOUSE - HIDE MOUSE CURSOR
					; SeeAlso: AX=0001h, INT 16/AX=FFFFh
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C7A7:				; CODE XREF: mouseshowcur+5j
					; mousehide+5j
		stc
		retn
endp		mousehide


; =============== S U B	R O U T	I N E =======================================


proc		sub_1C7A9 near		; CODE XREF: sub_1C7CF+10p
		cmp	cx, si
		jbe	short loc_1C7AF
		xchg	cx, si

loc_1C7AF:				; CODE XREF: sub_1C7A9+2j
		cmp	dx, di
		jbe	short loc_1C7B5
		xchg	dx, di

loc_1C7B5:				; CODE XREF: sub_1C7A9+8j
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

loc_1C7CA:				; CODE XREF: sub_1C7A9+Ej
					; sub_1C7A9+12j ...
		stc
		retn
endp		sub_1C7A9

; ---------------------------------------------------------------------------
; START	OF FUNCTION CHUNK FOR sub_1C7CF

loc_1C7CC:				; CODE XREF: sub_1C7CF+13j
		add	bx, 0Ah
; END OF FUNCTION CHUNK	FOR sub_1C7CF

; =============== S U B	R O U T	I N E =======================================


; void *__usercall sub_1C7CF<ebx>(struct struct_0 *mystr<ebx>)
proc		sub_1C7CF near		; CODE XREF: start+7ADp start+7C9p ...

; FUNCTION CHUNK AT 377C SIZE 00000003 BYTES

		mov	cx, [bx]
		cmp	cx, 0FFFFh
		jz	short loc_1C7E9
		mov	dx, [bx+2]
		mov	si, [bx+4]
		mov	di, [bx+6]
		call	sub_1C7A9
		jb	short loc_1C7CC
		mov	bx, [bx+8]
		clc
		retn
; ---------------------------------------------------------------------------

loc_1C7E9:				; CODE XREF: sub_1C7CF+5j
		stc
		retn
endp		sub_1C7CF ; sp-analysis	failed

; ---------------------------------------------------------------------------
		db 5 dup(0)
ends		seg001

; ===========================================================================

; Segment type:	Pure data
segment		dseg para public 'DATA' use16
		assume cs:dseg
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
off_1CA8E	dw offset f3_textmetter	; DATA XREF: start+182r
		dw offset f2_equal
		dw offset f5_graphspectr
		dw offset f4_patternnae
		dw offset f1_help
		dw offset f6_undoc
table_sndcrdname dw offset aGravisUltrasou ; DATA XREF:	text_init2+19Dr
					; "Gravis UltraSound"
		dw offset aProAudioSpectr ; "Pro Audio Spectrum	16"
		dw offset aWindowsSoundSy ; "Windows Sound System"
		dw offset aSoundBlaster16 ; "Sound Blaster 16/16ASP"
		dw offset aSoundBlasterPr ; "Sound Blaster Pro"
		dw offset aSoundBlaster	; "Sound Blaster"
		dw offset aCovox	; "Covox"
		dw offset aStereoOn1	; "Stereo-On-1"
		dw offset aAdlibSoundcard ; "Adlib SoundCard"
		dw offset aPcHonker	; "PC Honker"
		dw offset aGeneralMidi	; "General MIDI"
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
word_1CB6E	dw 152h			; DATA XREF: sub_1A75D+12o
InertiaPlayer	db 'Inertia Player V1.22 Assembly ',27h,'94 CD Edition by Sound Solutio'
		db 'ns'
		db    1
		db 0F4h	; ô
		db    1
aCopyrightC1994	db 'Copyright (c) 1994,1995 by Stefan Danes and Ramon van Gorkom',0
		db 2
		db  78h	; x
		db    1
		db 0AAh	; ª
		db    1
aShell130295211	db 'Shell: 13/02/95 21:15:58'
		db    1
		db  46h	; F
		db    1
aPlayer13029521	db 'Player: '
a130295211558	db '13/02/95 21:15:58',0 ; DATA XREF: sub_19E11+BEw
asc_1CC2A	db 0Ah,0		; DATA XREF: text_init2+21Fo
asc_1CC2C	db '                              ' ; DATA XREF: sub_19E11+A3o
		db    1
		db 0AAh	; ª
		db    0
		db    2
aFilename	db '~Filename      : '
		db    2
aFilename_ext	db 'FileName.Ext'      ; DATA XREF: sub_19E11:loc_19E41o
		db    1
		db  4Ah	; J
		db    1
		db    2
aModuleType	db '~Module Type   : '
		db    2
		db  7Fh	; 
asc_1CC85	db '    '               ; DATA XREF: sub_19E11+6Fw
		db    2
		db  7Eh	; ~
		db    1
		db 0EAh	; ê
		db    1
aChannels	db 'Channels      :'
		db    1
		db  8Ah	; Š
		db    2
aSamplesUsed	db 'Samples Used  :'
		db    1
		db  2Ah	; *
		db    3
aCurrentTrack	db 'Current Track :'
		db    1
		db 0CAh	; Ê
		db    3
aTrackPosition	db 'Track Position:'
		db    1
		db  6Ah	; j
		db    4
aSpeed		db 'Speed'
		db    1
		db  86h	; †
		db    4
		db  3Ah	; :
		db    2
		db  78h	; x
		db    1
		db 0A4h	; ¤
		db    4
aTab		db 'Tab'
		db    1
		db 0F8h	; ø
		db    0
		db    2
byte_1CCEB	db 78h			; DATA XREF: text_init2:loc_1A6C2w
		db 0FEh	; þ
		db    2
aPlayingInStere	db '~ Playing in Stereo, Free:'
		db    1
		db  98h	; ˜
		db    1
		db    2
		db  78h	; x
		db 0FEh	; þ
		db    2
aProtracker1_0	db '~ ProTracker 1.0'
		db    1
		db 0CEh	; Î
		db    1
		db    2
aXf9		db 'xF-9'
		db    1
		db  38h	; 8
		db    2
		db    2
		db  78h	; x
		db 0FEh	; þ
		db    2
aIgnoreBpmChang	db '~ Ignore BPM changes'
		db    1
		db  6Eh	; n
		db    2
		db    2
aXf10		db 'xF-10'
		db    2
		db  7Eh	; ~
		db    1
		db 0D8h	; Ø
		db    2
		db    2
		db  78h	; x
		db 0FEh	; þ
		db    2
aLoopModuleWhen	db '~ Loop Module when done'
		db    1
		db  0Eh
		db    3
		db    2
aXf11		db 'xF-11'
		db    2
		db '~'
		db    1
		db  78h	; x
		db    3
		db    2
		db 78h
		db 0FEh	; þ
		db    2
a24bitInterpola	db '~ 24bit Interpolation'
		db    1
		db 0AEh	; ®
		db    3
		db    2
aXf12		db 'xF-12'
		db    2
		db  7Eh	; ~
		db    1
		db  18h
		db    4
aMainVolume	db 'Main Volume   :'
		db    1
		db  4Eh	; N
		db    4
		db    2
		db  78h	; x
		db  2Dh	; -
		db  20h
		db  2Bh	; +
		db    2
		db  7Eh	; ~
		db    1
		db 0B8h	; ¸
		db    4
aVolumeAmplify	db 'Volume Amplify:'
		db    1
		db 0EEh	; î
		db    4
		db    2
		db  78h	; x
		db  5Bh	; [
		db  20h
		db  5Dh	; ]
		db    0
f1_help_text	dw 3F8h			; DATA XREF: seg001:1CD8o
aSoYouWantedSom	db 7Fh
aSoYouWantedSomeHelp db	'So you wanted some help?'
		db    1
		dw 468h
		db    2
aF2		db 7Fh
aF2_0		db 'F-2'
		db    2
aGraphicalScope	db 7Eh
aGraphicalScopesOneF db	'  Graphical scopes, one for each channel'
		db    1
		dw 508h
		db    2
aF3		db 7Fh
aF3_0		db 'F-3'
		db    2
aRealtimeVuMete	db 7Eh
aRealtimeVuMeters db '  Realtime VU meters'
		db    1
		dw 5A8h
		db    2
aF4		db 7Fh
aF4_0		db 'F-4'
		db    2
aViewSampleName	db 7Eh
aViewSampleNamesTwic db	'  View sample names (twice for more)'
		db    1
		dw 648h
		db    2
aF5		db 7Fh
aF5_0		db 'F-5'
		db    2
aFastfourierFre	db 7Eh
aFastfourierFrequenc db	'  FastFourier Frequency Analysis'
		db    1
		dw 6E8h
		db    2
aF8		db 7Fh
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
hopeyoulike	db 'Æ'                  ; DATA XREF: start+204o
		db    3
		db  7Eh	; ~
		db  48h	; H
		db  6Fh	; o
		db  70h	; p
		db  65h	; e
		db  20h
		db  79h	; y
		db  6Fh	; o
		db  75h	; u
		db  20h
		db  6Ch	; l
		db  69h	; i
		db  6Bh	; k
		db  65h	; e
		db  64h	; d
		db  20h
		db  75h	; u
		db  73h	; s
		db  69h	; i
		db  6Eh	; n
		db  67h	; g
		db  20h
		db  74h	; t
		db  68h	; h
		db  65h	; e
		db  20h
		db    2
		db  7Fh	; 
		db  49h	; I
		db  6Eh	; n
		db  65h	; e
		db  72h	; r
		db  74h	; t
		db  69h	; i
		db  61h	; a
		db  20h
		db  50h	; P
		db  6Ch	; l
		db  61h	; a
		db  79h	; y
		db  65h	; e
		db  72h	; r
		db    2
		db  7Eh	; ~
		db  20h
		db  77h	; w
		db  68h	; h
		db  69h	; i
		db  63h	; c
		db  68h	; h
		db  20h
		db  69h	; i
		db  73h	; s
		db  20h
		db  77h	; w
		db  72h	; r
		db  69h	; i
		db  74h	; t
		db  74h	; t
		db  65h	; e
		db  6Eh	; n
		db  20h
		db  69h	; i
		db  6Eh	; n
		db  20h
		db    2
		db  7Fh	; 
		db  31h	; 1
		db  30h	; 0
		db  30h	; 0
		db  25h	; %
		db  20h
		db  61h	; a
		db  73h	; s
		db  73h	; s
		db  65h	; e
		db  6Dh	; m
		db  62h	; b
		db  6Ch	; l
		db  65h	; e
		db  72h	; r
		db  21h	; !
		db    2
		db  7Eh	; ~
		db    1
		db  0Ch
		db    5
		db  49h	; I
		db  66h	; f
		db  20h
		db  79h	; y
		db  6Fh	; o
		db  75h	; u
		db  20h
		db  68h	; h
		db  61h	; a
		db  76h	; v
		db  65h	; e
		db  20h
		db  62h	; b
		db  75h	; u
		db  67h	; g
		db  2Dh	; -
		db  72h	; r
		db  65h	; e
		db  70h	; p
		db  6Fh	; o
		db  72h	; r
		db  74h	; t
		db  73h	; s
		db  2Ch	; ,
		db  20h
		db  73h	; s
		db  75h	; u
		db  67h	; g
		db  67h	; g
unk_1D0C6	db  65h	; e
		db  73h	; s
		db  74h	; t
		db  69h	; i
		db  6Fh	; o
		db  6Eh	; n
		db  73h	; s
		db  20h
		db  6Fh	; o
		db  72h	; r
		db  20h
		db  63h	; c
		db  6Fh	; o
		db  6Dh	; m
		db  6Dh	; m
		db  65h	; e
		db  6Eh	; n
		db  74h	; t
		db  73h	; s
		db  20h
		db  73h	; s
		db  65h	; e
		db  6Eh	; n
		db  64h	; d
		db  20h
		db  61h	; a
unk_1D0E0	db  20h
		db  6Dh	; m
		db  65h	; e
		db  73h	; s
		db  73h	; s
		db  61h	; a
		db  67h	; g
		db  65h	; e
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  3Ah	; :
		db    1
		db 0ACh	; ¬
		db    5
		db  49h	; I
unk_1D0F0	db  6Eh	; n
		db  74h	; t
		db  65h	; e
		db  72h	; r
		db  6Eh	; n
		db  65h	; e
		db  74h	; t
		db  20h
		db  3Ah	; :
		db  20h
		db    2
unk_1D0FB	db  7Fh	; 
		db  73h	; s
		db  64h	; d
		db  61h	; a
		db  6Eh	; n
		db  65h	; e
		db  73h	; s
		db  40h	; @
		db  6Dh	; m
		db  61h	; a
		db  72h	; r
		db  76h	; v
		db  65h	; e
		db  6Ch	; l
		db  73h	; s
		db  2Eh	; .
		db  68h	; h
		db  61h	; a
		db  63h	; c
		db  6Bh	; k
		db  74h	; t
		db  69h	; i
		db  63h	; c
		db  2Eh	; .
		db  6Eh	; n
		db  6Ch	; l
		db    2
		db  7Eh	; ~
		db    1
		db  4Ch	; L
		db    6
		db  46h	; F
		db  69h	; i
		db  64h	; d
		db  6Fh	; o
		db  4Eh	; N
		db  65h	; e
		db  74h	; t
		db  20h
		db  20h
		db  3Ah	; :
		db  20h
		db    2
		db  7Fh	; 
		db  32h	; 2
		db  3Ah	; :
		db  32h	; 2
		db  38h	; 8
		db  34h	; 4
		db  2Fh	; /
		db  31h	; 1
		db  31h	; 1
		db  36h	; 6
		db  2Eh	; .
		db  38h	; 8
		db    2
		db  7Eh	; ~
		db    1
		db  26h	; &
		db    8
		db  53h	; S
		db  65h	; e
		db  6Eh	; n
		db  64h	; d
		db  20h
		db  65h	; e
		db  6Dh	; m
		db  61h	; a
		db  69h	; i
		db  6Ch	; l
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db    2
		db  7Fh	; 
		db  6Ch	; l
		db  69h	; i
		db  73h	; s
		db  74h	; t
		db  73h	; s
		db  65h	; e
		db  72h	; r
		db  76h	; v
		db  65h	; e
		db  72h	; r
		db  40h	; @
		db  6Fh	; o
		db  6Ch	; l
		db  69h	; i
		db  76h	; v
		db  65h	; e
		db  72h	; r
		db  2Eh	; .
		db  73h	; s
		db  75h	; u
		db  6Eh	; n
		db  2Eh	; .
		db  61h	; a
		db  63h	; c
		db  2Eh	; .
		db  7Ah	; z
		db  61h	; a
		db    2
		db  7Eh	; ~
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  73h	; s
		db  75h	; u
		db  62h	; b
		db  73h	; s
		db  63h	; c
		db  72h	; r
		db  69h	; i
		db  62h	; b
		db  65h	; e
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  6Fh	; o
		db  6Eh	; n
		db  65h	; e
		db  20h
		db  6Fh	; o
		db  72h	; r
		db  20h
		db  62h	; b
		db  6Fh	; o
		db  74h	; t
		db  68h	; h
		db  20h
		db  6Fh	; o
		db  66h	; f
		db    1
		db 0C6h	; Æ
		db    8
		db  74h	; t
		db  68h	; h
		db  65h	; e
		db  20h
		db    2
		db  7Fh	; 
		db  49h	; I
		db  6Eh	; n
		db  65h	; e
		db  72h	; r
		db  74h	; t
		db  69h	; i
		db  61h	; a
		db  20h
		db  4Dh	; M
		db  61h	; a
		db  69h	; i
		db  6Ch	; l
		db  69h	; i
		db  6Eh	; n
		db  67h	; g
		db  6Ch	; l
		db  69h	; i
		db  73h	; s
		db  74h	; t
		db  73h	; s
		db    2
		db  7Eh	; ~
		db  20h
		db  61h	; a
		db  6Eh	; n
		db  64h	; d
		db  20h
		db  77h	; w
		db  72h	; r
		db  69h	; i
		db  74h	; t
		db  65h	; e
		db  20h
		db  66h	; f
		db  6Fh	; o
		db  6Ch	; l
		db  6Ch	; l
		db  6Fh	; o
		db  77h	; w
		db  69h	; i
		db  6Eh	; n
		db  67h	; g
		db  20h
		db  74h	; t
		db  65h	; e
		db  78h	; x
		db  74h	; t
		db  20h
		db  69h	; i
		db  6Eh	; n
		db  20h
		db  79h	; y
		db  6Fh	; o
		db  75h	; u
		db  72h	; r
		db  20h
		db  6Dh	; m
		db  65h	; e
		db  73h	; s
		db  73h	; s
		db  61h	; a
		db  67h	; g
		db  65h	; e
		db  3Ah	; :
		db    1
		db  66h	; f
		db    9
		db  54h	; T
		db  6Fh	; o
		db  20h
		db  63h	; c
		db  6Fh	; o
		db  6Eh	; n
		db  6Eh	; n
		db  65h	; e
		db  63h	; c
		db  74h	; t
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  42h	; B
		db  69h	; i
		db  6Eh	; n
		db  61h	; a
		db  72h	; r
		db  79h	; y
		db  20h
		db  49h	; I
		db  6Eh	; n
		db  65h	; e
		db  72h	; r
		db  74h	; t
		db  69h	; i
		db  61h	; a
		db  20h
		db  72h	; r
		db  65h	; e
		db  6Ch	; l
		db  65h	; e
		db 61h
		db  73h	; s
		db  65h	; e
		db  73h	; s
		db  3Ah	; :
		db  20h
		db    2
		db  7Fh	; 
		db  73h	; s
		db  75h	; u
		db  62h	; b
		db  73h	; s
		db  63h	; c
		db  72h	; r
		db  69h	; i
		db  62h	; b
		db  65h	; e
		db  20h
		db  69h	; i
		db  6Eh	; n
		db  65h	; e
		db  72h	; r
		db  74h	; t
		db  69h	; i
		db  61h	; a
		db  2Dh	; -
		db  6Ch	; l
		db  69h	; i
		db  73h	; s
		db  74h	; t
		db  20h
		db  59h	; Y
		db  6Fh	; o
		db  75h	; u
		db  72h	; r
		db  52h	; R
		db  65h	; e
		db  61h	; a
		db  6Ch	; l
		db  4Eh	; N
		db  61h	; a
		db  6Dh	; m
		db  65h	; e
		db    2
		db  7Eh	; ~
		db    1
		db    6
		db  0Ah
		db  54h	; T
		db  6Fh	; o
		db  20h
		db  63h	; c
		db  6Fh	; o
		db  6Eh	; n
		db  6Eh	; n
		db  65h	; e
		db  63h	; c
		db  74h	; t
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  44h	; D
		db  69h	; i
		db  73h	; s
		db  63h	; c
		db  75h	; u
		db  73h	; s
		db  73h	; s
		db  69h	; i
		db  6Fh	; o
		db  6Eh	; n
		db  20h
		db  4Dh	; M
		db  61h	; a
		db  69h	; i
		db  6Ch	; l
		db  69h	; i
		db  6Eh	; n
		db  67h	; g
		db  20h
		db  6Ch	; l
		db  69h	; i
		db  73h	; s
		db  74h	; t
		db  3Ah	; :
		db  20h
		db    2
		db  7Fh	; 
		db  73h	; s
		db  75h	; u
		db  62h	; b
		db  73h	; s
		db  63h	; c
		db  72h	; r
		db  69h	; i
		db  62h	; b
		db  65h	; e
		db  20h
		db  69h	; i
		db  6Eh	; n
		db  65h	; e
		db  72h	; r
		db  74h	; t
		db  69h	; i
		db  61h	; a
		db  2Dh	; -
		db  74h	; t
		db  61h	; a
		db  6Ch	; l
		db  6Bh	; k
		db  20h
		db  59h	; Y
		db  6Fh	; o
		db  75h	; u
		db  72h	; r
		db  52h	; R
		db  65h	; e
		db  61h	; a
		db  6Ch	; l
		db  4Eh	; N
		db  61h	; a
		db  6Dh	; m
		db  65h	; e
		db    0
; char byte_1D26D
byte_1D26D	db 0F2h			; DATA XREF: sub_1C1B9+19o
		db    3
		db  7Eh	; ~
		db  53h	; S
		db  68h	; h
		db  65h	; e
		db  6Ch	; l
		db  6Ch	; l
		db  69h	; i
		db  6Eh	; n
		db  67h	; g
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  4Fh	; O
		db  70h	; p
		db  65h	; e
		db  72h	; r
		db  61h	; a
		db  74h	; t
		db  69h	; i
		db  6Eh	; n
		db  67h	; g
		db  20h
		db  53h	; S
		db  79h	; y
		db  73h	; s
		db  74h	; t
		db  65h	; e
		db  6Dh	; m
		db  2Eh	; .
		db  2Eh	; .
		db  2Eh	; .
		db    1
		db  2Ah	; *
		db    5
		db  54h	; T
		db  79h	; y
		db  70h	; p
		db  65h	; e
		db  20h
		db    2
		db  7Fh	; 
		db  45h	; E
		db  58h	; X
		db  49h	; I
		db  54h	; T
		db    2
		db  7Eh	; ~
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  72h	; r
		db  65h	; e
		db  74h	; t
		db  75h	; u
		db  72h	; r
		db  6Eh	; n
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db    2
		db  7Fh	; 
		db  49h	; I
		db  6Eh	; n
		db  65h	; e
		db  72h	; r
		db  74h	; t
		db  69h	; i
		db  61h	; a
		db  20h
		db  50h	; P
		db  6Ch	; l
		db  61h	; a
		db  79h	; y
		db  65h	; e
		db  72h	; r
		db    0
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
aPal		db '(PAL) ',0           ; DATA XREF: draw_text_bottom+49o
; char aNtsc[]
aNtsc		db '(NTSC)',0           ; DATA XREF: draw_text_bottom+53o
; char aU[1]
aU		db 'ž'                  ; DATA XREF: start+723o
		db    4
		db  7Bh	; {
		db  46h	; F
		db  69h	; i
		db  6Ch	; l
		db  65h	; e
		db  20h
		db  53h	; S
		db  65h	; e
		db  6Ch	; l
		db  65h	; e
		db  63h	; c
		db  74h	; t
		db  6Fh	; o
		db  72h	; r
		db  20h
		db  48h	; H
		db  65h	; e
		db  6Ch	; l
		db  70h	; p
		db    1
		db 0F2h	; ò
		db    6
		db    2
		db  7Eh	; ~
		db  55h	; U
		db  73h	; s
		db  65h	; e
		db  20h
		db    2
		db  7Fh	; 
		db  48h	; H
		db  6Fh	; o
		db  6Dh	; m
		db  65h	; e
		db    2
		db  7Eh	; ~
		db  2Ch	; ,
		db    2
		db  7Fh	; 
		db  45h	; E
		db  6Eh	; n
		db  64h	; d
		db    2
		db  7Eh	; ~
		db  2Ch	; ,
		db    2
		db  7Fh	; 
		db  50h	; P
		db  67h	; g
		db  55h	; U
		db  70h	; p
		db    2
		db  7Eh	; ~
		db  2Ch	; ,
		db    2
		db  7Fh	; 
		db  50h	; P
		db  67h	; g
		db  44h	; D
		db  6Eh	; n
		db    2
		db  7Eh	; ~
		db 2Ch
		db    2
		db  7Fh	; 
		db  18h
		db    2
		db  7Eh	; ~
		db  20h
		db  61h	; a
		db  6Eh	; n
		db  64h	; d
		db  20h
		db    2
		db  7Fh	; 
		db  19h
		db    2
		db  7Eh	; ~
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  6Dh	; m
		db  6Fh	; o
		db  76h	; v
		db  65h	; e
		db  20h
		db  74h	; t
		db  68h	; h
		db  65h	; e
		db  20h
		db  68h	; h
		db  69h	; i
		db  67h	; g
		db  68h	; h
		db  6Ch	; l
		db  69h	; i
		db  67h	; g
		db  68h	; h
		db  74h	; t
		db  65h	; e
		db  64h	; d
		db  20h
		db  62h	; b
		db  61h	; a
		db  72h	; r
		db    1
		db  92h	; ’
		db    7
		db  50h	; P
		db  72h	; r
		db  65h	; e
		db  73h	; s
		db  73h	; s
		db  20h
		db    2
		db  7Fh	; 
		db  45h	; E
		db  6Eh	; n
		db  74h	; t
		db  65h	; e
		db  72h	; r
		db    2
		db  7Eh	; ~
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  70h	; p
		db  6Ch	; l
		db  61h	; a
		db  79h	; y
		db  20h
		db  74h	; t
		db  68h	; h
		db  65h	; e
		db  20h
		db  6Dh	; m
		db  6Fh	; o
		db  64h	; d
		db  75h	; u
		db  6Ch	; l
		db  65h	; e
		db  20h
		db  6Fh	; o
		db  72h	; r
		db  20h
		db  73h	; s
		db  65h	; e
		db  6Ch	; l
		db  65h	; e
		db  63h	; c
		db  74h	; t
		db  20h
		db  74h	; t
		db  68h	; h
		db  65h	; e
		db  20h
		db  64h	; d
		db  72h	; r
		db  69h	; i
		db  76h	; v
		db  65h	; e
		db  2Fh	; /
		db  64h	; d
		db  69h	; i
		db  72h	; r
		db  65h	; e
		db  63h	; c
		db  74h	; t
		db  6Fh	; o
		db  72h	; r
		db  79h	; y
		db    1
		db 0D2h	; Ò
		db    8
		db    2
		db  7Fh	; 
		db  45h	; E
		db  53h	; S
		db  43h	; C
		db    2
		db  7Eh	; ~
		db    1
		db 0E6h	; æ
		db    8
		db  51h	; Q
		db  75h	; u
		db  69h	; i
		db  74h	; t
		db  20h
		db  49h	; I
		db  50h	; P
		db  4Ch	; L
		db  41h	; A
		db  59h	; Y
		db    1
		db  72h	; r
		db    9
		db    2
		db  7Fh	; 
		db  46h	; F
		db  2Dh	; -
		db  31h	; 1
		db    2
		db  7Eh	; ~
		db    1
		db  86h	; †
		db    9
		db  54h	; T
		db  68h	; h
		db  69h	; i
		db  73h	; s
		db  20h
		db  68h	; h
		db  65h	; e
		db  6Ch	; l
		db  70h	; p
		db  20h
		db  73h	; s
		db  63h	; c
		db  72h	; r
		db  65h	; e
		db  65h	; e
		db  6Eh	; n
		db  2Ch	; ,
		db  20h
		db  62h	; b
		db  75h	; u
		db  74h	; t
		db  20h
		db  49h	; I
		db  20h
		db  67h	; g
		db  75h	; u
		db  65h	; e
		db  73h	; s
		db  73h	; s
		db  20h
		db  79h	; y
		db  6Fh	; o
		db  75h	; u
		db  20h
		db  61h	; a
		db  6Ch	; l
		db  72h	; r
		db  65h	; e
		db  61h	; a
		db  64h	; d
		db  79h	; y
		db  20h
		db  66h	; f
		db  6Fh	; o
		db  75h	; u
		db  6Eh	; n
		db  64h	; d
		db  20h
		db  69h	; i
		db  74h	; t
		db  2Eh	; .
		db  2Eh	; .
		db  2Eh	; .
		db    1
		db  12h
		db  0Ah
		db    2
		db  7Fh	; 
		db  46h	; F
		db  2Dh	; -
		db  38h	; 8
		db    2
		db  7Eh	; ~
		db    1
		db  26h	; &
		db  0Ah
		db  44h	; D
		db  4Fh	; O
		db  53h	; S
		db  20h
		db  53h	; S
		db  68h	; h
		db  65h	; e
		db  6Ch	; l
		db  6Ch	; l
		db  20h
		db  28h	; (
		db  54h	; T
		db  79h	; y
		db  70h	; p
		db  65h	; e
		db  20h
		db  45h	; E
		db  58h	; X
		db  49h	; I
		db  54h	; T
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  72h	; r
		db  65h	; e
		db  74h	; t
		db  75h	; u
		db  72h	; r
		db  6Eh	; n
		db  29h	; )
		db    1
		db 0B2h	; ²
		db  0Ah
		db    2
		db  7Fh	; 
		db 46h
		db  2Dh	; -
		db  39h	; 9
		db    2
		db  7Eh	; ~
		db    1
		db 0C6h	; Æ
		db  0Ah
		db  54h	; T
		db 6Fh
		db  67h	; g
		db  67h	; g
		db  6Ch	; l
		db  65h	; e
		db  20h
		db  51h	; Q
		db  75h	; u
		db  69h	; i
		db  63h	; c
		db  6Bh	; k
		db  52h	; R
		db  65h	; e
		db  61h	; a
		db  64h	; d
		db  69h	; i
		db  6Eh	; n
		db  67h	; g
		db  20h
		db  6Fh	; o
		db  66h	; f
		db  20h
		db  6Dh	; m
		db  6Fh	; o
		db  64h	; d
		db  75h	; u
		db  6Ch	; l
		db  65h	; e
		db  20h
		db  6Eh	; n
		db 61h
		db  6Dh	; m
		db  65h	; e
		db    1
		db  52h	; R
		db  0Bh
unk_1D516	db    2
		db  7Fh	; 
		db  44h	; D
		db  65h	; e
		db  6Ch	; l
		db    2
		db  7Eh	; ~
		db    1
		db 66h
		db  0Bh
		db  4Dh	; M
		db  61h	; a
		db  72h	; r
		db  6Bh	; k
		db  20h
		db  66h	; f
		db  69h	; i
		db  6Ch	; l
		db  65h	; e
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  64h	; d
		db  65h	; e
		db  6Ch	; l
		db  65h	; e
		db  74h	; t
		db  65h	; e
		db    1
		db 0F2h
		db  0Bh
		db    2
		db  7Fh	; 
		db  43h	; C
		db  74h	; t
		db  72h	; r
		db  6Ch	; l
		db  20h
		db  44h	; D
		db  65h	; e
		db  6Ch	; l
		db    2
		db  7Eh	; ~
		db    1
		db    6
		db  0Ch
		db  44h	; D
		db  65h	; e
		db  6Ch	; l
		db  65h	; e
		db  74h	; t
		db  65h	; e
		db  20h
		db  61h	; a
		db  6Ch	; l
		db  6Ch	; l
		db  20h
		db  66h	; f
		db  69h	; i
		db  6Ch	; l
		db  65h	; e
		db  73h	; s
		db  20h
		db  77h	; w
		db  68h	; h
		db  69h	; i
		db  63h	; c
		db  68h	; h
		db  20h
		db  61h	; a
		db  72h	; r
		db  65h	; e
		db  20h
		db  6Dh	; m
		db  61h	; a
		db  72h	; r
		db  6Bh	; k
		db  65h	; e
		db  64h	; d
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  64h	; d
		db  65h	; e
		db  6Ch	; l
		db  65h	; e
		db  74h	; t
		db  65h	; e
		db    1
		db 92h
		db  0Ch
		db    2
		db  7Fh	; 
		db  42h	; B
		db  61h	; a
		db  63h	; c
		db  6Bh	; k
		db  53h	; S
		db  70h	; p
		db  61h	; a
		db  63h	; c
		db  65h	; e
		db    2
		db  7Eh	; ~
		db    1
		db 0A6h	; ¦
		db  0Ch
		db  52h	; R
		db  65h	; e
		db  74h	; t
		db  75h	; u
		db  72h	; r
		db  6Eh	; n
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  70h	; p
		db  6Ch	; l
		db  61h	; a
		db  79h	; y
		db  6Dh	; m
		db  6Fh	; o
		db  64h	; d
		db  65h	; e
		db  20h
		db  5Bh	; [
		db  4Fh	; O
		db  6Eh	; n
		db  6Ch	; l
		db  79h	; y
		db  20h
		db  69h	; i
		db  66h	; f
		db  20h
		db  74h	; t
		db  68h	; h
		db  65h	; e
		db  20h
		db  6Dh	; m
		db  75h	; u
		db  73h	; s
		db  69h	; i
		db  63h	; c
		db  20h
		db  69h	; i
		db  73h	; s
		db  20h
		db  70h	; p
		db  6Ch	; l
		db  61h	; a
		db  79h	; y
		db  69h	; i
		db  6Eh	; n
		db  67h	; g
		db  5Dh	; ]
		db    1
		db  86h	; †
		db  0Eh
		db    2
		db  7Eh	; ~
		db  50h	; P
		db  72h	; r
		db  65h	; e
		db  73h	; s
		db  73h	; s
		db  20h
		db  61h	; a
		db  6Eh	; n
		db  79h	; y
		db  20h
		db  6Bh	; k
		db  65h	; e
		db  79h	; y
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  72h	; r
		db  65h	; e
		db  74h	; t
		db  75h	; u
		db  72h	; r
		db  6Eh	; n
		db  20h
		db  74h	; t
		db  6Fh	; o
		db  20h
		db  74h	; t
		db  68h	; h
		db  65h	; e
		db  20h
		db  66h	; f
		db  69h	; i
		db  6Ch	; l
		db  65h	; e
		db  73h	; s
		db  65h	; e
		db  6Ch	; l
		db  65h	; e
		db  63h	; c
		db  74h	; t
		db  6Fh	; o
		db  72h	; r
		db    0
; char aPressF1ForHelpQu[11]
aPressF1ForHelpQu db '                 Press F-1 for help, QuickRead='
					; DATA XREF: start+367o
word_1D614	dw 2020h		; DATA XREF: sub_197F2+7w
					; sub_197F2:loc_19810w
byte_1D616	db 20h			; DATA XREF: sub_197F2+Dw
					; sub_197F2+24w
aF9		db ' [F-9]              ',0
aHitBackspaceToRe db 'Hit backspace to return to playmode, F-1 for help, QuickRead='
					; DATA XREF: start+35Do
word_1D669	dw 2020h		; DATA XREF: sub_197F2+12w
					; sub_197F2+29w
byte_1D66B	db 20h			; DATA XREF: sub_197F2+18w
					; sub_197F2+2Fw
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
slider		db 'Ä\|/Ä\|/'           ; DATA XREF: modules_search+7Fr
					; modules_search+F8r
aModuleNotFound	db 'Module not found.',0Dh,0Ah,'$' ; DATA XREF: sub_1C29E+88o
aModuleLoadErro	db 'Module load error.',0Dh,0Ah,'$' ; DATA XREF: sub_19D6D+1Bo
					; sub_19E11+5o
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
byte_1DB6C	db 128 dup(0)		; DATA XREF: start+189r start+192r ...
byte_1DBEC	db 0			; DATA XREF: sub_1C29E+32o sub_1C332o
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
byte_1DC0A	db 62h dup(0)		; DATA XREF: sub_1C29E+6Fo
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
byte_1DC7C	db 70h dup(0)		; DATA XREF: modules_search+1BAo
					; modules_search+202o
dword_1DCEC	dd 10524E49h		; DATA XREF: loadcfg+1Ar
cfg_buffer	db    4			; DATA XREF: loadcfg+Co loadcfg+1Er
snd_card_type	db 3			; DATA XREF: text_init2+18Er
					; text_init2+1ADr ...
word_1DCF2	dw 0FFFFh		; DATA XREF: callsubx+3r callsubx+45w
byte_1DCF4	db 0FFh			; DATA XREF: callsubx+7r callsubx+49w
byte_1DCF5	db 0FFh			; DATA XREF: callsubx+Br callsubx+4Dw
byte_1DCF6	db 2Ch			; DATA XREF: callsubx+Fr callsubx+51w
byte_1DCF7	db 0FFh			; DATA XREF: callsubx+1Cr callsubx+55w
byte_1DCF8	db 14h			; DATA XREF: start+DAr	callsubx+20r ...
configword	dw 218Bh		; DATA XREF: start+60w	start+6Cw ...
byte_1DCFB	db 4Bh			; DATA XREF: callsubx+13r
		db    0
unk_1DCFD	db    0			; DATA XREF: start:loc_192E0o
					; start:loc_1964Eo
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
		db    0
		db    0
		db    0
; char byte_1DD3F[69]
byte_1DD3F	db 45h dup(0)		; DATA XREF: sub_1C1B9:loc_1C209o
					; sub_1C1B9:loc_1C25Co
a_mod_nst_669_s	db '.MOD.NST.669.STM.S3M.MTM.PSM.WOW.INR.FAR.ULT.OKT.OCT',0,0,0,0
					; DATA XREF: modules_search+12Do
					; sub_1C29E+46o
aPlaypausloop	db 'PlayPausLoop'       ; DATA XREF: draw_text_bottom+164o
aJanfebmaraprmayj db '   JanFebMarAprMayJunJulAugSepOctNovDec'
					; DATA XREF: filelist_198B8+A4o
frameborder	db '      ÛÛÛÛÛÛÉ»È¼ÍºÚ¿ÀÙÄ³Ö·Ó½ÄºÕ¸Ô¾Í³',0 ; DATA XREF: draw_frame+3Do
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
segfsbx_1DE28	dd 0			; DATA XREF: sub_19E11+99w
					; sub_19EFD:l_rightr ...
dword_1DE2C	dd 0			; DATA XREF: text_init2+22Aw
					; seg001:196Br	...
messagepointer	dd 0			; DATA XREF: start+228r start+23Dw ...
volume_1DE34	dd 0			; DATA XREF: sub_19E11+DAw
					; seg001:19F4r
outp_freq	dw 0			; DATA XREF: sub_19E11+82w
					; text_init2:loc_1A699r ...
esseg_atstart	dw 0			; DATA XREF: start+5w parse_cmdline+7r ...
off_1DE3C	dw offset loc_19050	; DATA XREF: start+186w start+6E7r ...
offs_draw	dw offset loc_19050	; DATA XREF: sub_19EFD+32r
					; sub_19EFD:l_f4r ...
off_1DE40	dw offset loc_19050	; DATA XREF: sub_19EFD+486r
					; sub_19EFD+49Ar ...
off_1DE42	dw offset loc_19050	; DATA XREF: sub_19EFD:l_f8r
					; f1_help+12w ...
word_1DE44	dw 0			; DATA XREF: sub_19E11+75w
					; sub_19E11+D1r ...
word_1DE46	dw 0			; DATA XREF: sub_19EFD+316r
					; text_init2+244w ...
current_patterns dw 0			; DATA XREF: sub_19E11+5Fw
					; sub_19EFD+30Fw ...
word_1DE4A	dw 0			; DATA XREF: sub_1C29E+14w
					; sub_1C29E+4Er
word_1DE4C	dw 0			; DATA XREF: sub_1C29E+2Ew
					; sub_1C29E+75r
word_1DE4E	dw 0			; DATA XREF: start+19Bw
					; modules_search+5Fw ...
word_1DE50	dw 0			; DATA XREF: start:loc_19242r
					; sub_19D6D:loc_19D75r	...
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
fhandle_1DE68	dw 0			; DATA XREF: init_vga_equalizr+42w
					; init_vga_equalizr+49r ...
word_1DE6A	dw 0			; DATA XREF: sub_19EFD+1Cw
					; draw_text_bottom+118r
word_1DE6C	dw 0			; DATA XREF: sub_19EFD+27w
					; draw_text_bottom+13Br
word_1DE6E	dw 0			; DATA XREF: sub_19EFD+30Br
					; text_init2+52w ...
byte_1DE70	db 0			; DATA XREF: start+168w start+268w ...
byte_1DE71	db 0			; DATA XREF: seg001:loc_1A934w
					; seg001:loc_1AA73w
byte_1DE72	db 0			; DATA XREF: sub_19EFD+5w
					; draw_text_bottom+66r
byte_1DE73	db 0			; DATA XREF: sub_19E11+79w
					; draw_text_bottom+72r
byte_1DE74	db 0			; DATA XREF: sub_19EFD+9w
					; draw_text_bottom+92r
byte_1DE75	db 0			; DATA XREF: sub_19EFD+Cw
					; draw_text_bottom+1Br
byte_1DE76	db 0			; DATA XREF: sub_19EFD+10w
					; draw_text_bottom+2Br
byte_1DE77	db 0			; DATA XREF: sub_19EFD+2Fw
					; draw_text_bottom+4Cr	...
byte_1DE78	db 0			; DATA XREF: sub_19E11+8Bw
					; sub_1C1B9+2Cr ...
byte_1DE79	db 0			; DATA XREF: video_1C340+2w
					; video_1C340:loc_1C365w ...
byte_1DE7A	db 0			; DATA XREF: video_1C340+7w
					; video_1C340+1Dw ...
byte_1DE7B	db 0			; DATA XREF: sub_19E11+96w
					; text_init2+20Fr
byte_1DE7C	db 0			; DATA XREF: start:loc_193BCr
					; start+347r ...
byte_1DE7D	db 0			; DATA XREF: start+32Fw start+34Ar ...
byte_1DE7E	db 0			; DATA XREF: start+1B9w start+217r ...
byte_1DE7F	db 0			; DATA XREF: start+260w start+2F0r ...
		db    1
byte_1DE81	db 0			; DATA XREF: sub_1BBC1+20r
					; video_1C340+58w
byte_1DE82	db 0			; DATA XREF: start+E1w
					; sub_1BBC1:loc_1BBF4r	...
byte_1DE83	db 3			; DATA XREF: start+E7w
					; seg001:loc_1AA4Fr ...
byte_1DE84	db 0			; DATA XREF: sub_19E11+65w
					; sub_19EFD:l_upw ...
byte_1DE85	db 0			; DATA XREF: sub_19EFD+2EBw
					; sub_19EFD+2FBw ...
byte_1DE86	db 0			; DATA XREF: start+D7w	text_init2r ...
		db 0
dword_1DE88	dd 0			; DATA XREF: start+7DBr start+7E2w ...
mousecolumn	dw 0			; DATA XREF: start+7A0r start+7BCr ...
mouserow	dw 0			; DATA XREF: start+7A3r start+7BFr ...
byte_1DE90	db 0			; DATA XREF: start:loc_193C7r
					; start+33Er ...
mouse_exist_flag db 0			; DATA XREF: mouseinit:loc_1C6EFw
					; mouseinit:loc_1C708w	...
byte_1DE92	db 0Ah dup(0)		; DATA XREF: mouseinitw sub_1C70F+Cw ...
byte_1DE9C	db 43h dup(0)		; DATA XREF: seg001:1E88o
					; video_1AF63+Do ...
		align 10h
; char buffer_1[272]
buffer_1	db 200h	dup(0)		; DATA XREF: start-30o
					; start:loc_1906Eo ...
					; 2800h
byte_1E0E0	db 7BBh	dup(0)		; DATA XREF: f5_draw+29Do f5_draw+56Do
		db 1E44h dup(0)
		align 10h
buffer_2	db 2800h dup(0)		; DATA XREF: init_vga_equalizr+173o
buffer_1seg	dw 0			; DATA XREF: text_init2+18Bw
					; seg001:18B2r	...
buffer_2seg	dw 0			; DATA XREF: seg001:loc_1A913w
					; seg001:19D1r	...
byte_22EE4	db 1000h dup(0)		; DATA XREF: f5_draw+2A8o f5_draw+2D0o ...
unk_23EE4	db    0			; DATA XREF: init_f5_spectr+98o
					; f5_draw+2D9o	...
byte_23EE5	db 63h dup(0)		; DATA XREF: f5_draw+5C0o
byte_23F48	db 12Ch	dup(0)		; DATA XREF: f5_draw+5E2o
unk_24074	db    0			; DATA XREF: f5_draw+5A9o f5_draw+5C9o ...
byte_24075	db 63h dup(0)		; DATA XREF: f5_draw+5D2o
byte_240D8	db 12Ch	dup(0)		; DATA XREF: f5_draw+5EFo
byte_24204	db 200h	dup(0)		; DATA XREF: f5_draw+1Ao f5_draw+2A5o	...
palette_24404	db    0			; DATA XREF: init_vga_equalizr+17o
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
vga_palette	db 0,0,0		; DATA XREF: init_vga_equalizr+1Fo
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
word_24445	dw 0			; DATA XREF: sub_1C1B9+69w
					; sub_1C1B9+78o ...
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
str_24461	struct_0 <6, 9,	49h, 9,	offset loc_1957F> ; DATA XREF: start+79Do
		struct_0 <6, 19h, 49h, 19h, offset loc_1953C>
		struct_0 <8, 0Ah, 47h, 18h, offset loc_19880>
		struct_0 <2, 1,	4Dh, 4,	offset loc_19762>
		dw 0FFFFh
; struct struct_0 stru_2448B
stru_2448B	struct_0 <6, 9,	49h, 9,	offset loc_1957F> ; DATA XREF: start+7B9o
		struct_0 <6, 19h, 49h, 19h, offset loc_1953C>
		struct_0 <2, 1,	4Dh, 4,	offset loc_1964E>
		dw 0FFFFh
; struct struct_0 stru_244AB
stru_244AB	struct_0 <2, 1,	4Dh, 4,	offset l_enter>	; DATA XREF: sub_19EFD+4AFo
		dw 0FFFFh
; struct struct_0 stru_244B7
stru_244B7	struct_0 <0, 0,	4Fh, 31h, offset l_esc>	; DATA XREF: sub_19EFD:loc_1A3C5o
		dw 0FFFFh
		db    0
unk_244C4	db    0			; DATA XREF: sub_1B084+14Ew
					; sub_1B084+18Br ...
		db    0
		db    0
		db    0
dword_244C8	dd 0			; DATA XREF: sub_1B084+39w
					; sub_1B084+62r ...
multip_244CC	dd 0			; DATA XREF: sub_1B084+2Fw
					; sub_1B084+152r ...
multip_244D0	dd 0			; DATA XREF: sub_1B084+25w
					; sub_1B084+169r ...
dword_244D4	dd 0			; DATA XREF: sub_1B084+3Dw
					; sub_1B084+6Ar ...
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
dword_244E4	dd 0			; DATA XREF: sub_1B084+8Bw
					; sub_1B084+104r ...
dword_244E8	dd 0			; DATA XREF: sub_1B084+9Aw
					; sub_1B084+115r ...
dword_244EC	dd 0			; DATA XREF: sub_1B084+A9w
					; sub_1B084+BFr ...
dword_244F0	dd 0			; DATA XREF: sub_1B084+B6w
					; sub_1B084+CFr ...
dword_244F4	dd 0			; DATA XREF: sub_1B084+66w
					; sub_1B084+BAr ...
dword_244F8	dd 0			; DATA XREF: sub_1B084+6Ew
					; sub_1B084+DFr ...
dword_244FC	dd 0			; DATA XREF: sub_1B084+CBw
					; sub_1B084+108r ...
dword_24500	dd 0			; DATA XREF: sub_1B084+DBw
					; sub_1B084+119r ...
dword_24504	dd 0			; DATA XREF: sub_1B084+100w
					; sub_1B084+10Dr ...
dword_24508	dd 0			; DATA XREF: sub_1B084+F0w
					; sub_1B084+11Er ...
word_2450C	dw 0			; DATA XREF: sub_1B406+4w
					; sub_1B406+77r ...
word_2450E	dw 0			; DATA XREF: sub_1B084w sub_1B084+7Ar	...
		db    0
		db    0
		db    0
		db    0
word_24514	dw 0			; DATA XREF: sub_1B084+Fr
					; sub_1B084+42r ...
word_24516	dw 0			; DATA XREF: sub_1B406+61w
					; sub_1B406:loc_1B46Dr	...
word_24518	dw 0			; DATA XREF: sub_1B406+B2w
					; sub_1B406+B8r ...
word_2451A	dw 0			; DATA XREF: sub_1B406+D8w
					; sub_1B406+DBr
word_2451C	dw 0			; DATA XREF: sub_1B406+74w
					; sub_1B406+BDr ...
word_2451E	dw 0			; DATA XREF: sub_1B406+D1w
					; sub_1B406+E7r
word_24520	dw 0			; DATA XREF: sub_1B406+Ar f5_draw+2CAw ...
word_24522	dw 0			; DATA XREF: sub_1B406+10w
					; sub_1B406+3Fr ...
word_24524	dw 0			; DATA XREF: init_f5_spectr:loc_1B080w
					; f5_draw+2C7r	...
tabledword_24526 dd    0,65536,46340,25079,12785,6423,3215,1608, 804, 402
					; DATA XREF: sub_1B084+20r
					; sub_1B084+1CDr ...
		dd  201, 100,  50,  25,	 12
tabledword_24562 dd -131072,-65536,-19196,-4989,-1260,-316, -79, -20,  -5
					; DATA XREF: sub_1B084+2Ar
					; sub_1B084+1DAr ...
		dd   -2,  -1,  -1,  -1,	 -1,   0
		db    0
		db    0
ends		dseg

; ===========================================================================

; Segment type:	Regular
segment		seg003 byte public 'UNK' use16
		assume cs:seg003
		assume es:nothing, ss:nothing, ds:dseg,	fs:nothing, gs:nothing
a070295122642	db '07/02/95 12:26:42',0 ; DATA XREF: seg003:off_2462Eo
					; seg003:off_24656o
pointer_245B4	dd 0			; DATA XREF: sub_135CA+1Cr
					; sub_135CA:loc_135FDw	...
dma_buf_pointer	dd 0			; DATA XREF: sub_11F4E+9Cw
					; sub_11F4E+144r ...
dword_245BC	dd 0			; DATA XREF: sub_12BF8+59w
					; sub_13177+1Dr ...
dword_245C0	dd 0			; DATA XREF: sub_12BF8:loc_12C3Cw
					; sub_13177+31r ...
dword_245C4	dd 0			; DATA XREF: sub_100BD:loc_101F4r
					; sub_1024A+33w ...
off_245C8	dw offset moduleread	; DATA XREF: sub_12DA8+3Ew
					; sub_13623:loc_13791r	...
off_245CA	dw offset moduleread	; DATA XREF: sub_12DA8+38w
					; sub_135CA+4Dr ...
off_245CC	dw offset moduleread	; DATA XREF: change_volume+1Ar
					; sub_12DA8+44w ...
off_245CE	dw offset moduleread	; DATA XREF: sub_12A66+Fr
					; sub_12DA8+4Aw ...
savesp_245D0	dw 0			; DATA XREF: moduleread+15w
					; moduleread+B6r ...
word_245D2	dw 0			; DATA XREF: sub_100BD+9w
					; sub_100BD+43w ...
word_245D4	dw 0			; DATA XREF: moduleread+81r
					; moduleread+87r ...
word_245D6	dw 0			; DATA XREF: sub_11C43+4Aw
					; sub_12B83+52w ...
word_245D8	dw 0			; DATA XREF: sub_11C43+50w
					; sub_12B83+57w
word_245DA	dw 0			; DATA XREF: sub_11C43+56w
					; sub_12B83+5Cw
word_245DC	dw 0			; DATA XREF: sub_13623+12Dw
					; sub_13623+29Cr ...
freq_245DE	dw 0			; DATA XREF: sub_1024A+40r
					; seg000:0411w	...
off_245E0	dw offset chrin		; DATA XREF: sub_12DA8+E9w
					; sub_16C69+57Fr
off_245E2	dw offset myin		; DATA XREF: sub_12DA8+EFw
					; sub_16C69:loc_17202r
word_245E4	dw 0			; DATA XREF: sub_12FCD+18r
					; sub_13CF6+4Dw ...
word_245E8	dw 0			; DATA XREF: sub_12DA8+5Aw
					; sub_12DA8+F9w ...
word_245EA	dw 0			; DATA XREF: sub_13CF6:loc_13D36w
					; sub_16C69+13r
word_245EC	dw 0			; DATA XREF: sub_13CF6+44w
					; sub_16C69+19r
word_245EE	dw 0			; DATA XREF: sub_13CF6+47w
					; sub_16C69+Aw	...
word_245F0	dw 0			; DATA XREF: sub_11C43+21w
					; sub_1265D+46r ...
word_245F2	dw 0			; DATA XREF: sub_100BD+12Dr
					; sub_102F5+17w ...
word_245F4	dw 0			; DATA XREF: seg000:0E5Cr sub_11B85r ...
word_245F6	dw 0			; DATA XREF: sub_11C43+27w
					; sub_1265D+42r ...
word_245F8	dw 0			; DATA XREF: sub_1021E:loc_10230w
					; far_module+9Aw ...
word_245FA	dw 0			; DATA XREF: sub_1021E+8w
					; seg000:loc_104F2w ...
volume_245FC	dw 100h			; DATA XREF: sub_1265D+5r
					; change_volume+Bw ...
amplification	dw 100			; DATA XREF: sub_11C43+83w
					; volume_prepare_waves+72r ...
word_24600	dw 0			; DATA XREF: sub_12EBA+2Cw
					; sub_13017+1Bw ...
word_24602	dw 0			; DATA XREF: sub_12EBA+32w
					; sb_14700:loc_14E10w ...
interrupt_mask	dw 0			; DATA XREF: setsb_handler+Cw
					; restore_intvector+3r
old_intprocoffset dw 0			; DATA XREF: setsb_handler+3Aw
					; restore_intvector+14r
old_intprocseg	dw 0			; DATA XREF: setsb_handler+3Ew
					; restore_intvector+1Ar
intvectoffset	dw 0			; DATA XREF: setsb_handler+2Dw
					; restore_intvector+Cr
word_2460C	dw 0			; DATA XREF: sub_125B9+12r
					; sub_12D35+1Fr ...
word_2460E	dw 0			; DATA XREF: sub_14358+D5w
					; set_proaud+8w ...
word_24610	dw 0			; DATA XREF: volume_prep+6w
					; sub_1279A+4r	...
word_24612	dw 0			; DATA XREF: volume_prep+9w
					; sub_1279A+Dr	...
word_24614	dw 0			; DATA XREF: sub_154F4+3Ew
					; sub_1609F-909r ...
byte_24616	db 0			; DATA XREF: sub_154F4+41w
					; sub_154F4+52w ...
byte_24617	db 0			; DATA XREF: sub_11EFFw sub_11F4Ew ...
byte_24618	db 0			; DATA XREF: sub_13D95-6w sub_13D95w ...
byte_24619	db 0			; DATA XREF: sub_13D95+16w
					; sub_14358+7Cw ...
byte_2461A	db 0			; DATA XREF: s3m_module+1Fw
					; createwritefile+44r ...
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
					; sb_14700+71Cw ...
byte_24621	db 0			; DATA XREF: sub_12EBA+3Dw
					; sb_14700+73Bw ...
sndflags_24622	db 0			; DATA XREF: sub_11787+9r
					; sub_118B0+AEr ...
byte_24623	db 0			; DATA XREF: sub_1265D+33r
					; sub_12DA8+50w ...
bit_mode	db 8			; DATA XREF: sub_12DA8+55w
					; sub_12DA8+E2r ...
byte_24625	db 0			; DATA XREF: sub_11C43+89w
					; change_amplif+Ew ...
word_24626	dw 0			; DATA XREF: volume_prep+61r
					; sub_13215+49r ...
byte_24628	db 0			; DATA XREF: sub_11F4E+1BFr
					; sub_1265D+27r ...
byte_24629	db 20h			; DATA XREF: sub_12BF8+64r
					; sub_18079:loc_18088w	...
byte_2462A	db 0			; DATA XREF: seg000:429Ew seg000:42C2w ...
byte_2462B	db 0			; DATA XREF: seg000:42A1w seg000:42CAw ...
byte_2462C	db 0			; DATA XREF: sub_11F4E+8Er
					; volume_prep+43r ...
byte_2462D	db 0			; DATA XREF: seg000:42AAw seg000:42D6w ...
off_2462E	dw offset a070295122642	; DATA XREF: sub_13044+1Bw
					; sub_13044+2Ew ...
					; "07/02/95 12:26:42"
word_24630	dw 0			; DATA XREF: sub_11C43+32w
					; sub_11F4E+EDr ...
word_24632	dw 0			; DATA XREF: sub_14358+DEr
					; sub_182E7+4Dw
word_24634	dw 0			; DATA XREF: sub_14358+D8r
					; sub_182E7+45w
word_24636	dw 0			; DATA XREF: sub_14358+B5r
					; sub_14358+D1w ...
freq2		dw 0			; DATA XREF: sub_12CCF+2Cr
					; sub_18079+1Dw
		db    0
byte_2463B	db 0			; DATA XREF: seg000:4278w seg000:4284w ...
dword_2463C	dd 0			; DATA XREF: sub_12BF8+8Aw
					; sub_13215+2Ar
dword_24640	dd 0			; DATA XREF: sub_125DA+13w
					; volume_prep+4Dw ...
		db    0
byte_24645	db 0			; DATA XREF: sub_182DB+5w sub_182E7+Cw ...
word_24646	dw 0			; DATA XREF: proaud_check:loc_145A6w
sound_port	dw 0			; DATA XREF: proaud_check+42w
					; proaud_check+90r ...
byte_2464A	db 0			; DATA XREF: proaud_check+6Aw
					; proaud_check+9Br ...
byte_2464B	db 0			; DATA XREF: proaud_check+64w
					; set_proaud+11r ...
base_port2	dw 0			; DATA XREF: seg000:loc_147C3w
					; seg000:4819r	...
dma_channel2	db 0			; DATA XREF: seg000:loc_147DCw
					; seg000:loc_14801r ...
irq_number2	db 0			; DATA XREF: seg000:loc_147D0w
					; seg000:47E5r	...
byte_24650	db 0			; DATA XREF: set_wss+54w wss_sndoff+4r
byte_24651	db 0			; DATA XREF: set_wss+61w wss_sndoff+Cr
sb_base_port	dw 0			; DATA XREF: set_sb16+17r set_sb16+44r ...
word_24654	dw 0			; DATA XREF: sub_183CC+78w
off_24656	dw offset a070295122642	; DATA XREF: sub_13044+21w
					; sub_13044+34w ...
					; "07/02/95 12:26:42"
dma_chn_mask	db 0			; DATA XREF: seg000:4ABEw
					; seg000:loc_14AF5w ...
irq_number3	db 0			; DATA XREF: seg000:4A8Fw
					; seg000:loc_14AB3w ...
sb_timeconst	db 0			; DATA XREF: seg000:4C57w set_sb-D1r ...
word_2465C	dw 0			; DATA XREF: sub_141F6:loc_15302w
					; sub_153F1r ...
freq1		dw 22050		; DATA XREF: volume_prepare_waves+48r
					; sub_12BF8+49r ...
fhandle_module	dw 0			; DATA XREF: moduleread+19w
					; moduleread:loc_1006Br ...
word_24662	dw 0			; DATA XREF: moduleread:loc_1002Dw
					; moduleread+73w ...
byte_24664	db 0			; DATA XREF: set_sb-FFw
					; sbpro_sndoff+1Dr
byte_24665	db 0			; DATA XREF: moduleread:loc_10064w
					; sub_125DA:loc_125F6r
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
byte_2466E	db 0			; DATA XREF: sub_11F4E:loc_1212Br
					; volume_prep:loc_1276Cr ...
dma_mode	db 0			; DATA XREF: set_proaud+3w set_wss+3w	...
byte_24670	db 0			; DATA XREF: sub_1849Aw
					; sub_1849A:loc_184B0r	...
byte_24671	db 0			; DATA XREF: sub_1265D+3Ar
					; sub_12EBA+22w ...
byte_24672	db 0			; DATA XREF: sub_11C43+68r
					; sub_12AD3+6r	...
byte_24673	db 0			; DATA XREF: s3m_module+14w
					; s3m_module+2Bw ...
byte_24674	db 0			; DATA XREF: sub_11F4E+32w
					; sub_11F4E+BFw ...
byte_24675	db 0			; DATA XREF: sub_11F4E+2Aw
					; sub_11F4E+B7w ...
byte_24676	db 0			; DATA XREF: sub_12220:loc_12228r
					; sub_12220+23w
byte_24677	db 0			; DATA XREF: sub_15413+4r sub_15413+Aw
byte_24678	db 0			; DATA XREF: sub_15413+2Aw
byte_24679	db 0			; DATA XREF: seg000:041Cw
					; s3m_module+EFw ...
byte_2467A	db 0			; DATA XREF: seg000:0420w
					; s3m_module+F5w ...
byte_2467B	db 0			; DATA XREF: far_module+2Cw
					; sub_12EBA+7Fw ...
byte_2467C	db 0			; DATA XREF: far_module+2Fw
					; sub_12EBA+82w ...
byte_2467D	db 0			; DATA XREF: sub_13044:loc_1305Aw
					; sub_13044:loc_1306Dw	...
byte_2467E	db 0			; DATA XREF: s3m_module+Fw
					; e669_module+1Fw ...
byte_2467F	db 0			; DATA XREF: sub_12C99+Bw
					; sub_12C99:loc_12CA7r	...
byte_24680	db 0			; DATA XREF: sub_12D05+Br sub_141F6r ...
byte_24681	db 0			; DATA XREF: sub_12DA8+60w
					; sub_1420F+7r	...
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
byte_2469A	db 0			; DATA XREF: alloc_dma_buf+8w
					; alloc_dma_buf+B0w ...
byte_2469B	db 0			; DATA XREF: alloc_dma_buf+Dw
byte_2469C	db 0			; DATA XREF: alloc_dma_buf+4w
					; alloc_dma_buf+3Br
		db 0
ems_pageframe	dw 0			; DATA XREF: sub_11787+3Er
					; ems_init+61w	...
ems_handle	dw 0			; DATA XREF: ems_init+74w sub_11E02+Dr ...
ems_log_pagenum	dw 0			; DATA XREF: ems_init+7Dw
					; sub_11E02+15w ...
ems_supported	db 0			; DATA XREF: ems_initw	ems_init+78w ...
byte_246A5	db 0			; DATA XREF: sub_11E47+1Bw
					; sub_11E68+7r
word_246A6	dw 0			; DATA XREF: sub_12CAD+9o
					; sub_12CAD+18w
byte_246A8	db 0			; DATA XREF: sub_12CAD+14w
word_246A9	dw 0			; DATA XREF: sub_12CAD+10w
module_type_text dd 20202020h		; DATA XREF: sub_100BDw
					; sub_100BD:mod_flt8_modulew ...
; char asc_246B0[32]
asc_246B0	db '                                ' ; DATA XREF: sub_1021E+22o
					; seg000:0432o	...
moduleflag_246D0 dw 0			; DATA XREF: sub_100BD+3Dw
					; sub_10311+12r ...
sndcard_type	db 0			; DATA XREF: seg000:0B03r
					; far_module+3Fr ...
snd_base_port	dw 0			; DATA XREF: sub_12CCF+9r sub_12D61+9w ...
irq_number	db 0			; DATA XREF: sub_12CCF+Dr sub_12D61+Cw ...
dma_channel	db 0			; DATA XREF: sub_12CCF+11r
					; sub_12D61+Fw	...
freq_246D7	db 0			; DATA XREF: sub_12CCF+15r
					; sub_12DA8+17w ...
byte_246D8	db 0			; DATA XREF: sub_12CCF+19r
					; sub_12D61+12w ...
byte_246D9	db 0			; DATA XREF: sub_12CCF+1Dr
					; sub_12D61+15w ...
word_246DA	dw 0			; DATA XREF: ems_init+8r
					; sub_12CCF:loc_12CFFr	...
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
					; DATA XREF: sub_10311:loc_10399r
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
off_252A2	dw offset gravis_check	; DATA XREF: sub_141F6+13r
		dw offset proaud_check
		dw offset check_wss
		dw offset sb16_check
		dw offset sbpro_check
		dw offset sb_check
		dw offset check_covox
		dw offset check_stereo
		dw offset adlib_check
		dw offset check_pc
		dw offset check_midi
off_252B8	dw offset set_gravis	; DATA XREF: sub_1420F+1Ar
		dw offset set_proaud
		dw offset set_wss
		dw offset set_sb16
		dw offset set_sbpro
		dw offset set_sb
		dw offset set_covox
off_252C6	dw offset set_stereoon
		dw offset set_adlib
		dw offset set_pc
		dw offset set_midi
off_252CE	dw offset gravis_sndoff	; DATA XREF: sub_1422D+1Er
		dw offset proaud_sndoff
		dw offset wss_sndoff
		dw offset sb16_sndoff
		dw offset sbpro_sndoff
		dw offset sb_sndoff
		dw offset covox_sndoff
		dw offset stereoon_sndoff
		dw offset adlib_sndoff
		dw offset pc_sndoff
		dw offset midi_sndoff
off_252E4	dw offset gravis_clean	; DATA XREF: sub_1424F+16r
		dw offset proaud_clean
		dw offset wss_clean
		dw offset sb16_clean
		dw offset sbpro_clean
		dw offset sb_clean
		dw offset covox_clean
		dw offset stereoon_clean
		dw offset adlib_clean
		dw offset pc_clean
		dw offset midi_clean
off_252FA	dw offset aGravisUltrasoun ; DATA XREF:	seg003:114Eo
					; seg003:1194o	...
					; "Gravis UltraSound"
		dw offset aProAudioSpectrum ; "Pro Audio Spectrum 16"
		dw offset aWindowsSoundSyst ; "Windows Sound System"
		dw offset aSoundBlaster1616 ; "Sound Blaster 16/16ASP"
		dw offset aSoundBlasterPro ; "Sound Blaster Pro"
		dw offset aSoundBlaster_0 ; "Sound Blaster"
		dw offset aCovox_0	; "Covox"
		dw offset aStereoOn1_0	; "Stereo-On-1"
		dw offset aAdlibSoundcard_0 ; "Adlib SoundCard"
		dw offset aPcHonker_0	; "PC Honker"
		dw offset aGeneralMidi_0 ; "General MIDI"
sndcards_table	dw offset unk_25659	; DATA XREF: sub_12D05+19r
		dw offset unk_256EA
		dw offset unk_256EA
		dw offset unk_256EA
		dw offset unk_256EA
		dw offset unk_256EA
		dw offset unk_25730
		dw offset unk_25730
		dw offset unk_2576A
		dw offset unk_2576A
		dw offset unk_2578A
off_25326	dw offset inr_module	; DATA XREF: moduleread+40o
					; INR
		db    0
		db    0
		db 16
aInertiaModule_1 db 'Inertia Module: '
		dw offset mod_mk_module
		db  38h	; 8
		db    4
		db    4
aM_k_		db 'M.K.'
		dw offset mod_mk_module
		db  38h	; 8
		db    4
		db    4
a_m_k		db '.M.K'
		dw offset mod_mk_module
		db  38h	; 8
		db    4
		db    4
aMK		db 'M&K!'
		dw offset mod_mk_module
		db  38h	; 8
		db    4
		db    4
aMK_0		db 'M!K!'
		dw offset mod_mk_module
		db  38h	; 8
		db    4
		db    4
aGsft		db 'GSFT'
		dw offset mod_mk_module
		db  38h	; 8
		db    4
		db    4
aE_g_		db 'E.G.'
		dw offset mod_mk_module
		db  38h	; 8
		db    4
		db    4
aFlt4		db 'FLT4'
		dw offset mod_flt8_module ; FLT8
		db  38h	; 8
		db    4
		db    4
aFlt8		db 'FLT8'
		dw offset mod_cd81_module
		db  38h	; 8
		db    4
		db    4
aCd81		db 'CD81'
		dw offset mod_cd81_module
		db  38h	; 8
		db    4
		db    4
aOcta		db 'OCTA'
		dw offset mod_chn_module
		db  39h	; 9
		db    4
		db    3
aChn		db 'CHN'
		dw offset mod_ch_module
		db  3Ah	; :
		db 4
		db    2
aCh		db 'CH'
		dw offset mod_tdz_module
		db  38h	; 8
		db    4
		db    3
aTdz		db 'TDZ'
		dw offset stm_module	; STM
		db  14h
		db    0
		db    8
aScream		db '!Scream!'
		dw offset _2stm_module	; 2STM
		db  14h
		db    0
		db    8
aBmod2stm	db 'BMOD2STM'
		dw offset s3m_module	; S3M
		db  2Ch	; ,
		db    0
		db    4
aScrm		db 'SCRM'
		dw offset mtm_module	; MTM
		db    0
		db    0
		db    3
aMtm		db 'MTM'
		dw offset psm_module	; PSM
		db    0
		db    0
		db    4
aPsm		db 'PSMþ'
		dw offset far_module	; FAR
		db    0
		db    0
		db    4
aFar		db 'FARþ'
		dw offset ult_module	; ULT
		db    0
		db    0
		db  0Ch
aMas_utrack_v	db 'MAS_UTrack_V'
		dw offset _669_module	; 669
		db    0
		db    0
		db    2
aIf		db 'if'
		dw offset e669_module	; E669
		db    0
		db    0
		db    2
aJn		db 'JN'
eModuleNotFound	db 'Module not found',0Dh,0Ah,0 ; DATA XREF: moduleread+1Co
aNotEnoughMemory db 'Not enough Memory available',0Dh,0Ah,0
					; DATA XREF: moduleread:loc_10099o
aNotEnoughDramOn db 'Not enough DRAM on UltraSound',0Dh,0Ah,0 ; DATA XREF: sub_11F4E+1CCo
aSomeFunctionsOf db 'Some functions of the UltraSound do not work!',0Dh,0Ah
		db 0Ah
		db 'Probably the AT-BUS Clock Speed is too high.',0Dh,0Ah
		db 'Try changing the AT-BUS Clock in the CMOS Setup.',0Dh,0Ah,0
aCouldNotFindThe db 'Could not find the ULTRASND environment string',0Dh,0Ah,0
					; DATA XREF: seg000:loc_1432Fo
aCouldNotFindT_0 db 'Could not find the Gravis UltraSound at the specified port addres'
		db 's',0Dh,0Ah,0
aThisProgramRequ db 'This program requires the soundcards device driver.',0Dh,0Ah,0
aErrorSoundcardN db 'Error: Soundcard not found!',0Dh,0Ah,0
					; DATA XREF: proaud_check:loc_1464Fo
					; sub_14996:loc_149ACo	...
aErrorCouldNotFi db 'Error: Could not find IRQ/DMA!',0Dh,0Ah,0
aErrorCouldNot_0 db 'Error: Could not find IRQ!',0Dh,0Ah,0 ; DATA XREF: sub_18449+4Co
aErrorCouldNot_1 db 'Error: Could not find DMA!',0Dh,0Ah,0 ; DATA XREF: sub_18449+D6o
aDeviceNotIniti	db 'Device not initialised!',0 ; DATA XREF: sub_12D05+8o
aAt		db ' at',0              ; DATA XREF: seg003:10BFo seg003:1152o ...
aBasePort	db ' base port ',0      ; DATA XREF: seg003:10C3o seg003:1156o ...
aMixedAt	db ', mixed at ',0      ; DATA XREF: seg003:1173o seg003:11A5o ...
aKhz		db 'kHz',0              ; DATA XREF: seg003:117Bo seg003:11ADo ...
aGravisUltrasoun db 'Gravis UltraSound',0 ; DATA XREF: seg003:off_252FAo
					; seg003:10BBo
unk_25659	db    1			; DATA XREF: seg003:sndcards_tableo
		db    0
		dw offset aGravisUltrasoun ; "Gravis UltraSound"
		db    1
		db    0
		dw offset aAt		; " at"
		db    1
		db    0
		dw offset aBasePort	; " base port "
		db  0Bh
		db    0
		dw offset snd_base_port
		db 68h
		db  2Ch	; ,
		db  20h
		db  47h	; G
		db  46h	; F
		db  31h	; 1
		db  2Dh	; -
		db  49h	; I
		db  52h	; R
		db  51h	; Q
		db  20h
		db    4
		db    0
		dw offset irq_number
		db  2Ch	; ,
		db  20h
		db  44h	; D
		db  52h	; R
		db  41h	; A
		db  4Dh	; M
		db  2Dh	; -
		db  44h	; D
		db  4Dh	; M
		db  41h	; A
		db  20h
		db    4
		db    0
		dw offset dma_channel
		db    0
aProAudioSpectrum db 'Pro Audio Spectrum 16',0 ; DATA XREF: seg003:0D5Co
aWindowsSoundSyst db 'Windows Sound System',0 ; DATA XREF: seg003:0D5Eo
aSoundBlaster1616 db 'Sound Blaster 16/16ASP',0 ; DATA XREF: seg003:0D60o
aSoundBlasterPro db 'Sound Blaster Pro',0 ; DATA XREF: seg003:0D62o
aSoundBlaster_0	db 'Sound Blaster',0    ; DATA XREF: seg003:0D64o
unk_256EA	db    2			; DATA XREF: seg003:0D72o seg003:0D74o ...
		db    0
		dw offset sndcard_type
		dw offset off_252FA
		db    1
		db    0
		dw offset aAt		; " at"
		db    1
		db    0
		dw offset aBasePort	; " base port "
		db 0Bh
		db    0
		dw offset snd_base_port
		db  68h	; h
		db  2Ch	; ,
		db  20h
		db  49h	; I
		db  52h	; R
		db  51h	; Q
		db  20h
		db    4
		db    0
		dw offset irq_number
		db  2Ch	; ,
		db  20h
		db  44h	; D
		db  4Dh	; M
		db  41h	; A
		db  20h
		db    4
		db    0
		dw offset dma_channel
		db    1
		db    0
		dw offset aMixedAt	; ", mixed at "
		db    4
		db    0
		dw offset freq_246D7
		db    1
		db    0
		dw offset aKhz		; "kHz"
		db    0
aCovox_0	db 'Covox',0            ; DATA XREF: seg003:0D66o
aStereoOn1_0	db 'Stereo-On-1',0      ; DATA XREF: seg003:0D68o
unk_25730	db    2			; DATA XREF: seg003:0D7Co seg003:0D7Eo
		db    0
		dw offset sndcard_type
		dw offset off_252FA
		db    1
		db    0
		dw offset aAt		; " at"
		db    1
		db    0
		dw offset aBasePort	; " base port "
		db  0Bh
		db    0
		dw offset snd_base_port
		db 68h
		db    1
		db    0
		dw offset aMixedAt	; ", mixed at "
		db    4
		db    0
		dw offset freq_246D7
		db    1
		db    0
		dw offset aKhz		; "kHz"
		db    0
aAdlibSoundcard_0 db 'Adlib SoundCard',0 ; DATA XREF: seg003:0D6Ao
aPcHonker_0	db 'PC Honker',0        ; DATA XREF: seg003:0D6Co
unk_2576A	db    2			; DATA XREF: seg003:0D80o seg003:0D82o
		db    0
		dw offset sndcard_type
		dw offset off_252FA
		db    1
		db    0
		dw offset aMixedAt	; ", mixed at "
		db    4
		db    0
		dw offset freq_246D7
		db    1
		db    0
		dw offset aKhz		; "kHz"
		db    0
aGeneralMidi_0	db 'General MIDI',0     ; DATA XREF: seg003:0D6Eo
unk_2578A	db    2			; DATA XREF: seg003:0D84o
		db    0
		dw offset sndcard_type
		dw offset off_252FA
		db    1
		db    0
		dw offset aAt		; " at"
		db    1
		db    0
		dw offset aBasePort	; " base port "
		db  0Bh
		db    0
		dw offset snd_base_port
		db  68h	; h
		db    0
		db    0
		db    0
dword_257A0	dd 0			; DATA XREF: createwritefile+170w
					; sub_118B0+82w ...
word_257A4	dw 0			; DATA XREF: createwritefile+106w
					; createwritefile+111r	...
aInertiaModule	db 'Inertia Module: ',0 ; DATA XREF: createwritefile+29o
					; createwritefile+80o ...
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
byte_257DA	db 10h			; DATA XREF: createwritefile+3Fw
byte_257DB	db 0			; DATA XREF: createwritefile+47w
					; inr_module+3Er
byte_257DC	db 0			; DATA XREF: createwritefile+4Dw
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
word_257E6	dw 4			; DATA XREF: createwritefile+53w
					; inr_module+4Ar
word_257E8	dw 0			; DATA XREF: createwritefile+59w
word_257EA	dw 0			; DATA XREF: createwritefile+5Fw
word_257EC	dw 0			; DATA XREF: createwritefile+65w
					; inr_module+54r
word_257EE	dw 0			; DATA XREF: createwritefile+6Bw
					; inr_module+5Ar
word_257F0	dw 0			; DATA XREF: createwritefile+71w
					; inr_module+60r
byte_257F2	db 0			; DATA XREF: createwritefile+77w
					; inr_module+66r
byte_257F3	db 0			; DATA XREF: createwritefile+7Dw
					; inr_module+6Cr
		db    0
		db    0
aInertiaModule_0 db 'Inertia Module: ',0 ; DATA XREF: createwritefile+23o
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
aInertiaSample	db 'Inertia Sample: '   ; DATA XREF: sub_1181D+11o
					; sub_1181D+5Fo ...
asc_25856	db '                                ',0Dh,0Ah,1Ah ; DATA XREF: sub_1181D+21o
					; sub_118B0+26o
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
dword_25886	dd 0			; DATA XREF: sub_1181D+59w
					; sub_118B0+64r
		db  10h
byte_2588B	db 0			; DATA XREF: sub_1181D+4Cw
					; sub_118B0+58r
byte_2588C	db 0			; DATA XREF: sub_1181D+46w
					; sub_118B0+52r
byte_2588D	db 0			; DATA XREF: sub_1181D+52w
					; sub_118B0+5Er
word_2588E	dw 0			; DATA XREF: sub_1181D+40w
					; sub_118B0+4Cr
		db    0
		db    0
dword_25892	dd 0			; DATA XREF: sub_1181D+31w
					; sub_118B0+32r
dword_25896	dd 0			; DATA XREF: sub_1181D+39w
					; sub_118B0+3Br
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
unk_258A6	db  49h	; I		; DATA XREF: sub_1181D+Eo
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
byte_25908	db 0A00h dup(0)		; DATA XREF: s3m_module+89o
					; sub_11C43+A2o ...
; char myout[152]
myout		db 18C0h dup(?)		; DATA XREF: sub_1024A+3o seg000:043Eo ...
dword_27BC8	dd ?			; DATA XREF: moduleread+8Eo
					; s3m_module:loc_1065Fw ...
dword_27BCC	dd ?			; DATA XREF: e669_module+4Ew
		db 18h dup(?)
segs_table	dw 100h	dup( ?)		; DATA XREF: createwritefile+13Cr
					; inr_module+10Dw ...
word_27DE8	dw 100h	dup( ?)		; DATA XREF: createwritefile+117r
					; inr_module+116w ...
byte_27FE8	db 0FFh	dup( ?)		; DATA XREF: sub_100BD+55o
					; sub_1021E+15o ...
byte_280E7	db ?			; DATA XREF: s3m_module+1F3w
byte_280E8	db 100h	dup( ?)		; DATA XREF: e669_module+80w
					; e669_module+97r ...
byte_281E8	db 100h	dup( ?)		; DATA XREF: e669_module+88w
					; seg000:0E6Ew	...
byte_282E8	db 20h dup( ?)		; DATA XREF: sub_11C43+AEo
					; sub_11C43+11Co ...
byte_28308	db 8200h dup( ?)	; DATA XREF: volume_prepare_waves+8Ao
					; sub_13044:loc_13091o	...
; char chrin[]
chrin		dd ?			; DATA XREF: moduleread:loc_10033o
					; moduleread:loc_10049o ...
; char myin[]
myin		dd ?			; DATA XREF: seg000:0AF7o seg000:0D65o ...
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
word_30515	dw ?			; DATA XREF: seg000:1253r seg000:1258w ...
unk_30517	db    ?	;		; DATA XREF: seg000:1273o
dword_30518	dd ?			; DATA XREF: seg000:loc_113F8o
					; seg000:1439o
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
word_30520	dw ?			; DATA XREF: sub_1422D-3644r
					; sub_1422D-3543r
byte_30522	db ?			; DATA XREF: seg000:0B2Dr
byte_30523	db ?			; DATA XREF: seg000:0B35r
word_30524	dw ?			; DATA XREF: sub_1422D-3534r
byte_30526	db ?			; DATA XREF: seg000:loc_10B25r
		db    ?	;
unk_30528	db    ?	;		; DATA XREF: s3m_module+102r
					; s3m_module+1D5r ...
byte_30529	db ?			; DATA XREF: seg000:0423r
word_3052A	dw ?			; DATA XREF: s3m_module+D0r
					; s3m_module+225r ...
word_3052C	dw ?			; DATA XREF: s3m_module+DEr
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
word_30532	dw ?			; DATA XREF: s3m_module+24r
		db    ?	;
		db    ?	;
		db    ?	;
byte_30537	db ?			; DATA XREF: seg000:1285r
byte_30538	db ?			; DATA XREF: seg000:043Bo seg000:127Fo ...
byte_30539	db ?			; DATA XREF: s3m_module+ECr
					; seg000:12A4o	...
byte_3053A	db ?			; DATA XREF: s3m_module+F2r
byte_3053B	db ?			; DATA XREF: s3m_module+4Ar
					; s3m_module+53r
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
byte_30548	db ?			; DATA XREF: s3m_module:loc_10628r
					; s3m_module+BEr
		db    ?	;
unk_3054A	db    ?	;		; DATA XREF: seg000:0B50o
byte_3054B	db ?			; DATA XREF: seg000:0D47r
byte_3054C	db ?			; DATA XREF: seg000:0D4Dr
		db    ?	;
		db    ?	;
		db    ?	;
byte_30550	db ?			; DATA XREF: seg000:0D53r
		db    ?	;
word_30552	dw ?			; DATA XREF: seg000:0D5Br
					; far_module+1Fr
word_30554	dw ?			; DATA XREF: seg000:0D3Br
					; far_module:loc_10F6Ar
word_30556	dw ?			; DATA XREF: seg000:0D35r
		db    ?	;
		db    ?	;
dword_3055A	dd ?			; DATA XREF: seg000:0E2Br
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
word_30562	dw ?			; DATA XREF: seg000:0E32r
word_30564	dw ?			; DATA XREF: seg000:0E36r
dword_30566	dd ?			; DATA XREF: seg000:0D7Br
					; s3m_module+FFo ...
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
byte_30576	db ?			; DATA XREF: e669_module+2Ar
byte_30577	db ?			; DATA XREF: e669_module+32r
		db    ?	;
byte_30579	db 21h dup( ?)		; DATA XREF: e669_module:loc_1096Fr
byte_3059A	db 5Fh dup( ?)		; DATA XREF: seg000:0D71o seg000:0D82o
byte_305F9	db 40h dup( ?)		; DATA XREF: e669_module+7Cr
byte_30639	db ?			; DATA XREF: seg000:13A2r
byte_3063A	db ?			; DATA XREF: seg000:13ABr
word_3063B	dw ?			; DATA XREF: seg000:13CBo
					; seg000:loc_113E2r ...
dword_3063D	dd ?			; DATA XREF: seg000:145Er
					; sub_1155A+19w ...
byte_30641	db 28h dup( ?)		; DATA XREF: seg000:1465r
byte_30669	db ?			; DATA XREF: far_module+85r
byte_3066A	db ?			; DATA XREF: far_module+95r
byte_3066B	db 0Eh dup( ?)		; DATA XREF: far_module+AAo
					; far_module+D9o
byte_30679	db 65h dup( ?)		; DATA XREF: e669_module+84r
byte_306DE	db 1E0h	dup( ?)		; DATA XREF: sub_100BD+15o
byte_308BE	db 4Ah dup( ?)		; DATA XREF: sub_100BD+4Fo
					; sub_100BD+F1o
byte_30908	db 38h dup( ?)		; DATA XREF: seg000:143Co seg000:148Eo
byte_30940	db ?			; DATA XREF: sub_100BD:mod_chn_moduler
					; sub_100BD+9Cr ...
unk_30941	db    ?	;		; DATA XREF: sub_100BD+ACr
		db    ?	;
byte_30943	db  ?			; DATA XREF: sub_100BD:mod_tdz_moduler
		db 0BC4h dup(?)
; char word_31508[]
word_31508	dw ?			; DATA XREF: sub_10311+5o
					; sub_10311+1Eo ...
byte_3150A	db ?			; DATA XREF: seg000:0E5Fr
					; far_module+130o
		db    ?	;
byte_3150C	db 7FCh	dup( ?)		; DATA XREF: seg000:0E76o seg000:0E86o
byte_31D08	db 1800h dup( ?)	; DATA XREF: sub_10311+21o
					; sub_10311+2Bo
byte_33508	db 1008h dup( ?)	; DATA XREF: sub_1422D-3632o
					; sub_1422D-3625o ...
ends		seg003

; ===========================================================================

; Segment type:	Uninitialized
segment		seg004 byte stack 'STACK' use16
		assume cs:seg004
		assume es:nothing, ss:nothing, ds:dseg,	fs:nothing, gs:nothing
byte_34510	db 1000h dup(?)
ends		seg004


		end start
