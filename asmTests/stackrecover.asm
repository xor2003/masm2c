.386p

_DATA segment use16 word public 'DATA' ;IGNORE
recover_sp dw 0
_DATA ends ;IGNORE

_TEXT segment use16 word public 'CODE' ;IGNORE
assume cs:_TEXT,ds:_DATA

start proc near
    mov ax,seg _DATA
    mov ds,ax

    mov al,1
    mov recover_sp,sp
    call outer

    cmp al,0
    jne failure
    mov ax,4c00h
    int 21h

failure:
    mov ax,4c01h
    int 21h
start endp

outer proc near
    call inner
    mov al,2
    ret
outer_fail:
    xor al,al
    ret
outer endp

inner proc near
    mov sp,recover_sp
    jmp outer_fail
inner endp

_TEXT ends ;IGNORE

stackseg segment para stack 'STACK' ;IGNORE
db 1000h dup(?) ;IGNORE
stackseg ends ;IGNORE

end start ;IGNORE
