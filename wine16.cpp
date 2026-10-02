/* wine16.cpp — Win16 (Windows 3.x) API layer over SDL2 for translated
 * programs (built with masm2c).
 *
 * Calling convention: every API is `far pascal`.  At fn entry the emulated
 * stack holds [sp]=retip, [sp+2]=retcs, [sp+4..]=args with the LAST declared
 * parameter nearest the frame.  W(i) reads the i-th 16-bit word counting
 * from the top (i=0 is the last param); D(i) reads a dd starting at word i.
 * Each function emulates `retf N` via DONE(N) = sp += 4 + N.
 */
#include "wine16.h"

#include <SDL.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdarg>
#include <cctype>
#include <cmath>
#include <vector>
#include <string>
#include <deque>
#include <algorithm>
#include <map>

extern "C" int DosMemAlloc(uint16_t size, int mode, uint16_t* para, uint16_t* asize);
extern "C" int DosMemFree(uint16_t para);
extern "C" int DosMemChange(uint16_t para, uint16_t size, uint16_t* maxSize);
extern "C" int DosMemLargest(uint16_t* size);

namespace m2c { void asm2C_INT(struct _STATE* state, int a); }

namespace w16 {

__attribute__((weak)) const char* app_title = "masm2c";
__attribute__((weak)) const char* exe_name = "GAME.EXE";
__attribute__((weak)) const char* data_dir = nullptr;

m2c::_STATE* g_state = nullptr;
void set_state(m2c::_STATE* s) { g_state = s; }
m2c::_STATE* state() { return g_state; }

dw argw(m2c::_STATE* s, int i) {
    dw v;
    memcpy(&v, m2c::stack_raddr_(s->ss, (dw)(s->esp + 4 + 2 * i)), 2);
    return v;
}
dd argd(m2c::_STATE* s, int i) {
    dd v;
    memcpy(&v, m2c::stack_raddr_(s->ss, (dw)(s->esp + 4 + 2 * i)), 4);
    return v;
}
dd argfp(m2c::_STATE* s, int i) { return argd(s, i); }
db* fptr(dd p) {
    if (!p) return nullptr;
    return m2c::raddr_((dw)(p >> 16), (dw)(p & 0xffff));
}
db* argptr(m2c::_STATE* s, int i) { return fptr(argd(s, i)); }
const char* fstr(dd p, std::string& out) {
    db* b = fptr(p);
    if (!b) { out.clear(); return ""; }
    const char* q = (const char*)b;
    size_t n = 0;
    while (n < 4096 && q[n]) ++n;
    out.assign(q, n);
    return out.c_str();
}
const char* argstr(m2c::_STATE* s, int i, std::string& out) {
    return fstr(argd(s, i), out);
}
void retw(m2c::_STATE* s, dw v) { s->eax = (s->eax & 0xffff0000) | v; }
void retd(m2c::_STATE* s, dd v) {
    s->eax = (s->eax & 0xffff0000) | (v & 0xffff);
    s->edx = (s->edx & 0xffff0000) | ((v >> 16) & 0xffff);
}
void retf_args(m2c::_STATE* s, int nbytes) {
    /* Emulated retf N: the word at ss:sp is the return ip pushed (and
     * return-marked) by the caller's CALL_. Consume the mark so the strict
     * return verification in CALL_ sees a real consume, then drop
     * ret+cs+args as the hardware would. */
    dw ip;
    memcpy(&ip, m2c::stack_raddr_(s->ss, (dw)s->esp), 2);
    size_t mdepth = m2c::native_return_call_depth;
    size_t mid = 0;
    int mmode = 0;
    m2c::consume_native_return(s, s->ss, (dw)s->esp, (m2c::MWORDSIZE)ip, &mdepth, &mid, &mmode);
    s->esp = (s->esp + 4 + nbytes) & 0xffff;
    m2c::last_ret_popped = 4 + nbytes;
    m2c::last_ret_mark_id = mid;
    m2c::last_ret_mark_mode = mmode;
    m2c::last_ret_site = 0;
}

static FILE* apilog = nullptr;
void log_api(const char* name, const char* fmt, ...) {
    if (!apilog) apilog = fopen("wine16.log", "a");
    if (!apilog) return;
    fprintf(apilog, "%-24s ", name);
    va_list ap;
    va_start(ap, fmt);
    vfprintf(apilog, fmt, ap);
    va_end(ap);
    fputc('\n', apilog);
    fflush(apilog);
}

/* ================= global heap (selector-based) ================= */
/* In protected-mode Windows a locked global block is a real selector
   spanning a full 64KB segment granule: guest code legally addresses any
   16-bit offset through it (the MSC far-heap manager adopts such segments
   wholesale as allocator arenas).  Back every GlobalAlloc block with an
   owned 64KB LDT region so that intra-segment addressing — including the
   generous overhangs the CRT performs — stays inside the block instead of
   stomping neighbours the way a byte-exact MCB arena would. */
static std::map<dw, dd> galloc_sizes;   /* sel -> requested bytes        */

dw galloc(dd bytes) {
    dw sel = m2c::m2c_pm_alloc_paras((dw)((bytes + 15) >> 4));
    if (sel) galloc_sizes[sel] = bytes;
    return sel;
}
void gfree(dw sel) {
    galloc_sizes.erase(sel);
    m2c::m2c_pm_free(sel);
}
db* gptr(dw sel) { return m2c::raddr_(sel, 0); }
dd gsize_of(dw sel) {
    auto it = galloc_sizes.find(sel);
    return it != galloc_sizes.end() ? it->second : 0;
}

/* ================= NE resources ================= */
std::vector<db> ne_image;
struct ResEntry { dw type_id, res_id; dd file_off, len; };
std::vector<ResEntry> g_res;
dd hinstance = 0x100;

dw rd16(const db* p) { return (dw)(p[0] | (p[1] << 8)); }
dd rd32(const db* p) { return (dd)(p[0] | (p[1] << 8) | (p[2] << 16) | (p[3] << 24)); }
void wr16(db* p, dw v) { p[0] = v & 0xff; p[1] = (v >> 8) & 0xff; }
void wr32(db* p, dd v) { p[0] = v & 0xff; p[1] = (v >> 8) & 0xff; p[2] = (v >> 16) & 0xff; p[3] = (v >> 24) & 0xff; }

/* NE resource-name table: offset -> string (for named lookups) */
static std::map<dw, std::string> res_names;

void res_init(const char* path) {
    FILE* f = fopen(path, "rb");
    if (!f) { log_api("RES", "cannot open %s", path); return; }
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    ne_image.resize(sz);
    fread(ne_image.data(), 1, sz, f);
    fclose(f);
    const db* img = ne_image.data();
    dd neoff = rd32(img + 0x3c);
    const db* ne = img + neoff;
    dw restab_off = rd16(ne + 0x24);
    dw resnames_off = rd16(ne + 0x26); // offset of resident-name table (from NE)
    dw modref = rd16(ne + 0x28);
    dw impnames = rd16(ne + 0x2a);
    dw nonres = rd16(ne + 0x2c);
    dw align_shift = rd16(ne + 0x32);
    if (!align_shift) align_shift = 4;
    const db* rt = ne + restab_off;
    rd16(rt);
    const db* ti = rt + 2;
    // resource table ends where the name table begins (relative to NE start)
    const db* names_end = ne + resnames_off;
    if (names_end <= rt) names_end = ne + modref;
    while (ti < names_end) {
        dw type_id = rd16(ti);
        if (type_id == 0) break;
        dw count = rd16(ti + 2);
        const db* ri = ti + 8;
        for (int i = 0; i < count; ++i, ri += 12) {
            ResEntry e{};
            e.type_id = type_id;
            dd off_units = rd16(ri);
            dd len_units = rd16(ri + 2);
            e.file_off = off_units << align_shift;
            e.len = len_units ? (len_units << align_shift) : 0;
            e.res_id = rd16(ri + 6);
            g_res.push_back(e);
        }
        ti += 8 + count * 12;
    }
    // Embedded resource name table: [len][chars][ordinal] records right
    // after the typeinfo terminator. rnName/rnType name references stored
    // in resource records are offsets relative to the resource table base.
    {
        const db* lim = ne_image.data() + ne_image.size();
        const db* n = ti + 2;
        while (n < lim) {
            dw l = *n;
            if (!l || n + 1 + l + 2 > lim) break;
            std::string nm((const char*)n + 1, l);
            res_names[(dw)(n - rt)] = nm;
            n += 1 + l + 2;
        }
    }
    log_api("RES", "%zu resources, %zu names", g_res.size(), res_names.size());
    (void)impnames; (void)nonres;
}

/* resolve a guest far-ptr (or ordinal) resource id to ordinal or string */
struct ResKey { bool is_ord; dw ord; std::string nm; };
static bool reskey(dd v, ResKey& k) {
    if ((v >> 16) == 0 || ((v & 0xffff) < 0x100 && (v >> 16) == 0)) {
        // In Win16 an integer id is stored as seg=0, off=id — BUT the guest
        // passes MAKEINTRESOURCE(id) = 0:id i.e. dword == id.
        if (v <= 0xffff) { k.is_ord = true; k.ord = v & 0xffff; return true; }
        // sometimes passed as 0001:xxxx? treat hi-word==0 only
        k.is_ord = true; k.ord = v & 0xffff;
        return true;
    }
    std::string s;
    fstr(v, s);
    k.is_ord = false; k.nm = s;
    return true;
}

static bool res_stored_match(dw raw, const ResKey& k, bool is_type) {
    if (raw & 0x8000)
        return k.is_ord && (raw & 0x7fff) == k.ord;
    if (k.is_ord) return false;
    // named resource: raw = offset of name in name table
    auto it = res_names.find(raw);
    if (it == res_names.end()) return false;
    std::string a = it->second, b = k.nm;
    for (auto& c : a) c = toupper(c);
    for (auto& c : b) c = toupper(c);
    return a == b;
    (void)is_type;
}

const db* res_find_data(dd name, dd type, dd* out_len) {
    ResKey nk, tk;
    reskey(name, nk);
    reskey(type, tk);
    for (auto& e : g_res) {
        if (!res_stored_match(e.type_id, tk, true)) continue;
        if (!res_stored_match(e.res_id, nk, false)) continue;
        *out_len = e.len;
        return ne_image.data() + e.file_off;
    }
    return nullptr;
}

/* ================= windows / messages ================= */
std::vector<W16Win*> windows;
dw main_hwnd = 0;
dw g_next_hwnd = 1;

struct Msg { dw hwnd, msg, wp; dd lp; };
std::deque<Msg> msgq;
bool quit_posted = false;
int quit_code = 0;

struct Timer { dw hwnd; dw id; dd cb; uint32_t period; uint32_t next; };
std::vector<Timer> timers;
dw g_focus = 0, g_capture = 0;

W16Win* find_hwnd(dw hwnd) {
    for (auto* w : windows) if (w->hwnd == hwnd) return w;
    return nullptr;
}

void post_msg(dw hwnd, dw msg, dw wp, dd lp) { msgq.push_back({hwnd, msg, wp, lp}); }

static void win_abs_pos(W16Win* w, int* ox, int* oy);
static W16Win* hit_test(int x, int y);

void sdl_event_to_msg(m2c::_STATE*, const SDL_Event& ev) {
    switch (ev.type) {
    case SDL_QUIT:
        post_msg(main_hwnd, 0x0010, 0, 0);
        break;
    case SDL_KEYDOWN: case SDL_KEYUP: {
        dw vk = 0;
        SDL_Keycode k = ev.key.keysym.sym;
        if (k >= SDLK_a && k <= SDLK_z) vk = 'A' + (k - SDLK_a);
        else if (k >= SDLK_0 && k <= SDLK_9) vk = '0' + (k - SDLK_0);
        else switch (k) {
        case SDLK_LEFT: vk = 0x25; break; case SDLK_RIGHT: vk = 0x27; break;
        case SDLK_UP: vk = 0x26; break; case SDLK_DOWN: vk = 0x28; break;
        case SDLK_SPACE: vk = 0x20; break; case SDLK_RETURN: vk = 0x0d; break;
        case SDLK_ESCAPE: vk = 0x1b; break; case SDLK_BACKSPACE: vk = 0x08; break;
        case SDLK_TAB: vk = 0x09; break; case SDLK_DELETE: vk = 0x2e; break;
        case SDLK_INSERT: vk = 0x2d; break; case SDLK_HOME: vk = 0x24; break;
        case SDLK_END: vk = 0x23; break; case SDLK_PAGEUP: vk = 0x21; break;
        case SDLK_PAGEDOWN: vk = 0x22; break;
        case SDLK_LSHIFT: case SDLK_RSHIFT: vk = 0x10; break;
        case SDLK_LCTRL: case SDLK_RCTRL: vk = 0x11; break;
        case SDLK_LALT: case SDLK_RALT: vk = 0x12; break;
        case SDLK_F1: vk = 0x70; break; case SDLK_F2: vk = 0x71; break;
        case SDLK_F3: vk = 0x72; break; case SDLK_F4: vk = 0x73; break;
        case SDLK_F5: vk = 0x74; break; case SDLK_F6: vk = 0x75; break;
        case SDLK_F7: vk = 0x76; break; case SDLK_F8: vk = 0x77; break;
        case SDLK_F9: vk = 0x78; break; case SDLK_F10: vk = 0x79; break;
        case SDLK_F11: vk = 0x7a; break; case SDLK_F12: vk = 0x7b; break;
        default: break;
        }
        if (!vk) break;
        dw hwnd = g_focus ? g_focus : main_hwnd;
        /* guest code reads the PC/XT (set-1) scancode out of lParam[23:16];
           SDL scancodes are HID-style and differ, so translate. */
        dw xt = 0;
        switch (ev.key.keysym.scancode) {
        case SDL_SCANCODE_ESCAPE: xt = 0x01; break;
        case SDL_SCANCODE_1: xt = 0x02; break; case SDL_SCANCODE_2: xt = 0x03; break;
        case SDL_SCANCODE_3: xt = 0x04; break; case SDL_SCANCODE_4: xt = 0x05; break;
        case SDL_SCANCODE_5: xt = 0x06; break; case SDL_SCANCODE_6: xt = 0x07; break;
        case SDL_SCANCODE_7: xt = 0x08; break; case SDL_SCANCODE_8: xt = 0x09; break;
        case SDL_SCANCODE_9: xt = 0x0a; break; case SDL_SCANCODE_0: xt = 0x0b; break;
        case SDL_SCANCODE_BACKSPACE: xt = 0x0e; break; case SDL_SCANCODE_TAB: xt = 0x0f; break;
        case SDL_SCANCODE_Q: xt = 0x10; break; case SDL_SCANCODE_W: xt = 0x11; break;
        case SDL_SCANCODE_E: xt = 0x12; break; case SDL_SCANCODE_R: xt = 0x13; break;
        case SDL_SCANCODE_T: xt = 0x14; break; case SDL_SCANCODE_Y: xt = 0x15; break;
        case SDL_SCANCODE_U: xt = 0x16; break; case SDL_SCANCODE_I: xt = 0x17; break;
        case SDL_SCANCODE_O: xt = 0x18; break; case SDL_SCANCODE_P: xt = 0x19; break;
        case SDL_SCANCODE_RETURN: xt = 0x1c; break; case SDL_SCANCODE_LCTRL: xt = 0x1d; break;
        case SDL_SCANCODE_A: xt = 0x1e; break; case SDL_SCANCODE_S: xt = 0x1f; break;
        case SDL_SCANCODE_D: xt = 0x20; break; case SDL_SCANCODE_F: xt = 0x21; break;
        case SDL_SCANCODE_G: xt = 0x22; break; case SDL_SCANCODE_H: xt = 0x23; break;
        case SDL_SCANCODE_J: xt = 0x24; break; case SDL_SCANCODE_K: xt = 0x25; break;
        case SDL_SCANCODE_L: xt = 0x26; break;
        case SDL_SCANCODE_Z: xt = 0x2c; break; case SDL_SCANCODE_X: xt = 0x2d; break;
        case SDL_SCANCODE_C: xt = 0x2e; break; case SDL_SCANCODE_V: xt = 0x2f; break;
        case SDL_SCANCODE_B: xt = 0x30; break; case SDL_SCANCODE_N: xt = 0x31; break;
        case SDL_SCANCODE_M: xt = 0x32; break;
        case SDL_SCANCODE_LSHIFT: xt = 0x2a; break; case SDL_SCANCODE_RSHIFT: xt = 0x36; break;
        case SDL_SCANCODE_LALT: xt = 0x38; break; case SDL_SCANCODE_SPACE: xt = 0x39; break;
        case SDL_SCANCODE_F1: xt = 0x3b; break; case SDL_SCANCODE_F2: xt = 0x3c; break;
        case SDL_SCANCODE_F3: xt = 0x3d; break; case SDL_SCANCODE_F4: xt = 0x3e; break;
        case SDL_SCANCODE_F5: xt = 0x3f; break; case SDL_SCANCODE_F6: xt = 0x40; break;
        case SDL_SCANCODE_F7: xt = 0x41; break; case SDL_SCANCODE_F8: xt = 0x42; break;
        case SDL_SCANCODE_F9: xt = 0x43; break; case SDL_SCANCODE_F10: xt = 0x44; break;
        case SDL_SCANCODE_F11: xt = 0x57; break; case SDL_SCANCODE_F12: xt = 0x58; break;
        case SDL_SCANCODE_HOME: xt = 0x47; break; case SDL_SCANCODE_UP: xt = 0x48; break;
        case SDL_SCANCODE_PAGEUP: xt = 0x49; break; case SDL_SCANCODE_LEFT: xt = 0x4b; break;
        case SDL_SCANCODE_RIGHT: xt = 0x4d; break; case SDL_SCANCODE_END: xt = 0x4f; break;
        case SDL_SCANCODE_DOWN: xt = 0x50; break; case SDL_SCANCODE_PAGEDOWN: xt = 0x51; break;
        case SDL_SCANCODE_INSERT: xt = 0x52; break; case SDL_SCANCODE_DELETE: xt = 0x53; break;
        default: xt = (dw)ev.key.keysym.scancode & 0x7f; break;
        }
        dd lp = ((dd)xt << 16) | 1;
        if (ev.type == SDL_KEYUP) lp |= 0xC0000000u;
        post_msg(hwnd, ev.type == SDL_KEYDOWN ? 0x0100 : 0x0101, vk, lp);
        if (ev.type == SDL_KEYDOWN && k >= 32 && k < 127)
            post_msg(hwnd, 0x0102, (dw)k, lp);
        break;
    }
    case SDL_MOUSEBUTTONDOWN: case SDL_MOUSEBUTTONUP: {
        dw msg = 0;
        bool down = ev.type == SDL_MOUSEBUTTONDOWN;
        switch (ev.button.button) {
        case SDL_BUTTON_LEFT:   msg = down ? 0x0201 : 0x0202; break;
        case SDL_BUTTON_MIDDLE: msg = down ? 0x0207 : 0x0208; break;
        case SDL_BUTTON_RIGHT:  msg = down ? 0x0204 : 0x0205; break;
        }
        if (!msg) break;
        /* Windows dispatches mouse input to the window under the cursor:
         * hit-test the visible window tree (topmost = latest creation)
         * rather than always the main window.  A real click also assigns
         * keyboard focus, so later keys reach the clicked window. */
        int mx = ev.button.x, my = ev.button.y;
        W16Win* hit = nullptr;
        if (!g_capture) hit = hit_test(mx, my);
        dw target = g_capture ? g_capture
                              : (hit ? hit->hwnd : main_hwnd);
        if (down && hit) g_focus = hit->hwnd;
        /* Convert screen coords to the target's client coordinates. */
        int rx = mx, ry = my;
        if (W16Win* t = find_hwnd(target)) {
            int tx, ty;
            win_abs_pos(t, &tx, &ty);
            rx -= tx; ry -= ty;
        }
        dd lp = ((dd)(dw)ry << 16) | (dw)rx;
        post_msg(target, msg, 0, lp);
        break;
    }
    case SDL_MOUSEMOTION: {
        dd lp = ((dd)(dw)ev.motion.y << 16) | (dw)ev.motion.x;
        post_msg(g_capture ? g_capture : main_hwnd, 0x0200, 0, lp);
        break;
    }
    }
}

bool fetch_msg(m2c::_STATE* s, dw hwndfilt, dw lofilt, dw hifilt,
               dw* hwnd, dw* msg, dw* wp, dd* lp) {
    for (;;) {
        uint32_t now = SDL_GetTicks();
        for (auto& t : timers) {
            if ((int32_t)(now - t.next) >= 0) {
                t.next = now + (t.period ? t.period : 1);
                if (t.cb) call_guest(s, t.cb, {t.hwnd, 0x0113, t.id, (dw)now});
                else post_msg(t.hwnd, 0x0113, t.id, 0);
            }
        }
        for (auto it = msgq.begin(); it != msgq.end(); ++it) {
            if (hwndfilt && it->hwnd && it->hwnd != hwndfilt) continue;
            if (it->msg < lofilt || (hifilt && it->msg > hifilt)) continue;
            *hwnd = it->hwnd; *msg = it->msg; *wp = it->wp; *lp = it->lp;
            msgq.erase(it);
            return *msg != 0x0012;
        }
        if (quit_posted) {
            *hwnd = 0; *msg = 0x0012; *wp = quit_code; *lp = 0;
            quit_posted = false;
            return false;
        }
        SDL_Event ev;
        bool had = false;
        while (SDL_PollEvent(&ev)) { had = true; sdl_event_to_msg(s, ev); }
        for (auto* w : windows)
            if (w->dirty && w->visible) { w->dirty = false; post_msg(w->hwnd, 0x000f, 0, 0); }
        if (msgq.empty()) {
            sdl_present(s);
            if (!had) SDL_Delay(2);
        }
    }
}

/* ================= GDI objects ================= */
struct GdiObj {
    dw handle = 0;
    int kind = 0;                 // 1 pen, 2 brush, 3 font, 4 bitmap, 5 region, 6 palette
    int pen_style = 0; dd pen_color = 0; int pen_w = 1;
    int brush_style = 0; dd brush_color = 0; int brush_hatch = 0;
    int font_h = 0;
    int bw = 0, bh = 0, bbpp = 0, stride = 0;
    std::vector<db> bits;
    std::vector<dd> palette;
    SDL_Surface* surf = nullptr;  // created on demand for bitmaps
};
std::vector<GdiObj*> gobjs;
dw g_next_obj = 0x300;
GdiObj* find_obj(dw h) { for (auto* o : gobjs) if (o->handle == h) return o; return nullptr; }
GdiObj* new_obj(int kind) {
    GdiObj* o = new GdiObj();
    o->handle = g_next_obj++;
    o->kind = kind;
    gobjs.push_back(o);
    return o;
}

struct DC {
    dw handle = 0;
    W16Win* win = nullptr;
    SDL_Surface* surf = nullptr;
    GdiObj* mem = nullptr;
    int mapmode = 1;
    dd textcolor = 0, bkcolor = 0xffffff;
    int bkmode = 2, rop2 = 13;
    dw pen = 0, brush = 0, font = 0, bitmap = 0;
    int curx = 0, cury = 0;
    int worgx = 0, worgy = 0, wextx = 0, wexty = 0;
    int vorgx = 0, vorgy = 0, vextx = 0, vexty = 0;
    dw selbitmap = 0;
    dd brush_org = 0;
};
std::vector<DC*> dcs;
dw g_next_dc = 0x800;
DC* find_dc(dw h) { for (auto* d : dcs) if (d->handle == h) return d; return nullptr; }
DC* make_dc(W16Win* w, SDL_Surface* surf, GdiObj* mem) {
    DC* d = new DC();
    d->handle = g_next_dc++;
    d->win = w; d->surf = surf; d->mem = mem;
    dcs.push_back(d);
    return d;
}

void dc_pt(DC* d, int x, int y, int* px, int* py) {
    if (d->mapmode == 1 || !d->wextx || !d->vextx) {
        *px = x - d->worgx + d->vorgx;
        *py = y - d->worgy + d->vorgy;
        return;
    }
    double sx = (double)d->vextx / d->wextx;
    double sy = (double)d->vexty / d->wexty;
    *px = (int)((x - d->worgx) * sx) + d->vorgx;
    *py = (int)((y - d->worgy) * sy) + d->vorgy;
}

void surf_px(SDL_Surface* s, int x, int y, dd rgb) {
    if (!s) return;
    if (x < 0 || y < 0 || x >= s->w || y >= s->h) return;
    db* p = (db*)s->pixels + y * s->pitch + x * 4;
    p[0] = rgb & 0xff; p[1] = (rgb >> 8) & 0xff; p[2] = (rgb >> 16) & 0xff; p[3] = 0xff;
}
dd surf_get(SDL_Surface* s, int x, int y) {
    if (!s) return 0;
    if (x < 0 || y < 0 || x >= s->w || y >= s->h) return 0;
    db* p = (db*)s->pixels + y * s->pitch + x * 4;
    return p[0] | (p[1] << 8) | (p[2] << 16);
}
void surf_fill(SDL_Surface* s, int x, int y, int w, int h, dd rgb) {
    if (!s) return;
    SDL_Rect r{x, y, w, h};
    SDL_FillRect(s, &r, SDL_MapRGB(s->format, rgb & 0xff, (rgb >> 8) & 0xff, (rgb >> 16) & 0xff));
}
void surf_line(SDL_Surface* s, int x0, int y0, int x1, int y1, dd rgb, int wid) {
    if (!s) return;
    int dx = abs(x1 - x0), dy = -abs(y1 - y0);
    int sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    int err = dx + dy;
    if (wid < 1) wid = 1;
    for (;;) {
        for (int ox = 0; ox < wid; ++ox)
            for (int oy = 0; oy < wid; ++oy)
                surf_px(s, x0 + ox, y0 + oy, rgb);
        if (x0 == x1 && y0 == y1) break;
        int e2 = 2 * err;
        if (e2 >= dy) { err += dy; x0 += sx; }
        if (e2 <= dx) { err += dx; y0 += sy; }
    }
}

dd rop_apply(dd rop, dd src, dd dst, dd pat) {
    switch (rop & 0xffffff) {
    case 0x000042: return 0;
    case 0xff0062: return 0xffffff;
    case 0x330032: return ~src & 0xffffff;
    case 0x550009: return ~dst & 0xffffff;
    case 0x660046: return src ^ dst;
    case 0x8800c6: return src & dst;
    case 0xbb0226: return ~src | dst;
    case 0xcc0020: return src;
    case 0xee0086: return src | dst;
    case 0xf00021: return pat;
    case 0x5a0049: return pat ^ dst;
    case 0xaf0229: return pat | ~dst;
    default: return src;
    }
}

/* object bitmap -> 32bpp SDL surface (cached) */
SDL_Surface* obj_surf(GdiObj* o) {
    if (!o || o->kind != 4 || o->bits.empty()) return nullptr;
    if (o->surf) return o->surf;
    SDL_Surface* s = SDL_CreateRGBSurfaceWithFormat(0, o->bw, o->bh, 32, SDL_PIXELFORMAT_BGRA32);
    for (int y = 0; y < o->bh; ++y)
        for (int x = 0; x < o->bw; ++x) {
            dd rgb = 0;
            if (o->bbpp == 8) {
                int idx = o->bits[y * o->stride + x];
                rgb = idx < (int)o->palette.size() ? o->palette[idx] : 0;
            } else if (o->bbpp == 4) {
                int byte = o->bits[y * o->stride + (x >> 1)];
                int idx = (x & 1) ? (byte & 0xf) : (byte >> 4);
                rgb = idx < (int)o->palette.size() ? o->palette[idx] : 0;
            } else if (o->bbpp == 1) {
                int byte = o->bits[y * o->stride + (x >> 3)];
                int idx = (byte >> (7 - (x & 7))) & 1;
                rgb = idx < (int)o->palette.size() ? o->palette[idx]
                                                   : (idx ? 0xffffff : 0);
            } else if (o->bbpp == 24) {
                const db* q = &o->bits[y * o->stride + x * 3];
                rgb = q[0] | (q[1] << 8) | (q[2] << 16);
            } else if (o->bbpp == 32) {
                const db* q = &o->bits[y * o->stride + x * 4];
                rgb = q[0] | (q[1] << 8) | (q[2] << 16);
            }
            surf_px(s, x, o->bh - 1 - y, rgb);   // bottom-up DIB
        }
    o->surf = s;
    return s;
}

/* blit DIB bits (any bpp) into DC surface with scaling + rop */
void dib_blit(DC* d, int dx, int dy, int dw_, int dh_,
              const db* bits, int bw, int bh, int bbpp,
              const std::vector<dd>& pal, int sx, int sy, int sw, int sh,
              dd rop, bool topdown) {
    if (!d || !d->surf || !bits) return;
    int stride = bbpp == 1 ? ((bw + 31) / 32) * 4
               : bbpp == 4 ? ((bw + 7) / 8) * 4
               : bbpp == 8 ? ((bw + 3) / 4) * 4
               : bbpp == 24 ? ((bw * 3 + 3) / 4) * 4 : bw * 4;
    for (int y = 0; y < dh_; ++y) {
        int syy = sy + (int)((long long)y * sh / dh_);
        int rowi = topdown ? syy : (bh - 1 - syy);
        if (rowi < 0 || rowi >= bh) continue;
        for (int x = 0; x < dw_; ++x) {
            int sxi = sx + (int)((long long)x * sw / dw_);
            if (sxi < 0 || sxi >= bw) continue;
            dd rgb = 0;
            const db* row = &bits[rowi * stride];
            if (bbpp == 8) {
                int idx = row[sxi];
                rgb = idx < (int)pal.size() ? pal[idx] : 0;
            } else if (bbpp == 4) {
                int byte = row[sxi >> 1];
                int idx = (sxi & 1) ? (byte & 0xf) : (byte >> 4);
                rgb = idx < (int)pal.size() ? pal[idx] : 0;
            } else if (bbpp == 1) {
                int byte = row[sxi >> 3];
                rgb = ((byte >> (7 - (sxi & 7))) & 1) ? 0xffffff : 0;
            } else if (bbpp == 24) {
                const db* q = &row[sxi * 3];
                rgb = q[0] | (q[1] << 8) | (q[2] << 16);
            } else if (bbpp == 32) {
                const db* q = &row[sxi * 4];
                rgb = q[0] | (q[1] << 8) | (q[2] << 16);
            }
            int px, py;
            dc_pt(d, dx + x, dy + y, &px, &py);
            dd cur = surf_get(d->surf, px, py);
            surf_px(d->surf, px, py, rop_apply(rop, rgb, cur, d->bkcolor));
        }
    }
}

/* blit surface->surface with rop */
void surf_blit(SDL_Surface* dst, int dx, int dy, int dw_, int dh_,
               SDL_Surface* src, int sx, int sy, int sw, int sh, dd rop, dd pat) {
    if (!dst || !src) return;
    for (int y = 0; y < dh_; ++y) {
        int syy = sy + (int)((long long)y * sh / dh_);
        for (int x = 0; x < dw_; ++x) {
            int sxi = sx + (int)((long long)x * sw / dw_);
            dd s_ = surf_get(src, sxi, syy);
            dd d_ = surf_get(dst, dx + x, dy + y);
            surf_px(dst, dx + x, dy + y, rop_apply(rop, s_, d_, pat));
        }
    }
}

bool parse_bmi(const db* p, int* w, int* h, int* bpp,
               std::vector<dd>* pal, const db** bits, int* stride) {
    dd hdrsize = rd32(p);
    int nw = 0, nh = 0, nbpp = 1, nclr = 0, ncomp = 0;
    if (hdrsize == 12) {
        nw = rd16(p + 4); nh = rd16(p + 6); nbpp = rd16(p + 10);
        if (nbpp <= 8) nclr = 1 << nbpp;
        if (nclr)
            for (int i = 0; i < nclr; ++i)
                pal->push_back(p[12 + i * 3] | (p[12 + i * 3 + 1] << 8) | (p[12 + i * 3 + 2] << 16));
        *bits = p + 12 + nclr * 3;
    } else {
        nw = (int)rd32(p + 4); nh = (int)rd32(p + 8);
        nbpp = rd16(p + 14);
        ncomp = rd32(p + 16);
        nclr = rd32(p + 32);
        if (!nclr && nbpp <= 8) nclr = 1 << nbpp;
        if (nclr)
            for (int i = 0; i < nclr; ++i)
                pal->push_back(p[40 + i * 4] | (p[40 + i * 4 + 1] << 8) | (p[40 + i * 4 + 2] << 16));
        *bits = p + hdrsize + nclr * 4;
    }
    if (nh < 0) nh = -nh;
    *w = nw; *h = nh; *bpp = nbpp;
    *stride = nbpp == 1 ? ((nw + 31) / 32) * 4
            : nbpp == 4 ? ((nw + 7) / 8) * 4
            : nbpp == 8 ? ((nw + 3) / 4) * 4
            : nbpp == 24 ? ((nw * 3 + 3) / 4) * 4 : nw * 4;
    (void)ncomp;
    return true;
}

GdiObj* load_bitmap_res(dd resid) {
    dd len = 0;
    const db* data = res_find_data(resid, 2, &len);   // RT_BITMAP = 2
    if (!data || len < 12) return nullptr;
    int w, h, bpp, stride;
    std::vector<dd> pal;
    const db* bits = nullptr;
    if (!parse_bmi(data, &w, &h, &bpp, &pal, &bits, &stride)) return nullptr;
    GdiObj* o = new_obj(4);
    o->bw = w; o->bh = h; o->bbpp = bpp; o->palette = pal; o->stride = stride;
    size_t need = (size_t)stride * h;
    if (bits + need > data + len)
        need = data + len > bits ? (size_t)(data + len - bits) : 0;
    o->bits.assign(bits, bits + need);
    return o;
}

/* crude 5x7 font — enough for TextOut diagnostics */
void draw_text(SDL_Surface* s, int x, int y, const char* txt, int len, dd fg) {
    if (!s) return;
    // simple 5x7 uppercase-ish font
    static const uint8_t gl[96][7] = {
        {0}, {0x04,0x04,0x04,0x04,0,0,0x04}, {0x0a,0x0a,0,0,0,0,0},
        {0x0a,0x1f,0x0a,0x0a,0x1f,0x0a,0}, {0x04,0x0f,0x14,0x0e,0x05,0x1e,0x04},
        {0x18,0x19,0x02,0x04,0x08,0x13,0x03}, {0x0c,0x12,0x14,0x08,0x15,0x12,0x0d},
        {0x04,0x04,0,0,0,0,0}, {0x02,0x04,0x08,0x08,0x08,0x04,0x02},
        {0x08,0x04,0x02,0x02,0x02,0x04,0x08}, {0,0x04,0x15,0x0e,0x15,0x04,0},
        {0,0x04,0x04,0x1f,0x04,0x04,0}, {0,0,0,0,0x04,0x04,0x08},
        {0,0,0,0x1f,0,0,0}, {0,0,0,0,0,0x0c,0x0c}, {0x01,0x02,0x04,0x08,0x10,0,0},
        {0x0e,0x11,0x13,0x15,0x19,0x11,0x0e}, {0x04,0x0c,0x04,0x04,0x04,0x04,0x0e},
        {0x0e,0x11,0x01,0x06,0x08,0x10,0x1f}, {0x0e,0x11,0x01,0x06,0x01,0x11,0x0e},
        {0x02,0x06,0x0a,0x12,0x1f,0x02,0x02}, {0x1f,0x10,0x1e,0x01,0x01,0x11,0x0e},
        {0x06,0x08,0x10,0x1e,0x11,0x11,0x0e}, {0x1f,0x01,0x02,0x04,0x08,0x08,0x08},
        {0x0e,0x11,0x11,0x0e,0x11,0x11,0x0e}, {0x0e,0x11,0x11,0x0f,0x01,0x02,0x0c},
        {0,0x0c,0x0c,0,0x0c,0x0c,0}, {0,0x0c,0x0c,0,0x0c,0x04,0x08},
        {0x02,0x04,0x08,0x10,0x08,0x04,0x02}, {0,0,0x1f,0,0x1f,0,0},
        {0x08,0x04,0x02,0x01,0x02,0x04,0x08}, {0x0e,0x11,0x01,0x06,0x04,0,0x04},
        {0x0e,0x11,0x01,0x0d,0x15,0x15,0x0e}, {0x0e,0x11,0x11,0x1f,0x11,0x11,0x11},
        {0x1e,0x11,0x11,0x1e,0x11,0x11,0x1e}, {0x0e,0x11,0x10,0x10,0x10,0x11,0x0e},
        {0x1e,0x11,0x11,0x11,0x11,0x11,0x1e}, {0x1f,0x10,0x10,0x1e,0x10,0x10,0x1f},
        {0x1f,0x10,0x10,0x1e,0x10,0x10,0x10}, {0x0e,0x11,0x10,0x17,0x11,0x11,0x0f},
        {0x11,0x11,0x11,0x1f,0x11,0x11,0x11}, {0x0e,0x04,0x04,0x04,0x04,0x04,0x0e},
        {0x07,0x02,0x02,0x02,0x02,0x12,0x0c}, {0x11,0x12,0x14,0x18,0x14,0x12,0x11},
        {0x10,0x10,0x10,0x10,0x10,0x10,0x1f}, {0x11,0x1b,0x15,0x15,0x11,0x11,0x11},
        {0x11,0x19,0x15,0x13,0x11,0x11,0x11}, {0x0e,0x11,0x11,0x11,0x11,0x11,0x0e},
        {0x1e,0x11,0x11,0x1e,0x10,0x10,0x10}, {0x0e,0x11,0x11,0x11,0x15,0x12,0x0d},
        {0x1e,0x11,0x11,0x1e,0x14,0x12,0x11}, {0x0f,0x10,0x10,0x0e,0x01,0x01,0x1e},
        {0x1f,0x04,0x04,0x04,0x04,0x04,0x04}, {0x11,0x11,0x11,0x11,0x11,0x11,0x0e},
        {0x11,0x11,0x11,0x11,0x11,0x0a,0x04}, {0x11,0x11,0x11,0x15,0x15,0x1b,0x11},
        {0x11,0x11,0x0a,0x04,0x0a,0x11,0x11}, {0x11,0x11,0x0a,0x04,0x04,0x04,0x04},
        {0x1f,0x01,0x02,0x04,0x08,0x10,0x1f}, {0x0e,0x08,0x08,0x08,0x08,0x08,0x0e},
        {0x10,0x08,0x04,0x02,0x01,0,0}, {0x0e,0x02,0x02,0x02,0x02,0x02,0x0e},
        {0x04,0x0a,0x11,0,0,0,0}, {0,0,0,0,0,0,0x1f}, {0x08,0x04,0,0,0,0,0},
        {0,0,0x0e,0x01,0x0f,0x11,0x0f}, {0x10,0x10,0x1e,0x11,0x11,0x11,0x1e},
        {0,0,0x0e,0x10,0x10,0x11,0x0e}, {0x01,0x01,0x0f,0x11,0x11,0x11,0x0f},
        {0,0,0x0e,0x11,0x1f,0x10,0x0e}, {0x06,0x08,0x1c,0x08,0x08,0x08,0x08},
        {0,0,0x0f,0x11,0x0f,0x01,0x0e}, {0x10,0x10,0x1e,0x11,0x11,0x11,0x11},
        {0x04,0,0x0c,0x04,0x04,0x04,0x0e}, {0x02,0,0x06,0x02,0x02,0x12,0x0c},
        {0x10,0x12,0x14,0x18,0x14,0x12,0x11}, {0x0c,0x04,0x04,0x04,0x04,0x04,0x0e},
        {0,0,0x1a,0x15,0x15,0x15,0x15}, {0,0,0x1e,0x11,0x11,0x11,0x11},
        {0,0,0x0e,0x11,0x11,0x11,0x0e}, {0,0,0x1e,0x11,0x1e,0x10,0x10},
        {0,0,0x0f,0x11,0x0f,0x01,0x01}, {0,0,0x16,0x18,0x10,0x10,0x10},
        {0,0,0x0f,0x10,0x0e,0x01,0x1e}, {0x08,0x08,0x1c,0x08,0x08,0x09,0x06},
        {0,0,0x11,0x11,0x11,0x11,0x0f}, {0,0,0x11,0x11,0x11,0x0a,0x04},
        {0,0,0x11,0x15,0x15,0x15,0x0a}, {0,0,0x11,0x0a,0x04,0x0a,0x11},
        {0,0,0x11,0x11,0x0f,0x01,0x0e}, {0,0,0x1f,0x02,0x04,0x08,0x1f},
        {0x06,0x04,0x04,0x08,0x04,0x04,0x06}, {0x04,0x04,0x04,0x04,0x04,0x04,0x04},
        {0x0c,0x04,0x04,0x02,0x04,0x04,0x0c}, {0,0x08,0x15,0x02,0,0,0}, {0}
    };
    for (int i = 0; i < len; ++i) {
        unsigned char c = (unsigned char)txt[i];
        if (c < 32 || c > 127) c = '?';
        const uint8_t* g = gl[c - 32];
        for (int ry = 0; ry < 7; ++ry)
            for (int rx = 0; rx < 5; ++rx)
                if ((g[ry] >> (4 - rx)) & 1)
                    surf_px(s, x + rx, y + ry, fg);
        x += 6;
    }
}

/* ================= SDL host glue ================= */
SDL_Window* win = nullptr;
SDL_Renderer* renderer = nullptr;
int win_w = 640, win_h = 480;
static SDL_Texture* tex = nullptr;

bool sdl_ok() { return win != nullptr; }

void sdl_init() {
    if (win) return;
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER | SDL_INIT_AUDIO) < 0) {
        fprintf(stderr, "SDL_Init: %s\n", SDL_GetError());
        return;
    }
    win = SDL_CreateWindow(app_title,
                           SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                           win_w, win_h, SDL_WINDOW_SHOWN);
    if (!win) { fprintf(stderr, "SDL_CreateWindow: %s\n", SDL_GetError()); return; }
    renderer = SDL_CreateRenderer(win, -1,
                                  SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer)
        renderer = SDL_CreateRenderer(win, -1, SDL_RENDERER_SOFTWARE);
    if (renderer) {
        SDL_RenderSetLogicalSize(renderer, win_w, win_h);
        tex = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_BGRA32,
                                SDL_TEXTUREACCESS_STREAMING, win_w, win_h);
    }
    // start with a white client area (typical Win3.x window bg)
}

void sdl_poll(m2c::_STATE* s) {
    if (!win) return;
    SDL_Event ev;
    while (SDL_PollEvent(&ev)) sdl_event_to_msg(s, ev);
}

/* Hit-test the visible window stack: topmost (latest-created) window whose
 * rect contains the point wins, mirroring Windows mouse dispatch. */
static W16Win* hit_test(int x, int y) {
    for (auto it = windows.rbegin(); it != windows.rend(); ++it) {
        W16Win* c = *it;
        if (!c->visible) continue;
        int ax, ay;
        win_abs_pos(c, &ax, &ay);
        int cw = c->w > 0 ? c->w : (c->surf ? c->surf->w : 0);
        int ch = c->h > 0 ? c->h : (c->surf ? c->surf->h : 0);
        if (x >= ax && x < ax + cw && y >= ay && y < ay + ch) return c;
    }
    return nullptr;
}

/* Window-tree compositing: each hwnd paints into its own surface; a Win16
 * display is the overlaid stack of every visible window at its position.
 * Child coords are relative to the parent's client origin; WS_POPUP
 * windows (dialogs, menus) position absolutely on screen.  Creation order
 * approximates z-order (later = on top). */
static void win_abs_pos(W16Win* w, int* ox, int* oy) {
    int x = w->x, y = w->y;
    if (!(w->style & 0x80000000u)) {          // WS_CHILD: relative to parent
        int depth = 32;
        dw p = w->parent;
        while (p && depth-- > 0) {
            W16Win* par = find_hwnd(p);
            if (!par) break;
            x += par->x; y += par->y;
            p = par->parent;
        }
    }
    *ox = x; *oy = y;
}

void sdl_present(m2c::_STATE*) {
    if (!win || !renderer || !tex) return;
    auto* w = find_hwnd(main_hwnd);
    if (!w) return;
    int fw = w->surf ? w->surf->w : (w->w > 0 ? w->w : 640);
    int fh = w->surf ? w->surf->h : (w->h > 0 ? w->h : 480);
    if (fw != win_w || fh != win_h) {
        SDL_DestroyTexture(tex);
        tex = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_BGRA32,
                                SDL_TEXTUREACCESS_STREAMING, fw, fh);
        if (tex) SDL_RenderSetLogicalSize(renderer, fw, fh);
        win_w = fw; win_h = fh;
    }
    if (!tex) return;
    SDL_Surface* frame = SDL_CreateRGBSurfaceWithFormat(0, fw, fh, 32,
                                                      SDL_PIXELFORMAT_BGRA32);
    if (!frame) return;
    if (w->surf) SDL_BlitSurface(w->surf, nullptr, frame, nullptr);
    // Overlay every other visible window at its absolute position, in
    // creation order (children and popups land on top of the main frame).
    for (auto* v : windows) {
        if (v == w || !v->visible || !v->surf) continue;
        int ax, ay;
        win_abs_pos(v, &ax, &ay);
        SDL_Rect dr{ax, ay, v->surf->w, v->surf->h};
        SDL_BlitSurface(v->surf, nullptr, frame, &dr);
    }
    void* px; int pitch;
    if (SDL_LockTexture(tex, nullptr, &px, &pitch) == 0) {
        for (int y = 0; y < fh; ++y)
            memcpy((db*)px + y * pitch, (db*)frame->pixels + y * frame->pitch,
                   fw * 4);
        SDL_UnlockTexture(tex);
    }
    SDL_FreeSurface(frame);
    SDL_RenderClear(renderer);
    SDL_RenderCopy(renderer, tex, nullptr, nullptr);
    SDL_RenderPresent(renderer);
}

void sdl_beep() { fflush(stdout); fputc('\a', stderr); fflush(stderr); }

} // namespace w16

/* ---------- API function implementations ---------- */

#define APIFN(name) bool name(m2c::_offsets, struct m2c::_STATE* _state)
#define DONE(n) { w16::retf_args(_state, n); return true; }
#define W(i) w16::argw(_state, i)
#define D(i) w16::argd(_state, i)
#define FP(i) w16::argptr(_state, i)
#define STR(i) w16::argstr(_state, i, _strtmp)
#define RETW(v) w16::retw(_state, (dw)(v))
#define RETD(v) w16::retd(_state, (dd)(v))
#define LOG(...) do { w16::log_api(__func__, ##__VA_ARGS__); } while (0)

#include "wine16_kernel.inc"
#include "wine16_user.inc"
#include "wine16_gdi.inc"
#include "wine16_mm.inc"
