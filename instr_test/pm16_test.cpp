// Dedicated 16-bit protected-mode (Win16/DPMI) tests.  The rest of this
// harness runs _BITS=32; this TU compiles asm.h in 16-bit protected mode so
// the emulated-LDT resolution path in asm_16.h is exercised directly.
#define _BITS 16
#define _PROTECTED_MODE 1
#include "asm.h"
// asm.h defines single-letter macros (T, R, ...) that clash with gtest
// template parameters — drop them before including gtest.
#ifdef R
#undef R
#endif
#ifdef T
#undef T
#endif
#include <gtest/gtest.h>
#include <cstring>

// Globals are defined in test_globals.cpp; only the externs this file uses
// are re-declared (test_globals.h itself hardcodes _BITS=32).
extern m2c::_STATE* _state;
extern m2c::eflags m2cflags;

namespace {

db* mbase() { return (db*)&m2c::m; }

void int31(dw fn) {
	X86_REGREF
	ax = fn;
	m2c::asm2C_INT(_state, 0x31);
}

// Allocate one 64KB-backed region; returns the selector.
dw alloc_region(dw paras = 0x1000) {
	dw sel = m2c::m2c_pm_alloc_paras(paras);
	EXPECT_NE(sel, 0);
	return sel;
}

} // namespace

TEST(PM16, SelectorEncodingAndStep) {
	X86_REGREF
	dw sel = alloc_region();
	EXPECT_TRUE(sel & 4) << "selector must carry the LDT TI bit";
	EXPECT_EQ(m2c::m2c_ldt_idx(sel), sel >> 3);
	// __AHINCR-style stepping: sel+8 names the next descriptor.
	dw sel2 = m2c::m2c_ldt_alloc(1);
	EXPECT_EQ(sel2, sel + 8);
	EXPECT_EQ(m2c::m2c_ldt_idx(sel2), (sel >> 3) + 1);
	m2c::m2c_ldt_free(sel);
	m2c::m2c_ldt_free(sel2);
}

TEST(PM16, RegionResolveFull64K) {
	X86_REGREF
	dw sel = alloc_region();
	// Real selectors expose the full 64KB regardless of request size:
	// every 16-bit offset must resolve to the same backing block.
	db* base = m2c::m2c_alloc_segment_raddr(sel, 0);
	ASSERT_NE(base, nullptr);
	EXPECT_EQ(m2c::m2c_alloc_segment_raddr(sel, 0xffff), base + 0xffff);

	// Writes through raddr_ land in the region, not in `m`.
	*m2c::raddr_(sel, 0x1234) = 0xab;
	*m2c::raddr_(sel, 0xfffe) = 0xcd;
	EXPECT_EQ(*m2c::raddr_(sel, 0x1234), 0xab);
	EXPECT_EQ(*m2c::raddr_(sel, 0xfffe), 0xcd);
	// Region blocks are malloc'd — must not alias `m` (m extent <= ~1MB).
	db* p0 = m2c::raddr_(sel, 0);
	EXPECT_TRUE(p0 < mbase() || p0 >= mbase() + 0x100000)
		<< "region must not alias m";
	m2c::m2c_pm_free(sel);
	EXPECT_EQ(m2c::m2c_alloc_segment_raddr(sel, 0), nullptr);
}

TEST(PM16, RaddrFallsThroughForParagraphs) {
	X86_REGREF
	// A plain real-mode paragraph (TI bit clear) resolves against `m`.
	db* p = m2c::raddr_(0x40, 0x10);
	EXPECT_EQ(p, mbase() + (0x40 << 4) + 0x10);
}

TEST(PM16, SegOffsetYieldsSelector) {
	X86_REGREF
	// Under _PROTECTED_MODE, `seg X` must produce a real LDT selector
	// aliasing the segment's m storage (this TU compiles with it defined).
	dw sel = seg_offset(m2c::stack);
	EXPECT_TRUE(sel & 4) << "seg value must be a selector";
	// The descriptor aliases the same bytes.
	EXPECT_EQ(m2c::raddr_(sel, 8), (db*)&m2c::stack[8]);
	// Repeated `seg` of the same paragraph shares the alias descriptor.
	EXPECT_EQ(seg_offset(m2c::stack), sel);
	// Stack segment resolution through a selector works too.
	EXPECT_EQ(m2c::stack_raddr_(sel, 0x10), (db*)&m2c::stack[0x10]);
	m2c::m2c_ldt_free(sel);
}

TEST(PM16, DpmiAllocDescriptors) {
	X86_REGREF
	cx = 3;
	int31(0x0000);
	EXPECT_EQ(m2cflags.getCF(), 0);
	dw sel = ax;
	EXPECT_TRUE(sel & 4);
	// Three consecutive descriptors were consumed.
	dw next = m2c::m2c_ldt_alloc(1);
	EXPECT_EQ(next, sel + 3 * 8);
	m2c::m2c_ldt_free(next);
	for (int i = 0; i < 3; ++i) m2c::m2c_ldt_free(sel + i * 8);
}

TEST(PM16, DpmiSetGetBase) {
	X86_REGREF
	cx = 1;
	int31(0x0000);
	ASSERT_EQ(m2cflags.getCF(), 0);
	dw sel = ax;
	// Set base to m-linear 0x2100 (inside m's extent).
	bx = sel; cx = 0; dx = 0x2100;
	int31(0x0007);
	EXPECT_EQ(m2cflags.getCF(), 0);
	EXPECT_EQ(m2c::raddr_(sel, 5), mbase() + 0x2105);
	// Get base must round-trip.
	bx = sel;
	int31(0x0006);
	EXPECT_EQ(m2cflags.getCF(), 0);
	EXPECT_EQ((((dd)cx) << 16) | dx, 0x2100u);
	m2c::m2c_ldt_free(sel);
}

TEST(PM16, DpmiRealSegmentConversion) {
	X86_REGREF
	bx = 0x1234;
	int31(0x0002);
	ASSERT_EQ(m2cflags.getCF(), 0);
	dw sel = ax;
	// Selector aliases m + seg*16.
	EXPECT_EQ(m2c::raddr_(sel, 0x20), mbase() + (0x1234 << 4) + 0x20);
	// Get base reports the real-mode linear address.
	bx = sel;
	int31(0x0006);
	EXPECT_EQ((((dd)cx) << 16) | dx, 0x12340u);
	// Repeat conversion of the same segment returns the same selector.
	bx = 0x1234;
	int31(0x0002);
	EXPECT_EQ(ax, sel);
	m2c::m2c_ldt_free(sel);
}

TEST(PM16, DpmiSetLimitAndRights) {
	X86_REGREF
	cx = 1;
	int31(0x0000);
	dw sel = ax;
	bx = sel; cx = 0; dx = 0x7fff;
	int31(0x0008);
	EXPECT_EQ(m2c::m2c_ldt[m2c::m2c_ldt_idx(sel)].limit, 0x7fffu);
	bx = sel; cx = 0x00fb;
	int31(0x0009);
	EXPECT_EQ(m2c::m2c_ldt[m2c::m2c_ldt_idx(sel)].rights, 0x00fb);
	// Bad selector must set CF.
	bx = 0x6004;               // TI set, never allocated
	int31(0x0008);
	EXPECT_EQ(m2cflags.getCF(), 1);
	m2c::m2c_ldt_free(sel);
}

TEST(PM16, DpmiFreeDescriptor) {
	X86_REGREF
	cx = 1;
	int31(0x0000);
	dw sel = ax;
	bx = sel;
	int31(0x0001);
	EXPECT_EQ(m2cflags.getCF(), 0);
	EXPECT_EQ(m2c::m2c_ldt[m2c::m2c_ldt_idx(sel)].used, 0);
	// Double-free reports failure.
	bx = sel;
	int31(0x0001);
	EXPECT_EQ(m2cflags.getCF(), 1);
}

TEST(PM16, DpmiMemoryBlockSpansDescriptors) {
	X86_REGREF
	// 128KB block -> 2 descriptors sharing one contiguous host block.
	bx = 2; cx = 0;
	int31(0x0501);
	ASSERT_EQ(m2cflags.getCF(), 0);
	dw handle = di;
	dd lin = (((dd)bx) << 16) | cx;
	EXPECT_TRUE(handle & 4);
	// sel and sel+8 both resolve, 64KB apart.
	db* b0 = m2c::m2c_alloc_segment_raddr(handle, 0);
	db* b1 = m2c::m2c_alloc_segment_raddr(handle + 8, 0);
	ASSERT_NE(b0, nullptr);
	ASSERT_NE(b1, nullptr);
	EXPECT_EQ(b1 - b0, 0x10000);
	// Linear base reported by 0006 matches the 0501 result.
	bx = handle;
	int31(0x0006);
	EXPECT_EQ((((dd)cx) << 16) | dx, lin);
	// Free by handle clears the whole multi-descriptor block.
	si = 0; di = handle;
	int31(0x0502);
	EXPECT_EQ(m2cflags.getCF(), 0);
	EXPECT_EQ(m2c::m2c_alloc_segment_raddr(handle, 0), nullptr);
	EXPECT_EQ(m2c::m2c_alloc_segment_raddr(handle + 8, 0), nullptr);
}

TEST(PM16, NeLoadEntryAndFixups) {
	X86_REGREF
	// Minimal NE image: 2 segments, seg0 (code) has one selector fixup
	// targeting seg1 (DGROUP).  Sector shift = 0 so offsets are 1:1.
	static db image[0x100];
	memset(image, 0, sizeof(image));
	auto w16 = [&](dd off, dw v) { image[off] = v & 0xff; image[off+1] = v >> 8; };
	// MZ stub
	w16(0x00, 0x5a4d);            // 'MZ'
	image[0x3c] = 0x40;           // e_lfanew = 0x40
	// NE header at 0x40
	w16(0x40, 0x454e);            // 'NE'
	w16(0x40+0x0e, 2);            // automatic data segment = seg2
	w16(0x40+0x14, 0x0000);       // entry ip
	w16(0x40+0x16, 1);            // entry cs = seg1
	w16(0x40+0x18, 0x0200);       // sp
	w16(0x40+0x1a, 2);            // ss = seg2
	w16(0x40+0x1c, 2);            // segment count
	w16(0x40+0x22, 0x40);         // seg table at NE+0x40 = file 0x80
	w16(0x40+0x32, 0);            // sector shift 0
	// Segment table at 0x80: {fileoff, len, flags, minalloc}
	w16(0x80+0, 0x90); w16(0x80+2, 0x10); w16(0x80+4, 0x0100); w16(0x80+6, 0x10); // code+reloc
	w16(0x88+0, 0xb0); w16(0x88+2, 0x20); w16(0x88+4, 0x0001); w16(0x88+6, 0x20); // data
	// seg0 code bytes at 0x90
	for (int i = 0; i < 0x10; ++i) image[0x90+i] = 0x40 + i;
	// seg0 relocs right after its data at 0xA0: one internal selector fixup
	w16(0xa0, 1);                 // count
	image[0xa2] = 2;              // addr type: 16-bit selector word
	image[0xa3] = 0;              // internal ref
	w16(0xa4, 0x0004);            // patch offset in seg0
	w16(0xa6, 2);                 // target segment index (1-based)
	w16(0xa8, 0x0000);            // target offset
	// seg1 data bytes at 0xB0
	for (int i = 0; i < 0x20; ++i) image[0xb0+i] = 0xa0 + i;

	m2c::M2cNeSegHost segs[2] = {};
	segs[0].para = 0x1000;        // -> m + 0x10000
	segs[1].para = 0x2000;        // -> m + 0x20000
	ASSERT_TRUE(m2c::m2c_ne_load(_state, image, sizeof(image), segs));

	// Both segments got real selectors aliasing their paragraphs.
	EXPECT_TRUE(segs[0].selector & 4);
	EXPECT_TRUE(segs[1].selector & 4);
	EXPECT_EQ(m2c::raddr_(segs[0].selector, 3), mbase() + 0x10003);
	EXPECT_EQ(m2c::raddr_(segs[1].selector, 0), mbase() + 0x20000);
	// File bytes were copied into the segment storage (byte 3 is left of
	// the fixup word at offset 4, which takes the selector value below).
	EXPECT_EQ(mbase()[0x10003], 0x43);
	EXPECT_EQ(mbase()[0x20007], 0xa7);
	// The fixup wrote seg1's selector into seg0+4.
	EXPECT_EQ(*(dw*)(mbase() + 0x10004), segs[1].selector);
	// Entry state: cs:ip / ss:sp / ds from the header.
	EXPECT_EQ(_state->cs, segs[0].selector);
	EXPECT_EQ((_state->eip) & 0xffff, 0u);
	EXPECT_EQ(_state->ss, segs[1].selector);
	EXPECT_EQ((_state->esp) & 0xffff, 0x200u);
	EXPECT_EQ(_state->ds, segs[1].selector);

	m2c::m2c_ldt_free(segs[0].selector);
	m2c::m2c_ldt_free(segs[1].selector);
}

TEST(PM16, DpmiProtectedVectorRoundTrip) {
	X86_REGREF
	// Install a PM vector with a selector aliasing `m` (like generated code).
	bx = 0x60;
	int31(0x0002);             // selector over real segment 0x60
	dw csel = ax;
	bl = 0x75; cx = csel; edx = 0x1234;
	int31(0x0205);
	EXPECT_EQ(m2cflags.getCF(), 0);
	// Get returns the exact sel:eip installed.
	bl = 0x75;
	int31(0x0204);
	EXPECT_EQ(cx, csel);
	EXPECT_EQ(edx, 0x1234u);
	// The m-backed handler was mirrored into the real-mode IVT so normal
	// INT dispatch can reach it.
	EXPECT_EQ(*(dw*)m2c::raddr_(0, 0x75 * 4 + 2), 0x60);
	EXPECT_EQ(*(dw*)m2c::raddr_(0, 0x75 * 4), 0x1234);
	m2c::m2c_ldt_free(csel);
}
