.386p

_DATA segment use16 word public 'DATA'
_DATA ends

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT, ds:_DATA

start:
mov al, 1
or al, al
jnz short $+3
ret
cmp al, 1
jne failure

xor ax, ax
clc
jnc short $+3
inc ax
cmp ax, 0
jne failure

stc
jnc short $+3
inc ax
cmp ax, 1
jne failure

mov al, 0
jmp exitLabel

failure:
mov al, 1

exitLabel:
mov ah, 4ch
int 21h

_TEXT ends

stackseg segment para stack 'STACK'
db 1000h dup(?)
stackseg ends

end start
