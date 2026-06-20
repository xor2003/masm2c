.386p

DATA segment use16 word public 'DATA'
vga_rgb_data db 768 dup(0)
vga_panel db 240 dup(0)
vga_panel1 db 12h, 23h, 34h, 237 dup(0)
setpaletteflag db 0
DATA ends

_TEXT segment use16 word public 'CODE' ;IGNORE
assume cs:_TEXT,ds:DATA
start proc near

mov ax, DATA
mov ds, ax

mov dx, 3c7h
mov al, 0b0h
out dx, al
mov dx, 3c9h
in al, dx
cmp al, 12h
mov al, 1
jne failure
in al, dx
cmp al, 23h
mov al, 2
jne failure
in al, dx
cmp al, 34h
mov al, 3
jne failure

cmp vga_panel, 12h
mov al, 4
jne failure
cmp vga_panel+1, 23h
mov al, 5
jne failure
cmp vga_panel+2, 34h
mov al, 6
jne failure
mov si, offset vga_rgb_data
add si, 176*3
cmp byte ptr [si], 12h
mov al, 7
jne failure
cmp setpaletteflag, 1
mov al, 8
jne failure

xor al, al
jmp exitLabel

failure:
exitLabel:
mov ah, 4ch
int 21h

start endp
_TEXT ends ;IGNORE

end start ;IGNORE
