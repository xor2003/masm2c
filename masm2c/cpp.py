# Masm2c S2S translator (initially based on SCUMMVM tasmrecover)
#
# Masm2c is the legal property of its developers, whose names
# are too numerous to list here. Please refer to the COPYRIGHT
# file distributed with this source distribution.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
import logging
import os
import re
from builtins import hex, range, str
from collections import OrderedDict

from lark import Tree, lark

from . import op
from . import proc as proc_module
from .Token import Token, Expression
from .enum import IndirectionType
from .gen import Gen, mangle_asm_labels, InjectCode
from .parser import ExprSizeCalculator, Vector
from .pgparser import OFFSETDIR, LABEL, PTRDIR, REGISTER, SEGMENTREGISTER, SEGOVERRIDE, SQEXPR, INTEGER, MEMBERDIR, \
    TopDownVisitor, Asm2IR


def flatten(s):
    if not s:
        return s
    if isinstance(s[0], list):
        return flatten(s[0]) + flatten(s[1:])
    return s[:1] + flatten(s[1:])


class SeparateProcStrategy:

    def __init__(self, renderer):
        self.renderer = renderer

    def produce_proc_start(self, name):
        return " // Procedure %s() start\n%s()\n{\n" % (name, self.renderer.cpp_mangle_label(name))

    def function_header(self, name, entry_point=''):
        header = """

 bool %s(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;
""" % self.renderer.cpp_mangle_label(name)

        if entry_point != '':
            header += """
    if (__disp == kbegin) goto %s;
""" % entry_point

        header += """
    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    %s:
    _begin:
""" % self.renderer.cpp_mangle_label(name)
        return header

    def write_declarations(self, procs, context):
        result = ""
        for p in sorted(procs):  # TODO only if used or public
            if p == 'mainproc' and not context.itislst:  # and not context.main_file:
                result += 'static '
            result += "bool %s(m2c::_offsets, struct m2c::_STATE*);\n" % self.renderer.cpp_mangle_label(p)

        for i in sorted(context.externals_procs):
            v = context.get_globals()[i]
            if v.used:
                result += f"extern bool {v.name}(m2c::_offsets, struct m2c::_STATE*);\n"

        result += """
bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state);
"""
        return result


class Cpp(Gen, TopDownVisitor):
    ''' Visitor which can produce C++ equivalents for asm instructions '''

    def __init__(self, context=None, outfile="", skip_output=None,
                 merge_data_segments=True):
        # proc_strategy = SingleProcStrategy()):
        '''

        :param context: pointer to Parser data
        :param outfile: Output filename
        :param skip_output: List of functions to skip at output
        :param proc_strategy: Strategy to Single/Separate functions
        '''
        super().__init__(context, outfile=outfile, skip_output=skip_output, merge_data_segments=merge_data_segments)
        self.proc_strategy = SeparateProcStrategy(self)
        self.renderer = self
        self._namespace = os.path.basename(outfile)
        self.__codeset = 'cp437'
        self._context = context

        self._indirection: IndirectionType = IndirectionType.VALUE

        # self.__current_size = 0
        # self._isjustlabel = False
        # self.__work_segment = 'ds'
        #
        self.__proc_queue = []
        self.__proc_done = []
        self.__failed = []
        self.__skip_output = skip_output
        # self.__translated = []
        self._proc_addr = []
        self.__used_data_offsets = set()
        self.__methods = []
        self.__pushpop_count = 0

        self.far = False
        self.size_changed = False
        self.needs_dereference = False
        self.itispointer = False

        self.struct_type = None

        self.dispatch = ''
        self.prefix = ''
        self._cmdlabel = ''

        self.isvariable = False
        self.islabel = False

        self.itisjump = False
        self.is_data = False

        self.__type_table = {op.DataType.NUMBER: self.produce_c_data_number,
                             op.DataType.ARRAY: self.produce_c_data_array,
                             op.DataType.ZERO_STRING: self.produce_c_data_zero_string,
                             op.DataType.ARRAY_STRING: self.produce_c_data_array_string,
                             op.DataType.OBJECT: self.produce_c_data_object
                             }

        self.element_size = -1


    def convert_label(self, token):
        name_original = mangle_asm_labels(token.children[0])
        token.children = name_original
        name = name_original.lower()
        logging.debug("convert_label name = %s indirection = %s", name, self._indirection)

        if self._indirection == IndirectionType.OFFSET:
            try:
                offset, _, _ = self._context.get_offset(name)
            except Exception:
                pass
            else:
                logging.debug("OFFSET = %s", offset)
                self._indirection = IndirectionType.VALUE
                self.__used_data_offsets.add((name, offset))
                return lark.Token('LABEL', "(dw)m2c::k" + name)
        return self.convert_label_(name)

    def convert_label_(self, name_original):
        name = name_original
        try:
            g = self._context.get_global(name)
        except Exception:
            # logging.warning("expand_cb() global '%s' is missing" % name)
            return name
        self.islabel = True
        if isinstance(g, op._equ):
            logging.debug("it is equ")
            #if not g.implemented:
            #    raise InjectCode(g)
            value = g.original_name
            #self.element_size = g.size
            logging.debug("equ: %s -> %s", name, value)
        elif isinstance(g, op._assignment):
            logging.debug("it is assignment")
            #if not g.implemented:
            #    raise InjectCode(g)
            value = g.original_name
            #self.element_size = g.size
            logging.debug("assignment %s = %s", name, value)
        elif isinstance(g, proc_module.Proc):
            logging.debug("it is proc")
            value = g.name  # For jump/call   TODO below check if it was needed
            '''
            if self._indirection != IndirectionType.OFFSET:
                logging.error("Invalid proc label usage proc %s offset %s", g.name, g.offset)
                value = "m2c::k" + g.name.lower()  # .capitalize()
            else:
                value = str(g.offset)
                self._indirection = IndirectionType.VALUE
            '''
        elif isinstance(g, op.var):
            logging.debug("it is var %s", g.size)
            self.variable_size = source_var_size = g.size
            if source_var_size:
                self.isvariable = True
            if self._middle_size == 0:  # TODO check
                self._middle_size = source_var_size
            if source_var_size == 0 and not g.issegment:
                raise Exception("invalid var '%s' size %u" % (name, source_var_size))
            if g.issegment:
                value = "seg_offset(%s)" % (name_original.lower())
                self._indirection = IndirectionType.VALUE
            else:
                self.needs_dereference = False
                self.itispointer = False
                if g.elements != 1:  # array
                    self.needs_dereference = True
                    self.itispointer = True
                    if not self.lea:
                        self._indirection = IndirectionType.POINTER
                if g.elements == 1 and self._isjustlabel and not self.lea and g.size == self.element_size:
                    # traceback.print_stack(file=sys.stdout)
                    value = g.name
                    self._indirection = IndirectionType.VALUE
                else:
                    if self._indirection == IndirectionType.POINTER:  # and self.isvariable:
                        value = g.name
                        if not self._isjustlabel:  # if not just single label: [a+3] address arithmetics
                            self.needs_dereference = True
                            self.itispointer = True
                            if g.elements == 1:  # array generates pointer himself
                                value = "&" + value  # get address of a scalar

                            if g.getsize() == 1:  # it is already a byte
                                value = "(%s)" % value
                            else:
                                value = "((db*)%s)" % value # cast to byte for address arihm
                                self.size_changed = True
                                self._middle_size = 1
                    elif self._indirection == IndirectionType.OFFSET:
                        value = "offset(%s,%s)" % (g.segment, g.name)
                        self.needs_dereference = False
                        self.itispointer = False
                    else:
                        value = name
                    if self._work_segment == 'cs':
                        self.body += '\tcs=seg_offset(' + g.segment + ');\n'
            # ?self.__indirection = 1
        elif isinstance(g, op.label):
            if self.is_data or not self.itisjump:
                value = "m2c::k" + g.name.lower()  # .capitalize()
            else:
                value = name
        else:
            source_var_size = g.getsize()
            if source_var_size == 0:
                raise Exception("invalid var '%s' size %u" % (name, source_var_size))
            if self._indirection in (IndirectionType.VALUE, IndirectionType.POINTER):  # x0r self.indirection == 1 ??
                value = "offsetof(struct Memory,%s)" % name_original
                if self._indirection == IndirectionType.POINTER:
                    self._indirection = IndirectionType.VALUE
            elif self._indirection == IndirectionType.OFFSET:
                value = str(g.offset)
                self._indirection = IndirectionType.VALUE
            else:
                raise Exception("invalid indirection %d name '%s' size %u" % (self._indirection, name, source_var_size))
        return value

    def render_data_c(self, segments):
        """
        It takes a list of DOS segments, and for each segment, it takes a list of data items, and for each data item, it
        produces a C++ assignment statement, a C++ extern statement, and a C++ reference statement

        :param segments: a dictionary of segments, where the key is the segment name and the value is the segment object
        :return: cpp_file, data_hpp_file, data_cpp_file, hpp_file
        """
        self.is_data = True

        cpp_file = ""
        data_hpp_file = ""
        data_cpp_file = ""
        hpp_file = ""
        for i in segments.values():
            #  Add segment address
            data_cpp_file += f"db& {i.name}=*((db*)&m2c::m+0x{i.offset:x});\n"
            hpp_file += f"extern db& {i.name};\n"

            for j in i.getdata():
                value, type_and_name, _ = self.produce_c_data_single_(j)

                type_and_name += ";\n"

                if not j.is_align():  # if align do not assign it
                    #  mycopy(bb, {'1','2','3','4','5'});
                    #  caa=3;
                    m = re.match(r'^(\w+)\s+(\w+)(\[\d+\])?;\n', type_and_name)
                    if not m:
                        logging.error(f'Failed to parse {value} {type_and_name}')
                    name = m.group(2)

                    type_and_size = re.sub(r'^(?P<type>\w+)\s+\w+(\[\d+\])?;\n', r'\g<type> tmp999\g<2>', type_and_name)

                    if name.startswith('dummy') and value == '0':
                        value = ''
                    elif m.group(2):  # if array
                        if value == '{}':
                            value = ''
                        else:
                            value = f'    {{{type_and_size}={value};MYCOPY({name})}}'
                    else:
                        # value = f'    {name}={value};'
                        value = f'    {{{type_and_size}={value};MYCOPY({name})}}'

                    # char (& bb)[5] = group.bb;
                    # int& caa = group.aaa;
                    # references
                    _reference_in_data_cpp = self._generate_dataref_from_declaration_c(type_and_name)
                    # externs
                    _extern_in_hpp = self._generate_extern_from_declaration_c(type_and_name)

                    if value:
                        real_seg, real_offset = j.getrealaddr()
                        if real_seg:
                            value += f' // {real_seg:04x}:{real_offset:04x}'
                            type_and_name = type_and_name[:-1] + f' // {real_seg:04x}:{real_offset:04x}\n'
                        value += "\n"
                    # c += " // " + j.getlabel() + "\n"  # TODO can put original_label

                    cpp_file += value  # cpp source - assigning
                    hpp_file += _extern_in_hpp  # extern for header

                    data_cpp_file += _reference_in_data_cpp  # reference in _data.cpp
                data_hpp_file += type_and_name  # headers in _data.h

        self.is_data = False
        return cpp_file, data_hpp_file, data_cpp_file, hpp_file

    def _generate_extern_from_declaration_c(self, _hpp):
        """
        It takes a C++ declaration and returns a extern declaration to the same

        :param _hpp: The C++ header file
        :return: The extern declaration of the function or variable.
        """
        _extern = re.sub(r'^(\w+)\s+([\w\[\]]+)(\[\d+\]);', r'extern \g<1> (& \g<2>)\g<3>;', _hpp)
        _extern = re.sub(r'^(\w+)\s+([\w\[\]]+);', r'extern \g<1>& \g<2>;', _extern)
        return _extern

    def _generate_dataref_from_declaration_c(self, _hpp):
        """
        It takes a C++ declaration and returns a reference to the same variable

        :param _hpp: declaration string
        :return: The reference to the same data
        """
        _reference = re.sub(r'^(\w+)\s+([\w\[\]]+)(\[\d+\]);',
                            r'\g<1> (& \g<2>)\g<3> = m2c::m.\g<2>;', _hpp)
        _reference = re.sub(r'^(\w+)\s+([\w\[\]]+);', r'\g<1>& \g<2> = m2c::m.\g<2>;', _reference)
        return _reference

    def memberdir(self, tree):
        return [self.convert_member_(tree.children)]

    def convert_member(self, token):
        """
        It converts Token with access to assembler structure member and converts to similar in C++

        :param token: The token to be converted
        :return: The value of the member.
        """
        logging.debug("name = %s indirection = %s", token, self._indirection)
        value = token
        label = [l.lower() for l in Token.find_tokens(token, LABEL)]
        return self.convert_member_(label)

    def convert_member_(self, label):
        self.struct_type = None
        value = ".".join(label)

        if self._indirection == IndirectionType.OFFSET:
            try:
                g = self._context.get_global(label[0])
            except:
                pass
            else:
                if isinstance(g, op.var):
                    value = f'offset({g.segment},{".".join(label)})'
                elif isinstance(g, op.Struct):
                    value = f'offsetof({label[0]},{".".join(label[1:])})'
                elif isinstance(g, (op._equ, op._assignment)):
                    value = f'({label[0]})+offsetof({g.original_type},{".".join(label[1:])})'
                else:
                    raise Exception('Not handled type ' + str(type(g)))
                self._indirection = IndirectionType.VALUE
                return value # Token('memberdir', value)

        try:
            g = self._context.get_global(label[0])
        except KeyError:
            logging.error("global '%s' is missing", label)
            return ".".join(label)

        if isinstance(g, (op._equ, op._assignment)):
            logging.debug(str(g))
            if not g.implemented:
                raise InjectCode(g)
            if self._isjustlabel:
                value = '.'.join(label)
            else:
                self.struct_type = g.value.original_type
                self.needs_dereference = True
                self.itispointer = False
                self._need_pointer_to_member = label
                value = ''
                #value = f"{label[0]}))->{'.'.join(label[1:])}"
            logging.debug("equ: %s -> %s", label[0], value)
        elif isinstance(g, op.var):

            source_var_size = self.calculate_member_size(label)
            self.variable_size = source_var_size
            if source_var_size:
                self.isvariable = True

            logging.debug("it is var %s", source_var_size)
            if self._middle_size == 0:
                self._middle_size = source_var_size

            self.isvariable = True
            self.islabel = True

            if source_var_size == 0:
                raise Exception(f"invalid var {label} size {source_var_size}")
            self.needs_dereference = False
            self.itispointer = False
            if g.elements != 1:
                self.needs_dereference = True
                self.itispointer = True
            if g.elements == 1 and self._isjustlabel and not self.lea and source_var_size == self._middle_size:
                # traceback.print_stack(file=sys.stdout)
                value = '.'.join(label)
                self._indirection = IndirectionType.VALUE
            else:
                if self._indirection == IndirectionType.POINTER: # ? and self.isvariable:
                    value = '.'.join(label)
                    if not self._isjustlabel:  # if not just single label
                        self.needs_dereference = True
                        self.itispointer = True
                        if g.elements == 1:  # array generates pointer himself
                            value = "&" + value

                        if g.getsize() == 1:  # it is already a byte
                            value = "(%s)" % value
                        else:
                            value = "((db*)%s)" % value
                            self.size_changed = True
                elif self._indirection == IndirectionType.OFFSET and self.isvariable:
                    value = "offset(%s,%s)" % (g.segment, '.'.join(label))
                if self._work_segment == 'cs':
                    self.body += '\tcs=seg_offset(' + g.segment + ');\n'
            # ?self.__indirection = 1
            #if value == token:
            #    logging.error('value not yet assigned')
        elif isinstance(g, op.Struct):
            #if self._isjustmember:
            value = f'offsetof({label[0]},{".".join(label[1:])})'

        if self._indirection == IndirectionType.POINTER and self.needs_dereference and self.struct_type:

            self._ismember = True

            #value = f'(({self.struct_type}*)raddr({self._work_segment},{value}'
            self.needs_dereference = False

        #if size == 0:
        #    raise Exception("invalid var '%s' size %u" % (str(label), size))
        return value

    def convert_sqbr_reference(self, segment: str, expr, destination: bool, size: int, islabel: bool,
                               lea: bool = False):
        if not lea or destination:
            if not self.islabel or not self.isvariable:
                self.needs_dereference = True
                self.itispointer = True
                if size == 1:
                    expr = f"raddr({segment},{expr})"
                elif size == 2:
                    expr = f"(dw*)(raddr({segment},{expr}))"
                elif size == 4:
                    expr = f"(dd*)(raddr({segment},{expr}))"
                elif size == 8:
                    expr = f"(dq*)(raddr({segment},{expr}))"
                else:
                    logging.error(f"~{expr}~ invalid size {size}")
                    expr = f"raddr({segment},{expr})"
            elif self.size_changed:  # or not self._isjustlabel:
                    expr = Cpp.render_new_pointer_size(self.itispointer, expr, size)
                    self.size_changed = False

            logging.debug(f"expr: {expr}")
        return expr

    @staticmethod
    def render_new_pointer_size(itispointer: bool, expr, target_size: int):
        """
        :param expr: the expression to be rendered
        :param target_size: the new size of the pointer
        :return: The expression with the new size.
        """
        if itispointer:
            if target_size == 1:
                expr = f"(db*)({expr})"
            elif target_size == 2:
                expr = f"(dw*)({expr})"
            elif target_size == 4:
                expr = f"(dd*)({expr})"
            elif target_size == 8:
                expr = f"(dq*)({expr})"
            else:
                logging.error(f"~{expr}~ unknown size {target_size}")
        else:
            if target_size == 1:
                expr = f"*(db*)(&{expr})"
            elif target_size == 2:
                expr = f"*(dw*)(&{expr})"
            elif target_size == 4:
                expr = f"*(dd*)(&{expr})"
            elif target_size == 8:
                expr = f"*(dq*)(&{expr})"
            else:
                logging.error(f"~{expr}~ unknown size {target_size}")

        return expr

    def tokens_to_string(self, expr):
        '''
        Convert remaining tokens to make it simple string
        :param expr: tokens
        :return: string
        '''
        if isinstance(expr, list):
            result = ''
            for i in expr:
                # TODO hack to handle ')register'
                if len(result) and result[-1] == ')' and isinstance(i, Token) and i.data == 'register':
                    result += '+'
                res = self.tokens_to_string(i)
                res = re.sub(r'([Ee])\+', r'\g<1> +',
                             res)  # prevent "error: unable to find numeric literal operator 'operator""+" 0x0E+vecl_1c0
                res = res.replace('+)', ')')  # TODO hack
                result += res
            return result
        elif isinstance(expr, Tree):

            if expr.data == 'STRING':
                m = re.match(r'^[\'\"](....)[\'\"]$', expr.children)  # char constants 'abcd'
                if m:
                    ex = m.group(1)
                    expr.children = '0x'
                    for i in range(0, 4):
                        # logging.debug("constant %s %d" %(ex,i))
                        ss = str(hex(ord(ex[i])))
                        # logging.debug("constant %s" %ss)
                        expr.children += ss[2:]
                expr.children = expr.children.replace('\\', '\\\\')  # escape c \ symbol

            return self.tokens_to_string(expr.children)
        return expr

    def render_instruction_argument_(self, expr, def_size: int = 0, destination: bool = False, lea: bool = False):
        '''
        Convert instruction argument Tokens into C
        :param expr: argument Tokens
        :param def_size: Preliminary calculate size in bytes
        :param destination: if it is destination argument
        :param lea: if it is lea operation
        :return: Argument in C format as string
        '''
        logging.debug("%s", expr)

        expr = Token.remove_tokens(expr, ['expr'])  # no need expr token any more
        origexpr = expr  # save original expression before we will change it
        self._work_segment = "ds"  # default work segment is ds
        self._middle_size = 0  # current size of argument is not yet found
        self.size_changed = False
        self.needs_dereference = False
        self.itispointer = False
        indirection: IndirectionType = IndirectionType.VALUE
        size = self.calculate_size(expr) if def_size == 0 else def_size  # calculate size if it not provided

        # calculate the segment register
        segoverride = Token.find_tokens(expr, SEGOVERRIDE)
        sqexpr = Token.find_tokens(expr, SQEXPR)
        if sqexpr:  # if [] then we want to get data using memory pointer
            indirection = IndirectionType.POINTER
        if segoverride:  # check if there is segment override
            expr = Token.remove_tokens(expr, [SEGMENTREGISTER])

        offsetdir = Token.find_tokens(expr, OFFSETDIR)
        if offsetdir:  # if 'offset' then we want just address of data
            indirection = IndirectionType.OFFSET
            expr = offsetdir

        ptrdir = Token.find_tokens(expr, PTRDIR)
        if ptrdir:  # word/byte ptr means we want to get data using memory pointer
            indirection = IndirectionType.POINTER

        if ptrdir or offsetdir or segoverride:  # no need it anymore. simplify
            expr = Token.remove_tokens(expr, [PTRDIR, OFFSETDIR, SEGOVERRIDE])

        # if it is a destination argument and there is only number then we want to put data using memory pointer
        # represented by integer
        if isinstance(expr, list) and len(expr) == 1 and isinstance(expr[0], Token) and expr[
            0].data == INTEGER and segoverride:
            indirection = IndirectionType.POINTER
            self.needs_dereference = True

        # Simplify by removing square brackets
        if sqexpr:
            expr, _ = Token.remove_squere_bracets(expr)

        # check if we pointing some member of structure
        memberdir = Token.find_tokens(expr, MEMBERDIR)
        # get struct name or instance name and member names
        islabel = Token.find_tokens(expr, LABEL)
        self.isvariable = False  # only address or variable
        if (islabel or memberdir) and not offsetdir:
            if memberdir:
                member_size = self.calculate_member_size(Token(MEMBERDIR, memberdir))
                if member_size:
                    self.isvariable = True
                    size = member_size
                    indirection = IndirectionType.POINTER
            elif islabel:
                for i in islabel:  # Strange !?
                    label_size = self.calculate_size(Token(LABEL, i))
                    if label_size:
                        self.isvariable = True
                        size = label_size
                        indirection = IndirectionType.POINTER
                        break
        if lea:  # If lea operation it is the same as getting offset
            indirection = IndirectionType.OFFSET

        if indirection == IndirectionType.POINTER and not segoverride:
            regs = Token.find_tokens(expr, REGISTER)  # if it was registers used: bp, sp
            if regs and any((i in {'bp', 'ebp', 'sp', 'esp'} for i in regs)):  # TODO doublecheck
                self._work_segment = "ss"  # and segment is not overriden means base is "ss:"
                self.isvariable = False
        if segoverride:  # if it was segment override then use provided value
            self._work_segment = segoverride[0][0].children[0]

        self._middle_size = size
        size_ovrr_by_ptr = size  # setting initial value
        if ptrdir:  # byte/word/struct ptr. get override type size
            value = ptrdir[0]
            # logging.debug('get_size res 1')
            size_ovrr_by_ptr = self._context.typetosize(value)  # size overriden by ptr
            if size_ovrr_by_ptr != size:
                self.size_changed = True
            else:
                origexpr = Token.remove_tokens(origexpr, [PTRDIR, SQEXPR])
                if isinstance(origexpr, list) and len(origexpr) == 1:
                    origexpr = origexpr[0]

        # if just "label" or "[label]" or member
        self._isjustlabel = (isinstance(origexpr, Token) and origexpr.data == LABEL) \
                            or (isinstance(origexpr, Token) and origexpr.data == SQEXPR \
                                and isinstance(origexpr.children, Token) and origexpr.children.data == LABEL) \
                            or (isinstance(origexpr, Token) and origexpr.data == MEMBERDIR)
        self._isjustmember = isinstance(origexpr, Token) and origexpr.data == MEMBERDIR

        self._indirection = indirection

        if memberdir:
            expr = Token.find_and_replace_tokens(expr, MEMBERDIR, self.convert_member)
            if self._indirection == IndirectionType.POINTER and self.needs_dereference and self.struct_type:

                # TODO A very hacky way to
                # put registers and numbers first since asm have byte aligned pointers
                # in comparison to C's type aligned
                registers = Token.find_tokens(expr, 'register')
                integers = Token.find_tokens(expr, 'integer')
                expr = Token.remove_tokens(expr, ['register', 'integer'])
                expr = self.tokens_to_string(expr)
                while len(expr) and expr[0] == '+':
                    expr = expr[1:]
                while len(expr) > 2 and expr[0] == '(' and expr[-1] == ')':
                    expr = expr[1:-1]
                if integers:
                    expr = '+'.join(integers) + '+' + expr
                if registers:
                    expr = '+'.join(registers) + '+' + expr
                expr = expr.replace('++', '+').replace('+-', '-')

                expr = [f'(({self.struct_type}*)raddr({self._work_segment},'] + [expr]
                self.needs_dereference = False
        else:
            if islabel:
                # assert(len(islabel) == 1)
                expr = Token.find_and_replace_tokens(expr, LABEL, self.convert_label)
        indirection = self._indirection
        if self._middle_size != 0 and size != self._middle_size and not self.size_changed:
            size = self._middle_size

        if self.size_changed:
            size = size_ovrr_by_ptr

        expr = self.tokens_to_string(expr)

        if not memberdir and indirection == IndirectionType.POINTER and (not self._isjustlabel or self.size_changed):
            expr = self.convert_sqbr_reference(self._work_segment, expr, destination, size, islabel, lea=lea)

        if self.size_changed:  # or not self._isjustlabel:
            expr = Cpp.render_new_pointer_size(self.itispointer, expr, size)
            self.size_changed = False

        if indirection == IndirectionType.POINTER and self.needs_dereference:
            self.needs_dereference = False
            if expr[0] == '(' and expr[-1] == ')':
                expr = "*%s" % expr
            else:
                expr = "*(%s)" % expr

        return expr

    def jump_post(self, expr):
        name = self.render_jump_label(expr)
        name, far = self.convert_jump_label(name)
        if 'far' in expr.mods:
            far = True
        elif 'near' in expr.mods:
            far = False

        hasglobal = self._context.has_global(name) if isinstance(name, str) else False
        if not hasglobal or isinstance(self._context.get_global(name), op.var):
            # jumps feat purpose:
            # * in sub __dispatch_call - for address based jumps or grouped subs
            # * direct jumps

            # how to handle jumps:
            # subs - direct jump to internal sub (maybe merged) - directly
            # labels - directly
            # offset - internal sub __dispatch_call disp=cs + offset
            #   register
            #   exact value
            # seg:offset - in sub __dispatch_call disp= seg:offset ?
            # ret += f"__disp={dst};\n"
            # dst = "__dispatch_call"
            # if self._context.has_global(name):
            # name = 'm2c::k'+name
            self.dispatch += f'__disp={name};\n'
            name = "__dispatch_call"
            # logging.debug(f'not sure if handle it properly {name}')

        return name, far

    def convert_jump_label(self, name):  # TODO Remove this!!!
        '''
        Convert argument tokens which for jump operations into C string
        :param name: Tokens
        :return: C string
        '''
        logging.debug("jump_to_label(%s)", name)

        indirection = -5
        '''
        #if isinstance(name, Token) and name.data == 'register':
        #    name = name.children
        #    indirection = IndirectionType.VALUE  # based register value

        #labeldir = Token.find_tokens(name, 'LABEL')
        #if labeldir:
        #    from masm2c.parser import Parser
        #    labeldir[0] = Parser.mangle_label(self.cpp_mangle_label(labeldir[0]))
        if self._context.has_global(name):
                g = self._context.get_global(name)
                if isinstance(g, op.var):
                    indirection = IndirectionType.POINTER  # []
                #elif isinstance(g, (op.label, proc_module.Proc)):
                #    indirection = IndirectionType.OFFSET  # direct using number
        #    else:
        #        name = labeldir[0]

        ptrdir = Token.find_tokens(name, 'ptrdir')
        if ptrdir:
            if any(isinstance(x, str) and x.lower() in ['near', 'far', 'short'] for x in ptrdir):
                indirection = IndirectionType.OFFSET  #
            else:
                indirection = IndirectionType.POINTER

        sqexpr = Token.find_tokens(name, 'sqexpr')
        if sqexpr:
            indirection = IndirectionType.POINTER

        if indirection == IndirectionType.POINTER:
            name = self.render_instruction_argument(name)

        if indirection == IndirectionType.OFFSET and labeldir:
            name = labeldir[0]

        logging.debug("label %s", name)
        '''

        hasglobal = False
        far = False
        if isinstance(name, str) and self._context.has_global(name):
            hasglobal = True
            g = self._context.get_global(name)
            if isinstance(g, proc_module.Proc):
                far = g.far


            # if hasglobal:
            elif isinstance(g, op.label):
                far = g.far  # make far calls to far procs
        '''
        if ptrdir:
            if any(isinstance(x, str) and x.lower() == 'far' for x in ptrdir):
                far = True
            elif any(isinstance(x, str) and x.lower() == 'near' for x in ptrdir):
                far = False
        '''
        return (name, far)

    def _label(self, name, isproc):
        if isproc:
            raise RuntimeError('Should not happen anymore probably')
            self._cmdlabel = self.proc_strategy.produce_proc_start(name)
        else:
            self._cmdlabel = "%s:\n" % self.cpp_mangle_label(name)
        return ''

    def _call(self, expr):
        logging.debug("cpp._call(%s)", expr)
        ret = ""
        if expr.ptr_size == 0:
            expr.ptr_size = 2
        size = self.calculate_size(expr)
        name = self.render_jump_label(expr)
        dst, far = self.convert_jump_label(name)
        if size == 4 or 'far' in expr.mods:
            far = True
        elif 'near' in expr.mods:
            far = False

        disp = '0'
        hasglobal = self._context.has_global(dst) if isinstance(dst, str) else None
        if hasglobal:
            g = self._context.get_global(dst)
            if isinstance(g, op.label) and not g.isproc and not dst in self._procs and not dst in self.grouped:
                # far = g.far  # make far calls to far procs
                disp = f"m2c::k{dst}"
                dst = self.label_to_proc[g.name]
            elif isinstance(g, op.var):
                disp = dst
                dst = "__dispatch_call"

            # calls feat purpose:
        # * grouped sub wrapper, exact subs  - direct name for external references
        #   intern sub jump dispatcher - for grouped subs
        # * global __dispatch_call - for address based calls CALL[es:bx]

        # how to handle call instr:
        # subs - (disp = 0) direct calls CALL(sub_0123)
        # labels
        #    in sub - self call the sub( with disp= klabel) ? or global dispatcher?
        #    other sub - __dispatch_call the sub( with disp= klabel)
        # offset - __dispatch_call disp=cs + offset
        #   register
        #   memory reference
        # seg:offset  - __dispatch_call disp= seg:offset
        # elif isinstance(g, proc_module.Proc) or dst in self.__procs or dst in self.grouped:
        #    self.body += f"__disp=0;\n"
        else:
            result = dst, "__dispatch_call"
            disp, dst = result
            # self.body += addtobody

        dst = self.cpp_mangle_label(dst)

        if far:
            ret += f"CALLF({dst},{disp})"
        else:
            ret += f"CALL({dst},{disp})"
        return ret

    def _ret(self, src):
        if src == []:
            self.a = '0'
        else:
            self.a = self.render_instruction_argument(src[0])
        return "RETN(%s)" % self.a

    def _retf(self, src):
        if src == []:
            self.a = '0'
        else:
            self.a = self.render_instruction_argument(src[0])
        return "RETF(%s)" % self.a

    def _xlat(self, src):
        if not src:
            return "XLAT"
        self.a = self.render_instruction_argument(src[0])[2:-1]
        return "XLATP(%s)" % self.a

    def parse2(self, dst, src):
        dst_size, src_size = self.calculate_size(dst), self.calculate_size(src)
        if dst_size == 0:
            if src_size == 0:
                logging.debug("parse2: %s %s both sizes are 0", dst, src)
                # raise Exception("both sizes are 0")
            size = src_size
            dst_size = src_size
            # dst.element_size = dst_size
        if src_size == 0:
            src_size = dst_size
            size = dst_size
            # src.element_size = src_size

        if src.indirection == IndirectionType.POINTER and src.element_size == 0 and dst_size and not src.ptr_size:
            src.ptr_size = dst_size
        if dst.indirection == IndirectionType.POINTER and dst.element_size == 0 and src_size and not dst.ptr_size:
            dst.ptr_size = src_size
        dst = self.render_instruction_argument(dst, dst_size, destination=True)
        src = self.render_instruction_argument(src, src_size)
        return dst, src

    def _add(self, dst, src):
        self.a, self.b = self.parse2(dst, src)
        # if self.d in ['sp', 'esp'] and check_int(self.s):
        #    self.__pushpop_count -= int(self.s)
        return "ADD(%s, %s)" % (self.a, self.b)

    def _mul(self, src):
        size = 0
        for i in src:
            if size == 0:
                size = self.calculate_size(i)
            else:
                break
        res = [self.render_instruction_argument(i, size) for i in src]
        if size == 0:
            size = self._middle_size
        return "MUL%d_%d(%s)" % (len(src), size, ",".join(res))

    def _imul(self, src):
        size = 0
        for i in src:
            if size == 0:
                size = self.calculate_size(i)
            else:
                break
        res = [self.render_instruction_argument(i, size) for i in src]
        if size == 0:
            size = self._middle_size
        return "IMUL%d_%d(%s)" % (len(src), size, ",".join(res))

    def _div(self, src):
        self.a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        return "DIV%d(%s)" % (size, self.a)

    def _idiv(self, src):
        self.a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        return "IDIV%d(%s)" % (size, self.a)

    def _jz(self, label):
        if self.isrelativejump(label):
            return "{;}"
        label, _ = self.jump_post(label)  # TODO
        return "JZ(%s)" % label

    def _jnz(self, label):
        label, _ = self.jump_post(label)
        return "JNZ(%s)" % label

    def _jbe(self, label):
        label, _ = self.jump_post(label)
        return "JBE(%s)" % label

    def _ja(self, label):
        label, far = self.jump_post(label)
        return "JA(%s)" % label

    def _jc(self, label):
        label, far = self.jump_post(label)
        return "JC(%s)" % label

    def _jnc(self, label):
        label, far = self.jump_post(label)
        return "JNC(%s)" % label

    '''
    def _push(self, regs):
        p = ""
        for r in regs:
            if self.get_size(r):
                self.__pushpop_count += 2
                r = self.expand(r)
                p += "PUSH(%s)" % (r)
        return p

    def _pop(self, regs):
        p = ""
        for r in regs:
            self.__pushpop_count -= 2
            r = self.expand(r)
            p += "POP(%s)" % r
        return p
    '''

    def _rep(self):
        # return "\tREP\n"
        self.prefix = '\tREP '
        return ''

    def _cmpsb(self):
        return "CMPSB"

    def _lodsb(self):
        return "LODSB"

    def _lodsw(self):
        return "LODSW"

    def _lodsd(self):
        return "LODSD"

    def _stosb(self):
        return "STOSB"

    def _stosw(self):
        return "STOSW"

    def _stosd(self):
        return "STOSD"

    def _movsb(self):
        return "MOVSB"

    def _movsw(self):
        return "MOVSW"

    def _movsd(self):
        return "MOVSD"

    def _scasb(self):
        return "SCASB"

    def _scasw(self):
        return "SCASW"

    def _scasd(self):
        return "SCASD"

    def _scas(self, src):
        self.a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        srcr = Token.find_tokens(src, REGISTER)
        return "SCAS(%s,%s,%d)" % (self.a, srcr[0], size)

    def save_cpp_files(self, fname):
        self.merge_procs()
        cpp_assigns, _, _, cpp_extern = self.render_data_c(self._context.segments)

        header_id = f"__M2C_{self._namespace.upper().replace('-', '_').replace('.', '_')}_STUBS_H__"

        banner = """/* THIS IS GENERATED FILE */

        """

        cpp_fname = f"{self._namespace.lower()}.cpp"
        header_fname = f"{self._namespace.lower()}.h"

        logging.info(f' *** Generating output files in C++ {cpp_fname} {header_fname}')

        cpp_file = open(cpp_fname, "wt", encoding=self.__codeset)
        hpp_file = open(header_fname, "wt", encoding=self.__codeset)

        cpp_file.write(f"""{banner}
        #include \"{header_fname}\"

{self.render_function_wrappers_c()}
{self.render_entrypoint_c()}
{self.write_procedures(banner, header_fname)}
{self.produce_global_jump_table(list(self._context.get_globals().items()), self._context.itislst)}

        #include <algorithm>
        #include <iterator>
        #ifdef DOSBOX_CUSTOM
        #include <numeric>

         #define MYCOPY(x) {{m2c::set_type(x);m2c::mycopy((db*)&x,(db*)&tmp999,sizeof(tmp999),#x);}}

         namespace m2c {{
          void   Initializer()
        #else
         #define MYCOPY(x) memcpy(&x,&tmp999,sizeof(tmp999));
         namespace {{
          struct Initializer {{
           Initializer()
        #endif
        {{
        {cpp_assigns}
        }}
        #ifndef DOSBOX_CUSTOM
          }};
         static const Initializer i;
        #endif
        }}
        """)
        cpp_file.close()

        hpp_file.write(f"""{banner}
#ifndef {header_id}
#define {header_id}

#include "asm.h"

{self.produce_structures(self._context.structures)}
{cpp_extern}
{self.produce_label_offsets()}
{self.proc_strategy.write_declarations(self._procs + list(self.grouped), self._context)}
{self.produce_externals(self._context)}
#endif
""")

        hpp_file.close()

        self.__methods += self.__failed
        done, failed = len(self.__proc_done), len(self.__failed)
        logging.info("%d ok, %d failed of %d, %3g%% translated", done, failed, done + failed,
                     100.0 * done / (done + failed))

        logging.info("\n".join(self.__failed))

        self.write_segment_file(self._context.segments, self._context.structures, fname)

    def write_procedures(self, banner, header_fname):
        cpp_file_text = ''
        last_segment = None
        cpp_segment_file = None
        for name in self._procs:
            proc_text, segment = self._render_procedure(name)
            if self._context.itislst and segment != last_segment:  # If .lst write to separate segments. Open new if changed
                last_segment = segment
                if cpp_segment_file:
                    cpp_segment_file.close()

                cpp_segment_fname = f"{self._namespace.lower()}_{segment}.cpp"
                logging.info(f' *** Generating output file in C++ {cpp_segment_fname}')
                cpp_segment_file = open(cpp_segment_fname, "wt", encoding=self.__codeset)
                cpp_segment_file.write(f'''{banner}
#include "{header_fname}"

                ''')

            if cpp_segment_file:
                cpp_segment_file.write(f"{proc_text}\n")
            else:
                cpp_file_text += f"{proc_text}\n"
            self.__proc_done.append(name)
            self.__methods.append(name)
        if cpp_segment_file:
            cpp_segment_file.close()

        return cpp_file_text

    def render_entrypoint_c(self):
        entry_point_text = ''
        if self._context.main_file:
            g = self._context.get_global(self._context.entry_point)
            if isinstance(g, op.label) and self._context.entry_point not in self.grouped:
                entry_point_text = f"""
                 bool {self._context.entry_point}(m2c::_offsets, struct m2c::_STATE* _state){{return {self.label_to_proc[g.name]}(m2c::k{self._context.entry_point}, _state);}}
                """

            entry_point_text += f"""namespace m2c{{ m2cf* _ENTRY_POINT_ = &{self._context.entry_point};}}
        """
        return entry_point_text

    def render_function_wrappers_c(self):
        wrappers = ""
        for p in sorted(self.grouped):
            wrappers += f"""
 bool {p}(m2c::_offsets, struct m2c::_STATE* _state){{return {self.groups[p]}(m2c::k{p}, _state);}}
"""
        return wrappers

    def convert_segment_files_into_datacpp(self, asm_files):
        """
        It reads .seg files, and writes the data segments to _data.cpp/h file

        :param asm_files: A list of the assembly files
        """
        self.write_data_segments_cpp(*self.read_segment_files(asm_files))

    def write_data_segments_cpp(self, segments, structures):
        """
        It writes the _data.cpp and _data.h files

        :param segments: a list of segments, each segment is a list of data items
        :param structures: a list of structures that are defined in the program
        """
        logging.info(" *** Producing _data.cpp and _data.h files")
        _, data_h, data_cpp_reference, _ = self.render_data_c(segments)
        fname = "_data.cpp"
        header = "_data.h"
        with open(fname, "wt", encoding=self.__codeset) as fd:
            fd.write(f'''#include "_data.h"
namespace m2c{{

struct Memory m;

struct Memory types;

db(& stack)[STACK_SIZE]=m.stack;
db(& heap)[HEAP_SIZE]=m.heap;
}}
{data_cpp_reference}

''')

        with open(header, "wt", encoding=self.__codeset) as hd:
            hd.write('''
#ifndef ___DATA_H__
#define ___DATA_H__
#include "asm.h"
''' + self.produce_structures(structures) + self.produce_data(data_h) + '''
#endif
''')

    def produce_label_offsets(self):
        labeloffsets = """namespace m2c{
void   Initializer();
static const dd kbegin = 0x1001;
"""
        i = 0x1001
        for k, v in list(self._context.get_globals().items()):
            # if isinstance(v, (op.label, proc_module.Proc)) and v.used:
            if isinstance(v, (op.label, proc_module.Proc)):
                k = re.sub(r'[^A-Za-z0-9_]', '_', k).lower()
                i += 1
                if v.real_offset or v.real_seg:
                    i = v.real_seg * 0x10000 + v.real_offset
                labeloffsets += "static const dd k%s = 0x%x;\n" % (k, i)
        labeloffsets += "}\n"
        return labeloffsets

    def produce_structures(self, strucs):
        structures = "\n"
        if len(strucs):
            structures += f"""#pragma pack(push, 1)"""
        for name, v in strucs.items():
            type = 'struct' if v.gettype() == op.Struct.Type.STRUCT else 'union'
            structures += f"""
{type} {name} {{
"""
            for member in v.getdata().values():
                structures += f"  {member.data_type} {member.label};\n"
            structures += """};
"""
        if len(strucs):
            structures += f"""
#pragma pack(pop)

"""
        return structures

    def produce_data(self, hdata_bin):
        data_head = """
#pragma pack(push, 1)
namespace m2c{
struct Memory{
"""
        data_head += "".join(hdata_bin)
        data_head += '''
#ifdef DOSBOX_CUSTOM
    db filll[1024*1024*16];
#endif
                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                '''
        data_head += """};
}
#pragma pack(pop)
"""
        return data_head

    def produce_externals(self, context):
        data = '\n'
        for i in context.externals_vars:
            v = context.get_globals()[i]
            if v.used:
                data += f"extern {v.original_type} {v.name};\n"
        return data

    def _lea(self, dst, src):
        self.lea = True
        src.indirection = IndirectionType.OFFSET
        src.mods.add('lea')
        dst.mods.add('lea')
        self.a, self.b = self.parse2(dst, src)
        #self.a = self.render_instruction_argument(dst, destination=True, lea=True)
        #self.b = self.render_instruction_argument(src, lea=True)
        r = "%s = %s" % (self.a, self.b)
        self.lea = False
        return r

    def _movs(self, dst, src):
        size = self.calculate_size(dst)
        dstr, srcr = Token.find_tokens(dst, REGISTER), Token.find_tokens(src, REGISTER)
        self.a, self.b = self.parse2(dst, src)
        return "MOVS(%s, %s, %s, %s, %d)" % (self.a, self.b, dstr[0], srcr[0], size)

    def _repe(self):
        # return "\tREPE\n"
        self.prefix = '\tREPE '
        return ''

    def _repne(self):
        # return "\tREPNE\n"
        self.prefix = '\tREPNE '
        return ''

    def _lods(self, src):
        self.a = self.render_instruction_argument(src)
        size = self.calculate_size(src)
        srcr = Token.find_tokens(src, REGISTER)
        return "LODS(%s,%s,%d)" % (self.a, srcr[0], size)

    def _leave(self):
        return "LEAVE"  # MOV(esp, ebp) POP(ebp)

    def _int(self, dst):
        self.a = self.render_instruction_argument(dst)
        return "_INT(%s)" % self.a

    def _instruction0(self, cmd):
        return "%s" % (cmd.upper())

    def _instruction1(self, cmd, dst) -> str:
        self.a = self.render_instruction_argument(dst)
        return "%s(%s)" % (cmd.upper(), self.a)

    def render_instruction_argument(self, expr, def_size: int = 0, destination: bool = False, lea: bool = False):
        # def_size = expr.size()
        if destination:
            expr.mods.add("destination")
        if lea:
            expr.mods.add("lea")
        if def_size == 0 and expr.element_size == 0 and expr.indirection != IndirectionType.POINTER:
            calc = ExprSizeCalculator(init=Vector(0, 0), context=self._context)
            def_size, _ = calc.visit(expr)  # , result=0)

        if def_size and expr.element_size == 0:
            expr.element_size = def_size
        ir2cpp = IR2Cpp(self._context)
        ir2cpp.lea = self.lea
        ir2cpp._indirection = expr.indirection
        ir2cpp.itisjump = self.itisjump
        result = "".join(ir2cpp.visit(expr))
        self.size_changed = ir2cpp.size_changed
        #self.islabel=False
        #self.isvaraible=False
        return result[1:-1] if self.check_parentesis(result) else result

    def check_parentesis(self, string):
        """Check if first ( matches the last one

        >>> self.check_parentesis('(())')
        True
        >>> self.check_parentesis('()()')
        False
        """
        if not string or string[0] != '(' or string[-1] != ')': return False
        res = 0
        for c in string[1:-1]:
            if c == '(': res += 1
            elif c == ')': res -= 1
            if res < 0: return False
        return True


    def render_jump_label(self, expr, def_size: int = 0):
        self.itisjump = True
        if expr.indirection != IndirectionType.OFFSET:
            result = self.render_instruction_argument(expr, def_size)  # TODO why need something else?
            self.itisjump = False
            return result
        if def_size and expr.element_size == 0:
            expr.element_size = def_size
        result = "".join(IR2CppJump(self._context).visit(expr))
        self.itisjump = False
        return result

    def _jump(self, cmd, label):
        if self.isrelativejump(label):
            return "{;}"

        label, _ = self.jump_post(label)
        if self._context.args.mergeprocs == 'separate' and cmd.upper() == 'JMP':
            if label == '__dispatch_call':
                return "return __dispatch_call(__disp, _state);"
            if self._context.has_global(label):
                g = self._context.get_global(label)
                target_proc_name = None
                if isinstance(g, op.label) and g.name in self.label_to_proc:
                    target_proc_name = self.label_to_proc[g.name]
                elif isinstance(g, proc_module.Proc):
                    target_proc_name = g.name
                if target_proc_name and self.proc.name != target_proc_name:
                    if g.name == target_proc_name:
                        return f"return {g.name}(0, _state);"
                    return f"return {target_proc_name}(m2c::k{label}, _state);"

        return "%s(%s)" % (cmd.upper(), label)

    def _instruction2(self, cmd, dst, src):
        self.a, self.b = self.parse2(dst, src)
        return "%s(%s, %s)" % (cmd.upper(), self.a, self.b)

    def _instruction3(self, cmd, dst, src, c):
        self.a, self.b = self.parse2(dst, src)
        self.c = self.render_instruction_argument(c)
        return "%s(%s, %s, %s)" % (cmd.upper(), self.a, self.b, self.c)

    def return_empty(self, _):
        return []

    def _assignment(self, stmt):
        dst, src = stmt
        asm2ir = Asm2IR(self._context, '')
        if not isinstance(src, Expression):
            src = asm2ir.transform(src)

        src.indirection = IndirectionType.VALUE
        o = src
        '''
        #src = Token.remove_tokens(src, ['expr'])
        #size = self.calculate_size(src)
        size = stmt.size()
        #calc = ExprSizeCalculator(init=Vector(0, 0))
        #size = calc.visit(src)[0]

        ptrdir = Token.find_tokens(src, 'ptrdir')
        if ptrdir:
            type = ptrdir[0]
            if isinstance(type, Token):
                type = type.children
            type = type.lower()
            src = Token.find_and_replace_tokens(src, 'ptrdir', self.return_empty)
        o = stmt  # self._context.get_global(dst)
        o.element_size = size
        if ptrdir:
            o.original_type = type
        o.implemented = True
        self._context.reset_global(dst, o)
        '''
        self._cmdlabel += "#undef %s\n#define %s %s\n" % (dst, dst, self.render_instruction_argument(src))
        return ''

    def _equ(self, dst):
        src = self._context.get_global(dst).value
        src.indirection = IndirectionType.VALUE
        self._cmdlabel += "#define %s %s\n" % (dst, self.render_instruction_argument(src))
        return ''

    def produce_c_data_single_(self, data):
        """
        It takes an assembler data and returns a C++ object

        :param data: The data to be converted
        :return: data value, declaration, size
        """
        # Real conversion
        internal_data_type = data.getinttype()
        self.element_size = data.getsize()

        logging.debug(f"current data type = {internal_data_type}")
        rc, rh = self.__type_table[internal_data_type](data)

        logging.debug(rc)
        logging.debug(rh)
        return rc, rh, data.getsize()

    def produce_c_data_number(self, data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        rc = ''.join(str(i) if isinstance(i, int) else ''.join(str(x) for x in self.visit(i)) for i in r)
        # rc = ''.join([str(i) if isinstance(i, int) else self.visit(i) for i in r])
        rh = f'{data_ctype} {label}'
        return rc, rh

    def produce_c_data_array(self, data: op.Data):
        label, data_ctype, _, r, elements, _ = data.getdata()
        if not any(r):  # all zeros
            r = [0]
        rc = '{'
        for i, v in enumerate(r):
            if i != 0:
                rc += ','
            if isinstance(v, op.Data):
                c = self.produce_c_data_single_(v)[0]
                rc += c
            # elif isinstance(v, (lark.Token, lark.Tree)):
            #    rc += "".join(flatten(self.visit(v)))
            elif isinstance(v, list):
                # print(v)
                l = [str(i) for i in v]
                # print(l)
                rc += "".join(l)
            else:
                rc += str(v)
        rc += '}'
        # assert(len(r)==elements)
        rh = f'{data_ctype} {label}[{elements}]'
        return rc, rh

    def produce_c_data_zero_string(self, data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        r = flatten(r)
        rc = '"' + ''.join(self.convert_str(i) for i in r[:-1]) + '"'
        rc = re.sub(r'(\\x[0-9a-f][0-9a-f])([0-9a-fA-F])', r'\g<1>" "\g<2>', rc)  # fix for stupid C hex escapes: \xaef
        rh = f'char {label}[{size}]'
        return rc, rh

    def produce_c_data_array_string(self, data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        r = flatten(r)
        rc = '{' + ",".join([self.convert_char(i) for i in r]) + '}'
        rh = f'char {label}[{size}]'
        return rc, rh

    def produce_c_data_object(self, data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        # rc = '{' + ",".join([str(i) for i in r]) + '}'
        rc = []
        for i in data.getmembers():
            c, _, _ = self.produce_c_data_single_(i)
            rc += [c]
        rc = '{' + ','.join(rc) + '}'
        rh = f'{data_ctype} {label}'
        return rc, rh

    def convert_char(self, c):
        if isinstance(c, int) and c not in [10, 13]:
            return str(c)
        return "'" + self.convert_str(c) + "'"

    def convert_str(self, c):
        vvv = ""
        if isinstance(c, int):
            if c == 13:
                vvv = r"\r"
            elif c == 10:
                vvv = r"\n"
            elif c == 0:
                vvv = r"\0"
            elif c < 32:
                vvv = "\\x{:02x}".format(c)
            else:
                vvv = chr(c)
        elif isinstance(c, str):
            # logging.debug "~~ " + r[i] + str(ord(r[i]))
            res = ''
            # string = c
            # for c in string:

            if c in ["\'", '\"', '\\']:
                vvv = "\\" + c
            elif ord(c) > 127:
                t = c.encode('cp437', 'backslashreplace')
                vvv = '\\' + hex(ord(t))[1:]
                # vvv = c
            elif c == '\0':
                vvv = '\\0'
            else:
                vvv = c
            # res += vvv
            # vvv = res
        return vvv

    def produce_global_jump_table(self, globals, itislst):
        # Produce call table
        if itislst:
            result = """
 bool __dispatch_call(m2c::_offsets __i, struct m2c::_STATE* _state){
    X86_REGREF
    if ((__i>>16) == 0) {__i |= ((dd)cs) << 16;}
    __disp=__i;
    switch (__i) {
"""
        else:
            result = """
 bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state){
    switch (__disp) {
"""
        entries = OrderedDict()
        for k, v in globals:
            if isinstance(v, proc_module.Proc) and v.used:
                k = re.sub(r'[^A-Za-z0-9_]', '_', k)  # need to do it during mangling
                # procs.append(k)
                entries[k] = (self.cpp_mangle_label(k), '0')
                # labels = self.leave_unique_labels(v.provided_labels)
                labels = v.provided_labels

                entries.update({label: (v.name, '__disp') for label in set(labels) if label != v.name})

        # procs = self.leave_unique_labels(procs)
        # for name in procs:
        #    if not name.startswith('_group'):  # TODO remove dirty hack. properly check for group
        #    result += "        case m2c::k%s: \t%s(0, _state); break;\n" % (name, cpp_mangle_label(name))
        #    entries[name] = (cpp_mangle_label(name), '0')

        names = self.leave_unique_labels(entries.keys())
        for name in names:
            result += "        case m2c::k%s: \t%s(%s, _state); break;\n" % (name, *entries[name])

        result += "        default: m2c::log_error(\"Don't know how to call to 0x%x. See \" __FILE__ \" line %d\\n\", __disp, __LINE__);m2c::stackDump(); abort();\n"
        result += "     };\n     return true;\n}\n"
        return result

    def _mov(self, dst, src):
        mapped_memory_access = False

        self.a, self.b = self.parse2(dst, src)
        # if self.d in ['sp', 'esp'] and check_int(self.s):
        #    self.__pushpop_count -= int(self.s)
        if 'raddr' in self.a or 'raddr' in self.b:
            mapped_memory_access = True

        if mapped_memory_access:
            return "MOV(%s, %s)" % (self.a, self.b)
        else:
            return "%s = %s;" % (self.a, self.b)

    def produce_jump_table_c(self, offsets):
        """
        It takes a list of labels and produces a C++ switch statement that jumps to the corresponding label

        :param labels: a list of labels that we want to jump to
        :return: The result of the function.
        """
        # Produce jump table
        result = """
            assert(0);
            __dispatch_call:
        #ifdef DOSBOX_CUSTOM
            if ((__disp >> 16) == 0xf000)
            {cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return false;}  // Jumping to BIOS
        #endif
            if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
            switch (__disp) {
        """
        for name, label in offsets:
            logging.debug('%s, %s', name, label)
            result += "        case m2c::k%s: \tgoto %s;\n" % (name, label)
        result += "        default: m2c::log_error(\"Don't know how to jump to 0x%x. See \" __FILE__ \" line %d\\n\", __disp, __LINE__);m2c::stackDump(); abort();\n"
        result += "    };\n}\n"
        return result

    def cpp_mangle_label(self, name):
        name = mangle_asm_labels(name)
        return name.lower()

    def produce_number_c(self, expr, radix, sign, value):
        if radix == 8:
            result = f'{sign}0{value}'
        elif radix == 16:
            result = f'{sign}0x{value}'
        elif radix == 10:
            result = f'{sign}{value}'
        elif radix == 2:
            result = f'{sign}{hex(int(value, 2))}'  # convert binary
        else:
            result = str(int(expr, radix))
        return result



    def INTEGER(self, t):
        # s = {2: hex(token.value), 8: oct(token.value), 10: str(token.value), 16: hex(token.value)}[token.column]
        return [self.produce_number_c('', t.start_pos, t.line, t.column)]

    def STRING(self, token):
        result = token.value
        # m = re.match(r'^[\'\"](....)[\'\"]$', token.value)  # char constants 'abcd'
        if len(token.value) == 4:  # m:
            ex = token
            # ex = m.group(1)
            result = '0x'
            for i in range(0, 4):
                # logging.debug("constant %s %d" %(ex,i))
                ss = str(hex(ord(ex[i])))
                # logging.debug("constant %s" %ss)
                result += ss[2:]
        else:
            result = result.replace('\\', '\\\\')  # escape c \ symbol
            result = "'" + result + "'"
        return [result]


    def expr(self, tree):
        self._indirection = tree.indirection

        single = len(tree.children) == 1
        origexpr = tree.children[0]
        while isinstance(origexpr, list) and origexpr:
            origexpr = origexpr[0]
        self._isjustlabel = single and ((isinstance(origexpr, lark.Token) and origexpr.type == LABEL) \
                                        or (isinstance(origexpr, lark.Token) and origexpr.type == SQEXPR \
                                            and isinstance(origexpr.children,
                                                           lark.Token) and origexpr.children.type == LABEL) \
                                        or (isinstance(origexpr, lark.Tree) and origexpr.data == MEMBERDIR))
        self._isjustmember = single and isinstance(origexpr, lark.Tree) and origexpr.data == MEMBERDIR

        self.element_size = tree.element_size
        self._ismember = False
        self._need_pointer_to_member = False
        result = "".join(self.visit(tree.children))
        tree.indirection = self._indirection

        if tree.indirection == IndirectionType.POINTER and tree.ptr_size == 0 and hasattr(self,"variable_size"):  # [ var ]
            tree.ptr_size = self.variable_size  # Set destination size based on variable size
        self.size_changed = self.size_changed or "size_changed" in tree.mods and self._middle_size != tree.size()

        if tree.indirection == IndirectionType.POINTER and tree.registers.intersection({'bp', 'ebp', 'sp', 'esp'}):
            self._work_segment = "ss"  # and segment is not overriden means base is "ss:"

        if self._need_pointer_to_member:
            result = result[:-1] if result[-1] == '+' else result
            result = result.replace('++', '+').replace('+-', '-')
            result = f"{result}+{self._need_pointer_to_member[0]}))->{'.'.join(self._need_pointer_to_member[1:])}"

        if tree.indirection == IndirectionType.POINTER and not self._ismember and (
                not self._isjustlabel or self.size_changed):
            result = self.convert_sqbr_reference(tree.segment_register, result, 'destination' in tree.mods,
                                                 tree.ptr_size, False, lea='lea' in tree.mods)
        if self._ismember:
            result = f'(({self.struct_type}*)raddr({self._work_segment},{result}'
        # if indirection == IndirectionType.POINTER and \
        if self.needs_dereference:
            self.needs_dereference = False
            if result[0] == '(' and result[-1] == ')':
                result = "*%s" % result
            else:
                result = "*(%s)" % result
        return result

    def data(self, data):
        binary_width = self._context.typetosize(data.data_type)  # TODO pervertion
        self.is_data = binary_width
        # For unit test
        from masm2c.parser import Parser
        Parser.c_dummy_label = 0
        c, h, size = self.produce_c_data_single_(data)
        c += ", // " + data.getlabel() + "\n"  # TODO can put original_label
        h += ";\n"
        self.is_data = False
        return c, h, size

    def LABEL(self, token):
        if self.is_data:
            size = self.is_data if type(self.is_data) == int else 0
            return [self._context.get_global_value(token, size=size)]
        return [self.convert_label_(token)]
        # return self._context.get_global_value(token, size=self.element_size)

    def offsetdir(self, tree):  # TODO equ, assign support
        name = tree.children[0]

        if isinstance(name, lark.Tree) and name.data=='memberdir':
            label = name.children
            try:
                g = self._context.get_global(label[0])
            except Exception:
                return label

            if isinstance(g, op.var):
                value = f'offset({g.segment},{".".join(label)})'
            elif isinstance(g, op.Struct):
                value = f'offsetof({label[0]},{".".join(label[1:])})'
            elif isinstance(g, (op._equ, op._assignment)):
                value = f'({label[0]})+offsetof({g.original_type},{".".join(label[1:])})'
            else:
                raise Exception('Not handled type ' + str(type(g)))
            self._indirection = IndirectionType.VALUE
            return [lark.Token('memberdir', value)]

        try:
            g = self._context.get_global(name)
        except Exception:
            # logging.warning("expand_cb() global '%s' is missing" % name)
            return name
        if isinstance(g, op.var):
            logging.debug("it is var %s", g.size)
            if self.element_size == 2:
                return "offset(%s,%s)" % (g.segment, g.name)
            elif self.element_size == 4:
                return "far_offset(%s,%s)" % (g.segment, g.name)
            else:
                raise ValueError("Unknown offset size %s", self.element_size)
        elif isinstance(g, proc_module.Proc):
            logging.debug("it is proc")
            return "m2c::k" + g.name.lower()  # .capitalize()
        elif isinstance(g, op.label):
            return "m2c::k" + g.name.lower()  # .capitalize()
        else:
            raise ValueError("Unknown type for offsetdir %s", type(g))

    def notdir(self, tree):
        return ['~'] + tree.children

    def ordir(self, tree):
        return [tree.children[0], " | ", tree.children[1]]

    def xordir(self, tree):
        return [tree.children[0], " ^ ", tree.children[1]]

    def anddir(self, tree):
        return [tree.children[0], " & ", tree.children[1]]

    def sizearg(self, tree):
        return [f"sizeof({tree.children[0]})"]


IR2Cpp = Cpp
'''
class IR2Cpp(TopDownVisitor, Cpp):

    def __init__(self, parser):
        super(IR2Cpp, self).__init__(context=parser)
'''

class IR2CppJump(IR2Cpp):

    def __init__(self, parser):
        super().__init__(parser)

    def expr(self, tree):
        if isinstance(tree.children, lark.Token) and tree.children.type == 'register':
            self._indirection = IndirectionType.VALUE  # based register value
            tree.indirection = self._indiretction
        return super().expr(tree)

    def LABEL(self, token):
        if self._context.has_global(token):
            g = self._context.get_global(token)
            if isinstance(g, op.var):
                self._indirection = IndirectionType.POINTER  # []
            elif isinstance(g, (op.label, proc_module.Proc)):
                self._indirection = IndirectionType.OFFSET  # direct using number
        return [token]


if __name__ == "__main__":
    import doctest
    doctest.testmod()