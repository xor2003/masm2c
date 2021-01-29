.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
load_handle dd 0
fileName db 'file1.txt',0
buffer db 64000 dup(0)
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA
start proc near

mov ax,_DATA
mov ds,ax

mov edx,0
mov ecx,2
lea edi,buffer
mov ebx,5

call load_raw
cmp al,0
jne failure

xor eax,eax
cmp dword ptr buffer,'tseT'
mov al, 1
jne failure
mov al,0
JMP exitLabel

failure:
;mov al,1
exitLabel:
mov ah,4ch                    ; AH=4Ch - Exit To DOS
int 21h                       ; DOS INT 21h
start endp

load_raw proc near ; ecx: offset dans le fichier.
                   ; edi: viseur dans donn�es ou ca serra copi� (ax:)
                   ; ebx: nombre de pixels dans le pcx

pushad
push es 
push ds

lea edx,fileName
xor eax,eax
mov al,00h  ;ouverture du fichier pour lecture.
mov ah,03dh
int 21h
jnc noerror
pop ds
pop es
popad
mov al,2
ret
noerror:

mov [load_handle],eax

mov ebx,[load_handle]
mov ah,042h
mov al,00h ;debut du fichier
mov dx,cx
shr ecx,16
int 21h

mov ecx,10

mov ebx,[load_handle]
mov ah,03fh
                   ; edi: viseur dans donn�es ou ca serra copi� (ax:)
push ds
;push fs
;pop  ds
mov edx,edi
int 21h

; to remove
;mov ebx,eax
;jmp failure
;

pop ds

mov ebx,[load_handle]
mov ah,03eh
int 21h

pop ds
pop es
popad
mov al,0
ret
load_raw endp



_TEXT   ends ;IGNORE

stackseg   segment para stack 'STACK' ;IGNORE
db 1000h dup(?)
stackseg   ends ;IGNORE

end start ;IGNORE
