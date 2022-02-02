from __future__ import division
from __future__ import division
from __future__ import print_function

import logging
import re
import sys, os
from collections import OrderedDict
from enum import Enum

import jsonpickle

from builtins import hex
from builtins import object
from builtins import range
from builtins import str
from copy import copy

import masm2c.proc as proc_module
from masm2c import op
from masm2c.Token import Token
from masm2c.op import DataType

OFFSETDIR = 'offsetdir'
LABEL = 'LABEL'
PTRDIR = 'ptrdir'
REGISTER = 'register'
SEGMENTREGISTER = 'segmentregister'
SEGOVERRIDE = 'segoverride'
SQEXPR = 'sqexpr'
INTEGER = 'INTEGER'
MEMBERDIR = 'memberdir'


class IndirectionType(Enum):
    OFFSET = -1
    VALUE = 0
    POINTER = 1


class InjectCode(Exception):

    def __init__(self, cmd):
        self.cmd = cmd
        super().__init__()


class SkipCode(Exception):
    pass


class CrossJump(Exception):
    pass


def produce_jump_table(labels):
    # Produce jump table
    result = """
    assert(0);
    __dispatch_call:
#ifdef DOSBOX
    if ((__disp >> 16) == 0xf000)
	{cs=0xf000;eip=__disp&0xffff;m2c::fix_segs();return;}  // Jumping to BIOS
    if ((__disp>>16) == 0) {__disp |= ((dd)cs) << 16;}
#endif
    switch (__disp) {
"""
    offsets = []
    for k in labels:
        k = re.sub(r'[^A-Za-z0-9_]', '_', k)
        offsets.append((k.lower(), k))
    offsets = sorted(offsets, key=lambda t: t[1])
    for name, label in offsets:
        logging.debug(f'{name}, {label}')
        result += "        case m2c::k%s: \tgoto %s;\n" % (name, cpp_mangle_label(label))
    result += "        default: m2c::log_error(\"Jump to nowhere to 0x%x. See line %d\\n\", __disp, __LINE__);m2c::stackDump(_state); abort();\n"
    result += "    };\n}\n"
    return result


class SeparateProcStrategy:

    def forward_to_dispatcher(self, disp):
        return disp, "__dispatch_call"

    def fix_call_label(self, dst):
        return dst

    def produce_proc_start(self, name):
        ret = " // Procedure %s() start\n%s()\n{\n" % (name, cpp_mangle_label(name))
        return ret

    def function_header(self, name, entry_point=''):
        header = """

 void %s(m2c::_offsets _i, struct m2c::_STATE* _state){
    X86_REGREF
    __disp = _i;
""" % cpp_mangle_label(name)
        if entry_point != '':
            header += """
    if (__disp == kbegin) goto %s;
""" % entry_point
        header += """
    if (__disp == 0) goto _begin;
    else goto __dispatch_call;
    %s:
    _begin:
""" % cpp_mangle_label(name)
        return header

    def function_end(self):
        return ' }\n'

    def write_declarations(self, procs, context):
        result = ""
        for p in sorted(procs):  # TODO only if used or public
            if p == 'mainproc':  # and not context.main_file:
                result += 'static '
            result += "void %s(m2c::_offsets, struct m2c::_STATE*);\n" % cpp_mangle_label(p)

        for i in sorted(context.externals_procs):
            v = context.get_globals()[i]
            if v.used:
                result += f"extern void {v.name}(m2c::_offsets, struct m2c::_STATE*);\n"

        result += """
#ifndef DOSBOX
static
#endif
bool __dispatch_call(m2c::_offsets __disp, struct m2c::_STATE* _state);
"""
        return result

    def get_strategy(self):
        return ""


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def parse_bin(s):
    sign = s.group(1)
    b = s.group(2)
    v = hex(int(b, 2))
    if sign:
        v = sign + v
    # logging.debug("BINARY: %s -> %s" %(b, v))
    return v


def convert_number_to_c(expr, radix=10):
    origexpr = expr
    if expr == '?':
        return '0'
    try:
        if re.match(r'^([+-]?)([0-8]+)[OoQq]$', expr):
            radix = 8
        elif re.match(r'^([+-]?)([0-9][0-9A-Fa-f]*)[Hh]$', expr):
            radix = 16
        elif re.match(r'^([+-]?)([0-9]+)[Dd]$', expr):
            radix = 10
        elif re.match(r'^([+-]?)([0-1]+)[Bb]$', expr):
            radix = 2

        if radix == 8:
            expr = re.sub(r'^([+-]?)([0-8]+)[OoQq]?$', r'\g<1>0\g<2>', expr)
        elif radix == 16:
            expr = re.sub(r'^([+-]?)([0-9][0-9A-Fa-f]*)[Hh]?$', r'\g<1>0x\g<2>', expr)
        elif radix == 10:
            expr = re.sub(r'^([+-]?)([0-9]+)[Dd]?$', r'\g<1>\g<2>', expr)
        elif radix == 2:
            expr = re.sub(r'^([+-]?)([0-1]+)[Bb]?$', parse_bin, expr)  # convert binary
        else:
            expr = str(int(expr, radix))
    except Exception:
        logging.error(f"Failed to parse number {origexpr} radix {radix}")

    return expr


def guess_int_size(v):
    size = 0
    if v < 0:
        v = -2 * v - 1
    if v < 256:
        size = 1
    elif v < 65536:
        size = 2
    elif v < 4294967296:
        size = 4
    else:
        logging.error(f'too big number {v}')

    logging.debug('guess_int_size %d' % size)
    return size


def cpp_mangle_label(name):
    name = name.lower()
    if name == 'main':
        name = 'asmmain'
    return name.replace('$', '_tmp')


class Cpp(object):
    ''' Visitor for all operations to produce C++ code '''

    def __init__(self, context, outfile="", skip_output=None, function_name_remapping=None,
                 proc_strategy=SeparateProcStrategy(), merge_data_segments=True):
        # proc_strategy = SingleProcStrategy()):
        '''

        :param context: pointer to Parser data
        :param outfile: Output filename
        :param skip_output: List of functions to skip at output
        :param function_name_remapping: Dict for how to rename functions
        :param proc_strategy: Strategy to Single/Separate functions
        '''

        self.__namespace = os.path.basename(outfile)
        self.__indirection: IndirectionType = IndirectionType.VALUE
        self.__current_size = 0
        self.__work_segment = ""
        self.__codeset = 'cp437'
        self.__context = context

        self.proc_strategy = proc_strategy

        self.__procs = context.proc_list
        self.__proc_queue = []
        self.__proc_done = []
        self.__failed = []
        self.__skip_output = skip_output
        self.__function_name_remapping = function_name_remapping
        self.__translated = []
        self.__proc_addr = []
        self.__used_data_offsets = set()
        self.__methods = []
        self.__pushpop_count = 0

        self.lea = False
        self.far = False
        self.size_changed = False
        self.needs_dereference = False
        self.itispointer = False

        self.body = ""
        self.struct_type = None
        self.grouped = set()
        self.groups = OrderedDict()

        self.dispatch = ''
        self.prefix = ''
        self.label = ''
        self.merge_data_segments = merge_data_segments

    def produce_c_data(self, segments):
        cdata_seg = ""
        hdata_seg = ""
        rdata_seg = ""
        edata_seg = ""
        for i in segments.values():
            rdata_seg += f"db& {i.name}=*((db*)&m2c::m+0x{i.offset:x});\n"
            edata_seg += f"extern db& {i.name};\n"
            for j in i.getdata():
                c, h, size = self.produce_c_data_single_(j)

                h += ";\n"

                if not j.getalign():  # if align do not assign it
                    #  mycopy(bb, {'1','2','3','4','5'});
                    #  caa=3;
                    m = re.match(r'^([0-9A-Za-z_]+)\s+([0-9A-Za-z_]+)(\[\d+\])?;\n', h)
                    if not m:
                        logging.error(f'Failed to parse {c} {h}')
                    name = m.group(2)

                    asgn = re.sub(r'^([0-9A-Za-z_]+)\s+(?:[0-9A-Za-z_]+(\[\d+\])?);\n', r'\g<1> tmp999\g<2>', h)

                    if name.startswith('dummy') and c == '0':
                        c = ''
                    else:
                        if m.group(3):  # if array
                            if c == '{}':
                                c = ''
                            else:
                                c = f'    {{{asgn}={c};MYCOPY({name})}}'
                        else:
                            # c = f'    {name}={c};'
                            c = f'    {{{asgn}={c};MYCOPY({name})}}'

                    real_seg, real_offset = j.getrealaddr()
                    if real_seg:
                        if c:
                            c += f' // {real_seg:04x}:{real_offset:04x}'
                        c += "\n"
                    # c += " // " + j.getlabel() + "\n"  # TODO can put original_label

                    # char (& bb)[5] = group.bb;
                    # int& caa = group.aaa;
                    # references
                    r = re.sub(r'^([0-9A-Za-z_]+)\s+([0-9A-Za-z_\[\]]+)(\[\d+\]);',
                               r'\g<1> (& \g<2>)\g<3> = m2c::m.\g<2>;', h)
                    r = re.sub(r'^([0-9A-Za-z_]+)\s+([0-9A-Za-z_\[\]]+);', r'\g<1>& \g<2> = m2c::m.\g<2>;', r)
                    # externs
                    e = re.sub(r'^([0-9A-Za-z_]+)\s+([0-9A-Za-z_\[\]]+)(\[\d+\]);', r'extern \g<1> (& \g<2>)\g<3>;', h)
                    e = re.sub(r'^([0-9A-Za-z_]+)\s+([0-9A-Za-z_\[\]]+);', r'extern \g<1>& \g<2>;', e)

                    if real_seg:
                        if c:
                            h = h[:-1] + f' // {real_seg:04x}:{real_offset:04x}\n'

                    cdata_seg += c  # cpp source - assigning
                    rdata_seg += r  # reference in _data.cpp
                    edata_seg += e  # extern for header
                hdata_seg += h  # headers in _data.h

        return cdata_seg, hdata_seg, rdata_seg, edata_seg

    def convert_label(self, token):
        name_original = token.value
        name = name_original.lower()
        logging.debug("convert_label name = %s indirection = %s" % (name, str(self.__indirection)))

        if self.__indirection == IndirectionType.OFFSET:
            try:
                offset, _, _ = self.__context.get_offset(name)
            except Exception:
                pass
            else:
                logging.debug("OFFSET = %s" % offset)
                self.__indirection = IndirectionType.VALUE
                self.__used_data_offsets.add((name, offset))
                return Token('LABEL', "(dw)m2c::k" + name)

        try:
            g = self.__context.get_global(name)
        except Exception:
            # logging.warning("expand_cb() global '%s' is missing" % name)
            return token

        if isinstance(g, op._equ):
            logging.debug("it is equ")
            if not g.implemented:
                raise InjectCode(g)
            value = g.original_name
            # value = self.expand_equ(g.value)
            logging.debug("equ: %s -> %s" % (name, value))
        elif isinstance(g, op._assignment):
            logging.debug("it is assignment")
            if not g.implemented:
                raise InjectCode(g)
            value = g.original_name
            # value = self.expand_equ(g.value)
            logging.debug("assignment %s = %s" % (name, value))
        elif isinstance(g, proc_module.Proc):
            logging.debug("it is proc")
            if self.__indirection != IndirectionType.OFFSET:
                logging.error("Invalid proc label usage proc %s offset %s" % (g.name, str(g.offset)))
                value = "m2c::k" + g.name.lower()  # .capitalize()
            else:
                value = str(g.offset)
                self.__indirection = IndirectionType.VALUE
        elif isinstance(g, op.var):
            logging.debug("it is var " + str(g.size))
            size = g.size
            if self.__current_size == 0:  # TODO check
                self.__current_size = size
            if size == 0 and not g.issegment:
                raise Exception("invalid var '%s' size %u" % (name, size))
            if g.issegment:
                value = "seg_offset(%s)" % (name_original.lower())
                self.__indirection = IndirectionType.VALUE
            else:
                self.needs_dereference = False
                self.itispointer = False
                if g.elements != 1:
                    self.needs_dereference = True
                    self.itispointer = True
                if g.elements == 1 and self.__isjustlabel and not self.lea and g.size == self.__current_size:
                    # traceback.print_stack(file=sys.stdout)
                    value = g.name
                    self.__indirection = IndirectionType.VALUE
                else:
                    if self.__indirection == IndirectionType.POINTER and self.isvariable:
                        value = g.name
                        if not self.__isjustlabel:  # if not just single label
                            self.needs_dereference = True
                            self.itispointer = True
                            if g.elements == 1:  # array generates pointer himself
                                value = "&" + value

                            if g.getsize() == 1:  # it is already a byte
                                value = "(%s)" % value
                            else:
                                value = "((db*)%s)" % value
                                self.size_changed = True
                    else:
                        value = "offset(%s,%s)" % (g.segment, g.name)
                    if self.__work_segment == 'cs':
                        self.body += '\tcs=seg_offset(' + g.segment + ');\n'
            # ?self.__indirection = 1
        elif isinstance(g, op.label):
            value = "m2c::k" + g.name.lower()  # .capitalize()
        else:
            size = g.getsize()
            if size == 0:
                raise Exception("invalid var '%s' size %u" % (name, size))
            if self.__indirection in [IndirectionType.VALUE or IndirectionType.POINTER]:  # x0r self.indirection == 1 ??
                value = "offsetof(struct Memory,%s)" % name_original
                if self.__indirection == IndirectionType.POINTER:
                    self.__indirection = IndirectionType.VALUE
            elif self.__indirection == IndirectionType.OFFSET:
                value = "%s" % g.offset
                self.__indirection = IndirectionType.VALUE
            else:
                raise Exception("invalid indirection %d name '%s' size %u" % (self.__indirection, name, size))
        return Token('LABEL', value)

    def remove_dots(self, tokens):
        if isinstance(tokens, list):
            l = []
            for i in tokens:
                i = self.remove_dots(i)
                if i != '.':
                    l += [i]
            return l
        else:
            return tokens

    def convert_member(self, token):
        logging.debug("name = %s indirection = %s" % (str(token), str(self.__indirection)))
        value = token
        label = [l.lower() for l in Token.find_tokens(token, LABEL)]
        self.struct_type = None

        if self.__indirection == IndirectionType.OFFSET:
            try:
                g = self.__context.get_global(label[0])
            except:
                pass
            else:
                if isinstance(g, op.var):
                    value = f'offset({g.segment},{".".join(label)})'
                elif isinstance(g, op.Struct):
                    value = f'offsetof({label[0]},{".".join(label[1:])})'
                else:
                    raise Exception('Not handled type ' + str(type(g)))
                self.__indirection = IndirectionType.VALUE
                return Token('memberdir', value)

        size = self.get_size(token)
        try:
            g = self.__context.get_global(label[0])
        except:
            # logging.warning("expand_cb() global '%s' is missing" % name)
            return token

        if isinstance(g, (op._equ, op._assignment)):
            logging.debug(str(g))
            if not g.implemented:
                raise InjectCode(g)
            if self.__isjustlabel:
                value = '.'.join(label)
            else:
                self.struct_type = g.original_type
                self.needs_dereference = True
                self.itispointer = False
                value = f"{label[0]}))->{'.'.join(label[1:])}"
            logging.debug("equ: %s -> %s" % (label[0], value))
        elif isinstance(g, op.var):
            logging.debug("it is var " + str(size))

            if self.__current_size == 0:  # TODO check
                self.__current_size = size
            if size == 0:
                raise Exception(f"invalid var {label} size {size}")
            self.needs_dereference = False
            self.itispointer = False
            if g.elements != 1:
                self.needs_dereference = True
                self.itispointer = True
            if g.elements == 1 and self.__isjustlabel and not self.lea and size == self.__current_size:
                # traceback.print_stack(file=sys.stdout)
                value = '.'.join(label)
                self.__indirection = IndirectionType.VALUE
            else:
                if self.__indirection == IndirectionType.POINTER and self.isvariable:
                    value = '.'.join(label)
                    if not self.__isjustlabel:  # if not just single label
                        self.needs_dereference = True
                        self.itispointer = True
                        if g.elements == 1:  # array generates pointer himself
                            value = "&" + value

                        if g.getsize() == 1:  # it is already a byte
                            value = "(%s)" % value
                        else:
                            value = "((db*)%s)" % value
                            self.size_changed = True
                elif self.__indirection == IndirectionType.OFFSET and self.isvariable:
                    value = "offset(%s,%s)" % (g.segment, '.'.join(label))
                if self.__work_segment == 'cs':
                    self.body += '\tcs=seg_offset(' + g.segment + ');\n'
            # ?self.__indirection = 1
            if value == token:
                logging.error('value not yet assigned')
        elif isinstance(g, op.Struct):
            if self.__isjustmember:
                value = f'offsetof({label[0]},{".".join(label[1:])})'
            else:
                register = Token.remove_tokens(token, [MEMBERDIR, 'LABEL'])
                register = self.remove_dots(register)
                register = self.tokenstostring(register)
                register = register.replace('(+', '(')

                self.struct_type = label[0]
                self.needs_dereference = True
                self.itispointer = False
                value = f"{register}))->{'.'.join(label[1:])}"

        if size == 0:
            raise Exception("invalid var '%s' size %u" % (str(label), size))
        return value

    def get_size(self, expr):
        '''
        Get tokens memory size
        :param expr: Tokens
        :return: byte size
        '''
        logging.debug('get_size("%s")' % expr)
        # if isinstance(expr, string):
        #    expr = expr.strip()
        origexpr = expr

        expr = Token.remove_tokens(expr, ['expr'])

        ptrdir = Token.find_tokens(expr, PTRDIR)
        if ptrdir:
            value = ptrdir[0]
            # logging.debug('get_size res 1')
            return self.__context.typetosize(value)

        issqexpr = Token.find_tokens(expr, SQEXPR)
        segover = Token.find_tokens(expr, 'segoverride')
        if issqexpr or segover:
            expr = Token.remove_tokens(expr, ['segmentregister', 'register', 'INTEGER', SQEXPR, 'segoverride'])
            return self.get_size(expr)
            # return 0

        if isinstance(expr, list) and all(
                isinstance(i, str) or (isinstance(i, Token) and i.type == 'INTEGER') for i in expr):
            s = "".join([x.value if isinstance(x, Token) else x for x in expr])
            s = re.sub(r'^0+(?=\d)', '', s)  # TODO put it to parser
            try:
                s = eval(s)
                expr = Token('INTEGER', str(s))
            except:
                pass

        if isinstance(expr, Token):
            if expr.type in ('register', 'segmentregister'):
                return self.__context.is_register(expr.value)
            elif expr.type == 'INTEGER':
                try:
                    # v = self.__context.parse_int(expr.value)
                    v = eval(re.sub(r'^0+(?=\d)', '', expr.value))
                    size = guess_int_size(v)
                    return size
                except:
                    pass
            elif expr.type == 'STRING':
                m = re.match(r'\'(.+)\'$', expr.value)  # char constants
                if m:
                    return len(m.group(1))
            elif expr.type == 'LABEL':
                name = expr.value
                logging.debug('name = %s' % name)
                try:
                    g = self.__context.get_global(name)
                    if isinstance(g, (op._equ, op._assignment)):
                        if g.value != origexpr:  # prevent loop
                            return self.get_size(g.value)
                        else:
                            return 0
                    logging.debug('get_size res %d' % g.size)
                    return g.size
                except:
                    pass
            elif expr.type == MEMBERDIR:
                label = Token.find_tokens(expr.value, LABEL)
                g = self.__context.get_global(label[0])
                if isinstance(g, op.Struct):
                    type = label[0]
                else:
                    type = g.original_type

                try:
                    for member in label[1:]:
                        g = self.__context.get_global(type)
                        if isinstance(g, op.Struct):
                            g = g.getitem(member)
                            type = g.type
                        else:
                            return self.get_size(g)
                except KeyError as ex:
                    logging.debug(f"Didn't found for {label} {ex.args} will try workaround")
                    # if members are global as with M510 or tasm try to find last member size
                    g = self.__context.get_global(label[-1])

                return self.get_size(g)

        if isinstance(expr, list):
            if len(expr) == 0:
                return 0
            return max([self.get_size(i) for i in expr])

        offsetdir = Token.find_tokens(expr, 'offsetdir')
        if offsetdir:
            return 2  # TODO 16 bit word size

        # if isinstance(expr, str):  # in ('+','-','*','(',')','/'):
        #    return 0
        if isinstance(expr, str):
            from masm2c.parser import Parser
            return Parser.is_register(expr)
        elif isinstance(expr, (op.Data, op.var, op._assignment, op._equ)):
            return expr.getsize()
        else:
            logging.debug(f"Could not identify type for {expr} to get size")
        return 0

    def get_member_size(self, expr):
        '''
        Get (structure/object).member primitive size (like db, dw, dd...)
        :param expr: Tokens
        :return: size in bytes
        '''
        logging.debug('get_size("%s")' % expr)

        if isinstance(expr, Token):
            if expr.type == MEMBERDIR:
                label = Token.find_tokens(expr.value, LABEL)
                g = self.__context.get_global(label[0])
                if isinstance(g, op.Struct):
                    type = label[0]
                else:
                    type = g.gettype()

                try:
                    for member in label[1:]:
                        g = self.__context.get_global(type)
                        if isinstance(g, op.Struct):
                            g = g.getitem(member)
                            type = g.gettype()
                        else:
                            return self.get_size(g)
                except KeyError as ex:
                    logging.debug(f"Didn't found for {label} {ex.args} will try workaround")
                    # if members are global as with M510 or tasm try to find last member size
                    g = self.__context.get_global(label[-1])

                return self.__context.typetosize(Token(LABEL, g.gettype()))
        return 0

    def convert_sqbr_reference(self, expr, destination, size, islabel, lea=False):
        if not lea or destination:
            if not islabel or not self.isvariable:
                self.needs_dereference = True
                self.itispointer = True
                if size == 1:
                    expr = "raddr(%s,%s)" % (self.__work_segment, expr)
                elif size == 2:
                    expr = "(dw*)(raddr(%s,%s))" % (self.__work_segment, expr)
                elif size == 4:
                    expr = "(dd*)(raddr(%s,%s))" % (self.__work_segment, expr)
                elif size == 8:
                    expr = "(dq*)(raddr(%s,%s))" % (self.__work_segment, expr)
                else:
                    logging.error(f"~{expr}~ invalid size {size}")
                    expr = "raddr(%s,%s)" % (self.__work_segment, expr)
            else:
                if self.size_changed:  # or not self.__isjustlabel:
                    expr = self.point_new_size(expr, size)

            logging.debug("expr: %s" % expr)
        return expr

    def point_new_size(self, expr, size):
        if self.itispointer:
            if size == 1:
                expr = "(db*)(%s)" % expr
            elif size == 2:
                expr = "(dw*)(%s)" % expr
            elif size == 4:
                expr = "(dd*)(%s)" % expr
            elif size == 8:
                expr = "(dq*)(%s)" % expr
            else:
                logging.error(f"~{expr}~ invalid size {size}")
        else:
            if size == 1:
                expr = "TODB(%s)" % expr
            elif size == 2:
                expr = "TODW(%s)" % expr
            elif size == 4:
                expr = "TODD(%s)" % expr
            elif size == 8:
                expr = "TODQ(%s)" % expr
            else:
                logging.error(f"~{expr}~ invalid size {size}")

        self.size_changed = False
        return expr

    def tokenstostring(self, expr):
        '''
        Convert remaining tokens to make it simple string
        :param expr: tokens
        :return: string
        '''
        if isinstance(expr, list):
            result = ''
            for i in expr:
                # TODO hack to handle ')register'
                if len(result) and result[-1] == ')' and isinstance(i, Token) and i.type == 'register':
                    result += '+'
                res = self.tokenstostring(i)
                res = re.sub(r'([Ee])\+', r'\g<1> +',
                             res)  # prevent "error: unable to find numeric literal operator 'operator""+" 0x0E+vecl_1c0
                res = res.replace('+)', ')')  # TODO hack
                result += res
            return result
        elif isinstance(expr, Token):

            if expr.type == 'STRING':
                m = re.match(r'^[\'\"](....)[\'\"]$', expr.value)  # char constants 'abcd'
                if m:
                    ex = m.group(1)
                    expr.value = '0x'
                    for i in range(0, 4):
                        # logging.debug("constant %s %d" %(ex,i))
                        ss = str(hex(ord(ex[i])))
                        # logging.debug("constant %s" %ss)
                        expr.value += ss[2:]
                expr.value = expr.value.replace('\\', '\\\\')  # escape c \ symbol

            return self.tokenstostring(expr.value)
        return expr

    def expand(self, expr, def_size=0, destination=False, lea=False):
        '''
        Convert argument Tokens into C
        :param expr: argument Tokens
        :param def_size: Preliminary calculate size in bytes
        :param destination: if it is destination argument
        :param lea: if it is lea operation
        :return: Argument in C format as string
        '''
        logging.debug(str(expr))

        expr = Token.remove_tokens(expr, ['expr'])  # no need expr token any more
        origexpr = expr  # save original expression before we will change it
        self.__work_segment = "ds"  # default work segment is ds
        self.__current_size = 0  # current size of argument is not yet found
        self.size_changed = False
        self.needs_dereference = False
        self.itispointer = False
        indirection: IndirectionType = IndirectionType.VALUE
        size = self.get_size(expr) if def_size == 0 else def_size  # calculate size if it not provided

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
            0].type == INTEGER and segoverride:
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
                member_size = self.get_member_size(Token(MEMBERDIR, memberdir))
                if member_size:
                    self.isvariable = True
                    size = member_size
                    indirection = IndirectionType.POINTER
            elif islabel:
                for i in islabel:  # Strange !?
                    label_size = self.get_size(Token(LABEL, i))
                    if label_size:
                        self.isvariable = True
                        size = label_size
                        indirection = IndirectionType.POINTER
                        break
        if lea:  # If lea operation it is the same as getting offset
            indirection = IndirectionType.OFFSET

        if indirection == IndirectionType.POINTER and not segoverride:
            regs = Token.find_tokens(expr, REGISTER)  # if it was registers used: bp, sp
            if regs and any([i in ['bp', 'ebp', 'sp', 'esp'] for i in regs]):  # TODO doublecheck
                self.__work_segment = "ss"  # and segment is not overriden means base is "ss:"
                self.isvariable = False
        if segoverride:  # if it was segment override then use provided value
            self.__work_segment = segoverride[0].value

        self.__current_size = size
        size_ovrr_by_ptr = size  # setting initial value
        if ptrdir:  # byte/word/struct ptr. get override type size
            value = ptrdir[0]
            # logging.debug('get_size res 1')
            size_ovrr_by_ptr = self.__context.typetosize(value)  # size overriden by ptr
            if size_ovrr_by_ptr != size:
                self.size_changed = True
            else:
                origexpr = Token.remove_tokens(origexpr, [PTRDIR, SQEXPR])
                if isinstance(origexpr, list) and len(origexpr) == 1:
                    origexpr = origexpr[0]

        # if just "label" or "[label]" or member
        self.__isjustlabel = (isinstance(origexpr, Token) and origexpr.type == LABEL) \
                             or (isinstance(origexpr, Token) and origexpr.type == SQEXPR \
                                 and isinstance(origexpr.value, Token) and origexpr.value.type == LABEL) \
                             or (isinstance(origexpr, Token) and origexpr.type == MEMBERDIR)
        self.__isjustmember = isinstance(origexpr, Token) and origexpr.type == MEMBERDIR

        self.__indirection = indirection

        if memberdir:
            expr = Token.find_and_replace_tokens(expr, MEMBERDIR, self.convert_member)
            if self.__indirection == IndirectionType.POINTER and self.needs_dereference and self.struct_type:

                # TODO A very hacky way to
                # put registers and numbers first since asm have byte aligned pointers
                # in comparison to C's type aligned
                registers = Token.find_tokens(expr, 'register')
                integers = Token.find_tokens(expr, 'INTEGER')
                expr = Token.remove_tokens(expr, ['register', 'INTEGER'])
                expr = self.tokenstostring(expr)
                while len(expr) and expr[0] == '+':
                    expr = expr[1:]
                while len(expr) > 2 and expr[0] == '(' and expr[-1] == ')':
                    expr = expr[1:-1]
                if integers:
                    expr = '+'.join(integers) + '+' + expr
                if registers:
                    expr = '+'.join(registers) + '+' + expr
                expr = expr.replace('++', '+').replace('+-', '-')

                expr = [f'(({self.struct_type}*)raddr({self.__work_segment},'] + [expr]
                self.needs_dereference = False
        else:
            if islabel:
                # assert(len(islabel) == 1)
                expr = Token.find_and_replace_tokens(expr, LABEL, self.convert_label)
        indirection = self.__indirection
        if self.__current_size != 0 and size != self.__current_size and not self.size_changed:
            size = self.__current_size

        if self.size_changed:
            size = size_ovrr_by_ptr

        expr = self.tokenstostring(expr)

        if indirection == IndirectionType.POINTER and not memberdir and (not self.__isjustlabel or self.size_changed):
            expr = self.convert_sqbr_reference(expr, destination, size, islabel, lea=lea)

        if self.size_changed:  # or not self.__isjustlabel:
            expr = self.point_new_size(expr, size)

        if indirection == IndirectionType.POINTER and self.needs_dereference:
            if expr[0] == '(' and expr[-1] == ')':
                expr = "*%s" % expr
            else:
                expr = "*(%s)" % expr

        return expr

    def jump_post(self, name):
        name, far = self.jump_to_label(name)
        hasglobal = self.__context.has_global(name)
        if not hasglobal:
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
            # if self.__context.has_global(name):
            # name = 'm2c::k'+name
            addtobody, name = self.proc_strategy.forward_to_dispatcher(name)
            self.dispatch += f'__disp={addtobody};\n'
            logging.debug(f'not sure if handle it properly {name} {addtobody}')
        else:
            g = self.__context.get_global(name)
            if isinstance(g, op.var):
                self.dispatch += f'__disp={name};\n'
                name = "__dispatch_call"

        return name, far

    def jump_to_label(self, name):
        '''
        Convert argument tokens which for jump operations into C string
        :param name: Tokens
        :return: C string
        '''
        logging.debug("jump_to_label(%s)" % name)
        # Token(expr, Token(LABEL, printf))
        #
        name = Token.remove_tokens(name, ['expr'])

        # jump_proc = False

        indirection = -5

        segoverride = Token.find_tokens(name, 'segoverride')
        if segoverride:
            self.__work_segment = segoverride[0].value

        if isinstance(name, Token) and name.type == 'register':
            name = name.value
            indirection = IndirectionType.VALUE  # based register value

        labeldir = Token.find_tokens(name, 'LABEL')
        if labeldir:
            from masm2c.parser import Parser
            labeldir[0] = Parser.mangle_label(cpp_mangle_label(labeldir[0]))
            if self.__context.has_global(labeldir[0]):
                g = self.__context.get_global(labeldir[0])
                if isinstance(g, op.var):
                    indirection = IndirectionType.POINTER  # []
                elif isinstance(g, (op.label, proc_module.Proc)):
                    indirection = IndirectionType.OFFSET  # direct using number
            else:
                name = labeldir[0]

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
            name = self.expand(name)

        if indirection == IndirectionType.OFFSET and labeldir:
            name = labeldir[0]

        logging.debug("label %s" % name)

        hasglobal = False
        far = False
        if self.__context.has_global(name):
            hasglobal = True
            g = self.__context.get_global(name)
            if isinstance(g, proc_module.Proc):
                far = g.far

        # if name in self.proc.retlabels:
        #    return "return /* (%s) */" % name, far

        if hasglobal:
            if isinstance(g, op.label):
                far = g.far  # make far calls to far procs

        if ptrdir:
            if any(isinstance(x, str) and x.lower() == 'far' for x in ptrdir):
                far = True
            elif any(isinstance(x, str) and x.lower() == 'near' for x in ptrdir):
                far = False

        return (name, far)

    def _label(self, name, isproc):
        if isproc:
            self.label = self.proc_strategy.produce_proc_start(name)
        else:
            self.label = "%s:\n" % cpp_mangle_label(name)
        return ''

    def schedule(self, name):
        name = name.lower()
        if name in self.__proc_queue or name in self.__proc_done or name in self.__failed:
            return
        logging.debug("+scheduling function %s..." % name)
        self.__proc_queue.append(name)

    def _call(self, name):
        logging.debug("cpp._call(%s)" % str(name))
        ret = ""
        size = self.get_size(name)
        dst, far = self.jump_to_label(name)
        if size == 4:
            far = True
        disp = '0'
        hasglobal = self.__context.has_global(dst)
        if hasglobal:
            g = self.__context.get_global(dst)
            if isinstance(g, op.label) and not g.isproc and not dst in self.__procs and not dst in self.grouped:
                #far = g.far  # make far calls to far procs
                disp = f"m2c::k{dst}"
                dst = g.proc
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
            disp, dst = self.proc_strategy.forward_to_dispatcher(dst)
            # self.body += addtobody

        dst = self.proc_strategy.fix_call_label(dst)
        dst = cpp_mangle_label(dst)

        if far:
            ret += f"CALLF({dst},{disp})"
        else:
            ret += f"CALL({dst},{disp})"
        return ret

    @staticmethod
    def _ret():
        return "RETN"

    def _retf(self, src):
        if src == []:
            self.a = '0'
        else:
            self.a = self.expand(src)
        return "RETF(%s)" % self.a

    def _xlat(self, src):
        if src == []:
            return "XLAT"
        else:
            self.a = self.expand(src)[2:-1]
            return "XLATP(%s)" % self.a

    def parse2(self, dst, src):
        dst_size, src_size = self.get_size(dst), self.get_size(src)
        if dst_size == 0:
            if src_size == 0:
                logging.debug("parse2: %s %s both sizes are 0" % (dst, src))
                # raise Exception("both sizes are 0")
            dst_size = src_size
        if src_size == 0:
            src_size = dst_size

        dst = self.expand(dst, dst_size, destination=True)
        src = self.expand(src, src_size)
        return dst, src

    def _add(self, dst, src):
        self.a, self.b = self.parse2(dst, src)
        # if self.d in ['sp', 'esp'] and check_int(self.s):
        #    self.__pushpop_count -= int(self.s)
        return "ADD(%s, %s)" % (self.a, self.b)

    def _sub(self, dst, src):
        self.a, self.b = self.parse2(dst, src)
        # if self.d in ['sp', 'esp'] and check_int(self.s):
        #    self.__pushpop_count += int(self.s)
        return "SUB(%s, %s)" % (self.a, self.b)

    def _xor(self, dst, src):
        self.a, self.b = self.parse2(dst, src)
        return "XOR(%s, %s)" % (self.a, self.b)

    def _mul(self, src):
        size = 0
        for i in src:
            if size == 0:
                size = self.get_size(i)
            else:
                break
        res = [self.expand(i, size) for i in src]
        if size == 0:
            size = self.__current_size
        return "MUL%d_%d(%s)" % (len(src), size, ",".join(res))

    def _imul(self, src):
        size = 0
        for i in src:
            if size == 0:
                size = self.get_size(i)
            else:
                break
        res = [self.expand(i, size) for i in src]
        if size == 0:
            size = self.__current_size
        return "IMUL%d_%d(%s)" % (len(src), size, ",".join(res))

    def _div(self, src):
        size = self.get_size(src)
        self.a = self.expand(src)
        return "DIV%d(%s)" % (size, self.a)

    def _idiv(self, src):
        size = self.get_size(src)
        self.a = self.expand(src)
        return "IDIV%d(%s)" % (size, self.a)

    def _jz(self, label):
        result = self.isrelativejump(label)
        if result:
            return "\n"
        else:
            label, far = self.jump_post(label)  # TODO
            return "JZ(%s)" % label

    def _jnz(self, label):
        label, far = self.jump_post(label)
        return "JNZ(%s)" % label

    def _jbe(self, label):
        label, far = self.jump_post(label)
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

    def _stosb(self, n, clear_cx):
        return "STOSB"  # %("" if n == 1 else n, ", true" if clear_cx else "")

    def _stosw(self, n, clear_cx):
        return "STOSW"  # %("" if n == 1 else n, ", true" if clear_cx else "")

    def _stosd(self, n, clear_cx):
        return "STOSD"  # %("" if n == 1 else n, ", true" if clear_cx else "")

    def _movsb(self, n, clear_cx):
        return "MOVSB"

    def _movsw(self, n, clear_cx):
        return "MOVSW"

    def _movsd(self, n, clear_cx):
        return "MOVSD"

    def _scasb(self):
        return "SCASB"

    def _scasw(self):
        return "SCASW"

    def _scasd(self):
        return "SCASD"

    def _scas(self, src):
        size = self.get_size(src)
        self.a = self.expand(src)
        srcr = Token.find_tokens(src, REGISTER)
        return "SCAS(%s,%s,%d)" % (self.a, srcr[0], size)

    def __proc(self, name, def_skip=0):
        logging.info("     Generating proc %s" % name)
        # traceback.print_stack(file=sys.stdout)
        try:
            skip = def_skip
            self.__pushpop_count = 0
            self.temps_max = 0
            if self.__context.has_global(name):
                self.proc = self.__context.get_global(name)
            else:
                logging.debug("No procedure named %s, trying label" % name)
                off, src_proc, skip = self.__context.get_offset(name)

                self.proc = proc_module.Proc(name)
                self.proc.stmts = copy(src_proc.stmts)
                self.proc.provided_labels = copy(src_proc.provided_labels)
                # self.proc.retlabels = copy(src_proc.retlabels)

            self.__proc_addr.append((name, self.proc.offset))
            self.body = ""

            if name in self.__function_name_remapping:
                self.body += "int %s() {\ngoto %s;\n" % (
                    self.__function_name_remapping[name], self.__context.entry_point)
            else:
                entry_point = ''
                try:
                    g = self.__context.get_global(self.__context.entry_point)
                except:
                    g = None
                if g and isinstance(g, op.label) and g.proc == self.proc:
                    entry_point = self.__context.entry_point
                self.body += self.proc_strategy.function_header(name, entry_point)

            # logging.info(name)
            # self.proc.optimize()
            # self.__unbounded = []
            self.proc.visit(self, skip)

            '''
            labels = OrderedDict()
            for k, v in self.__context.get_globals().items():
                if isinstance(v, op.label) and v.used and v.proc == self.proc:
                        labels[k] = v
            '''

            self.body += produce_jump_table(self.proc.provided_labels)

            if name not in self.__skip_output:
                self.__translated.append(self.body)

            self.proc = None

            if self.__pushpop_count != 0:
                logging.warning("push/pop balance = %d non zero at the exit of proc" % self.__pushpop_count)
            return True
        except (CrossJump, op.Unsupported) as e:
            logging.error("%s: ERROR: %s" % (name, e))
            self.__failed.append(name)
        except:
            raise

    def generate(self, start):
        fname = self.__namespace.lower() + ".cpp"
        header = self.__namespace.lower() + ".h"
        logging.info(f' *** Generating output files in C++ {fname} {header}')

        cpp_assign, _, _, cpp_extern = self.produce_c_data(self.__context.segments)

        if sys.version_info >= (3, 0):
            cppd = open(fname, "wt", encoding=self.__codeset)
            hd = open(header, "wt", encoding=self.__codeset)
        else:
            cppd = open(fname, "wt")
            hd = open(header, "wt")

        banner = """/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */
#include <algorithm>
#include <iterator>
"""

        hid = "__M2C_%s_STUBS_H__" % self.__namespace.upper().replace('-', '_')

        hd.write(f"""#ifndef {hid}
#define {hid}

{banner}""")

        hd.write(self.proc_strategy.get_strategy())

        cppd.write(f"""{banner}
#include \"{header}\"
#include <curses.h>

""")

        if self.__context.main_file:
            g = self.__context.get_global(self.__context.entry_point)
            if isinstance(g, op.label):
                cppd.write(f"""
                 void {self.__context.entry_point}(m2c::_offsets, struct m2c::_STATE* _state){{{g.proc}(m2c::k{self.__context.entry_point}, _state);}}
                """)
            cppd.write(f"""namespace m2c{{ m2cf* _ENTRY_POINT_ = &{self.__context.entry_point};}}
""")

        '''
        if self.__context.main_file:
#            cppd.write("""
 int init(struct _STATE* _state)
 {
    X86_REGREF
    
    m2c::log_debug("~~~ heap_size=%%d heap_para=%%d heap_seg=%%s\\n", HEAP_SIZE, (HEAP_SIZE >> 4), seg_offset(heap) );
    /* We expect ram_top as Kbytes, so convert to paragraphs */
    mcb_init(seg_offset(heap), (HEAP_SIZE >> 4) - seg_offset(heap) - 1, MCB_LAST);
    
    R(MOV(ss, seg_offset(stack)));
 #if _BITS == 32
    esp = ((dd)(db*)&stack[STACK_SIZE - 4]);
 #else
    esp = 0;
    sp = STACK_SIZE - 4;
    es = 0;
    *(dw*)(raddr(0, 0x408)) = 0x378; //LPT
 #endif
    
    return(0);
 }
#""")
'''
        # self.__proc_queue.append(start)
        # while len(self.__proc_queue):
        self.merge_procs()

        for p in sorted(self.grouped):
            self.body += f"""
 void {p}(m2c::_offsets, struct m2c::_STATE* _state){{{self.groups[p]}(m2c::k{p}, _state);}}
"""
        self.__translated.append(self.body)

        for name in self.__procs:
            self.__proc(name)
            self.__proc_done.append(name)
            self.__methods.append(name)
        # self.write_stubs("_stubs.cpp", self.__failed)
        self.__methods += self.__failed
        done, failed = len(self.__proc_done), len(self.__failed)

        cppd.write("\n")
        cppd.write("\n".join(self.__translated))
        cppd.write("\n")

        logging.info(
            "%d ok, %d failed of %d, %3g%% translated" % (done, failed, done + failed, 100.0 * done / (done + failed)))
        logging.info("\n".join(self.__failed))

        cppd.write(self.produce_global_jump_table(list(self.__context.get_globals().items()), self.__context.itislst))

        hd.write(f"""
#include "asm.h"

{self.produce_structures(self.__context.structures)}
""")

        hd.write(cpp_extern)

        labeloffsets = self.produce_label_offsets()
        hd.write(labeloffsets)

        hd.write(self.proc_strategy.write_declarations(self.__procs + list(self.grouped), self.__context))

        data = self.produce_externals(self.__context)
        hd.write(data)

        hd.write("\n#endif\n")
        hd.close()

        cppd.write(f"""
#include <algorithm>
#include <iterator>
#ifdef DOSBOX
#include <numeric>

 #define MYCOPY(x) {{m2c::set_type(x);m2c::mycopy((db*)&x,(db*)&tmp999,sizeof(tmp999),#x);}}

 namespace m2c {{
  void   Initializer()
#else
 #define MYCOPY(x) std::copy(std::begin(tmp999),std::end(tmp999),std::begin(x));
 namespace {{
  struct Initializer {{
   Initializer()
#endif
{{
{cpp_assign}
}}
#ifndef DOSBOX
  }};
 static const Initializer i;
#endif
}}
""")

        cppd.close()

        self.write_segment(self.__context.segments, self.__context.structures)

    def merge_procs(self):
        '''
        Merge procs in case they have cross jumps since incompatible with C

        :return:
        '''
        if not self.__context.args.singleproc:
            for index, first_proc_name in enumerate(self.__procs):
                first_proc = self.__context.get_global(first_proc_name)

                labels = set()  # leave only real labels
                for label_name in first_proc.used_labels:
                    first_label = self.__context.get_global(label_name)
                    if isinstance(first_label, (op.label, proc_module.Proc)):
                        labels.add(label_name)
                first_proc.used_labels = labels
                logging.debug(f"Proc {first_proc_name} used labels {first_proc.used_labels}")
                logging.debug(f"                   provided labels {first_proc.provided_labels}")

                missing = first_proc.used_labels - first_proc.provided_labels
                logging.debug(f"                    missing labels {missing}")
                proc_to_merge = set()
                if not first_proc.if_terminated_proc():
                    '''If execution does not terminated in the procedure range when merge it with next proc'''
                    if index + 1 < len(self.__procs):
                        logging.info(
                            f"Execution does not terminated need to merge {first_proc_name} with {self.__procs[index + 1]}")
                        proc_to_merge.add(self.__procs[index + 1])
                    else:
                        logging.info(f"Execution does not terminated could not find proc after {first_proc_name}")
                if missing:
                    proc_to_merge.add(first_proc_name)
                    for l in missing:
                        first_label = self.__context.get_global(l)
                        if isinstance(first_label, op.label):
                            logging.debug(f" {l} is label, will merge {first_label.proc} proc")
                            proc_to_merge.add(first_label.proc)  # if label then merge proc implementing it
                        elif isinstance(first_label, proc_module.Proc):
                            logging.debug(f" {l} is proc, will merge {first_label.name} proc")
                            proc_to_merge.add(first_label.name)

                if self.__context.args.procperseg:
                    for pname in self.__procs:
                        if pname != first_proc_name:
                            p_proc = self.__context.get_global(pname)
                            if first_proc.segment == p_proc.segment:
                                proc_to_merge.add(pname)

                first_proc.to_group_with = proc_to_merge
                logging.debug(f" will merge {proc_to_merge}")
            changed = True
            iteration = 0
            while changed:
                iteration += 1
                logging.info(f"     Identifing proc to merge #{iteration}")
                changed = False
                for first_proc_name in self.__procs:
                    logging.debug(f"Proc {first_proc_name}")
                    first_proc = self.__context.get_global(first_proc_name)
                    for next_proc_name in first_proc.to_group_with:
                        if first_proc_name != next_proc_name:
                            logging.debug(f"  will group with {next_proc_name}")
                            next_proc = self.__context.get_global(next_proc_name)
                            if not next_proc.to_group_with:
                                next_proc.to_group_with = set()
                            if first_proc.to_group_with != next_proc.to_group_with:
                                next_proc.to_group_with = set.union(next_proc.to_group_with, first_proc.to_group_with)
                                first_proc.to_group_with = next_proc.to_group_with
                                changed = True
                    logging.debug(f"  will group with {first_proc.to_group_with}")
            for first_proc_name in self.__procs:
                first_proc = self.__context.get_global(first_proc_name)
                if first_proc.to_group_with:
                    logging.info(f"     ~{first_proc_name}")
                    for p_name in first_proc.to_group_with:
                        logging.info(f"       {p_name}")
        groups = []
        groups_id = 1
        for first_proc_name in self.__procs:
            if first_proc_name not in self.grouped:
                first_proc = self.__context.get_global(first_proc_name)
                if self.__context.args.singleproc or first_proc.to_group_with:
                    logging.debug(f"Merging {first_proc_name}")
                    new_group_name = f'_group{groups_id}'
                    first_label = op.label(first_proc_name, proc=new_group_name, isproc=False,
                                           line_number=first_proc.line_number, far=first_proc.far)
                    first_label.real_offset, first_label.real_seg = first_proc.real_offset, first_proc.real_seg

                    first_label.used = True
                    first_proc.stmts.insert(0, first_label)
                    first_proc.provided_labels.add(first_proc_name)
                    self.__context.reset_global(first_proc_name, first_label)
                    self.grouped.add(first_proc_name)

                    self.groups[first_proc_name] = new_group_name
                    # self.grouped |= first_proc.group
                    for next_proc_name in self.__procs:
                        if next_proc_name != first_proc_name and (
                                self.__context.args.singleproc or next_proc_name in first_proc.to_group_with):  # Maintaining initial proc order
                            next_proc = self.__context.get_global(next_proc_name)
                            if isinstance(next_proc, proc_module.Proc):  # and first_proc.far == next_proc.far:
                                self.groups[next_proc_name] = new_group_name
                                next_label = op.label(next_proc_name, proc=first_proc_name, isproc=False,
                                                      line_number=next_proc.line_number, far=next_proc.far)
                                next_label.real_offset, next_label.real_seg = next_proc.real_offset, next_proc.real_seg
                                next_label.used = True
                                first_proc.add_label(next_proc_name, next_label)
                                logging.debug(f"     with {next_proc_name}")
                                first_proc.merge_two_procs(new_group_name, next_proc)
                                self.__context.reset_global(next_proc_name, next_label)
                                self.grouped.add(next_proc_name)
                    groups += [new_group_name]
                    self.__context.set_global(new_group_name, first_proc)
                    groups_id += 1
        self.__procs = [x for x in self.__procs if x not in self.grouped]
        self.__procs += groups

    def write_segment(self, segments, structs):
        jsonpickle.set_encoder_options('json', indent=2)
        with open(self.__namespace.lower() + '.seg', 'w') as outfile:
            outfile.write(jsonpickle.encode((segments, structs)))

    def produce_data_cpp(self, asm_files):
        self.generate_data(*self.read_segments(asm_files))

    def read_segments(self, asm_files):
        logging.info(" *** Merging .seg files")
        segments = OrderedDict()
        structs = OrderedDict()
        for file in asm_files:
            file = file.replace('.asm', '.seg').replace('.lst', '.seg')
            logging.info(f'     Merging data from {file}')
            with open(file, 'rt') as infile:
                segments, structures = self.merge_segments(segments, structs, *jsonpickle.decode(infile.read()))
        return segments, structures

    def merge_segments(self, allsegments: OrderedDict, allstructs: OrderedDict, newsegments: OrderedDict,
                       newstructs: OrderedDict):
        if self.merge_data_segments:
            logging.info('Will merge public data segments')
        for k, v in newsegments.items():
            segclass = v.segclass
            ispublic = v.options and 'public' in v.options
            if segclass and ispublic and self.merge_data_segments:
                if segclass not in allsegments:
                    allsegments[segclass] = v
                else:
                    data = v.getdata()
                    # allsegments[segclass].insert_label(data[0])
                    for d in data:
                        allsegments[segclass].append(d)
            else:
                if k in allsegments and (v.getsize() > 0 or allsegments[k].getsize() > 0):
                    old = jsonpickle.encode(allsegments[k], unpicklable=False)
                    new = jsonpickle.encode(v, unpicklable=False)
                    if old != new:
                        logging.error(f'Overwritting segment {k}')
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

    def generate_data(self, segments, structures):
        logging.info(" *** Producing _data.cpp and _data.h files")
        _, data_h, data_cpp_reference, _ = self.produce_c_data(segments)
        fname = "_data.cpp"
        header = "_data.h"
        if sys.version_info >= (3, 0):
            fd = open(fname, "wt", encoding=self.__codeset)
            hd = open(header, "wt", encoding=self.__codeset)
        else:
            fd = open(fname, "wt")
            hd = open(header, "wt")

        data_impl = f'''#include "_data.h"
namespace m2c{{
static struct Memory mm;
struct Memory& m = mm;

static struct Memory t;
struct Memory& types = t;

db(& stack)[STACK_SIZE]=m.stack;
db(& heap)[HEAP_SIZE]=m.heap;
}}
{data_cpp_reference}
        '''

        fd.write(data_impl)

        # hdata_bin = self.__hdata_seg
        data = '''
#ifndef ___DATA_H__
#define ___DATA_H__
#include "asm.h"
''' + self.produce_structures(structures) + self.produce_data(data_h) + '''
#endif
'''
        hd.write(data)

        fd.write("\n")
        fd.close()

    def produce_label_offsets(self):
        # hd.write("\nenum _offsets MYINT_ENUM {\n")
        offsets = []
        '''        
        for k, v in list(self.__context.get_globals().items()):
            k = re.sub(r'[^A-Za-z0-9_]', '_', k)
            if isinstance(v, (op.label, proc_module.Proc)):
                offsets.append((k.lower(), hex(v.line_number)))
        offsets = sorted(offsets, key=lambda t: t[1])
        '''
        labeloffsets = """namespace m2c{
void   Initializer();
static const dd kbegin = 0x1001;
"""
        i = 0x1001
        for k, v in list(self.__context.get_globals().items()):
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
                structures += f"  {member.type} {member.label};\n"
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
#ifdef DOSBOX
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
        self.a = self.expand(dst, destination=True, lea=True)
        self.b = self.expand(src, lea=True)
        r = "%s = %s" % (self.a, self.b)
        self.lea = False
        return r

    def _movs(self, dst, src):
        size = self.get_size(dst)
        dstr, srcr = Token.find_tokens(dst, REGISTER), Token.find_tokens(src, REGISTER)
        self.a, self.b = self.parse2(dst, src)
        return "MOVS(%s, %s, %s, %s, %d" % (self.a, self.b, dstr[0], srcr[0], size)

    def _repe(self):
        # return "\tREPE\n"
        self.prefix = '\tREPE '
        return ''

    def _repne(self):
        # return "\tREPNE\n"
        self.prefix = '\tREPNE '
        return ''

    def _lods(self, src):
        size = self.get_size(src)
        self.a = self.expand(src)
        srcr = Token.find_tokens(src, REGISTER)
        return "LODS(%s,%s,%d)" % (self.a, srcr[0], size)

    def _leave(self):
        return "LEAVE"  # MOV(esp, ebp) POP(ebp)

    def _int(self, dst):
        self.a = self.expand(dst)
        return "_INT(%s)" % self.a

    def _instruction0(self, cmd):
        return "%s" % (cmd.upper())

    def _instruction1(self, cmd, dst):
        self.a = self.expand(dst)
        return "%s(%s)" % (cmd.upper(), self.a)

    def _jump(self, cmd, label):
        result = self.isrelativejump(label)
        if result:
            return "\n"
        else:
            label, far = self.jump_post(label)  # TODO
            return "%s(%s)" % (cmd.upper(), label)

    def isrelativejump(self, label):
        result = '$' in str(label)  # skip j* $+2
        return result

    def _instruction2(self, cmd, dst, src):
        self.a, self.b = self.parse2(dst, src)
        return "%s(%s, %s)" % (cmd.upper(), self.a, self.b)

    def _instruction3(self, cmd, dst, src, c):
        self.a, self.b = self.parse2(dst, src)
        self.c = self.expand(c)
        return "%s(%s, %s, %s)" % (cmd.upper(), self.a, self.b, self.c)

    def return_empty(self, _):
        return []

    def _assignment(self, stmt, dst, src):
        src = Token.remove_tokens(src, ['expr'])
        size = self.get_size(src)
        ptrdir = Token.find_tokens(src, 'ptrdir')
        if ptrdir:
            type = ptrdir[0]
            if isinstance(type, Token):
                type = type.value
            type = type.lower()
            src = Token.find_and_replace_tokens(src, 'ptrdir', self.return_empty)
        o = stmt  # self.__context.get_global(dst)
        o.size = size
        if ptrdir:
            o.original_type = type
        o.implemented = True
        self.__context.reset_global(dst, o)

        self.label += "#undef %s\n#define %s %s\n" % (dst, dst, self.expand(src))
        return ''

    def _equ(self, dst, src):
        self.label += "#define %s %s\n" % (dst, self.expand(src))
        return ''

    @staticmethod
    def produce_c_data_single(data):
        # For unit test
        from masm2c.parser import Parser
        Parser.c_dummy_label = 0
        c, h, size = Cpp.produce_c_data_single_(data)
        c += ", // " + data.getlabel() + "\n"  # TODO can put original_label
        h += ";\n"
        return c, h, size

    @staticmethod
    def produce_c_data_single_(data):
        # Real conversion
        internal_data_type = data.getinttype()

        logging.debug(f"current data type = {internal_data_type}")
        rc, rh = {DataType.NUMBER: Cpp.produce_c_data_number,
                  DataType.ARRAY: Cpp.produce_c_data_array,
                  DataType.ZERO_STRING: Cpp.produce_c_data_zero_string,
                  DataType.ARRAY_STRING: Cpp.produce_c_data_array_string,
                  DataType.OBJECT: Cpp.produce_c_data_object
                  }[internal_data_type](data)

        logging.debug(rc)
        logging.debug(rh)
        return rc, rh, data.getsize()

    @staticmethod
    def produce_c_data_number(data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        rc = ''.join([str(i) for i in r])
        rh = f'{data_ctype} {label}'
        return rc, rh

    @staticmethod
    def produce_c_data_array(data: op.Data):
        label, data_ctype, _, r, elements, _ = data.getdata()
        rc = '{'
        for i, v in enumerate(r):
            if i != 0:
                rc += ','
            if isinstance(v, op.Data):
                c, _, _ = Cpp.produce_c_data_single_(v)
                rc += c
            else:
                rc += str(v)
        rc += '}'
        # assert(len(r)==elements)
        rh = f'{data_ctype} {label}[{elements}]'
        return rc, rh

    @staticmethod
    def produce_c_data_zero_string(data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        rc = '"' + ''.join([Cpp.convert_str(i) for i in r[:-1]]) + '"'
        rc = re.sub(r'(\\x[0-9a-f][0-9a-f])([0-9a-f])', r'\g<1>" "\g<2>', rc)   # fix for stupid C hex escapes: \xaef
        rh = f'char {label}[{str(len(r))}]'
        return rc, rh

    @staticmethod
    def produce_c_data_array_string(data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        rc = '{' + ",".join([Cpp.convert_char(i) for i in r]) + '}'
        rh = f'char {label}[{str(len(r))}]'
        return rc, rh

    @staticmethod
    def produce_c_data_object(data: op.Data):
        label, data_ctype, _, r, elements, size = data.getdata()
        # rc = '{' + ",".join([str(i) for i in r]) + '}'
        rc = list()
        for i in data.getmembers():
            c, _, _ = Cpp.produce_c_data_single_(i)
            rc += [c]
        rc = '{' + ','.join(rc) + '}'
        rh = f'{data_ctype} {label}'
        return rc, rh

    @staticmethod
    def convert_char(c):
        if isinstance(c, int) and c not in [10, 13]:
            return str(c)
        return "'" + Cpp.convert_str(c) + "'"

    @staticmethod
    def convert_str(c):
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
            # vvv = "'" + vvv + "'"
        return vvv

    def dump_globals(self):
        fname = self.__namespace.lower() + ".list"
        logging.info(f' *** Generating globals listing {fname}')

        jsonpickle.set_encoder_options('json', indent=2)
        with open(fname, 'w') as lst:
            lst.write(f'Segment:\n')
            for v in self.__context.segments:
                lst.write(f'{v}\n')

            lst.write(f'\nLabels:\n')
            for k, v in self.__context.get_globals().items():
                if isinstance(v, op.label):
                    lst.write(f'{v.name}\n')

            lst.write(f'\nProcs:\n')
            for k, v in self.__context.get_globals().items():
                if isinstance(v, proc_module.Proc):
                    lst.write(f'{v.name} {v.offset}\n')

            lst.write(f'\nVars:\n')
            for k, v in self.__context.get_globals().items():
                if isinstance(v, op.var):
                    lst.write(f'{v.name} {v.offset}\n')

            lst.write(
                jsonpickle.encode((self.__context.get_globals(), self.__context.segments, self.__context.structures)))

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
        offsets = []
        for k, v in globals:
            k = re.sub(r'[^A-Za-z0-9_]', '_', k)
            if isinstance(v, proc_module.Proc) and v.used:
                offsets.append((k.lower(), k))

                for label in sorted(v.provided_labels):
                    if label != v.name:
                        result += f"        case m2c::k{label}: \t{v.name}(__disp, _state); break;\n"

        offsets = sorted(offsets, key=lambda t: t[1])
        for name, label in offsets:
            logging.debug(f'{name}, {label}')
            if not name.startswith('_group'):  # TODO remove dirty hack. properly check for group
                result += "        case m2c::k%s: \t%s(0, _state); break;\n" % (name, cpp_mangle_label(label))

        result += "        default: m2c::log_error(\"Call to nowhere to 0x%x. See line %d\\n\", __disp, __LINE__);m2c::stackDump(_state); abort();\n"
        result += "     };\n     return true;\n}\n"
        return result
