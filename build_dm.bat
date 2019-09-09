set OPT=-mldw -6 -a1 -Ab -cpp -IC:\inertia_player\dm\include -LC:\inertia_player\dm\lib  -DDEBUG=3
set CC=C:\inertia_player\dm\bin\dmc.exe
%CC% asm.cpp  -c %OPT%
%CC% memmgr.cpp -c %OPT%
%CC% %1.cpp -c %OPT%
%CC% %1.o asm.o memmgr.o -o %1 %OPT% pdcurses.lib
rem  -lgdi32 -lcomdlg32