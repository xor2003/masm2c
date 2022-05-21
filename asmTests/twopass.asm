
.386p

_DATA   segment use16 word public 'DATA' ;IGNORE
var3 dw var4
var4 dw var3
var5 dw lab1
var6 dw lab2

_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
assume  cs:_TEXT,ds:_DATA

start proc near

lab1:
MOV ax, lab2
MOV ax, var1
MOV ax, var2
MOV ax, var3
MOV ax, var4
MOV ax, lab1
lab2:
mov ax,4c00h
int 21h

start endp


_TEXT   ends ;IGNORE



_DATA2   segment use16 word public 'DATA' ;IGNORE
var1 dw var2
var2 dw var1

_DATA2   ends ;IGNORE

end start ;IGNORE
