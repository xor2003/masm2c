.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
;start proc near
false_start:
jmp failure

start:
mov eax,2
xor eax,eax
jnz failure

mov eax,511
mov ebx,255
xor eax,ebx
jz failure

mov eax,511
mov ebx,255
xor ax,bx
jz failure

mov eax,511
mov ebx,255
xor al,bl
jnz failure

cmp eax,256
jne failure

mov ecx,0f0ffh
mov ebx,00fffh

xor ch,bh
cmp ecx,0ffffh
jne failure

mov ecx,0df01h
or cl,0f0h
cmp ecx,0dff1h
jne failure

mov eax,1
or eax,eax
jz failure

mov eax,0
or eax,eax
jnz failure

xor eax,eax
JMP exitLabel
failure:
mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h
;start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
