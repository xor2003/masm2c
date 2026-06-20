.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_TEXT
start proc near

mov ax, _TEXT
mov ds, ax

mov dx, offset existingFile
xor cx, cx
mov ah, 4eh
int 21h
jc fail1
cmp ax, 0
jne fail2

mov dx, offset missingFile
xor cx, cx
mov ah, 4eh
int 21h
jnc fail3
cmp ax, 2
jne fail4

xor al, al
jmp exitLabel

fail1:
mov al, 1
jmp failure
fail2:
mov al, 2
jmp failure
fail3:
mov al, 3
jmp failure
fail4:
mov al, 4

failure:
exitLabel:
mov ah, 4ch
int 21h

existingFile db 'dos_find.asm',0
missingFile db 'missing.zzz',0

start endp
_TEXT   ends ;IGNORE

end start ;IGNORE
