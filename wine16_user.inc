/* wine16_user.inc — USER API implementations. Included by wine16.cpp. */

struct W16Class {
    std::string name;
    dd wndproc;
    dw style;
    int cbcls, cbwnd;
    dw hicon, hcursor, hbr;
    dd menu_name;
};

static std::vector<W16Class> w16classes;
static std::map<dw, std::string> dlgproc_store;

static dw find_class(const std::string& n) {
    for (size_t i = 0; i < w16classes.size(); ++i)
        if (w16classes[i].name == n) return (dw)(i + 1);
    return 0;
}

static dw wnd_create(m2c::_STATE* _state, w16::W16Win* pw) {
    w16::W16Win* w = new w16::W16Win();
    w->hwnd = w16::g_next_hwnd++;
    w->wndproc = pw ? pw->wndproc : 0;
    w->x = w->y = 0; w->w = w16::win_w; w->h = w16::win_h;
    w->style = 0; w->parent = pw ? pw->hwnd : 0;
    w->visible = true; w->enabled = true; w->dirty = true;
    memset(w->userdata, 0, sizeof(w->userdata));
    memset(w->winwords, 0, sizeof(w->winwords));
    w->surf = nullptr;
    w16::windows.push_back(w);
    return w->hwnd;
}

/* ================================================================ */

APIFN(registerclass) {
    X86_REGREF
    std::string _strtmp;
    // RegisterClass(LPWNDCLASS): WNDCLASS far ptr at D(0)
    db* p = FP(0);
    W16Class c{};
    if (p) {
        c.style = w16::rd16(p);
        c.wndproc = w16::rd32(p + 2);
        c.cbcls = w16::rd16(p + 6); c.cbwnd = w16::rd16(p + 8);
        w16::rd16(p + 10); // hinstance
        c.hicon = w16::rd16(p + 12);
        c.hcursor = w16::rd16(p + 14);
        c.hbr = w16::rd16(p + 16);
        c.menu_name = w16::rd32(p + 18);
        c.name = "";
        w16::fstr(w16::rd32(p + 22), c.name);
        LOG("cls='%s' wndproc=%08x hbr=%x", c.name.c_str(), c.wndproc, c.hbr);
    }
    w16classes.push_back(c);
    eax = (dw)w16classes.size();
    DONE(4);
}

APIFN(unregisterclass) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(6);
}

APIFN(getclassinfo) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(10);
}

APIFN(getclassname) {
    X86_REGREF
    std::string _strtmp;
    dw hwnd = W(3); dd buf = D(1); dw n = W(0);
    w16::W16Win* w = w16::find_hwnd(hwnd);
    int l = 0;
    if (w) {
        db* p = w16::fptr(buf);
        l = (int)w->cls.size();
        if (p) { strncpy((char*)p, w->cls.c_str(), n); if (n) p[n - 1] = 0; }
    }
    eax = (dw)l;
    DONE(8);
}

/* --- window creation --- */

APIFN(createwindow) {
    X86_REGREF
    std::string _strtmp;
    // CreateWindow(cls(4), title(4), style(4), X,Y,W,H(8), parent(2),
    //              menu(2), inst(2), param(4)) — 32 bytes
    dd lp = D(0); dw hinst = W(2); dw menu = W(3); dw parent = W(4);
    dw hgt = W(5), wid = W(6), y = W(7), x = W(8);
    dd style = D(9); dd title = D(11); dd cls = D(13);
    std::string cname, tname;
    if (cls >> 16) w16::fstr(cls, cname); else cname = "";
    if (title >> 16) w16::fstr(title, tname);
    LOG("cls='%s'@%08x title='%s' style=%08x %d,%d %dx%d parent=%x",
        cname.c_str(), cls, tname.c_str(), style, (int16_t)x, (int16_t)y,
        (int16_t)wid, (int16_t)hgt, parent);

    w16::W16Win* w = new w16::W16Win();
    w->hwnd = w16::g_next_hwnd++;
    w->cls = cname;
    w->title = tname;
    dw clsid = find_class(cname);
    w->wndproc = clsid ? w16classes[clsid - 1].wndproc : 0;
    w->x = (int16_t)x; w->y = (int16_t)y;
    w->w = (int16_t)wid; w->h = (int16_t)hgt;
    w->style = (dw)style; w->parent = parent; w->menu = menu;
    w->visible = false; w->enabled = true; w->dirty = true;
    memset(w->userdata, 0, sizeof(w->userdata));
    memset(w->winwords, 0, sizeof(w->winwords));
    w->surf = nullptr;
    w16::windows.push_back(w);
    if (!w16::main_hwnd) {
        w16::main_hwnd = w->hwnd;
        if (w->w <= 0 || w->w > 3000) w->w = w16::win_w;
        if (w->h <= 0 || w->h > 3000) w->h = w16::win_h;
        w16::win_w = w->w; w16::win_h = w->h;
        w16::sdl_init();
        // send WM_CREATE then WM_SIZE/SHOWWINDOW-ish
        w16::post_msg(w->hwnd, 0x0001, 0, 0);   // WM_CREATE
    }
    eax = w->hwnd;
    DONE(30);
}

APIFN(createwindowex) {
    X86_REGREF
    std::string _strtmp;
    // CreateWindowEx(exstyle(4), cls(4), title(4), style(4), X,Y,W,H(8),
    //                parent(2), menu(2), inst(2), param(4)) — 36 bytes
    dd lp = D(0); dw hinst = W(2); dw menu = W(3); dw parent = W(4);
    dw hgt = W(5), wid = W(6), y = W(7), x = W(8);
    dd style = D(9); dd title = D(11); dd cls = D(13); dd exstyle = D(15);
    std::string cname, tname;
    if (cls >> 16) w16::fstr(cls, cname);
    if (title >> 16) w16::fstr(title, tname);
    LOG("ex='%08x' cls='%s' title='%s' style=%08x %d,%d %dx%d",
        exstyle, cname.c_str(), tname.c_str(), style,
        (int16_t)x, (int16_t)y, (int16_t)wid, (int16_t)hgt);
    w16::W16Win* w = new w16::W16Win();
    w->hwnd = w16::g_next_hwnd++;
    w->cls = cname; w->title = tname;
    dw clsid = find_class(cname);
    w->wndproc = clsid ? w16classes[clsid - 1].wndproc : 0;
    w->x = (int16_t)x; w->y = (int16_t)y;
    w->w = (int16_t)wid; w->h = (int16_t)hgt;
    w->style = (dw)style; w->exstyle = (dw)exstyle;
    w->parent = parent; w->menu = menu;
    w->visible = false; w->enabled = true; w->dirty = true;
    memset(w->userdata, 0, sizeof(w->userdata));
    memset(w->winwords, 0, sizeof(w->winwords));
    w->surf = nullptr;
    w16::windows.push_back(w);
    if (!w16::main_hwnd) {
        w16::main_hwnd = w->hwnd;
        if (w->w <= 0 || w->w > 3000) w->w = w16::win_w;
        if (w->h <= 0 || w->h > 3000) w->h = w16::win_h;
        w16::win_w = w->w; w16::win_h = w->h;
        w16::sdl_init();
        w16::post_msg(w->hwnd, 0x0001, 0, 0);
    }
    eax = w->hwnd;
    DONE(34);
}

APIFN(destroywindow) {
    X86_REGREF
    std::string _strtmp;
    dw hwnd = W(0);
    LOG("hwnd=%x", hwnd);
    for (size_t i = 0; i < w16::windows.size(); ++i)
        if (w16::windows[i]->hwnd == hwnd) {
            if (w16::windows[i]->surf) SDL_FreeSurface(w16::windows[i]->surf);
            delete w16::windows[i];
            w16::windows.erase(w16::windows.begin() + i);
            break;
        }
    eax = 1;
    DONE(2);
}

APIFN(iswindow) {
    X86_REGREF
    std::string _strtmp;
    eax = w16::find_hwnd(W(0)) ? 1 : 0;
    DONE(2);
}

APIFN(iswindowenabled) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(0));
    eax = w ? (dw)w->enabled : 0;
    DONE(2);
}

APIFN(enablewindow) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(1));
    dw en = W(0);
    eax = 0;
    if (w) { eax = w->enabled ? 1 : 0; w->enabled = en != 0; }
    DONE(4);
}

APIFN(showwindow) {
    X86_REGREF
    std::string _strtmp;
    dw hwnd = W(1); dw cmd = W(0);
    auto* w = w16::find_hwnd(hwnd);
    LOG("hwnd=%x cmd=%x", hwnd, cmd);
    eax = 0;
    if (w) {
        eax = w->visible ? 1 : 0;
        w->visible = (cmd != 0);
        w->dirty = true;
        if (cmd && w->hwnd == w16::main_hwnd)
            w16::post_msg(hwnd, 0x0018, 1, 0);  // WM_SHOWWINDOW
    }
    DONE(4);
}

APIFN(movewindow) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(5));
    if (w) {
        w->x = (int16_t)W(4); w->y = (int16_t)W(3);
        w->w = (int16_t)W(2); w->h = (int16_t)W(1);
        if (w->surf) { SDL_FreeSurface(w->surf); w->surf = nullptr; }
    }
    eax = 1;
    DONE(12);
}

APIFN(getwindowrect) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(2));
    db* r = FP(0);
    if (w && r) {
        w16::wr16(r, (dw)w->x); w16::wr16(r + 2, (dw)w->y);
        w16::wr16(r + 4, (dw)(w->x + w->w)); w16::wr16(r + 6, (dw)(w->y + w->h));
    }
    DONE(6);
}

APIFN(getclientrect) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(2));
    db* r = FP(0);
    if (w && r) {
        w16::wr16(r, 0); w16::wr16(r + 2, 0);
        w16::wr16(r + 4, (dw)w->w); w16::wr16(r + 6, (dw)w->h);
    }
    DONE(6);
}

APIFN(getwindowlong) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(1));
    int idx = (int16_t)W(0);
    dd v = 0;
    if (w) {
        if (idx == -8) v = w->wndproc;           // GWL_WNDPROC
        else if (idx == -6) v = w16::hinstance;  // GWL_HINSTANCE
        else if (idx == -16) v = w->style;       // GWL_STYLE
        else if (idx >= 0 && idx < 16) v = w->userdata[idx / 2];
    }
    RETD(v);
    DONE(4);
}

APIFN(setwindowlong) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(3));
    int idx = (int16_t)W(2);
    dd v = D(0);
    dd old = 0;
    if (w) {
        if (idx == -8) { old = w->wndproc; w->wndproc = v; }
        else if (idx == -16) { old = w->style; w->style = (dw)v; }
        else if (idx >= 0 && idx < 16) { old = w->userdata[idx / 2]; w->userdata[idx / 2] = v; }
    }
    RETD(old);
    DONE(8);
}

APIFN(getwindowword) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(1));
    int idx = (int16_t)W(0);
    dw v = 0;
    if (w && idx >= 0 && idx < 16) v = w->winwords[idx];
    eax = v;
    DONE(4);
}

APIFN(setwindowword) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(2));
    int idx = (int16_t)W(1);
    dw v = W(0), old = 0;
    if (w && idx >= 0 && idx < 16) { old = w->winwords[idx]; w->winwords[idx] = v; }
    eax = old;
    DONE(6);
}

APIFN(setwindowtext) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(2));
    std::string t; w16::fstr(D(0), t);
    if (w) {
        w->title = t;
        if (w->hwnd == w16::main_hwnd && w16::win)
            SDL_SetWindowTitle(w16::win, t.c_str());
    }
    eax = 1;
    DONE(6);
}

APIFN(getwindowtext) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(3));
    db* p = w16::fptr(D(1)); dw n = W(0);
    int l = 0;
    if (w && p) {
        l = (int)w->title.size();
        strncpy((char*)p, w->title.c_str(), n);
        if (n) p[n - 1] = 0;
    }
    eax = (dw)l;
    DONE(8);
}

APIFN(getwindowtextlength) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(0));
    eax = w ? (dw)w->title.size() : 0;
    DONE(2);
}

APIFN(getparent) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(0));
    eax = w ? w->parent : 0;
    DONE(2);
}

APIFN(ischild) {
    X86_REGREF
    std::string _strtmp;
    dw p = W(1), c = W(0);
    auto* w = w16::find_hwnd(c);
    eax = (w && w->parent == p) ? 1 : 0;
    DONE(4);
}

APIFN(windowfrompoint) {
    X86_REGREF
    std::string _strtmp;
    eax = w16::main_hwnd;
    DONE(4);
}

APIFN(getdesktopwindow) {
    X86_REGREF
    std::string _strtmp;
    eax = 0xffff;
    DONE(0);
}

/* --- messages --- */

/* MSG layout (16-bit): hwnd, message, wParam, lParam(dd), time(dd), pt(dd) = 16 bytes */
static void write_msg_struct(m2c::_STATE* _state, dd lpmsg,
                             dw hwnd, dw msg, dw wp, dd lp) {
    db* p = w16::fptr(lpmsg);
    if (!p) return;
    w16::wr16(p, hwnd); w16::wr16(p + 2, msg); w16::wr16(p + 4, wp);
    w16::wr32(p + 6, lp);
    w16::wr32(p + 10, SDL_GetTicks());
    w16::wr32(p + 14, 0);
}

APIFN(getmessage) {
    X86_REGREF
    std::string _strtmp;
    // GetMessage(LPMSG lpMsg(4), HWND hwnd(2), UINT wFirst(2), UINT wLast(2))
    dw last = W(0), first = W(1), hwndf = W(2); dd lpmsg = D(3);
    dw hwnd, msg, wp; dd lp;
    bool ok = w16::fetch_msg(_state, hwndf, first, last, &hwnd, &msg, &wp, &lp);
    write_msg_struct(_state, lpmsg, hwnd, msg, wp, lp);
    eax = ok ? 1 : 0;
    DONE(10);
}

APIFN(peekmessage) {
    X86_REGREF
    std::string _strtmp;
    // PeekMessage(lpMsg(4), hwnd(2), first(2), last(2), remove(2)) = 14
    dw remove = W(0), last = W(1), first = W(2), hwndf = W(3); dd lpmsg = D(4);
    dw hwnd, msg, wp; dd lp;
    // non-blocking check
    uint32_t now = SDL_GetTicks();
    for (auto& t : w16::timers)
        if ((int32_t)(now - t.next) >= 0) {
            t.next = now + (t.period ? t.period : 1);
            if (t.cb) w16::call_guest(_state, t.cb, {t.hwnd, 0x0113, t.id, (dw)now});
            else w16::post_msg(t.hwnd, 0x0113, t.id, 0);
        }
    SDL_Event ev;
    while (SDL_PollEvent(&ev)) w16::sdl_event_to_msg(_state, ev);
    bool found = false;
    for (auto it = w16::msgq.begin(); it != w16::msgq.end(); ++it) {
        if (hwndf && it->hwnd && it->hwnd != hwndf) continue;
        if (it->msg < first || (last && it->msg > last)) continue;
        hwnd = it->hwnd; msg = it->msg; wp = it->wp; lp = it->lp;
        if (remove & 1) w16::msgq.erase(it);
        found = true;
        break;
    }
    if (!found && w16::quit_posted) {
        hwnd = 0; msg = 0x0012; wp = (dw)w16::quit_code; lp = 0;
        w16::quit_posted = false;
        found = true;
    }
    if (!found) {
        // repaint dirty windows on idle
        for (auto* w : w16::windows)
            if (w->dirty && w->visible) {
                if (remove & 1) { w->dirty = false; w16::post_msg(w->hwnd, 0x000f, 0, 0); }
                found = true;
                break;
            }
        if (!found) { w16::sdl_present(_state); eax = 0; DONE(12); }
        // re-scan for the paint message
        for (auto it = w16::msgq.begin(); it != w16::msgq.end(); ++it) {
            if (hwndf && it->hwnd && it->hwnd != hwndf) continue;
            if (it->msg < first || (last && it->msg > last)) continue;
            hwnd = it->hwnd; msg = it->msg; wp = it->wp; lp = it->lp;
            if (remove & 1) w16::msgq.erase(it);
            break;
        }
    }
    write_msg_struct(_state, lpmsg, hwnd, msg, wp, lp);
    eax = 1;
    DONE(12);
}

APIFN(dispatchmessage) {
    X86_REGREF
    std::string _strtmp;
    dd lpmsg = D(0);
    db* p = w16::fptr(lpmsg);
    dw hwnd = w16::rd16(p), msg = w16::rd16(p + 2), wp = w16::rd16(p + 4);
    dd lp = w16::rd32(p + 6);
    auto* w = w16::find_hwnd(hwnd);
    dd ret = 0;
    if (w && w->wndproc)
        ret = w16::call_guest(_state, w->wndproc, {hwnd, msg, wp, (dw)(lp >> 16), (dw)(lp & 0xffff)});
    eax = (dw)(ret & 0xffff); edx = (edx & 0xffff0000) | (dw)(ret >> 16);
    DONE(4);
}

APIFN(postmessage) {
    X86_REGREF
    std::string _strtmp;
    // PostMessage(hwnd,msg,wp,lp4): lp=D(0), wp=W(2), msg=W(3), hwnd=W(4)
    dw hwnd = W(4), msg = W(3), wp = W(2); dd lp = D(0);
    w16::post_msg(hwnd, msg, wp, lp);
    eax = 1;
    DONE(10);
}

APIFN(postquitmessage) {
    X86_REGREF
    std::string _strtmp;
    w16::quit_code = (int16_t)W(0);
    w16::quit_posted = true;
    w16::post_msg(0, 0x0012, (dw)w16::quit_code, 0);
    DONE(2);
}

APIFN(sendmessage) {
    X86_REGREF
    std::string _strtmp;
    // SendMessage(hwnd(2), msg(2), wp(2), lp(4)) = 10
    dw hwnd = W(4), msg = W(3), wp = W(2); dd lp = D(0);
    LOG("hwnd=%x msg=%x wp=%x lp=%08x", hwnd, msg, wp, lp);
    auto* w = w16::find_hwnd(hwnd);
    dd ret = 0;
    if (w && w->wndproc)
        ret = w16::call_guest(_state, w->wndproc, {hwnd, msg, wp, (dw)(lp >> 16), (dw)(lp & 0xffff)});
    eax = (dw)(ret & 0xffff); edx = (edx & 0xffff0000) | (dw)(ret >> 16);
    DONE(10);
}

APIFN(callwindowproc) {
    X86_REGREF
    std::string _strtmp;
    // CallWindowProc(lpPrevWndFunc(4), hwnd,msg,wp,lp(2,2,2,4))
    dd proc = D(5); dw hwnd = W(4), msg = W(3), wp = W(2); dd lp = D(0);
    dd ret = w16::call_guest(_state, proc, {hwnd, msg, wp, (dw)(lp >> 16), (dw)(lp & 0xffff)});
    eax = (dw)(ret & 0xffff); edx = (edx & 0xffff0000) | (dw)(ret >> 16);
    DONE(14);
}

APIFN(defwindowproc) {
    X86_REGREF
    std::string _strtmp;
    dw hwnd = W(4), msg = W(3); dw wp = W(2); dd lp = D(0);
    LOG("hwnd=%x msg=%x wp=%x lp=%08x", hwnd, msg, wp, lp);
    dd ret = 0;
    switch (msg) {
    case 0x000f: { // WM_PAINT: fill bg
        auto* w = w16::find_hwnd(hwnd);
        if (w && w->surf) w16::surf_fill(w->surf, 0, 0, w->surf->w, w->surf->h, 0xffffff);
        if (w) w->dirty = false;
        ret = 0; break;
    }
    case 0x0086: ret = 1; break;  // WM_NCACTIVATE -> keep active
    case 0x0087: ret = 0; break;  // WM_NCDESTROY
    default: ret = 0;
    }
    eax = (dw)(ret & 0xffff); edx = (edx & 0xffff0000) | (dw)(ret >> 16);
    DONE(10);
}

APIFN(translatemessage) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(4);
}

APIFN(translateaccelerator) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(8);
}

APIFN(translatemdisysaccel) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(6);
}

APIFN(isdialogmessage) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(6);
}

/* --- timers, focus, capture, caret --- */

APIFN(settimer) {
    X86_REGREF
    std::string _strtmp;
    // SetTimer(hwnd(2), id(2), elapse(2), lpfn(4)) = 10
    dw hwnd = W(4), id = W(3), elapse = W(2); dd cb = D(0);
    for (auto& t : w16::timers)
        if (t.hwnd == hwnd && t.id == id) {
            t.cb = cb; t.period = elapse; t.next = SDL_GetTicks() + elapse;
            eax = id; DONE(10);
        }
    w16::timers.push_back({hwnd, id, cb, elapse, SDL_GetTicks() + elapse});
    eax = id ? id : 1;
    DONE(10);
}

APIFN(killtimer) {
    X86_REGREF
    std::string _strtmp;
    dw hwnd = W(1), id = W(0);
    for (auto it = w16::timers.begin(); it != w16::timers.end(); ++it)
        if (it->hwnd == hwnd && it->id == id) { w16::timers.erase(it); break; }
    eax = 1;
    DONE(4);
}

APIFN(getfocus) {
    X86_REGREF
    std::string _strtmp;
    eax = w16::g_focus ? w16::g_focus : w16::main_hwnd;
    DONE(0);
}

APIFN(setfocus) {
    X86_REGREF
    std::string _strtmp;
    dw old = w16::g_focus;
    w16::g_focus = W(0);
    eax = old;
    DONE(2);
}

APIFN(setcapture) {
    X86_REGREF
    std::string _strtmp;
    dw old = w16::g_capture;
    w16::g_capture = W(0);
    eax = old;
    DONE(2);
}

APIFN(releasecapture) {
    X86_REGREF
    std::string _strtmp;
    w16::g_capture = 0;
    DONE(0);
}

APIFN(createcaret) {
    X86_REGREF
    std::string _strtmp;
    DONE(8);
}

APIFN(destroycaret) {
    X86_REGREF
    std::string _strtmp;
    DONE(0);
}

APIFN(setcaretpos) {
    X86_REGREF
    std::string _strtmp;
    DONE(4);
}

APIFN(setcaretblinktime) {
    X86_REGREF
    std::string _strtmp;
    DONE(2);
}

APIFN(getcaretblinktime) {
    X86_REGREF
    std::string _strtmp;
    eax = 500;
    DONE(0);
}

APIFN(showcaret) {
    X86_REGREF
    std::string _strtmp;
    DONE(2);
}

APIFN(setcursor) {
    X86_REGREF
    std::string _strtmp;
    eax = W(0);
    DONE(2);
}

APIFN(destroycursor) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(2);
}

APIFN(destroyicon) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(2);
}

APIFN(destroymenu) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(2);
}

APIFN(getcursorpos) {
    X86_REGREF
    std::string _strtmp;
    db* p = FP(0);
    if (p) { int x, y; SDL_GetMouseState(&x, &y); w16::wr16(p, (dw)x); w16::wr16(p + 2, (dw)y); }
    DONE(4);
}

APIFN(getkeystate) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(2);
}

/* --- misc --- */

APIFN(getcurrenttime) {
    X86_REGREF
    std::string _strtmp;
    RETD(SDL_GetTicks());
    DONE(0);
}

APIFN(getdialogbaseunits) {
    X86_REGREF
    std::string _strtmp;
    RETD(0x00080008);
    DONE(0);
}

APIFN(getsystemmetrics) {
    X86_REGREF
    std::string _strtmp;
    dw idx = W(0);
    dw v = 0;
    switch (idx) {
    case 0: v = (dw)w16::win_w; break;  // CXSCREEN
    case 1: v = (dw)w16::win_h; break;
    case 2: case 3: v = 20; break;      // scrollbar
    case 4: v = 20; break;              // caption
    case 5: case 6: v = 1; break;       // border
    case 7: case 8: v = 24; break;      // dlgframe
    case 12: case 13: v = 16; break;    // smicon
    case 20: case 21: v = 16; break;    // icon
    case 30: v = 1; break;              // kanjiwindow?
    case 15: v = 8; break;
    default: v = 0;
    }
    eax = v;
    DONE(2);
}

APIFN(getsyscolor) {
    X86_REGREF
    std::string _strtmp;
    static const dd colors[] = {
        0x808080, /* scrollbar */ 0x0000ff, 0x000080, 0xc0c0c0,
        0xffffff, 0x000000, 0x000000, 0x000000, 0xffffff,
        0xc0c0c0, 0xc0c0c0, 0x808080, 0x000000, 0xffffff,
        0xc0c0c0, 0x808080, 0x000000, 0xc0c0c0, 0x000000
    };
    dw idx = W(0);
    RETD(idx < sizeof(colors) / sizeof(dd) ? colors[idx] : 0);
    DONE(2);
}

APIFN(getsystemmenu) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(4);
}

APIFN(getmenu) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(2);
}

APIFN(setmenu) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(4);
}

APIFN(removemenu) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(6);
}

APIFN(loadmenu) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(6);
}

APIFN(loadcursor) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(6);
}

APIFN(loadicon) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(6);
}

APIFN(drawicon) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(8);
}

APIFN(messagebeep) {
    X86_REGREF
    std::string _strtmp;
    w16::sdl_beep();
    DONE(2);
}

APIFN(messagebox) {
    X86_REGREF
    std::string _strtmp;
    // MessageBox(hwnd(2), text(4), caption(4), type(2)) = 12
    std::string text, cap;
    dw hwnd = W(5); w16::fstr(D(3), text); w16::fstr(D(1), cap); dw type = W(0);
    LOG("hwnd=%x text='%s' cap='%s' type=%x", hwnd, text.c_str(), cap.c_str(), type);
    if (w16::sdl_ok())
        SDL_ShowSimpleMessageBox(SDL_MESSAGEBOX_INFORMATION, cap.c_str(), text.c_str(), w16::win);
    eax = 1; // IDOK
    DONE(12);
}

APIFN(invalidaterect) {
    X86_REGREF
    std::string _strtmp;
    // (hwnd, lpRect4, erase): erase=W(0), rect=D(1), hwnd=W(3)
    auto* w = w16::find_hwnd(W(3));
    if (w) w->dirty = true;
    DONE(8);
}

APIFN(invalidatergn) {
    X86_REGREF
    std::string _strtmp;
    // (hwnd, hrgn, erase): erase=W(0), rgn=W(1), hwnd=W(2)
    auto* w = w16::find_hwnd(W(2));
    if (w) w->dirty = true;
    DONE(6);
}

APIFN(updatewindow) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(0));
    if (w && w->dirty && w->wndproc) {
        w->dirty = false;
        w16::call_guest(_state, w->wndproc, {w->hwnd, 0x000f, 0, 0, 0});
        w16::sdl_present(_state);
    }
    DONE(2);
}

APIFN(scrollwindow) {
    X86_REGREF
    std::string _strtmp;
    DONE(14);
}

APIFN(screentoclient) {
    X86_REGREF
    std::string _strtmp;
    DONE(6);
}

static dw scrollpos_val[64];
static dw scrollrange_val[64][2];

APIFN(setscrollpos) {
    X86_REGREF
    std::string _strtmp;
    // (hwnd, bar, pos, redraw)
    dw hwnd = W(3), bar = W(2), pos = W(1);
    dw old = scrollpos_val[(hwnd & 63)];
    scrollpos_val[(hwnd & 63)] = pos;
    eax = old;
    DONE(8);
}

APIFN(setscrollrange) {
    X86_REGREF
    std::string _strtmp;
    // (hwnd, bar, min, max, redraw)
    dw hwnd = W(4), bar = W(3), mn = W(2), mx = W(1);
    scrollrange_val[hwnd & 63][0] = mn;
    scrollrange_val[hwnd & 63][1] = mx;
    DONE(10);
}

APIFN(setclassword) {
    X86_REGREF
    std::string _strtmp;
    // (hwnd, offset, newword): new=W(0), off=W(1), hwnd=W(2)
    dw hwnd = W(2); int idx = (int16_t)W(1); dw v = W(0);
    auto* w = w16::find_hwnd(hwnd);
    dw old = 0;
    if (w && idx >= 0 && idx < 32) { old = w->winwords[8 + idx / 2]; w->winwords[8 + idx / 2] = v; }
    eax = old;
    DONE(6);
}

APIFN(dptolp) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(8);
}

APIFN(graystring) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(22);
}

APIFN(beginpaint) {
    X86_REGREF
    std::string _strtmp;
    // BeginPaint(hwnd(2), lpPaint(4)) -> hdc; fills PAINTSTRUCT
    dw hwnd = W(2); dd lpps = D(0);
    auto* w = w16::find_hwnd(hwnd);
    db* p = w16::fptr(lpps);
    if (w && !w->surf) {
        w->surf = SDL_CreateRGBSurfaceWithFormat(0, w->w > 0 ? w->w : 640,
                                               w->h > 0 ? w->h : 480, 32,
                                               SDL_PIXELFORMAT_BGRA32);
    }
    w16::DC* d = w ? w16::make_dc(w, w->surf, nullptr) : nullptr;
    if (p && d) {
        w16::wr16(p, d->handle);          // hdc
        w16::wr16(p + 2, 0);              // fErase
        w16::wr16(p + 4, 0); w16::wr16(p + 6, 0);
        w16::wr16(p + 8, w ? (dw)w->w : 0); w16::wr16(p + 10, w ? (dw)w->h : 0);
    }
    eax = d ? d->handle : 0;
    DONE(6);
}

APIFN(endpaint) {
    X86_REGREF
    std::string _strtmp;
    dw hwnd = W(2); dd lpps = D(0);
    db* p = w16::fptr(lpps);
    if (p) {
        dw hdc = w16::rd16(p);
        for (auto it = w16::dcs.begin(); it != w16::dcs.end(); ++it)
            if ((*it)->handle == hdc) { delete *it; w16::dcs.erase(it); break; }
    }
    auto* w = w16::find_hwnd(hwnd);
    if (w) w->dirty = false;
    w16::sdl_present(_state);
    eax = 1;
    DONE(6);
}

APIFN(getdc) {
    X86_REGREF
    std::string _strtmp;
    auto* w = w16::find_hwnd(W(0));
    if (w && !w->surf)
        w->surf = SDL_CreateRGBSurfaceWithFormat(0, w->w > 0 ? w->w : 640,
                                               w->h > 0 ? w->h : 480, 32,
                                               SDL_PIXELFORMAT_BGRA32);
    w16::DC* d = w16::make_dc(w, w ? w->surf : nullptr, nullptr);
    eax = d->handle;
    DONE(2);
}

APIFN(releasedc) {
    X86_REGREF
    std::string _strtmp;
    dw hwnd = W(1); dw hdc = W(0);
    auto* d = w16::find_dc(hdc);
    if (d) {
        for (auto it = w16::dcs.begin(); it != w16::dcs.end(); ++it)
            if (*it == d) { w16::dcs.erase(it); break; }
        delete d;
        w16::sdl_present(_state);
        eax = 1;
    } else eax = 0;
    DONE(4);
}

APIFN(ansinext) {
    X86_REGREF
    std::string _strtmp;
    // AnsiNext(lpch far) -> far ptr advanced by 1
    RETD(D(0) + 1);
    DONE(4);
}

APIFN(getopenfilename) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(4);
}

APIFN(getsavefilename) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(4);
}

/* printf-style helpers */

APIFN(_wsprintf) {
    X86_REGREF
    std::string _strtmp;
    // cdecl far: args pushed right-to-left: [sp+4]=buf(4), [sp+8]=fmt(4), varargs...
    dd buf = D(0); dd fmt = D(2);
    db* dstp = w16::fptr(buf);
    std::string fmtstr;
    w16::fstr(fmt, fmtstr);
    // collect varargs starting at word index 4
    std::string out;
    int ai = 4;
    for (size_t i = 0; i < fmtstr.size(); ++i) {
        if (fmtstr[i] != '%') { out += fmtstr[i]; continue; }
        ++i;
        bool lng = false;
        char spec = 0;
        size_t j = i;
        for (; j < fmtstr.size(); ++j) {
            char c = fmtstr[j];
            if (c == 'l') { lng = true; continue; }
            if (isalpha((unsigned char)c) || c == '%') { spec = c; break; }
        }
        std::string conv = fmtstr.substr(i, j - i);
        i = j;
        char tmp[128];
        if (spec == 'd' || spec == 'i' || spec == 'u' || spec == 'x' || spec == 'X' || spec == 'c') {
            if (lng) { dd v = w16::argd(_state, ai); ai += 2; snprintf(tmp, sizeof(tmp), ("%" + conv + spec).c_str(), v); }
            else { dw v = w16::argw(_state, ai); ++ai; snprintf(tmp, sizeof(tmp), ("%" + conv + spec).c_str(), v); }
            out += tmp;
        } else if (spec == 's') {
            std::string sv;
            if (lng) { dd v = w16::argd(_state, ai); ai += 2; w16::fstr(v, sv); }
            else { dw v = w16::argw(_state, ai); ++ai; db* q = w16::fptr(((dd)ds << 16) | v); const char* qq = (const char*)q; sv = qq ? qq : ""; }
            out += sv;
        } else if (spec == '%') out += '%';
    }
    if (dstp) strcpy((char*)dstp, out.c_str());
    eax = (dw)out.size();
    DONE(0);   // cdecl — caller cleans
}

APIFN(wvsprintf) {
    X86_REGREF
    std::string _strtmp;
    // wvsprintf(buf(4), fmt(4), arglist(4)) — args via pointer; approximate
    dd buf = D(4); dd fmt = D(2); dd argp = D(0);
    db* dstp = w16::fptr(buf);
    std::string fmtstr; w16::fstr(D(1), fmtstr);
    db* ap = w16::fptr(argp);
    std::string out;
    int ai = 0;
    for (size_t i = 0; i < fmtstr.size(); ++i) {
        if (fmtstr[i] != '%') { out += fmtstr[i]; continue; }
        ++i;
        bool lng = false;
        char spec = 0;
        size_t j = i;
        for (; j < fmtstr.size(); ++j) {
            char c = fmtstr[j];
            if (c == 'l') { lng = true; continue; }
            if (isalpha((unsigned char)c) || c == '%') { spec = c; break; }
        }
        std::string conv = fmtstr.substr(i, j - i);
        i = j;
        char tmp[128];
        if (spec == 'd' || spec == 'i' || spec == 'u' || spec == 'x' || spec == 'X' || spec == 'c') {
            if (lng) { dd v = w16::rd32(ap + ai); ai += 4; snprintf(tmp, sizeof(tmp), ("%" + conv + spec).c_str(), v); }
            else { dw v = w16::rd16(ap + ai); ai += 2; snprintf(tmp, sizeof(tmp), ("%" + conv + spec).c_str(), v); }
            out += tmp;
        } else if (spec == 's') {
            dd v = lng ? w16::rd32(ap + ai) : (((dd)ds << 16) | w16::rd16(ap + ai));
            ai += lng ? 4 : 2;
            std::string sv; w16::fstr(v, sv);
            out += sv;
        } else if (spec == '%') out += '%';
    }
    if (dstp) strcpy((char*)dstp, out.c_str());
    eax = (dw)out.size();
    DONE(12);
}
