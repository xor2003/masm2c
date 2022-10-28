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
from builtins import str
from collections import OrderedDict
from enum import Enum

# import traceback


class Unsupported(Exception):
    pass


class baseop:
    # __slots__ = ["cmd", "line", "line_number", "elements", "args"]

    def __init__(self):
        self.cmd = ""
        self.raw_line = ""
        self.line_number = 0
        self.elements = 1
        self.args = []
        self.size = 0
        self.real_offset = None
        self.real_seg = None

    def getsize(self):
        return self.size

    # def __str__(self):
    #        return self.cmd+" "+self.command+" "+str(self.line_number)

    def __str__(self):
        return str(self.__class__)


class var:

    def __init__(self, size, offset, name="", segment="", issegment=False, elements=1,
                 external=False, original_type="", filename='', raw='', line_number=0):
        '''
        Global variable with name representing data

        :param size:
        :param offset:
        :param name:
        :param segment:
        :param issegment:
        :param elements:
        :param external:
        :param original_type:
        :param filename:
        :param raw:
        :param line_number:
        '''
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
        self.filename = filename
        self.line = raw
        self.line_number = line_number
        # logging.debug("op.var(%s)" %(str(self.__dict__).replace('\n',' ')))

    def getsize(self):
        return self.size

    def gettype(self):
        return self.original_type


class Segment:
    # __slots__ = ['name', 'offset', '__data', 'original_name', 'used']
    simple_segments = {
        "tiny": {
            ".CODE": {
                "Name": "_TEXT",
                "Align": 2,
                "Combine": "public",
                "Class": "CODE",
                "Group": "DGROUP"
            },
            ".FARDATA": {
                "Name": "FAR_DATA",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_DATA",
                "Group": ""
            },
            ".FARDATA?": {
                "Name": "FAR_BSS",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_BSS",
                "Group": ""
            },
            ".DATA": {
                "Name": "_DATA",
                "Align": 2,
                "Combine": "public",
                "Class": "DATA",
                "Group": "DGROUP"
            },
            ".CONST": {
                "Name": "CONST",
                "Align": 2,
                "Combine": "public",
                "Class": "CONST",
                "Group": "DGROUP"
            },
            ".DATA?": {
                "Name": "_BSS",
                "Align": 2,
                "Combine": "public",
                "Class": "BSS",
                "Group": "DGROUP"
            }
        },
        "small": {
            ".CODE": {
                "Name": "_TEXT",
                "Align": 2,
                "Combine": "public",
                "Class": "CODE",
                "Group": ""
            },
            ".FARDATA": {
                "Name": "FAR_DATA",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_DATA",
                "Group": ""
            },
            ".FARDATA?": {
                "Name": "FAR_BSS",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_BSS",
                "Group": ""
            },
            ".DATA": {
                "Name": "_DATA",
                "Align": 2,
                "Combine": "public",
                "Class": "DATA",
                "Group": "DGROUP"
            },
            ".CONST": {
                "Name": "CONST",
                "Align": 2,
                "Combine": "public",
                "Class": "CONST",
                "Group": "DGROUP"
            },
            ".DATA?": {
                "Name": "_BSS",
                "Align": 2,
                "Combine": "public",
                "Class": "BSS",
                "Group": "DGROUP"
            },
            ".STACK": {
                "Name": "STACK",
                "Align": 0x10,
                "Combine": "STACK",
                "Class": "STACK",
                "Group": "DGROUP*"
            }
        },
        "medium": {
            ".CODE": {
                "Name": "name_TEXT",
                "Align": 2,
                "Combine": "public",
                "Class": "CODE",
                "Group": ""
            },

            ".FARDATA": {
                "Name": "FAR_DATA",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_DATA",
                "Group": ""
            },
            ".FARDATA?": {
                "Name": "FAR_BSS",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_BSS",
                "Group": ""
            },
            ".DATA": {
                "Name": "_DATA",
                "Align": 2,
                "Combine": "public",
                "Class": "DATA",
                "Group": "DGROUP"
            },
            ".CONST": {
                "Name": "CONST",
                "Align": 2,
                "Combine": "public",
                "Class": "CONST",
                "Group": "DGROUP"
            },
            ".DATA?": {
                "Name": "_BSS",
                "Align": 2,
                "Combine": "public",
                "Class": "BSS",
                "Group": "DGROUP"
            },
            ".STACK": {
                "Name": "STACK",
                "Align": 0x10,
                "Combine": "STACK",
                "Class": "STACK",
                "Group": "DGROUP*"
            }
        },
        "compact": {
            ".CODE": {
                "Name": "_TEXT",
                "Align": 2,
                "Combine": "public",
                "Class": "CODE",
                "Group": ""
            },
            ".FARDATA": {
                "Name": "FAR_DATA",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_DATA",
                "Group": ""
            },
            ".FARDATA?": {
                "Name": "FAR_BSS",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_BSS",
                "Group": ""
            },
            ".DATA": {
                "Name": "_DATA",
                "Align": 2,
                "Combine": "public",
                "Class": "DATA",
                "Group": "DGROUP"
            },
            ".CONST": {
                "Name": "CONST",
                "Align": 2,
                "Combine": "public",
                "Class": "CONST",
                "Group": "DGROUP"
            },
            ".DATA?": {
                "Name": "_BSS",
                "Align": 2,
                "Combine": "public",
                "Class": "BSS",
                "Group": "DGROUP"
            },
            ".STACK": {
                "Name": "STACK",
                "Align": 0x10,
                "Combine": "STACK",
                "Class": "STACK",
                "Group": "DGROUP*"
            }
        },
        "large": {  # or huge
            ".CODE": {
                "Name": "name_TEXT",
                "Align": 2,
                "Combine": "public",
                "Class": "CODE",
                "Group": ""
            },
            ".FARDATA": {
                "Name": "FAR_DATA",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_DATA",
                "Group": ""
            },
            ".FARDATA?": {
                "Name": "FAR_BSS",
                "Align": 0x10,
                "Combine": "private",
                "Class": "FAR_BSS",
                "Group": ""
            },
            ".DATA": {
                "Name": "_DATA",
                "Align": 2,
                "Combine": "public",
                "Class": "DATA",
                "Group": "DGROUP"
            },
            ".CONST": {
                "Name": "CONST",
                "Align": 2,
                "Combine": "public",
                "Class": "CONST",
                "Group": "DGROUP"
            },
            ".DATA?": {
                "Name": "_BSS",
                "Align": 2,
                "Combine": "public",
                "Class": "BSS",
                "Group": "DGROUP"
            },
            ".STACK": {
                "Name": "STACK",
                "Align": 0x10,
                "Combine": "STACK",
                "Class": "STACK",
                "Group": "DGROUP*"
            }
        },
        "flat": {
            ".CODE": {
                "Name": "_TEXT",
                "Align": 4,
                "Combine": "public",
                "Class": "CODE",
                "Group": ""
            },
            ".FARDATA": {
                "Name": "_DATA",
                "Align": 4,
                "Combine": "public",
                "Class": "DATA",
                "Group": ""
            },
            ".FARDATA?": {
                "Name": "_BSS",
                "Align": 4,
                "Combine": "public",
                "Class": "BSS",
                "Group": ""
            },
            ".DATA": {
                "Name": "_DATA",
                "Align": 4,
                "Combine": "public",
                "Class": "DATA",
                "Group": ""
            },
            ".CONST": {
                "Name": "CONST",
                "Align": 4,
                "Combine": "public",
                "Class": "CONST",
                "Group": ""
            },
            ".DATA?": {
                "Name": "_BSS",
                "Align": 4,
                "Combine": "public",
                "Class": "BSS",
                "Group": ""
            },
            ".STACK": {
                "Name": "STACK",
                "Align": 4,
                "Combine": "public",
                "Class": "STACK",
                "Group": ""
            }
        }
    }

    def __init__(self, name, offset, options=None, segclass=None, comment=''):
        '''
        Represents MASM Segment

        :param name: Segment name
        :param offset: In-memory segment offset in paragraphs. TODO: Used?
        :param options: Segment options
        :param segclass: Segment class name
        :param comment: Source of element
        '''
        self.name = name.lower()
        self.offset = offset
        self.original_name = name
        self.used = False
        self.__data = []
        self.options = options
        self.segclass = segclass
        # self.comment = comment
        self.seglabels = {self.name,}
        self.size = 0  # Check if needed

    def getsize(self):
        return self.size

    def append(self, data):
        self.__data.append(data)
        self.size += data.getsize()

    def insert_label(self, data):
        if data.getlabel() not in self.seglabels:
            self.__data.insert(1, data)
            self.seglabels.add(data.getlabel())

    def getdata(self):
        return self.__data

    def setdata(self, data):
        self.__data = data

class DataType(Enum):
    ZERO_STRING = 1
    ARRAY_STRING = 2
    NUMBER = 3
    ARRAY = 4
    OBJECT = 5


class Data(baseop):
    # __slots__ = ['label', 'type', 'data_internal_type', 'array', 'elements', 'size', 'members',
    #             'filename', 'line', 'line_number']

    def __init__(self, label, type, data_internal_type: DataType, array, elements, size, filename='', raw_line='',
                 line_number=0, comment='', align=False, offset=0):
        '''
        One element of data

        :param label: Data label
        :param type: Input data type
        :param data_internal_type: Internal type. See DataType
        :param array: Value or values
        :param elements: Number of elements
        :param size: Memory size
        :param filename: Source filename
        :param raw_line: Raw input string
        :param line_number: Source linenumber
        :param comment: Source of element
        :param offset: offset from begging of the memory inside Memory structure
        '''
        super().__init__()
        self.label = label
        self.type = type
        self.data_internal_type = data_internal_type
        self.elements = elements
        self.size = size
        self.array = array
        self.__members = []
        self.filename = filename
        self.raw_line = raw_line
        self.line_number = line_number
        self.align = align
        # self.comment = comment
        self.real_seg, self.real_offset = None, None
        self.offset = offset

    def isobject(self):
        return self.data_internal_type == DataType.OBJECT

    def setmembers(self, members):
        self.__members = members

    def getmembers(self):
        return self.__members

    def setvalue(self, value):
        if self.isobject():
            for m, v in zip(self.__members, value):
                m.setvalue(v)
        else:
            self.array = value

    def getlabel(self):
        return self.label

    def getsize(self):
        return self.size

    def gettype(self):
        return self.type

    def getinttype(self):
        return self.data_internal_type

    def getdata(self):
        return self.label, self.type, self.data_internal_type, self.array, self.elements, self.size

    def is_align(self):
        return self.align

    def getrealaddr(self):
        return self.real_seg, self.real_offset

class Struct:
    class Type(Enum):
        STRUCT = 1
        UNION = 2

    def __init__(self, name, dtype):
        '''
        Represent structure

        :param name: Name
        :param dtype: Structure or Union?
        '''
        self.__name = name
        self.__fields = OrderedDict()
        self.__size = 0
        self.__type = Struct.Type.UNION if dtype.lower() == 'union' else Struct.Type.STRUCT

    def append(self, data):
        self.__fields[data.label.lower()] = data
        if self.__type == Struct.Type.STRUCT:
            self.__size += data.getsize()
        else:  # Union
            self.__size = max(self.__size, data.getsize())

    def getdata(self):
        return self.__fields

    def getitem(self, key):
        return self.__fields[key.lower()]

    def getsize(self):
        return self.__size

    def gettype(self):
        return self.__type


class basejmp(baseop):
    pass


class _call(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._call(*self.args)


class _rep(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._rep(*self.args)


class _add(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._add(*self.args)



class _mul(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._mul(self.args)  #


class _div(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._div(*self.args)



class _jne(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._jnz(*self.args)


class _je(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._jz(*self.args)


class _jb(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._jc(*self.args)


class _jae(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._jnc(*self.args)


class _jnb(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._jnc(*self.args)


'''
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

    def accept(self, visitor):
        return visitor._push(self.args)


class _pop(baseop):
    def __init__(self, arg):
        super().__init__()
        if isinstance(arg, list) and len(arg) and isinstance(arg[0], Token) \
                and arg[0].type in ['register', 'segmentregister']:
            self.args = arg
        else:
            self.args = flattenpush(Token.remove_tokens(arg, 'expr'))

    def accept(self, visitor):
        return visitor._pop(self.args)
'''


class _ret(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._ret(self.args)

class _retn(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._ret(self.args)

class _retf(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._retf(self.args)


class _lodsb(baseop):
    def __init__(self, arg):
        super().__init__()

    def accept(self, visitor):
        return visitor._lodsb()


class _scasb(baseop):
    def __init__(self, arg):
        super().__init__()

    def accept(self, visitor):
        return visitor._scasb()


class _scasw(baseop):
    def __init__(self, arg):
        super().__init__()

    def accept(self, visitor):
        return visitor._scasw()


class _scasd(baseop):
    def __init__(self, arg):
        super().__init__()

    def accept(self, visitor):
        return visitor._scasd()


class _cmpsb(baseop):
    def __init__(self, arg):
        super().__init__()

    def accept(self, visitor):
        return visitor._cmpsb()


class _lodsw(baseop):
    def __init__(self, arg):
        super().__init__()

    def accept(self, visitor):
        return visitor._lodsw()


class _lodsd(baseop):
    def __init__(self, arg):
        super().__init__()

    def accept(self, visitor):
        return visitor._lodsd()


class _stosd(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor):
        return visitor._stosd()


class _stosw(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor):
        return visitor._stosw()


class _stosb(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor):
        return visitor._stosb()


class _movsw(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor):
        return visitor._movsw()


class _movsd(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor):
        return visitor._movsd()


class _movsb(baseop):
    def __init__(self, arg):
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor):
        return visitor._movsb()


class _int(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._int(*self.args)

'''
class _nop(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def accept(self, visitor):
        return ""
'''

class label(baseop):

    def __init__(self, name, proc:str=None, isproc=False, line_number=0, far=False, globl=True):
        '''
        Label

        :param name:
        :param proc:
        :param isproc:
        :param line_number:
        :param far:
        :param globl:
        '''
        super().__init__()
        self.name = name
        self.original_name = name
        self.line_number = line_number
        self.far = far
        #self.proc:str = proc
        self.isproc = isproc
        self.used = False
        self.globl = globl

    def accept(self, visitor):
        return visitor._label(self.name, self.isproc)


class _lea(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._lea(*self.args)


class _repe(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._repe(*self.args)


class _repne(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._repne(*self.args)


class _jna(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._jbe(*self.args)


class _jnbe(basejmp):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._ja(*self.args)


class _imul(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._imul(self.args)  #


class _movs(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._movs(*self.args)


class _lods(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._lods(*self.args)


class _scas(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._scas(*self.args)


class _leave(baseop):
    def __init__(self, arg):
        super().__init__()

    def accept(self, visitor):
        return visitor._leave()


class _idiv(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._idiv(*self.args)


class _instruction0(baseop):
    def __init__(self, arg):
        super().__init__()

    def accept(self, visitor):
        return visitor._instruction0(self.cmd)


class _instruction1(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._instruction1(self.cmd, *self.args)


class _jump(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._jump(self.cmd, *self.args)


class _instruction2(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._instruction2(self.cmd, *self.args)


class _instruction3(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._instruction3(self.cmd, *self.args)


class _equ(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.original_name = ''
        self.original_type = ''
        self.implemented = False
        self.size = 0

    def gettype(self):
        return self.original_type

    def accept(self, visitor):
        if self.implemented == False:
            self.implemented = True
            return visitor._equ(*self.args)
        else:
            from masm2c.gen import SkipCode
            raise SkipCode


class _assignment(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.original_name = ''
        self.original_type = ''
        self.implemented = False
        self.size = 0

    def gettype(self):
        return self.original_type

    def accept(self, visitor):
        # if self.implemented == False:
        self.implemented = True
        return visitor._assignment(self, *self.args)
        # else:
        #    from masm2c.cpp import SkipCode
        #    raise SkipCode

class _xlat(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._xlat(self.args)

class _mov(baseop):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def accept(self, visitor):
        return visitor._mov(*self.args)
