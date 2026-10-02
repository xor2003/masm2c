import tempfile
import unittest
from pathlib import Path

from masm2c.lift import lift_cpp_file, lift_cpp_files, lifted_name


class LiftCppTest(unittest.TestCase):
    def _lift(self, text: str) -> str:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.cpp"
            p.write_text(text)
            lift_cpp_file(str(p))
            return p.read_text()

    def test_mov_cmp_jcc(self):
        out = self._lift(
            '\tR(bx = *(dw*)raddr(ds,0x0A9E););\t// 1 mov bx, ds:0A9Eh\n'
            '\tR(CMP(bx, 0x0FFFF));\t// 2 cmp bx, 0FFFFh\n'
            '\tJ(JZ(locret_1012e));\t// 3 jz locret_1012E\n'
        )
        self.assertIn('bx = *(dw*)raddr(ds,0x0A9E);', out)
        self.assertIn('CMP(bx, 0x0FFFF);', out)
        self.assertIn('if ((dw)(bx) == (dw)(0x0FFFF)) {goto locret_1012e;}', out)

    def test_signed_width_cmp(self):
        # negative literal compare must compare at operand width (uint16)
        out = self._lift(
            '\tR(CMP(ax, -5));\t// 1 cmp ax,-5\n'
            '\tJ(JNZ(failure));\t// 2 jne failure\n'
        )
        self.assertIn('if ((dw)(ax) != (dw)(-5)) {goto failure;}', out)

    def test_pending_dies_on_flag_write(self):
        out = self._lift(
            '\tR(CMP(eax, 0x0f3));\t// 1 cmp eax,0f3h\n'
            '\tR(CLC);\t// 2 clc\n'
            '\tJ(JC(failure));\t// 3 jc failure\n'
        )
        self.assertIn('if (CF) {goto failure;}', out)

    def test_pending_dies_on_subreg_write(self):
        # `mov al,3` clobbers eax: jne must read real ZF, not folded eax
        out = self._lift(
            '\tR(CMP(eax, 4));\t// 1 cmp eax,4\n'
            '\tR(al = 3;);\t// 2 mov al,3\n'
            '\tJ(JNZ(failure));\t// 3 jne failure\n'
        )
        self.assertIn('if (!ZF) {goto failure;}', out)

    def test_pending_dies_on_cmp_operand_store(self):
        # `cmp ax, word_x` / `mov word_x, ax` / `jz`: the mov overwrites a
        # compared operand, so `ax == word_x` text would always be true —
        # the jump must read the materialized ZF instead
        out = self._lift(
            '\tR(CMP(ax, word_29814));\t// 1 cmp ax,word_29814\n'
            '\tR(MOV(word_29814, ax));\t// 2 mov word_29814,ax\n'
            '\tJ(JZ(loc_1));\t// 3 jz loc_1\n'
        )
        self.assertIn('if (ZF) {goto loc_1;}', out)

    def test_clc_keeps_equality_fold(self):
        # clc touches CF only: jz may still fold on the cmp operands
        out = self._lift(
            '\tR(CMP(ax, bx));\t// 1 cmp ax,bx\n'
            '\tR(CLC);\t// 2 clc\n'
            '\tJ(JZ(loc_1));\t// 3 jz loc_1\n'
        )
        self.assertIn('if ((dw)(ax) == (dw)(bx)) {goto loc_1;}', out)

    def test_pending_dies_on_call(self):
        # a call may clobber a pending operand (or flags): no folding across it
        out = self._lift(
            '\tR(CMP(ax, word_x));\t// 1 cmp ax,word_x\n'
            '\tR(sub_1234());\t// 2 call sub_1234\n'
            '\tJ(JZ(loc_1));\t// 3 jz loc_1\n'
        )
        self.assertIn('if (ZF) {goto loc_1;}', out)

    def test_movsx_keeps_macro(self):
        out = self._lift('\tR(MOVSX(bx, bl));\t// 1 movsx bx,bl\n')
        self.assertIn('MOVSX(bx, bl);', out)

    def test_call_retn(self):
        out = self._lift(
            '\tJ(CALL(start,0));\t// 1 call start\n'
            '\tJ(RETN(0));\t// 2 retn\n'
        )
        self.assertIn('CALL(start, 0);', out)
        self.assertIn('RETN(0);', out)

    def test_two_stmts_one_line(self):
        out = self._lift(
            '\tJ(CALL(start,0));\tJ(RETN(0));\n'
        )
        self.assertIn('CALL(start, 0);', out)
        self.assertIn('RETN(0);', out)

    def test_non_stmt_lines_passthrough(self):
        out = self._lift('label:\n\tif (x) {\n')
        self.assertEqual(out, 'label:\n\tif (x) {\n')

    def test_separate_files(self):
        # stock .cpp stays untouched; readable code goes to *_lifted.cpp and
        # lifted segment includes are repointed to the lifted siblings
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "snake_seg001.cpp").write_text(
                '\tR(ax = 1;);\t// 1 mov ax,1\n')
            (td / "snake.cpp").write_text(
                '#include "snake.h"\n#include "snake_seg001.cpp"\n'
                '\tR(bx = 2;);\t// 2 mov bx,2\n')
            lift_cpp_files([str(td / "snake.cpp"), str(td / "snake_seg001.cpp")])

            # stock files untouched
            self.assertIn('R(bx = 2;)', (td / "snake.cpp").read_text())
            self.assertIn('R(ax = 1;)', (td / "snake_seg001.cpp").read_text())
            # lifted files exist and are self-consistent
            lifted_main = (td / "snake_lifted.cpp").read_text()
            self.assertIn('bx = 2;', lifted_main)
            self.assertIn('#include "snake_seg001_lifted.cpp"', lifted_main)
            self.assertIn('ax = 1;', (td / "snake_seg001_lifted.cpp").read_text())

    def test_lifted_name(self):
        self.assertEqual(lifted_name('/d/foo.cpp'), '/d/foo_lifted.cpp')


if __name__ == '__main__':
    unittest.main()
