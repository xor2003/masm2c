import unittest

from masm2c.parser import Parser


class ParserConditionalAssemblyTest(unittest.TestCase):
    def test_ifnb_else_endif_keeps_true_branch(self):
        parser = Parser([])
        src = "IFNB <X>\nmov ax,1\nELSE\nmov ax,2\nENDIF\n"
        out = parser.apply_conditional_assembly(src)
        self.assertIn("mov ax,1", out)
        self.assertNotIn("mov ax,2", out)
        self.assertNotIn("IFNB", out)
        self.assertNotIn("ENDIF", out)

    def test_ifidni_case_insensitive(self):
        parser = Parser([])
        src = "IFIDNI <AbC>,<aBc>\nmov bx,3\nELSE\nmov bx,4\nENDIF\n"
        out = parser.apply_conditional_assembly(src)
        self.assertIn("mov bx,3", out)
        self.assertNotIn("mov bx,4", out)

    def test_nested_if_else(self):
        parser = Parser([])
        src = (
            "IFNB <1>\n"
            "IFDIF <A>,<B>\n"
            "mov cx,5\n"
            "ELSE\n"
            "mov cx,6\n"
            "ENDIF\n"
            "ELSE\n"
            "mov cx,7\n"
            "ENDIF\n"
        )
        out = parser.apply_conditional_assembly(src)
        self.assertIn("mov cx,5", out)
        self.assertNotIn("mov cx,6", out)
        self.assertNotIn("mov cx,7", out)


if __name__ == "__main__":
    unittest.main()
