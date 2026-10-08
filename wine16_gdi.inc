/* wine16_gdi.inc — GDI API implementations. Included by wine16.cpp. */

/* helpers are in namespace w16; the APIFN bodies run at global scope. */

APIFN(createpen) {
    X86_REGREF
    std::string _strtmp;
    // (style, width, color4)
    dd color = D(0); dw wid = W(2); dw style = W(3);
    w16::GdiObj* o = w16::new_obj(1);
    o->pen_style = style; o->pen_color = color; o->pen_w = wid ? wid : 1;
    LOG("style=%x w=%x color=%06x -> %x", style, wid, color, o->handle);
    eax = o->handle;
    DONE(8);
}

APIFN(createsolidbrush) {
    X86_REGREF
    std::string _strtmp;
    dd color = D(0);
    w16::GdiObj* o = w16::new_obj(2);
    o->brush_style = 0; o->brush_color = color;
    eax = o->handle;
    DONE(4);
}

APIFN(createhatchbrush) {
    X86_REGREF
    std::string _strtmp;
    dd color = D(0); dw hatch = W(2);
    w16::GdiObj* o = w16::new_obj(2);
    o->brush_style = 1; o->brush_color = color; o->brush_hatch = hatch;
    eax = o->handle;
    DONE(6);
}

APIFN(createfontindirect) {
    X86_REGREF
    std::string _strtmp;
    db* lf = FP(0);
    w16::GdiObj* o = w16::new_obj(3);
    if (lf) o->font_h = (int16_t)w16::rd16(lf);
    eax = o->handle;
    DONE(4);
}

APIFN(getstockobject) {
    X86_REGREF
    std::string _strtmp;
    dw i = W(0);
    // stock handles: return tagged pseudo handles
    eax = (dw)(0x8000 + i);
    DONE(2);
}

APIFN(deleteobject) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(0);
    for (size_t i = 0; i < w16::gobjs.size(); ++i)
        if (w16::gobjs[i]->handle == h) {
            if (w16::gobjs[i]->surf) SDL_FreeSurface(w16::gobjs[i]->surf);
            delete w16::gobjs[i];
            w16::gobjs.erase(w16::gobjs.begin() + i);
            eax = 1; DONE(2);
        }
    eax = 1;
    DONE(2);
}

/* stock object colors */
static dd stock_color(dw h, bool* ispen, dd* col) {
    switch (h) {
    case 0x8006: *ispen = true; *col = 0xffffff; return 1;  // WHITE_PEN
    case 0x8007: *ispen = true; *col = 0; return 1;         // BLACK_PEN
    case 0x8008: *ispen = true; *col = 0; return 0;         // NULL_PEN (transparent)
    case 0x8000: *col = 0xffffff; return 1;                 // WHITE_BRUSH
    case 0x8001: *col = 0xc0c0c0; return 1;
    case 0x8002: *col = 0x808080; return 1;
    case 0x8003: *col = 0x404040; return 1;
    case 0x8004: *col = 0; return 1;                        // BLACK_BRUSH
    case 0x8005: *col = 0; return 0;                        // NULL_BRUSH
    }
    *col = 0; return 1;
}

APIFN(selectobject) {
    X86_REGREF
    std::string _strtmp;
    dw hobj = W(0); dw hdc = W(1);
    auto* d = w16::find_dc(hdc);
    dw old = 0;
    if (d) {
        auto* o = w16::find_obj(hobj);
        if (o) {
            if (o->kind == 4) {                 // bitmap -> mem DC
                old = d->selbitmap;
                d->selbitmap = hobj;
                if (!o->surf) w16::obj_surf(o);
                d->surf = o->surf;
                d->mem = o;
            } else if (o->kind == 1) { old = d->pen; d->pen = hobj; }
            else if (o->kind == 2) { old = d->brush; d->brush = hobj; }
            else if (o->kind == 3) { old = d->font; d->font = hobj; }
            else old = hobj;
        } else if ((hobj & 0xff00) == 0x8000) {
            old = d->pen; d->pen = hobj;   // stock object id
        } else old = hobj;
    }
    eax = old ? old : hobj;
    DONE(4);
}

APIFN(selectpalette) {
    X86_REGREF
    std::string _strtmp;
    eax = W(1);
    DONE(6);
}

APIFN(realizepalette) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(2);
}

APIFN(createcompatibledc) {
    X86_REGREF
    std::string _strtmp;
    LOG("hit\n");
    auto* srcdc = w16::find_dc(W(0));
    w16::DC* d = w16::make_dc(nullptr, nullptr, nullptr);
    if (srcdc) {
        d->mapmode = srcdc->mapmode;
        d->wextx = srcdc->wextx; d->wexty = srcdc->wexty;
        d->vextx = srcdc->vextx; d->vexty = srcdc->vexty;
    }
    eax = d->handle;
    DONE(2);
}

APIFN(createic) {
    X86_REGREF
    std::string _strtmp;
    w16::DC* d = w16::make_dc(nullptr, nullptr, nullptr);
    eax = d->handle;
    DONE(16);
}

APIFN(deletedc) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(0);
    for (auto it = w16::dcs.begin(); it != w16::dcs.end(); ++it)
        if ((*it)->handle == h) { delete *it; w16::dcs.erase(it); break; }
    eax = 1;
    DONE(2);
}

APIFN(createcompatiblebitmap) {
    X86_REGREF
    std::string _strtmp;
    dw hgt = W(0), wid = W(1);
    w16::GdiObj* o = w16::new_obj(4);
    o->bw = wid; o->bh = hgt; o->bbpp = 32; o->stride = wid * 4;
    o->bits.resize((size_t)o->stride * hgt, 0xff);
    o->surf = SDL_CreateRGBSurfaceWithFormat(0, wid, hgt, 32, SDL_PIXELFORMAT_BGRA32);
    LOG("%dx%d -> %x", wid, hgt, o->handle);
    eax = o->handle;
    DONE(6);
}

APIFN(loadbitmap) {
    X86_REGREF
    std::string _strtmp;
    dd name = D(0);
    LOG("resid/str=%08x", name);
    w16::GdiObj* o = w16::load_bitmap_res(name);
    eax = o ? o->handle : 0;
    DONE(6);
}

APIFN(createdibitmap) {
    X86_REGREF
    std::string _strtmp;
    // (hdc, lpbmih4, fdwInit4, lpbits4, lpbmi4, usage2)
    dd bmi = D(1); dd bits = D(3); dd init = D(5); dd bmih = D(7);
    const db* hdr = w16::fptr(bmih ? bmih : bmi);
    const db* pix = w16::fptr(bits);
    int w = 0, h = 0, bpp = 0, stride = 0;
    std::vector<dd> pal;
    const db* dstp = nullptr;
    if (hdr && w16::parse_bmi(hdr, &w, &h, &bpp, &pal, &dstp, &stride)) {
        w16::GdiObj* o = w16::new_obj(4);
        o->bw = w; o->bh = h; o->bbpp = bpp; o->palette = pal; o->stride = stride;
        if (init && pix) {
            o->bits.assign(pix, pix + (size_t)stride * h);
        } else {
            o->bits.resize((size_t)stride * h, 0);
        }
        eax = o->handle;
    } else eax = 0;
    DONE(20);
}

APIFN(getobject) {
    X86_REGREF
    std::string _strtmp;
    dd lpv = D(0); dw cb = W(2); dw h = W(3);
    auto* o = w16::find_obj(h);
    db* p = w16::fptr(lpv);
    if (o && o->kind == 4 && p && cb >= 14) {
        // Win16 BITMAP is 14 bytes: bmBits (far ptr) sits at +10.
        // Writing a dword at +12 overruns the caller's buffer (here it
        // zeroed the saved BP on the stack and crashed the layout walk).
        w16::wr16(p, 0);                 // bmType
        w16::wr16(p + 2, (dw)o->bw);
        w16::wr16(p + 4, (dw)o->bh);
        w16::wr16(p + 6, (dw)o->stride);
        p[8] = 1;                        // bmPlanes
        p[9] = (db)o->bbpp;              // bmBitsPixel
        w16::wr32(p + 10, 0);            // bmBits
        eax = 14;
    } else eax = 0;
    DONE(8);
}

APIFN(getdibits) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(18);
}

/* ---- DC attributes ---- */

APIFN(setbkcolor) {
    X86_REGREF
    std::string _strtmp;
    dd color = D(0); dw hdc = W(2);
    auto* d = w16::find_dc(hdc);
    dd old = d ? d->bkcolor : 0;
    if (d) d->bkcolor = color;
    RETD(old);
    DONE(6);
}

APIFN(setbkmode) {
    X86_REGREF
    std::string _strtmp;
    dw mode = W(0); dw hdc = W(1);
    auto* d = w16::find_dc(hdc);
    int old = d ? d->bkmode : 0;
    if (d) d->bkmode = mode;
    eax = (dw)old;
    DONE(4);
}

APIFN(getbkmode) {
    X86_REGREF
    std::string _strtmp;
    auto* d = w16::find_dc(W(0));
    eax = d ? (dw)d->bkmode : 0;
    DONE(2);
}

APIFN(settextcolor) {
    X86_REGREF
    std::string _strtmp;
    dd color = D(0); dw hdc = W(2);
    auto* d = w16::find_dc(hdc);
    dd old = d ? d->textcolor : 0;
    if (d) d->textcolor = color;
    RETD(old);
    DONE(6);
}

APIFN(setrop2) {
    X86_REGREF
    std::string _strtmp;
    dw rop = W(0); dw hdc = W(1);
    auto* d = w16::find_dc(hdc);
    int old = d ? d->rop2 : 0;
    if (d) d->rop2 = rop;
    eax = (dw)old;
    DONE(4);
}

APIFN(setmapmode) {
    X86_REGREF
    std::string _strtmp;
    dw mode = W(0); dw hdc = W(1);
    auto* d = w16::find_dc(hdc);
    int old = d ? d->mapmode : 1;
    if (d) d->mapmode = mode;
    eax = (dw)old;
    DONE(4);
}

APIFN(getmapmode) {
    X86_REGREF
    std::string _strtmp;
    auto* d = w16::find_dc(W(0));
    eax = d ? (dw)d->mapmode : 1;
    DONE(2);
}

APIFN(setviewportext) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(0), w = W(1), hdc = W(2);
    auto* d = w16::find_dc(hdc);
    dd old = d ? ((dd)(dw)d->vexty << 16 | (dw)d->vextx) : 0x00010001;
    if (d) { d->vextx = w; d->vexty = h; }
    RETD(old);
    DONE(6);
}

APIFN(setviewportorg) {
    X86_REGREF
    std::string _strtmp;
    dw y = W(0), x = W(1), hdc = W(2);
    auto* d = w16::find_dc(hdc);
    dd old = d ? ((dd)(dw)d->vorgy << 16 | (dw)d->vorgx) : 0;
    if (d) { d->vorgx = (int16_t)x; d->vorgy = (int16_t)y; }
    RETD(old);
    DONE(6);
}

APIFN(setwindowext) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(0), w = W(1), hdc = W(2);
    auto* d = w16::find_dc(hdc);
    dd old = d ? ((dd)(dw)d->wexty << 16 | (dw)d->wextx) : 0x00010001;
    if (d) { d->wextx = w; d->wexty = h; }
    RETD(old);
    DONE(6);
}

APIFN(setwindoworg) {
    X86_REGREF
    std::string _strtmp;
    dw y = W(0), x = W(1), hdc = W(2);
    auto* d = w16::find_dc(hdc);
    dd old = d ? ((dd)(dw)d->worgy << 16 | (dw)d->worgx) : 0;
    if (d) { d->worgx = (int16_t)x; d->worgy = (int16_t)y; }
    RETD(old);
    DONE(6);
}

/* ---- drawing ---- */

APIFN(setpixel) {
    X86_REGREF
    std::string _strtmp;
    dd color = D(0); dw y = W(2), x = W(3), hdc = W(4);
    auto* d = w16::find_dc(hdc);
    dd ret = (dd)-1;
    if (d && d->surf) {
        int px, py;
        w16::dc_pt(d, (int16_t)x, (int16_t)y, &px, &py);
        w16::surf_px(d->surf, px, py, color);
        ret = color;
    }
    RETD(ret);
    DONE(10);
}

APIFN(moveto) {
    X86_REGREF
    std::string _strtmp;
    dw y = W(0), x = W(1), hdc = W(2);
    auto* d = w16::find_dc(hdc);
    dd old = 0;
    if (d) {
        old = ((dd)(dw)d->cury << 16) | (dw)d->curx;
        d->curx = (int16_t)x; d->cury = (int16_t)y;
    }
    RETD(old);
    DONE(6);
}

APIFN(lineto) {
    X86_REGREF
    std::string _strtmp;
    dw y = W(0), x = W(1), hdc = W(2);
    auto* d = w16::find_dc(hdc);
    if (d && d->surf) {
        auto* p = w16::find_obj(d->pen);
        dd col = p && p->kind == 1 ? p->pen_color : 0;
        int wid = p && p->kind == 1 ? p->pen_w : 1;
        int x0, y0, x1, y1;
        w16::dc_pt(d, d->curx, d->cury, &x0, &y0);
        w16::dc_pt(d, (int16_t)x, (int16_t)y, &x1, &y1);
        w16::surf_line(d->surf, x0, y0, x1, y1, col, wid);
        d->curx = (int16_t)x; d->cury = (int16_t)y;
    }
    eax = 1;
    DONE(6);
}

APIFN(rectangle) {
    X86_REGREF
    std::string _strtmp;
    dw b = W(0), r = W(1), t = W(2), l = W(3), hdc = W(4);
    auto* d = w16::find_dc(hdc);
    if (d && d->surf) {
        auto* br = w16::find_obj(d->brush);
        dd fill = br && br->kind == 2 ? br->brush_color : 0xffffff;
        bool hollow = br == nullptr && (d->brush & 0xff00) == 0x8000 && (d->brush & 0xff) == 5;
        int x0, y0, x1, y1;
        w16::dc_pt(d, (int16_t)l, (int16_t)t, &x0, &y0);
        w16::dc_pt(d, (int16_t)r, (int16_t)b, &x1, &y1);
        if (x1 < x0) std::swap(x0, x1);
        if (y1 < y0) std::swap(y0, y1);
        if (!hollow) w16::surf_fill(d->surf, x0, y0, x1 - x0, y1 - y0, fill);
        auto* p = w16::find_obj(d->pen);
        dd col = p && p->kind == 1 ? p->pen_color : 0;
        w16::surf_line(d->surf, x0, y0, x1, y0, col, 1);
        w16::surf_line(d->surf, x1, y0, x1, y1, col, 1);
        w16::surf_line(d->surf, x1, y1, x0, y1, col, 1);
        w16::surf_line(d->surf, x0, y1, x0, y0, col, 1);
    }
    eax = 1;
    DONE(10);
}

APIFN(textout) {
    X86_REGREF
    std::string _strtmp;
    // (hdc, x, y, lpstr4, count)
    dw count = W(0); dd str = D(1); dw y = W(3), x = W(4); dw hdc = W(5);
    auto* d = w16::find_dc(hdc);
    const db* s = w16::fptr(str);
    if (d && d->surf && s) {
        int px, py;
        w16::dc_pt(d, (int16_t)x, (int16_t)y, &px, &py);
        w16::draw_text(d->surf, px, py, (const char*)s, (int)(int16_t)count, d->textcolor);
    }
    eax = 1;
    DONE(12);
}

APIFN(bitblt) {
    X86_REGREF
    std::string _strtmp;
    LOG("hit\n");
    // (hdcDst,x,y,w,h,hdcSrc,xs,ys,rop4)
    dd rop = D(0); dw ys = W(2), xs = W(3), hsrc = W(4);
    dw hh = W(5), ww = W(6), yd = W(7), xd = W(8), hdst = W(9);
    auto* dst = w16::find_dc(hdst);
    auto* src = w16::find_dc(hsrc);
    if (dst && dst->surf) {
        int x0, y0;
        w16::dc_pt(dst, (int16_t)xd, (int16_t)yd, &x0, &y0);
        if (src && src->surf)
            w16::surf_blit(dst->surf, x0, y0, (int16_t)ww, (int16_t)hh,
                           src->surf, (int16_t)xs, (int16_t)ys,
                           (int16_t)ww, (int16_t)hh, rop, dst->bkcolor);
        else {
            // no src -> pattern ops
            dd v = w16::rop_apply(rop, 0, 0, dst->bkcolor);
            w16::surf_fill(dst->surf, x0, y0, (int16_t)ww, (int16_t)hh, v);
        }
    }
    eax = 1;
    DONE(20);
}

APIFN(patblt) {
    X86_REGREF
    std::string _strtmp;
    LOG("hit\n");
    // (hdc,x,y,w,h,rop4)
    dd rop = D(0); dw hh = W(2), ww = W(3), yd = W(4), xd = W(5), hdc = W(6);
    auto* d = w16::find_dc(hdc);
    if (d && d->surf) {
        auto* br = w16::find_obj(d->brush);
        dd pat = br && br->kind == 2 ? br->brush_color : d->bkcolor;
        int x0, y0;
        w16::dc_pt(d, (int16_t)xd, (int16_t)yd, &x0, &y0);
        for (int yy = 0; yy < (int16_t)hh; ++yy)
            for (int xx = 0; xx < (int16_t)ww; ++xx) {
                dd cur = w16::surf_get(d->surf, x0 + xx, y0 + yy);
                w16::surf_px(d->surf, x0 + xx, y0 + yy,
                             w16::rop_apply(rop, 0, cur, pat));
            }
    }
    eax = 1;
    DONE(14);
}

APIFN(stretchdibits) {
    X86_REGREF
    std::string _strtmp;
    LOG("hit\n");
    // (hdc,xDst,yDst,wDst,hDst,xSrc,ySrc,wSrc,hSrc,lpBits4,lpbmi4,usage2,rop4)
    dd rop = D(0); dd lpbmi = D(3); dd lpbits = D(5);
    dw hSrc = W(7), wSrc = W(8), ySrc = W(9), xSrc = W(10);
    dw hDst = W(11), wDst = W(12), yDst = W(13), xDst = W(14), hdc = W(15);
    auto* d = w16::find_dc(hdc);
    const db* hdr = w16::fptr(lpbmi);
    const db* bits = w16::fptr(lpbits);
    if (d && d->surf && hdr && bits) {
        int w, h, bpp, stride;
        std::vector<dd> pal;
        const db* dstp = nullptr;
        if (w16::parse_bmi(hdr, &w, &h, &bpp, &pal, &dstp, &stride))
            w16::dib_blit(d, (int16_t)xDst, (int16_t)yDst, (int16_t)wDst, (int16_t)hDst,
                          bits, w, h, bpp, pal, (int16_t)xSrc, (int16_t)ySrc,
                          wSrc ? (int16_t)wSrc : w, hSrc ? (int16_t)hSrc : h,
                          rop, false);
    }
    eax = 1;
    DONE(32);
}

APIFN(getdevicecaps) {
    X86_REGREF
    std::string _strtmp;
    dw idx = W(0);
    dw v = 0;
    switch (idx) {
    case 0: v = 1; break;              // DRIVERVERSION
    case 4: case 8: v = (dw)w16::win_w; break;   // HORZRES
    case 6: case 10: v = (dw)w16::win_h; break;  // VERTRES
    case 12: v = 24; break;            // BITSPIXEL
    case 14: v = 1; break;             // PLANES
    case 38: v = 1; break;             // COLORS? (NUMCOLORS)
    default: v = 1;
    }
    eax = v;
    DONE(4);
}

APIFN(getclipbox) {
    X86_REGREF
    std::string _strtmp;
    db* r = FP(0);
    auto* d = w16::find_dc(W(2));
    if (r) {
        w16::wr16(r, 0); w16::wr16(r + 2, 0);
        w16::wr16(r + 4, (dw)(d && d->surf ? d->surf->w : w16::win_w));
        w16::wr16(r + 6, (dw)(d && d->surf ? d->surf->h : w16::win_h));
    }
    eax = 2; // SIMPLEREGION
    DONE(6);
}

APIFN(gettextextent) {
    X86_REGREF
    std::string _strtmp;
    dw count = W(0);
    RETD(((dd)8 << 16) | (dw)(count * 6));
    DONE(8);
}

APIFN(gettextmetrics) {
    X86_REGREF
    std::string _strtmp;
    db* p = FP(0);
    if (p) {
        // Win16 TEXTMETRIC is 32 bytes; a larger memset overruns the
        // caller's stack buffer and clobbers its saved BP.
        memset(p, 0, 32);
        w16::wr16(p, 8);      // tmHeight
        w16::wr16(p + 2, 0);  // tmAscent
        w16::wr16(p + 4, 2);  // tmDescent
        w16::wr16(p + 10, 6); // tmAveCharWidth
    }
    eax = 1;
    DONE(6);
}

APIFN(escape) {
    X86_REGREF
    std::string _strtmp;
    eax = 1;
    DONE(14);
}
