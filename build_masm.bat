del iplay_masm.obj iplay_masm.exe
JWasm.exe -Fl  iplay_masm.asm 
rem wlink  name iplay_nasm.exe system dos file iplay_nasm.obj option verbose
alink -m -oEXE iplay_masm.obj
D:\upx.exe  --ultra-brute iplay_masm.exe
type IPLAY.PCT >> iplay_masm.exe
ren iplay_masm.exe iplay_m.exe
