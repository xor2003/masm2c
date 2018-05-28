.386p

_DATA   segment use32 dword public 'DATA' ;IGNORE
var1 db 2,5,6
var2 dw 4,6,9
var3 dd 11,-11,2,4
var4 db 100 dup (1)
_DATA   ends ;IGNORE

_TEXT   segment use32 dword public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
_start proc near

start: ;IGNORE

mov eax,10B
test eax,eax
jz failure

test al,0B
jnz failure

test al,010B
jz failure

mov ebx,0ffff01ffh
test bh,01h
jz failure

test bh,02h
jnz failure
jb failure

mov eax,0
inc eax
dec eax
setnz al
cmp eax,0
jnz failure

mov eax,0
mov ebx,0
inc eax
setnz bh
cmp ebx,100h
jnz failure

mov eax,0
inc eax
dec eax
setz al
cmp eax,1
jnz failure

mov eax,0
mov ebx,0
inc eax
setz bh
cmp ebx,0
jnz failure

clc
mov eax,0
setb al
cmp eax,0
jnz failure

stc
mov eax,0
setb al
cmp eax,1
jnz failure

mov eax,0100b
bt eax,2
jnc failure
bt eax,0
jc failure

mov eax,0100b
btc eax,2
jnc failure
btc eax,0
jc failure
cmp eax,1
jne failure

mov eax,0100b
btr eax,2
jnc failure
btr eax,0
jc failure
cmp eax,0
jne failure

mov eax,0100b
bts eax,2
jnc failure
bts eax,0
jc failure
cmp eax,0101b
jne failure

MOV al,0
JMP exitLabel
failure:
mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h
_start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
