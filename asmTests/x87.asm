.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
; IEEE-754 bit patterns (float literals are not supported in data)
half_d   dd 3F000000h            ; 0.5f
one_d    dd 3F800000h            ; 1.0f
one5_d   dd 3FC00000h            ; 1.5f
two_d    dd 40000000h            ; 2.0f
neg15_d  dd 0BFC00000h           ; -1.5f
neg2_d   dd 0C0000000h           ; -2.0f
four_d   dd 40800000h            ; 4.0f
sixq_d   dd 40C80000h            ; 6.25f
two5_d   dd 40200000h            ; 2.5f
one_q    dq 3FF0000000000000h    ; 1.0
two_q    dq 4000000000000000h    ; 2.0
three_q  dq 4008000000000000h    ; 3.0
four_q   dq 4010000000000000h    ; 4.0
six_q    dq 4018000000000000h    ; 6.0
seven_q  dq 401C000000000000h    ; 7.0
eight_q  dq 4020000000000000h    ; 8.0
twelve_q dq 4028000000000000h    ; 12.0
p075_q   dq 3FE8000000000000h    ; 0.75
piby4_q  dq 3FE921FB54442D18h    ; pi/4
pi_q     dq 400921FB54442D18h    ; pi
ln2_q    dq 3FE62E42FEFA39EFh    ; ln(2)
lg2_q    dq 3FD34413509F79FFh    ; log10(2)
l2e_q    dq 3FF71547652B82FEh    ; log2(e)
l2t_q    dq 400A934F0979A371h    ; log2(10)
tb_1     dt 3FFF8000000000000000h ; 1.0 tbyte
tb_10    dt 4002A000000000000000h ; 10.0 tbyte
bcd1234  db 78h,56h,34h,12h,0,0,0,0,0,0  ; packed BCD 12345678
intw     dw 7
intwn    dw -3
intd     dd 42
intd2    dd 3
outw     dw ?
outd     dd ?
outq     dq ?
outtb    dt ?
bcdout   dt ?
fsw      dw ?
fcw      dw ?
cw_trunc dw 0C7Fh               ; RC=11 truncate, rest like 037f
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start:

fninit

; ---------- fld dword / fstp dword ----------
fld one_d
fstp outd
cmp outd,3F800000h
jne failure

; ---------- fld qword / fst qword (no pop) ----------
fld six_q
fst outq
cmp dword ptr outq,0
jne failure
cmp dword ptr outq+4,40180000h
jne failure
fstp st                       ; pop (fstp st(0))

; ---------- fld st(i) / register stack ----------
fld six_q                     ; st0=6
fld st                        ; push st0 -> st0=6,st1=6
fadd                          ; bare fadd = faddp st1,st0 -> st0=12
fistp outd
cmp outd,12
jne failure

; ---------- fld st(i) explicit ----------
fld six_q                     ; st0=6
fld st                        ; st0=6 st1=6
fstp st(1)                    ; st1=st0=6, pop -> st0=6
fistp outd
cmp outd,6
jne failure

; ---------- fild word / fistp word ----------
fild intw                     ; 7.0
fistp outw
cmp outw,7
jne failure

; ---------- fild dword ----------
fild intd                     ; 42.0
fistp outd
cmp outd,42
jne failure

; ---------- fiadd ----------
fld one_d
fiadd intw                    ; 1+7=8
fistp outd
cmp outd,8
jne failure

; ---------- fisub / fimul / fidiv ----------
fild intd
fisub intw                    ; 42-7=35
fistp outd
cmp outd,35
jne failure

fild intd
fimul intw                    ; 42*7=294
fistp outd
cmp outd,294
jne failure

fild intd
fidiv intw                    ; 42/7=6
fistp outd
cmp outd,6
jne failure

; ---------- fsub/fmul/fdiv memory ----------
fld six_q
fsub one_q                    ; 5.0
fistp outd
cmp outd,5
jne failure

fld two_q
fmul six_q                    ; 12.0
fistp outd
cmp outd,12
jne failure

fld six_q
fdiv two_q                    ; 3.0
fistp outd
cmp outd,3
jne failure

fld six_q
fsub dword ptr two_d          ; 6-2=4 (real4 operand)
fistp outd
cmp outd,4
jne failure

; ---------- reversed ----------
fld two_q
fsubr six_q                   ; 6-2=4
fistp outd
cmp outd,4
jne failure

fld two_q
fdivr six_q                   ; 6/2=3
fistp outd
cmp outd,3
jne failure

; ---------- register two-operand forms ----------
fld six_q                     ; st1=6
fld two_q                     ; st0=2
fadd st(1),st                 ; st1=6+2=8
fistp outd                    ; pop st0=2 -> outd=2
cmp outd,2
jne failure
fistp outd                    ; 8
cmp outd,8
jne failure

fld six_q
fld two_q
fmul st,st(1)                 ; st0=2*6=12
fistp outd
cmp outd,12
jne failure
fstp st                       ; pop leftover 6

fld six_q                     ; st1=6
fld two_q                     ; st0=2
fsub st(1),st                 ; st1=6-2=4
fstp st                       ; drop st0
fistp outd                    ; 4
cmp outd,4
jne failure

fld six_q
fld two_q
fdivr st(1),st                ; st1 = st0/st1 = 2/6 = 1/3
fstp st                       ; drop st0=2
fistp outd                    ; rint(1/3)=0
cmp outd,0
jne failure

fld six_q
fld two_q
fdiv st(1),st                 ; st1 = st1/st0 = 6/2 = 3
fstp st                       ; drop st0=2
fistp outd
cmp outd,3
jne failure

fld six_q
fld two_q
fdiv st,st(1)                 ; st0 = st0/st1 = 2/6 = 1/3
fistp outd                    ; rint(1/3)=0
cmp outd,0
jne failure
fstp st                       ; drop leftover st1=6

; ---------- popping forms ----------
fld six_q
fld two_q
faddp st(1),st                ; st1=8 pop -> st0=8
fistp outd
cmp outd,8
jne failure

fld two_q
fld six_q
fmulp st(1),st                ; st1=12 pop
fistp outd
cmp outd,12
jne failure

fld six_q
fld two_q
fsubp st(1),st                ; st1=6-2=4 pop
fistp outd
cmp outd,4
jne failure

fld six_q
fld two_q
fdivp st(1),st                ; st1=6/2=3 pop
fistp outd
cmp outd,3
jne failure

; ---------- tbyte load/store ----------
fld tb_1
fstp outtb
cmp dword ptr outtb+4,80000000h
jne failure
cmp word ptr outtb+8,3FFFh
jne failure

fld tbyte ptr tb_10           ; 10.0
fistp outd
cmp outd,10
jne failure

; ---------- fcom + fstsw ax + sahf ----------
fld one_d
fcom two_d                    ; 1 < 2 -> C0 -> CF
fstsw ax
sahf
jae failure

fld two_d
fcom one_d                    ; 2 > 1 -> no flags -> ja
fstsw ax
sahf
jbe failure

fld one_d
fcom one_d                    ; equal -> C3 -> ZF
fstsw ax
sahf
jne failure

fld one_d
fcomp two_d                   ; compare + pop; stack now empty
fstsw ax
sahf
jae failure

fld two_d
fld two_d
fcompp                        ; equal, pop both
fstsw ax
sahf
jne failure

fld two_d
fld one_d
fcom st(1)                    ; st0=1 < st1=2 -> CF
fstsw ax
sahf
jae failure
fcomp                         ; bare fcomp = fcomp st(1): st0=1 < st1=2 -> CF, pop
fstsw ax
sahf
jae failure
fstp st                       ; drop leftover st0=2

fld one_d
fld two_d
fcom                          ; bare fcom = fcom st(1): st0=2 > st1=1 -> no flags
fstsw ax
sahf
jbe failure
fstp st                       ; drop st0
fstp st                       ; drop st1

; ---------- ficom / ficomp ----------
fld one5_d                    ; 1.5
ficom intw                    ; 1.5 > 7? no: below -> CF
fstsw ax
sahf
jb ok_ficom
jmp failure
ok_ficom:

fld four_d
ficomp intw                   ; 4 < 7 -> CF -> jb
fstsw ax
sahf
jae failure

; ---------- ftst ----------
fldz
ftst                          ; 0 == 0 -> C3 -> ZF
fstsw ax
sahf
jne failure

fld1
ftst                          ; 1 > 0 -> clear
fstsw ax
sahf
jbe failure

; ---------- fabs / fchs ----------
fld neg15_d
fabs                          ; 1.5
fstp outd
cmp outd,3FC00000h
jne failure

fld one_d
fchs                          ; -1.0
fistp outw
cmp outw,-1
jne failure

; ---------- fxch ----------
fld one_d                     ; st1=1
fld two_d                     ; st0=2
fxch                          ; st0<->st1 -> st0=1
fistp outw
cmp outw,1
jne failure
fistp outw                    ; st0=2 now
cmp outw,2
jne failure

; ---------- constant loads ----------
fldpi
fstp outq
cmp dword ptr outq+4,400921FBh
jne failure

fldln2
fstp outq
cmp dword ptr outq+4,3FE62E42h
jne failure

fldl2e
fstp outq
cmp dword ptr outq+4,3FF71547h
jne failure

fldl2t
fstp outq
cmp dword ptr outq+4,400A934Fh
jne failure

fldlg2
fstp outq
cmp dword ptr outq+4,3FD34413h
jne failure

; ---------- fsqrt / frndint / fscale ----------
fld four_d                    ; 4.0
fsqrt                         ; 2.0
fistp outw
cmp outw,2
jne failure

fld sixq_d                    ; 6.25
fsqrt                         ; 2.5
fadd half_d                   ; 3.0
fistp outw
cmp outw,3
jne failure

fld one5_d                    ; 1.5
frndint                       ; 2 (to-nearest-even)
fistp outw
cmp outw,2
jne failure

fld neg15_d
frndint                       ; -2
fistp outw
cmp outw,-2
jne failure

fild intd2                    ; 3
fld one5_d                    ; 1.5
fscale                        ; 1.5 * 2^3 = 12
fistp outw
cmp outw,12
jne failure
fstp st                       ; drop leftover 3

; ---------- fprem / fprem1 ----------
fld two_q
fld seven_q
fprem                         ; 7 mod 2 = 1
fistp outw
cmp outw,1
jne failure
fstp st                       ; drop 2

fld two_q
fld seven_q
fprem1                        ; IEEE remainder 7,2 -> -1 (quot 3.5->4 even)
fistp outw
cmp outw,-1
jne failure
fstp st

; ---------- fxtract ----------
fld twelve_q
fxtract                       ; st0=exp(4), st1=sig(0.75)
fistp outw
cmp outw,4
jne failure
fstp outq
cmp dword ptr outq+4,3FE80000h
jne failure

; ---------- f2xm1 ----------
fld1
f2xm1                         ; 2^1-1 = 1
fistp outw
cmp outw,1
jne failure

; ---------- fyl2x ----------
fld two_q                     ; y=2
fld eight_q                   ; x=8
fyl2x                         ; st1 = 2*log2(8) = 6, pop
fistp outw
cmp outw,6
jne failure

; ---------- fptan / fpatan / fsin / fcos / fsincos ----------
fldz
fptan                         ; tan(0)=0, push 1.0
fistp outw                    ; pop the pushed 1.0
cmp outw,1
jne failure
fistp outw                    ; tan(0)=0
cmp outw,0
jne failure

fld1
fld1
fpatan                        ; atan2(1,1)=pi/4
fstp outq
cmp dword ptr outq+4,3FE921FBh
jne failure

fldz
fsin                          ; sin(0)=0
fistp outw
cmp outw,0
jne failure

fldz
fcos                           ; cos(0)=1
fistp outw
cmp outw,1
jne failure

fldz
fsincos                       ; st0=sin(0)=0, push cos(0)=1
fistp outw                    ; cos
cmp outw,1
jne failure
fistp outw                    ; sin
cmp outw,0
jne failure

; ---------- fxam ----------
fldz
fxam                          ; zero -> C3 -> ZF
fstsw ax
sahf
jnz failure

fld1
fxam                          ; normal -> C2 -> PF
fstsw ax
sahf
jnp failure

fld neg2_d
fxam                          ; negative normal -> C2 + C1(sign,sw bit9)
fstsw fsw
test fsw,0600h                ; C1(bit9)|C2(bit10)
jz failure

; ---------- fincstp / fdecstp ----------
fld1
fincstp
fdecstp
fistp outw                    ; still 1.0
cmp outw,1
jne failure

; ---------- fstcw / fldcw + rounding control ----------
fstcw fcw
cmp fcw,037Fh
jne failure

fldcw cw_trunc                ; RC=truncate
fld one5_d                    ; 1.5
frndint                       ; trunc -> 1
fistp outw
cmp outw,1
jne failure

fldcw fcw                     ; restore to-nearest
fld one5_d
frndint                       ; 2
fistp outw
cmp outw,2
jne failure

; ---------- fnstsw to memory ----------
fldz
ftst
fnstsw fsw
mov ax,fsw
sahf
jnz failure

; ---------- fbld / fbstp ----------
fbld tbyte ptr bcd1234        ; 12345678
fistp outd
cmp outd,12345678
jne failure

fild intd2                    ; 3
fimul intw                    ; 21
fbstp tbyte ptr bcdout        ; -> 0x21 packed
mov al,byte ptr bcdout
cmp al,21h
jne failure
cmp byte ptr bcdout+9,0
jne failure

; ---------- fist (no pop) / fistp qword ----------
fild intd
fist outw                     ; 42, no pop
cmp outw,42
jne failure
fstp st                       ; drop

fld six_q
fistp outq                    ; 64-bit fistp = 6
cmp dword ptr outq,6
jne failure
cmp dword ptr outq+4,0
jne failure

; ---------- fucom / fucomp ----------
fld one_d
fucom one_d                   ; equal -> ZF
fstsw ax
sahf
jne failure

fld one_d
fucomp two_d                  ; 1<2 -> CF
fstsw ax
sahf
jae failure

; ---------- fistp rounding (to-nearest-even) ----------
fld half_d                    ; 0.5
fistp outw                    ; -> 0 (tie to even)
cmp outw,0
jne failure

fld two5_d                    ; 2.5
fistp outw                    ; -> 2 (tie to even)
cmp outw,2
jne failure

fnop
fwait
fclex
fnclex
feni
fdisi
fsetpm

MOV al,0
JMP exitLabel
failure:
mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h                       ; DOS INT 21h

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
