.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
var4 db 1
var1 db 2,5,6
var2 dw 4,6,9
var3 dd 11,-11,2,4000000
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near


sti                             ; Set The Interrupt Flag
cld                             ; Clear The Direction Flag

MOV ax, _data
MOV ds, ax
mov bx,1
mov si,1

mov al,13
cmp var4[2],5
jne failure

mov al,12
cmp var1[1],5
jne failure

mov al,11
cmp var1[bx],5
jne failure

mov al,10
cmp var1[bx+si],6
jne failure

mov al,1
cmp var1,2
jne failure

mov al,2
cmp [var1],2
jne failure

;JMP exitLabel


mov al,3
cmp [var1+1],5
jne failure


mov al,4
cmp [var2],4
jne failure

mov al,5
cmp [var2+2],6
jne failure

mov al,6
cmp [var3],11
jne failure

mov al,7
cmp [var3+3*4],4000000
jne failure

mov al,8
cmp var3+3*4,4000000
jne failure

mov al,9
mov ebp,3*4
cmp ds:[var3+ebp],4000000
jne failure

;mov al,10
;cmp ds:var3+ebp,4000000
;jne failure

MOV al,0
JMP exitLabel
failure:
;mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h                       ; DOS INT 21h
start endp

_TEXT   ends ;IGNORE



stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
