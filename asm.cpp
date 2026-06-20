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
  #include <sys/time.h>
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
#include <ctime>
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <thread>

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

#ifdef M2CDEBUG
  size_t debug = M2CDEBUG;
#else
  size_t debug = 0;
#endif
bool defered_irqs=false;
  size_t counter = 0;

    db _indent=0;
    const char *_str="";
    bool fix_segs(){return true;}
    void interpret_unknown_callf(dw cs, dd eip, db source){assert(0);}


ShadowStack shadow_stack;

//db vgaPalette[256*3];
#include "vgapal.h"
dd selectorsPointer;
dd selectors[NB_SELECTORS];

dd heapPointer;
struct find_t;
static db defaultDiskTransferArea[128] = {};
struct find_t * diskTransferAddr = reinterpret_cast<find_t *>(defaultDiskTransferArea);
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
	db current_mode = 3;
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
	uint64_t last_us = 0;
	uint64_t accum_us = 0;
	int divider_20hz = 0;
};

struct HostHardware {
	HostMouse mouse;
	HostVga vga;
	HostPit pit;
	HostTimer timer;
	db ppi_port_b = 0;
	db keyboard_scan_code = 0;
};

static HostHardware host;

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
		renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
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

static size_t vga_count_nonzero_at_start(size_t start, bool require_visible_palette) {
	size_t count = 0;
	for (int y = 0; y < 200; ++y) {
		for (int x = 0; x < 320; ++x) {
			const size_t byte_offset = (start + y * 80 + x / 4) % VGA_WINDOW_SIZE;
			const db color = vgaMode13Pixels[byte_offset * 4 + (x & 3)];
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
			const size_t byte_offset = (start + y * 80 + x / 4) % VGA_WINDOW_SIZE;
			const db color = vgaMode13Pixels[byte_offset * 4 + (x & 3)];
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

static size_t vga_crtc_start_byte_offset() {
	const size_t crtc_start = (static_cast<size_t>(host.vga.crtc_regs[0x0c]) << 8) | host.vga.crtc_regs[0x0d];
	if (host.vga.current_mode == 0x13 && host.vga.seq_regs[2] != 0) {
		return (crtc_start * 2) % VGA_WINDOW_SIZE;
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
		"vga stats #%u mode=%02x crtc=%04zx seq2=%02x gc5=%02x visible=%zu visible-lit=%zu p0=%zu p4000=%zu p8000=%zu pc000=%zu\n",
		dump_count,
		host.vga.current_mode,
		crtc_start,
		host.vga.seq_regs[2],
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
				const size_t byte_offset = (crtc_start + y * 80 + x / 4) % VGA_WINDOW_SIZE;
				color = vgaMode13Pixels[byte_offset * 4 + (x & 3)];
			} else {
				color = vgaPlanarPixels[y * 640 + x];
			}
			vgaSdlFrame[y * vga_logical_width + x] = vga_color_to_argb(color);
		}
	}

	SDL_UpdateTexture(vgaTexture, NULL, vgaSdlFrame, vga_logical_width * static_cast<int>(sizeof(uint32_t)));
	SDL_RenderClear(renderer);
	SDL_RenderCopy(renderer, vgaTexture, NULL, NULL);
}

void vga_present_pending() {
	if (renderer && vga_render_dirty) {
		vga_render_indexed_frame();
		SDL_RenderPresent(renderer);
		vga_render_dirty = false;
		vga_render_writes = 0;
	}
}

static bool vga_is_planar_mode() {
	return host.vga.seq_regs[2] != 0;
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
	if (!ensure_sdl_vga_window(320, 200)) {
		return;
	}
	if (di < 320 * 200) {
		vgaMode13Pixels[di * 4] = color;
	}
	vga_render_dirty = true;
	if (++vga_render_writes >= VGA_RENDER_WRITE_FLUSH_THRESHOLD) {
		vga_present_pending();
	}
}
 #endif
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

static void host_set_key(int scan_code, bool pressed) {
	db* keys = host_key_state();
	if (scan_code < 0 || scan_code >= 128 || keys == nullptr) {
		return;
	}
	keys[scan_code] = pressed ? 1 : 0;
	host.keyboard_scan_code = pressed ? scan_code : (scan_code | 0x80);
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

	host.timer.in_callback = true;
	int ticks_this_pump = 0;
	while (host.timer.accum_us >= 10000 && ticks_this_pump < 5) {
		host.timer.accum_us -= 10000;
		++ticks_this_pump;
		if (::gameintr100) {
			::gameintr100(0, _state);
		}
		if (++host.timer.divider_20hz >= 5) {
			host.timer.divider_20hz = 0;
			if (::gameintr20) {
				::gameintr20(0, _state);
			}
		}
	}
	host.timer.in_callback = false;
}

static void poll_host_events(struct _STATE* _state) {
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
			case SDL_KEYUP:
				host_set_key(sdl_scancode_to_pc(event.key.keysym.scancode),
					event.type == SDL_KEYDOWN);
				break;
			default:
				break;
			}
		}
	}
#endif
	host_run_timer(_state);
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
#endif
}
void log_debug(const char *fmt, ...) {
#ifdef M2CDEBUG
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
	case 0x20:
	case 0x21:
		break;
		case 0x40:
			host.pit.channel0_latch = data;
			break;
	case 0x43:
		break;
	case 0x61:
		host.ppi_port_b = data;
		break;
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
		log_debug("unknown OUT %x,%x at %x:%x\n",address, data,cs,eip);
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
	case 0x3DA:
		host.vga.attr_waiting_for_index = true;
  #if SDL_MAJOR_VERSION == 2 && !defined(NOSDL) && M2CDEBUG != -1
		vga_present_pending();
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
#define SUCCESS         0       /* Function was successful      */
	log_debug2("INT %x ax=%x bx=%x cx=%x dx=%x\n",a,ax,bx,cx,dx);


	switch(a) {
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
				log_debug2("Switch to text mode\n");
				return;
			}
			case 0x13: {
				log_debug2("Switch to VGA\n");
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
			bh = 0;
			return;
		}
		case 0x02: { // set cursor
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
	case 0x21:

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
		case 0x3d: //open
		{
				char fileName[1000];
	//			if (path!=NULL) {
	//				sprintf(fileName,"%s/%s",path,(const char *) realAddress(dx, ds));
	//			} else {
					sprintf(fileName,"%s",(const char *) realAddress(dx, ds));
	//			}
				if (fileName[0] == '\0') {
					log_error("Error opening empty filename ds=%04x dx=%04x\n", ds, dx);
					stackDump(_state);
				}
				file=fopen(fileName, "rb"); //TOFIX, multiple files support
				log_debug2("Opening file %s -> %p\n",fileName,(void *) file);
				if (m2c_stats_enabled()) {
					std::fprintf(stderr, "dos open %s -> %p\n", fileName, static_cast<void *>(file));
				}
				if (file!=NULL) {
					eax=1; //TOFIX
				} else {
					AFFECT_CF(1);
					log_error("Error opening file %s\n",fileName);
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
			// bx: file handle to close
			//TOFIX
			log_debug2("Closing file. bx:%d\n",bx);
			if (!file || fclose(file))  {
				AFFECT_CF(1);
				perror("Error");
				log_error("Error closing file ? bx:%d %p\n",bx,(void *) file);
			}

			file=NULL;
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

			if (feof(file)) {
				log_debug2("feof(file)\n");
				eax=0;
			} else {
				size_t r=fread (buffer,1,cx,file);
				if (r!=cx) {
					perror("Error");
					log_error("r!=cx cx:%d R:%zu \n",cx,r);
					if(!feof(file)) {
						log_error("Error reading ? %d %zu %p\n",cx,r,(void *) file);
						AFFECT_CF(1);
					}
				} else {
					log_debug2("Reading OK %p\n",(void *) file);
				}
				eax=r;
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
			switch(ah) {
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
			if (fseek(file,offset,seek)!=0) {
				log_error("Error seeking\n");
				AFFECT_CF(1);
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
		case 0x4c:
		{
			stackDump(_state);
			jumpToBackGround = 1;
			executionFinished = 1;
			exitCode = al;
			log_error("Graceful exit al=%d\n",al);
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
/*  protected mode temporrary disabled
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
			if (selectorsPointer+cx>=NB_SELECTORS) {
				AFFECT_CF(1);
				log_error("Not enough free selectors (increase NB_SELECTORS)\n");
				return;
			} else {
				eax = selectorsPointer;
				selectorsPointer+=cx;
				log_debug2("Return %x\n",eax);
			}
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
			 
			log_debug2("Function 0002h - Converts a real mode segment into a protected mode descriptor real mode segment: %d\n",ebx);
			if (selectorsPointer+1>=NB_SELECTORS) {
				AFFECT_CF(1);
				log_error("Not enough free selectors (increase NB_SELECTORS)\n");
				return;
			}
			// TOFIX ?
			// always return vga adress.
			selectors[selectorsPointer]=offsetof(struct Mem,vgaRam); // bx;
			eax=selectorsPointer;
			log_debug2("Returns new selector: eax: %d\n",eax);
			selectorsPointer++;

			// Multiple calls for the same real mode segment return the same selector. The returned descriptor should never be modified or freed. <- TOFIX
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
			log_debug2("Function 0007h - Set Segment Base Address: ebx: %x, edx:%x ecx:%x\n",ebx,edx,ecx);
			if (bx>selectorsPointer) {
				AFFECT_CF(1);
				log_error("Error: selector number doesnt exist\n");
				return;
			}
			selectors[bx]=(dx&0xffff)+(cx<<16);
			log_debug2("Address for selector %d: %x\n",bx,selectors[bx]);
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
			 

			// To implement...
			log_debug2("Function 0008h - Set Segment Limit for selector %d (Ignored)\n",bx);
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
			 
			int32_t nbBlocks=(bx<<16)+cx;
			log_debug2("Function 0501h - Allocate Memory Block: %d bytes\n",nbBlocks);

			if (heapPointer+nbBlocks>=HEAP_SIZE) {
				AFFECT_CF(1);
				log_error("Not enough memory (increase HEAP_SIZE)\n");
				exit(1);
				return;
			} else {
				dd a=offsetof(struct Mem,heap)+heapPointer;
				heapPointer+=nbBlocks;
				{
					log_debug2("New top of heap: %x\n",(dd) offsetof(struct Mem,heap)+heapPointer);
				}
				ecx=a & 0xFFFF;
				ebx=a >> 16;
				edi=0; // TOFIX
				esi=0; // TOFIX
				log_debug2("Return %x ebx:ecx %x:%x\n",a,ebx,ecx);
				return;
			}
			break;
		}
		case 0x205: {
			
			//   fo implement
			//   ;2.18 - Function 0204h - Get Protected Mode Interrupt Vector:
			//   ;------------------------------------------------------------
			//   ;
			//   ;  Returns the address of the current protected mode interrupt handler for the
			//   ;specified interrupt.
			//   ;
			//   ;In:
			//   ;  AX     = 0204h
			//   ;  BL     = interrupt number
			//   ;
			//   ;Out:
			//   ;  always successful:
			//   ;    carry flag clear
			//   ;    CX:EDX = selector:offset of protected mode interrupt handler
			
			//   ;  AX     = 0204h
			//   ;  BL     = interrupt number
			//   ;
			//   ;Out:
			//   ;  always successful:
			//   ;    carry flag clear
			//   ;    CX:EDX = selector:offset of protected mode interrupt handler
			 

			return;
		}
		default:
			break;
		}
		break;
*/
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
	log_debug("Error DOSInt 0x%x ah:0x%x al:0x%x: bx:0x%x not supported.\n",a,ah,al,bx);
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
    
    log_debug("~~~ heap_size=%d heap_para=%x heap_seg=%x\n", HEAP_SIZE, (HEAP_SIZE >> 4), seg_offset(heap) );
    /* We expect ram_top as Kbytes, so convert to paragraphs */
    mcb_init(seg_offset(heap), (HEAP_SIZE >> 4) - seg_offset(heap) - 1, MCB_LAST);
    
    R(MOV(ss, seg_offset(stack)));
 #if _BITS == 32
    esp = ((dd)(db*)&stack[STACK_SIZE - 4]);
 #else
    esp = 0;
    sp = STACK_SIZE - 4;
    ds = es = 0x192; // dosbox PSP
    *(dw*)(raddr(0, 0x408)) = 0x378; //LPT
 #endif

    if (m2c::Initializer) {
        m2c::Initializer();
    }

//	*(dw *)realAddress(8*4,0)=k_int8old;
//    int8_thread = std::thread(int8_thread_proc);
//	int8_thread.detach();
    
    return(0);
 }

 void log_regs_m2c(const char *file, int line, const char *instr, _STATE* _state)
 {
  ++counter;
  X86_REGREF
  log_debug("%x %05d %04X:%08X  %-54s EAX:%08X EBX:%08X ECX:%08X EDX:%08X ESI:%08X EDI:%08X EBP:%08X ESP:%08X DS:%04X ES:%04X FS:%04X GS:%04X SS:%04X CF:%d ZF:%d SF:%d OF:%d AF:%d PF:%d IF:%d\n", \
                         counter,line,cs,eip,instr,       eax,     ebx,     ecx,     edx,     esi,     edi,     ebp,     esp,     ds,     es,     fs,     gs,     ss,     GET_CF()   ,GET_ZF()   ,GET_SF()   ,GET_OF()   ,GET_AF()   ,GET_PF(),   GET_IF());
 }

}

static void write_dos_command_tail(int argc, char *argv[]) {
    if (argc < 2) {
        return;
    }

    db *psp = ((db *) &m2c::m);
    size_t tail_len = 0;

    for (int i = 1; i < argc && tail_len < 126; ++i) {
        if (!argv[i]) {
            continue;
        }
        psp[0x81 + tail_len++] = ' ';
        for (const char *arg = argv[i]; *arg && tail_len < 126; ++arg) {
            psp[0x81 + tail_len++] = static_cast<db>(*arg);
        }
    }

    psp[0x80] = static_cast<db>(tail_len);
    psp[0x81 + tail_len] = 0x0d;
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
