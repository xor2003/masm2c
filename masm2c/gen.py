import logging
import pickle
import re
from collections import OrderedDict
from copy import copy
from typing import TYPE_CHECKING

import jsonpickle

from lark import lark
from masm2c import op
from masm2c import proc as proc_module
from masm2c.Token import Expression

if TYPE_CHECKING:
    from masm2c.parser import Parser


class Gen:
    def __init__(self,context: "Parser", outfile: str="", skip_output: None=None,
                 merge_data_segments: bool=True) -> None:
        self.label_to_proc = {}
        self._isjustlabel = False
        self.groups = OrderedDict()
        self.grouped = set()
        self._middle_size = 0
        self.merge_data_segments = merge_data_segments
        self._procs = context.proc_list
        self.body = ""
        self.lea = False
        self._work_segment = "ds"
        self.isvariable = False  # only address or variable
        context.cpp = self




    def calculate_size(self, expr: Expression) -> int:
        result = expr.size()
        return result


    def calculate_member_size(self, label: list[str]) -> int:
        g = self._context.get_global(label[0])
        type = label[0] if isinstance(g, op.Struct) else g.original_type

        try:
            for member in label[1:]:
                if (g := self._context.get_global(type)) is None:
                    raise KeyError(type)
                if isinstance(g, op.Struct):
                    g = g.getitem(member)
                    type = g.data
                else:
                    return g._size
        except KeyError as ex:
            logging.debug(f"Didn't found for {label} {ex.args} will try workaround")
            # if members are global as with M510 or tasm try to find last member size
            g = self._context.get_global(label[-1])

        return g.size



    def leave_unique_labels(self, labels):
        """For IDA .lst it takes a list of labels and returns a list of unique labels based on address.

        :param labels: a list of labels to be processed
        :return: A list of labels.
        """
        if not self._context.itislst:
            return labels
        uniq_labels = OrderedDict()
        for label in labels:
            g = self._context.get_global(label)
            uniq_labels[f"{g.real_seg}_{g.real_offset}"] = label
        return uniq_labels.values()

    def merge_procs(self):
        """Merge procs in case they have cross jumps since incompatible with C.

        :return:
        """
        if self._context.args.mergeprocs == "separate":
            for index, first_proc_name in enumerate(self._procs):
                first_proc = self._context.get_global(first_proc_name)
                if not first_proc.if_terminated_proc() and index < len(self._procs) - 1:
                    result = self._context.parse_text(self._procs[index + 1], start_rule="expr")
                    expr = self._context.process_ast("", result)
                    o = first_proc.create_instruction_object("jmp", [expr])
                    o.filename = ""
                    o.line_number = 0
                    o.raw_line = ""
                    o.syntetic = True
                    first_proc.stmts.append(o)

        self.generate_label_to_proc_map()

        #if self._context.args.mergeprocs == 'separate':

        if self._context.args.mergeprocs != "single":
            for index, first_proc_name in enumerate(self._procs):
                first_proc = self._context.get_global(first_proc_name)

                first_proc.used_labels = self.leave_only_procs_and_labels(first_proc.used_labels)
                logging.debug(f"Proc {first_proc_name} used labels {first_proc.used_labels}")
                logging.debug(f"                   provided labels {first_proc.provided_labels}")

                missing_labels = first_proc.used_labels - first_proc.provided_labels
                logging.debug(f"                    missing labels {missing_labels}")
                procs_to_merge = set()
                if not first_proc.if_terminated_proc():
                    """If execution does not terminated in the procedure range when merge it with next proc"""
                    if index + 1 < len(self._procs):
                        logging.info(
                            f"Execution does not terminated need to merge {first_proc_name} with {self._procs[index + 1]}")
                        procs_to_merge.add(self._procs[index + 1])
                    else:
                        logging.info(f"Execution does not terminated could not find proc after {first_proc_name}")

                if missing_labels:
                    procs_to_merge.add(first_proc_name)  # TODO Why?
                    for missing_label in missing_labels:
                        procs_to_merge.add(self.find_related_proc(missing_label))  # if label then merge proc implementing it

                if self._context.args.mergeprocs == "persegment":
                    for pname in self._procs:
                        if pname != first_proc_name:
                            p_proc = self._context.get_global(pname)
                            if first_proc.segment == p_proc.segment:
                                procs_to_merge.add(pname)

                first_proc.to_group_with = procs_to_merge
                logging.debug(f" will merge {procs_to_merge}")
            changed = True
            iteration = 0
            while changed:
                iteration += 1
                logging.info(f"     Identifing proc to merge #{iteration}")
                changed = False
                for first_proc_name in self._procs:
                    logging.debug(f"Proc {first_proc_name}")
                    first_proc = self._context.get_global(first_proc_name)
                    for next_proc_name in first_proc.to_group_with:
                        if first_proc_name != next_proc_name:
                            logging.debug(f"  will group with {next_proc_name}")
                            next_proc = self._context.get_global(next_proc_name)
                            if not next_proc.to_group_with:
                                next_proc.to_group_with = set()
                            if first_proc.to_group_with != next_proc.to_group_with:
                                first_proc.to_group_with = next_proc.to_group_with = set.union(next_proc.to_group_with, first_proc.to_group_with)
                                changed = True
                    logging.debug(f"  will group with {first_proc.to_group_with}")

            for first_proc_name in self._procs:
                logging.debug(f"Proc {first_proc_name}")
                self.leave_only_same_segment_procs(first_proc_name)

            self.print_how_procs_merged()

        groups = []
        groups_id = 1
        for first_proc_name in self._procs:
            if first_proc_name not in self.grouped:
                first_proc = self._context.get_global(first_proc_name)
                if self._context.args.mergeprocs == "single" or first_proc.to_group_with:
                    logging.debug(f"Merging {first_proc_name}")
                    new_group_name = f"_group{groups_id}"
                    first_label = op.label(first_proc_name, proc=new_group_name, isproc=False,
                                           line_number=first_proc.line_number, far=first_proc.far)
                    first_label.real_offset, first_label.real_seg = first_proc.real_offset, first_proc.real_seg

                    first_label.used = True
                    first_proc.stmts.insert(0, first_label)
                    first_proc.provided_labels.add(first_proc_name)
                    self._context.reset_global(first_proc_name, first_label)
                    self.grouped.add(first_proc_name)

                    self.groups[first_proc_name] = new_group_name
                    proc_to_group = self._procs if self._context.args.mergeprocs == "single" else first_proc.to_group_with
                    proc_to_group = self.sort_procedure_list_in_linenumber_order(proc_to_group)

                    for next_proc_name in proc_to_group:
                        if next_proc_name != first_proc_name and next_proc_name not in self.grouped:
                            next_proc = self._context.get_global(next_proc_name)
                            if isinstance(next_proc, proc_module.Proc):  # and first_proc.far == next_proc.far:
                                self.groups[next_proc_name] = new_group_name
                                next_label = op.label(next_proc_name, proc=first_proc_name, isproc=False,
                                                      line_number=next_proc.line_number, far=next_proc.far)
                                next_label.real_offset, next_label.real_seg = next_proc.real_offset, next_proc.real_seg
                                next_label.used = True
                                first_proc.add_label(next_proc_name, next_label)
                                logging.debug(f"     with {next_proc_name}")
                                first_proc.merge_two_procs(new_group_name, next_proc)
                                for missing_label in first_proc.provided_labels:
                                    self.label_to_proc[missing_label] = new_group_name
                                self._context.reset_global(next_proc_name, next_label)
                                self.grouped.add(next_proc_name)
                    groups += [new_group_name]
                    self._context.set_global(new_group_name, first_proc)
                    groups_id += 1
        self._procs = [x for x in self._procs if x not in self.grouped]
        self._procs += groups
        self._procs = self.sort_procedure_list_in_linenumber_order(self._procs)

    def generate_label_to_proc_map(self):
        for proc_name in self._procs:
            proc = self._context.get_global(proc_name)
            logging.debug(f"Proc {proc_name} provides: {proc.provided_labels}")
            for label in proc.provided_labels:
                self.label_to_proc[label] = proc_name

    def sort_procedure_list_in_linenumber_order(self, proc_list):
        """It takes a list of procedure names, and returns sorted in the order in which they appear in the program.

        :param proc_list: a list of procedure names
        :return: A list of procedure names in line number order.
        """
        line_to_proc = {
            self._context.get_global(first_proc_name).line_number: first_proc_name for first_proc_name in
             proc_list}
        return [line_to_proc[line_number] for line_number in sorted(line_to_proc.keys())]

    def leave_only_same_segment_procs(self, proc_name):
        """It takes a procedure name and returns a set of procedure names that are in the same segment as the given
        procedure.

        :param proc_name: The name of the procedure to leave only same segment procs for
        """
        proc = self._context.get_global(proc_name)
        only_current_segment_procs = set()
        for other_proc_name in proc.to_group_with:
            if proc_name != other_proc_name:
                other_proc = self._context.get_global(other_proc_name)
                if proc.segment == other_proc.segment:
                    only_current_segment_procs.add(other_proc_name)
        proc.to_group_with = only_current_segment_procs

    def print_how_procs_merged(self):
        """It prints out the names of the procedures that were merged together."""
        for first_proc_name in self._procs:
            first_proc = self._context.get_global(first_proc_name)
            if first_proc.to_group_with:
                logging.info(f"     ~{first_proc_name}")
                for p_name in first_proc.to_group_with:
                    logging.info(f"       {p_name}")

    def find_related_proc(self, name):
        """:param name: the name of the global object
        :return: The name of the related proc.
        """
        logging.debug(f"get_related_proc {name}")
        global_object = self._context.get_global(name)
        if isinstance(global_object, op.label):
            related_proc = self.label_to_proc[name]
            logging.debug(f" {name} is a label, related proc nameL {related_proc}")
        elif isinstance(global_object, proc_module.Proc):
            related_proc = global_object.name
            logging.debug(f" {name} is a proc, related proc nameL {related_proc}")
        return related_proc

    def leave_only_procs_and_labels(self, all_labels):
        """It takes a list of labels and returns a list of labels that are actually labels or proc names.

        :param all_labels: a list of all labels in the program
        :return: A set of labels.
        """
        labels = set()  # leave only real labels
        for label_name in all_labels:
            first_label = self._context.get_global(label_name)
            if isinstance(first_label, op.label | proc_module.Proc):
                labels.add(label_name)
        return labels

    def write_segment_file(self, segments, structs, fname):
        jsonpickle.set_encoder_options("json", indent=2)
        fname = fname.replace(".asm",".seg").replace(".lst",".seg")
        with open(fname, "wb") as f:
            pickle.dump((segments, structs), f)

    def read_segment_files(self, asm_files):
        logging.info(" *** Merging .seg files")
        segments = OrderedDict()
        structs = OrderedDict()
        for file in asm_files:
            file = file.replace(".asm", ".seg").replace(".lst", ".seg")
            logging.info(f"     Merging data from {file}")
            with open(file, "rb") as f:
                segments, structures = self.merge_segments(segments, structs, *pickle.load(f))
        return segments, structures

    def merge_segments(self, allsegments: OrderedDict, allstructs: OrderedDict, newsegments: OrderedDict,
                       newstructs: OrderedDict):
        """If the segment is public and the user wants to merge public segments, then merge the segment. Otherwise, if the
        segment already exists, overwrite it.

        :param allsegments: OrderedDict
        :param allstructs: OrderedDict
        :param newsegments: OrderedDict
        :param newstructs: OrderedDict
        :return: Merged segments and merged structs
        """
        if self.merge_data_segments:
            logging.info("Will merge public data segments")
        for k, v in newsegments.items():
            segclass = v.segclass
            ispublic = v.options and "public" in v.options
            if segclass and ispublic and self.merge_data_segments:
                if segclass not in allsegments:
                    allsegments[segclass] = v
                else:
                    data = v.getdata()
                    for d in data:
                        allsegments[segclass].append(d)
            else:
                if k in allsegments and (v.getsize() > 0 or allsegments[k].getsize() > 0):
                    old = jsonpickle.encode(allsegments[k], unpicklable=False)
                    new = jsonpickle.encode(v, unpicklable=False)
                    if old != new:
                        logging.error("Overwritting segment %s", k)
                allsegments[k] = v

        if allstructs != newstructs and set(allstructs.keys()) & set(newstructs.keys()):
            for k, v in newstructs.items():
                if k in allstructs:
                    old = jsonpickle.encode(allstructs[k], unpicklable=False)
                    new = jsonpickle.encode(v, unpicklable=False)
                    if old != new:
                        logging.error(f"Overwriting structure {k}")
        allstructs.update(newstructs)
        return allsegments, allstructs

    def _render_procedure(self, name, def_skip=0):
        """It takes a procedure name, and returns a C++ string containing for that procedure.

        :param name: The name of the procedure to be rendered
        :param def_skip: defaults to 0 (optional)
        :return: The body of the procedure and the segment it is in.
        """
        logging.info("     Generating proc %s", name)
        try:
            skip = def_skip
            self.__pushpop_count = 0
            self.temps_max = 0
            if g := self._context.get_global(name):
                self.proc = g
            else:
                logging.debug("No procedure named %s, trying label", name)
                off, src_proc, skip = self._context.get_offset(name)

                self.proc = proc_module.Proc(name)
                self.proc.stmts = copy(src_proc.stmts)
                self.proc.provided_labels = copy(src_proc.provided_labels)

            self._proc_addr.append((name, self.proc.offset))
            self.body = ""

            entry_point = ""
            if g := self._context.get_global(self._context.entry_point) and isinstance(g, op.label) and self.label_to_proc[g.name] == self.proc:
                entry_point = self._context.entry_point
            self.body += self.proc_strategy.function_header(name, entry_point)

            self.proc.visit(self, skip)

            labels = self.leave_unique_labels(self.proc.provided_labels)

            offsets = self.make_enums_and_labels(labels)
            self.body += self.renderer.produce_jump_table_c(offsets)

            segment = self.proc.segment
            self.proc = None

            if self.__pushpop_count != 0:
                logging.warning("push/pop balance = %d non zero at the exit of proc", self.__pushpop_count)
            return self.body, segment
        except (CrossJump, op.Unsupported) as e:
            logging.error("%s: ERROR: %s", name, e)
            self.__failed.append(name)
            raise
        except Exception as ex:
            logging.error(f"Exception {ex.args} for {name}")
            raise
        return None, None

    @staticmethod
    def isrelativejump(label: Expression) -> bool:
        result = (isinstance(label, lark.Tree) and \
        isinstance(label.children[0], lark.Tree) and label.children[0].data == "adddir" and \
        isinstance(label.children[0].children[0], lark.Tree) and label.children[0].children[0].data == "ptrdir3" and \
        isinstance(label.children[0].children[0].children[0], lark.Token) and label.children[0].children[0].children[0].type == "LABEL" and \
        label.children[0].children[0].children[0].value=="dol") or \
        (isinstance(label, lark.Tree) and \
         isinstance(label.children[0], lark.Tree) and label.children[0].data == "adddir" and \
        isinstance(label.children[0].children[0], lark.Tree) and label.children[0].children[0].data == "dollar")
        return result

    def dump_globals(self):
        name = self._namespace.lower() + ".list"
        logging.info(f" *** Generating globals listing {name}")

        jsonpickle.set_encoder_options("json", indent=2)
        with open(name, "w") as lst:
            lst.write("Segment:\n")
            for v in self._context.segments:
                lst.write(f"{v}\n")

            lst.write("\nLabels:\n")
            for _k, v in self._context.get_globals().items():
                if isinstance(v, op.label):
                    lst.write(f"{v.name}\n")

            lst.write("\nProcs:\n")
            for _k, v in self._context.get_globals().items():
                if isinstance(v, proc_module.Proc):
                    lst.write(f"{v.name} {v.offset}\n")

            lst.write("\nVars:\n")
            for _k, v in self._context.get_globals().items():
                if isinstance(v, op.var):
                    lst.write(f"{v.name} {v.offset}\n")

            lst.write(
                jsonpickle.encode((self._context.get_globals(), self._context.segments, self._context.structures)))


    def make_enums_and_labels(self, labels):
        offsets = []
        for k in labels:
            k = re.sub(r"\W", "_", k)
            offsets.append((k.lower(), self.renderer.cpp_mangle_label(k)))
        offsets = sorted(offsets, key=lambda t: t[1])
        return offsets

    def convert_asm_number_into_c(self, expr: str, radix: int=10) -> str:
        """It tryes to convert assembler number in any base to a C number string with the same base.

        :param result: The expression to convert
        :param radix: The radix of the number, defaults to 10 (optional)
        :return: The number in the specified radix.
        """
        try:
            from masm2c.parser import parse_asm_number
            radix, sign, value = parse_asm_number(expr, radix)

            result = self.renderer.produce_number_c(expr, radix, sign, value)
        except Exception as ex:
            logging.error("Failed to parse number %s radix %d %s", expr, radix, ex)
            result = expr

        return result


def guess_int_size(v: int) -> int:
    """It returns the number of bytes needed to store the given integer.

    :param v: integer
    :return: The size of the integer.
    """
    size = 0
    if v < 0:
        v = -2 * v - 1
    if v < 2**8:
        size = 1
    elif v < 2**16:
        size = 2
    elif v < 2**32:
        size = 4
    else:
        logging.error("too big number %d", v)

    logging.debug("guess_int_size %d", size)
    return size


def mangle_asm_labels(name: str) -> str:
    """Modifies assembler functions to be acceptable for other languages.

    :param name: the name of assembler the function
    :return: The name of the C function.
    """
    if name == "main":
        name = "asmmain"
    return name.replace("$", "_tmp").replace("?", "que")


class SkipCode(Exception):
    pass


class CrossJump(Exception):
    pass


class InjectCode(Exception):
    """A way to inject additional instructions during processing of some instruction."""

    def __init__(self, cmd) -> None:
        self.cmd = cmd
