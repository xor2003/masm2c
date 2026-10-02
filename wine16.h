/* wine16.h — Win16 API compatibility layer over SDL2 for translated programs.
 *
 * Calling convention (all Win16 APIs are `far pascal`): at fn entry the
 * guest stack holds  [sp]=return ip, [sp+2]=return cs, [sp+4..]=args with
 * the LAST parameter pushed adjacent to the return frame.  Each API
 * emulates `retf N` by `sp += 4 + N` before returning true.
 *
 * 16-bit arg words are read with ARGW(i) (i counts from the last param,
 * i.e. sp+4+2*i); 32-bit args use ARGD(i); far pointers use ARGFP(i)
 * returning (seg<<16)|off.
 */
#ifndef WINE16_H
#define WINE16_H

#include "asm.h"
#include <vector>
#include <cstdint>
#include <string>

struct SDL_Window;
struct SDL_Renderer;
struct SDL_Surface;
union SDL_Event;

namespace w16 {

/* Call a guest far function (WndProc / dialog proc / MakeProcInstance
 * target).  `args` are 16-bit words pushed in declared order (args[0]
 * deepest).  Implemented in zeek16.cpp where __dispatch_call is visible. */
dd call_guest(m2c::_STATE* s, dd fnaddr, const std::vector<dw>& args);

/* SDL side + glue, implemented in zeek16.cpp / wine16.cpp */
void sdl_init();
void sdl_poll(m2c::_STATE* s);          // pump SDL events into msg queue
void sdl_present(m2c::_STATE* s);       // blit main window surface to screen
void sdl_beep();

bool sdl_ok();
extern SDL_Window* win;
extern SDL_Renderer* renderer;
extern int win_w, win_h;

/* Game-provided identity; weak defaults in wine16.cpp.  A translated
 * program overrides them by defining the same symbols (strong). */
extern const char* app_title;   // SDL window title
extern const char* exe_name;    // name reported by GetModuleFileName
extern const char* data_dir;    // fallback dir for guest file opens

/* helpers shared between wine16*.cpp / zeek16.cpp */
dw rd16(const db* p);
dd rd32(const db* p);
void wr16(db* p, dw v);
void wr32(db* p, dd v);
db* fptr(dd p);
const char* fstr(dd p, std::string& out);
void sdl_event_to_msg(m2c::_STATE* s, const SDL_Event& ev);

dw argw(m2c::_STATE* s, int i);
dd argd(m2c::_STATE* s, int i);
dd argfp(m2c::_STATE* s, int i);          // far pointer value seg<<16|off
db* argptr(m2c::_STATE* s, int i);        // host pointer to far arg
const char* argstr(m2c::_STATE* s, int i, std::string& out); // far str -> host
void retw(m2c::_STATE* s, dw v);
void retd(m2c::_STATE* s, dd v);
void retf_args(m2c::_STATE* s, int nbytes);
void log_api(const char* name, const char* fmt = "", ...);

/* resource + window state used by both TUs */
struct W16Win {
    dw hwnd;
    dd wndproc;        // guest far ptr
    std::string cls;
    std::string title;
    int x, y, w, h;
    dw style;
    dw exstyle;
    dw parent;
    dw menu;
    bool visible;
    bool enabled;
    dw userdata[16];   // SetWindowLong/GetWindowLong scratch
    dw winwords[16];   // SetWindowWord scratch
    bool dirty;
    SDL_Surface* surf; // 32bpp backing store
};
extern std::vector<W16Win*> windows;
W16Win* find_hwnd(dw hwnd);
extern dw main_hwnd;

/* expose the guest _STATE for the SDL pump to use for callbacks */
void set_state(m2c::_STATE* s);
m2c::_STATE* state();

/* posted + translated message queue helpers */
void post_msg(dw hwnd, dw msg, dw wp, dd lp);
bool fetch_msg(m2c::_STATE* s, dw hwndfilt, dw lofilt, dw hifilt,
               dw* hwnd, dw* msg, dw* wp, dd* lp);

/* resource loader (NE file) */
void res_init(const char* nepath);
const db* res_find(dd name, dd type, dd* out_len);
extern dd hinstance;

} // namespace w16

#endif
