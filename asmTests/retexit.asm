.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT

start:
    call exitpsp

fail:
    mov ax, 4c01h
    int 21h

exitpsp proc near
    mov ax, ds
    push ax
    xor ax, ax
    push ax
    retf
exitpsp endp

_TEXT ends

stackseg segment para stack 'STACK'
    db 1000h dup(?)
stackseg ends

end start
