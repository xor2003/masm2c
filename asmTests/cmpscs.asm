.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT

start:
    push cs
    pop es
    mov si, offset codeb
    mov di, offset codeb2
    cmpsb cs:[si], es:[di]
    jne fail

pass:
    mov ax, 4c00h
    int 21h

fail:
    mov ax, 4c01h
    int 21h

codeb db 41h
codeb2 db 41h

_TEXT ends

stackseg segment para stack 'STACK'
    db 1000h dup(?)
stackseg ends

end start
