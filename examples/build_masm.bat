del iplay_m.obj iplay_m.exe 
rem JWasm.exe -Fl -Zd -Zi3 iplay_m.asm 
ml.exe /Zi /c /Fl /Sa iplay_m.asm 
rem wlink  name iplay_nasm.exe system dos file iplay_nasm.obj option verbose
rem alink -m -oEXE iplay_m.obj
LINK.EXE /nopackcode /co iplay_m.obj 
rem \upx.exe  --ultra-brute iplay_m.exe
rem type IPLAY.PCT >> iplay_m.exe
rem ren iplay_m.exe iplay_m.exe
