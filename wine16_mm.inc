/* wine16_mm.inc — MMSYSTEM / WIN87EM / misc. Included by wine16.cpp. */

/* __fptrap is called by the CRT when the x87 emulator (WIN87EM) isn't
 * present or on FP faults.  Our host FPU emulation makes it a no-op. */
APIFN(__fptrap) {
    X86_REGREF
    std::string _strtmp;
    LOG("ax=%x", ax);
    DONE(0);
}

/* ---- MMIO ---- */

struct Mmio { FILE* f; long data_start, data_len; std::string name; };
static std::vector<Mmio> mmios;

APIFN(mmioopen) {
    X86_REGREF
    std::string _strtmp;
    // mmioOpen(name4, mmioinfo4, flags4)
    dd flags = D(0); dd info = D(2); dd name = D(4);
    std::string nm; w16::fstr(name, nm);
    LOG("'%s' flags=%08x", nm.c_str(), flags);
    FILE* f = nullptr;
    if (!nm.empty()) {
        f = fopen(nm.c_str(), (flags & 0x30000) ? "r+b" : "rb");
        if (!f) { std::string p = std::string("../") + nm; f = fopen(p.c_str(), p.size() ? "rb" : "rb"); }
        if (!f && w16::data_dir) {
            char buf[512];
            snprintf(buf, sizeof(buf), "%s/%s", w16::data_dir, nm.c_str());
            f = fopen(buf, "rb");
        }
    } else {
        /* mmioOpen(NULL, ..., MMIO_READWRITE) creates a memory-backed hmmio;
         * the caller uses it like a file. tmpfile() gives real seek/read/write
         * semantics so descend/create chunks behave correctly. */
        f = tmpfile();
    }
    dw h = 0;
    if (f) {
        mmios.push_back({f, 0, 0, nm});
        h = (dw)(mmios.size());   // 1-based
    }
    eax = h;
    DONE(12);
}

APIFN(mmioread) {
    X86_REGREF
    std::string _strtmp;
    // (hmmio, buf4, len4)
    dd len = D(0); dd buf = D(2); dw h = W(4);
    db* p = w16::fptr(buf);
    dd n = 0;
    if (h && h <= mmios.size() && mmios[h - 1].f && p)
        n = (dd)fread(p, 1, len, mmios[h - 1].f);
    eax = (dw)(n & 0xffff); edx = (edx & 0xffff0000) | (dw)(n >> 16);
    DONE(10);
}

APIFN(mmioclose) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(1);
    if (h && h <= mmios.size() && mmios[h - 1].f) { fclose(mmios[h - 1].f); mmios[h - 1].f = nullptr; }
    eax = 0;
    DONE(4);
}

APIFN(mmiodescend) {
    X86_REGREF
    std::string _strtmp;
    // (hmmio, lpck4, lpckparent4, flags) — fill MMCKINFO loosely
    // pushed L->R: hmmio, lpck, parent, flags -> flags=W(0), parent=D(1), lpck=D(3), hmmio=W(5)
    dw hmm = W(5); dd lpck = D(3); dd par = D(1); dw fl = W(0);
    db* ck = w16::fptr(lpck);
    if (hmm && hmm <= mmios.size() && mmios[hmm - 1].f && ck) {
        FILE* f = mmios[hmm - 1].f;
        uint8_t hdr[8];
        if (fread(hdr, 1, 8, f) == 8) {
            memcpy(ck, hdr, 4);
            w16::wr32(ck + 4, hdr[4] | hdr[5] << 8 | hdr[6] << 16 | hdr[7] << 24);
            w16::wr32(ck + 8, 0);            // dwDataOffset-ish
            w16::wr32(ck + 12, 0);
        }
    }
    eax = 0; // MMSYSERR_NOERROR
    DONE(12);
}

APIFN(mmioascend) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(8);
}

APIFN(mcisendcommand) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(12);
}

/* ---- waveOut (silent stubs — game logic unaffected) ---- */

APIFN(waveoutopen) {
    X86_REGREF
    std::string _strtmp;
    // (lphwo4, devid2, lpwf4, cb4, cbi4, flags4)
    db* p = FP(5);
    if (p) w16::wr16(p, 1);   // fake device handle 1
    eax = 0;
    DONE(22);
}

APIFN(waveoutprepareheader) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(10);
}

APIFN(waveoutunprepareheader) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(10);
}

APIFN(waveoutwrite) {
    X86_REGREF
    std::string _strtmp;
    eax = 0;
    DONE(10);
}
