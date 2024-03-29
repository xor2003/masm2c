.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
var1 db 2,5,6
var2 dw 4,6,9
var3 dd 11,-11,2,4
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA

start proc near

MOV ax, _data
MOV ds, ax

MOV al,1
mov edi,offset var1
mov dl,byte ptr [edi]
cmp dl,2
jne failure

MOV al,2
mov cl,2
mov ds:[edi],cl
mov dl,byte ptr [edi]
cmp dl,2
jne failure

MOV al,3
mov edi,offset var1
mov dl,[edi+1]
cmp dl,5
jne failure

MOV al,4
inc byte ptr [edi+1]
cmp byte ptr [edi+1],6
jne failure


MOV al,5
mov edi,offset var2
mov dl,[edi]
cmp dl,4
jne failure

MOV al,6
lea esi,var2
cmp edi,esi
jne failure

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
