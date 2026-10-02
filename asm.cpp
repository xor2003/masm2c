/*
MIT License

Copyright (c) 2017 Franck GOTTHOLD, xor2003

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
#include "asm.h"

#include <exception>

#ifndef __BORLANDC__
 #ifndef _WIN32
  #include <sys/select.h>
  #include <sys/time.h>
  #include <unistd.h>
  #include <fcntl.h>
  #include <dirent.h>
  #include <strings.h>
 #endif
 #ifndef __DJGPP__
  #ifndef NOSDL
   #include <SDL2/SDL.h>
  #endif
 #endif
// #include <thread>
#endif

#ifdef __DJGPP__
 #include <pc.h>
 #include <dos.h>
 #include <dpmi.h>
 #include <go32.h>
 #include <sys/farptr.h>
#endif

#ifdef _WIN32
//#include <windows.h>
#endif

//#include <assert.h>
//#include <time.h>
#include <cassert>
#include <cerrno>
#include <string>
#include <ctime>
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <csignal>
#include <thread>
#include <vector>

#ifndef M2C_LOAD_SEG
#define M2C_LOAD_SEG 0x192
#endif

// DOS program segment prefix paragraph. For hosted .COM-style runs it equals
// M2C_LOAD_SEG; for EXE-style two-segment programs the code loads at
// M2C_LOAD_SEG while the PSP lives one paragraph below it.
#ifndef M2C_PSP_SEG
#define M2C_PSP_SEG M2C_LOAD_SEG
#endif

#ifndef NOCURSES
#include <curses.h>
#endif

extern bool gameintr100(m2c::_offsets, struct m2c::_STATE*) __attribute__((weak));
extern bool gameintr20(m2c::_offsets, struct m2c::_STATE*) __attribute__((weak));
extern db* key __attribute__((weak));
extern dw* ticker __attribute__((weak));
extern dw* frames __attribute__((weak));
extern dw* countdown __attribute__((weak));
extern dd* elapsedtime __attribute__((weak));
extern db vga_rgb_data __attribute__((weak));
extern db vga_panel __attribute__((weak));
extern db vga_panel1 __attribute__((weak));
extern db setpaletteflag __attribute__((weak));

/* https://commons.wikimedia.org/wiki/File:Table_of_x86_Registers_svg.svg */


//struct uc_x86_state {
//    REGDEF_nol(flags);
//};



/*
#undef REGDEF_hl
#undef REGDEF_l
#undef REGDEF_bwd
#undef REGDEF_nol

struct __fl
{
	bool _CF:1;
	bool res1:1;
	bool _PF:1;
	bool res2:1;
	bool _AF:1;
	bool res3:1;
	bool _ZF:1;
	bool _SF:1;
	bool _TF:1;
	bool _IF:1;
	bool _DF:1;
	bool _OF:1;
	int _IOPL:2;
	bool _NT:1;
	bool res4:1;
	bool res5:16;
};
static struct __fl __eflags;

#define CF __eflags._CF
#define ZF __eflags._ZF
#define DF __eflags._DF
#define SF __eflags._SF
*/
// SDL2 VGA
#ifndef NOSDL
 #if SDL_MAJOR_VERSION == 2
    SDL_Renderer *renderer;
    SDL_Window *window;
    static bool vga_render_dirty;
    static unsigned vga_render_writes;
    static int vga_logical_width = 320;
    static int vga_logical_height = 200;
    static const unsigned VGA_RENDER_WRITE_FLUSH_THRESHOLD = 8 * 1024;
    static const size_t VGA_WINDOW_SIZE = 0x20000;
    static db vgaPlanarPixels[640 * 200];
    static db vgaMode13Pixels[VGA_WINDOW_SIZE * 4];
    static db vgaReadLatch[4];
    static db vgaPendingReadLatch[4][4];
    static size_t vgaPendingReadLatchCount;
    static size_t vgaPendingReadLatchNext;
    static uint32_t vgaSdlFrame[640 * 200];
    static SDL_Texture *vgaTexture;

db vgaRamPaddingBefore[VGARAM_SIZE];
db vgaRam[VGARAM_SIZE];
db vgaRamPaddingAfter[VGARAM_SIZE];
 #endif
#endif

  bool from_callf=false;

namespace m2c {
  int last_ret_popped=-1;
  size_t last_ret_mark_id=0;
  int last_ret_mark_mode=0;
  dd last_ret_site=0;

#ifdef M2CDEBUG
  /* Per-instruction tracing is expensive enough to freeze a program, so it
   * is strictly opt-in: M2CDEBUG only compiles the support in, M2C_DEBUG
   * must be set explicitly to turn it on (default off). */
  size_t debug = std::getenv("M2C_DEBUG") ? (size_t)atoi(std::getenv("M2C_DEBUG")) : 0;
#else
  size_t debug = 0;
#endif
bool defered_irqs=false;
  size_t counter = 0;
    std::vector<NativeReturnMark> native_return_marks;
    std::vector<NativeReturnMark> native_return_values;
    size_t native_return_next_id = 0;
    size_t native_return_call_depth = 0;
    bool suppress_native_return_push_transfer = false;

    db _indent=0;
    const char *_str="";
    bool fix_segs(){return true;}
void interpret_unknown_callf(dw cs, dd eip, db source){assert(0);}
    __attribute__((weak)) db* linked_code_segment_raddr(dw, dw){return nullptr;}
    __attribute__((weak)) db* linked_data_segment_raddr(dw, dw){return nullptr;}
    __attribute__((weak)) void set_segment_register(dw& reg, dw value){reg = value;}
    __attribute__((weak)) void copy_linked_program_segment_prefix(dw, const void*, size_t) {}
    // Translated TANDYSND overlay module (tnd_module.cpp). tnd_seg is the EXEC
    // load segment of TANDYSND.EXE; tnd_code_seg is its code segment (+7 paras,
    // past the 0x70-byte header/seg000). Weak stubs: overridden by the real
    // module when it is linked, and stay inert (tnd_code_seg==0) otherwise.
    __attribute__((weak)) dw tnd_seg = 0;
    __attribute__((weak)) dw tnd_code_seg = 0;
    __attribute__((weak)) bool tnd_overlay_call(dd, _STATE*) { return false; }
    // Private image buffer for the translated overlay (see asm.h). tnd_img_paras
    // is the mapped span in paragraphs; 0 keeps the raddr_ route inert.
    db tnd_img[0x8000] = {};
    dw tnd_img_paras = 0;
    // BIOS ROM shadow for the F000 segment (see asm.h). Zeroed by default; the
    // Tandy signature bytes are planted only when the tnd module is linked.
    db m2c_bios_rom[0x10000] = {};
    // tnd_module.cpp defines this strong=1 so the game auto-detects a
    // Tandy/PCjr BIOS (F000:FFFE==0xFF && F000:C000==0x21) and loads TANDYSND.EXE.
    __attribute__((weak)) bool tnd_present = false;
    bool host_try_overlay_retf(_offsets __disp, _STATE* _state, bool* out_result);
    __attribute__((weak)) bool m2c_guest_thunk(_offsets __disp, _STATE* _state) {
        (void)__disp; (void)_state;
        return false;
    }
    __attribute__((weak)) bool dispatch_external_code(_offsets __disp, _STATE* _state, bool* handled) {
        bool res = true;
        if (host_try_overlay_retf(__disp, _state, &res)) {
            if (handled) {
                *handled = true;
            }
            return res;
        }
        if (handled) {
            *handled = false;
        }
        return true;
    }


ShadowStack shadow_stack;

x87_t fpu;

long double fpu_ld80(const void* p) {
    if (sizeof(long double) >= 10) {
        long double v = 0;
        memcpy(&v, p, 10);
        return v;
    }
    // Portable decode for hosts where long double is not 80-bit x87 ext.
    const db* b = (const db*)p;
    uint64_t mant;
    memcpy(&mant, b, 8);
    int se = b[8] | (b[9] << 8);
    int sign = se >> 15;
    int exp = se & 0x7fff;
    if (exp == 0 && mant == 0) return sign ? -0.0L : 0.0L;
    return (long double)std::ldexp((long double)mant, exp - 16383 - 63) * (sign ? -1.0L : 1.0L);
}

void fpu_st80(void* p, long double v) {
    db* b = (db*)p;
    if (sizeof(long double) >= 10) {
        memcpy(b, &v, 10);
        return;
    }
    // Portable encode to 80-bit x87 extended.
    int sign = std::signbit(v);
    long double a = std::fabs(v);
    uint64_t mant = 0;
    int se = 0;
    if (a != 0 && std::isfinite(a)) {
        int exp;
        long double f = std::frexp(a, &exp);          // a = f * 2^exp, f in [0.5,1)
        mant = (uint64_t)std::ldexp(f, 64);           // 1 bit int + 63 fraction
        se = exp - 1 + 16383;
    }
    memcpy(b, &mant, 8);
    b[8] = se & 0xff;
    b[9] = ((se >> 8) & 0x7f) | (sign ? 0x80 : 0);
}

void fpu_init() {
    memset(&fpu, 0, sizeof(fpu));
    fpu.cw = 0x037f;
    std::fesetround(FE_TONEAREST);
}

//db vgaPalette[256*3];
#include "vgapal.h"
// Legacy selector table — superseded by m2c_ldt (emulated LDT).  Kept
// because historical asm_16.h copies reference `selectors[segment]` under
// _PROTECTED_MODE; the shared runtime no longer uses it.
dd selectorsPointer;
dd selectors[NB_SELECTORS];

dd heapPointer;
struct find_t;
static db defaultDiskTransferArea[128] = {};
struct find_t * diskTransferAddr = reinterpret_cast<find_t *>(defaultDiskTransferArea);

/* Win16 / protected-mode descriptor table (emulated LDT).  Under real
   protected mode, segment registers hold *selectors*: 16-bit values encoded
   as (index<<3 | TI<<2 | RPL).  Each selector indexes a descriptor
   {base, limit, rights}.  We emulate that:

   - m2c_ldt[] is the descriptor store, indexed by selector>>3.
   - base is a HOST pointer: either inside `m` (aliases of real-mode
     segments / the loaded image) or a malloc'd block (DPMI/RTM allocations).
   - lin is the guest-visible linear base (m-offset for m-aliases, a
     synthetic address for owned blocks).
   - Real-mode paragraphs in segregs are not descriptors: they resolve
     through the `m` paragraph view in raddr_().

   Allocated selectors are encoded (idx<<3 | 7) starting at m2c_pm_sel_base
   (default 0x4000 -> index 2048), above normal image paragraphs, so plain
   paragraph values never alias a used descriptor.  Because the encoding is
   the real one, guest descriptor arithmetic works: sel+8 (__AHINCR) steps
   to the next descriptor and sel>>3 (__AHSHIFT) yields the table index. */
PmDesc m2c_ldt[NB_LDT];
static unsigned m2c_ldt_next_idx;   // allocation cursor (index)
// First allocated selector *value*. Weak so a program can place its
// descriptor space above its loaded image; default suits images < 256KB.
__attribute__((weak)) dw m2c_pm_sel_base = 0x4000;
static unsigned m2c_pm_next_linear = 0x1000000;  // synthetic linear base for owned blocks

int m2c_ldt_idx(dw sel) { return (sel >> 3) & (NB_LDT - 1); }

// Allocate n consecutive descriptors; returns the base selector value
// (idx<<3 | 7) or 0 on exhaustion.  Entries are marked used with no base —
// the client sets base/limit via INT31 0007/0008 or the m2c_ldt_* helpers.
dw m2c_ldt_alloc(int n) {
	if (!m2c_ldt_next_idx) m2c_ldt_next_idx = m2c_ldt_idx(m2c_pm_sel_base);
	unsigned start = m2c_ldt_next_idx;
	if (start + n >= NB_LDT) {
		log_error("ldt: out of descriptors (need %d at %u)\n", n, start);
		return 0;
	}
	for (int i = 0; i < n; ++i) {
		PmDesc& d = m2c_ldt[start + i];
		if (d.used) { // shouldn't happen past the cursor; be loud
			log_error("ldt: descriptor %u already used\n", start + i);
		}
		d.base = nullptr;
		d.limit = 0xffff;
		d.rights = 0x00f3;  // data, read/write, accessed (DPMI default)
		d.lin = 0;
		d.used = 1;
		d.owned = 0;
	}
	m2c_ldt_next_idx = start + n;
	return (dw)((start << 3) | 7);
}

void m2c_ldt_free(dw sel) {
	int idx = m2c_ldt_idx(sel);
	PmDesc& d = m2c_ldt[idx];
	if (!d.used) return;
	if (d.owned) {
		db* blk = d.base;
		dd ext = d.extent ? d.extent : 0x10000;
		free(blk);
		// Clear every descriptor aliasing the freed block.
		for (int i = 0; i < NB_LDT; ++i) {
			if (m2c_ldt[i].used && m2c_ldt[i].base >= blk &&
			    m2c_ldt[i].base < blk + ext)
				m2c_ldt[i] = PmDesc{};
		}
	} else {
		d = PmDesc{};
	}
}

// `struct Memory` is program-defined and incomplete here; its layout ends
// with the `heap` array (a link-bound reference into m), so the usable
// extent of `m` linear addresses is (&heap - &m) + HEAP_SIZE.
static inline dd m2c_m_extent() {
	return (dd)((db*)&heap - (db*)&m) + HEAP_SIZE;
}

// Guest linear base for INT31 0006: m-offset for m-aliased descriptors,
// the recorded synthetic base for owned regions.
dd m2c_ldt_get_lin(dw sel) {
	const PmDesc& d = m2c_ldt[m2c_ldt_idx(sel)];
	if (!d.base) return d.lin;
	if (d.base >= (db*)&m && d.base < (db*)&m + m2c_m_extent())
		return (dd)(d.base - (db*)&m);
	return d.lin;
}

// Allocate a 64KB-backed region and return its selector.  Real selectors
// cover the full 64KB regardless of the requested size — guest code may
// legally touch any 16-bit offset — so the host block is always 64KB.
dw m2c_pm_alloc_paras(dw paras) {
	dw sel = m2c_ldt_alloc(1);
	if (!sel) {
		log_error("pm alloc: out of descriptors (req=%04x)\n", (unsigned)paras);
		return 0;
	}
	db* p = static_cast<db*>(calloc(1, 0x10000));
	if (!p) { m2c_ldt_free(sel); return 0; }
	PmDesc& d = m2c_ldt[m2c_ldt_idx(sel)];
	d.base = p;
	d.limit = 0xffff;
	d.lin = m2c_pm_next_linear;
	d.extent = 0x10000;
	m2c_pm_next_linear += 0x10000;
	d.owned = 1;
	log_debug2("pm alloc req=%04x -> sel=%04x lin=%x\n", (unsigned)paras, sel, d.lin);
	return sel;
}

void m2c_pm_free(dw sel) { m2c_ldt_free(sel); }

// Under the protected-mode memory model, `seg X` must produce a *selector*:
// value stored into ds/es/ss/cs, passed to DPMI, or written by NE fixups.
// Resolve a paragraph to a descriptor aliasing that m storage.  Aliases are
// shared (same paragraph -> same selector) and cached for the common
// repeated `seg DGROUP` pattern.
dw m2c_seg_selector(dw para) {
	dd lin = (dd)para << 4;
	static dw last_para = 0xffff, last_sel = 0;
	if (para == last_para) return last_sel;
	for (int i = 0; i < NB_LDT; ++i) {
		const PmDesc& d = m2c_ldt[i];
		if (d.used && !d.owned && d.lin == lin) {
			last_para = para;
			last_sel = (dw)((i << 3) | 7);
			return last_sel;
		}
	}
	dw sel = m2c_ldt_alloc(1);
	if (!sel) return para;  // LDT exhausted — paragraph still resolves via m
	PmDesc& d = m2c_ldt[m2c_ldt_idx(sel)];
	d.base = (db*)&m + lin;
	d.lin = lin;
	last_para = para;
	last_sel = sel;
	return sel;
}

// `seg X` where X names a segment the NE loader mapped: the descriptor the
// loader created is the guest-visible selector value (ds/ss hold selectors,
// NE fixups store selectors), so data initializers and `seg` expressions
// must agree with them.  Paragraphs with no descriptor keep their real-mode
// identity, so DOS programs see no behaviour change.  Lookup only — unlike
// m2c_seg_selector this never allocates, and misses are not cached so it is
// safe to call before the loader runs.
dw m2c_seg_selector_or_para(dw para) {
	const dd lin = (dd)para << 4;
	static dw last_para = 0xffff, last_sel = 0;
	if (para == last_para) return last_sel;
	for (int i = 0; i < NB_LDT; ++i) {
		const PmDesc& d = m2c_ldt[i];
		if (d.used && !d.owned && d.lin == lin) {
			last_para = para;
			last_sel = (dw)((i << 3) | 7);
			return last_sel;
		}
	}
	return para;
}

/* Generic NE (Win16) image loader — shared implementation behind the
   m2c_ne_entry_setup hook.  The caller owns where each segment lives
   (M2cNeSegHost::base/para); this routine does the format work: descriptor
   creation, file-data copies, internal-reference fixups, entry state. */
static dw ne_w(const db* p) { return (dw)(p[0] | (p[1] << 8)); }
static dd ne_d(const db* p) {
	return (dd)p[0] | ((dd)p[1] << 8) | ((dd)p[2] << 16) | ((dd)p[3] << 24);
}

static M2cNeImport s_ne_imports[512];
static char s_ne_mod_names[32][16];
M2cNeImport* m2c_ne_imports = s_ne_imports;
dw m2c_ne_import_count = 0;
const char* m2c_ne_import_mod_name(dw mod_idx) {
	if (!mod_idx || mod_idx > 32 || !s_ne_mod_names[mod_idx - 1][0]) return "?";
	return s_ne_mod_names[mod_idx - 1];
}
static dw ne_import_add(dw mod_idx, dw ord) {
	for (dw i = 0; i < m2c_ne_import_count; ++i)
		if (s_ne_imports[i].mod_idx == mod_idx && s_ne_imports[i].ordinal == ord)
			return i;
	dw idx = m2c_ne_import_count;
	if (idx < sizeof(s_ne_imports) / sizeof(*s_ne_imports)) {
		s_ne_imports[idx].mod_idx = mod_idx;
		s_ne_imports[idx].ordinal = ord;
		++m2c_ne_import_count;
	}
	return idx;
}

bool m2c_ne_load(_STATE* _state, const db* image, dd image_size,
                 M2cNeSegHost* segs) {
	X86_REGREF
	if (!image || image_size < 0x40 || ne_w(image) != 0x5a4d /*'MZ'*/) {
		log_error("NE load: not an MZ image\n");
		return false;
	}
	dd ne = ne_d(image + 0x3c);
	if (ne + 0x40 > image_size || ne_w(image + ne) != 0x454e /*'NE'*/) {
		log_error("NE load: no NE signature\n");
		return false;
	}
	const db* hdr = image + ne;
	const dw ds_idx  = ne_w(hdr + 0x0e);   // automatic data segment
	const dw entry_ip = ne_w(hdr + 0x14);
	const dw cs_idx  = ne_w(hdr + 0x16);
	const dw entry_sp = ne_w(hdr + 0x18);
	const dw ss_idx  = ne_w(hdr + 0x1a);
	const dw nseg    = ne_w(hdr + 0x1c);
	const dw segoff  = ne_w(hdr + 0x22);   // segment table, rel to NE
	const dw shift   = ne_w(hdr + 0x32);   // logical sector shift
	if (!nseg || ne + segoff + nseg * 8 > image_size) {
		log_error("NE load: bad segment table (count=%u)\n", nseg);
		return false;
	}
	const db* stab = hdr + segoff;
	for (int i = 0; i < nseg; ++i) {
		const db* e = stab + i * 8;
		dd  foff  = (dd)ne_w(e) << shift;
		dd  len   = ne_w(e + 2); if (!len) len = 0x10000;
		dw  flags = ne_w(e + 4);
		segs[i].flags = flags;
		if (!segs[i].base && segs[i].para)
			segs[i].base = (db*)&m + ((dd)segs[i].para << 4);
		if (!segs[i].base) {
			log_error("NE load: segment %d has no host storage\n", i + 1);
			return false;
		}
		// File bytes (code images, preinitialized data) into host storage.
		if (foff && foff + len <= image_size)
			memcpy(segs[i].base, image + foff, len);
		// Selector aliasing the segment storage; keep lin = paragraph
		// linear so get-base and the PM-vector IVT mirror stay consistent.
		dw sel = m2c_ldt_alloc(1);
		if (!sel) return false;
		PmDesc& d = m2c_ldt[m2c_ldt_idx(sel)];
		d.base = segs[i].base;
		d.lin = (dd)segs[i].para << 4;
		segs[i].selector = sel;
	}
	// Module-reference table -> imported module names (for diagnostics).
	const dw nmods = ne_w(hdr + 0x1e);
	const db* mrt  = hdr + ne_w(hdr + 0x28);   // module-reference table
	const db* itab = hdr + ne_w(hdr + 0x2a);   // imported names table
	for (dw mi = 0; mi < nmods && mi < 32 && mrt + 2 * mi + 2 <= image + image_size; ++mi) {
		const db* np = itab + ne_w(mrt + 2 * mi);
		dw nl = np[0]; if (nl > 15) nl = 15;
		if (np + 1 + nl <= image + image_size) {
			memcpy(s_ne_mod_names[mi], np + 1, nl);
			s_ne_mod_names[mi][nl] = 0;
		}
	}
	// Relocation records.
	// Non-additive records (flag bit2 clear) are CHAIN records: the stored
	// word at each site holds the offset of the next site and 0xffff ends
	// the list; the record supplies the whole fixup value.  Additive records
	// are single sites whose stored word is an addend to the record target.
	//   rtype&3 == 0  internal ref  -> seg selector / target offset
	//   rtype&3 == 1  imported ordinal / 2 imported name -> sentinel 0000:80NN
	//   rtype&3 == 3  osfixup (x87 emulator patching) -> skipped: real FPU
	for (int i = 0; i < nseg; ++i) {
		const db* e = stab + i * 8;
		dd  foff  = (dd)ne_w(e) << shift;
		dd  len   = ne_w(e + 2); if (!len) len = 0x10000;
		if (!(segs[i].flags & 0x0100)) continue;  // no relocations
		dd rp = foff + len;
		if (rp + 2 > image_size) break;
		dw count = ne_w(image + rp);
		rp += 2;
		for (dw r = 0; r < count && rp + 8 <= image_size; ++r, rp += 8) {
			const db* rec = image + rp;
			const db atype = rec[0];
			const db rtype = rec[1];
			const dw rkind = rtype & 3;
			const bool additive = (rtype & 4) != 0;
			if (rkind == 3) continue;
			dw off = ne_w(rec + 2);
			dw guard = 0;
			if (rkind == 1 || rkind == 2) {
				const dw mod = ne_w(rec + 4);
				const dw ord = ne_w(rec + 6);
				const dw sentinel = (dw)(0x8000 | ne_import_add(mod, ord));
				do {
					db* loc = segs[i].base + off;
					dw link = ne_w(loc);
					switch (atype) {
					case 2: *(dw*)loc = 0; break;                            // seg word -> null
					case 3: *(dw*)loc = sentinel; *(dw*)(loc + 2) = 0; break; // far ptr -> 0000:80NN
					case 5: *(dw*)loc = sentinel; break;                     // off16 -> sentinel
					default: log_error("NE load: import addr type %u\n", atype); break;
					}
					off = additive ? 0xffff : link;
				} while (off != 0xffff && ++guard < 0x8000);
				continue;
			}
			const dw tseg = ne_w(rec + 4);
			const dw toff = ne_w(rec + 6);
			if (!tseg || tseg > nseg) continue;
			const dw tsel = segs[tseg - 1].selector;
			do {
				db* loc = segs[i].base + off;
				dw link = ne_w(loc);
				switch (atype) {
				case 2: *(dw*)loc = tsel; break;                     // selector word
				case 3: *(dw*)loc = toff; *(dw*)(loc + 2) = tsel; break; // far ptr
				case 5: *(dw*)loc = additive ? (dw)(link + toff) : toff; break;
				default:
					log_error("NE load: addr type %u unsupported\n", atype);
				}
				off = additive ? 0xffff : link;
			} while (off != 0xffff && ++guard < 0x8000);
		}
	}
	cs  = segs[cs_idx - 1].selector;
	eip = entry_ip;
	if (ss_idx) { ss = segs[ss_idx - 1].selector; }
	sp  = entry_sp ? entry_sp : (dw)(STACK_SIZE - 4);
	if (ds_idx) { ds = es = segs[ds_idx - 1].selector; }
	log_debug("NE load: entry %04x:%04x stack %04x:%04x ds %04x (%u segs)\n",
	          cs, entry_ip, ss, sp, ds, nseg);
	return true;
}
db* m2c_alloc_segment_raddr(dw segment, dw offset) {
	const PmDesc& d = m2c_ldt[m2c_ldt_idx(segment)];
	// Only values with the LDT table-indicator bit (sel&4) are selectors;
	// plain paragraphs fall through to the `m` view.  Lenient on the limit:
	// blocks are backed by 64KB so every 16-bit offset resolves; the limit
	// is recorded for get/set fidelity.
	if ((segment & 4) && d.used && d.base)
		return d.base + offset;
	return nullptr;
}

// Protected-mode vectors installed via INT31 0203/0205 (CX:EDX = sel:eip).
// Recorded verbatim for faithful get/set round-trips; additionally mirrored
// into the real-mode IVT when the handler selector aliases `m`.
static dw pm_vec_sel[256];
static dd pm_vec_off[256];
static db pm_vec_set[256];

// Compatibility name used by NE/RTM-style translated programs (asm.h).
// Weak so a program harness can substitute its own allocator.
__attribute__((weak)) dw tlink_rtm_alloc_paras(dw paras) { return m2c_pm_alloc_paras(paras); }

// DOS file-handle table: handles 0..4 are the predefined std devices;
// regular files occupy 5..N (like DOS's SFT).
static dw dta_seg = 0;   // guest-visible seg:off of the DTA (as set by AH=1Ah)
static dw dta_off = 0x80;
static FILE * dos_files[0x40] = {};
static const dw DOS_HANDLE_BASE = 5;
static int dos_last_child_rc = 0;
static FILE * dos_std[5] = {};
static FILE * dos_get_file(dw h) {
	if (h < DOS_HANDLE_BASE) {
		// Predefined DOS devices 0..4 (stdin/stdout/stderr/aux/prn). Map to
		// dup'd host stdio so guest dup()/close() on them is harmless.
		if (!dos_std[h]) {
			FILE * sf = (h == 0) ? stdin : (h == 1) ? stdout : (h == 2) ? stderr
				: (h == 3) ? stdout : stderr;
			int fd = dup(fileno(sf));
			int acc = fd >= 0 ? (fcntl(fd, F_GETFL) & O_ACCMODE) : -1;
			const char * sm = acc == O_RDONLY ? "r" : acc == O_WRONLY ? "a" : "r+";
			dos_std[h] = fd >= 0 ? fdopen(fd, sm) : nullptr;
		}
		return dos_std[h];
	}
	if (h - DOS_HANDLE_BASE >= 0x40) return nullptr;
	return dos_files[h - DOS_HANDLE_BASE];
}
static dw dos_alloc_handle(FILE * f) {
	for (dw h = 0; h < 0x40; ++h)
		if (!dos_files[h]) { dos_files[h] = f; return DOS_HANDLE_BASE + h; }
	fclose(f);
	return 0xffff;
}

// DOS file names are case-insensitive. Resolve a guest path against the
// host filesystem component-by-component, folding case via directory
// listing, so "hello.obj" finds "HELLO.OBJ". Returns true on success.
static bool dos_resolve_case(const char *path, char *out, size_t outsz) {
	if (!path || !*path || !out || outsz < 2) return false;
	char buf[1024];
	std::snprintf(buf, sizeof(buf), "%s", path);
	for (char *p = buf; *p; ++p) if (*p == '\\') *p = '/';
	std::string resolved;
	size_t pos = 0;
	if (buf[0] == '/') { resolved = "/"; pos = 1; }
	while (pos <= strlen(buf)) {
		const char *sep = strchr(buf + pos, '/');
		size_t len = sep ? (size_t)(sep - (buf + pos)) : strlen(buf + pos);
		if (len == 0) {
			if (!sep) break;
			pos += 1;
			continue;
		}
		char comp[256];
		if (len >= sizeof(comp)) return false;
		std::memcpy(comp, buf + pos, len);
		comp[len] = 0;
		const char *dir = resolved.empty() ? "." : resolved.c_str();
		// exact match first
		std::string cand = resolved + comp;
		if (access(cand.c_str(), F_OK) != 0) {
			DIR *d = opendir(dir);
			if (!d) return false;
			struct dirent *e;
			bool found = false;
			while ((e = readdir(d))) {
				if (!strcasecmp(e->d_name, comp)) {
					cand = resolved + e->d_name;
					found = true;
					break;
				}
			}
			closedir(d);
			if (!found) return false;
		}
		resolved = cand;
		if (!sep) break;
		resolved += "/";
		pos += len + 1;
	}
	if (resolved.size() >= outsz) return false;
	std::memcpy(out, resolved.c_str(), resolved.size() + 1);
	return true;
}
//#include "memmgr.c"


bool isLittle;
bool jumpToBackGround;
//char *path;
bool executionFinished;
db exitCode;

FILE * logDebug=NULL;

struct HostMouse {
	bool installed = true;
	bool visible = false;
	int x = 160;
	int y = 100;
	int last_x = 160;
	int last_y = 100;
	int min_x = 0;
	int max_x = 319;
	int min_y = 0;
	int max_y = 199;
	int buttons = 0;
	int motion_x = 0;
	int motion_y = 0;
};

struct HostVga {
	static const int TEXT_PAGES = 8;
	static const int TEXT_ROWS = 25;
	static const int TEXT_COLS = 80;
	struct TextCell {
		db ch = ' ';
		db attr = 0x07;
	};
	db seq_index = 0;
	db gc_index = 0;
	db crtc_index = 0;
	db attr_index = 0;
	bool attr_waiting_for_index = true;
	db seq_regs[0x100] = {};
	db gc_regs[0x100] = {};
	db crtc_regs[0x100] = {};
	db attr_regs[0x100] = {};
	size_t dac_read_index = 0;
	size_t dac_write_index = 0;
	size_t dac_write_start = 0;
	size_t dac_write_count = 0;
	db cursor_start = 0;
	db cursor_end = 0;
	db current_mode = 3;
	db active_page = 0;
	db cursor_row[TEXT_PAGES] = {};
	db cursor_col[TEXT_PAGES] = {};
	TextCell text[TEXT_PAGES][TEXT_ROWS][TEXT_COLS] = {};
};

struct HostPit {
	db channel0_latch = 0;
	bool channel0_waiting_high = false;
	db channel0_low = 0;
	uint16_t channel0_divisor = 0;
};

struct HostTimer {
	bool enabled = false;
	bool in_callback = false;
	std::atomic<bool> background_running{false};
	std::atomic<bool> irq_running{false};
	uint64_t last_us = 0;
	uint64_t accum_us = 0;
	int divider_20hz = 0;
};

struct HostHardware {
	HostMouse mouse;
	HostVga vga;
	HostPit pit;
	HostTimer timer;
	dw current_psp = M2C_PSP_SEG;
	db ppi_port_b = 0;
	db keyboard_scan_code = 0;
	dw keyboard_buffer[16] = {};
	db keyboard_head = 0;
	db keyboard_tail = 0;
	// Segments populated by EXEC AL=03h overlay loads (e.g. MSC sound drivers).
	// Their x86 code is not translated; far calls into them are treated as
	// no-ops by dispatch_external_code, which emulates the driver's retf.
	std::vector<std::pair<dw, dw>> overlay_segs;
};

static HostHardware host;

// Accessor for NE-harness glue (zeek16.cpp) which installs a fake PSP after
// segment binding; HostHardware itself is file-local.
void m2c_set_current_psp(dw psp) { host.current_psp = psp; }
dw m2c_current_psp() { return host.current_psp; }

bool is_dos_terminate_vector(dw segment, dw offset) {
	// 0:0 is the sentinel pushed for synthesized interrupt frames (IVT IRQ
	// delivery); reaching it means unwind to C++, not program termination.
	if (segment == 0 && offset == 0) {
		return true;
	}
	if (segment != host.current_psp || offset != 0) {
		return false;
	}
	log_error("terminate vector hit at %x:%x\n", segment, offset);
	jumpToBackGround = true;
	executionFinished = true;
	exitCode = 0;
	return true;
}

static db* host_physical_address(dw segment, dw offset) {
	// The translated TANDYSND overlay image lives in a private buffer (see
	// asm.h): the EXEC load segment aliases the game's adapter-region buffer
	// writes, so the image must not sit inside struct Memory's heap.
	if (tnd_img_paras && segment >= tnd_seg && segment < tnd_seg + tnd_img_paras)
		return tnd_img + ((segment - tnd_seg) << 4) + offset;
	// PM selectors resolve through the emulated LDT (DOS services given a
	// selector must see the same memory the guest sees).
	if (db* sel_mem = m2c_alloc_segment_raddr(segment, offset))
		return sel_mem;
	return reinterpret_cast<db*>(&m2c::m) + (static_cast<size_t>(segment) << 4) + offset;
}

static db host_text_page(db page) {
	return page < HostVga::TEXT_PAGES ? page : 0;
}

static db host_text_row(db row) {
	return row < HostVga::TEXT_ROWS ? row : HostVga::TEXT_ROWS - 1;
}

static db host_text_col(db col) {
	return col < HostVga::TEXT_COLS ? col : HostVga::TEXT_COLS - 1;
}

static void host_text_clear_page(db page, db attr = 0x07) {
	page = host_text_page(page);
	for (int row = 0; row < HostVga::TEXT_ROWS; ++row) {
		for (int col = 0; col < HostVga::TEXT_COLS; ++col) {
			host.vga.text[page][row][col].ch = ' ';
			host.vga.text[page][row][col].attr = attr;
		}
	}
	host.vga.cursor_row[page] = 0;
	host.vga.cursor_col[page] = 0;
}

static void host_text_clear_all(db attr = 0x07) {
	for (int page = 0; page < HostVga::TEXT_PAGES; ++page) {
		host_text_clear_page(static_cast<db>(page), attr);
	}
}

static void host_text_scroll_up_window(db page, db attr, db top, db left, db bottom, db right, db lines) {
	page = host_text_page(page);
	top = host_text_row(top);
	bottom = host_text_row(bottom);
	left = host_text_col(left);
	right = host_text_col(right);
	if (top > bottom || left > right) {
		return;
	}
	if (lines == 0 || lines > bottom - top + 1) {
		lines = static_cast<db>(bottom - top + 1);
	}
	for (int row = top; row <= bottom; ++row) {
		const int src_row = row + lines;
		for (int col = left; col <= right; ++col) {
			if (src_row <= bottom) {
				host.vga.text[page][row][col] = host.vga.text[page][src_row][col];
			} else {
				host.vga.text[page][row][col].ch = ' ';
				host.vga.text[page][row][col].attr = attr;
			}
		}
	}
}

static void host_text_write(db page, db row, db col, db ch, db attr, dw count) {
	page = host_text_page(page);
	size_t pos = static_cast<size_t>(host_text_row(row)) * HostVga::TEXT_COLS + host_text_col(col);
	const size_t cells = HostVga::TEXT_ROWS * HostVga::TEXT_COLS;
	for (dw n = 0; n < count && pos < cells; ++n, ++pos) {
		host.vga.text[page][pos / HostVga::TEXT_COLS][pos % HostVga::TEXT_COLS].ch = ch;
		host.vga.text[page][pos / HostVga::TEXT_COLS][pos % HostVga::TEXT_COLS].attr = attr;
	}
}

static void vga_set_mode13_defaults() {
	host.vga.seq_regs[2] = 0x0f; // map mask: all planes writable
	host.vga.seq_regs[4] = 0x0e; // extended memory, odd/even disabled, chain-4 enabled
	host.vga.gc_regs[4] = 0x00;  // read map select
	host.vga.gc_regs[5] = 0x40;  // 256-color shift mode, write mode 0
	host.vga.crtc_regs[0x0c] = 0;
	host.vga.crtc_regs[0x0d] = 0;
}

static bool m2c_stats_enabled() {
	const char *enabled = std::getenv("M2C_VGA_STATS");
	return enabled && *enabled;
}

static bool bytes_have_nonzero(const db *data, size_t size) {
	for (size_t i = 0; i < size; ++i) {
		if (data[i] != 0) {
			return true;
		}
	}
	return false;
}

static db *translated_data_symbol_address(db *symbol_storage) {
	if (!symbol_storage) {
		return NULL;
	}
	db *target = NULL;
	std::copy(
		symbol_storage,
		symbol_storage + sizeof(target),
		reinterpret_cast<db *>(&target)
	);
	const uintptr_t target_addr = reinterpret_cast<uintptr_t>(target);
	const uintptr_t memory_addr = reinterpret_cast<uintptr_t>(&m);
	if (target_addr >= memory_addr && target_addr - memory_addr < 64u * 1024u * 1024u) {
		return target;
	}
	return symbol_storage;
}

static void maybe_apply_translated_vga_panel_palette() {
	const size_t panel_color_start = 176 * 3;
	const size_t panel_palette_size = 80 * 3;
	if (!&::vga_rgb_data || !&::vga_panel || !&::vga_panel1 || !&::setpaletteflag) {
		return;
	}

	db *rgb_data = translated_data_symbol_address(&::vga_rgb_data);
	db *panel = translated_data_symbol_address(&::vga_panel);
	db *panel1 = translated_data_symbol_address(&::vga_panel1);
	db *palette_flag = translated_data_symbol_address(&::setpaletteflag);
	if (!rgb_data || !panel || !panel1 || !palette_flag) {
		return;
	}
	if (!bytes_have_nonzero(panel1, panel_palette_size)) {
		return;
	}
	if (bytes_have_nonzero(rgb_data + panel_color_start, panel_palette_size)
		|| bytes_have_nonzero(panel, panel_palette_size)) {
		return;
	}

	std::copy(panel1, panel1 + panel_palette_size, panel);
	std::copy(panel1, panel1 + panel_palette_size, rgb_data + panel_color_start);
	std::copy(panel1, panel1 + panel_palette_size, vgaPalette + panel_color_start);
	*palette_flag = 1;
	if (m2c_stats_enabled()) {
		std::fprintf(stderr, "vga panel palette initialized from translated VGA_Panel1 symbols\n");
	}
}

static void vga_maybe_dump_dac_upload() {
	if (!m2c_stats_enabled() || host.vga.dac_write_start != 0 || host.vga.dac_write_count != 256 * 3) {
		return;
	}
	static unsigned upload_count = 0;
	++upload_count;
	std::fprintf(stderr, "vga dac upload #%u:", upload_count);
	const db colors[] = {0x00, 0x85, 0x96, 0xa0, 0xc0, 0xc1, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xcf};
	for (size_t i = 0; i < sizeof(colors) / sizeof(colors[0]); ++i) {
		const size_t index = static_cast<size_t>(colors[i]) * 3;
		std::fprintf(
			stderr,
			" #%02x(%u,%u,%u)",
			colors[i],
			static_cast<unsigned>(vgaPalette[index]),
			static_cast<unsigned>(vgaPalette[index + 1]),
			static_cast<unsigned>(vgaPalette[index + 2])
		);
	}
	std::fprintf(stderr, "\n");
}

#ifndef NOSDL
 #if SDL_MAJOR_VERSION == 2
static int sdl_vga_scale(int width, int height) {
	const char *forced_scale = getenv("M2C_SDL_SCALE");
	if (forced_scale && *forced_scale) {
		int scale = atoi(forced_scale);
		return scale > 0 ? scale : 1;
	}

	SDL_DisplayMode mode;
	if (SDL_GetCurrentDisplayMode(0, &mode) == 0 && mode.w > 0 && mode.h > 0) {
		int scale_x = mode.w / width;
		int scale_y = mode.h / height;
		int scale = scale_x < scale_y ? scale_x : scale_y;
		return scale > 0 ? scale : 1;
	}

	return 4;
}

static void configure_sdl_vga_window(int width, int height) {
	if ((SDL_WasInit(SDL_INIT_VIDEO) & SDL_INIT_VIDEO) == 0) {
		SDL_Init(SDL_INIT_VIDEO);
	}

	SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "0");
	const int scale = sdl_vga_scale(width, height);
	if (!window) {
		window = SDL_CreateWindow(
			"masm2c VGA",
			SDL_WINDOWPOS_CENTERED,
			SDL_WINDOWPOS_CENTERED,
			width * scale,
			height * scale,
			SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE
		);
	}
	if (!renderer && window) {
		renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
		if (!renderer) {
			renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_SOFTWARE);
		}
		if (!renderer) {
			log_error("SDL_CreateRenderer failed: %s\n", SDL_GetError());
			return;
		}
	}
	const bool logical_size_changed = vga_logical_width != width || vga_logical_height != height;
	if (window && logical_size_changed) {
		SDL_SetWindowSize(window, width * scale, height * scale);
	}
	if (renderer) {
		if (logical_size_changed && vgaTexture) {
			SDL_DestroyTexture(vgaTexture);
			vgaTexture = NULL;
		}
		SDL_RenderSetLogicalSize(renderer, width, height);
	}
	vga_logical_width = width;
	vga_logical_height = height;
}

static bool ensure_sdl_vga_window(int width, int height) {
	if (renderer && vga_logical_width == width && vga_logical_height == height) {
		return true;
	}
	configure_sdl_vga_window(width, height);
	return renderer != NULL;
}

void init_sdl_vga_window() {
	configure_sdl_vga_window(320, 200);
	std::fill(vgaPlanarPixels, vgaPlanarPixels + 640 * 200, 0);
	std::fill(vgaMode13Pixels, vgaMode13Pixels + VGA_WINDOW_SIZE * 4, 0);
	std::fill(vgaReadLatch, vgaReadLatch + 4, 0);
	std::fill(&vgaPendingReadLatch[0][0], &vgaPendingReadLatch[0][0] + 16, 0);
	std::fill(vgaSdlFrame, vgaSdlFrame + 640 * 200, 0xff000000u);
	vgaPendingReadLatchCount = 0;
	vgaPendingReadLatchNext = 0;
	if (!renderer) {
		return;
	}
	SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
	SDL_RenderClear(renderer);
	SDL_RenderPresent(renderer);
	vga_render_dirty = false;
	vga_render_writes = 0;
}

// ---------------------------------------------------------------------------
// Tandy 3-voice sound (SN76496 / NCR8496 compatible) on I/O port 0xC0.
// Chip model borrowed from MAME's sn76496 (via dosbox-staging), rendered
// through an SDL2 audio stream. Tandy PSG clock = 14318180/4 = 3579545 Hz.
namespace m2c_snd {

constexpr int SND_CLOCK = 3579545;
constexpr int SND_MAX_OUTPUT = 0x7fff;
// Counter decrement ("tick") rate: MAME runs the stream at clock/2 and
// subdivides by m_clock_divider (8), so tone/noise counters tick at clock/16.
constexpr double SND_TICK_HZ = SND_CLOCK / 16.0;

// NCR8496 (Tandy) parameters: feedback 0x8000, taps D/E via 0x02/0x20,
// XNOR noise feedback, data-writes to odd/noise regs ignored.
constexpr int SND_FEEDBACK_MASK = 0x8000;
constexpr int SND_TAP1 = 0x02;
constexpr int SND_TAP2 = 0x20;
constexpr bool SND_NEGATE = true;

struct Sn76496 {
	int32_t reg[8] = {};
	int last_reg = 0;
	int32_t period[4] = {};
	int32_t count[4] = {};
	int output[4] = {};
	int32_t volume[4] = {};
	int32_t vol_table[16] = {};
	uint32_t rng = 0;
	double tick_accum = 0.0;
	bool started = false;
};

static Sn76496 snd;
static SDL_AudioDeviceID snd_dev = 0;
static double snd_ticks_per_sample = 0.0;

// --- MIDI capture ---------------------------------------------------------
// The game streams raw SN76496 register words, so each tone write is a real
// note frequency (f = SND_CLOCK/(32*period)). We mirror that into a Standard
// MIDI File: tone channels 0..2 -> MIDI channels 0..2, noise channel 3 ->
// percussion on channel 9. Events are timestamped in microseconds and flushed
// at exit. Capture is opt-in: set M2C_MIDI_OUT to the .mid path to enable it.
struct MidiEvt { uint64_t us; uint8_t status, a, b; };
static std::vector<MidiEvt> midi_evts;
static int midi_note_state[4] = {-1, -1, -1, -1};   // sounding note or -1
static bool midi_started = false;

static uint64_t midi_now_us() {
	using namespace std::chrono;
	return (uint64_t)duration_cast<microseconds>(
		steady_clock::now().time_since_epoch()).count();
}

static int snd_freq_to_midi(int period) {
	if (period <= 0) return -1;
	const double f = SND_CLOCK / (32.0 * (double)period);
	if (f < 8.0) return -1;
	int n = (int)lround(69.0 + 12.0 * log2(f / 440.0));
	return n < 0 ? 0 : (n > 127 ? 127 : n);
}

static void midi_push(uint8_t status, uint8_t a, uint8_t b, uint64_t us) {
	midi_evts.push_back({us, status, a, b});
}

// Re-evaluate channel c's sounding note and emit note-on/off on change.
static void midi_commit(int c) {
	if (!midi_started) return; // capture is opt-in via M2C_MIDI_OUT
	int note = -1;
	if (snd.volume[c] > 0) {
		note = (c < 3) ? snd_freq_to_midi(snd.period[c]) : 38; // noise -> snare
	}
	if (note == midi_note_state[c]) return;
	const uint64_t now = midi_now_us();
	const int mch = (c < 3) ? c : 9;
	if (midi_note_state[c] >= 0) midi_push(0x80 | mch, midi_note_state[c], 0, now);
	if (note >= 0)               midi_push(0x90 | mch, note, 100, now);
	midi_note_state[c] = note;
}

static void midi_flush() {
	if (midi_evts.empty()) return;
	const char* path = getenv("M2C_MIDI_OUT");
	if (!path || !*path) return;
	FILE* f = fopen(path, "wb");
	if (!f) return;
	// Sort by timestamp, then write a single-track type-0 file at 96 PPQ,
	// 120 BPM (500000us/qn => 1 MIDI tick = 5208.33us of wall time).
	std::stable_sort(midi_evts.begin(), midi_evts.end(),
		[](const MidiEvt& x, const MidiEvt& y){ return x.us < y.us; });
	const double us_per_tick = 500000.0 / 96.0;
	fwrite("MThd", 1, 4, f);
	uint32_t hdrlen = 6; fwrite(&hdrlen, 4, 1, f); // big-endian below
	fseek(f, -4, SEEK_CUR);
	fputc(0, f); fputc(0, f); fputc(0, f); fputc(6, f);          // hdr len
	fputc(0, f); fputc(0, f); fputc(0, f); fputc(1, f);          // fmt 0, 1 track
	fputc(0, f); fputc(96, f);                                    // division=96 PPQ
	// body into memory to learn its length
	std::vector<uint8_t> trk;
	auto put=[&](uint8_t b){ trk.push_back(b); };
	auto putvlq=[&](uint32_t v){ uint8_t b[5];int n=0;b[n++]=v&0x7f;
		while(v>>=7)b[n++]=0x80|(v&0x7f); while(n--)trk.push_back(b[n]); };
	uint64_t prev = midi_evts.front().us; // first event anchors t=0
	for (auto& e : midi_evts) {
		uint64_t dt = (uint64_t)((e.us - prev) / us_per_tick + 0.5);
		prev = e.us;
		putvlq((uint32_t)dt);
		put(e.status); put(e.a); put(e.b);
	}
	putvlq(0); put(0xff); put(0x2f); put(0x00);                  // end of track
	fwrite("MTrk", 1, 4, f);
	uint32_t len = (uint32_t)trk.size();
	fputc((len>>24)&255, f); fputc((len>>16)&255, f);
	fputc((len>>8)&255, f); fputc(len&255, f);
	fwrite(trk.data(), 1, trk.size(), f);
	fclose(f);
	m2c::log_error("MIDI: wrote %zu note events to %s\n", midi_evts.size(), path);
}

static void midi_init() {
	if (midi_started) return;
	const char* path = getenv("M2C_MIDI_OUT");
	if (!path || !*path) return; // opt-in: no output file configured
	midi_started = true;
	atexit(midi_flush);
	// Route SIGTERM/SIGINT through exit() so atexit dumps the capture even when
	// the game is killed rather than quitting via its own exit path.
	auto die = [](int){ exit(0); };
	signal(SIGTERM, die);
	signal(SIGINT, die);
}
// --- end MIDI capture -----------------------------------------------------

static void snd_reset() {
	double out = SND_MAX_OUTPUT / 4; // per-channel headroom
	int gain = 16;
	while (gain-- > 0) {
		out *= 1.023292992; // +0.2 dB per step
	}
	for (int i = 0; i < 15; ++i) {
		snd.vol_table[i] = static_cast<int32_t>(out) < SND_MAX_OUTPUT / 4
			? static_cast<int32_t>(out)
			: SND_MAX_OUTPUT / 4;
		out /= 1.258925412; // -2 dB per step
	}
	snd.vol_table[15] = 0;
	for (int i = 0; i < 8; ++i) snd.reg[i] = 0;
	for (int i = 0; i < 4; ++i) {
		snd.volume[i] = 0;
		snd.period[i] = 0;
		snd.count[i] = 0;
		snd.output[i] = 0;
	}
	snd.last_reg = 3; // sega_style_psg default
	snd.rng = SND_FEEDBACK_MASK;
	snd.output[3] = snd.rng & 1;
	snd.tick_accum = 0.0;
}

static bool snd_in_noise_mode() { return (snd.reg[6] & 4) != 0; }

static void snd_write(uint8_t data) {
	int r;
	if (data & 0x80) {
		r = (data & 0x70) >> 4;
		snd.last_reg = r;
		if (r == 6 && ((data & 0x04) != (snd.reg[6] & 0x04))) snd.rng = SND_FEEDBACK_MASK;
		snd.reg[r] = (snd.reg[r] & 0x3f0) | (data & 0x0f);
	} else {
		r = snd.last_reg;
		if ((r & 1) || (r == 6)) return; // NCR8496 ignores data writes to vol/noise regs
	}
	const int c = r >> 1;
	switch (r) {
	case 0: case 2: case 4: // tone frequency
		if (!(data & 0x80)) snd.reg[r] = (snd.reg[r] & 0x0f) | ((data & 0x3f) << 4);
		snd.period[c] = snd.reg[r] != 0 ? snd.reg[r] : 0x400;
		if (r == 4 && (snd.reg[6] & 0x03) == 0x03) snd.period[3] = snd.period[2] << 1;
		// Frequency divider is complete only after the data byte; commit then.
		if (!(data & 0x80)) midi_commit(c);
		break;
	case 1: case 3: case 5: case 7: // volume
		snd.volume[c] = snd.vol_table[data & 0x0f];
		if (!(data & 0x80)) snd.reg[r] = (snd.reg[r] & 0x3f0) | (data & 0x0f);
		midi_commit(c);
		break;
	case 6: // noise frequency/mode
		if (!(data & 0x80)) snd.reg[r] = (snd.reg[r] & 0x3f0) | (data & 0x0f);
		{
			const int n = snd.reg[6];
			snd.period[3] = ((n & 3) == 3) ? (snd.period[2] << 1) : (1 << (5 + (n & 3)));
		}
		midi_commit(3);
		break;
	}
}

// One counter-decrement step (the MAME "new divided clock" block).
static void snd_tick() {
	for (int i = 0; i < 3; ++i) {
		if (--snd.count[i] <= 0) {
			snd.output[i] ^= 1;
			snd.count[i] = snd.period[i];
		}
	}
	if (--snd.count[3] <= 0) {
		if (((snd.rng & SND_TAP1) != 0) !=
		    ((static_cast<int32_t>(snd.rng & SND_TAP2) != SND_TAP2) && snd_in_noise_mode())) {
			snd.rng >>= 1;
			snd.rng |= SND_FEEDBACK_MASK;
		} else {
			snd.rng >>= 1;
		}
		snd.output[3] = snd.rng & 1;
		snd.count[3] = snd.period[3];
	}
}

static int snd_sample() {
	int out = (snd.output[0] ? snd.volume[0] : 0)
	        + (snd.output[1] ? snd.volume[1] : 0)
	        + (snd.output[2] ? snd.volume[2] : 0)
	        + (snd.output[3] ? snd.volume[3] : 0);
	return SND_NEGATE ? -out : out;
}

// --- live note-based soft-synth ("MIDI" engine) ------------------------------
// Two audio engines share the same SN76496 register state (period[c] -> note
// frequency, volume[c] -> amplitude):
//   midi (default): each tone channel is rendered as a triangle-wave voice with
//                   a short attack and a gentle release, so the score reads as
//                   soft instruments instead of raw square beeps. The noise
//                   channel keeps the chip's own percussion output.
//   psg           : the original cycle-level square-wave emulation.
// Select with M2C_SND_ENGINE=midi|psg (default: midi). The .mid file recorder
// (M2C_MIDI_OUT) is independent and works with either engine.
static int    snd_engine_sel = -1;  // -1 unresolved; 0 = midi, 1 = psg
static double snd_sample_rate = 0.0;
static double midi_phase[4] = {0.0, 0.0, 0.0, 0.0};
static double midi_amp[4]   = {0.0, 0.0, 0.0, 0.0};

static int snd_engine() {
	if (snd_engine_sel >= 0) return snd_engine_sel;
	const char* e = getenv("M2C_SND_ENGINE");
	snd_engine_sel = (e && (!strcmp(e, "psg") || !strcmp(e, "square") ||
	                        !strcmp(e, "tandy") || !strcmp(e, "chip")))
	                 ? 1 : 0;
	return snd_engine_sel;
}

// One audio sample from the note-based (MIDI) engine. Only called on the audio
// thread, so the per-voice phase/amplitude accumulators need no locking.
static int midi_synth_sample(double dt) {
	int acc = 0;
	for (int c = 0; c < 3; ++c) {
		const double f = snd.period[c] > 0 ? SND_CLOCK / (32.0 * snd.period[c]) : 0.0;
		const double tgt = static_cast<double>(snd.volume[c]) / SND_MAX_OUTPUT;
		const double rate = tgt > midi_amp[c] ? 400.0 : 50.0; // fast attack, slow release
		const double k = rate * dt > 1.0 ? 1.0 : rate * dt;
		midi_amp[c] += (tgt - midi_amp[c]) * k;
		midi_phase[c] += f * dt;
		midi_phase[c] -= floor(midi_phase[c]);
		const double t = midi_phase[c];
		const double tri = t < 0.5 ? 4.0 * t - 1.0 : 3.0 - 4.0 * t; // -1..1
		acc += static_cast<int>(tri * midi_amp[c] * SND_MAX_OUTPUT);
	}
	acc += snd.output[3] ? snd.volume[3] : 0; // noise channel stays percussion
	return SND_NEGATE ? -acc : acc;
}

static void snd_sdl_callback(void*, Uint8* stream, int len) {
	int16_t* out = reinterpret_cast<int16_t*>(stream);
	const int samples = len / static_cast<int>(sizeof(int16_t));
	const bool midi = (snd_engine() == 0);
	const double dt = snd_sample_rate > 0.0 ? 1.0 / snd_sample_rate : 0.0;
	for (int i = 0; i < samples; ++i) {
		snd.tick_accum += snd_ticks_per_sample;
		while (snd.tick_accum >= 1.0) {
			snd.tick_accum -= 1.0;
			snd_tick();
		}
		out[i] = static_cast<int16_t>(midi ? midi_synth_sample(dt) : snd_sample());
	}
}

static void snd_init() {
	if (snd.started) {
		return;
	}
	snd.started = true;
	snd_reset();
	midi_init();
	if ((SDL_WasInit(SDL_INIT_AUDIO) & SDL_INIT_AUDIO) == 0) {
		SDL_InitSubSystem(SDL_INIT_AUDIO);
	}
	SDL_AudioSpec want = {};
	want.freq = 22050;
	want.format = AUDIO_S16SYS;
	want.channels = 1;
	want.samples = 512;
	want.callback = snd_sdl_callback;
	SDL_AudioSpec got = {};
	snd_dev = SDL_OpenAudioDevice(nullptr, 0, &want, &got, 0);
	if (snd_dev == 0) {
		log_error("Tandy SDL_OpenAudioDevice failed: %s\n", SDL_GetError());
		return;
	}
	snd_ticks_per_sample = SND_TICK_HZ / got.freq;
	snd_sample_rate = got.freq;
	SDL_PauseAudioDevice(snd_dev, 0);
	log_debug("Tandy sound: SDL audio %d Hz, engine=%s\n", got.freq,
	          snd_engine() == 0 ? "midi" : "psg");
}

} // namespace m2c_snd

void tandy_snd_write(db data) {
	m2c_snd::snd_init();
	if (m2c_snd::snd_dev) {
		SDL_LockAudioDevice(m2c_snd::snd_dev);
	}
	m2c_snd::snd_write(data);
	if (m2c_snd::snd_dev) {
		SDL_UnlockAudioDevice(m2c_snd::snd_dev);
	}
	static unsigned long snd_writes = 0;
	++snd_writes;
	if (snd_writes <= 32 || (snd_writes % 512) == 0) {
		m2c::log_error("snd c0 wr #%lu data=%02x\n", snd_writes, data);
	}
}

static uint8_t vga_dac_to_sdl(db value) {
	if (value > 63) {
		return value;
	}
	return static_cast<uint8_t>((value << 2) | (value >> 4));
}

static uint32_t vga_color_to_argb(db color) {
	const size_t index = 3 * color;
	const uint8_t r = vga_dac_to_sdl(vgaPalette[index]);
	const uint8_t g = vga_dac_to_sdl(vgaPalette[index + 1]);
	const uint8_t b = vga_dac_to_sdl(vgaPalette[index + 2]);
	return 0xff000000u | (static_cast<uint32_t>(r) << 16) | (static_cast<uint32_t>(g) << 8) | b;
}

static bool vga_mode13_chain4_enabled() {
	return host.vga.current_mode == 0x13 && (host.vga.seq_regs[4] & 0x08) != 0;
}

static db vga_mode13_visible_color(size_t start, int x, int y) {
	if (vga_mode13_chain4_enabled()) {
		const size_t byte_offset = (start + y * 320 + x) % VGA_WINDOW_SIZE;
		return vgaMode13Pixels[byte_offset];
	}
	const size_t byte_offset = (start + y * 80 + x / 4) % VGA_WINDOW_SIZE;
	return vgaMode13Pixels[byte_offset * 4 + (x & 3)];
}

static size_t vga_count_nonzero_at_start(size_t start, bool require_visible_palette) {
	size_t count = 0;
	for (int y = 0; y < 200; ++y) {
		for (int x = 0; x < 320; ++x) {
			const db color = vga_mode13_visible_color(start, x, y);
			if (color == 0) {
				continue;
			}
			if (require_visible_palette && (vga_color_to_argb(color) & 0x00ffffffu) == 0) {
				continue;
			}
			++count;
		}
	}
	return count;
}

static void vga_dump_top_visible_colors(size_t start) {
	size_t counts[256];
	std::fill(counts, counts + 256, 0);
	for (int y = 0; y < 200; ++y) {
		for (int x = 0; x < 320; ++x) {
			const db color = vga_mode13_visible_color(start, x, y);
			++counts[color];
		}
	}
	std::fprintf(stderr, "vga colors:");
	for (int rank = 0; rank < 8; ++rank) {
		size_t best_count = 0;
		int best_color = -1;
		for (int color = 0; color < 256; ++color) {
			if (counts[color] > best_count) {
				best_count = counts[color];
				best_color = color;
			}
		}
		if (best_color < 0 || best_count == 0) {
			break;
		}
		const size_t index = static_cast<size_t>(best_color) * 3;
		std::fprintf(
			stderr,
			" #%02x=%zu(rgb=%u,%u,%u)",
			best_color,
			best_count,
			static_cast<unsigned>(vgaPalette[index]),
			static_cast<unsigned>(vgaPalette[index + 1]),
			static_cast<unsigned>(vgaPalette[index + 2])
		);
		counts[best_color] = 0;
	}
	std::fprintf(stderr, "\n");
}

static size_t vga_crtc_start_byte_offset();

static void vga_maybe_dump_frame() {
	static bool dumped = false;
	static unsigned frame_count = 0;
	static unsigned since_last = 0;
	++frame_count;
	if (dumped) {
		return;
	}
	const char *path = std::getenv("M2C_VGA_DUMP_FRAME");
	if (!path || !*path) {
		return;
	}
	const char *frame_at_value = std::getenv("M2C_VGA_DUMP_FRAME_AT");
	const unsigned frame_at = frame_at_value && *frame_at_value
		? static_cast<unsigned>(std::strtoul(frame_at_value, NULL, 10))
		: 0;
	if (frame_at != 0 && frame_count < frame_at) {
		return;
	}
	// Continuous mode: when no specific frame was requested, refresh the dump
	// file periodically so the live screen can be inspected without gdb.
	if (frame_at == 0 && ++since_last < 15) {
		return;
	}
	since_last = 0;

	size_t lit_pixels = 0;
	for (int i = 0; i < vga_logical_width * vga_logical_height; ++i) {
		if ((vgaSdlFrame[i] & 0x00ffffffu) != 0) {
			++lit_pixels;
		}
	}
	if (lit_pixels == 0) {
		return;
	}

	FILE *f = std::fopen(path, "wb");
	if (!f) {
		log_error("could not write M2C_VGA_DUMP_FRAME=%s\n", path);
		dumped = true;
		return;
	}
	std::fprintf(f, "P6\n%d %d\n255\n", vga_logical_width, vga_logical_height);
	for (int i = 0; i < vga_logical_width * vga_logical_height; ++i) {
		const uint32_t pixel = vgaSdlFrame[i];
		const unsigned char rgb[3] = {
			static_cast<unsigned char>((pixel >> 16) & 0xff),
			static_cast<unsigned char>((pixel >> 8) & 0xff),
			static_cast<unsigned char>(pixel & 0xff),
		};
		std::fwrite(rgb, 1, sizeof(rgb), f);
	}
	std::fclose(f);
	// Companion diagnostics: dump the raw per-pixel palette indices and the DAC
	// palette alongside the rendered frame so corruption can be attributed to
	// bad pixel data vs a bad palette entry.
	{
		std::string pal_path = std::string(path) + ".pal";
		FILE *pf = std::fopen(pal_path.c_str(), "wb");
		if (pf) {
			std::fwrite(vgaPalette, 1, 256 * 3, pf);
			std::fclose(pf);
		}
	}
	{
		std::string idx_path = std::string(path) + ".idx";
		FILE *ix = std::fopen(idx_path.c_str(), "wb");
		if (ix) {
			const size_t start = vga_crtc_start_byte_offset();
			for (int y = 0; y < vga_logical_height; ++y) {
				for (int x = 0; x < vga_logical_width; ++x) {
					const db color = (host.vga.current_mode == 0x13 && vga_logical_width == 320)
						? vga_mode13_visible_color(start, x, y)
						: vgaPlanarPixels[y * 640 + x];
					std::fwrite(&color, 1, 1, ix);
				}
			}
			std::fclose(ix);
		}
	}
	if (frame_at != 0) {
		std::fprintf(stderr, "vga dumped frame #%u to %s lit=%zu\n", frame_count, path, lit_pixels);
		dumped = true;
	}
}

static size_t vga_crtc_start_byte_offset() {
	const size_t crtc_start = (static_cast<size_t>(host.vga.crtc_regs[0x0c]) << 8) | host.vga.crtc_regs[0x0d];
	if (host.vga.current_mode == 0x13 && (host.vga.seq_regs[4] & 0x08) == 0) {
		/* Unchained (mode-X style) plane addressing: the start-address units
		 * follow the CRTC addressing mode -- dword mode (CRTC 0x14 bit6)
		 * scales x4, word mode (CRTC 0x17 bit6=0) x2, byte mode (bit6=1) x1.
		 * Tornado programs the start directly in plane bytes ({0, 0x4000}),
		 * so byte mode must not scale or the display reads the wrong page. */
		if (host.vga.crtc_regs[0x14] & 0x40) {
			return (crtc_start * 4) % VGA_WINDOW_SIZE;
		}
		if ((host.vga.crtc_regs[0x17] & 0x40) == 0) {
			return (crtc_start * 2) % VGA_WINDOW_SIZE;
		}
	}
	return crtc_start % VGA_WINDOW_SIZE;
}

static void vga_maybe_dump_stats(size_t crtc_start) {
	static unsigned dump_count = 0;
	const char *enabled = std::getenv("M2C_VGA_STATS");
	if (!enabled || !*enabled) {
		return;
	}
	++dump_count;
	if (dump_count != 1 && dump_count % 30 != 0) {
		return;
	}
	std::fprintf(
		stderr,
		"vga stats #%u mode=%02x crtc=%04zx r0c=%02x r0d=%02x r11=%02x seq2=%02x seq4=%02x gc5=%02x visible=%zu visible-lit=%zu p0=%zu p4000=%zu p8000=%zu pc000=%zu\n",
		dump_count,
		host.vga.current_mode,
		crtc_start,
		host.vga.crtc_regs[0x0c],
		host.vga.crtc_regs[0x0d],
		host.vga.crtc_regs[0x11],
		host.vga.seq_regs[2],
		host.vga.seq_regs[4],
		host.vga.gc_regs[5],
		vga_count_nonzero_at_start(crtc_start, false),
		vga_count_nonzero_at_start(crtc_start, true),
		vga_count_nonzero_at_start(0x0000, false),
		vga_count_nonzero_at_start(0x4000, false),
			vga_count_nonzero_at_start(0x8000, false),
			vga_count_nonzero_at_start(0xc000, false)
		);
		vga_dump_top_visible_colors(crtc_start);
	}

static void vga_render_indexed_frame() {
	if (!renderer) {
		return;
	}
	if (!vgaTexture) {
		vgaTexture = SDL_CreateTexture(
			renderer,
			SDL_PIXELFORMAT_ARGB8888,
			SDL_TEXTUREACCESS_STREAMING,
			vga_logical_width,
			vga_logical_height
		);
		if (!vgaTexture) {
			log_error("SDL_CreateTexture failed: %s\n", SDL_GetError());
			return;
		}
	}

	maybe_apply_translated_vga_panel_palette();
	const size_t crtc_start = vga_crtc_start_byte_offset();
	vga_maybe_dump_stats(crtc_start);
	for (int y = 0; y < vga_logical_height; ++y) {
		for (int x = 0; x < vga_logical_width; ++x) {
			db color = 0;
			if (host.vga.current_mode == 0x13 && vga_logical_width == 320) {
				color = vga_mode13_visible_color(crtc_start, x, y);
			} else {
				color = vgaPlanarPixels[y * 640 + x];
			}
			vgaSdlFrame[y * vga_logical_width + x] = vga_color_to_argb(color);
		}
	}

	SDL_UpdateTexture(vgaTexture, NULL, vgaSdlFrame, vga_logical_width * static_cast<int>(sizeof(uint32_t)));
	vga_maybe_dump_frame();
	SDL_RenderClear(renderer);
	SDL_RenderCopy(renderer, vgaTexture, NULL, NULL);
}

static uint64_t vga_last_present_ms = 0;

static void vga_present_now() {
	vga_render_indexed_frame();
	SDL_RenderPresent(renderer);
	vga_last_present_ms = SDL_GetTicks64();
	vga_render_dirty = false;
	vga_render_writes = 0;
}

/* Rate-limited mid-frame present. The write-flush threshold fires several times
   inside one ~64 KB frame and each call used to re-render + present the whole
   framebuffer, which is heavy CPU work and can queue up vsync on a real display.
   Cap those mid-frame flushes to ~30 Hz; the completed frame is still shown once
   per frame by the retrace boundary (vga_present_forced) and by the periodic
   event pump. vga_render_writes/dirty stay set on a skip so the next check still
   sees pending work. */
void vga_present_pending() {
	if (renderer && vga_render_dirty &&
	    SDL_GetTicks64() - vga_last_present_ms >= 33) {
		vga_present_now();
	}
}

/* Frame-boundary present: always shows the accumulated frame. Called from the
   VGA vertical-retrace poll (IN 0x3DA), i.e. once per logical game frame. */
void vga_present_forced() {
	if (renderer && vga_render_dirty) {
		vga_present_now();
	}
}

static bool vga_is_planar_mode() {
	if (host.vga.current_mode == 0x13) {
		return !vga_mode13_chain4_enabled();
	}
	return true;
}

static bool vga_mode13_address(size_t offset, size_t *page_offset) {
	if (offset >= VGA_WINDOW_SIZE) {
		return false;
	}
	*page_offset = offset;
	return true;
}

static void vga_latch_mode13_byte(size_t page_offset, db *latch) {
	for (int plane = 0; plane < 4; ++plane) {
		latch[plane] = vgaMode13Pixels[page_offset * 4 + plane];
	}
}

db vga_read_byte_value_from_memory(const db *d) {
	if (host.vga.current_mode != 0x13) {
		return *d;
	}
	const size_t offset = d - ((const db*)&m) - 0xa0000;
	size_t page_offset = 0;
	if (!vga_mode13_address(offset, &page_offset)) {
		return *d;
	}
	if (vga_mode13_chain4_enabled()) {
		return vgaMode13Pixels[page_offset];
	}
	vga_latch_mode13_byte(page_offset, vgaReadLatch);
	const db read_plane = host.vga.gc_regs[4] & 0x03;
	return vgaReadLatch[read_plane];
}

void vga_read_bytes_from_memory(const db *d, size_t size) {
	if (host.vga.current_mode != 0x13) {
		return;
	}
	vgaPendingReadLatchCount = 0;
	vgaPendingReadLatchNext = 0;
	for (size_t i = 0; i < size && i < 4; ++i) {
		const size_t offset = (d + i) - ((const db*)&m) - 0xa0000;
		size_t page_offset = 0;
		if (!vga_mode13_address(offset, &page_offset)) {
			continue;
		}
		vga_latch_mode13_byte(page_offset, vgaReadLatch);
		vga_latch_mode13_byte(page_offset, vgaPendingReadLatch[vgaPendingReadLatchCount]);
		++vgaPendingReadLatchCount;
	}
}

void vga_read_byte_from_memory(const db *d) {
	vga_read_bytes_from_memory(d, 1);
}

static const db *vga_latch_for_mode13_write() {
	if (vgaPendingReadLatchNext < vgaPendingReadLatchCount) {
		const db *latch = vgaPendingReadLatch[vgaPendingReadLatchNext++];
		if (vgaPendingReadLatchNext >= vgaPendingReadLatchCount) {
			vgaPendingReadLatchCount = 0;
			vgaPendingReadLatchNext = 0;
		}
		return latch;
	}
	return vgaReadLatch;
}

static void vga_write_mode13_chain4_byte(size_t offset, db value) {
	if (!ensure_sdl_vga_window(320, 200)) {
		return;
	}

	size_t page_offset = 0;
	if (!vga_mode13_address(offset, &page_offset)) {
		return;
	}
	db map_mask = host.vga.seq_regs[2] & 0x0f;
	if (!map_mask) {
		map_mask = 0x0f;
	}
	const db plane = page_offset & 0x03;
	if ((map_mask & (1 << plane)) == 0) {
		return;
	}
	vgaMode13Pixels[page_offset] = value;
	vga_render_dirty = true;
	if (++vga_render_writes >= VGA_RENDER_WRITE_FLUSH_THRESHOLD) {
		vga_present_pending();
	}
}

static void vga_write_mode13_planar_byte(size_t offset, db value) {
	if (!ensure_sdl_vga_window(320, 200)) {
		return;
	}

	size_t page_offset = 0;
	if (!vga_mode13_address(offset, &page_offset)) {
		return;
	}
	db map_mask = host.vga.seq_regs[2] & 0x0f;
	if (!map_mask) {
		map_mask = 0x0f;
	}
	const bool write_mode_1 = (host.vga.gc_regs[5] & 0x03) == 1;
	const db *write_latch = write_mode_1 ? vga_latch_for_mode13_write() : vgaReadLatch;
	for (int plane = 0; plane < 4; ++plane) {
		if ((map_mask & (1 << plane)) == 0) {
			continue;
		}
		const db pixel = write_mode_1 ? write_latch[plane] : value;
		vgaMode13Pixels[page_offset * 4 + plane] = pixel;
	}
	vga_render_dirty = true;
	if (++vga_render_writes >= VGA_RENDER_WRITE_FLUSH_THRESHOLD) {
		vga_present_pending();
	}
}

static void vga_write_planar_byte(size_t offset, db value) {
	if (host.vga.current_mode == 0x13) {
		vga_write_mode13_planar_byte(offset, value);
		return;
	}

	if (!ensure_sdl_vga_window(640, 200)) {
		return;
	}

	const size_t page_offset = offset % 0x4000;
	const int y = page_offset / 80;
	const int x0 = (page_offset % 80) * 8;
	if (y < 0 || y >= 200) {
		return;
	}

	db map_mask = host.vga.seq_regs[2] & 0x0f;
	if (!map_mask) {
		map_mask = 0x0f;
	}
	for (int bit = 0; bit < 8; ++bit) {
		const int x = x0 + bit;
		if (x >= 640) {
			break;
		}
		const db source_bit = (value >> (7 - bit)) & 1;
		db &pixel = vgaPlanarPixels[y * 640 + x];
		for (int plane = 0; plane < 4; ++plane) {
			const db plane_mask = 1 << plane;
			if ((map_mask & plane_mask) == 0) {
				continue;
			}
			if (source_bit) {
				pixel |= plane_mask;
			} else {
				pixel &= ~plane_mask;
			}
		}
	}
	vga_render_dirty = true;
	if (++vga_render_writes >= VGA_RENDER_WRITE_FLUSH_THRESHOLD) {
		vga_present_pending();
	}
}

void vga_write_pixel_from_memory(db *d, db color) {
	if (!renderer) {
		init_sdl_vga_window();
	}
	if (!renderer) {
		return;
	}
	const size_t di = d - ((db*)&m) - 0xa0000;
	if (vga_is_planar_mode()) {
		vga_write_planar_byte(di, color);
		return;
	}
	vga_write_mode13_chain4_byte(di, color);
}
 #endif
#endif

#ifdef NOSDL
void tandy_snd_write(db) {}
#endif

static int host_clamp_int(int value, int min_value, int max_value) {
	if (value < min_value) {
		return min_value;
	}
	if (value > max_value) {
		return max_value;
	}
	return value;
}

static void clamp_host_mouse() {
	host.mouse.x = host_clamp_int(host.mouse.x, host.mouse.min_x, host.mouse.max_x);
	host.mouse.y = host_clamp_int(host.mouse.y, host.mouse.min_y, host.mouse.max_y);
}

static db* host_key_state() {
	return &::key ? ::key : nullptr;
}

static bool host_keyboard_buffer_empty() {
	return host.keyboard_head == host.keyboard_tail;
}

static bool host_keyboard_buffer_full() {
	return static_cast<db>((host.keyboard_tail + 1) % 16) == host.keyboard_head;
}

static bool host_keyboard_push(dw bios_key) {
	if (bios_key == 0 || host_keyboard_buffer_full()) {
		return false;
	}
	host.keyboard_buffer[host.keyboard_tail] = bios_key;
	host.keyboard_tail = static_cast<db>((host.keyboard_tail + 1) % 16);
	return true;
}

static bool host_keyboard_peek(dw* bios_key) {
	if (host_keyboard_buffer_empty()) {
		return false;
	}
	*bios_key = host.keyboard_buffer[host.keyboard_head];
	return true;
}

static bool host_keyboard_pop(dw* bios_key) {
	if (!host_keyboard_peek(bios_key)) {
		return false;
	}
	host.keyboard_head = static_cast<db>((host.keyboard_head + 1) % 16);
	return true;
}

static db host_ascii_to_pc_scan(db ch) {
	switch (ch) {
	case 0x1b: return 0x01;
	case '1': case '!': return 0x02;
	case '2': case '@': return 0x03;
	case '3': case '#': return 0x04;
	case '4': case '$': return 0x05;
	case '5': case '%': return 0x06;
	case '6': case '^': return 0x07;
	case '7': case '&': return 0x08;
	case '8': case '*': return 0x09;
	case '9': case '(': return 0x0a;
	case '0': case ')': return 0x0b;
	case '-': case '_': return 0x0c;
	case '=': case '+': return 0x0d;
	case '\b': return 0x0e;
	case '\t': return 0x0f;
	case 'q': case 'Q': return 0x10;
	case 'w': case 'W': return 0x11;
	case 'e': case 'E': return 0x12;
	case 'r': case 'R': return 0x13;
	case 't': case 'T': return 0x14;
	case 'y': case 'Y': return 0x15;
	case 'u': case 'U': return 0x16;
	case 'i': case 'I': return 0x17;
	case 'o': case 'O': return 0x18;
	case 'p': case 'P': return 0x19;
	case '[': case '{': return 0x1a;
	case ']': case '}': return 0x1b;
	case '\r': case '\n': return 0x1c;
	case 'a': case 'A': return 0x1e;
	case 's': case 'S': return 0x1f;
	case 'd': case 'D': return 0x20;
	case 'f': case 'F': return 0x21;
	case 'g': case 'G': return 0x22;
	case 'h': case 'H': return 0x23;
	case 'j': case 'J': return 0x24;
	case 'k': case 'K': return 0x25;
	case 'l': case 'L': return 0x26;
	case ';': case ':': return 0x27;
	case '\'': case '"': return 0x28;
	case '`': case '~': return 0x29;
	case '\\': case '|': return 0x2b;
	case 'z': case 'Z': return 0x2c;
	case 'x': case 'X': return 0x2d;
	case 'c': case 'C': return 0x2e;
	case 'v': case 'V': return 0x2f;
	case 'b': case 'B': return 0x30;
	case 'n': case 'N': return 0x31;
	case 'm': case 'M': return 0x32;
	case ',': case '<': return 0x33;
	case '.': case '>': return 0x34;
	case '/': case '?': return 0x35;
	case ' ': return 0x39;
	default: return 0;
	}
}

static dw host_stdin_char_to_bios_key(db ch) {
	const db ascii = ch == '\n' ? '\r' : ch;
	return static_cast<dw>((static_cast<dw>(host_ascii_to_pc_scan(ascii)) << 8) | ascii);
}

static db host_keyboard_shift_flags() {
	const db* keys = host_key_state();
	if (keys == nullptr) {
		return 0;
	}
	db flags = 0;
	if (keys[54]) {
		flags |= 0x01;
	}
	if (keys[42]) {
		flags |= 0x02;
	}
	if (keys[29]) {
		flags |= 0x04;
	}
	if (keys[56]) {
		flags |= 0x08;
	}
	return flags;
}

static dw* host_ticker_counter() {
	return &::ticker ? ::ticker : nullptr;
}

static dw* host_frames_counter() {
	return &::frames ? ::frames : nullptr;
}

static dw* host_countdown_counter() {
	return &::countdown ? ::countdown : nullptr;
}

static dd* host_elapsed_time() {
	return &::elapsedtime ? ::elapsedtime : nullptr;
}

static void host_advance_timer_counters() {
	if (dw* ticker_counter = host_ticker_counter()) {
		++*ticker_counter;
	}
	if (dw* frames_counter = host_frames_counter()) {
		++*frames_counter;
	}
	dw* countdown_counter = host_countdown_counter();
	if (countdown_counter && *countdown_counter > 0) {
		--*countdown_counter;
	}
	if (dd* elapsed_time = host_elapsed_time()) {
		++*elapsed_time;
	}
}

static void host_start_timer_thread() {
	bool expected = false;
	if (!host.timer.background_running.compare_exchange_strong(expected, true)) {
		return;
	}
	std::thread([] {
		while (host.timer.background_running.load()) {
			std::this_thread::sleep_for(std::chrono::milliseconds(10));
			if (host.timer.enabled) {
				host_advance_timer_counters();
			}
		}
	}).detach();
}

// The translated program's main state, captured in init(). The IRQ thread
// consults its IF flag so guest cli sections are honored while polling the
// IVT for handlers installed with direct vector writes (no int 21h AH=25h).
static _STATE* host_irq_main_state = nullptr;

/* Cooperative IRQ delivery. A real ISR shares the caller's machine state and
   runs on the interrupted thread between instructions; the generated code uses
   shared bookkeeping (native_return_*, data_offset stacks, etc.) that is NOT
   thread-safe. Running the IVT handler on a separate thread races the game on
   that shared state (observed as non-deterministic "Don't know how to call"
   faults). Instead the timer thread only bumps the BIOS tick and a pending
   counter; the game thread drains it here, on its own stack, exactly like
   host_run_timer_handler does for registered timer procs. */
static std::atomic<int> host_pending_irq8{0};
static std::atomic<int> host_pending_irq1c{0};

/* PIT channel-0 period in microseconds. The game/sound driver reprograms the
   8253 divisor via ports 0x43/0x40 (e.g. TANDYSND loads 0x4DAE => ~60 Hz for
   its sequencer); the IRQ thread paces int8/int1c at this rate so music tempo,
   animation and input polling run at the speed the game expects. Default is
   the BIOS rate (65536 divisor => 18.2 Hz). */
static std::atomic<int> host_irq_period_us{54945};

/* The ISR runs on a dedicated machine state whose stack lives in stack[]; the
   frame sentinel (0,0) makes IRET/RETF unwind back to C++. It is only ever run
   on the game thread (via host_drain_irq) so the shared generated-code
   bookkeeping is used serially, never concurrently. */
static _STATE host_irq_state;
static bool host_irq_state_init = false;

static void host_fire_ivt(int intno, _STATE* _state) {
	const dw off = *(dw*)host_physical_address(0, intno * 4);
	const dw seg = *(dw*)host_physical_address(0, intno * 4 + 2);
	// Skip unset/BIOS-adapter-region vectors, but let the translated TANDYSND
	// ISR (which lives at its own code segment, e.g. a239:0373) fire.
	if ((off | seg) == 0 || (seg >= 0xa000 && seg != tnd_code_seg)) {
		return;
	}
	if (host_irq_main_state && !host_irq_main_state->IF) {
		return;
	}
	if (!host_irq_state_init) {
		std::memset(&host_irq_state, 0, sizeof(host_irq_state));
		host_irq_state_init = true;
	}
	_STATE* irq = &host_irq_state;
	/* On real hardware the CPU pushes the interrupt frame onto the
	   interrupted task's own ss:sp. Placing it at the top of stack[] instead
	   breaks when the game itself runs on stack[]: the handler's pushes
	   descend into live frames and corrupt both the stack bytes and the
	   shared shadow-stack map (indexed by raw sp). Run the ISR on the game's
	   stack, just below its live sp; fall back to a dedicated arena at the
	   bottom of stack[] only when no game state exists yet. */
	dw irq_ss = seg_offset(stack);
	dw irq_sp = STACK_SIZE / 4;
	if (host_irq_main_state && host_irq_main_state->esp > 0x10) {
		irq_ss = host_irq_main_state->ss;
		irq_sp = (dw)(host_irq_main_state->esp - 8);
	}
	// IRET lowers to RETF(0) here, which pops ip then cs; ip==0 is the
	// sentinel that unwinds back to C++.
	irq->ss = irq_ss;
	irq->esp = irq_sp;
	*(dw*)m2c::stack_raddr_(irq->ss, (dw)irq->esp) = 0;
	*(dw*)m2c::stack_raddr_(irq->ss, (dw)(irq->esp + 2)) = 0;
	irq->cs = seg;
	irq->eip = off;
#ifdef SHADOW_STACK
	const ShadowStack::SavedState saved_shadow = m2c::shadow_stack.save_state();
#endif
	// Snapshot native-return bookkeeping; the handler may leave stale marks
	// behind (e.g. when a StackPop unwind bypasses the matching RET).
	const size_t saved_marks = m2c::native_return_marks.size();
	const size_t saved_values = m2c::native_return_values.size();
	const size_t saved_depth = m2c::native_return_call_depth;
	const bool saved_suppress = m2c::suppress_native_return_push_transfer;
	/* Dispatch through the aggregate global-offset table: IVT offsets were
	   stored by generated `OFFSET` writes (kglobal_* space), so `off` maps
	   directly (e.g. Tornado's 0x13a2 -> timerintr). _ENTRY_POINT_ is the
	   program's main proc and ignores its argument -- running it per IRQ
	   re-enters the whole game loop inside the ISR. Untranslated overlay ISRs
	   (TANDYSND) are still reached via host_try_overlay_retf: irq->cs holds the
	   vector's segment, so the tseg==0 internal-dispatch case applies. */
	bool handled = false;
	try {
		m2c::dispatch_external_code(static_cast<_offsets>(off), irq, &handled);
	} catch (const m2c::StackPop&) {
		// An IRET/RETF inside the handler unwound past the synthesized frame;
		// that is the normal way back to C++, not an error.
	}
	if (!handled) {
		log_debug2("irq vector %x:%x not handled by translated code\n", seg, off);
	}
	m2c::native_return_marks.resize(saved_marks);
	m2c::native_return_values.resize(saved_values);
	m2c::native_return_call_depth = saved_depth;
	m2c::suppress_native_return_push_transfer = saved_suppress;
#ifdef SHADOW_STACK
	m2c::shadow_stack.restore_state(saved_shadow);
	// The handler pushed frames below the live stack top; they are stale now
	// and would otherwise be miscounted as uncontrolled pops by later scans.
	m2c::shadow_stack.clear_frames_below(irq_sp);
#endif
}

// Run pending IVT interrupts on the caller's (game) thread. Called from
// poll_host_events and from a periodic hook inside the arithmetic helpers so
// that pure compute delay loops (e.g. waits on an int1c-decremented counter)
// still get their ticks. */
struct HostIrqCallbackGuard {
	HostIrqCallbackGuard() { host.timer.in_callback = true; }
	~HostIrqCallbackGuard() { host.timer.in_callback = false; }
};

static void host_drain_irq() {
	if (host.timer.in_callback) {
		return;
	}
	HostIrqCallbackGuard callback_guard;
	/* Real hardware latches at most one pending IRQ per source: ticks that
	   arrive while the game is busy are lost, never queued. Clamp the catch-up
	   batch so a stall (heavy frame, debugger pause) cannot queue thousands of
	   handler invocations and trap the game thread inside this loop. The BIOS
	   tick count at 0x40:0x6c still advances at wall-clock rate. */
	int n8 = host_pending_irq8.exchange(0);
	if (n8 > 4) n8 = 4;
	while (n8-- > 0) host_fire_ivt(0x08, nullptr);
	int n1c = host_pending_irq1c.exchange(0);
	if (n1c > 4) n1c = 4;
	while (n1c-- > 0) host_fire_ivt(0x1c, nullptr);
}

// Cheap periodic drain trigger injected into hot generated-code helpers. The
// counter bounds overhead; the atomic pending check makes the common case a
// single load. Runs on whichever thread executes generated code (the game's).
void host_irq_poll() {
	if (host_pending_irq8.load() <= 0 && host_pending_irq1c.load() <= 0) return;
	host_drain_irq();
}

// Far call/jump targets inside EXEC-loaded overlay regions (sound drivers)
// have no translated code. The drivers end with `retf`, which pops the
// caller's cs:ip frame. Emulate that by popping the frame and returning
// true: the C++ call chain then unwinds to the statement after the original
// far call, which is exactly where the driver's retf would resume.
bool host_try_overlay_retf(_offsets __disp, _STATE* _state, bool* out_result) {
	// A null far target means the jump/call chained to an empty vector --
	// e.g. Tornado's timerintr tails into the saved DOS IRQ0 handler, which
	// was 0:0 because no BIOS handler was ever installed. On real hardware
	// that slot ends in EOI+IRET, i.e. the whole activation simply ends:
	// returning false unwinds the dispatch exactly like a completed retf.
	if (__disp == 0) {
		*out_result = false;
		return true;
	}
	const dw tseg = static_cast<dw>(__disp >> 16);
	// Translated TANDYSND overlay: an external far call / ISR targets the
	// driver's code segment (tseg == tnd_code_seg), while an internal indirect
	// dispatch (e.g. `call off_10380[bx]`) arrives with tseg == 0 while cs is
	// still the driver's code segment. Route both into tnd_overlay_call.
	if (tnd_code_seg &&
	    (tseg == tnd_code_seg || (tseg == 0 && _state->cs == tnd_code_seg))) {
		log_debug2("tnd call disp=%x cs=%x\n", __disp, _state->cs);
		*out_result = tnd_overlay_call(__disp, _state);
		return true;
	}
	for (const auto& r : host.overlay_segs) {
		if (tseg < r.first || tseg >= r.second) {
			continue;
		}
		X86_REGREF
		dw ret_ip = 0, ret_cs = 0;
		POP(ret_ip);
		POP(ret_cs);
		/* The POPs moved the caller's return mark into the value list;
		 * claim it so CALL_'s strict verification sees a real consume. */
		size_t ov_mid = 0;
		if (take_native_return_value(_state, (MWORDSIZE)ret_ip, &ret_ip, &ov_mid)) {
			m2c::last_ret_mark_id = ov_mid;
			m2c::last_ret_mark_mode = 4;
		}
		m2c::last_ret_popped = 4;
		log_debug2("overlay entry %x:%x emulated as retf to %x:%x\n",
			tseg, (dw)(__disp & 0xffff), ret_cs, ret_ip);
		*out_result = true;
		return true;
	}
	/* Packed far target (seg:off from a dd pointer, e.g. Tornado's
	 * `call UserVctr100` = 0x4d1d:0x1659): SEG of a generated proc is an
	 * opaque value, not a real address, so the aggregate dispatch only ever
	 * matches the offset part. BIOS (f000) and overlay segments were already
	 * excluded above; retry the remaining packed pointers by global offset.
	 * Never retry off==0: the inner dispatch's null-target rule would claim
	 * it as an empty vector and "end the activation", silently swallowing a
	 * real far call whose target segment simply starts at offset 0 (e.g. an
	 * NE listing-mode key 0x15c5:0000 that the local switch owns).
	 * The retry is also skipped when `tseg` resolves to a real segment of
	 * this image: a packed value carrying a live code paragraph or LDT
	 * selector is a genuine seg:off key owned by the local switch (or the
	 * selector thunk), and stripping the segment aliases its offset word
	 * against unrelated aggregate-table entries -- e.g. Zeek's packed
	 * 0x11ed:0x1066 (kloc_11516) collapsed to global offset 0x1066 and ran
	 * loc_11918 instead.  Tornado's packed pointers survive the gate
	 * because their bank "seg" matches no resolver. */
	if (tseg != 0 && tseg != 0xf000 && (__disp & 0xffff) != 0) {
		const dw toff = static_cast<dw>(__disp & 0xffff);
		const bool real_seg =
			(tlink_code_segment_raddr != nullptr &&
			 tlink_code_segment_raddr(tseg, toff) != nullptr) ||
			(m2c_code_segment_raddr != nullptr &&
			 m2c_code_segment_raddr(tseg, toff) != nullptr) ||
			linked_code_segment_raddr(tseg, toff) != nullptr ||
			m2c_alloc_segment_raddr(tseg, toff) != nullptr;
		if (!real_seg) {
			bool inner = false;
			const bool ok = dispatch_external_code(
				static_cast<_offsets>(toff), _state, &inner);
			if (inner) {
				*out_result = ok;
				return true;
			}
		}
	}
	return false;
}

static void host_start_irq_thread() {
	bool expected = false;
	if (!host.timer.irq_running.compare_exchange_strong(expected, true)) {
		return;
	}
	std::thread([] {
		while (host.timer.irq_running.load()) {
			int us = host_irq_period_us.load();
			if (us < 1000) us = 1000; // clamp: don't spin below 1 kHz
			std::this_thread::sleep_for(std::chrono::microseconds(us));
			++*(dd*)host_physical_address(0x40, 0x6c); // BIOS tick count
			// Mark IRQ0/IRQ1C pending; the game thread drains them in
			// host_drain_irq so handler code never races the game on
			// shared (non-thread-local) generated-code bookkeeping.
			host_pending_irq8.fetch_add(1);
			host_pending_irq1c.fetch_add(1);
		}
	}).detach();
}

static uint64_t host_now_us() {
	using clock = std::chrono::steady_clock;
	return std::chrono::duration_cast<std::chrono::microseconds>(
		clock::now().time_since_epoch()).count();
}

static db host_to_bcd(int value) {
	return static_cast<db>(((value / 10) << 4) | (value % 10));
}

#ifndef NOSDL
static int sdl_scancode_to_pc(SDL_Scancode scancode) {
	switch (scancode) {
	case SDL_SCANCODE_ESCAPE: return 1;
	case SDL_SCANCODE_1: return 2;
	case SDL_SCANCODE_2: return 3;
	case SDL_SCANCODE_3: return 4;
	case SDL_SCANCODE_4: return 5;
	case SDL_SCANCODE_5: return 6;
	case SDL_SCANCODE_6: return 7;
	case SDL_SCANCODE_7: return 8;
	case SDL_SCANCODE_8: return 9;
	case SDL_SCANCODE_9: return 10;
	case SDL_SCANCODE_0: return 11;
	case SDL_SCANCODE_MINUS: return 12;
	case SDL_SCANCODE_EQUALS: return 13;
	case SDL_SCANCODE_BACKSPACE: return 14;
	case SDL_SCANCODE_TAB: return 15;
	case SDL_SCANCODE_Q: return 16;
	case SDL_SCANCODE_W: return 17;
	case SDL_SCANCODE_E: return 18;
	case SDL_SCANCODE_R: return 19;
	case SDL_SCANCODE_T: return 20;
	case SDL_SCANCODE_Y: return 21;
	case SDL_SCANCODE_U: return 22;
	case SDL_SCANCODE_I: return 23;
	case SDL_SCANCODE_O: return 24;
	case SDL_SCANCODE_P: return 25;
	case SDL_SCANCODE_LEFTBRACKET: return 26;
	case SDL_SCANCODE_RIGHTBRACKET: return 27;
	case SDL_SCANCODE_RETURN: return 28;
	case SDL_SCANCODE_LCTRL:
	case SDL_SCANCODE_RCTRL: return 29;
	case SDL_SCANCODE_A: return 30;
	case SDL_SCANCODE_S: return 31;
	case SDL_SCANCODE_D: return 32;
	case SDL_SCANCODE_F: return 33;
	case SDL_SCANCODE_G: return 34;
	case SDL_SCANCODE_H: return 35;
	case SDL_SCANCODE_J: return 36;
	case SDL_SCANCODE_K: return 37;
	case SDL_SCANCODE_L: return 38;
	case SDL_SCANCODE_SEMICOLON: return 39;
	case SDL_SCANCODE_APOSTROPHE: return 40;
	case SDL_SCANCODE_GRAVE: return 41;
	case SDL_SCANCODE_LSHIFT: return 42;
	case SDL_SCANCODE_BACKSLASH: return 43;
	case SDL_SCANCODE_Z: return 44;
	case SDL_SCANCODE_X: return 45;
	case SDL_SCANCODE_C: return 46;
	case SDL_SCANCODE_V: return 47;
	case SDL_SCANCODE_B: return 48;
	case SDL_SCANCODE_N: return 49;
	case SDL_SCANCODE_M: return 50;
	case SDL_SCANCODE_COMMA: return 51;
	case SDL_SCANCODE_PERIOD: return 52;
	case SDL_SCANCODE_SLASH: return 53;
	case SDL_SCANCODE_RSHIFT: return 54;
	case SDL_SCANCODE_KP_MULTIPLY: return 55;
	case SDL_SCANCODE_LALT:
	case SDL_SCANCODE_RALT: return 56;
	case SDL_SCANCODE_SPACE: return 57;
	case SDL_SCANCODE_CAPSLOCK: return 58;
	case SDL_SCANCODE_F1: return 59;
	case SDL_SCANCODE_F2: return 60;
	case SDL_SCANCODE_F3: return 61;
	case SDL_SCANCODE_F4: return 62;
	case SDL_SCANCODE_F5: return 63;
	case SDL_SCANCODE_F6: return 64;
	case SDL_SCANCODE_F7: return 65;
	case SDL_SCANCODE_F8: return 66;
	case SDL_SCANCODE_F9: return 67;
	case SDL_SCANCODE_F10: return 68;
	case SDL_SCANCODE_NUMLOCKCLEAR: return 69;
	case SDL_SCANCODE_SCROLLLOCK: return 70;
	case SDL_SCANCODE_KP_7:
	case SDL_SCANCODE_HOME: return 71;
	case SDL_SCANCODE_KP_8:
	case SDL_SCANCODE_UP: return 72;
	case SDL_SCANCODE_KP_9:
	case SDL_SCANCODE_PAGEUP: return 73;
	case SDL_SCANCODE_KP_MINUS: return 74;
	case SDL_SCANCODE_KP_4:
	case SDL_SCANCODE_LEFT: return 75;
	case SDL_SCANCODE_KP_5: return 76;
	case SDL_SCANCODE_KP_6:
	case SDL_SCANCODE_RIGHT: return 77;
	case SDL_SCANCODE_KP_PLUS: return 78;
	case SDL_SCANCODE_KP_1:
	case SDL_SCANCODE_END: return 79;
	case SDL_SCANCODE_KP_2:
	case SDL_SCANCODE_DOWN: return 80;
	case SDL_SCANCODE_KP_3:
	case SDL_SCANCODE_PAGEDOWN: return 81;
	case SDL_SCANCODE_KP_0:
	case SDL_SCANCODE_INSERT: return 82;
	case SDL_SCANCODE_KP_PERIOD:
	case SDL_SCANCODE_DELETE: return 83;
	case SDL_SCANCODE_F11: return 87;
	case SDL_SCANCODE_F12: return 88;
	default: return -1;
	}
}
#endif

// Weak default: games whose INT 9 hardware-keyboard ISR was not translated
// (kept as data bytes) provide a strong override to maintain their held-key
// bitmask. Called on every host key make (pressed) / break (released).
// host_int9_diverts_key mirrors the real ISR's routing: a key is diverted to the
// held-key bitmask only when it has a table entry; all other keys (and keys
// pressed while the ISR is disabled) still reach the BIOS buffer for INT 16h.
__attribute__((weak)) void host_int9_update(int scan_code, bool pressed) {}
__attribute__((weak)) bool host_int9_diverts_key(int scan_code) { return false; }

// Terminal (stdin) input produces only key-down events -- there is no release.
// Emulate a short key tap: raise the held-key bit immediately, then release it
// ~60ms later so menus that sample the held-key bitmask register one press.
struct HostTap { int scan; uint64_t release_us; };
static HostTap host_taps[8];
static int host_tap_count = 0;

static void host_int9_tap(int scan_code) {
	if (scan_code <= 0 || scan_code >= 0x80) return;
	host_int9_update(scan_code, true);
	if (host_tap_count < 8) {
		host_taps[host_tap_count].scan = scan_code;
		host_taps[host_tap_count].release_us = host_now_us() + 60000;
		++host_tap_count;
	}
}

static void host_int9_release_taps() {
	const uint64_t now = host_now_us();
	for (int i = 0; i < host_tap_count; ++i) {
		if (now >= host_taps[i].release_us) {
			host_int9_update(host_taps[i].scan, false);
			host_taps[i] = host_taps[--host_tap_count];
			--i;
		}
	}
}

static void host_set_key(int scan_code, bool pressed) {
	if (scan_code < 0 || scan_code >= 128) {
		return;
	}
	host.keyboard_scan_code = pressed ? scan_code : (scan_code | 0x80);
	// The game's INT 9 held-key bitmask is independent of the generic key[]
	// table; update it even when that table is absent (key is a null weak sym).
	host_int9_update(scan_code, pressed);
	db* keys = host_key_state();
	if (keys == nullptr) {
		return;
	}
	keys[scan_code] = pressed ? 1 : 0;
	switch (scan_code) {
	case 42:
		keys[54] = keys[42];
		break;
	case 54:
		keys[42] = keys[54];
		break;
	case 12:
		keys[74] = keys[12];
		break;
	case 74:
		keys[12] = keys[74];
		break;
	case 13:
		keys[78] = keys[13];
		break;
	case 78:
		keys[13] = keys[78];
		break;
	default:
		break;
	}
}

#ifndef NOSDL
static db sdl_keycode_to_bios_ascii(SDL_Keycode keycode, SDL_Keymod modifiers) {
	const bool shifted = (modifiers & KMOD_SHIFT) != 0;
	if (keycode >= SDLK_a && keycode <= SDLK_z) {
		const int letter = keycode - SDLK_a;
		return static_cast<db>((shifted ? 'A' : 'a') + letter);
	}
	if (keycode >= SDLK_0 && keycode <= SDLK_9) {
		static const char normal[] = "0123456789";
		static const char shifted_digits[] = ")!@#$%^&*(";
		const int digit = keycode - SDLK_0;
		return static_cast<db>((shifted ? shifted_digits : normal)[digit]);
	}
	switch (keycode) {
	case SDLK_SPACE: return ' ';
	case SDLK_RETURN:
	case SDLK_KP_ENTER: return '\r';
	case SDLK_ESCAPE: return 0x1b;
	case SDLK_BACKSPACE: return '\b';
	case SDLK_TAB: return '\t';
	case SDLK_MINUS: return shifted ? '_' : '-';
	case SDLK_EQUALS: return shifted ? '+' : '=';
	case SDLK_LEFTBRACKET: return shifted ? '{' : '[';
	case SDLK_RIGHTBRACKET: return shifted ? '}' : ']';
	case SDLK_BACKSLASH: return shifted ? '|' : '\\';
	case SDLK_SEMICOLON: return shifted ? ':' : ';';
	case SDLK_QUOTE: return shifted ? '"' : '\'';
	case SDLK_COMMA: return shifted ? '<' : ',';
	case SDLK_PERIOD: return shifted ? '>' : '.';
	case SDLK_SLASH: return shifted ? '?' : '/';
	case SDLK_BACKQUOTE: return shifted ? '~' : '`';
	default: return 0;
	}
}

static dw sdl_key_event_to_bios_key(const SDL_KeyboardEvent& event) {
	const int scan_code = sdl_scancode_to_pc(event.keysym.scancode);
	if (scan_code < 0 || scan_code > 0xff) {
		return 0;
	}
	return static_cast<dw>((scan_code << 8) | sdl_keycode_to_bios_ascii(event.keysym.sym, SDL_GetModState()));
}
#endif

// The game timer handlers are far procedures ending in RETF/IRET. Like a real
// interrupt, push a frame onto the current stack: the handler's final far
// return pops it and unwinds to C++ (is_dos_terminate_vector treats 0:0 as the
// synthesized-frame sentinel). The whole CPU state is restored afterwards: an
// interrupt must not leak the popped sentinel values (cs=0, eip=0) or an
// unbalanced sp into the interrupted code.
static void host_run_timer_handler(m2cf* handler, struct _STATE* _state) {
	const struct _STATE saved = *_state;
	// Snapshot native-return bookkeeping; a StackPop unwind out of the handler
	// can bypass the matching RET and leave stale marks behind.
	const size_t saved_marks = m2c::native_return_marks.size();
	const size_t saved_values = m2c::native_return_values.size();
	const size_t saved_depth = m2c::native_return_call_depth;
	const bool saved_suppress = m2c::suppress_native_return_push_transfer;
	m2c::suppress_native_return_push_transfer = true;
	PUSH_((dw)0, _state); // flags slot (IRET) / padding (RETF)
	PUSH_((dw)0, _state); // sentinel cs
	PUSH_((dw)0, _state); // sentinel ip=0 -> unwind to C++
	m2c::suppress_native_return_push_transfer = saved_suppress;
#ifdef SHADOW_STACK
	// Isolate the handler's bookkeeping: its pushes/rets must not perturb the
	// interrupted code's call-depth accounting (spurious StackPop unwinds).
	const ShadowStack::SavedState saved_shadow = m2c::shadow_stack.save_state();
#endif
	try {
		handler(0, _state);
	} catch (const m2c::StackPop&) {
		// A RETF inside the handler unwound past the interrupt entry frame.
		// The emulated state is restored below either way.
	}
	*_state = saved;
	m2c::native_return_marks.resize(saved_marks);
	m2c::native_return_values.resize(saved_values);
	m2c::native_return_call_depth = saved_depth;
	m2c::suppress_native_return_push_transfer = saved_suppress;
#ifdef SHADOW_STACK
	m2c::shadow_stack.restore_state(saved_shadow);
	// The sentinel words and the handler's own pushes left frames below the
	// live stack top; they are stale now and would otherwise be miscounted as
	// uncontrolled pops by later scans.
	m2c::shadow_stack.clear_frames_below((dw)saved.esp);
#endif
}

static void host_run_timer(struct _STATE* _state) {
	if (!host.timer.enabled || host.timer.in_callback) {
		return;
	}
	const uint64_t now_us = host_now_us();
	if (host.timer.last_us == 0) {
		host.timer.last_us = now_us;
		return;
	}
	uint64_t delta_us = now_us - host.timer.last_us;
	host.timer.last_us = now_us;
	delta_us = std::min<uint64_t>(delta_us, 250000);
	host.timer.accum_us += delta_us;

	HostIrqCallbackGuard callback_guard;
	int ticks_this_pump = 0;
	while (host.timer.accum_us >= 10000 && ticks_this_pump < 5) {
		host.timer.accum_us -= 10000;
		++ticks_this_pump;
		if (::gameintr100) {
			host_run_timer_handler(::gameintr100, _state);
		}
		if (++host.timer.divider_20hz >= 5) {
			host.timer.divider_20hz = 0;
			if (::gameintr20) {
				host_run_timer_handler(::gameintr20, _state);
			}
		}
	}
}

static void poll_host_stdin() {
#if !defined(_WIN32) && !defined(__DJGPP__)
	/* Terminal arrow keys arrive as CSI "ESC [ <final>". Parse that sequence so
	   they produce PC extended keys (AL=0, AH=scancode) the menu code expects.
	   A bare ESC (no '[' following) still pushes the Escape key. */
	static int esc_state = 0;   // 0 = normal, 1 = got ESC, 2 = got "ESC ["
	for (int n = 0; n < 8 && !host_keyboard_buffer_full(); ++n) {
		fd_set readfds;
		FD_ZERO(&readfds);
		FD_SET(STDIN_FILENO, &readfds);
		timeval timeout = {0, 0};
		if (select(STDIN_FILENO + 1, &readfds, NULL, NULL, &timeout) <= 0 ||
		    !FD_ISSET(STDIN_FILENO, &readfds)) {
			break;
		}
		unsigned char ch = 0;
		if (read(STDIN_FILENO, &ch, 1) <= 0) {
			break;
		}
		dw key = 0;
		if (esc_state == 0) {
			if (ch == 0x1b) { esc_state = 1; continue; }
			key = host_stdin_char_to_bios_key(ch);
		} else if (esc_state == 1) {
			if (ch == '[') { esc_state = 2; continue; }
			esc_state = 0;
			host_keyboard_push(host_stdin_char_to_bios_key(0x1b));
			if (host_keyboard_buffer_full()) break;
			key = host_stdin_char_to_bios_key(ch);   // ESC then a normal key
		} else { // esc_state == 2, final byte of CSI
			esc_state = 0;
			int scan = 0;
			switch (ch) {
			case 'A': scan = 0x48; break; // up
			case 'B': scan = 0x50; break; // down
			case 'C': scan = 0x4d; break; // right
			case 'D': scan = 0x4b; break; // left
			case 'H': scan = 0x47; break; // home
			case 'F': scan = 0x4f; break; // end
			default: break;
			}
			if (!scan) continue;
			key = (dw)(scan << 8); // extended key: AL=0, AH=scancode
		}
		if (key) {
			// A key is diverted to the game's held-key bitmask only when its
			// INT 9 ISR maps it (table entry nonzero); all other keys still
			// chain to the BIOS buffer for INT 16h. Terminal keys have no
			// release event, so emulate a short tap for diverted keys.
			if (host_int9_diverts_key((key >> 8) & 0x7f)) {
				host_int9_tap((key >> 8) & 0x7f);
			} else {
				host_keyboard_push(key);
			}
		}
	}
#endif
}

#ifndef NOCURSES
static void host_render_text_memory() {
	if (host.vga.current_mode > 3 && host.vga.current_mode != 7) {
		return;
	}
	static db shadow[80 * 25 * 2] = {};
	const db *vram = reinterpret_cast<const db*>(&m) +
		(static_cast<size_t>(host.vga.current_mode == 7 ? 0xB0000 : 0xB8000));
	if (std::memcmp(vram, shadow, sizeof(shadow)) == 0) {
		return;
	}
	std::memcpy(shadow, vram, sizeof(shadow));
	for (int pos = 0; pos < 80 * 25; ++pos) {
		const db ch = vram[pos * 2] ? vram[pos * 2] : ' ';
		const db attr = vram[pos * 2 + 1];
		const int pair = ((attr >> 4) & 0x0f) * 16 + (attr & 0x0f);
		mvaddch(pos / 80, pos % 80, ch | COLOR_PAIR(pair));
	}
	const db page = host_text_page(host.vga.active_page);
	move(host.vga.cursor_row[page], host.vga.cursor_col[page]);
	refresh();
}
#endif

static void poll_host_events(struct _STATE* _state) {
	poll_host_stdin();
	host_int9_release_taps();
#ifndef NOCURSES
	host_render_text_memory();
#endif
#ifndef NOSDL
	if ((SDL_WasInit(SDL_INIT_VIDEO) & SDL_INIT_VIDEO) != 0) {
		SDL_Event event;
		while (SDL_PollEvent(&event)) {
			switch (event.type) {
			case SDL_QUIT:
				executionFinished = true;
				jumpToBackGround = true;
				break;
			case SDL_MOUSEMOTION:
				host.mouse.x = event.motion.x;
				host.mouse.y = event.motion.y;
				host.mouse.motion_x += event.motion.xrel;
				host.mouse.motion_y += event.motion.yrel;
				clamp_host_mouse();
				break;
			case SDL_MOUSEBUTTONDOWN:
			case SDL_MOUSEBUTTONUP: {
				int bit = 0;
				if (event.button.button == SDL_BUTTON_LEFT) {
					bit = 1;
				} else if (event.button.button == SDL_BUTTON_RIGHT) {
					bit = 2;
				} else if (event.button.button == SDL_BUTTON_MIDDLE) {
					bit = 4;
				}
				if (event.type == SDL_MOUSEBUTTONDOWN) {
					host.mouse.buttons |= bit;
				} else {
					host.mouse.buttons &= ~bit;
				}
				break;
			}
			case SDL_KEYDOWN:
			case SDL_KEYUP: {
				const int pc_scan =
					sdl_scancode_to_pc(event.key.keysym.scancode);
				host_set_key(pc_scan, event.type == SDL_KEYDOWN);
				// A key diverted to the game's held-key bitmask (mapped in its
				// INT 9 ISR table) is consumed by it; every other key still
				// chains to the BIOS buffer for INT 16h, as on real hardware.
				if (event.type == SDL_KEYDOWN && event.key.repeat == 0 &&
					!host_int9_diverts_key(pc_scan)) {
					host_keyboard_push(sdl_key_event_to_bios_key(event.key));
				}
				break;
			}
			default:
				break;
			}
		}
	}
#endif
	host_run_timer(_state);
	host_drain_irq();
#ifndef NOSDL
	/* Flush any pending frame tail on screens that draw then idle waiting for
	   input without polling the retrace port; rate-limited so it stays cheap. */
	vga_present_pending();
#endif
}

static bool host_keyboard_wait(struct _STATE* _state, dw* bios_key) {
	while (!executionFinished) {
		poll_host_events(_state);
		if (host_keyboard_pop(bios_key)) {
			return true;
		}
		std::this_thread::sleep_for(std::chrono::milliseconds(1));
	}
	return false;
}

#define MAX_FMT_SIZE 1024
void log_error(const char *fmt, ...) {
	char formatted_string[MAX_FMT_SIZE];
	va_list argptr;
	va_start(argptr,fmt);
	vsprintf (formatted_string,fmt, argptr);
	va_end(argptr);
#ifdef __LIBRETRO__
	log_cb(RETRO_LOG_ERROR,"%s",formatted_string);
#else
	if (logDebug!=NULL) { fprintf(logDebug,"%s",formatted_string); fflush(logDebug);}
	{ printf("%s",formatted_string); }
	/* Errors must be visible even when stdout is redirected into a trace
	 * file or /dev/null -- always mirror to stderr and flush. */
	{ fprintf(stderr, "%s", formatted_string); fflush(stderr); }
#endif
}
void log_debug(const char *fmt, ...) {
#if M2CDEBUG
	char formatted_string[MAX_FMT_SIZE];
	va_list argptr;
	va_start(argptr,fmt);
	vsprintf (formatted_string,fmt, argptr);
	va_end(argptr);
#ifdef __LIBRETRO__
	log_cb(RETRO_LOG_DEBUG,"%s",formatted_string);
#else
	if (logDebug!=NULL) { fprintf(logDebug,"%s",formatted_string); fflush(logDebug); } else { printf("%s",formatted_string); }
#endif
#endif
}

void log_info(const char *fmt, ...) {
	char formatted_string[MAX_FMT_SIZE];
	va_list argptr;
	va_start(argptr,fmt);
	vsprintf (formatted_string,fmt, argptr);
	va_end(argptr);
#ifdef __LIBRETRO__
	log_cb(RETRO_LOG_INFO,"%s",formatted_string);
#else
	if (logDebug!=NULL) { fprintf(logDebug,"%s",formatted_string); fflush(logDebug); } else { printf("%s",formatted_string); }
#endif
}

void log_debug2(const char *fmt, ...) {
#if M2CDEBUG>=2
	char formatted_string[MAX_FMT_SIZE];
	va_list argptr;
	va_start(argptr,fmt);
	vsprintf (formatted_string,fmt, argptr);
	va_end(argptr);
	log_debug(formatted_string);
#endif
}

void checkIfVgaRamEmpty() {
#ifndef NOSDL
 #if SDL_MAJOR_VERSION == 2
	int i;
	int vgaram_empty = 1;
	for(i = 0; i < VGARAM_SIZE; i++)
		if(vgaRam[i])
			vgaram_empty = 0;
	log_debug("vgaram_empty : %s\n", vgaram_empty ? "true" : "false");
	(void) vgaram_empty;
 #endif
#endif
}

void stackDump(struct _STATE* _state) {
	if (!_state) {
		log_debug("stackDump skipped: no CPU state provided\n");
		return;
	}
X86_REGREF

	log_debug("is_little_endian()=%d\n",isLittle);
	log_debug("sizeof(dd)=%zu\n",sizeof(dd));
	log_debug("sizeof(dd *)=%zu\n",sizeof(dd *));
	log_debug("sizeof(dw)=%zu\n",sizeof(dw));
	log_debug("sizeof(db)=%zu\n",sizeof(db));
//	log_debug("sizeof(jmp_buf)=%zu\n",sizeof(jmp_buf));
//	log_debug("sizeof(mem)=%zu\n",sizeof(m));
	log_debug("eax: %x\n",eax);
//	hexDump(&eax,sizeof(dd));
	log_debug("ebx: %x\n",ebx);
	log_debug("ecx: %x\n",ecx);
	log_debug("edx: %x\n",edx);
	log_debug("ebp: %x\n",ebp);
	log_debug("cs: %d -> %p\n",cs,(void *) realAddress(0,cs));
	log_debug("ds: %d -> %p\n",ds,(void *) realAddress(0,ds));
	log_debug("esi: %x\n",esi);
	log_debug("ds:esi %p\n",(void *) realAddress(esi,ds));
	log_debug("es: %d -> %p\n",es,(void *) realAddress(0,es));
	hexDump(&es,sizeof(dd));
	log_debug("edi: %x\n",edi);
	log_debug("es:edi %p\n",(void *) realAddress(edi,es));
	log_debug("es:edi hex dump skipped; diagnostic dumps must not dereference arbitrary emulated addresses\n");
	log_debug("fs: %d -> %p\n",fs,(void *) realAddress(0,fs));
	log_debug("gs: %d -> %p\n",gs,(void *) realAddress(0,gs));
//	log_debug("adress heap: %p\n",(void *) &m.heap);
#ifndef NOSDL
 #if SDL_MAJOR_VERSION == 2
	log_debug("adress vgaRam: %p\n",(void *) &vgaRam);
	log_debug("first pixels vgaRam: %x\n",*vgaRam);
 #endif
#endif
	log_debug("flags: ZF = %d\n",GET_ZF());
	log_debug("top stack=%d\n",stackPointer);
	// Diagnostic: dump the emulated stack window around ss:sp so the failing
	// return-address chain is visible even when debug logging is compiled out.
	{
		db* sb = (db*)m2c::stack_raddr_(ss, (dw)(stackPointer - 16));
		fprintf(stderr, "[stackdump] ss=%04x sp=%04x words from sp-16:\n", ss, stackPointer);
		for (int i = -16; i < 64; i += 2) {
			dw w = *(dw*)(sb + (i + 16));
			fprintf(stderr, "  sp%+03d = %04x\n", i, w);
		}
		// Dump the tracked native-return marks/values so a dispatch failure
		// shows which return markers are live and at what sp/depth.
		fprintf(stderr, "[marks] depth=%zu nmarks=%zu nvals=%zu\n",
			(size_t)native_return_call_depth,
			native_return_marks.size(), native_return_values.size());
		int shown = 0;
		for (auto it = native_return_marks.rbegin();
		     it != native_return_marks.rend() && shown < 12; ++it, ++shown) {
			fprintf(stderr, "  mark rip=%04x ss=%04x sp=%04x depth=%zu id=%zu\n",
				(unsigned)it->return_ip, it->stack_segment,
				it->stack_offset, it->call_depth, it->id);
		}
		for (auto it = native_return_values.rbegin();
		     it != native_return_values.rend() && shown < 24; ++it, ++shown) {
			fprintf(stderr, "  val  rip=%04x depth=%zu id=%zu carrier=%p\n",
				(unsigned)it->return_ip, it->call_depth, it->id, it->carrier);
		}
		fflush(stderr);
	}
	checkIfVgaRamEmpty();
}

// thanks to paxdiablo http://stackoverflow.com/users/14860/paxdiablo for the hexDump function
void hexDump (void *addr, int len) {
	int i;
	unsigned char buff[17];
	unsigned char *pc = (unsigned char*)addr;
	(void) buff;
	log_debug ("hexDump %p:\n", addr);

	if (len == 0) {
		log_debug("  ZERO LENGTH\n");
		return;
	}
	if (len < 0) {
		log_debug("  NEGATIVE LENGTH: %i\n",len);
		return;
	}

	// Process every byte in the data.
	for (i = 0; i < len; i++) {
		// Multiple of 16 means new line (with line offset).

		if ((i % 16) == 0) {
			// Just don't print ASCII for the zeroth line.
			if (i != 0)
				log_debug ("  %s\n", buff);

			// Output the offset.
			log_debug ("  %04x ", i);
		}

		// Now the hex code for the specific character.
		log_debug (" %02x", pc[i]);

		// And store a printable ASCII character for later.
		if ((pc[i] < 0x20) || (pc[i] > 0x7e))
			buff[i % 16] = '.';
		else
			buff[i % 16] = pc[i];
		buff[(i % 16) + 1] = '\0';
	}

	// Pad out last line if not exactly 16 characters.
	while ((i % 16) != 0) {
		log_debug ("   ");
		i++;
	}

	// And print the final ASCII bit.
	log_debug ("  %s\n", buff);
}

void asm2C_OUT(int16_t address, int data,_STATE* _state) {
#ifdef __DJGPP__
	outportb(address, data);
#else
X86_REGREF
	if ((data & ~0xff) != 0) {
		const int port = address & 0xffff;
		if (port == 0x3c4 || port == 0x3ce || port == 0x3d4) {
			asm2C_OUT(address, data & 0xff, _state);
			asm2C_OUT(address + 1, (data >> 8) & 0xff, _state);
			return;
		}
	}
	data &= 0xff;
	switch(address & 0xffff) {
	case 0x00:
	case 0x01:
	case 0x02:
	case 0x03:
	case 0x04:
	case 0x05:
	case 0x06:
	case 0x07:
	case 0x08:
	case 0x09:
	case 0x0a:
	case 0x0b:
	case 0x0c:
	case 0x0d:
	case 0x0e:
	case 0x0f:
		break; // 8237 DMA controller ports; hosted runtime does not execute DMA transfers.
	case 0x20:
	case 0x21:
		break;
		case 0x40:
			host.pit.channel0_latch = data;
			// In lobyte-then-hibyte mode (control 0x36) the first write is the
			// low divisor byte, the second the high byte. When the divisor
			// completes, derive the int8 tick period (PIT clock ~1.19318 MHz).
			if (!host.pit.channel0_waiting_high) {
				host.pit.channel0_low = data;
				host.pit.channel0_waiting_high = true;
			} else {
				host.pit.channel0_divisor = (uint16_t)((data << 8) | host.pit.channel0_low);
				host.pit.channel0_waiting_high = false;
				uint32_t d = host.pit.channel0_divisor ? host.pit.channel0_divisor : 0x10000;
				host_irq_period_us.store((int)((d / 1193181.818) * 1000000.0));
			}
			break;
	case 0x43:
		// Channel-0 control with lobyte/hibyte access (0x3x) restarts the
		// two-write divisor sequence on port 0x40.
		if ((data & 0xc0) == 0 && (data & 0x30) == 0x30) {
			host.pit.channel0_waiting_high = false;
		}
		break;
	case 0x61:
		host.ppi_port_b = data;
		break;
	case 0x64:
		break; // 8042 keyboard controller command port.
	case 0xc0:
	case 0xc1:
		tandy_snd_write(data);
		break; // Tandy SN76496/NCR8496 sound chip.
	case 0x3c0:
		if (host.vga.attr_waiting_for_index) {
			host.vga.attr_index = data & 0x1f;
		} else {
			host.vga.attr_regs[host.vga.attr_index] = data;
		}
		host.vga.attr_waiting_for_index = !host.vga.attr_waiting_for_index;
		break;
	case 0x3c4:
		host.vga.seq_index = data;
		break;
	case 0x3c5:
		host.vga.seq_regs[host.vga.seq_index] = data;
		break;
	case 0x3c7:
		host.vga.dac_read_index = (static_cast<size_t>(data) * 3) % (256 * 3);
		break;
	case 0x3c8:
		host.vga.dac_write_index = (static_cast<size_t>(data) * 3) % (256 * 3);
		host.vga.dac_write_start = host.vga.dac_write_index;
		host.vga.dac_write_count = 0;
		break;
	case 0x3c9:
		if (host.vga.dac_write_index < 256 * 3) {
			vgaPalette[host.vga.dac_write_index]=data;
			host.vga.dac_write_index = (host.vga.dac_write_index + 1) % (256 * 3);
			++host.vga.dac_write_count;
			vga_maybe_dump_dac_upload();
  #if SDL_MAJOR_VERSION == 2 && !defined(NOSDL) && M2CDEBUG != -1
			vga_render_dirty = true;
  #endif
		} else {
			log_error("error: dac_write_index>767 %zu\n", host.vga.dac_write_index);
		}
		break;
	case 0x3ce:
		host.vga.gc_index = data;
		break;
	case 0x3cf:
		host.vga.gc_regs[host.vga.gc_index] = data;
		break;
	case 0x3d4:
		host.vga.crtc_index = data;
		break;
	case 0x3d5:
		host.vga.crtc_regs[host.vga.crtc_index] = data;
		break;
	default:
		log_error("unknown OUT %x,%x at %x:%x\n",address, data,cs,eip);
		break;
	}
#endif
}

int8_t asm2C_IN(int16_t address,_STATE* _state) {
#ifdef __DJGPP__
	return inportb(address);
#else
X86_REGREF
	poll_host_events(_state);
		static bool vblTick = 1;
			switch(address & 0xffff) {
			case 0x00:
				return 0;
			case 0x20:
			case 0x21:
				return 0;
			case 0x40:
				return host.pit.channel0_latch;
			case 0x60:
				return host.keyboard_scan_code;
		case 0x61:
			return host.ppi_port_b;
		case 0x64:
			return 0;  // keyboard controller status: no pending host scancode
		case 0x201:
			{
				return 0xff;  // no joystick
			}
	case 0x3c1:
		return host.vga.attr_regs[host.vga.attr_index];
	case 0x3c4:
		{
			static const int disable_ega = std::getenv("M2C_DISABLE_EGA") ? 1 : 0;
			if (disable_ega) {
				return 0;
			}
			return host.vga.seq_index;
		}
	case 0x3c5:
		return host.vga.seq_regs[host.vga.seq_index];
	case 0x3cf:
		return host.vga.gc_regs[host.vga.gc_index];
	case 0x3c9:
		{
			maybe_apply_translated_vga_panel_palette();
			const db value = vgaPalette[host.vga.dac_read_index];
			host.vga.dac_read_index = (host.vga.dac_read_index + 1) % (256 * 3);
			return value;
		}
	case 0x3d4:
		return host.vga.crtc_index;
	case 0x3b4:
		return host.vga.crtc_index;
	case 0x3DA:
		host.vga.attr_waiting_for_index = true;
  #if SDL_MAJOR_VERSION == 2 && !defined(NOSDL) && M2CDEBUG != -1
		vga_present_forced();
  #endif
		if (vblTick) {
			vblTick = 0;
			return 0;
		} else {
			vblTick = 1;
			jumpToBackGround = 1;
			return 8;
		}
		//break;
	case 0x3d5:
		return host.vga.crtc_regs[host.vga.crtc_index];
	case 0x3b5:
		return host.vga.crtc_regs[host.vga.crtc_index];
	default:
		log_error("Unknown IN %x at %x:%x\n",address,cs,eip);
		return 0;
	}
#endif
}

uint16_t asm2C_INW(uint16_t address,_STATE* _state) {
#ifdef __DJGPP__
	return inportw(address);
#else
X86_REGREF
	switch(address) {
	case 0x3DA:
		break;
	default:
		log_error("Unknown IN %x at %x:%x\n",address,cs,eip);
		return 0;
	}
#endif
	return 0;
}

bool is_little_endian_real_check() {
	union
	{
		uint16_t x;
		uint8_t y[2];
	} u;

	u.x = 1;
	return u.y[0];
}

/**
 * is_little_endian:
 *
 * Checks if the system is little endian or big-endian.
 *
 * Returns: greater than 0 if little-endian,
 * otherwise big-endian.
 **/
bool is_little_endian()
{
#if defined(__x86_64) || defined(__i386) || defined(_M_IX86) || defined(_M_X64)
	return 1;
#elif defined(MSB_FIRST)
	return 0;
#else
	return is_little_endian_real_check();
#endif
}


#ifndef __BORLANDC__ //TODO
//#if !CYGWIN
double realElapsedTime(void) {              // returns 0 first time called
#ifndef _WIN32
	struct timeval tv;
    gettimeofday(&tv, 0);
    return ((tv.tv_sec /*- t0.tv_sec*/ + (tv.tv_usec /* - t0.tv_usec*/)) / 1000000.) * 18.;
#else
	return 0;
#endif
}
#endif
/*
#else
#include <windows.h>
double realElapsedTime(void) {              // granularity about 50 microsecs
    static LARGE_INTEGER freq, start;
    LARGE_INTEGER count;
    if (!QueryPerformanceCounter(&count))
        assert(0 && "QueryPerformanceCounter");
    if (!freq.QuadPart) {                   // one time initialization
        if (!QueryPerformanceFrequency(&freq))
            assert(0 && "QueryPerformanceFrequency");
        start = count;
    }
    return (double)(count.QuadPart) / freq.QuadPart;
}
#endif
*/
void call_dos_realint(struct _STATE* _state, int a)
{

#ifdef __DJGPP__
X86_REGREF
	log_debug2("call_dos_realint %x ax=%x bx=%x cx=%x dx=%x\n",a,ax,bx,cx,dx);
__dpmi_regs _dpmi_reg;
   _dpmi_reg.x.ax = ax;
   _dpmi_reg.x.bx = bx;
   _dpmi_reg.x.cx = cx;
   _dpmi_reg.x.dx = dx;
   _dpmi_reg.x.si = si;
   _dpmi_reg.x.di = di;
   _dpmi_reg.x.bp = bp;
   _dpmi_reg.x.ds = ds;
   _dpmi_reg.x.es = es;
   __dpmi_int(a, &_dpmi_reg);
   ds = _dpmi_reg.x.ds;
   es = _dpmi_reg.x.es;
   ax = _dpmi_reg.x.ax;
   bx = _dpmi_reg.x.bx;
   cx = _dpmi_reg.x.cx;
   dx = _dpmi_reg.x.dx;
   si = _dpmi_reg.x.si;
   di = _dpmi_reg.x.di;
   bp = _dpmi_reg.x.bp;
#endif

}

void call_dos_protint(struct _STATE* _state, int a)
{
#ifdef __DJGPP__
X86_REGREF
// int21h: 9, 39h, 3Ah, 3Bh, 3Ch, 3Dh, 3Fh, 40h, 41h, 43h, 47h, 56h
	log_debug2("call_dos_protint %x eax=%x ebx=%x ecx=%x edx=%x\n",a,eax,ebx,ecx,edx);
     union REGS _dpmi_reg;
   _dpmi_reg.d.eax = eax;
   _dpmi_reg.d.ebx = ebx;
   _dpmi_reg.d.ecx = ecx;
   _dpmi_reg.d.edx = (dd)raddr(ds,dx);
   _dpmi_reg.d.esi = esi;
   _dpmi_reg.d.edi = (dd)raddr(es,di);//edi;
   _dpmi_reg.d.ebp = ebp;
   _dpmi_reg.d.ebx = ebx;

   int86(a, &_dpmi_reg, &_dpmi_reg);

   eax = _dpmi_reg.d.eax;
   ebx = _dpmi_reg.d.ebx;
   ecx = _dpmi_reg.d.ecx;
//   edx = _dpmi_reg.d.edx;
   esi = _dpmi_reg.d.esi;
   edi = _dpmi_reg.d.edi;
   ebx = _dpmi_reg.d.ebx;
   ebp = _dpmi_reg.d.ebp;
   AFFECT_CF(_dpmi_reg.d.cflag&1);
#endif

}


void asm2C_init() {
	isLittle=is_little_endian();
#ifdef MSB_FIRST
	if (isLittle) {
		log_error("Inconsistency: is_little_endian=true and MSB_FIRST defined.\n");
		exit(1);
	}
#endif
	if (isLittle!=is_little_endian_real_check()) {
		log_error("Inconsistency in little/big endianess detection. Please check if the Makefile sets MSB_FIRST properly for this architecture.\n");
		exit(1);
	}
	log_debug2("asm2C_init is_little_endian:%d\n",isLittle);
}


void asm2C_INT(struct _STATE* _state, int a) {
X86_REGREF
	static FILE * file;
	int i;
	AFFECT_CF(0);
	int rc;
#if M2CDEBUG>=2
	{
		static char last[128] = "";
		static int rep = 0;
		char cur[128];
		snprintf(cur, sizeof(cur), "INT%02x ax=%04x bx=%04x cx=%04x dx=%04x ds=%04x es=%04x\n",
			a, ax & 0xffff, bx & 0xffff, cx & 0xffff, dx & 0xffff, ds, es);
		if (!strcmp(cur, last)) { ++rep; }
		else {
			if (rep) { fprintf(stderr, "   [repeated x%d]\n", rep); rep = 0; }
			fprintf(stderr, "%s", cur);
			strncpy(last, cur, sizeof(last) - 1);
		}
	}
#endif
#define SUCCESS         0       /* Function was successful      */
	log_debug2("INT %x ax=%x bx=%x cx=%x dx=%x\n",a,ax,bx,cx,dx);


	switch(a) {
	case 0x80:
	case 0x81:
		/* Hosted Tornado builds load DOS sound driver binaries and invoke them
		   through private interrupts. The binaries are not executed here; expose
		   a deterministic no-op driver so translated sound code does not fall
		   into the generic unsupported interrupt path. */
		if (ah == 0x05 || ah == 0x14) {
			al = 0; // Tornado treats AL == 55h as "card missing".
		}
		AFFECT_CF(0);
		return;
	case 0x10:
	{
		switch(ah)
			{
			case 0: { // set mode
				host.vga.current_mode = al;
				switch(al)
				 {
				case 0x03: {
#ifndef NOCURSES
					resize_term(25, 80);
					clear();
					refresh();
#endif
					host_text_clear_all();
					log_debug2("Switch to text mode\n");
					return;
				}
			
			case 0x04: {
				log_debug2("Switch to CGA\n");
#ifdef __DJGPP__
        call_dos_realint(_state, a);
#endif

#ifndef NOSDL
 #if SDL_MAJOR_VERSION == 2

				init_sdl_vga_window();
				if (renderer) {
					SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
					SDL_RenderClear(renderer);
					SDL_RenderPresent(renderer);
				}
 #endif
#endif
				//stackDump(_state);
				return;
			}

				case 0x83: {
#ifndef NOCURSES

					resize_term(25, 80);
					refresh();
#endif
					host_text_clear_all();
					log_debug2("Switch to text mode\n");
					return;
				}
			case 0x13: {
				log_debug2("Switch to VGA\n");
				vga_set_mode13_defaults();
#ifdef __DJGPP__
        call_dos_realint(_state, a);
#endif

#ifndef NOSDL
 #if SDL_MAJOR_VERSION == 2

				init_sdl_vga_window();
				if (renderer) {
					SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
					SDL_RenderClear(renderer);
					SDL_RenderPresent(renderer);
				}
 #endif
#endif
				//stackDump(_state);
				return;
			 }
			}

			}
			case 0x0f: { // get current video mode
				al = host.vga.current_mode;
				ah = 80;
				bh = host.vga.active_page;
				return;
			}
			case 0x02: { // set cursor
				const db page = host_text_page(bh);
				host.vga.cursor_row[page] = host_text_row(dh);
				host.vga.cursor_col[page] = host_text_col(dl);
#ifndef NOCURSES
				    int y,x;
					if (dh >= getmaxy(stdscr) || dl >= getmaxx(stdscr))
				{
					curs_set(0);
				}
				else
				{
//					curs_set(1);
					move(dh, dl);
					refresh();
				}
#endif
					return;
			}
			case 0x03: { // get cursor position and shape
				const db page = host_text_page(bh);
				ch = host.vga.cursor_start;
				cl = host.vga.cursor_end;
				dh = host.vga.cursor_row[page];
				dl = host.vga.cursor_col[page];
				return;
			}
			case 0x05: { // select active display page
				host.vga.active_page = host_text_page(al);
				return;
			}
			case 0x06: { // scroll up / clear window
				host_text_scroll_up_window(host.vga.active_page, bh, ch, cl, dh, dl, al);
#ifndef NOCURSES
				if (al == 0) {
					clear();
					refresh();
				}
#endif
				return;
			}
			case 0x08: { // read character and attribute at cursor
				const db page = host_text_page(bh);
				const db row = host.vga.cursor_row[page];
				const db col = host.vga.cursor_col[page];
				const HostVga::TextCell &cell = host.vga.text[page][row][col];
				al = cell.ch;
				ah = cell.attr;
				return;
			}
			case 0x01: { // set cursor shape
				host.vga.cursor_start = ch;
				host.vga.cursor_end = cl;
				return;
			}
			case 0x09: { // write character and attribute at cursor
				const db page = host_text_page(bh);
				host_text_write(page, host.vga.cursor_row[page], host.vga.cursor_col[page], al, bl, cx);
#ifndef NOCURSES
				for (dw n = 0; n < cx; ++n) {
					addch(al);
				}
				refresh();
#endif
				return;
			}
			case 0x0b: { // set background/border color
				return;
			}
		case 0x11: {        //set charset size
			switch(al)
			{
			case 0x11: {
#ifndef NOCURSES
				resize_term(30, 80);
				refresh();
#endif
				return;
			}
			case 0x12: {
#ifndef NOCURSES
				resize_term(50, 80);
				refresh();
#endif
				return;
			}
			}
			break;
		}
		case 0x10: {
				switch (al) {
				case 0x03:
					// Toggle intensity/blink. Hosted text output does not model
					// attribute blinking.
					return;
				case 0x00: // set individual palette (attribute) register: BL=index, BH=value
					host.vga.attr_regs[bl & 0x1f] = bh;
					return;
				case 0x01: // set overscan (border) color register: BH=value
					host.vga.attr_regs[0x11] = bh;
					return;
				case 0x02: { // set all palette registers + overscan: ES:DX -> 17 bytes
					db *src = host_physical_address(es, dx);
					if (src) {
						std::copy(src, src + 17, host.vga.attr_regs);
					}
					return;
				}
				case 0x07: // read individual palette register: BL=index -> BH
					bh = host.vga.attr_regs[bl & 0x1f];
					return;
				case 0x08: // read overscan register -> BH
					bh = host.vga.attr_regs[0x11];
					return;
				case 0x09: { // read all palette registers + overscan: ES:DX -> 17 bytes
					db *dst = host_physical_address(es, dx);
					if (dst) {
						std::copy(host.vga.attr_regs, host.vga.attr_regs + 17, dst);
					}
					return;
				}
				case 0x10: { // set individual DAC color register: BX=reg, DH=red, CH=green, CL=blue
					if (bx < 256) {
						vgaPalette[bx * 3 + 0] = dh;
						vgaPalette[bx * 3 + 1] = ch;
						vgaPalette[bx * 3 + 2] = cl;
#if SDL_MAJOR_VERSION == 2 && !defined(NOSDL) && M2CDEBUG != -1
						vga_render_dirty = true;
#endif
					}
					return;
				}
				case 0x12: { // set block of DAC color registers: ES:DX -> RGB triples, BX=first, CX=count
					db *src = host_physical_address(es, dx);
					if (src) {
						for (dw i = 0; i < cx && (bx + i) < 256; ++i) {
							vgaPalette[(bx + i) * 3 + 0] = src[i * 3 + 0];
							vgaPalette[(bx + i) * 3 + 1] = src[i * 3 + 1];
							vgaPalette[(bx + i) * 3 + 2] = src[i * 3 + 2];
						}
#if SDL_MAJOR_VERSION == 2 && !defined(NOSDL) && M2CDEBUG != -1
						vga_render_dirty = true;
#endif
					}
					return;
				}
				case 0x15: { // read individual DAC color register: BX=reg -> DH=red, CH=green, CL=blue
					if (bx < 256) {
						dh = vgaPalette[bx * 3 + 0];
						ch = vgaPalette[bx * 3 + 1];
						cl = vgaPalette[bx * 3 + 2];
					}
					return;
				}
				case 0x17: { // read block of DAC color registers: ES:DX -> buffer, BX=first, CX=count
					db *dst = host_physical_address(es, dx);
					if (dst) {
						for (dw i = 0; i < cx && (bx + i) < 256; ++i) {
							dst[i * 3 + 0] = vgaPalette[(bx + i) * 3 + 0];
							dst[i * 3 + 1] = vgaPalette[(bx + i) * 3 + 1];
							dst[i * 3 + 2] = vgaPalette[(bx + i) * 3 + 2];
						}
					}
					return;
				}
				}
			break;
		}
		case 0x1a: {        //vga
			switch(al)
			{
			case 0: {
				bx=8;  //vga
				al=0x1a;
				return;
			}
			}
			break;
			}
			case 0xef: {
				// OEM BIOS extension. Hosted mode has no adapter-specific action to
				// perform, but the call must report success.
				AFFECT_CF(0);
				return;
			}
		}
		break;
	}
	case 0x1A:
	{
#ifdef __DJGPP__
		call_dos_realint(_state, a);
		return;
#else
		const time_t raw_time = time(nullptr);
		struct tm local_tm;
#if defined(_WIN32)
		localtime_s(&local_tm, &raw_time);
#else
		localtime_r(&raw_time, &local_tm);
#endif
		switch (ah) {
		case 0x00: {
			const uint32_t seconds = static_cast<uint32_t>(
				local_tm.tm_hour * 3600 + local_tm.tm_min * 60 + local_tm.tm_sec);
			const uint32_t ticks = static_cast<uint32_t>(seconds * 18.2065);
			cx = static_cast<dw>(ticks >> 16);
			dx = static_cast<dw>(ticks & 0xffff);
			al = 0;
			AFFECT_CF(0);
			return;
		}
		case 0x02:
			ch = host_to_bcd(local_tm.tm_hour);
			cl = host_to_bcd(local_tm.tm_min);
			dh = host_to_bcd(local_tm.tm_sec);
			dl = 0;
			AFFECT_CF(0);
			return;
		case 0x04: {
			const int year = local_tm.tm_year + 1900;
			ch = host_to_bcd(year / 100);
			cl = host_to_bcd(year % 100);
			dh = host_to_bcd(local_tm.tm_mon + 1);
			dl = host_to_bcd(local_tm.tm_mday);
			AFFECT_CF(0);
			return;
		}
		default:
			log_debug("Unsupported BIOS time INT 1Ah ah:0x%x al:0x%x\n", ah, al);
			AFFECT_CF(1);
			return;
		}
#endif
	}
	case 0x16:
	{
#ifdef __DJGPP__
		call_dos_realint(_state, a);
		return;
#else
		poll_host_events(_state);
		dw bios_key = 0;
		switch (ah) {
		case 0x00:
		case 0x10:
			if (host_keyboard_wait(_state, &bios_key)) {
				ax = bios_key;
				AFFECT_ZF(0);
			} else {
				ax = 0;
				AFFECT_ZF(1);
			}
			return;
		case 0x01:
		case 0x11:
			if (host_keyboard_peek(&bios_key)) {
				ax = bios_key;
				AFFECT_ZF(0);
			} else {
				ax = 0;
				AFFECT_ZF(1);
			}
			return;
		case 0x02:
			al = host_keyboard_shift_flags();
			return;
		case 0x05:
			al = host_keyboard_push(cx) ? 0 : 1;
			return;
		case 0x12:
			ax = host_keyboard_shift_flags();
			return;
		default:
			log_debug("Unsupported BIOS keyboard INT 16h ah:0x%x al:0x%x\n", ah, al);
			ax = 0;
			AFFECT_ZF(1);
			return;
		}
#endif
	}
	case 0x21:
		{
		static dd tnd_img_guard = 0;
		if (tnd_seg) {
			db* gp = (db*)host_physical_address(tnd_seg, 0);
			dd cur = *(dd*)gp;
			if (cur != tnd_img_guard)
				log_debug("imgchg ah=%02x %08x->%08x ds=%x dx=%x es=%x at %x:%x\n", ah, tnd_img_guard, cur, ds, dx, es, cs, eip);
			tnd_img_guard = cur;
		}
		if (ah == 0x48 || ah == 0x49 || ah == 0x4b || ah == 0x4c || ah == 0x09 || ah == 0x4a || ah == 0x3f)
			log_debug("int21 ah=%02x bx=%x dx=%x es=%x ds=%x at %x:%x\n", ah, bx, dx, es, ds, cs, eip);
		}
#ifdef __DJGPP__
		switch(ah)
		{
			case 0x9:
			case 0x19:
			case 0x1A:
			case 0x39:
			case 0x3A:
			case 0x3B:
			case 0x3C:
			case 0x3D:
			case 0x3E:
			case 0x3F:
			case 0x40:
			case 0x41:
			case 0x43:
			case 0x4e:
			case 0x4f:
//			case 0x47:
//			case 0x56:
			case 0x58:
			{
			call_dos_protint(_state, 0x21);
			return;
			}
			case 0x42:
			{
		        call_dos_realint(_state, a);
			}
			default:
				break;
		}
#endif
		switch(ah)
		{
		case 0x02: // Display character in DL
		{
#ifdef __DJGPP__
			call_dos_realint(_state, a);
#else
			std::putchar(dl);
			std::fflush(stdout);
			AFFECT_ZF(0);
#endif
			return;
		}
		case 0x06: // Direct console I/O
		{
#ifdef __DJGPP__
			call_dos_realint(_state, a);
#else
			if (dl == 0xff) {
				poll_host_events(_state);
				dw bios_key = 0;
				if (host_keyboard_pop(&bios_key)) {
					al = static_cast<db>(bios_key & 0xff);
					AFFECT_ZF(0);
				} else {
					al = 0;
					AFFECT_ZF(1);
				}
			} else {
				std::putchar(dl);
				std::fflush(stdout);
				al = dl;
				AFFECT_ZF(0);
			}
#endif
			return;
		}
		case 0x9:
		{
			char * s=(char *) realAddress(dx,ds);
			for (i=0; s[i]!='$'; i++) {
				printf("%c", s[i]);
			}
			return;
		}
		case 0xe: // select disk
		{
#ifdef __DJGPP__
//        call_dos_realint(_state, a);
     unsigned int _drives;
     _dos_setdrive(dl+1, &_drives);
     al = _drives;
#else
			al=1;
#endif
			return;
		}
		case 0x11: // search fcb
		case 0x12: // search fcb
		{
			al=0xff;
			return;
		}
		case 0x19: // Get default disk
		{
#ifdef __DJGPP__
        call_dos_realint(_state, a);
#else
			// def disk is C:
			al=0x2;
#endif
			return;
		}
		case 0x1A: // Set disk transfer addr
		{
			diskTransferAddr=(find_t *)realAddress(dx,ds);
			dta_seg = ds;
			dta_off = dx;
			return;
		}
		case 0x2F: // Get disk transfer addr -> ES:BX
		{
			es = dta_seg ? dta_seg : host.current_psp;
			bx = dta_off;
			return;
		}
			case 0x25: // Set disk transfer addr
			{
				*(dw *)realAddress(al*4,0)=dx;
				*(dw *)realAddress(al*4+2,0)=ds;
			if (al == 0x08) {
				host.timer.enabled = true;
				host.timer.last_us = host_now_us();
				host.timer.accum_us = 0;
				host.timer.divider_20hz = 0;
				host_start_timer_thread();
				}
				return;
			}
				case 0x26:
					/* DOS "create PSP": copy the current program segment prefix
					 * into the segment supplied in DX. */
					{
						const void* psp = host_physical_address(host.current_psp, 0);
						if (m2c::copy_linked_program_segment_prefix) {
							m2c::copy_linked_program_segment_prefix(dx, psp, 0x100);
						} else {
							std::memmove(host_physical_address(dx, 0), psp, 0x100);
						}
					}
				AFFECT_CF(0);
				return;
			case 0x30: // ver
			{
				ax=5;
                        bx=0xff00;
                        cx=0;
			return;
		}
		case 0x35: // Set disk transfer addr
		{
			if (al == 0x33) {
				bx = 0x33 * 4;
				es = 0;
			} else {
				bx=*(dw *)realAddress(al*4,0);
				es=*(dw *)realAddress(al*4+2,0);
			}
			return;
		}
		case 0x2a:
		{
#ifdef __DJGPP__
        call_dos_realint(_state, a);
			return;
#else
			const time_t raw_time = time(nullptr);
			struct tm local_tm;
#if defined(_WIN32)
			localtime_s(&local_tm, &raw_time);
#else
			localtime_r(&raw_time, &local_tm);
#endif
			cx = static_cast<dw>(local_tm.tm_year + 1900);
			dh = static_cast<db>(local_tm.tm_mon + 1);
			dl = static_cast<db>(local_tm.tm_mday);
			al = static_cast<db>(local_tm.tm_wday);
			return;
#endif
		}
		case 0x2b:
			al = (cx >= 1980 && cx <= 2099 && dh >= 1 && dh <= 12 && dl >= 1 && dl <= 31) ? 0 : 0xff;
			return;
		case 0x2d:
			al = (ch <= 23 && cl <= 59 && dh <= 59 && dl <= 99) ? 0 : 0xff;
			return;
		case 0x2c:
		{
#ifdef __DJGPP__
        call_dos_realint(_state, a);
			return;
#else
			const time_t raw_time = time(nullptr);
			struct tm local_tm;
#if defined(_WIN32)
			localtime_s(&local_tm, &raw_time);
#else
			localtime_r(&raw_time, &local_tm);
#endif
			ch = static_cast<db>(local_tm.tm_hour);
			cl = static_cast<db>(local_tm.tm_min);
			dh = static_cast<db>(local_tm.tm_sec);
			dl = 0;
			return;
#endif
		}
		case 0x3c: // create file (CX = attr)
		case 0x5a: // create temp file (DS:DX = dir path ending with '\')
		case 0x5b: // create new file (fail if exists)
		{
			char fileName[1000];
			if (ah == 0x5a) {
				// Build a name inside the given directory.
				char dir[1000];
				std::snprintf(dir, sizeof(dir), "%s", (const char *)realAddress(dx, ds));
				std::snprintf(fileName, sizeof(fileName), "%stl%04x.tmp", dir, (unsigned)(getpid() & 0xffff));
			} else {
				std::snprintf(fileName, sizeof(fileName), "%s", (const char *)realAddress(dx, ds));
			}
			if (fileName[0] == '\0') {
				ax = 3; // path not found
				AFFECT_CF(1);
				break;
			}
			if (ah == 0x5b && access(fileName, F_OK) == 0) {
				ax = 0x50; // file exists
				AFFECT_CF(1);
				break;
			}
			FILE * f = fopen(fileName, "w+b");
			log_debug2("dos create %s -> %p\n", fileName, (void *)f);
			if (!f) {
				ax = (access(fileName, F_OK) == 0 || ah == 0x5a) ? 5 : 3;
				AFFECT_CF(1);
				break;
			}
			dw h = dos_alloc_handle(f);
			if (h == 0xffff) { ax = 4; AFFECT_CF(1); break; }
			log_debug2("dos create %s -> handle %d\n", fileName, h);
			ax = h;
			AFFECT_CF(0);
			return;
		}
		case 0x3d: //open
		{
				char fileName[1000];
					snprintf(fileName,sizeof(fileName),"%s",(const char *) realAddress(dx, ds));
				if (fileName[0] == '\0') {
					ax = 2;
					AFFECT_CF(1);
					return;
				}
				const char * mode = "rb";
				switch (al & 7) {
				case 0: mode = "rb"; break;
				case 1: mode = "r+b"; break;
				case 2: mode = "r+b"; break;
				default: mode = "rb"; break;
				}
				FILE * f = fopen(fileName, mode);
				if (!f) {
					char resolved[1000];
					if (dos_resolve_case(fileName, resolved, sizeof(resolved)))
						f = fopen(resolved, mode);
				}
				log_debug2("Opening file %s -> %p\n",fileName,(void *) f);
				if (m2c_stats_enabled()) {
					std::fprintf(stderr, "dos open %s -> %p\n", fileName, static_cast<void *>(f));
				}
				if (f!=NULL) {
					dw h = dos_alloc_handle(f);
					if (h == 0xffff) { ax=4; AFFECT_CF(1); return; }
					eax=h;
					AFFECT_CF(0);
				} else {
					AFFECT_CF(1);
					ax = (errno == ENOENT) ? 2 : 5;
					std::fprintf(stderr, "Error opening file %s\n", fileName);
				}
			/*
			   // [Index]AH = 3Dh - "OPEN" - OPEN EXISTING FILE
			   Entry:

			   AL = access and sharing modes
			   DS:DX -> ASCIZ filename
			   Return:

			   CF clear if successful, AX = file handle
			    CF set on error AX = error code (01h,02h,03h,04h,05h,0Ch,56h)
			 */
			// TODO
			return;
		}
		case 0x3e: //close
		{
			log_debug2("Closing file. bx:%d\n",bx);
			FILE * f = dos_get_file(bx);
			if (!f && file && bx == 1) f = file;   // legacy single-handle compat
			if (!f) {
				// Closing a handle that was never opened is accepted
				// silently by the reference environment; keep it a no-op
				// so exit-time handle sweeps stay idempotent instead of
				// cascading into the fatal-error reporter.
				AFFECT_CF(0);
				return;
			}
			if (bx >= DOS_HANDLE_BASE && f != file) dos_files[bx - DOS_HANDLE_BASE] = nullptr;
			if (fclose(f)) {
				ax = 6;
				AFFECT_CF(1);
				log_error("Error closing file ? bx:%d\n",bx);
				return;
			}
			if (bx < DOS_HANDLE_BASE) dos_std[bx] = nullptr;
			if (f == file) file = NULL;
			AFFECT_CF(0);
			return;
		}
		case 0x41: // delete file (DS:DX -> ASCIZ name)
		{
			char fileName[1000];
			std::snprintf(fileName, sizeof(fileName), "%s", (const char *)realAddress(dx, ds));
			char resolved[1000];
			const char* target = dos_resolve_case(fileName, resolved, sizeof(resolved)) ? resolved : fileName;
			if (unlink(target) == 0) {
				AFFECT_CF(0);
			} else {
				ax = 2; // file not found
				AFFECT_CF(1);
			}
			return;
		}
		case 0x40: // write to file/device
		{
			// BX = handle, CX = count, DS:DX -> buffer
			void * buffer = (db *)realAddress(dx, ds);
			FILE * f = dos_get_file(bx);
			if (bx <= 4) {
				// std device: write to host stdout/stderr
				size_t w = fwrite(buffer, 1, cx, bx <= 2 ? stdout : stderr);
				ax = (dw)w;
				AFFECT_CF(0);
				return;
			}
			if (!f) {
				ax = 6;
				AFFECT_CF(1);
				return;
			}
			size_t w = fwrite(buffer, 1, cx, f);
			log_debug2("dos write handle=%d count=%d -> %zu\n", bx, cx, w);
			if (w != cx && ferror(f)) {
				ax = 5;
				AFFECT_CF(1);
				return;
			}
			ax = (dw)w;
			AFFECT_CF(0);
			return;
		}
		case 0x44: // ioctl (subset: get info)
		{
			// AL=0 get device info word; AL=8 check removable; others: fail
			if (al == 0) {
				dx = (bx <= 4) ? 0x80d3 : 0x0000; // isdev bit for std handles
				AFFECT_CF(0);
			} else if (al == 8) {
				ax = 1; // not removable
				AFFECT_CF(0);
			} else {
				ax = 1;
				AFFECT_CF(1);
			}
			return;
		}
		case 0x45: // dup handle
		{
			FILE * f = dos_get_file(bx);
			if (!f) { ax = 6; AFFECT_CF(1); return; }
			// Underlying OS dup so both handles share the file offset.
			// Mode must match the fd access mode or fdopen fails EINVAL.
			int dfd = dup(fileno(f));
			if (dfd < 0) { ax = 4; AFFECT_CF(1); return; }
			int acc = fcntl(dfd, F_GETFL) & O_ACCMODE;
			const char * dmode = acc == O_RDONLY ? "rb" : acc == O_WRONLY ? "ab" : "r+b";
			FILE * nf = fdopen(dfd, dmode);
			if (!nf) { close(dfd); ax = 4; AFFECT_CF(1); return; }
			dw h = dos_alloc_handle(nf);
			if (h == 0xffff) { ax = 4; AFFECT_CF(1); return; }
			ax = h;
			AFFECT_CF(0);
			return;
		}
		case 0x46: // force duplicate handle
		{
			FILE * f = dos_get_file(bx);
			if (!f) { ax = 6; AFFECT_CF(1); return; }
			if (cx >= DOS_HANDLE_BASE && cx - DOS_HANDLE_BASE < 0x40) {
				if (dos_files[cx - DOS_HANDLE_BASE])
					fclose(dos_files[cx - DOS_HANDLE_BASE]);
				dos_files[cx - DOS_HANDLE_BASE] = fdopen(dup(fileno(f)), "r+b");
				if (!dos_files[cx - DOS_HANDLE_BASE]) { ax = 4; AFFECT_CF(1); return; }
			}
			AFFECT_CF(0);
			return;
		}
		case 0x4d: // get child return code
		{
			ax = (dw)(dos_last_child_rc & 0xffff);
			ah = 0;   // terminated normally
			AFFECT_CF(0);
			return;
		}
		case 0x56: // rename file
		{
			char oldn[1000], newn[1000];
			std::snprintf(oldn, sizeof(oldn), "%s", (const char *)realAddress(dx, ds));
			std::snprintf(newn, sizeof(newn), "%s", (const char *)realAddress(di, es));
			if (rename(oldn, newn) == 0) { AFFECT_CF(0); }
			else { ax = (errno == ENOENT) ? 2 : 5; AFFECT_CF(1); }
			return;
		}
		case 0x57: // get/set file date+time (stub: get returns zeros)
		{
			if (!dos_get_file(bx)) { ax = 6; AFFECT_CF(1); return; }
			if (al == 0) { cx = dx = 0; AFFECT_CF(0); }
			else { AFFECT_CF(0); }
			return;
		}
		case 0x67: // set handle count
		case 0x68: // commit file
		{
			FILE * f = dos_get_file(bx);
			if (ah == 0x68 && !f) { ax = 6; AFFECT_CF(1); return; }
			if (ah == 0x68) fflush(f);
			AFFECT_CF(0);
			return;
		}
		case 0x3f: // read
		{
			/*
			   [Index]AH = 3Fh - "READ" - READ FROM FILE OR DEVICE

			   Entry:

			   BX = file handle
			   CX = number of bytes to read
			   DS:DX -> buffer for data
			   Return:

			   CF clear if successful - AX = number of bytes actually read (0 if at EOF before call)
			    CF set on error AX = error code (05h,06h)
			 */
			//char grosbuff[100000];
			void * buffer=(db *) realAddress(dx, ds);
			// log_debug2("Reading ecx=%d cx=%d eds=%x edx=%x -> %p file: %p\n",m.ecx,cx,m.ds,m.edx,buffer,(void *)  file);
			FILE * rf = dos_get_file(bx);
			if (!rf && file) rf = file;   // legacy single-handle compat

			if (!rf) {
				log_debug2("dos read: no open file (bx=%04x)\n", bx);
				eax = 6; // invalid handle
				AFFECT_CF(1);
			} else if (bx >= DOS_HANDLE_BASE && feof(rf)) {
				log_debug2("feof(handle %d)\n", bx);
				eax=0;
				AFFECT_CF(0);
			} else {
				size_t r=fread (buffer,1,cx,rf);
				if (r!=cx) {
					// short read is EOF (not an OS error) - only report real errors
					if(!feof(rf)) {
						log_error("Error reading ? %d %zu %p\n",cx,r,(void *) rf);
						AFFECT_CF(1);
					}
				} else {
					log_debug2("Reading OK %p\n",(void *) rf);
				}
				eax=r;
				AFFECT_CF(0);
				if (m2c_stats_enabled()) {
					std::fprintf(
						stderr,
						"dos read handle=%04x count=%u -> %u buffer=%p\n",
						bx,
						static_cast<unsigned>(cx),
						static_cast<unsigned>(eax),
						buffer
					);
				}
			}
			/*
			   if (ax!=cx) {
			    log_debug("Error reading ? %d %d\n",ax,cx);
			    m.AFFECT_CF(1);

			   }
			 */
			return;
		}
		// [Index]AH=42h - "LSEEK" - SET CURRENT FILE POSITION
		case 0x42:
		{
			/*

			   AH=42h - "LSEEK" - SET CURRENT FILE POSITION

			   Entry:

			   AL = origin of move 00h start of file 01h current file position 02h end of file
			   BX = file handle
			   CX:DX = offset from origin of new file position

			 */
			int seek = 0;
			switch(al) {
			case 0x0:
				seek = SEEK_SET;
				break;
			case 0x1:
				seek = SEEK_CUR;
				break;
			case 0x2:
				seek = SEEK_END;
				break;
			}
			long int offset=(((long int )cx)<<16)+dx;
			log_debug2("Seeking to offset %ld %d\n",offset,seek);
			FILE * sf = dos_get_file(bx);
			if (!sf && file) sf = file;
			if (!sf) {
				log_debug2("dos seek: no open file (bx=%04x)\n", bx);
				eax = 6;
				AFFECT_CF(1);
			} else if (fseek(sf,offset,seek)!=0) {
				log_error("Error seeking\n");
				eax = 6;
				AFFECT_CF(1);
			} else {
				const long pos = ftell(sf);
				dx = (dw)((pos >> 16) & 0xffff);
				ax = (dw)(pos & 0xffff);
				AFFECT_CF(0);
			}
			return;
		}
		case 0x47: // Get cur dir
		{
			// cur dir is root
			*(char *) realAddress(dx, ds)='\0';
			ax = 0x0100;
			return;
		}
		case 0x48:
		{

			//   ;2.29 - Function 048h - Allocate Memory Block:
			//   ;In:  AH     = 48h
			//   ;  BX  = size of block in 16xbytes (must be non-zero)
			//   ;Out: if successful:
			//   ;    carry flag clear
			//   ;    AX  =  address of allocated memory block
/*
			if (bx==0xffff)
				{ AFFECT_CF(1);
				  return;
				}

			int32_t nbBlocks=(bx<<4);
			log_debug2("Function 0501h - Allocate Memory Block: %d para\n",bx);

			if (heapPointer+nbBlocks>=HEAP_SIZE) {
				AFFECT_CF(1);
				log_error("Not enough memory (increase HEAP_SIZE)\n");
				exit(1);
				return;
			} else {
				dd a=offsetof(struct Memory,heap)+heapPointer;
				heapPointer+=nbBlocks;
				{
					log_debug2("New top of heap: %x\n",(dd) offsetof(struct Memory,heap)+heapPointer);
				}
				ax=a >> 4;
				log_debug2("Return pointer %x, seg ax =%x\n",a,ax);
				return;
			}
*/
      /* Allocate memory */
      if ((rc = DosMemAlloc(bx, mem_access_mode, &ax, &bx)) < 0)
      {
        DosMemLargest(&bx);
        if (DosMemCheck() != SUCCESS)
           {log_error("MCB chain corrupted\n");exit(1);}
           AFFECT_CF(1);
           return;
      }
	AFFECT_CF(rc!=SUCCESS);
      ax++;   /* DosMemAlloc() returns seg of MCB rather than data */
	return;
			break;
		}
      /* Free memory */
	    case 0x49:
      if ((rc = DosMemFree(es - 1)) < SUCCESS)
      {
        if (DosMemCheck() != SUCCESS)
           {log_error("MCB chain corrupted\n");exit(1);}
           AFFECT_CF(1);
      }
	AFFECT_CF(rc!=SUCCESS);
	return;
      break;

	      /* Set memory block size */
			    case 0x4a:
#ifndef __DJGPP__
	      /* Hosted builds do not own the DOS PSP MCB chain. Treat resize as
	       * successful so startup code can release conventional memory. */
	      ax = es;
		AFFECT_CF(0);
		return;
#else
	        if (DosMemCheck() != SUCCESS)
	           {log_error("before 4a: MCB chain corrupted\n");exit(1);}

	      if ((rc = DosMemChange(es, bx, &bx)) < 0)
	      {
        if (DosMemCheck() != SUCCESS)
           {log_error("after 4a: MCB chain corrupted\n");exit(1);}
#ifndef __DJGPP__
        log_debug2("Ignoring hosted DOS resize failure es:%x bx:%x rc:%d\n", es, bx, rc);
        rc = SUCCESS;
#else
        AFFECT_CF(1);
#endif
	      }
	      ax = es; /* Undocumented MS-DOS behaviour expected by BRUN45! */
		AFFECT_CF(rc!=SUCCESS);
		return;
#endif
		      break;
			case 0x51:
				bx = host.current_psp;
				AFFECT_CF(0);
				return;
			case 0x4E: // find first matching file
			{
				// cur dir is root
				const char *fileName = reinterpret_cast<const char *>(realAddress(dx, ds));
				log_debug2("Find first file %s\n", fileName);
				if (fileName[0] == '\0') {
					log_error("Find first with empty filename ds=%04x dx=%04x\n", ds, dx);
					stackDump(_state);
				}
	#ifdef __DJGPP__
     AFFECT_CF(_dos_findfirst((const char *) raddr(ds, dx), cx,
                                 diskTransferAddr));
#else
			FILE *found = fopen(fileName, "rb");
			if (found == nullptr) {
				ax = 2;  // file not found
				AFFECT_CF(1);
				return;
			}
			fclose(found);
			if (diskTransferAddr == nullptr) {
				diskTransferAddr = reinterpret_cast<find_t *>(defaultDiskTransferArea);
			}
			std::snprintf(reinterpret_cast<char *>(diskTransferAddr) + 0x1e, 13, "%s", fileName);
			ax = 0;
			AFFECT_CF(0);
#endif
			return;
		}
		case 0x4F: // find next matching file
		{
			// cur dir is root
			log_debug2("Find next file %s\n",(void *) (db *) realAddress(dx, ds));
#ifdef __DJGPP__
     AFFECT_CF(_dos_findnext(diskTransferAddr));
#else
			AFFECT_CF(1);
#endif
			return;
		}
		case 0x4b: // EXEC - load overlay (AL=03h); code runs via dispatch_external_code
		{
			if (al != 0x03) {
				AFFECT_CF(1);
				ax = 1;
				return;
			}
			const dw loadseg = *(dw*)realAddress(bx, es);
			const dw relocfactor = *(dw*)realAddress(bx + 2, es);
			const char* fname = (const char*)realAddress(dx, ds);
			FILE* ovf = fopen(fname, "rb");
			if (!ovf) {
				AFFECT_CF(1);
				ax = 2;
				return;
			}
			// Detect the translated TANDYSND overlay before loading so the image
			// write and relocations route into tnd_img instead of m's heap.
			bool is_tnd = false;
			{
				char nm[96]; size_t i = 0;
				for (; fname[i] && i < sizeof(nm) - 1; ++i) nm[i] = toupper((db)fname[i]);
				nm[i] = 0;
				is_tnd = strstr(nm, "TANDY") != nullptr;
				if (is_tnd) {
					tnd_seg = loadseg;
					tnd_code_seg = (dw)(loadseg + 7);
				}
			}
			db hdr[0x20];
			bool bad = fread(hdr, 1, 0x20, ovf) != 0x20 || hdr[0] != 'M' || (hdr[1] != 'Z' && hdr[1] != 'M');
			dw hsize = 0, nreloc = 0; dw reloff = 0;
			if (!bad) {
				hsize = (*(dw*)(hdr + 8)) * 16;
				nreloc = *(dw*)(hdr + 6);
				reloff = *(dw*)(hdr + 0x18);
			}
			fseek(ovf, 0, SEEK_END);
			const long fsz = ftell(ovf);
			if (is_tnd) {
				tnd_img_paras = (dw)((fsz - hsize + 15) / 16 + 2);
				if (tnd_img_paras * 16 > sizeof(tnd_img)) { bad = true; }
			}
			if (!bad && hsize < fsz) {
				fseek(ovf, hsize, SEEK_SET);
				db* base = (db*)host_physical_address(loadseg, 0);
				bad = fread(base, 1, fsz - hsize, ovf) != (size_t)(fsz - hsize);
				for (dw i = 0; !bad && i < nreloc; ++i) {
					db rent[4];
					fseek(ovf, reloff + i * 4, SEEK_SET);
					if (fread(rent, 1, 4, ovf) != 4) { bad = true; break; }
					const dw roff = *(dw*)rent;
					const dw rseg = *(dw*)(rent + 2);
					dw* w = (dw*)host_physical_address(loadseg + rseg, roff);
					*w += relocfactor;
				}
			}
			fclose(ovf);
			if (bad) {
				AFFECT_CF(1);
				ax = 8;
				return;
			}
			host.overlay_segs.push_back({loadseg, (dw)(loadseg + (fsz - hsize + 15) / 16 + 8)});
			if (is_tnd) {
				log_error("TANDYSND bound: image %x code %x paras %x\n", tnd_seg, tnd_code_seg, tnd_img_paras);
			}
			log_error("EXEC overlay %s loaded at %x fsz=%ld hsize=%x nreloc=%d img=%02x%02x%02x%02x base=%p\n",
				fname, loadseg, fsz, (unsigned)hsize, (int)nreloc,
				((db*)host_physical_address(loadseg,0))[0], ((db*)host_physical_address(loadseg,0))[1],
				((db*)host_physical_address(loadseg,0))[2], ((db*)host_physical_address(loadseg,0))[3],
				(void*)host_physical_address(loadseg,0));
			AFFECT_CF(0);
			return;
		}
		case 0x4c:
		{
			jumpToBackGround = 1;
			executionFinished = 1;
			exitCode = al;
			// Runtime status, not guest output — stderr keeps it in test
			// logs while guest stdout stays clean for golden comparisons.
			std::fprintf(stderr, "Graceful exit al=%d\n", al);
			exit(al);
			return;
		}
		case 0x58: // mem allocation policy
		{
#ifdef __DJGPP__
        call_dos_realint(_state, a);
			return;
#endif
			return;
		}
		default:
			break;
		}
		return;
	case 0x31:
		switch(ax)
		{
		case 0x0:
		{
			
			//   ;2.0 - Function 0000h - Allocate Descriptors:
			//   ;--------------------------------------------
			//   ;  Allocates one or more descriptors in the client's descriptor table. The
			//   ;descriptor(s) allocated must be initialized by the application with other
			//   ;function calls.
			//   ;In:
			//   ;  AX     = 0000h
			//   ;  CX     = number of descriptors to allocate
			//   ;Out:
			//   ;  if successful:
			//   ;    carry flag clear
			//   ;    AX     = base selector
			 
			log_debug2("Function 0000h - Allocate %d Descriptors\n",cx);
			dw base_sel = m2c_ldt_alloc(cx);
			if (!base_sel) {
				AFFECT_CF(1);
				log_error("Not enough free LDT descriptors\n");
				return;
			}
			ax = base_sel;
			AFFECT_CF(0);
			log_debug2("Return base selector %x\n", ax);
			return;
		}
		case 0x02:
		{

			//   This function Converts a real mode segment into a protected mode descriptor.
			//   BX =    real mode segment
			//   Out:
			//   if successful:
			//   carry flag clear
			//   AX =  selector
			//  if failed:
			//   carry flag set

			log_debug2("Function 0002h - real segment %x -> selector\n", bx);
			// Per spec, repeated conversions of the same real-mode segment
			// return the same selector.
			for (int i = 0; i < NB_LDT; ++i) {
				const PmDesc& d = m2c_ldt[i];
				if (d.used && !d.owned && d.lin == ((dd)bx << 4)) {
					ax = (dw)((i << 3) | 7);
					AFFECT_CF(0);
					return;
				}
			}
			{
				dw sel = m2c_ldt_alloc(1);
				if (!sel) { AFFECT_CF(1); return; }
				PmDesc& d = m2c_ldt[m2c_ldt_idx(sel)];
				d.base = (db*)&m + ((dd)bx << 4);
				d.lin = (dd)bx << 4;
				ax = sel;
				AFFECT_CF(0);
				log_debug2("Returns new selector: %x\n", ax);
			}
			return;
		}
		case 0x01: // Free descriptor(s): BX = base selector
		{
			if (!m2c_ldt[m2c_ldt_idx(bx)].used) {
				AFFECT_CF(1);
				log_error("Function 0001h - bad selector %x\n", bx);
				return;
			}
			m2c_ldt_free(bx);
			AFFECT_CF(0);
			return;
		}
		case 0x06: // Get Segment Base Address: BX = sel -> CX:DX linear base
		{
			if (!m2c_ldt[m2c_ldt_idx(bx)].used) {
				AFFECT_CF(1);
				log_error("Function 0006h - bad selector %x\n", bx);
				return;
			}
			dd base = m2c_ldt_get_lin(bx);
			cx = (dw)(base >> 16);
			dx = (dw)(base & 0xffff);
			AFFECT_CF(0);
			return;
		}
		//   ;2.5 - Function 0007h - Set Segment Base Address:
		//   ; Sets the 32bit linear base address field in the descriptor for the specified
		//   ; segment.
		//   ; In:   AX     = 0007h
		//   ; BX     = selector
		//   ;  CX:DX  = 32bit linear base address of segment

		case 0x07:
		{
			dd lin = (dw)dx + ((dd)cx << 16);
			log_debug2("Function 0007h - Set Segment Base: sel=%x lin=%x\n", bx, lin);
			PmDesc& d = m2c_ldt[m2c_ldt_idx(bx)];
			if (!d.used) {
				AFFECT_CF(1);
				log_error("Error: selector number doesnt exist\n");
				return;
			}
			d.lin = lin;
			if (lin < m2c_m_extent()) {
				d.base = (db*)&m + lin;
			} else {
				// Synthetic linear of an owned region (0501 result):
				// alias into the recorded host block (mid-block bases OK).
				for (int i = 0; i < NB_LDT; ++i) {
					if (m2c_ldt[i].owned && m2c_ldt[i].extent &&
					    lin >= m2c_ldt[i].lin &&
					    lin < m2c_ldt[i].lin + m2c_ldt[i].extent) {
						d.base = m2c_ldt[i].base + (lin - m2c_ldt[i].lin);
						break;
					}
				}
				if (!d.base && !d.owned) {
					log_error("Function 0007h - linear %x not mapped\n", lin);
				}
			}
			AFFECT_CF(0);
			return;
		}
		case 0x08:
		{

			//   ;2.6 - Function 0008h - Set Segment Limit:
			//   ;-----------------------------------------
			//   ;  Sets the limit field in the descriptor for the specified segment.
			//   ;  In:
			//   ;  AX     = 0008h
			//   ;  BX     = selector
			//   ;  CX:DX  = 32bit segment limit
			//   ;  Out:
			//   ;  if successful:
			//   ;    carry flag clear
			//   ;  if failed:
			//   ;    carry flag set


			// Record the limit; backing is always >=64KB so emulation
			// resolution is unaffected, but clients may read it back.
			{
				PmDesc& d = m2c_ldt[m2c_ldt_idx(bx)];
				if (!d.used) { AFFECT_CF(1); return; }
				d.limit = (dw)dx + ((dd)cx << 16);
				log_debug2("Function 0008h - Set Limit sel=%x -> %x\n", bx, d.limit);
				AFFECT_CF(0);
			}
			return;
		}
		case 0x09: // Set Descriptor Access Rights: BX=sel, CL=rights
		{
			PmDesc& d = m2c_ldt[m2c_ldt_idx(bx)];
			if (!d.used) { AFFECT_CF(1); return; }
			d.rights = cx;
			AFFECT_CF(0);
			return;
		}
		case 0x501:
		{

			//   ;2.29 - Function 0501h - Allocate Memory Block:
			//   ;In:  AX     = 0501h
			//   ;  BX:CX  = size of block in bytes (must be non-zero)
			//   ;Out: if successful:
			//   ;    carry flag clear
			//   ;    BX:CX  = linear address of allocated memory block
			//   ;    SI:DI  = memory block handle (used to resize and free block)

			dd size = ((dd)bx << 16) + cx;
			log_debug2("Function 0501h - Allocate Memory Block: %u bytes\n", size);

			// One descriptor per 64KB, one contiguous host block; the handle
			// returned is the base selector, so sel+8/__AHINCR steps across
			// the block exactly like real LDT descriptors.
			int n = (int)((size + 0xffff) >> 16);
			dw sel = m2c_ldt_alloc(n);
			if (!sel) { AFFECT_CF(1); return; }
			dd bytes = (dd)n << 16;
			db* blk = static_cast<db*>(calloc(1, bytes));
			if (!blk) { AFFECT_CF(1); return; }
			for (int i = 0; i < n; ++i) {
				PmDesc& d = m2c_ldt[m2c_ldt_idx(sel) + i];
				d.base = blk + ((dd)i << 16);
				d.lin = m2c_pm_next_linear + ((dd)i << 16);
				d.limit = 0xffff;
				d.owned = (i == 0);
				d.extent = (i == 0) ? bytes : 0;
			}
			m2c_pm_next_linear += bytes;
			cx = (dw)(m2c_ldt[m2c_ldt_idx(sel)].lin & 0xffff);
			bx = (dw)(m2c_ldt[m2c_ldt_idx(sel)].lin >> 16);
			di = sel;
			si = 0;
			AFFECT_CF(0);
			log_debug2("Return lin %x:%x handle %x\n", bx, cx, di);
			return;
		}
		case 0x502: // Free Memory Block: SI:DI = handle (base selector)
		{
			dw sel = (dw)((si << 16) | di);
			if (!m2c_ldt[m2c_ldt_idx(sel)].used) { AFFECT_CF(1); return; }
			m2c_ldt_free(sel);
			AFFECT_CF(0);
			return;
		}
		case 0x200: // get real-mode interrupt vector -> CX:DX
		{
			cx = *(dw *)realAddress(bl * 4 + 2, 0);
			dx = *(dw *)realAddress(bl * 4, 0);
			AFFECT_CF(0);
			return;
		}
		case 0x201: // set real-mode interrupt vector = CX:DX
		{
			*(dw *)realAddress(bl * 4, 0) = dx;
			*(dw *)realAddress(bl * 4 + 2, 0) = cx;
			AFFECT_CF(0);
			return;
		}
		case 0x202: // get processor exception handler -> CX:EDX
		case 0x204: // get PM interrupt vector -> CX:EDX
		{
			if (pm_vec_set[bl]) {
				cx = pm_vec_sel[bl];
				edx = pm_vec_off[bl];
			} else {
				// Report the real-mode IVT entry as an opaque far pointer.
				cx = *(dw *)realAddress(bl * 4 + 2, 0);
				edx = *(dw *)realAddress(bl * 4, 0);
			}
			AFFECT_CF(0);
			return;
		}
		case 0x203: // set processor exception handler = CX:EDX
		case 0x205: // set PM interrupt vector = CX:EDX
		{
			pm_vec_sel[bl] = cx;
			pm_vec_off[bl] = edx;
			pm_vec_set[bl] = 1;
			// When the handler's selector aliases `m` (generated code always
			// does — code descriptors over image segments), mirror the real
			// paragraph into the IVT so real-mode INT dispatch reaches it.
			const PmDesc& d = m2c_ldt[m2c_ldt_idx(cx)];
			if (d.used && d.base >= (db*)&m &&
			    d.base < (db*)&m + m2c_m_extent()) {
				*(dw *)realAddress(bl * 4, 0) = (dw)(edx & 0xffff);
				*(dw *)realAddress(bl * 4 + 2, 0) = (dw)(m2c_ldt_get_lin(cx) >> 4);
			}
			AFFECT_CF(0);
			return;
		}
		default:
			break;
		}
		break;
	case 0x33:
	{
#ifdef __DJGPP__
        call_dos_realint(_state, a);
			return;
#endif
			poll_host_events(_state);
		switch (ax) {
		case 0x0000:
			host.mouse.installed = true;
			host.mouse.visible = false;
			host.mouse.buttons = 0;
			host.mouse.motion_x = 0;
			host.mouse.motion_y = 0;
			clamp_host_mouse();
			ax = 0xffff;
			bx = 2;
			return;
		case 0x0001:
			host.mouse.visible = true;
			return;
		case 0x0002:
			host.mouse.visible = false;
			return;
		case 0x0003:
			bx = host.mouse.buttons;
			cx = host.mouse.x;
			dx = host.mouse.y;
			return;
		case 0x0004:
			host.mouse.last_x = host.mouse.x;
			host.mouse.last_y = host.mouse.y;
			host.mouse.x = cx;
			host.mouse.y = dx;
			clamp_host_mouse();
			host.mouse.motion_x += host.mouse.x - host.mouse.last_x;
			host.mouse.motion_y += host.mouse.y - host.mouse.last_y;
			return;
		case 0x0005:
		case 0x0006:
			ax = host.mouse.buttons;
			bx = 0;
			cx = host.mouse.x;
			dx = host.mouse.y;
			return;
		case 0x0007:
			host.mouse.min_x = std::min<int>(cx, dx);
			host.mouse.max_x = std::max<int>(cx, dx);
			clamp_host_mouse();
			return;
		case 0x0008:
			host.mouse.min_y = std::min<int>(cx, dx);
			host.mouse.max_y = std::max<int>(cx, dx);
			clamp_host_mouse();
			return;
		case 0x0010:
		case 0x1000:
			// Define mouse hidden region. The host runtime does not draw a hardware cursor.
			return;
		case 0x000b:
			cx = static_cast<dw>(host.mouse.motion_x);
			dx = static_cast<dw>(host.mouse.motion_y);
			host.mouse.motion_x = 0;
			host.mouse.motion_y = 0;
			return;
		default:
			log_debug("Unsupported mouse INT 33h ax:0x%x bx:0x%x cx:0x%x dx:0x%x\n", ax, bx, cx, dx);
			ax = 0;
			bx = 0;
			return;
		}
	}
	default:
#ifdef __DJGPP__
        call_dos_realint(_state, a);
			return;
#endif
		break;
	}
	AFFECT_CF(1);
	log_error("Error DOSInt 0x%x ah:0x%x al:0x%x: bx:0x%x not supported.\n",a,ah,al,bx);
}

//jmp_buf jmpbuffer;

/*
void program() {
int i;
#ifdef INCLUDEMAIN
dest=NULL;src=NULL;i=0; //to avoid a warning.
#endif
if (executionFinished) goto moveToBackGround;
if (jumpToBackGround) {
jumpToBackGround = 0;
#ifdef MRBOOM
if (nosetjmp) stackPointer=0; // this an an hack to avoid setJmp in saved state.
if (nosetjmp==2) goto directjeu;
if (nosetjmp==1) goto directmenu;
#endif
RET;
			}
//R(JMP(_main));
//...
executionFinished = 1;
moveToBackGround:
return ;//(executionFinished == 0);
}
*/

const char* log_spaces(int n)
{
 static const char s[]="                                                                                          ";
//	memset(s, ' ', n); 
//	*(s+n) = 0; 
  return s+(88-n);
}

dw getscan()
{
 dw o=0;
#ifndef NOCURSES
 int chr = getch();
 o = chr;
 //if (ch==ERR) return(0);

//log_debug(">> %x\n",ch);

 switch (chr)
{
case ERR: {o=0;break;}

case 0x31: {o=0x2;break;}
case 0x32: {o=0x3;break;}
case 0x33: {o=0x4;break;}
case 0x34: {o=0x5;break;}
case 0x35: {o=0x6;break;}
case 0x36: {o=0x7;break;}
case 0x37: {o=0x8;break;}
case 0x38: {o=0x9;break;}
case 0x39: {o=0xa;break;}
case 0x30: {o=0xb;break;}

case KEY_F(1): {o=0x3B;break;}
case KEY_F(2): {o=0x3C;break;}
case KEY_F(3): {o=0x3D;break;}
case KEY_F(4): {o=0x3E;break;}
case KEY_F(5): {o=0x3F;break;}
case KEY_F(6): {o=0x40;break;}
case KEY_F(7): {o=0x41;break;}
case KEY_F(8): {o=0x42;break;}
case KEY_F(9): {o=0x43;break;}
case KEY_F(10): {o=0x44;break;}
case KEY_LEFT: {o=0xe04B;break;}
case KEY_B2: {o=0x4C;break;}
case KEY_RIGHT: {o=0xe04D;break;}
case KEY_END: {o=0x4F;break;}
case KEY_DOWN: {o=0xe050;break;}
case KEY_NPAGE: {o=0xe051;break;}
case KEY_IC: {o=0xe052;break;}
case KEY_DC: {o=0xe053;break;}
case KEY_F(13): {o=0x54;break;}
case KEY_F(14): {o=0x55;break;}
case KEY_F(15): {o=0x56;break;}
case KEY_F(11): {o=0x57;break;}
case KEY_F(12): {o=0x58;break;}
case KEY_F(18): {o=0x59;break;}
case KEY_F(19): {o=0x5A;break;}
case KEY_F(20): {o=0x5B;break;}
case KEY_F(21): {o=0x5C;break;}
case KEY_F(22): {o=0x5D;break;}
case KEY_F(25): {o=0x5E;break;}
case KEY_F(26): {o=0x5F;break;}
case KEY_F(27): {o=0x60;break;}
case KEY_F(28): {o=0x61;break;}
case KEY_F(29): {o=0x62;break;}
case KEY_F(30): {o=0x63;break;}
case KEY_F(31): {o=0x64;break;}
case KEY_F(32): {o=0x65;break;}
case KEY_F(33): {o=0x66;break;}
case KEY_F(34): {o=0x67;break;}
case KEY_F(37): {o=0x68;break;}
case KEY_F(38): {o=0x69;break;}
case KEY_F(39): {o=0x6A;break;}
case KEY_F(40): {o=0x6B;break;}
case KEY_F(41): {o=0x6C;break;}
case KEY_F(42): {o=0x6D;break;}
case KEY_F(43): {o=0x6E;break;}
case KEY_F(44): {o=0x6F;break;}
case KEY_F(45): {o=0x70;break;}
case KEY_F(46): {o=0x71;break;}
case KEY_BTAB: {o=0xF;break;}
case KEY_HOME: {o=0xe047;break;}
case KEY_UP: {o=0xe048;break;}
case KEY_PPAGE: {o=0xe049;break;}
case KEY_F(23): {o=0x87;break;}
case KEY_F(24): {o=0x88;break;}
case KEY_F(35): {o=0x89;break;}
case KEY_F(36): {o=0x8A;break;}
case KEY_F(47): {o=0x8B;break;}
case KEY_F(48): {o=0x8C;break;}
#ifdef __PDCURSES__
case ALT_ESC: {o=0x1;break;}
case ALT_BKSP: {o=0xE;break;}
case ALT_Q: {o=0x10;break;}
case ALT_W: {o=0x11;break;}
case ALT_E: {o=0x12;break;}
case ALT_R: {o=0x13;break;}
case ALT_T: {o=0x14;break;}
case ALT_Y: {o=0x15;break;}
case ALT_U: {o=0x16;break;}
case ALT_I: {o=0x17;break;}
case ALT_O: {o=0x18;break;}
case ALT_P: {o=0x19;break;}
case ALT_LBRACKET: {o=0x1A;break;}
case ALT_RBRACKET: {o=0x1B;break;}
case ALT_ENTER: {o=0x1C;break;}
case ALT_A: {o=0x1E;break;}
case ALT_S: {o=0x1F;break;}
case ALT_D: {o=0x20;break;}
case ALT_F: {o=0x21;break;}
case ALT_G: {o=0x22;break;}
case ALT_H: {o=0x23;break;}
case ALT_J: {o=0x24;break;}
case ALT_K: {o=0x25;break;}
case ALT_L: {o=0x26;break;}
case ALT_SEMICOLON: {o=0x27;break;}
case ALT_FQUOTE: {o=0x28;break;}
case ALT_BQUOTE: {o=0x29;break;}
case ALT_BSLASH: {o=0x2B;break;}
case ALT_Z: {o=0x2C;break;}
case ALT_X: {o=0x2D;break;}
case ALT_C: {o=0x2E;break;}
case ALT_V: {o=0x2F;break;}
case ALT_B: {o=0x30;break;}
case ALT_N: {o=0x31;break;}
case ALT_M: {o=0x32;break;}
case ALT_COMMA: {o=0x33;break;}
case ALT_STOP: {o=0x34;break;}
case ALT_FSLASH: {o=0x35;break;}
case ALT_PADSTAR: {o=0x37;break;}
case ALT_PADMINUS: {o=0x4A;break;}
case ALT_PADPLUS: {o=0x4E;break;}
case CTL_LEFT: {o=0x73;break;}
case CTL_RIGHT: {o=0x74;break;}
case CTL_END: {o=0x75;break;}
case CTL_PGDN: {o=0x76;break;}
case CTL_HOME: {o=0x77;break;}
case ALT_1: {o=0x78;break;}
case ALT_2: {o=0x79;break;}
case ALT_3: {o=0x7A;break;}
case ALT_4: {o=0x7B;break;}
case ALT_5: {o=0x7C;break;}
case ALT_6: {o=0x7D;break;}
case ALT_7: {o=0x7E;break;}
case ALT_8: {o=0x7F;break;}
case ALT_9: {o=0x80;break;}
case ALT_0: {o=0x81;break;}
case ALT_MINUS: {o=0x82;break;}
case ALT_EQUAL: {o=0x83;break;}
case CTL_PGUP: {o=0x84;break;}
//case KEY_F(11): {o=0x85;break;}
//case KEY_F(12): {o=0x86;break;}
case CTL_UP: {o=0x8D;break;}
case CTL_PADMINUS: {o=0x8E;break;}
case CTL_PADCENTER: {o=0x8F;break;}
case CTL_PADPLUS: {o=0x90;break;}
case CTL_DOWN: {o=0x91;break;}
case CTL_INS: {o=0x92;break;}
case CTL_DEL: {o=0x93;break;}
case CTL_TAB: {o=0x94;break;}
case CTL_PADSLASH: {o=0x95;break;}
case CTL_PADSTAR: {o=0x96;break;}
case ALT_HOME: {o=0x97;break;}
case ALT_UP: {o=0x98;break;}
case ALT_PGUP: {o=0x99;break;}
case ALT_LEFT: {o=0x9B;break;}
case ALT_RIGHT: {o=0x9D;break;}
case ALT_END: {o=0x9F;break;}
case ALT_DOWN: {o=0xA0;break;}
case ALT_PGDN: {o=0xA1;break;}
case ALT_INS: {o=0xA2;break;}
case ALT_DEL: {o=0xA3;break;}
case ALT_PADSLASH: {o=0xA4;break;}
case ALT_TAB: {o=0xA5;break;}
case ALT_PADENTER: {o=0xA6;break;}
#endif
 }
#endif
 return o;
}

void realtocurs()
{
#ifndef NOCURSES
    for(int colorNumber=0;colorNumber<16; colorNumber++)
	{
	short red   =  (510*((colorNumber & 4)>>2) + 255*((colorNumber & 8)>>3))/3;
	short green =  (510*((colorNumber & 2)>>1)    + 255*((colorNumber & 8)>>3))/3;
	short blue  =  (510*((colorNumber & 1)) + 255*((colorNumber & 8)>>3))/3;
	if (colorNumber == 6) green >>= 1;
	}

    for( int b=0;b<16; b++)
    {
       for( int f=0;f<16; f++)
        {

		   init_pair((b<<4)+f, f, b);
        }
    }
#endif
}


/*
static short realtocurs[16] =
{
    COLOR_BLACK, COLOR_BLUE, COLOR_GREEN, COLOR_CYAN, COLOR_RED,
    COLOR_MAGENTA, COLOR_YELLOW, COLOR_WHITE, 
//    COLOR_BLACK, COLOR_BLUE, COLOR_GREEN, COLOR_CYAN, COLOR_RED,
//    COLOR_MAGENTA, COLOR_YELLOW, COLOR_WHITE

    COLOR_BLACK + 8, COLOR_BLUE + 8, COLOR_GREEN + 8, COLOR_CYAN + 8, COLOR_RED + 8,
    COLOR_MAGENTA + 8, COLOR_YELLOW + 8, COLOR_WHITE + 8

};
    for( int b=0;b<16; b++)
{
       for( int f=0;f<16; f++)
        {
           if(b !=0 && f !=0)
                init_pair((b<<4)+f, realtocurs[f], realtocurs[b]);
        }
}
*/


/*
"Programming for MS-DOS" (Ray Duncan)

                  COM                            EXE
                  ===                            ===
CS:IP           PSP:0100H             Defined by program's END statement
AL              00 if default FCB#1 has valid drive, FF if invalid drive
AH              Ditto, FCB#2
 Bill comment : FCB1 is filled from the first command argument, FCB2 from the
    second. From DOS5 (or maybe DOS6 - it's a long time ago...) FCB1 was
    left empty and FCB2 was filled from argument 1. AFAIAA, this was never
    fixed. What effect it has on this claim (re AX contents) I'm not sure.

DS              PSP                              PSP
ES              PSP                              PSP
SS              PSP                              Seg with STACK attribute
SP              0FFFEH or top word in avail.     Size of STACK segment
                 memory, whichever is least.

From: "The MS-DOS Encyclopaedia" (also Duncan) - talking about .EXE files. There is no comment on this point when discussing .COM files.

"The other processor registers (BX,CX,DX,BP,SI and DI) contain unknown values when the program receives control from MS-DOS."
*/

int init(struct _STATE *state);

void mainproc(_offsets _i, struct _STATE *state);

#ifndef NOCURSES
chtype vga_to_curses[256];
#endif

void prepare_cp437_to_curses() {
#ifndef NOCURSES

    for (size_t i = 0; i < 256; i++) { vga_to_curses[i] = i; }
    vga_to_curses['\0'] = ' ';
    vga_to_curses[0x04] = ACS_DIAMOND;
    vga_to_curses[0x18] = ACS_UARROW;
    vga_to_curses[0x19] = ACS_DARROW;
    vga_to_curses[0x1a] = ACS_RARROW;
    vga_to_curses[0x1b] = ACS_LARROW;
    vga_to_curses[0x9c] = ACS_STERLING;
    vga_to_curses[0xb0] = ACS_BOARD;
    vga_to_curses[0xb1] = ACS_CKBOARD;
    vga_to_curses[0xb3] = ACS_VLINE;
    vga_to_curses[0xb4] = ACS_RTEE;
    vga_to_curses[0xbf] = ACS_URCORNER;
    vga_to_curses[0xc0] = ACS_LLCORNER;
    vga_to_curses[0xc1] = ACS_BTEE;
    vga_to_curses[0xc2] = ACS_TTEE;
    vga_to_curses[0xc3] = ACS_LTEE;
    vga_to_curses[0xc4] = ACS_HLINE;
    vga_to_curses[0xc5] = ACS_PLUS;
    vga_to_curses[0xce] = ACS_LANTERN;
    vga_to_curses[0xd8] = ACS_NEQUAL;
    vga_to_curses[0xd9] = ACS_LRCORNER;
    vga_to_curses[0xda] = ACS_ULCORNER;
    vga_to_curses[0xdb] = ACS_BLOCK;
    vga_to_curses[0xe3] = ACS_PI;
    vga_to_curses[0xf1] = ACS_PLMINUS;
    vga_to_curses[0xf2] = ACS_GEQUAL;
    vga_to_curses[0xf3] = ACS_LEQUAL;
    vga_to_curses[0xf8] = ACS_DEGREE;
    vga_to_curses[0xfe] = ACS_BULLET;
#endif
}
/*
#include <thread>         // std::thread
std::thread int8_thread;
void int8_thread_proc()
{
_STATE state;
_STATE* _state = &state;
X86_REGREF

//R(MOV(cs, seg_offset(_text)));	// mov cs,_TEXT

  R(MOV(ss, seg_offset(int8stack)));	// mov cs,_TEXT
#if _BITS == 32
  esp = ((dd)(db*)&m.int8stack[STACK_SIZE - 4]);
#else
  esp=0;
  sp = STACK_SIZE - 4;
#endif

  es=0;

while(true)
	{
		bx=*(dw *)realAddress(8*4,0);
//		es=(dw *)realAddress(8*4+2,0);

		if (bx)
		{

			CALL(static_cast<_offsets>(bx));
std::this_thread::sleep_for(std::chrono::microseconds(1));
		}
	}
}
*/
 int init(struct _STATE* _state)
 {
    X86_REGREF
    
    log_debug("~~~ heap_size=%d heap_para=%x heap_seg=%x\n", HEAP_SIZE, (HEAP_SIZE >> 4), seg_para(heap) );
    /* We expect ram_top as Kbytes, so convert to paragraphs */
    mcb_init(seg_para(heap), (HEAP_SIZE >> 4) - seg_para(heap) - 1, MCB_LAST);
    
    R(MOV(ss, seg_offset(stack)));
 #if _BITS == 32
    esp = ((dd)(db*)&stack[STACK_SIZE - 4]);
 #else
    esp = 0;
    /* Win16/NE programs start with cs:eip, ss:sp and ds from the NE header
       rather than the MZ/EXE convention below; the optional program hook
       installs that state (and applies segment fixups / initial data) and
       returns true to suppress the defaults. */
    if (!(m2c_ne_entry_setup && m2c_ne_entry_setup(_state))) {
        sp = STACK_SIZE - 4;
        cs = M2C_LOAD_SEG;
        ds = es = M2C_PSP_SEG; // EXE-style entry: CS is the load segment, DS/ES point at the PSP
    }
    *(dw*)(raddr(0, 0x408)) = 0x378; //LPT
    /* DOS loader fills PSP:0002 with the top of the program's memory block
       ("top of memory", in paragraphs). Programs like GW-BASIC copy the
       control block into their data segment and read CPMMEM from offset 2.
       Report 640K - the top of conventional memory on the emulated PC. */
    *(dw*)(host_physical_address(host.current_psp, 2)) = 0xA000;
 #endif

    /* When the Tandy overlay module is linked, present a Tandy/PCjr BIOS
       signature so the game's hardware probe (F000:FFFE==0xFF and
       F000:C000==0x21) selects TANDYSND.EXE instead of the PC speaker driver. */
    if (tnd_present) {
        m2c_bios_rom[0xFFFE] = 0xFF;   // model byte
        m2c_bios_rom[0xC000] = 0x21;   // secondary Tandy ROM marker
        log_debug2("tandy: planted PCjr/Tandy BIOS signature in F000 shadow\n");
    }

    if (m2c::Initializer) {
        m2c::Initializer();
    }

    host_irq_main_state = _state;
    if (!std::getenv("M2C_NO_IRQ")) host_start_irq_thread();

//	*(dw *)realAddress(8*4,0)=k_int8old;
//    int8_thread = std::thread(int8_thread_proc);
//	int8_thread.detach();
    
    return(0);
 }

 void log_regs_m2c(const char *file, int line, const char *instr, _STATE* _state)
 {
  ++counter;
  if (!debug) return;
  X86_REGREF
  log_debug("%x %05d %04X:%08X  %-54s EAX:%08X EBX:%08X ECX:%08X EDX:%08X ESI:%08X EDI:%08X EBP:%08X ESP:%08X DS:%04X ES:%04X FS:%04X GS:%04X SS:%04X CF:%d ZF:%d SF:%d OF:%d AF:%d PF:%d IF:%d\n", \
                         counter,line,cs,eip,instr,       eax,     ebx,     ecx,     edx,     esi,     edi,     ebp,     esp,     ds,     es,     fs,     gs,     ss,     GET_CF()   ,GET_ZF()   ,GET_SF()   ,GET_OF()   ,GET_AF()   ,GET_PF(),   GET_IF());
 }

}

static void write_dos_command_tail(int argc, char *argv[]) {
    db tail[126] = {};
    size_t tail_len = 0;

    for (int i = 1; i < argc && tail_len < 126; ++i) {
        if (!argv[i]) {
            continue;
        }
        tail[tail_len++] = ' ';
        for (const char *arg = argv[i]; *arg && tail_len < 126; ++arg) {
            tail[tail_len++] = static_cast<db>(*arg);
        }
    }

    db *psp = ((db *) &m2c::m) + (static_cast<size_t>(m2c::host.current_psp) << 4);
    psp[0x80] = static_cast<db>(tail_len);
    for (size_t i = 0; i < tail_len; ++i) {
        psp[0x81 + i] = tail[i];
    }
    psp[0x81 + tail_len] = 0x0d;
    m2c::copy_linked_program_segment_prefix(m2c::host.current_psp, psp, 0x100);
}

int main(int argc, char *argv[]) {
    struct m2c::_STATE state;
    struct m2c::_STATE *_state = &state;
    X86_REGREF

    eax = ebx = ecx = edx = ebp = esi = edi = fs = gs = 0; // according to ms-dos 6.22 debuger
    cs=eip=0;

    AFFECT_DF(0);
    AFFECT_CF(0);
    AFFECT_ZF(0);
    AFFECT_SF(0);
    AFFECT_OF(0);
    AFFECT_AF(0);
    AFFECT_PF(0);
    AFFECT_IF(0);
    cx = 0xff; // dummy size of executable


    try {
        m2c::_indent = 0;
        if (m2c::debug)
            m2c::logDebug = fopen("asm.log", "w");
#ifndef NOCURSES
        initscr();
        resize_term(25, 80);
        noecho(); // do not echo

        if (!has_colors()) {
            printw("Unable to use colors");
        }
        start_color();

        m2c::realtocurs();
        curs_set(0);

        refresh();
        cbreak(); // put keys directly to program
        keypad(stdscr, TRUE); // provide keypad buttons
#endif

        m2c::init(_state);

        write_dos_command_tail(argc, argv);
        (*m2c::_ENTRY_POINT_)((m2c::_offsets) 0, _state);
    }
    catch (const std::exception &e) {
        printf("std::exception& %s\n", e.what());
    }
    catch (...) {
        printf("some exception\n");
    }
    return (0);
}
