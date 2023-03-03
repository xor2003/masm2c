.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
var1 dw 4
     db 12
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near

;mov eax, E  TODO implement several passes
;cmp eax,1
;mov al,1
;jne failure
;E = 1

F equ bx
G = byte ptr -2
H equ word ptr 1+2
;I = word + 5 ;TODO
;J equ word + 5 ; word here means 2
;JJ equ dw -5 ; text = "dw -5"
;error JJ = dw -5 ; word here means 2

push seg _DATA
pop ds

;mov ax, word ptr +5 ; result to just 5
;mov ax, word ptr [5] ; [5]
;mov ax, word ptr ds:[5] ; [5]
;mov ax, word ptr [byte]

;mov eax, I
cmp eax, 7
mov al,7
;jne failure

;mov eax, J
cmp eax, 7
mov al,6
;jne failure

BBB = 2
mov eax, BBB
cmp eax,2
mov al,2
jne failure

mov eax, CC
cmp eax,4
mov al,3
jne failure
BBB = 1

call incebx
jne failure

DDD = var1 ; actually it is address of var1
mov ax, DDD
cmp ax, var1
mov al,4
jne failure

MOV al,0
JMP exitLabel
failure::

exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h
start endp

incebx proc near

BBB = 3
mov eax, BBB
cmp eax,3
mov al,5

CC equ 4

ret
inceBX endp


_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?) ;IGNORE
stackseg   ends ;IGNORE

end start ;IGNORE
