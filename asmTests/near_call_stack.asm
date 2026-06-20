.386p

_DATA segment use16 word public 'DATA'
_DATA ends

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT, ds:_DATA

start proc near
    mov ax, _DATA
    mov ds, ax

    push 1234h
    call touch_ax
    mov al, 1
    pop bx
    cmp bx, 1234h
    jne failure

    mov al, 2
    cmp ah, 12h
    jne failure

    xor al, al
failure:
    mov ah, 4ch
    int 21h
start endp

touch_ax proc near
    mov ah, 12h
    ret
touch_ax endp

_TEXT ends

stackseg segment para stack 'STACK'
    db 1000h dup(?)
stackseg ends

end start
