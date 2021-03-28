from __future__ import absolute_import

import logging
from builtins import str
from builtins import object

from masm2c import parser
from masm2c.Token import Token
from enum import Enum

# import traceback

class Unsupported(Exception):
    pass


class var(object):

    def __init__(self, size, offset, name="", segment="", issegment=False, elements=1, external=False, original_type=""):
        # logging.debug("op.var(%d, %d, %s, %s, %s, %d)" %(size, offset, name, segment, issegment, elements))
        self.size = size
        self.offset = offset
        self.original_name = name
        self.name = name.lower()
        self.segment = segment
        self.issegment = issegment
        self.elements = elements
        self.used = False
        self.external = external
        self.original_type = original_type.lower()
        # logging.debug("op.var(%s)" %(str(self.__dict__).replace('\n',' ')))

    def getsize(self):
        return self.size

class Segment:
	#__slots__ = ['name', 'offset', '__data', 'original_name', 'used']

    def __init__(self, name, offset):
        # logging.debug("op.var(%d, %d, %s, %s, %s, %d)" %(size, offset, name, segment, issegment, elements))
        self.name = name.lower()
        self.offset = offset
        self.original_name = name
        self.used = False
        self.__data = list()

    def append(self, data):
        self.__data.append(data)

    def getdata(self):
        return self.__data

class DataType(Enum):
    ZERO_STRING = 1
    ARRAY_STRING = 2
    NUMBER = 3
    ARRAY_NUMBER = 4
    STRUCT = 5

class Data:
    __slots__ = ['label', 'type', 'data_internal_type', 'array', 'elements', 'size']

    def __init__(self, label, type, data_internal_type: DataType, array, elements, size):
        self.label = label
        self.type = type
        self.data_internal_type = data_internal_type
        self.array = array
        self.elements = elements
        self.size = size

    def getdata(self):
        return self.label, self.type, self.data_internal_type, self.array, self.elements, self.size

    def getsize(self):
        return self.size


class Struct:
    class Type(Enum):
        STRUCT = 1
        UNION = 2

    def __init__(self, name, type):
        self.__name = name
        self.__fields = dict()
        self.__size = 0
        self.__type = Struct.Type.UNION if type.lower() == 'union' else Struct.Type.STRUCT

    def append(self, data):
        self.__fields[data.label] = data
        if self.__type == Struct.Type.STRUCT:
            self.__size += data.getsize()
        else: # Union
            self.__size = max(self.__size, data.getsize())

    def getdata(self):
        return self.__fields

    def __getitem__(self, key):
        return self.__fields[key]

    def getsize(self):
        return self.__size

    def gettype(self):
        return self.__type
'''
class reg(object):
    def __init__(self, name):
        self.name = name

    def size(self):
        return 2 if self.name[1] == 'x' else 1

    def __str__(self):
        return "<register %s>" % self.name


class unref(object):
    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return "<unref %s>" % self.exp


class ref(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<ref %s>" % self.name


class glob(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<global %s>" % self.name


'''


class baseop(object):
    __slots__ = ["cmd", "line", "line_number", "elements", "args"]

    def __init__(self):
        self.cmd = ""
        self.line = ""
        self.line_number = 0
        self.elements = 1
        self.args = []
        self.size = 0

    def getsize(self):
        return self.size

    # def __str__(self):
    #        return self.cmd+" "+self.command+" "+str(self.line_number)

    def __str__(self):
        return str(self.__class__)


class basejmp(baseop):
    pass


class _call(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._call(*self.args)


class _rep(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._rep(*self.args)


class _add(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._add(*self.args)

class _sub(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._sub(*self.args)


class _mul(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._mul(self.args)  #


class _div(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._div(*self.args)


class _xor(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._xor(*self.args)


class _jne(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._jnz(*self.args)


class _je(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._jz(*self.args)


class _jb(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._jc(*self.args)


class _jae(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._jnc(*self.args)


class _jnb(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._jnc(*self.args)


def flatten(s):
    if not s:
        return s
    if isinstance(s[0], list):
        return flatten(s[0]) + flatten(s[1:])
    return s[:1] + flatten(s[1:])


def flattenpush(s):  # TODO will work most of the time
    s = flatten(s)
    res = []
    ressec = []
    for i in s:
        ressec.append(i)
        if isinstance(i, Token) and i.type in ['offset']:
            res.append(ressec)
            ressec = []
    if ressec:
        res.append(ressec)
    return res

'''
class _push(baseop):
    def __init__(self, arg):
        super().__init__()
        #        self.arg = Token.find_and_call_tokens(arg,'expr') #flattenpush(arg)
        if isinstance(arg, list) and len(arg) and isinstance(arg[0], Token) \
                and arg[0].type in ['register', 'segmentregister']:
            self.args = arg
        else:
            self.args = flattenpush(Token.remove_tokens(arg, 'expr'))

    def visit(self, visitor):
        return visitor._push(self.args)


class _pop(baseop):
    def __init__(self, arg):
        super().__init__()
        if isinstance(arg, list) and len(arg) and isinstance(arg[0], Token) \
                and arg[0].type in ['register', 'segmentregister']:
            self.args = arg
        else:
            self.args = flattenpush(Token.remove_tokens(arg, 'expr'))

    def visit(self, visitor):
        return visitor._pop(self.args)
'''

class _ret(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._ret()


class _retn(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._ret()


class _lodsb(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._lodsb()


class _scasb(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._scasb()


class _scasw(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._scasw()


class _scasd(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._scasd()


class _cmpsb(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._cmpsb()


class _lodsw(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._lodsw()


class _lodsd(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._lodsd()


class _stosd(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def visit(self, visitor):
        return visitor._stosd(self.repeat, self.clear_cx)


class _stosw(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def visit(self, visitor):
        return visitor._stosw(self.repeat, self.clear_cx)


class _stosb(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def visit(self, visitor):
        return visitor._stosb(self.repeat, self.clear_cx)


class _movsw(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def visit(self, visitor):
        return visitor._movsw(self.repeat, self.clear_cx)


class _movsd(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def visit(self, visitor):
        return visitor._movsd(self.repeat, self.clear_cx)


class _movsb(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def visit(self, visitor):
        return visitor._movsb(self.repeat, self.clear_cx)


class _int(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._int(*self.args)


class _nop(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return ""


class label(baseop):

    def __init__(self, name, proc, line_number=0, far=False):
        super().__init__()
        self.name = name
        self.original_name = name
        self.line_number = line_number
        self.far = far
        self.proc = proc
        self.used = False

    def visit(self, visitor):
        return visitor._label(self.name, self.proc)


class _lea(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._lea(*self.args)


class _repe(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._repe(*self.args)


class _repne(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._repne(*self.args)


class _jna(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._jbe(*self.args)


class _jnbe(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._ja(*self.args)


class _imul(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._imul(self.args)  #


class _movs(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._movs(*self.args)


class _lods(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._lods(*self.args)


class _scas(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._scas(*self.args)


class _leave(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._leave()


class _idiv(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._idiv(*self.args)


class _instruction0(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def visit(self, visitor):
        return visitor._instruction0(self.cmd)


class _instruction1(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._instruction1(self.cmd, *self.args)


class _jump(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._jump(self.cmd, *self.args)


class _instruction2(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._instruction2(self.cmd, *self.args)


class _instruction3(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def visit(self, visitor):
        return visitor._instruction3(self.cmd, *self.args)


class _equ(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.original_name = ''
        self.original_type = ''
        self.implemented = False
        self.size = 0

    def visit(self, visitor):
        if self.implemented == False:
            self.implemented = True
            return visitor._equ(*self.args)
        else:
            from masm2c.cpp import SkipCode
            raise SkipCode


class _assignment(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.original_name = ''
        self.original_type = ''
        self.implemented = False
        self.size = 0

    def visit(self, visitor):
        if self.implemented == False:
            self.implemented = True
            return visitor._assignment(*self.args)
        else:
            from masm2c.cpp import SkipCode
            raise SkipCode
