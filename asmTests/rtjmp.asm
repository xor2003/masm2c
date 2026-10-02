.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT

start:
    mov ax, offset pass
    push ax
    ret

fail:
    mov ax, 4c01h
    int 21h

pass:
    mov ax, 4c00h
    int 21h

_TEXT ends

stackseg segment para stack 'STACK'
    db 1000h dup(?)
stackseg ends

end start
