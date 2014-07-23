del iplay_tasm.obj iplay_tasm.exe
lzasm /q /la /w2 /c /kh32768 iplay_tasm.asm
rem wlink  name iplay_tasm.exe system dos file iplay_tasm.obj option verbose
alink -m -oEXE iplay_tasm.obj
D:\upx.exe  --ultra-brute iplay_tasm.exe
type IPLAY.PCT >> iplay_tasm.exe
ren iplay_tasm.exe iplay_t.exe

