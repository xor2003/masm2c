.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
var1 db 2,5,6
var2 dw 4,6,9
var3 dd 11,-11,2,4
var4 db 100 dup (1)
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near


mov eax,10B
cmp eax,2
jne failure

SHR eax,1
cmp eax,1
jne failure

mov ebx,0ffffffffh
mov bl,011111111B
SHR bl,1

cmp bl,001111111B
jne failure

mov ecx,0ffffffffh
mov ch,011111111B
SHR ch,1
cmp ch,001111111B
jne failure

SHL ch,2
cmp ch,011111100B
jne failure

mov eax,4
sar eax,1
cmp eax,2
jne failure

mov eax,-4
sar eax,1
cmp eax,-2
jne failure

mov eax,-8
sar eax,2
cmp eax,-2
jne failure

mov edx,0abcdef77h
mov eax,012345678h
shrd eax, edx, 8
cmp eax,077123456h
jne failure
cmp edx,0abcdef77h
jne failure


MOV al,0
JMP exitLabel
failure:
mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h
start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
