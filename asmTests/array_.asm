
_DATA   segment use16 word public 'DATA' ;IGNORE
var3 dd 11,-11,2,4000000
_DATA   ends ;IGNORE

_TEXT   segment use16 word public 'CODE' ;IGNORE
start proc near

cmp var3+3*4,4000000
start endp

_TEXT   ends ;IGNORE


end 
