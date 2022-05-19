.286

_TEXT   segment use16 public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
@df@@@@9 proc
mylabel3::
ret
@df@@@@9 endp

test2 proc
mylabel1::
jmp mylabel2
test2 endp

test3 proc
jmp mylabel1
test3 endp

test4 proc
test4 endp

mov bp, 34
jmp failure
start proc near

mov ax,_DATA
mov ds,ax

jmp mylabel1
mylabel2::

call mylabel3

mov ax, [cs:jtable+bx]

mov bp,33
jmp @F
jmp failure
@@:
jmp label34
@@:
jmp failure
label34:

mov bp,35
jmp label35
jmp failure
@@:
jmp label351
label35:
jmp @B
label351:

mov bp,32
mov bx,4
jmp near ptr [cs:jtable+bx]
jmp failure
mov bp,30
@df@@@@8:

mov bp,2
mov bx,6
call near ptr [cs:jtable+bx]
jmp next
mov bp,31


next:

mov bp,3
mov ax,-1
test ax,ax
js @df@@@@
@df@@@@:
jns failure

mov bp,4
xor ax,ax
js failure

mov bp,5
mov ax,-1
test ax,ax
jns failure

mov bp,6
mov al,[a]
mov bl,[a+1]
cmp bl,al
ja failure


mov bp,7
mov bl,192
cmp bl,192
jb failure

mov bp,8
cmp bl,193
jnb failure

mov bp,9
mov dx,-1
cmp dx,0
jns failure

mov bp,10
mov dx,1
cmp dx,0
js failure


mov bp,11
mov cx,0ffffh
mov cl,1
or cx,cx
jz failure

mov bp,12
xor cx,cx
jnz failure

mov bp,13
lea si,BBB
mov al,byte ptr [si]
cmp byte ptr [si],1
jb failure

mov bp,14
cmp byte ptr [si],4
ja failure

mov bp,15
mov byte ptr [si],-2
cmp byte ptr [si],1
jb failure  ; // because unsigned comparaison

mov bp,16
mov dx,-1
cmp dx,0
jg failure

mov bp,17
mov dx,5
cmp dx,5
jg failure

mov bp,18
mov ax,5
cmp ax,4
jg @df@@@@1
jmp failure
@df@@@@1:

mov bp,19
mov ax,4
cmp ax,4
jge @df@@@@2
jmp failure
@df@@@@2:

mov bp,20
mov ax,5
cmp ax,4
jge @df@@@@3
jmp failure
@df@@@@3:

mov bp,21
mov dx,-1
cmp dx,0
jge failure

mov bp,22
mov dx,0
cmp dx,-1
jl failure

mov bp,23
mov dx,5
cmp dx,5
jl failure

mov bp,24
mov ax,4
cmp ax,5
jl @df@@@@4
jmp failure
@df@@@@4:

mov bp,25
mov ax,4
cmp ax,4
jle @df@@@@5
jmp failure
@df@@@@5:

mov bp,26
mov ax,4
cmp ax,5
jle @df@@@@6
jmp failure
@df@@@@6:

mov bp,27
mov dx,0
cmp dx,-1
jle failure

mov bp,28
mov cx,-1
jcxz failure

mov bp,29
mov cx,0
jcxz @df@@@@7
jmp failure
@df@@@@7:

mov bp,35
call test35  ; handle call call pop ret

mov bp,36
call test36

mov bp,37
call test37_lbl

good:
MOV al,0
JMP exitLabel
failure::
mov ax,bp
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h

jmp test4

jtable   dw 0
	dw offset failure
  dw @df@@@@8
  dw @df@@@@9


start endp

test35 proc  
call test35_
jmp failure
ret
test35 endp

test35_ proc
pop ax
ret
test35_ endp

test36 proc
jmp test36_lbl
jmp failure
test36 endp

test36_ proc
jmp failure
test36_lbl::
ret
test36_ endp

test37 proc
jmp failure
test37_lbl::
ret
test37 endp

_TEXT   ends ;IGNORE

_DATA   segment use16 public 'DATA' ;IGNORE
a db 0ffh,0dfh,0h
BBB db 2
_DATA   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 100h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
