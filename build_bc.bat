set CC=C:\inertia_player\BC5\BIN\BCC.EXE 
set OPT=-1- -d -Os -a16 -v -G -d -w-par -c -mh -M -IC:\inertia_player\BC5\INCLUDE -LC:\inertia_player\BC5\LIB -DDEBUG=3
%CC% %OPT% asm.cpp
rem %CC% %OPT% -S asm.cpp
%CC% %OPT% memmgr.cpp
rem C:\inertia_player\BC5\BIN\CPP.EXE  %OPT% memmgr.cpp
rem C:\inertia_player\BC5\BIN\CPP.EXE  %OPT% %1.cpp
rem %CC% %OPT% -S %1.cpp
copy /y %1.cpp %1_build.cpp
del %1_build.obj %1_build.exe %1_build.asm
%CC% %OPT% -B %1_build.cpp
perl -i -pe "s!^\s*([a-z0-9_@]+)::?!$1::!" %1_build.asm
uasm64 -Fl -Zi3 %1_build.asm
rem ml /c %1_build.asm
copy /y %1_build.obj %1.obj
rem del %1_build.*
C:\inertia_player\BC5\BIN\ulink.exe -vv -s -Tde c0h.obj %1.obj asm.obj memmgr.obj,%1.exe,,gen.lib pdcurses.lib mathh.lib ch.lib