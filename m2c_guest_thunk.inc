/* m2c_guest_thunk.inc — generic Win16 guest-thunk interpreter for masm2c.
 *
 * Include this ONCE inside the game's unity translation unit, AFTER the
 * generated <game>.cpp and wine16.h, so the file-local __dispatch_call /
 * __dispatch_call_ext helpers and w16:: helpers are visible.
 *
 * Before including, the game TU must define its import table:
 *     #include "import_apis.inc"        // provides kImpApis[]
 * and may define M2C_THUNK_SENTINEL_OFF(bit) customizations.  The thunk
 * interprets linker/CRT byte stubs (`push imm`, `push cs; call rel16`,
 * `callf`, small prologues) ending in retf/retn that IDA labeled `byte_*`
 * data rather than procs, plus NE import sentinels (0000:8NNN).
 */

namespace w16 {

/* ---- guest callback trampoline ---- */

/* call a guest far proc (segment:offset or aggregate index).  Args pushed in
 * order: args[0] deepest.  For dd params split hi,lo words and pass hi first. */
dd call_guest(m2c::_STATE* s, dd fnaddr, const std::vector<dw>& args) {
    if (!fnaddr) return 0;
    dw saved_sp = (dw)s->esp;
    dw saved_bp = (dw)s->ebp;
    auto push = [&](dw v) {
        s->esp = (s->esp - 2) & 0xffff;
        w16::wr16(m2c::stack_raddr_(s->ss, (dw)s->esp), v);
    };
    for (dw a : args) push(a);
    const dw fake_cs = 0xFFFD;
    const dw fake_ip = 0xFFFE;
    push(fake_cs);
    push(fake_ip);
    m2c::mark_native_return(s, s->ss, (dw)s->esp, (m2c::MWORDSIZE)fake_ip);
    dd ret = 0;
    try {
        __dispatch_call_ext((m2c::_offsets)fnaddr, s);
    } catch (m2c::StackPop&) {
        log_api("call_guest", "StackPop unwind at %08x", fnaddr);
    } catch (const std::exception& e) {
        log_api("call_guest", "exception %s at %08x", e.what(), fnaddr);
    }
    s->esp = (s->esp & 0xffff0000) | saved_sp;
    s->ebp = (s->ebp & 0xffff0000) | saved_bp;
    ret = (s->eax & 0xffff) | ((s->edx & 0xffff) << 16);
    log_api("call_guest", "fn=%08x hwnd=%x msg=%x -> %08x",
            fnaddr, args.size() > 0 ? args[0] : 0,
            args.size() > 1 ? args[1] : 0, ret);
    return ret;
}

} // namespace w16

namespace m2c {

/* Linker/CRT thunk stubs and byte-labeled helper sequences are emitted by the
 * translator as `byte_*` data (IDA never labeled them procs): padding bytes,
 * `push imm`/`push cs; call rel16` far-call records, `callf`, tiny register
 * prologues (`enter`/`leave`/`mov reg,imm`), ending in `retf`/`retn`.
 * `dispatch_external_code` hands unresolved para-form targets here; this is a
 * bounded interpreter over the loaded code image inside `m`.
 *
 * Calls into real procs go through call_guest (which pushes a fake far
 * return).  The final retf/retn pops the caller's pushed return address and
 * consumes the native-return mark so the CALL_ site resumes normally.
 */
static dw& gth_r16(_STATE* s, int i) {
    dd* t[8] = {&s->eax,&s->ecx,&s->edx,&s->ebx,&s->esp,&s->ebp,&s->esi,&s->edi};
    return *(dw*)t[i];
}
static dw& gth_sg(_STATE* s, int i) {
    dw* t[4] = {&s->es,&s->cs,&s->ss,&s->ds};
    return *t[i];
}

/* The game supplies its NE import table as "import_apis.inc" (kImpApis[])
 * on the include path; absent one, imports dispatch to nothing. */
#if defined(__has_include)
#if __has_include("import_apis.inc")
#include "import_apis.inc"
#else
static const struct { const char* mod; m2c::dw ord; m2c::m2cf* fn; const char* name; } kImpApis[] = {};
#endif
#else
#include "import_apis.inc"
#endif

static const bool gth_trace = std::getenv("M2C_THUNK") != nullptr;

/* NE import fixups patched call sites to the sentinel far address
 * 0000:0x8000|idx.  By the time this runs the caller already pushed the
 * far frame ([ret ip][cs] under the args), matching w16::argw(sp+4). */
static bool gth_import(dd idx, _STATE* s) {
    if (idx >= m2c_ne_import_count) {
        log_error("thunk: import idx %u out of range\n", (unsigned)idx);
        return false;
    }
    const M2cNeImport& e = m2c_ne_imports[idx];
    const char* mod = m2c_ne_import_mod_name(e.mod_idx);
    for (const auto& a : kImpApis) {
        if (a.ord != e.ordinal || strcmp(a.mod, mod)) continue;
        w16::log_api("importcall", "%s.%u %s", mod, (unsigned)e.ordinal, a.name);
        if (gth_trace) fprintf(stderr, "[thunk] imp %s.%u %s\n", mod, (unsigned)e.ordinal, a.name);
        if (!a.fn) return true;      /* data import reached as code: nop */
        return a.fn((_offsets)0, s);
    }
    log_error("thunk: unmapped import %s.%u\n", mod, (unsigned)e.ordinal);
    return false;
}

static bool gth_is_import(dw sgm, dw off) { return sgm == 0 && (off & 0x8000); }

bool m2c_guest_thunk(dd disp, _STATE* s) {
    dw cur = (dw)(disp >> 16);            /* current paragraph */
    dw pc  = (dw)(disp & 0xffff);
    if (!cur && (disp & 0x8000))           /* NE import sentinel 0000:8NNN */
        return gth_import(disp & 0x7fff, s);
    if (cur & 4) {                         /* selector-form disp -> para */
        const dd lin = m2c_ldt_get_lin(cur);
        if (lin) cur = (dw)(lin >> 4);
    }
    const db* img = (const db*)&m;
    if (!cur) return false;

    /* A selector-form callback target (a registered wndproc like
     * 403f:2036) resolves here to its translated para:offset key.  Hand it
     * back to the dispatcher so the COMPILED code runs when a generated
     * case owns the key; only targets no case claims end up interpreted
     * below (linker byte stubs, thunk tails, tiny helper records).  Without
     * this, entire wndprocs get byte-interpreted. */
    {
        const dd key = ((dd)cur << 16) | (dd)pc;
        if (key != disp)
            return __dispatch_call((_offsets)key, s);
    }

    /* RETF-via-variable: a callee may pop cs:ip into memory and jmp to it
       (MS CRT __setargv pops the caller's far return into dword_3A8CE then
       jmps to it).  The POP moves the caller's native-return mark into
       native_return_values, so a target equal to the innermost pending
       return must unwind this frame instead of re-interpreting the call
       site's own bytes. */
    for (auto it = m2c::native_return_marks.rbegin();
         it != m2c::native_return_marks.rend(); ++it) {
        if (it->state == s
            && it->return_ip == (m2c::MWORDSIZE)pc
            && it->call_depth == m2c::native_return_call_depth) {
            m2c::last_ret_popped = -1;
            m2c::last_ret_mark_id = it->id;
            m2c::last_ret_mark_mode = 4;
            m2c::last_ret_site = disp;
            m2c::native_return_marks.erase(std::next(it).base());
            if (gth_trace)
                fprintf(stderr, "[thunk] %04x:%04x is a native return mark -> unwind\n", cur, pc);
            return true;
        }
    }
    for (auto it = m2c::native_return_values.rbegin();
         it != m2c::native_return_values.rend(); ++it) {
        if (it->state == s
            && it->return_ip == (m2c::MWORDSIZE)pc
            && it->call_depth == m2c::native_return_call_depth) {
            m2c::last_ret_popped = -1;
            m2c::last_ret_mark_id = it->id;
            m2c::last_ret_mark_mode = 4;
            m2c::last_ret_site = disp;
            m2c::native_return_values.erase(std::next(it).base());
            if (gth_trace)
                fprintf(stderr, "[thunk] %04x:%04x is a carried return -> unwind\n", cur, pc);
            return true;
        }
    }
    if (gth_trace) fprintf(stderr, "[thunk] enter %04x:%04x\n", cur, pc);

    auto rd8i  = [&]() -> dw { dw v = img[((dd)cur << 4) + pc]; ++pc; return v; };
    auto rd16i = [&]() -> dw { dw v; memcpy(&v, img + ((dd)cur << 4) + pc, 2); pc += 2; return v; };
    auto push = [&](dw v) {
        s->esp = (s->esp & 0xffff0000u) | ((dw)((dw)s->esp - 2));
        dw t = v; memcpy(stack_raddr_((dw)s->ss, (dw)s->esp), &t, 2);
    };
    auto pop = [&]() -> dw {
        dw v; memcpy(&v, stack_raddr_((dw)s->ss, (dw)s->esp), 2);
        s->esp = (s->esp & 0xffff0000u) | ((dw)((dw)s->esp + 2));
        return v;
    };
    auto rdm16 = [&](dw sgm, dw off) -> dw { dw v; memcpy(&v, raddr_(sgm, off), 2); return v; };
    auto wrm16 = [&](dw sgm, dw off, dw v) { memcpy(raddr_(sgm, off), &v, 2); };
    auto set_r8 = [&](int i, dw v) {
        dd* t[8] = {&s->eax,&s->ecx,&s->edx,&s->ebx,&s->eax,&s->ecx,&s->edx,&s->ebx};
        if (i < 4) *t[i] = (*t[i] & 0xffffff00u) | (v & 0xff);
        else       *t[i] = (*t[i] & 0xffff00ffu) | ((v & 0xff) << 8);
    };
    auto get_r8 = [&](int i) -> dw {
        dd* t[8] = {&s->eax,&s->ecx,&s->edx,&s->ebx,&s->eax,&s->ecx,&s->edx,&s->ebx};
        return (i < 4) ? (*t[i] & 0xff) : ((*t[i] >> 8) & 0xff);
    };

    eflags fl(s);
    auto flags16 = [&](dd v) { set_logic_flags(2, (dw)v, fl); };
    /* szp + carry for add/sub.  set_logic_flags() clears CF, so arithmetic
     * ops must publish only SZP or every jae/jb/jbe after cmp/sub breaks. */
    auto alu = [&](int rgop, dw d, dw v2, int bytes) -> dw {
        dd r;
        const dd c = s->CF ? 1 : 0;
        switch (rgop) {
        case 0: r = (dd)d + v2; fl.setCF(r >= (1u << (bytes*8))); break;
        case 2: r = (dd)d + v2 + c; fl.setCF(r >= (1u << (bytes*8))); break;
        case 3: r = (dd)d - v2 - c; fl.setCF((dd)d < (dd)v2 + c); break;
        case 5: r = (dd)d - v2; fl.setCF(d < v2); break;
        case 7: r = (dd)d - v2; fl.setCF(d < v2); break;
        case 1: r = d | v2; break;
        case 4: r = d & v2; break;
        case 6: r = d ^ v2; break;
        default: r = d | v2; break;
        }
        const dw msk = (bytes == 1) ? 0xff : 0xffff;
        if (rgop == 0 || rgop == 2 || rgop == 3 || rgop == 5 || rgop == 7)
            set_szp_flags(bytes, r & msk, fl);
        else
            set_logic_flags(bytes, r & msk, fl);
        return (dw)(r & msk);
    };

    auto shf = [&](int rgop, dw d, int cnt, int bytes) -> dw {
        const int bits = bytes * 8;
        const dw msk = (bytes == 1) ? 0xff : 0xffff;
        cnt &= 0x1f;
        dw r = (dw)(d & msk);
        if (!cnt) return r;
        switch (rgop) {
        case 0: { const int c = cnt % bits;
                  r = (dw)(((r << c) | (r >> (bits - c))) & msk); fl.setCF(r & 1); break; }
        case 1: { const int c = cnt % bits;
                  r = (dw)(((r >> c) | (r << (bits - c))) & msk); fl.setCF((r >> (bits - 1)) & 1); break; }
        case 2: case 3: { const int c = cnt % (bits + 1);
                  dd e = (dd)r | ((dd)(s->CF ? 1 : 0) << bits);
                  const dd em = (1u << (bits + 1)) - 1;
                  e = (rgop == 2) ? ((e << c) | (e >> (bits + 1 - c))) & em
                                  : ((e >> c) | (e << (bits + 1 - c))) & em;
                  fl.setCF((e >> bits) & 1);
                  r = (dw)(e & msk); break; }
        default:
            if (cnt >= bits) {
                fl.setCF(false);
                r = (rgop == 7 && (d & (1u << (bits - 1)))) ? msk : 0;
            } else if (rgop == 4 || rgop == 6) {
                fl.setCF((r >> (bits - cnt)) & 1);
                r = (dw)((r << cnt) & msk);
            } else if (rgop == 5) {
                fl.setCF((r >> (cnt - 1)) & 1);
                r = (dw)(r >> cnt);
            } else {
                fl.setCF((r >> (cnt - 1)) & 1);
                const int sv = (bytes == 1) ? (int)(int8_t)r : (int)(int16_t)r;
                r = (dw)(sv >> cnt) & msk;
            }
            break;
        }
        set_logic_flags(bytes, r, fl);
        return r;
    };

    auto sel_to_key = [&](dw sgm) -> dd {
        if (sgm & 4) {
            const dd lin = m2c_ldt_get_lin(sgm);
            if (lin) return lin >> 4;
        }
        /* Not a live selector: NE images below 0x4000 store plain
         * paragraphs (data inits, self-patched thunks) whose value can
         * alias the LDT-indicated form.  Treat it as a paragraph. */
        return sgm;
    };

    /* Emulate a real x86 call: push the proper return frame (marked like
     * CALL_), run the callee through the aggregate dispatcher, then resume
     * interpreting at the return address.  The callee's retf/retn pops the
     * marked slot and returns true, handing control back here at pc. */
    dw opc_pc = 0;                 /* offset of the opcode being interpreted */
    auto call_disp = [&](dd agg, bool far_frame) -> bool {
        if (far_frame) push(cur);   /* executing segment acts as cs */
        m2c::NativeCallDepthScope native_call_depth_scope;
        m2c::suppress_native_return_push_transfer = true;
        push(pc);
        m2c::suppress_native_return_push_transfer = false;
        const size_t mid = m2c::mark_native_return(s, (dw)s->ss, (dw)s->esp,
                                                   (m2c::MWORDSIZE)pc);
        if (!__dispatch_call_ext((m2c::_offsets)agg, s)) {
            m2c::discard_native_return(mid);
            return false;
        }
        return true;
    };

    auto finish_ret = [&](bool far, dw nargs) -> bool {
        const dw rss = (dw)s->ss;
        const dw rsp = (dw)s->esp;
        const dd ret_site = ((dd)cur << 16) | (dd)opc_pc;
        dw ip = pop();
        size_t mdepth = m2c::native_return_call_depth;
        size_t mid = 0;
        int mmode = 0;
        bool native_ret =
            m2c::consume_native_return(s, rss, rsp, (m2c::MWORDSIZE)ip, &mdepth, &mid, &mmode);
        if (!native_ret) {
            native_ret = m2c::take_native_return_value(s, (m2c::MWORDSIZE)ip, &ip, &mid);
            if (native_ret) mmode = 4;
        }
        dw ncs = far ? pop() : cur;
        if (nargs)
            s->esp = (s->esp & 0xffff0000u) | (dw)((dw)s->esp + nargs);
        m2c::last_ret_popped = (far ? 4 : 2) + (int)nargs;
        m2c::last_ret_mark_id = mid;
        m2c::last_ret_mark_mode = mmode;
        m2c::last_ret_site = ret_site;
        if (native_ret) {
            if (mdepth < m2c::native_return_call_depth)
                throw m2c::StackPop(m2c::native_return_call_depth - mdepth);
            return true;
        }
        const dd para = sel_to_key(ncs);
        if (!para) {
            log_error("thunk: ret to bad cs %04x:%04x\n", ncs, ip);
            return true;
        }
        return __dispatch_call((m2c::_offsets)((para << 16) | (dd)ip), s);
    };

    for (int steps = 0; steps < 4000; ++steps) {
        if (((dd)cur << 4) + pc + 8 >= 0x3d000) { fprintf(stderr,"[thunk] bound %04x:%04x\n",cur,pc); return false; }
        dw segovr = 0;
        opc_pc = pc;
        db op = rd8i();
        while (true) {
            if (op == 0x26)      { segovr = (dw)s->es; op = rd8i(); continue; }
            if (op == 0x2e)      { segovr = cur; op = rd8i(); continue; }
            if (op == 0x36)      { segovr = (dw)s->ss; op = rd8i(); continue; }
            if (op == 0x3e)      { segovr = (dw)s->ds; op = rd8i(); continue; }
            if (op == 0xf0 || op == 0xf2 || op == 0xf3 || op == 0x90) { op = rd8i(); continue; }
            break;
        }

        /* ---- returns ---- */
        if (op == 0xcb) return finish_ret(true, 0);
        if (op == 0xca) { dw n = rd16i(); return finish_ret(true, n); }
        if (op == 0xc3) return finish_ret(false, 0);
        if (op == 0xc2) { dw n = rd16i(); return finish_ret(false, n); }

        /* ---- calls ---- */
        if (op == 0xe8) {                                    /* call rel16 */
            const int16_t rel = (int16_t)rd16i();
            if (gth_trace) fprintf(stderr, "[thunk] %04x:%04x calln -> %04x:%04x\n", cur, opc_pc, cur, (dw)(pc+rel));
            if (!call_disp(((dd)cur << 16) | (dw)(pc + rel), false)) { fprintf(stderr,"[thunk] calln failed\n"); return false; }
            continue;
        }
        if (op == 0x9a) {                                    /* callf ptr16:16 */
            const dw o16 = rd16i(); const dw s16 = rd16i();
            const dd tpara = sel_to_key(s16);
            if (gth_trace) fprintf(stderr, "[thunk] %04x:%04x callf %04x:%04x -> para %04x\n", cur, opc_pc, s16, o16, (dw)tpara);
            if (!gth_is_import(s16, o16) && !tpara) { log_error("thunk: callf bad seg %04x\n", s16); return false; }
            if (!call_disp((tpara << 16) | (dd)o16, true)) { fprintf(stderr,"[thunk] callf failed\n"); return false; }
            continue;
        }
        if (op == 0xeb) { pc = (dw)(pc + (int8_t)rd8i()); continue; }       /* jmp8 */
        if (op == 0xe9) { const int16_t r = (int16_t)rd16i(); pc = (dw)(pc + r); continue; }
        if (op == 0xea) { const dw o = rd16i(); const dw g = rd16i();
                          if (gth_is_import(g, o)) return gth_import(o & 0x7fff, s); /* tail call */
                          const dd para = sel_to_key(g);
                          if (!para) { log_error("thunk: jmpf bad seg %04x\n", g); return false; }
                          cur = (dw)para; pc = o; continue; }              /* jmpf */

        if (op >= 0x70 && op <= 0x7f) {                      /* jcc8 */
            const int8_t dd8 = (int8_t)rd8i();
            bool t = false;
            switch (op & 0xf) {
            case 0: t = s->OF; break;  case 1: t = !s->OF; break;
            case 2: t = s->CF; break;  case 3: t = !s->CF; break;
            case 4: t = s->ZF; break;  case 5: t = !s->ZF; break;
            case 6: t = s->CF || s->ZF; break;
            case 7: t = !(s->CF || s->ZF); break;
            case 8: t = s->SF; break;  case 9: t = !s->SF; break;
            case 0xa: t = s->PF; break; case 0xb: t = !s->PF; break;
            case 0xc: t = s->SF != s->OF; break;
            case 0xd: t = s->SF == s->OF; break;
            case 0xe: t = s->ZF || (s->SF != s->OF); break;
            case 0xf: t = !s->ZF && (s->SF == s->OF); break;
            }
            if (t) pc = (dw)(pc + dd8);
            continue;
        }
        if (op >= 0xe0 && op <= 0xe3) {                      /* loopne/loope/loop/jcxz */
            const int8_t dd8 = (int8_t)rd8i();
            dw cx = gth_r16(s, 1);
            bool t;
            if (op == 0xe3) t = (cx == 0);
            else { cx = (dw)(cx - 1); gth_r16(s, 1) = cx;
                   t = (cx != 0) && (op == 0xe1 ? s->ZF : op == 0xe0 ? !s->ZF : true); }
            if (t) pc = (dw)(pc + dd8);
            continue;
        }

        /* ---- push/pop ---- */
        if (op >= 0x50 && op <= 0x57) { push(gth_r16(s, op - 0x50)); continue; }
        if (op >= 0x58 && op <= 0x5f) { gth_r16(s, op - 0x58) = pop(); continue; }
        if (op == 0x06) { push((dw)s->es); continue; }
        if (op == 0x16) { push((dw)s->ss); continue; }
        if (op == 0x1e) { push((dw)s->ds); continue; }
        if (op == 0x0e) { push(cur); continue; }             /* push cs */
        if (op == 0x07) { s->es = pop(); continue; }
        if (op == 0x17) { s->ss = pop(); continue; }
        if (op == 0x1f) { s->ds = pop(); continue; }
        if (op == 0x68) { push(rd16i()); continue; }
        if (op == 0x6a) { push((dw)(int8_t)rd8i()); continue; }
        if (op == 0x9c) { push((dw)fl.getvalue()); continue; }
        if (op == 0x9d) { fl.setvalue(pop()); continue; }

        /* ---- mov/xchg immediates ---- */
        if (op >= 0xb0 && op <= 0xb7) { set_r8(op - 0xb0, rd8i()); continue; }
        if (op >= 0xb8 && op <= 0xbf) { gth_r16(s, op - 0xb8) = rd16i(); continue; }
        if (op >= 0x91 && op <= 0x97) { dw& a = gth_r16(s,0); dw& r = gth_r16(s, op-0x90); dw t=a; a=r; r=t; continue; }

        /* ---- inc/dec/convert/frame ---- */
        if (op >= 0x40 && op <= 0x47) { dw& r = gth_r16(s, op - 0x40); r = (dw)(r+1); flags16(r); continue; }
        if (op >= 0x48 && op <= 0x4f) { dw& r = gth_r16(s, op - 0x48); r = (dw)(r-1); flags16(r); continue; }
        if (op == 0x98) { gth_r16(s,0) = (s->eax & 0x80) ? (dw)(0xff00|(s->eax&0xff)) : (dw)(s->eax&0xff); continue; }
        if (op == 0x99) { gth_r16(s,2) = (s->eax & 0x8000) ? 0xffff : 0; continue; }
        if (op == 0xc9) { s->esp = (s->esp & 0xffff0000u) | (dw)s->ebp;
                          gth_r16(s,5) = pop(); continue; }                  /* leave */
        if (op == 0xc8) { const dw n = rd16i(); (void)rd8i();                /* enter n,0 */
                          push((dw)s->ebp);
                          s->ebp = (s->ebp & 0xffff0000u) | (dw)s->esp;
                          if (n) s->esp = (s->esp & 0xffff0000u) | (dw)((dw)s->esp - n);
                          continue; }

        /* ---- accumulator-immediate forms ---- */
        if ((op & 0xc7) == 0x04 || (op & 0xc7) == 0x05) {
            const int rgop = op >> 3;
            if (op & 1) { dw imm = rd16i(); dw v = alu(rgop, gth_r16(s,0), imm, 2); if (rgop != 7) gth_r16(s,0) = v; }
            else        { dw imm = rd8i();  dw v = alu(rgop, get_r8(0), imm, 1); if (rgop != 7) set_r8(0, v); }
            continue;
        }

        /* ---- flag ops (harmless in stub context) ---- */
        if (op == 0xf8) { s->CF = false; continue; }
        if (op == 0xf9) { s->CF = true;  continue; }
        if (op == 0xfa || op == 0xfb) continue;              /* cli/sti */
        if (op == 0xfc) { s->DF = false; continue; }
        if (op == 0xfd) { s->DF = true;  continue; }

        /* ---- string ops ---- */
        if (op == 0xa4 || op == 0xa5) {                      /* movs */
            const int w = op & 1;
            dw off = w ? 2 : 1;
            db* dst = raddr_((dw)s->es, gth_r16(s,7));
            const db* src = raddr_(segovr ? segovr : (dw)s->ds, gth_r16(s,6));
            if (w) { dw v; memcpy(&v, src, 2); memcpy(dst, &v, 2); } else *dst = *src;
            const int dir = s->DF ? -(int)off : (int)off;
            gth_r16(s,6) = (dw)(gth_r16(s,6) + dir);
            gth_r16(s,7) = (dw)(gth_r16(s,7) + dir);
            continue;
        }
        if (op == 0xaa || op == 0xab) {                      /* stos */
            const int w = op & 1;
            db* dst = raddr_((dw)s->es, gth_r16(s,7));
            if (w) { dw v = gth_r16(s,0); memcpy(dst, &v, 2); } else *dst = (db)s->eax;
            gth_r16(s,7) = (dw)(gth_r16(s,7) + (s->DF ? -(w?2:1) : (w?2:1)));
            continue;
        }
        if (op == 0xac || op == 0xad) {                      /* lods */
            const int w = op & 1;
            const db* src = raddr_(segovr ? segovr : (dw)s->ds, gth_r16(s,6));
            if (w) { dw v; memcpy(&v, src, 2); gth_r16(s,0) = v; } else set_r8(0, *src);
            gth_r16(s,6) = (dw)(gth_r16(s,6) + (s->DF ? -(w?2:1) : (w?2:1)));
            continue;
        }

        /* ---- modrm instructions ---- */
        const db modrm = rd8i();
        const int mod = modrm >> 6, rg = (modrm >> 3) & 7, rm = modrm & 7;
        /* decode EA once (consumes disp bytes via pc) */
        dw ea_off = 0, ea_seg = 0;
        const bool isreg = (mod == 3);
        if (!isreg) {
            dw base16 = 0; bool use_ss = false;
            switch (rm) {
            case 0: base16 = (dw)(gth_r16(s,3) + gth_r16(s,6)); break;
            case 1: base16 = (dw)(gth_r16(s,3) + gth_r16(s,7)); break;
            case 2: base16 = (dw)(gth_r16(s,5) + gth_r16(s,6)); use_ss = true; break;
            case 3: base16 = (dw)(gth_r16(s,5) + gth_r16(s,7)); use_ss = true; break;
            case 4: base16 = gth_r16(s,6); break;
            case 5: base16 = gth_r16(s,7); break;
            case 6: if (mod == 0) base16 = rd16i();
                    else { base16 = gth_r16(s,5); use_ss = true; } break;
            case 7: base16 = gth_r16(s,3); break;
            }
            if (mod == 1) base16 = (dw)(base16 + (int8_t)rd8i());
            else if (mod == 2) base16 = (dw)(base16 + rd16i());
            ea_off = base16;
            ea_seg = segovr ? segovr : (use_ss ? (dw)s->ss : (dw)s->ds);
        }
        auto rdw = [&]() -> dw { return isreg ? gth_r16(s,rm) : rdm16(ea_seg, ea_off); };
        auto wrw = [&](dw v) { if (isreg) gth_r16(s,rm) = v; else wrm16(ea_seg, ea_off, v); };
        auto rdb = [&]() -> dw { return isreg ? get_r8(rm) : (dw)*raddr_(ea_seg, ea_off); };
        auto wrb = [&](dw v) { if (isreg) set_r8(rm, v); else *raddr_(ea_seg, ea_off) = (db)v; };

        bool ok = true;
        switch (op) {
        case 0x88: wrb(get_r8(rg)); break;
        case 0x89: wrw(gth_r16(s, rg)); break;
        case 0x8a: set_r8(rg, rdb()); break;
        case 0x8b: gth_r16(s, rg) = rdw(); break;
        case 0x8c: wrw(gth_sg(s, rg & 3)); break;
        case 0x8e: gth_sg(s, rg & 3) = rdw(); break;
        case 0x8d: if (!isreg) gth_r16(s, rg) = ea_off; else ok = false; break;
        case 0x8f: if (rg == 0 && !isreg) wrw(pop()); else ok = false; break;
        case 0xc4: if (!isreg) { gth_r16(s, rg) = rdw(); s->es = rdm16(ea_seg, (dw)(ea_off + 2)); } else ok = false; break;  /* les */
        case 0xc5: if (!isreg) { gth_r16(s, rg) = rdw(); s->ds = rdm16(ea_seg, (dw)(ea_off + 2)); } else ok = false; break;  /* lds */
        case 0x86: { dw v = rdb(); wrb(get_r8(rg)); set_r8(rg, v); } break;
        case 0x87: { dw v = rdw(); wrw(gth_r16(s, rg)); gth_r16(s, rg) = v; } break;
        case 0xc6: { dw v = rd8i(); wrb(v); } break;
        case 0xc7: { dw v = rd16i(); wrw(v); } break;
        case 0x00: wrb(alu(0, rdb(), get_r8(rg), 1)); break;
        case 0x01: wrw(alu(0, rdw(), gth_r16(s, rg), 2)); break;
        case 0x02: set_r8(rg, alu(0, get_r8(rg), rdb(), 1)); break;
        case 0x03: gth_r16(s,rg) = alu(0, gth_r16(s,rg), rdw(), 2); break;
        case 0x08: wrb(alu(1, rdb(), get_r8(rg), 1)); break;
        case 0x09: wrw(alu(1, rdw(), gth_r16(s, rg), 2)); break;
        case 0x0a: set_r8(rg, alu(1, get_r8(rg), rdb(), 1)); break;
        case 0x0b: gth_r16(s,rg) = alu(1, gth_r16(s,rg), rdw(), 2); break;
        case 0x10: wrb(alu(2, rdb(), get_r8(rg), 1)); break;
        case 0x11: wrw(alu(2, rdw(), gth_r16(s, rg), 2)); break;
        case 0x12: set_r8(rg, alu(2, get_r8(rg), rdb(), 1)); break;
        case 0x13: gth_r16(s,rg) = alu(2, gth_r16(s,rg), rdw(), 2); break;
        case 0x18: wrb(alu(3, rdb(), get_r8(rg), 1)); break;
        case 0x19: wrw(alu(3, rdw(), gth_r16(s, rg), 2)); break;
        case 0x1a: set_r8(rg, alu(3, get_r8(rg), rdb(), 1)); break;
        case 0x1b: gth_r16(s,rg) = alu(3, gth_r16(s,rg), rdw(), 2); break;
        case 0x20: wrb(alu(4, rdb(), get_r8(rg), 1)); break;
        case 0x21: wrw(alu(4, rdw(), gth_r16(s, rg), 2)); break;
        case 0x22: set_r8(rg, alu(4, get_r8(rg), rdb(), 1)); break;
        case 0x23: gth_r16(s,rg) = alu(4, gth_r16(s,rg), rdw(), 2); break;
        case 0x28: wrb(alu(5, rdb(), get_r8(rg), 1)); break;
        case 0x29: wrw(alu(5, rdw(), gth_r16(s, rg), 2)); break;
        case 0x2a: set_r8(rg, alu(5, get_r8(rg), rdb(), 1)); break;
        case 0x2b: gth_r16(s,rg) = alu(5, gth_r16(s,rg), rdw(), 2); break;
        case 0x30: wrb(alu(6, rdb(), get_r8(rg), 1)); break;
        case 0x31: wrw(alu(6, rdw(), gth_r16(s, rg), 2)); break;
        case 0x32: set_r8(rg, alu(6, get_r8(rg), rdb(), 1)); break;
        case 0x33: gth_r16(s,rg) = alu(6, gth_r16(s,rg), rdw(), 2); break;
        case 0x38: (void)alu(7, rdb(), get_r8(rg), 1); break;
        case 0x39: (void)alu(7, rdw(), gth_r16(s, rg), 2); break;
        case 0x3a: (void)alu(7, get_r8(rg), rdb(), 1); break;
        case 0x3b: (void)alu(7, gth_r16(s,rg), rdw(), 2); break;
        case 0x84: (void)alu(4, rdb(), get_r8(rg), 1); break;
        case 0x85: (void)alu(4, rdw(), gth_r16(s, rg), 2); break;
        case 0xff:
            switch (rg) {
            case 0: wrw(alu(0, rdw(), 1, 2)); break;
            case 1: wrw(alu(5, rdw(), 1, 2)); break;
            case 2: if (!call_disp(((dd)cur << 16) | rdw(), false)) return false; break;
            case 3: { dw o = rdw(); dw g = rdm16(ea_seg, (dw)(ea_off + 2));
                      dd para = sel_to_key(g);
                      if (gth_trace) fprintf(stderr, "[thunk] %04x:%04x callf [mem %04x:%04x] -> %04x:%04x para %04x\n", cur, opc_pc, ea_seg, ea_off, g, o, (dw)para);
                      if (!gth_is_import(g, o) && !para) { ok = false; break; }
                      if (!call_disp((para << 16) | (dd)o, true)) return false; } break;
            case 4: pc = rdw(); break;
            case 5: { dw o = rdw(); dw g = rdm16(ea_seg, (dw)(ea_off + 2));
                      if (gth_is_import(g, o)) return gth_import(o & 0x7fff, s);
                      dd para = sel_to_key(g); if (!para) { ok = false; break; }
                      cur = (dw)para; pc = o; } break;
            case 6: push(rdw()); break;
            default: ok = false;
            }
            break;
        case 0xc0: case 0xc1: { const int c = rd8i();
            if (op == 0xc0) wrb(shf(rg, rdb(), c, 1)); else wrw(shf(rg, rdw(), c, 2)); } break;
        case 0xd0: case 0xd1: case 0xd2: case 0xd3: {
            const int c = (op <= 0xd1) ? 1 : (gth_r16(s, 1) & 0x1f);
            if (!(op & 1)) wrb(shf(rg, rdb(), c, 1)); else wrw(shf(rg, rdw(), c, 2)); } break;
        case 0x80: case 0x81: case 0x83: {
            dw imm;
            if (op == 0x81) imm = rd16i(); else imm = (dw)(int8_t)rd8i();
            if (op == 0x80) { dw v = alu(rg, rdb(), imm, 1); if (rg != 7) wrb(v); }
            else            { dw v = alu(rg, rdw(), imm, 2); if (rg != 7) wrw(v); }
        } break;
        case 0xf6: case 0xf7: {
            const int byt = (op == 0xf6);
            dw d = byt ? rdb() : rdw();
            switch (rg) {
            case 0: { dw v = byt ? rd8i() : rd16i(); (void)alu(4, d, v, byt ? 1 : 2); } break; /* test */
            case 2: d = (dw)~d; if (byt) wrb(d); else wrw(d); break;
            case 3: d = (dw)-d; fl.setCF(d != 0); set_logic_flags(byt?1:2, d, fl); if (byt) wrb(d); else wrw(d); break;
            default: ok = false;
            }
        } break;
        default:
            ok = false;
        }
        if (!ok) {
            if (gth_trace) fprintf(stderr, "[thunk] unhandled opcode %02x at %04x:%04x\n", op, cur, opc_pc);
            log_error("thunk: unhandled opcode %02x at %04x:%04x\n", op, cur, opc_pc);
            return false;
        }
    }
    log_error("thunk: step limit at %04x:%04x\n", cur, pc);
    return false;
}
} // namespace m2c
