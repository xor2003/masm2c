.386p

_DATA segment use16 word public 'DATA'
_DATA ends

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT, ds:_DATA

start proc near
mov ax, _DATA
mov ds, ax

mov al, LOW OFFSET 377O
cmp al, 255
jne failure

mov al, LOW OFFSET 200O
cmp al, 128
jne failure

mov al, LOW OFFSET 377O-200O
cmp al, 127
jne failure

mov al, 0
jmp exitLabel

failure:
mov al, 1

exitLabel:
mov ah, 4ch
int 21h
start endp

_TEXT ends

stackseg segment para stack 'STACK'
db 1000h dup(?)
stackseg ends

end start
