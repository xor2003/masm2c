/* wine16_mm.inc — MMSYSTEM / WIN87EM / misc. Included by wine16.cpp. */

/* __fptrap is called by the CRT when the x87 emulator (WIN87EM) isn't
 * present or on FP faults.  Our host FPU emulation makes it a no-op. */
APIFN(__fptrap) {
    X86_REGREF
    std::string _strtmp;
    LOG("ax=%x", ax);
    DONE(0);
}

/* ---- MMIO ----
 * Supports both file-backed and memory-backed (fccIOProc='MEM ' / pchBuffer)
 * handles.  The latter is how the game streams the embedded "WAVE" resources:
 * it fills an MMIOINFO whose pchBuffer points at the locked resource, then uses
 * descend/read/ascend to walk the RIFF 'fmt '/'data' chunks. */

struct Mmio {
    FILE* f;                 // file-backed stream (nullptr for memory)
    const db* buf;           // memory buffer (host ptr)  — MMIOINFO.pchBuffer
    dd buflen;               //                            MMIOINFO.cchBuffer
    bool mem;
    std::string name;
    dd pos;                  // absolute stream offset
};
static std::vector<Mmio> mmios;

static dd mm_len(Mmio& m) {
    if (m.mem) return m.buflen;
    if (!m.f) return 0;
    long cur = ftell(m.f); fseek(m.f, 0, SEEK_END);
    long n = ftell(m.f); fseek(m.f, cur, SEEK_SET);
    return n < 0 ? 0 : (dd)n;
}
static dd mm_read(Mmio& m, dd off, void* out, dd n) {
    dd lim = mm_len(m);
    if (off >= lim) return 0;
    if (off + n > lim) n = lim - off;
    if (m.mem) memcpy(out, m.buf + off, n);
    else { fseek(m.f, off, SEEK_SET); n = (dd)fread(out, 1, n, m.f); }
    return n;
}
static dd mm_rd32(Mmio& m, dd off) { uint8_t b[4] = {0,0,0,0}; mm_read(m, off, b, 4); return (dd)(b[0] | b[1] << 8 | b[2] << 16 | (dd)b[3] << 24); }

APIFN(mmioopen) {
    X86_REGREF
    std::string _strtmp;
    // mmioOpen(name4, lpmmioinfo4, flags4)
    dd flags = D(0); dd info = D(2); dd name = D(4);
    std::string nm; w16::fstr(name, nm);
    Mmio m; m.f = nullptr; m.buf = nullptr; m.buflen = 0; m.mem = false; m.pos = 0; m.name = nm;
    /* Memory-backed open: an MMIOINFO with a buffer is passed (fccIOProc 'MEM '
     * or a non-null pchBuffer). */
    db* inf = info ? w16::fptr(info) : nullptr;
    if (inf) { m.buf = w16::fptr(w16::rd32(inf + 20)); m.buflen = w16::rd32(inf + 16); }
    if (m.buf && m.buflen) {
        m.mem = true;
        LOG("mem buf=%p len=%u", (const void*)m.buf, (unsigned)m.buflen);
    } else {
        FILE* f = nullptr;
        if (!nm.empty()) {
            f = fopen(nm.c_str(), (flags & 0x30000) ? "r+b" : "rb");
            if (!f) { std::string p = std::string("../") + nm; f = fopen(p.c_str(), "rb"); }
            if (!f && w16::data_dir) {
                char buf[512]; snprintf(buf, sizeof(buf), "%s/%s", w16::data_dir, nm.c_str());
                f = fopen(buf, "rb");
            }
        } else {
            /* Scratch mmio with no buffer: a real file gives working seek/read. */
            f = tmpfile();
        }
        if (!f) { eax = 0; DONE(12); }
        m.f = f;
    }
    mmios.push_back(m);
    eax = (dw)mmios.size();      // 1-based
    DONE(12);
}

APIFN(mmioread) {
    X86_REGREF
    std::string _strtmp;
    // (hmmio, buf4, len4)
    dd len = D(0); dd buf = D(2); dw h = W(4);
    db* p = w16::fptr(buf);
    dd n = 0;
    if (h && h <= mmios.size() && p) {
        Mmio& m = mmios[h - 1];
        n = mm_read(m, m.pos, p, len);
        m.pos += n;
    }
    w16::retd(_state, n);        // LONG count in dx:ax
    DONE(10);
}

APIFN(mmioclose) {
    X86_REGREF
    std::string _strtmp;
    dw h = W(1);
    if (h && h <= mmios.size()) { Mmio& m = mmios[h - 1]; if (m.f) fclose(m.f); m.f = nullptr; m.mem = false; }
    eax = 0;
    DONE(4);
}

APIFN(mmiodescend) {
    X86_REGREF
    std::string _strtmp;
    // (hmmio, lpck4, lpckparent4, flags) — fill MMCKINFO
    // pushed L->R: hmmio, lpck, parent, flags -> flags=W(0), parent=D(1), lpck=D(3), hmmio=W(5)
    dw hmm = W(5); dd lpck = D(3); dd par = D(1); dw fl = W(0);
    db* ck = w16::fptr(lpck);
    dd err = 0x10;               // MMIOERR_CHUNKNOTFOUND
    if (hmm && hmm <= mmios.size() && ck) {
        Mmio& m = mmios[hmm - 1];
        dd lim = mm_len(m);
        /* Search region: inside lpckparent's data, else whole stream. */
        dd beg = 0, end = lim;
        db* pp = par ? w16::fptr(par) : nullptr;
        if (pp) {
            beg = w16::rd32(pp + 12);                 // parent dwDataOffset
            dd psz = w16::rd32(pp + 4);               // parent cksize
            end = beg + psz - (w16::rd32(pp + 8) ? 4 : 0); // RIFF/LIST fccType eats 4
            if (end > lim) end = lim;
            if (beg > lim) beg = lim;
        }
        dd target = w16::rd32(ck + ((fl & 0x20) ? 8 : 0));  // FINDRIFF->fccType, FINDCHUNK->ckid
        for (dd off = beg; off + 8 <= end;) {
            dd cid = mm_rd32(m, off), csz = mm_rd32(m, off + 4);
            bool hit = false; dd dataoff = 0;
            if ((fl & 0x10) && cid == target) { hit = true; dataoff = off + 8; }
            else if ((fl & 0x20) && (cid == 0x46464952 /*RIFF*/ || cid == 0x5453494c /*LIST*/)
                     && mm_rd32(m, off + 8) == target) { hit = true; dataoff = off + 12; }
            if (hit) {
                w16::wr32(ck + 0, cid);
                w16::wr32(ck + 4, csz);
                w16::wr32(ck + 8, (fl & 0x20) ? mm_rd32(m, off + 8) : 0); // fccType
                w16::wr32(ck + 12, dataoff);                            // dwDataOffset
                w16::wr32(ck + 16, 0);
                m.pos = dataoff;
                err = 0;
                break;
            }
            if (!csz) { ++off; continue; }            // resync on malformed chunk
            off += 8 + csz + (csz & 1);               // chunks are word-aligned
        }
    }
    w16::retd(_state, err);
    DONE(12);
}

APIFN(mmioascend) {
    X86_REGREF
    std::string _strtmp;
    // (hmmio, lpck4, flags) — resume at end of the ascended chunk
    // pushed L->R: hmmio, lpck, flags -> flags=W(0), lpck=D(1), hmmio=W(3)
    dw hmm = W(3); dd lpck = D(1);
    if (hmm && hmm <= mmios.size()) {
        db* ck = lpck ? w16::fptr(lpck) : nullptr;
        if (ck) { dd d = w16::rd32(ck + 12), s = w16::rd32(ck + 4); mmios[hmm - 1].pos = d + s + (s & 1); }
    }
    eax = 0;
    DONE(8);
}

/* ---- audio via SDL_mixer ----
 * waveOut* plays embedded "WAVE" resources (PCM SFX); mciSendCommand drives a
 * "sequencer" device whose elements are the MIDI files ZEEKDAT.000..006.
 * The mixer device is opened lazily so games without audio still run when the
 * host has no sound device. */

static bool audio_tried = false, audio_ok = false;
static bool audio_init() {
    if (audio_tried) return audio_ok;
    audio_tried = true;
    if (Mix_OpenAudio(44100, AUDIO_S16SYS, 2, 1024) != 0) {
        LOG("audio: Mix_OpenAudio failed: %s", Mix_GetError());
        return false;
    }
    /* Point fluidsynth at a GM soundfont so the sequencer device can render. */
    if (!getenv("SDL_SOUNDFONTS") && !getenv("TIMIDITY_CFG")) {
        const char* sfs[] = {
            "/usr/share/sounds/sf2/default-GM.sf2",
            "/usr/share/sounds/sf2/FluidR3_GM.sf2",
            "/usr/share/sounds/sf2/FluidR3_GS.sf2",
            "/usr/share/sounds/sf2/TimGM6mb.sf2",
            nullptr };
        for (int i = 0; sfs[i]; ++i)
            if (FILE* f = fopen(sfs[i], "rb")) { fclose(f); Mix_SetSoundFonts(sfs[i]); break; }
    }
    audio_ok = true;
    return true;
}

static int wf_ch = 1, wf_rate = 11025, wf_bits = 8;   /* guest WAVEFORMAT */
static std::map<dd, Mix_Chunk*> wav_chunks;           /* WAVEHDR* -> chunk */

static Mix_Chunk* wav_chunk(dd lpwh) {
    std::map<dd, Mix_Chunk*>::iterator it = wav_chunks.find(lpwh);
    if (it != wav_chunks.end()) return it->second;
    db* hdr = w16::fptr(lpwh);
    if (!hdr) return nullptr;
    dd lpdata = w16::rd32(hdr);          /* WAVEHDR.lpData */
    dd len    = w16::rd32(hdr + 4);      /* WAVEHDR.dwBufferLength */
    db* pcm   = w16::fptr(lpdata);
    if (!pcm || !len || len > (1 << 22)) return nullptr;
    /* Wrap the raw PCM in a RIFF/WAVE header so the mixer decodes+converts. */
    std::vector<uint8_t> w(44 + len);
    uint8_t* p = w.data();
    memcpy(p + 0, "RIFF", 4);  w16::wr32(p + 4, 36 + len); memcpy(p + 8, "WAVE", 4);
    memcpy(p + 12, "fmt ", 4); w16::wr32(p + 16, 16);
    w16::wr16(p + 20, 1);                          /* PCM */
    w16::wr16(p + 22, (dw)wf_ch);
    w16::wr32(p + 24, (dd)wf_rate);
    w16::wr32(p + 28, (dd)(wf_rate * wf_ch * (wf_bits / 8)));
    w16::wr16(p + 32, (dw)(wf_ch * (wf_bits / 8)));
    w16::wr16(p + 34, (dw)wf_bits);
    memcpy(p + 36, "data", 4); w16::wr32(p + 40, len);
    memcpy(p + 44, pcm, len);
    SDL_RWops* rw = SDL_RWFromConstMem(w.data(), (int)w.size());
    Mix_Chunk* c = rw ? Mix_LoadWAV_RW(rw, 1) : nullptr;
    wav_chunks[lpwh] = c;
    return c;
}

APIFN(waveoutopen) {
    X86_REGREF
    std::string _strtmp;
    /* (lphwo4, uDeviceID, lpFormat4, dwCallback4, dwInstance4, dwFlags4) */
    db* fmt = FP(6);
    if (fmt) {
        int tag = w16::rd16(fmt), ch = w16::rd16(fmt + 2);
        int rate = (int)w16::rd32(fmt + 4), bits = w16::rd16(fmt + 12);
        if (tag == 1 && ch >= 1 && ch <= 2 && rate >= 4000 && rate <= 48000
            && (bits == 8 || bits == 16)) {
            wf_ch = ch; wf_rate = rate; wf_bits = bits;
        }
    }
    LOG("rate=%d ch=%d bits=%d", wf_rate, wf_ch, wf_bits);
    audio_init();
    db* p = FP(9);                                   /* LPHWAVEOUT */
    if (p) w16::wr16(p, 1);                          /* single fake device */
    eax = 0;
    DONE(22);
}

APIFN(waveoutprepareheader) {
    X86_REGREF
    std::string _strtmp;
    /* (hwo, lpwh4, uSize) */
    if (audio_init()) wav_chunk(D(1));
    eax = 0;
    DONE(8);
}

APIFN(waveoutunprepareheader) {
    X86_REGREF
    std::string _strtmp;
    dd lpwh = D(1);
    std::map<dd, Mix_Chunk*>::iterator it = wav_chunks.find(lpwh);
    if (it != wav_chunks.end()) { if (it->second) Mix_FreeChunk(it->second); wav_chunks.erase(it); }
    eax = 0;
    DONE(8);
}

APIFN(waveoutwrite) {
    X86_REGREF
    std::string _strtmp;
    /* (hwo, lpwh4, uSize) — queue the chunk; mark the header done. */
    dd lpwh = D(1);
    if (audio_init()) {
        Mix_Chunk* c = wav_chunk(lpwh);
        db* hdr = w16::fptr(lpwh);
        dd len = hdr ? w16::rd32(hdr + 4) : 0;
        LOG("sfx lpwh=%08x len=%u chunk=%p", lpwh, (unsigned)len, (void*)c);
        if (c) Mix_PlayChannel(-1, c, 0);
        if (hdr) w16::wr32(hdr + 16, w16::rd32(hdr + 16) | 8); /* WHDR_DONE */
    }
    eax = 0;
    DONE(8);
}

/* ---- MCI ---- */
static std::map<dw, Mix_Music*> mci_devs;
static dw mci_next_id = 1;

/* Case-insensitive lookup of a guest filename under a directory. */
static bool mci_find(const char* dir, const std::string& nm, std::string& out) {
    std::string base = nm;
    size_t sl = base.find_last_of("/\\"); if (sl != std::string::npos) base = base.substr(sl + 1);
    std::string p = dir ? (std::string(dir) + "/" + base) : base;
    FILE* f = fopen(p.c_str(), "rb");
    if (f) { fclose(f); out = p; return true; }
    const char* d = dir && *dir ? dir : ".";
    if (DIR* dp = opendir(d)) {
        struct dirent* e;
        while ((e = readdir(dp))) {
            if (!strcasecmp(e->d_name, base.c_str())) {
                closedir(dp); out = std::string(d) + "/" + e->d_name; return true;
            }
        }
        closedir(dp);
    }
    return false;
}
static void mci_resolve(const std::string& nm, std::string& out) {
    out.clear();
    if (nm.empty()) return;
    const char* sl = strpbrk(nm.c_str(), "/\\");
    std::string dirpart, base = nm;
    if (sl) { dirpart.assign(nm, 0, sl - nm.c_str()); base = sl + 1; }
    if (mci_find(dirpart.empty() ? nullptr : dirpart.c_str(), base, out)) return;
    if (mci_find("..", base, out)) return;
    if (w16::data_dir && mci_find(w16::data_dir, base, out)) return;
}

APIFN(mcisendcommand) {
    X86_REGREF
    std::string _strtmp;
    /* (wDeviceID, wMessage, dwParam1, dwParam2) */
    dw dev = W(5); dw msg = W(4); dd flags = D(2); dd parms = D(0);
    LOG("mci dev=%u msg=%03x flags=%08x parms=%08x", (unsigned)dev, msg, flags, parms);
    dd err = 0;
    switch (msg) {
    case 0x803: /* MCI_OPEN */
        if (parms && audio_init()) {
            db* p = w16::fptr(parms);
            if (p) {
                std::string fn; w16::fstr(w16::rd32(p + 12), fn); /* lpstrElementName */
                std::string path; mci_resolve(fn, path);
                Mix_Music* m = path.empty() ? nullptr : Mix_LoadMUS(path.c_str());
                dw id = mci_next_id++;
                mci_devs[id] = m;
                w16::wr16(p + 4, id);              /* wDeviceID out */
                LOG("mci open '%s' -> id=%u music=%p", fn.c_str(), (unsigned)id, (void*)m);
            }
        }
        break;
    case 0x806: /* MCI_PLAY */
        if (mci_devs.count(dev) && mci_devs[dev]) Mix_PlayMusic(mci_devs[dev], 1);
        break;
    case 0x807: /* MCI_SEEK (dwParam1 0x100 = TO_START) */
        if (flags & 0x100) Mix_RewindMusic();
        break;
    case 0x808: /* MCI_STOP */
        Mix_HaltMusic();
        break;
    case 0x804: /* MCI_CLOSE */
        if (mci_devs.count(dev)) {
            if (mci_devs[dev]) { Mix_HaltMusic(); Mix_FreeMusic(mci_devs[dev]); }
            mci_devs.erase(dev);
        }
        break;
    }
    w16::retd(_state, err);                        /* dx:ax = result */
    DONE(12);
}
