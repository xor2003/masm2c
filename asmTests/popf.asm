.386p

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near

push 1234h

loc_15c4a: ; POPF
or bh, 0
sub_15c:
push cs
call loc_15c4a+1

pushf
pop ax

CMP ax, 1234h
JNE failure

;mov ax, (ax SHL 4) + dx
;mov ax,cs
;mov dx, offset loc_2
;push dx ; offset
;push ax ; segment
;retf
;loc_2:

MOV al,0
JMP exitLabel
failure:
;mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h
start endp

_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 100h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
