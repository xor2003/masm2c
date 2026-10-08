/* wine16_kernel.inc — KERNEL API implementations. Included by wine16.cpp. */

/* ---- task / init ---- */

APIFN(inittask) {
    X86_REGREF
    std::string _strtmp;
    LOG("");
    /* returns: ax=1, bx=cmdline off in PSP, cx=stack limit, dx=nCmdShow,
       es=PSP, di=hInstance, si=hPrevInstance */
    eax = 1;
    ebx = (ebx & 0xffff0000) | 0x81;          // PSP:81h command tail
    ecx = (ecx & 0xffff0000) | 0x400;         // stack limit (offset)
    edx = (edx & 0xffff0000) | 1;             // SW_SHOWNORMAL
    es  = m2c::m2c_current_psp();
    edi = (edi & 0xffff0000) | (w16::hinstance & 0xffff);
    esi = (esi & 0xffff0000);                 // hPrevInstance = 0
    DONE(0);
}

APIFN(initapp) {
    X86_REGREF
    std::string _strtmp;
    dw hinst = W(0);
    LOG("hinst=%x", hinst);
    eax = 1;
    DONE(2);
}

APIFN(waitevent) {
    X86_REGREF
    std::string _strtmp;
    LOG("");
    w16::sdl_poll(_state);
    eax = 0;
    DONE(2);
}

APIFN(locksegment) {
    X86_REGREF
    std::string _strtmp;
    dw seg = W(0);
    LOG("seg=%x", seg);
    eax = (dw)(seg == 0xffff ? ds : seg);
    DONE(2);
}

APIFN(fatalexit) {
    X86_REGREF
    std::string _strtmp;
    LOG("code=%x", W(0));
    throw std::runtime_error("FatalExit");
}

APIFN(fatalappexit) {
    X86_REGREF
    std::string _strtmp;
    LOG("action=%x msg='%s'", W(2), STR(0));
    DONE(6);
}

APIFN(getversion) {
    X86_REGREF
    std::string _strtmp;
    eax = 0x0a03;   // Windows 3.10 (al=major, ah=minor after xchg)
    DONE(0);
}

APIFN(getdosenvironment) {
    X86_REGREF
    std::string _strtmp;
    // return far ptr to environment block in PSP region (seg=psp, off=0x2c is env seg...)
    // simplest: fabricate empty env in PSP scratch area? Return psp env.
    RETD(((dd)m2c::m2c_current_psp() << 16) | 0x2c);
    DONE(0);
}

APIFN(getmodulefilename) {
    X86_REGREF
    std::string _strtmp;
    dw hmod = W(3); dd buf = D(1); dw n = W(0);
    LOG("hmod=%x buf=%08x n=%x", hmod, buf, n);
    const char* s = w16::exe_name;
    db* p = w16::fptr(buf);
    if (p) {
        size_t l = strlen(s) + 1;
        if (l > n) l = n;
        memcpy(p, s, l);
        eax = (dw)(l - 1);
    } else eax = 0;
    DONE(8);
}

APIFN(dos3call) {
    X86_REGREF
    std::string _strtmp;
    LOG("ax=%x", ax);
    // emulate as int21
    m2c::asm2C_INT(_state, 0x21);
    DONE(0);
}

APIFN(outputdebugstring) {
    X86_REGREF
    std::string _strtmp;
    LOG("'%s'", STR(0));
    DONE(4);
}

/* ---- global memory ---- */

APIFN(globalalloc) {
    X86_REGREF
    std::string _strtmp;
    dw flags = W(2); dd bytes = D(0);
    dw h = w16::galloc(bytes ? bytes : 1);
    if (h && (flags & 0x0040)) memset(w16::gptr(h), 0, bytes); // GMEM_ZEROINIT
    LOG("flags=%x bytes=%u -> %x", flags, (unsigned)bytes, h);
    eax = h;
    DONE(6);
}

APIFN(globalfree) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(0);
    w16::gfree(h);                /* handle is the block's selector */
    LOG("h=%x", h);
    eax = 0;
    DONE(2);
}

APIFN(globallock) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(0);
    LOG("h=%x", h);
    RETD(((dd)h << 16));   // seg:0
    DONE(2);
}

APIFN(globalunlock) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(2);
}

APIFN(globalhandle) {
    X86_REGREF
    std::string _strtmp;
    dw seg = W(0);
    eax = seg; edx = (edx & 0xffff0000) | seg;
    DONE(2);
}

APIFN(globalsize) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(0);
    RETD(w16::gsize_of(h));
    DONE(2);
}

APIFN(globalrealloc) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(3); dd bytes = D(1); dw flags = W(0);
    LOG("h=%x bytes=%u flags=%x", h, (unsigned)bytes, flags);
    dw newpara = 0;
    if (bytes) {
        /* Selector blocks are fixed 64KB regions; shrinking is a no-op,
           growing just moves the contents to a fresh block. */
        newpara = w16::galloc(bytes);
        if (newpara) {
            dd old = w16::gsize_of(h);
            memcpy(w16::gptr(newpara), w16::gptr(h), old < bytes ? old : bytes);
            w16::gfree(h);
        }
    }
    eax = newpara;
    DONE(8);
}

/* ---- resources ---- */

APIFN(findresource) {
    X86_REGREF
    std::string _strtmp;
    // FindResource(hInstance, lpName, lpType): type D(0), name D(2), hinst W(4)
    dd type = D(0); dd name = D(2); dw hinst = W(4);
    LOG("hinst=%x name=%08x type=%08x", hinst, name, type);
    dd len = 0;
    const db* d = w16::res_find_data(name, type, &len);
    // Return a handle = index+1 into g_res
    dw h = 0;
    if (d) {
        for (size_t i = 0; i < w16::g_res.size(); ++i)
            if (w16::ne_image.data() + w16::g_res[i].file_off == d) { h = (dw)(i + 1); break; }
    }
    eax = h;
    DONE(10);
}

APIFN(loadresource) {
    X86_REGREF
    std::string _strtmp;
    dw hinst = W(1); dw hres = W(0);
    LOG("hinst=%x hres=%x", hinst, hres);
    if (!hres || hres > (dw)w16::g_res.size()) { eax = 0; DONE(4); }
    auto& e = w16::g_res[hres - 1];
    dw h = w16::galloc(e.len ? e.len : 1);
    if (h) memcpy(w16::gptr(h), w16::ne_image.data() + e.file_off, e.len);
    eax = h;
    DONE(4);
}

APIFN(lockresource) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(0);
    LOG("h=%x", h);
    RETD(((dd)h << 16));
    DONE(2);
}

APIFN(freeresource) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(0);
    w16::gfree(h);
    eax = 0;
    DONE(2);
}

/* ---- modules ---- */

APIFN(loadlibrary) {
    X86_REGREF
    std::string _strtmp;
    LOG("'%s'", STR(0));
    eax = 32;   // >32 = success fake handle
    DONE(4);
}

APIFN(freelibrary) {
    X86_REGREF
    std::string _strtmp;
    DONE(2);
}

APIFN(makeprocinstance) {
    X86_REGREF
    std::string _strtmp;
    dd proc = D(1); dw hinst = W(0);
    LOG("proc=%08x hinst=%x", proc, hinst);
    RETD(proc);  // thunk = raw proc (our dispatch handles aggregate)
    DONE(6);
}

APIFN(freeprocinstance) {
    X86_REGREF
    std::string _strtmp;
    DONE(4);
}

/* ---- string helpers ---- */

APIFN(lstrcpy) {
    X86_REGREF
    std::string _strtmp;
    dd dst = D(2); dd src = D(0);
    db* d = w16::fptr(dst);
    std::string s;
    w16::fstr(src, s);
    if (d) { strcpy((char*)d, s.c_str()); }  // NOLINT(clang-analyzer-security.insecureAPI.strcpy) lstrcpy is unbounded by API contract; d is guest memory
    RETD(dst);
    DONE(8);
}

APIFN(lstrcat) {
    X86_REGREF
    std::string _strtmp;
    dd dst = D(2); dd src = D(0);
    db* d = w16::fptr(dst);
    std::string s;
    w16::fstr(src, s);
    if (d) strcat((char*)d, s.c_str());  // NOLINT(clang-analyzer-security.insecureAPI.strcpy) lstrcat is unbounded by API contract; d is guest memory
    RETD(dst);
    DONE(8);
}

APIFN(lstrlen) {
    X86_REGREF
    std::string _strtmp;
    std::string s;
    w16::fstr(D(0), s);
    eax = (dw)s.size();
    DONE(4);
}

APIFN(lstrcmp) {
    X86_REGREF
    std::string _strtmp;
    std::string a, b;
    w16::fstr(D(2), a); w16::fstr(D(0), b);
    eax = (dw)(int16_t)strcmp(a.c_str(), b.c_str());
    DONE(8);
}

/* ---- file I/O ---- */

struct W16File { FILE* f; std::string name; };
static std::vector<W16File> w16files;

static dw wf_alloc(FILE* f, const std::string& n) {
    for (size_t i = 1; i < w16files.size(); ++i)
        if (!w16files[i].f) { w16files[i].f = f; w16files[i].name = n; return (dw)i; }
    w16files.push_back({f, n});
    return (dw)(w16files.size() - 1);
}

APIFN(_lopen) {
    X86_REGREF
    std::string _strtmp;
    // _lopen(lpPathName(4), iReadWrite(2)): nearest = mode W(0), path D(1)
    dw mode = W(0); std::string nm; w16::fstr(D(1), nm);
    LOG("'%s' mode=%x", nm.c_str(), mode);
    const char* m = (mode & 3) == 1 ? "wb" : (mode & 3) == 2 ? "r+b" : "rb";
    FILE* f = fopen(nm.c_str(), m);
    if (!f) { std::string p = std::string("../") + nm; f = fopen(p.c_str(), m); }
    if (!f && w16::data_dir) {
        // try the NE dir explicitly
        char buf[512];
        snprintf(buf, sizeof(buf), "%s/%s", w16::data_dir, nm.c_str());
        f = fopen(buf, m);
    }
    eax = f ? wf_alloc(f, nm) : (dw)0xffff;  // HFILE_ERROR
    DONE(6);
}

APIFN(_lread) {
    X86_REGREF
    std::string _strtmp;
    // _lread(hFile, lpBuffer, wBytes): bytes W(0), buf D(1), hf W(3)
    dw cnt = W(0);
    db* p = w16::fptr(D(1));
    dw hf = W(3);
    eax = 0xffff;
    if (hf < w16files.size() && w16files[hf].f && p)
        eax = (dw)fread(p, 1, cnt, w16files[hf].f);
    DONE(8);
}

APIFN(_lclose) {
    X86_REGREF
    std::string _strtmp;
    dw hf = W(0);
    if (hf < w16files.size() && w16files[hf].f) { fclose(w16files[hf].f); w16files[hf].f = nullptr; }
    eax = 0;
    DONE(2);
}

APIFN(_llseek) {
    X86_REGREF
    std::string _strtmp;
    // _llseek(hFile, lOffset, iOrigin): origin W(0), off D(1), hf W(3)
    dw hf = W(3); dd off = D(1); dw whence = W(0);
    long pos = -1;
    if (hf < w16files.size() && w16files[hf].f)
        pos = fseek(w16files[hf].f, (long)(int32_t)off,
                    whence == 0 ? SEEK_SET : whence == 1 ? SEEK_CUR : SEEK_END) == 0
              ? ftell(w16files[hf].f) : -1;
    RETD((dd)pos);
    DONE(8);
}

/* ---- profile / misc ---- */

APIFN(getprofilestring) {
    X86_REGREF
    std::string _strtmp;
    // (app, key, def, buf, size): size W(0), buf D(1), def D(3), key D(5), app D(7)
    std::string app, key, defl;
    w16::fstr(D(7), app); w16::fstr(D(5), key); w16::fstr(D(3), defl);
    db* dstp = w16::fptr(D(1));
    dw sz = W(0);
    LOG("app='%s' key='%s' def='%s'", app.c_str(), key.c_str(), defl.c_str());
    int l = (int)defl.size();
    if (dstp && sz) {
        size_t n = std::min((size_t)sz - 1, defl.size());
        memcpy(dstp, defl.c_str(), n);
        dstp[n] = 0;
    }
    eax = (dw)std::min(l, (int)sz - 1);
    DONE(18);
}

APIFN(muldiv) {
    X86_REGREF
    std::string _strtmp;
    dw a = W(2), b = W(1), c = W(0);
    int32_t r = c ? (int32_t)(((int64_t)(int16_t)a * (int16_t)b) / (int16_t)c) : -1;
    eax = (dw)r;
    DONE(6);
}
