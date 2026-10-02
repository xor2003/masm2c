.386p

_TEXT segment use16 word public 'CODE'
assume cs:_TEXT

main PROC FAR
    jmp worker
    mov ax, 4c01h
    int 21h
main ENDP

worker PROC FAR
    mov ax, 4c00h
    int 21h
worker ENDP

_TEXT ends

stackseg segment para stack 'STACK'
    db 1000h dup(?)
stackseg ends

end main
