.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT

target_proc proc near
ret
target_proc endp

start:
mov ax, OFFSET (target_proc-0)
cmp ax, OFFSET target_proc
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
