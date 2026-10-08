.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT

first proc near
xor al, al
jz @done
mov al, 1
@done:
ret
first endp

second proc near
xor bl, bl
jz @done
mov bl, 1
@done:
ret
second endp

start:
call first
call second
or al, bl
mov ah, 4ch
int 21h

_TEXT ends

stackseg segment para stack 'STACK'
db 1000h dup(?)
stackseg ends

end start
