from __future__ import division
from __future__ import print_function

import logging
import re
import sys
from builtins import hex
from builtins import object
from builtins import range
from builtins import str
from copy import copy

import masm2c.proc as proc_module
from masm2c import op
from masm2c.Token import Token

OFFSETDIR = 'offsetdir'
LABEL = 'LABEL'
PTRDIR = 'ptrdir'
REGISTER = 'register'
SEGMENTREGISTER = 'segmentregister'
SEGOVERRIDE = 'segoverride'
SQEXPR = 'sqexpr'

class InjectCode(Exception):

    def __init__(self, cmd):
        self.cmd = cmd
        super().__init__()

class SkipCode(Exception):
    pass

class CrossJump(Exception):
    pass

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


def convert_number_to_c(expr, radix = 10):
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
            expr = re.sub(r'^([+-]?)([0-8]+)[OoQq]?$', '\g<1>0\g<2>', expr)
        elif radix == 16:
            expr = re.sub(r'^([+-]?)([0-9][0-9A-Fa-f]*)[Hh]?$', '\g<1>0x\g<2>', expr)
        elif radix == 10:
            expr = re.sub(r'^([+-]?)([0-9]+)[Dd]?$', '\g<1>\g<2>', expr)
        elif radix == 2:
            expr = re.sub(r'^([+-]?)([0-1]+)[Bb]?$', parse_bin, expr)  # convert binary
        else:
            expr = str(int(expr, radix))
    except:
        logging.error("Failed to parse number " + expr)

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
    logging.debug('get_size res %d' % size)
    return size


def mangle2_label(name):
    name = name.lower()
    return re.sub(r'\$', '_tmp', name)


class Cpp(object):
    def __init__(self, context, outfile="", skip_first=0, blacklist=[], skip_output=None, skip_dispatch_call=False,
                 skip_addr_constants=False, header_omit_blacklisted=False, function_name_remapping=None):
        FORMAT = "%(filename)s:%(lineno)d %(message)s"
        logging.basicConfig(format=FORMAT)

        self.__namespace = outfile
        self.__indirection = 0
        self.__current_size = 0
        self.__work_segment = ""
        self.__codeset = 'cp437'
        self.__context = context

        self.__cdata_seg = ""
        self.__hdata_seg = ""
        for i in context.segments.values():
            for j in i.getdata():
                c, h, size = self.produce_c_data(j)
                self.__cdata_seg += c
                self.__hdata_seg += h

        self.__procs = context.proc_list
        self.__proc_queue = []
        self.__proc_done = []
        self.__blacklist = blacklist
        self.__failed = list(blacklist)
        self.__skip_output = skip_output
        self.__skip_dispatch_call = skip_dispatch_call
        self.__skip_addr_constants = skip_addr_constants
        self.__function_name_remapping = function_name_remapping
        self.__translated = list()  # []
        self.__proc_addr = []
        self.__used_data_offsets = set()
        self.__methods = []
        self.__pushpop_count = 0
        self.lea = False
        self.__far = False
        self.size_changed = False
        self.address = False
        self.body = ""

    def convert_label(self, token):
        name_original = token.value
        name = name_original.lower()
        logging.debug("convert_label name = %s indirection = %u" % (name, self.__indirection))

        if self.__indirection == -1:
            try:
                offset, _, _ = self.__context.get_offset(name)
            except:
                pass
            else:
                logging.debug("OFFSET = %s" % offset)
                self.__indirection = 0
                self.__used_data_offsets.add((name, offset))
                return Token('LABEL', "k" + name)

        try:
            g = self.__context.get_global(name)
        except:
            # logging.warning("expand_cb() global '%s' is missing" % name)
            return token

        if isinstance(g, op._equ):
            logging.debug("it is equ")
            if g.implemented == False:
                raise InjectCode(g)
            value = g.original_name
            # value = self.expand_equ(g.value)
            logging.debug("equ: %s -> %s" % (name, value))
        elif isinstance(g, op._assignment):
            logging.debug("it is assignment")
            if g.implemented == False:
                raise InjectCode(g)
            value = g.original_name
            # value = self.expand_equ(g.value)
            logging.debug("assignment %s = %s" % (name, value))
        elif isinstance(g, proc_module.Proc):
            logging.debug("it is proc")
            if self.__indirection != -1:
                logging.error("proc %s offset %s" % (str(proc_module.Proc), str(g.offset)))
                raise Exception("invalid proc label usage")
            value = str(g.offset)
            self.__indirection = 0
        elif isinstance(g, op.var):
            logging.debug("it is var " + str(g.size))
            size = g.size
            if self.__current_size == 0:  # TODO check
                self.__current_size = size
            if size == 0 and not g.issegment:
                raise Exception("invalid var '%s' size %u" % (name, size))
            if g.issegment:
                value = "seg_offset(%s)" % (name_original.lower())
                self.__indirection = 0
            else:
                self.address = False
                if g.elements != 1:
                    self.address = True
                if g.elements == 1 and self.__isjustlabel and not self.lea and g.size == self.__current_size:
                    # traceback.print_stack(file=sys.stdout)
                    value = "m." + g.name
                    self.__indirection = 0
                else:
                    if self.__indirection == 1 and self.variable:
                        value = "m.%s" % g.name
                        if not self.__isjustlabel: # if not just single label
                            self.address = True
                            if g.elements == 1: # array generates pointer himself
                                value = "&" + value

                            if g.getsize() == 1: # if byte no need for (db*)
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
            value = "k" + g.name.lower()  # .capitalize()
        else:
            if isinstance(g, op.Struct):
                pass
            size = g.getsize()
            if size == 0:
                raise Exception("invalid var '%s' size %u" % (name, size))
            if self.__indirection == 0 or self.__indirection == 1:  # x0r self.indirection == 1 ??
                value = "offsetof(struct Mem,%s)" % name_original
                if self.__indirection == 1:
                    self.__indirection = 0
            elif self.__indirection == -1:
                value = "%s" % g.offset
                self.__indirection = 0
            else:
                raise Exception("invalid indirection %d name '%s' size %u" % (self.__indirection, name, size))
        return Token('LABEL', value)

    def get_size(self, expr):
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
        if issqexpr:
            return 0

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

        if isinstance(expr, list):
            return max([self.get_size(i) for i in expr])

        offsetdir = Token.find_tokens(expr, 'offsetdir')
        if offsetdir:
            return 2  # TODO 16 bit word size

        # if isinstance(expr, str):  # in ('+','-','*','(',')','/'):
        #    return 0
        if isinstance(expr, str):
            from masm2c.parser import Parser
            return Parser.is_register(expr)
        return 0

    def convert_sqbr_reference(self, expr, destination, size, islabel, lea=False):
        if not lea or destination:
            if not islabel or not self.variable:
                self.address = True
                if size == 1:
                    expr = "raddr(%s,%s)" % (self.__work_segment, expr)
                elif size == 2:
                    expr = "(dw*)(raddr(%s,%s))" % (self.__work_segment, expr)
                elif size == 4:
                    expr = "(dd*)(raddr(%s,%s))" % (self.__work_segment, expr)
                elif size == 8:
                    expr = "(dq*)(raddr(%s,%s))" % (self.__work_segment, expr)
                else:
                    logging.error("~%s~ @invalid size 0" % expr)
                    expr = "raddr(%s,%s)" % (self.__work_segment, expr)
            else:
                if self.size_changed: # or not self.__isjustlabel:
                    if size == 1:
                        expr = "(db*)(%s)" % expr
                    elif size == 2:
                        expr = "(dw*)(%s)" % expr
                    elif size == 4:
                        expr = "(dd*)(%s)" % expr
                    elif size == 8:
                        expr = "(dq*)(%s)" % expr
                    else:
                        logging.error("~%s~ @invalid size 0" % expr)
                        #expr = "(dw*)(%s)" % expr
            logging.debug("expr: %s" % expr)
        return expr

    def tokenstostring(self, expr):
        if isinstance(expr, list):
            result = "".join([self.tokenstostring(i) for i in expr])
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

            return self.tokenstostring(expr.value)
        return expr

    def expand(self, expr, def_size=0, destination=False, lea=False):
        logging.debug("EXPAND(expr:\"%s\")" % expr)

        expr = Token.remove_tokens(expr, ['expr'])
        origexpr = expr
        self.__work_segment = "ds"
        self.__current_size = 0
        self.size_changed = False
        self.address = False
        indirection = 0
        size = self.get_size(expr) if def_size == 0 else def_size  # calculate size if it not provided
        # self.__expr_size = size

        # calculate the segment register
        segoverride = Token.find_tokens(expr, SEGOVERRIDE)
        sqexpr = Token.find_tokens(expr, SQEXPR)
        if sqexpr:
            indirection = 1
        if segoverride:
            expr = Token.remove_tokens(expr, [SEGMENTREGISTER])

        offsetdir = Token.find_tokens(expr, OFFSETDIR)
        if offsetdir:
            indirection = -1
            expr = offsetdir

        ptrdir = Token.find_tokens(expr, PTRDIR)
        if ptrdir:
            indirection = 1

        if ptrdir or offsetdir or segoverride:
            expr = Token.remove_tokens(expr, [PTRDIR, OFFSETDIR, SEGOVERRIDE])

        if sqexpr:
            expr, _ = Token.remove_squere_bracets(expr)

        memberdir = Token.find_tokens(expr, 'memberdir')
        islabel = Token.find_tokens(expr, LABEL)
        self.variable = False
        if islabel and not offsetdir and not memberdir:
                for i in islabel:
                    res = self.get_var_size(i)
                    if res:
                        self.variable = True
                        size = res
                        indirection = 1
                        break
        if lea:
            indirection = -1

        if indirection == 1 and not segoverride:
            regs = Token.find_tokens(expr, REGISTER)
            if regs and any([i in ['bp', 'ebp', 'sp', 'esp'] for i in regs]):  # TODO doublecheck
                self.__work_segment = "ss"
                self.variable = False
        if segoverride:
            self.__work_segment = segoverride[0].value

        self.__current_size = size
        newsize = size
        if ptrdir:
            value = ptrdir[0]
            # logging.debug('get_size res 1')
            newsize = self.__context.typetosize(value)
            if newsize != size:
                self.size_changed = True
            else:
                origexpr = Token.remove_tokens(origexpr, [PTRDIR, SQEXPR])
                if isinstance(origexpr, list) and len(origexpr)==1:
                    origexpr = origexpr[0]

        # for "label" or "[label]" get size
        self.__isjustlabel = (isinstance(origexpr, Token) and origexpr.type == LABEL) \
                             or (isinstance(origexpr, Token) and origexpr.type == SQEXPR \
                                 and isinstance(origexpr.value, Token) and origexpr.value.type == LABEL) \
                            or (isinstance(origexpr, Token) and origexpr.type == 'memberdir')


        if memberdir:
            expr = memberdir[0]
            label = islabel
            g = None
            try:
                g = self.__context.get_global(label[0])
                if isinstance(g, (op.var, op.Struct)):
                    if indirection == -1:
                        expr = ["offset(%s,%s" % (g.segment, g.name)]+expr[1:]+[')']
                    elif indirection == 0:
                        self.address = True
                        expr = ["m." + (".".join(label))]
                    elif indirection == 1:
                        registers = Token.find_tokens(expr, 'register')
                        if not registers:
                            register = []
                        integers = Token.find_tokens(expr, 'INTEGER')
                        if not integers:
                            integers = []
                        expr = ["(*(%s*)(raddr(%s,%s))).%s" % (label[0], self.__work_segment, "+".join(registers+integers), ".".join(label[1:]))]
            except:
                pass
        else:
            self.__indirection = indirection
            expr = Token.find_and_replace_tokens(expr, LABEL, self.convert_label)
            indirection = self.__indirection
        if self.__current_size != 0:  # and (indirection != 1 or size == 0):
            size = self.__current_size

        if self.size_changed:
            size = newsize

        expr = self.tokenstostring(expr)

        if indirection == 1 and not memberdir and (not self.__isjustlabel or self.size_changed):
            expr = self.convert_sqbr_reference(expr, destination, size, islabel, lea=lea)
        if indirection == 1 and self.address:
            if expr[0] == '(' and expr[-1] == ')':
                expr = "*%s" % expr
            else:
                expr = "*(%s)" % expr

        return expr

    def get_var_size(self, name):
        size = 0
        if self.__context.has_global(name):
            g = self.__context.get_global(name)
            if isinstance(g, (op.var, op.Struct, op._equ, op._assignment)):
                size = g.getsize()
        return size

    def jump_to_label(self, name):
        logging.debug("jump_to_label(%s)" % name)
        name = Token.remove_tokens(name, ['expr'])

        # name = name.strip()
        jump_proc = False

        self.__far = False
        # name_original = name

        # prog = re.compile(r'^\s*(near|far|short)\s*(ptr)?\s*', re.I)  # x0r TODO
        # name = re.sub(prog, '', name)
        indirection = -5

        segoverride = Token.find_tokens(name, 'segoverride')
        if segoverride:
            self.__work_segment = segoverride[0].value
        #    name = Token.remove_tokens(name, ['segoverride', 'segmentregister'])

        if isinstance(name, Token) and name.type == 'register':
            name = name.value
            indirection = 0  # based register value

        labeldir = Token.find_tokens(name, 'LABEL')
        if labeldir:
            labeldir[0] = self.__context.mangle_label(mangle2_label(labeldir[0]))
            if self.__context.has_global(labeldir[0]):
                g = self.__context.get_global(labeldir[0])
                if isinstance(g, op.var):
                    indirection = 1  # []
                elif isinstance(g, op.label):
                    indirection = -1  # direct using number
            else:
                name = labeldir[0]

        ptrdir = Token.find_tokens(name, 'ptrdir')
        if ptrdir:
            if any(isinstance(x, str) and x.lower() in ['near', 'far', 'short'] for x in ptrdir):
                indirection = -1  #
            else:
                indirection = 1

        sqexpr = Token.find_tokens(name, 'sqexpr')
        if sqexpr:
            indirection = 1

        if indirection == 1:
            name = self.expand(name)

        if indirection == -1:
            if labeldir:
                name = labeldir[0]

        # name = self.resolve_label(name)
        logging.debug("label %s" % name)
        hasglobal = False
        if name in self.__blacklist:
            jump_proc = True

        if self.__context.has_global(name):
            hasglobal = True
            g = self.__context.get_global(name)
            if isinstance(g, proc_module.Proc):
                jump_proc = True

        if jump_proc:
            if name in self.__function_name_remapping:
                return "%s" % self.__function_name_remapping[name]
            else:
                return name
        else:
            # TODO: name or self.resolve_label(name) or self.mangle_label(name)??
            if name in self.proc.retlabels:
                return "return /* (%s) */" % name
            ## x0r return "goto %s" %self.resolve_label(name)
            if not hasglobal:
                ##name = self.expand_old(name, destination=True)  # TODO
                self.body += "__disp = (dw)(" + name + ");\n"
                name = "__dispatch_call"
            else:
                if isinstance(g, op.label) and g.far:
                    self.__far = True  # make far calls to far procs

            if ptrdir:
                if any(isinstance(x, str) and x.lower() == 'far' for x in ptrdir):
                    self.__far = True
                elif any(isinstance(x, str) and x.lower() == 'near' for x in ptrdir):
                    self.__far = False

        return name

    def _label(self, name, proc):
        ret = ""
        if proc:
            ret += " // Procedure %s() start\n" % (name)
        ret += "%s:\n" % mangle2_label(name)
        return ret

    def schedule(self, name):
        name = name.lower()
        if name in self.__proc_queue or name in self.__proc_done or name in self.__failed:
            return
        logging.debug("+scheduling function %s..." % name)
        self.__proc_queue.append(name)

    def _call(self, name):
        logging.debug("cpp._call(%s)" % str(name))
        ret = ""
        # dst = self.expand(name, destination = False)
        dst = self.jump_to_label(name)
        if dst != "__dispatch_call":
            dst = "k" + dst
        else:
            dst = "__disp"

        if self.__far:
            ret += "\tR(CALLF(%s));\n" % (dst)
        else:
            ret += "\tR(CALL(%s));\n" % (dst)
        '''
                name = name.lower()
                if self.is_register(name):
                        ret += "\t__dispatch_call(%s);\n" %self.expand(name, 2)
                        return
                if name in self.__function_name_remapping:
                        ret += "\tR(CALL(%s));\n" %self.__function_name_remapping[name]
                else:
                        ret += "\tR(CALL(%s));\n" %name
                self.schedule(name)
        '''
        return ret

    @staticmethod
    def _ret():
        return "\tR(RETN);\n"

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
        self.d, self.s = self.parse2(dst, src)
        #if self.d in ['sp', 'esp'] and check_int(self.s):
        #    self.__pushpop_count -= int(self.s)
        return "\tR(ADD(%s, %s));\n" % (self.d, self.s)

    def _sub(self, dst, src):
        self.d, self.s = self.parse2(dst, src)
        #if self.d in ['sp', 'esp'] and check_int(self.s):
        #    self.__pushpop_count += int(self.s)
        if self.d == self.s:
            return "\t%s = 0;AFFECT_ZF(0); AFFECT_SF(%s,0);\n" % (self.d, self.d)
        else:
            return "\tR(SUB(%s, %s));\n" % (self.d, self.s)

    def _xor(self, dst, src):
        self.d, self.s = self.parse2(dst, src)
        if self.d == self.s:
            return "\t%s = 0;AFFECT_ZF(0); AFFECT_SF(%s,0);\n" % (self.d, self.d)
        else:
            return "\tR(XOR(%s, %s));\n" % (self.d, self.s)

    def _mul(self, src):
        res = []
        size = 0
        for i in src:
            if size == 0:
                size = self.get_size(i)
            else:
                break
        for i in src:
            res.append(self.expand(i, size))
        if size == 0:
            size = self.__current_size
        return "\tR(MUL%d_%d(%s));\n" % (len(src), size, ",".join(res))

    def _imul(self, src):
        res = []
        size = 0
        for i in src:
            if size == 0:
                size = self.get_size(i)
            else:
                break
        for i in src:
            res.append(self.expand(i, size))
        if size == 0:
            size = self.__current_size
        return "\tR(IMUL%d_%d(%s));\n" % (len(src), size, ",".join(res))

    def _div(self, src):
        size = self.get_size(src)
        src = self.expand(src)
        return "\tR(DIV%d(%s));\n" % (size, src)

    def _idiv(self, src):
        size = self.get_size(src)
        src = self.expand(src)
        return "\tR(IDIV%d(%s));\n" % (size, src)

    def _jz(self, label):
        result = self.isrelativejump(label)
        if result:
            return "\n"
        else:
            label = self.jump_to_label(label)  # TODO
            return "\t\tR(JZ(%s));\n" % label

    def _jnz(self, label):
        label = self.jump_to_label(label)
        return "\t\tR(JNZ(%s));\n" % label

    def _jbe(self, label):
        label = self.jump_to_label(label)
        return "\t\tR(JBE(%s));\n" % label

    def _ja(self, label):
        label = self.jump_to_label(label)
        return "\t\tR(JA(%s));\n" % label

    def _jc(self, label):
        label = self.jump_to_label(label)
        return "\t\tR(JC(%s));\n" % label

    def _jnc(self, label):
        label = self.jump_to_label(label)
        return "\t\tR(JNC(%s));\n" % label

    '''
    def _push(self, regs):
        p = ""
        for r in regs:
            if self.get_size(r):
                self.__pushpop_count += 2
                r = self.expand(r)
                p += "\tR(PUSH(%s));\n" % (r)
        return p

    def _pop(self, regs):
        p = ""
        for r in regs:
            self.__pushpop_count -= 2
            r = self.expand(r)
            p += "\tR(POP(%s));\n" % r
        return p
    '''

    def _rep(self):
        return "\tREP\n"

    def _cmpsb(self):
        return "CMPSB;\n"

    def _lodsb(self):
        return "LODSB;\n"

    def _lodsw(self):
        return "LODSW;\n"

    def _lodsd(self):
        return "LODSD;\n"

    def _stosb(self, n, clear_cx):
        return "STOSB;\n"  # %("" if n == 1 else n, ", true" if clear_cx else "")

    def _stosw(self, n, clear_cx):
        return "STOSW;\n"  # %("" if n == 1 else n, ", true" if clear_cx else "")

    def _stosd(self, n, clear_cx):
        return "STOSD;\n"  # %("" if n == 1 else n, ", true" if clear_cx else "")

    def _movsb(self, n, clear_cx):
        return "MOVSB;\n"  # %("" if n == 1 else n, ", true" if clear_cx else "")

    def _movsw(self, n, clear_cx):
        return "MOVSW;\n"  # %("" if n == 1 else n, ", true" if clear_cx else "")

    def _movsd(self, n, clear_cx):
        return "MOVSD;\n"  # %("" if n == 1 else n, ", true" if clear_cx else "")

    def _scasb(self):
        return "SCASB;\n"

    def _scasw(self):
        return "SCASW;\n"

    def _scasd(self):
        return "SCASD;\n"

    def _scas(self, src):
        size = self.get_size(src)
        src = self.expand(src)
        return "\tR(SCAS(%s,%d));\n" % (src, size)

    def __proc(self, name, def_skip=0):
        logging.debug("cpp::__proc(%s)" % name)
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
                self.proc.labels = copy(src_proc.labels)
                self.proc.retlabels = copy(src_proc.retlabels)

            self.__proc_addr.append((name, self.proc.offset))
            self.body = ""

            if name in self.__function_name_remapping:
                self.body += "int %s() {\ngoto %s;\n" % (
                    self.__function_name_remapping[name], self.__context.entry_point)
            else:
                self.body += """
int init(struct _STATE* _state)
{
X86_REGREF

  log_debug("~~~ heap_size=%%d para=%%d heap_ofs=%%d", HEAP_SIZE, (HEAP_SIZE >> 4), seg_offset(heap) );
  /* We expect ram_top as Kbytes, so convert to paragraphs */
  mcb_init(seg_offset(heap), (HEAP_SIZE >> 4) - seg_offset(heap) - 1, MCB_LAST);

  R(MOV(ss, seg_offset(stack)));
#if _BITS == 32
  esp = ((dd)(db*)&m.stack[STACK_SIZE - 4]);
#else
  esp=0;
  sp = STACK_SIZE - 4;
  es=0;
 *(dw*)(raddr(0,0x408)) = 0x378; //LPT
#endif

        return(0);
}

void %s(_offsets _i, struct _STATE* _state){
X86_REGREF
__disp=_i;
if (__disp==kbegin) goto %s;
else goto __dispatch_call;
mainproc_begin:
""" % (name, self.__context.entry_point)

            logging.info(name)
            self.proc.optimize()
            self.__unbounded = []
            self.proc.visit(self, skip)

            if name not in self.__skip_output:
                self.__translated.insert(0, self.body)
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
        if sys.version_info >= (3, 0):
            self.fd = open(fname, "wt", encoding=self.__codeset)
            self.hd = open(header, "wt", encoding=self.__codeset)
        else:
            self.fd = open(fname, "wt")
            self.hd = open(header, "wt")

        banner = """/* PLEASE DO NOT MODIFY THIS FILE. ALL CHANGES WILL BE LOST! LOOK FOR README FOR DETAILS */

/* 
 *
 */
"""

        hid = "__M2C_%s_STUBS_H__" % self.__namespace.upper().replace('-', '_')

        self.hd.write("""#ifndef %s
#define %s

%s""" % (hid, hid, banner))

        self.fd.write("""%s
#include \"%s\"
#include <curses.h>

//namespace %s {
""" % (banner, header, self.__namespace))

        self.__proc_queue.append(start)
        while len(self.__proc_queue):
            name = self.__proc_queue.pop()
            if name in self.__failed or name in self.__proc_done:
                continue
            if len(self.__proc_queue) == 0 and len(self.__procs) > 0:
                logging.info("queue's empty, adding remaining __procs:")
                for p in self.__procs:
                    self.schedule(p)
                self.__procs = []
            logging.info("continuing on %s" % name)
            self.__proc_done.append(name)
            self.__proc(name)
            self.__methods.append(name)
        # self.write_stubs("_stubs.cpp", self.__failed)
        self.__methods += self.__failed
        done, failed = len(self.__proc_done), len(self.__failed)

        self.fd.write("\n")
        self.fd.write("\n".join(self.__translated))
        self.fd.write("\n")

        logging.info(
            "%d ok, %d failed of %d, %3g%% translated" % (done, failed, done + failed, 100.0 * done / (done + failed)))
        logging.info("\n".join(self.__failed))

        # data_bin = self.data_seg
        cdata_bin = self.__cdata_seg
        hdata_bin = self.__hdata_seg

        data_impl = ""

        self.fd.write("\nreturn;\n")

        self.produce_jump_table()

        data_impl += "\nstruct Memory m = {\n"
        for v in cdata_bin:
            # data_impl += "0x%02x, " %v
            data_impl += "%s" % v
        data_impl += """
                {0},
                {0}
                """
        data_impl += "};\n"

        self.hd.write(
            """\n#include "asm.h"

//namespace %s {

"""
            % (self.__namespace))

        labeloffsets = self.produce_label_offsets()
        self.hd.write(labeloffsets)

        structures = self.produce_structures()
        self.hd.write(structures)

        data = self.produce_data(hdata_bin)
        self.hd.write(data)

        data = self.produce_externals(self.__context)
        self.hd.write(data)


        self.hd.write("//};\n\n//} // End of namespace DreamGen\n\n#endif\n")
        self.hd.close()

        self.fd.write(" %s\n" % data_impl)

        self.fd.write("\n\n//} // End of namespace DreamGen\n")
        self.fd.close()

    def produce_label_offsets(self):
        # self.hd.write("\nenum _offsets MYINT_ENUM {\n")
        offsets = []
        for k, v in list(self.__context.get_globals().items()):
            k = re.sub(r'[^A-Za-z0-9_]', '_', k)
            if isinstance(v, op.label):
                offsets.append((k.lower(), hex(v.line_number)))
        offsets = sorted(offsets, key=lambda t: t[1])
        labeloffsets = "static const uint16_t kbegin = 0x1001;\n"
        for o in offsets:
            labeloffsets += "static const uint16_t k%s = %s;\n" % o
        return labeloffsets

    def produce_structures(self):
        structures = "\n"
        for name, v in self.__context.structures.items():
            structures += "struct MYPACKED "+name+" {\n"
            for member in v.getdata():
                structures += "%s %s;\n" %(member.type, member.label)
            structures += "};\n"
        return structures

    def produce_data(self, hdata_bin):
        data_head = "\nstruct MYPACKED Memory{\n"
        data_head += "".join(hdata_bin)
        data_head += '''
                        db stack[STACK_SIZE];
                        db heap[HEAP_SIZE];
                '''
        data_head += "};\n"
        return data_head

    def produce_externals(self, context):
        data = '\n'
        for i in context.externals:
            v = context.get_global(i)
            data += f"extern {v.original_type} {v.name};\n"
        return data


    def produce_jump_table(self):
        self.fd.write("__dispatch_call:\nswitch (__disp) {\n")
        offsets = []
        for k, v in list(self.__context.get_globals().items()):
            k = re.sub(r'[^A-Za-z0-9_]', '_', k)
            if isinstance(v, op.label):
                offsets.append((k.lower(), k))
        offsets = sorted(offsets, key=lambda t: t[1])
        for o in offsets:
            logging.debug(o)
            self.fd.write("case k%s: \tgoto %s;\n" % o)
        self.fd.write("default: log_error(\"Jump/call to nothere %d\\n\", __disp);stackDump(_state); abort();\n")
        self.fd.write("};\n}\n")

    def _lea(self, dst, src):
        self.lea = True
        r = "\tR(%s = %s);\n" % (self.expand(dst, destination=True, lea=True), self.expand(src, lea=True))
        self.lea = False
        return r

    def _movs(self, dst, src):
        size = self.get_size(dst)
        a, b = self.parse2(dst, src)
        return "MOVS(%s, %s, %d);\n" % (a, b, size)

    def _repe(self):
        return "\tREPE\n"

    def _repne(self):
        return "\tREPNE\n"

    def _lods(self, src):
        size = self.get_size(src)
        src = self.expand(src)
        return "\tR(LODS(%s,%d));\n" % (src, size)

    def _leave(self):
        return "\tR(MOV(esp, ebp));\nR(POP(ebp));\n"

    def _int(self, dst):
        dst = self.expand(dst)
        return "\tR(_INT(%s));\n" % (dst)

    def _instruction0(self, cmd):
        return "\tR(%s);\n" % (cmd.upper())

    def _instruction1(self, cmd, dst):
        dst = self.expand(dst)
        return "\tR(%s(%s));\n" % (cmd.upper(), dst)

    def _jump(self, cmd, label):
        result = self.isrelativejump(label)
        if result:
            return "\n"
        else:
            label = self.jump_to_label(label)  # TODO
            return "\t\tR(%s(%s));\n" % (cmd.upper(), label)

    def isrelativejump(self, label):
        result = '$' in str(label)  # skip j* $+2
        return result

    def _instruction2(self, cmd, dst, src):
        self.a, self.b = self.parse2(dst, src)
        return "\tR(%s(%s, %s));\n" % (cmd.upper(), self.a, self.b)

    def _instruction3(self, cmd, dst, src, c):
        self.a, self.b = self.parse2(dst, src)
        self.c = self.expand(c)
        return "\tR(%s(%s, %s, %s));\n" % (cmd.upper(), self.a, self.b, self.c)

    def _assignment(self, dst, src):
        return "#undef %s\n#define %s %s\n" % (dst, dst, self.expand(src))

    def _equ(self, dst, src):
        return "#define %s %s\n" % (dst, self.expand(src))

    @staticmethod
    def produce_c_data(data):
        label, type, cur_data_type, r, elements, size = data.getdata()
        data_ctype = type
        logging.debug("current data type = %d current data c type = %s" % (cur_data_type, data_ctype))
        rc = [None] * len(r)
        rh = []
        vh = ""
        vc = ""
        if cur_data_type == 1:  # 0 terminated string
            vh = "char " + label + "[" + str(len(r)) + "]"

        elif cur_data_type == 2:  # array string
            vh = "char " + label + "[" + str(len(r)) + "]"
            vc = "{"

        elif cur_data_type == 3:  # number
            vh = data_ctype + " " + label

        elif cur_data_type == 4:  # array
            vh = data_ctype + " " + label + "[" + str(elements) + "]"
            vc = "{"
        elif cur_data_type == 5:  # struct
            vh = data_ctype + " " + label
            vc = "{"

        if cur_data_type == 1:  # string
            vv = "\""
            for i in range(0, len(r) - 1):
                vv += Cpp.convert_str(r[i])
            vv += "\""
            rc = ["", vv]

        elif cur_data_type == 2:  # array of char
            vv = ""
            logging.debug(r)
            for i in range(0, len(r)):
                vv += Cpp.convert_char(r[i])
                if i != len(r) - 1:
                    vv += ","
            rc = ["", vv]

        elif cur_data_type == 3:  # number
            if len(r):
                rc[0] = str(r[0])
            else:
                rc = ['']

        elif cur_data_type in [4, 5]:  # array of numbers
            # vv = ""
            for i in range(0, len(r)):
                rc[i] = str(r[i])
                if i != len(r) - 1:
                    rc[i] += ","
        rc.insert(0, vc)
        rh.insert(0, vh)
        # if it was array of numbers or array string
        if cur_data_type in [2, 4, 5]:
            rc.append("}")
        rc.append(", // " + label + "\n")  # TODO can put original_label
        rh.append(";\n")
        logging.debug(rc)
        logging.debug(rh)
        rc = "".join(rc)
        rh = "".join(rh)
        return rc, rh, size

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
            elif c < 10:
                vvv = "\\{:01x}".format(c)
            elif c < 32:
                vvv = "\\x{:02x}".format(c)
            else:
                vvv = chr(c)
        elif isinstance(c, str):
            # logging.debug "~~ " + r[i] + str(ord(r[i]))
            if c in ["\'", '\"', '\\']:
                vvv = "\\" + c
            elif ord(c) > 127:
                vvv = '\\' + hex(ord(c.encode('cp437', 'backslashreplace')))[1:]
                # vvv = c
            elif c == '\0':
                vvv = '\\0'
            else:
                vvv = c
            # vvv = "'" + vvv + "'"
        return vvv
