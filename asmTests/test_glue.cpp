/* asmTests glue: binds test program symbols to the universal runtime hooks.
 * The runtime (asm.cpp) never names program symbols -- tests that exercise a
 * hook declare the well-known symbol names in their .asm, this file picks
 * them up via weak linkage and registers them at startup. */
#include "asm.h"

/* vga_panel_palette.asm: seeds a VGA palette block from a source table. */
extern "C" {
extern m2c::db vga_rgb_data[] __attribute__((weak));
extern m2c::db vga_panel[] __attribute__((weak));
extern m2c::db vga_panel1[] __attribute__((weak));
extern m2c::db setpaletteflag __attribute__((weak));
}

/* timer_thread.asm: defines the deterministic counter cells the host timer
 * thread advances; any test defining the same well-known names gets them
 * ticked the same way. Generated symbols are references -- cells holding a
 * pointer into _data -- so each extern is declared as the pointer type the
 * slot stores; reading it yields the referent address. &sym still resolves
 * to the slot itself, which is what the weak-undef null check needs. */
extern "C" {
extern m2c::db* key __attribute__((weak));
extern m2c::dw* ticker __attribute__((weak));
extern m2c::dw* frames __attribute__((weak));
extern m2c::dw* countdown __attribute__((weak));
extern dd* elapsedtime __attribute__((weak));
}

__attribute__((constructor)) static void test_glue_register_hooks() {
	m2c::m2c_game_hooks hooks = {};
	if (&key) hooks.key_state = key;
	if (&ticker) hooks.det_ticker = ticker;
	if (&frames) hooks.det_frames = frames;
	if (&countdown) hooks.det_countdown = countdown;
	if (&elapsedtime) hooks.det_elapsed = elapsedtime;
	m2c::m2c_set_game_hooks(&hooks);

	if (&vga_rgb_data && &vga_panel && &vga_panel1 && &setpaletteflag) {
		m2c::m2c_palette_map map = {};
		map.flag = &setpaletteflag;
		map.src = vga_panel1;
		map.dst_a = vga_panel;
		map.dst_b = vga_rgb_data;
		map.start = 176 * 3;
		map.size = 80 * 3;
		m2c::m2c_register_palette_map(&map);
	}
}
