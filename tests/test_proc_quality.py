import unittest

from masm2c import op
from masm2c.proc import Proc


class ProcQualityTest(unittest.TestCase):
    def test_optimize_removes_unreachable_until_label(self):
        proc = Proc("p")
        mov1 = proc.create_instruction_object("mov", [])
        ret = proc.create_instruction_object("ret", [])
        dead = proc.create_instruction_object("mov", [])
        live_after_label = proc.create_instruction_object("mov", [])
        join = op.label("join", proc="p")

        proc.stmts = [mov1, ret, dead, join, live_after_label]
        removed = proc.optimize()

        self.assertEqual(removed, 1)
        self.assertEqual(proc.stmts, [mov1, ret, join, live_after_label])

    def test_complexity_metrics_counts_branches(self):
        proc = Proc("p")
        jnz = proc.create_instruction_object("jnz", [])
        ret = proc.create_instruction_object("ret", [])
        lbl = op.label("l1", proc="p")
        proc.stmts = [lbl, jnz, ret]

        m = proc.complexity_metrics()
        self.assertEqual(m["statements"], 3)
        self.assertEqual(m["labels"], 1)
        self.assertEqual(m["branch_points"], 1)
        self.assertEqual(m["cyclomatic"], 2)


if __name__ == "__main__":
    unittest.main()
