.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT

start:
xor al, al
jp parity_set
mov al, 1
jmp exitLabel

parity_set:
mov al, 0

exitLabel:
mov ah, 4ch
int 21h

_TEXT ends

stackseg segment para stack 'STACK'
db 1000h dup(?)
stackseg ends

end start
