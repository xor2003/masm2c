.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT

start:
    call readin
    db 41h
    cmp al, 41h
    jne fail

pass:
    mov ax, 4c00h
    int 21h

fail:
    mov ax, 4c01h
    int 21h

readin proc near
    pop si
    mov al, cs:[si]
    inc si
    push si
    ret
readin endp

_TEXT ends

stackseg segment para stack 'STACK'
    db 1000h dup(?)
stackseg ends

end start
