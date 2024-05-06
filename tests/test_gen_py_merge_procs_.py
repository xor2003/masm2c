from collections import OrderedDict

from masm2c.gen import Gen
import masm2c.proc as proc_module
from masm2c.parser import Parser

class Test_MergeAllProcs:

    #  Merges all procs that have cross jumps and are incompatible with C.
    def test_merge_procs_with_cross_jumps(self):
        context = Parser()
        first_proc_name = "proc1"
        first_proc = proc_module.Proc(first_proc_name, line_number=1)
        first_proc.to_group_with = set(["proc2", "proc3"])
        context.set_global(first_proc_name, first_proc)
        proc2 = proc_module.Proc("proc2", line_number=2)
        proc2.to_group_with = set(["proc1", "proc3"])
        context.set_global("proc2", proc2)
        proc3 = proc_module.Proc("proc3", line_number=3)
        proc3.to_group_with = set(["proc1", "proc2"])
        context.set_global("proc3", proc3)

        gen = Gen(context=context)
        gen._procs = ["proc1", "proc2", "proc3"]
        gen.grouped = set()

        gen._merge_all_procs()

        assert gen._procs == ["_group1"]
        assert gen.grouped == set(["proc1", "proc2", "proc3"])
        assert gen.groups == OrderedDict({'proc1': '_group1', 'proc2': '_group1', 'proc3': '_group1'})
        assert first_proc.to_group_with == set(["proc2", "proc3"])
        assert first_proc.provided_labels == set(["proc1", "proc2", "proc3"])
        assert first_proc.stmts[0].proc == "_group1"
        assert first_proc.stmts[0].data == "label"
        assert first_proc.stmts[0].real_offset == first_proc.real_offset
        assert first_proc.stmts[0].real_seg == first_proc.real_seg
        assert gen._context.get_global("_group1") == first_proc

    def test_merge_two_procs_with_label_updates_groups_dictionary(self):
        first_proc_name = "proc1"
        first_proc = proc_module.Proc("proc1")
        next_proc_name = "proc2"
        next_proc = proc_module.Proc("proc2")
        new_group_name = "group1"

        context = Parser()
        gen = Gen(context=context)
        gen.merge_two_procs_with_label(first_proc_name, first_proc, next_proc_name, next_proc, new_group_name)

        assert gen.groups[next_proc_name] == new_group_name