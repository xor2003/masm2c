"""
Defines classes for different types of assembly instructions and operands.
It include classes like _mov, _add, _jmp, etc., each with methods to generate equivalent C code.
"""
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
from collections import OrderedDict
from copy import deepcopy
from enum import Enum
from typing import TYPE_CHECKING, Any, Union, Optional, Final

from lark import lark

if TYPE_CHECKING:
    from masm2c.cpp import Cpp

from masm2c.Token import Expression

class Unsupported(Exception):
    pass


class baseop(lark.Tree):

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__.lower(), [])
        self.cmd = ""
        self.raw_line = ""
        self.filename = ""
        self.line_number = 0
        self.elements = 1
        self.size = 0
        self.real_offset: Optional[int] = None
        self.real_seg: Optional[int] = None
        self.syntetic = False

    def getsize(self) -> int:
        return self.size

    # def __str__(self):

    def __str__(self) -> str:
        return str(self.__class__)

    def accept(self, visitor: "Cpp") -> str:
        raise NotImplementedError()

class var:

    def __init__(self, size: int, offset: int, name: str="", segment: str="", issegment: bool=False, elements: int=1,
                 external: bool=False, original_type: str="", filename: str="", raw: str="", line_number: int=0) -> None:
        """Global variable with name representing data.

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
        """
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

    def getsize(self) -> int:
        return self.size

    def gettype(self):
        return self.original_type


SIMPLE_SEGMENTS = {
    "tiny": {
        ".CODE": {
            "Name": "_TEXT",
            "Align": 2,
            "Combine": "public",
            "Class": "CODE",
            "Group": "DGROUP",
        },
        ".FARDATA": {
            "Name": "FAR_DATA",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_DATA",
            "Group": "",
        },
        ".FARDATA?": {
            "Name": "FAR_BSS",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_BSS",
            "Group": "",
        },
        ".DATA": {
            "Name": "_DATA",
            "Align": 2,
            "Combine": "public",
            "Class": "DATA",
            "Group": "DGROUP",
        },
        ".CONST": {
            "Name": "CONST",
            "Align": 2,
            "Combine": "public",
            "Class": "CONST",
            "Group": "DGROUP",
        },
        ".DATA?": {
            "Name": "_BSS",
            "Align": 2,
            "Combine": "public",
            "Class": "BSS",
            "Group": "DGROUP",
        },
    },
    "small": {
        ".CODE": {
            "Name": "_TEXT",
            "Align": 2,
            "Combine": "public",
            "Class": "CODE",
            "Group": "",
        },
        ".FARDATA": {
            "Name": "FAR_DATA",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_DATA",
            "Group": "",
        },
        ".FARDATA?": {
            "Name": "FAR_BSS",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_BSS",
            "Group": "",
        },
        ".DATA": {
            "Name": "_DATA",
            "Align": 2,
            "Combine": "public",
            "Class": "DATA",
            "Group": "DGROUP",
        },
        ".CONST": {
            "Name": "CONST",
            "Align": 2,
            "Combine": "public",
            "Class": "CONST",
            "Group": "DGROUP",
        },
        ".DATA?": {
            "Name": "_BSS",
            "Align": 2,
            "Combine": "public",
            "Class": "BSS",
            "Group": "DGROUP",
        },
        ".STACK": {
            "Name": "STACK",
            "Align": 0x10,
            "Combine": "STACK",
            "Class": "STACK",
            "Group": "DGROUP*",
        },
    },
    "medium": {
        ".CODE": {
            "Name": "name_TEXT",
            "Align": 2,
            "Combine": "public",
            "Class": "CODE",
            "Group": "",
        },

        ".FARDATA": {
            "Name": "FAR_DATA",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_DATA",
            "Group": "",
        },
        ".FARDATA?": {
            "Name": "FAR_BSS",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_BSS",
            "Group": "",
        },
        ".DATA": {
            "Name": "_DATA",
            "Align": 2,
            "Combine": "public",
            "Class": "DATA",
            "Group": "DGROUP",
        },
        ".CONST": {
            "Name": "CONST",
            "Align": 2,
            "Combine": "public",
            "Class": "CONST",
            "Group": "DGROUP",
        },
        ".DATA?": {
            "Name": "_BSS",
            "Align": 2,
            "Combine": "public",
            "Class": "BSS",
            "Group": "DGROUP",
        },
        ".STACK": {
            "Name": "STACK",
            "Align": 0x10,
            "Combine": "STACK",
            "Class": "STACK",
            "Group": "DGROUP*",
        },
    },
    "compact": {
        ".CODE": {
            "Name": "_TEXT",
            "Align": 2,
            "Combine": "public",
            "Class": "CODE",
            "Group": "",
        },
        ".FARDATA": {
            "Name": "FAR_DATA",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_DATA",
            "Group": "",
        },
        ".FARDATA?": {
            "Name": "FAR_BSS",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_BSS",
            "Group": "",
        },
        ".DATA": {
            "Name": "_DATA",
            "Align": 2,
            "Combine": "public",
            "Class": "DATA",
            "Group": "DGROUP",
        },
        ".CONST": {
            "Name": "CONST",
            "Align": 2,
            "Combine": "public",
            "Class": "CONST",
            "Group": "DGROUP",
        },
        ".DATA?": {
            "Name": "_BSS",
            "Align": 2,
            "Combine": "public",
            "Class": "BSS",
            "Group": "DGROUP",
        },
        ".STACK": {
            "Name": "STACK",
            "Align": 0x10,
            "Combine": "STACK",
            "Class": "STACK",
            "Group": "DGROUP*",
        },
    },
    "large": {  # or huge
        ".CODE": {
            "Name": "name_TEXT",
            "Align": 2,
            "Combine": "public",
            "Class": "CODE",
            "Group": "",
        },
        ".FARDATA": {
            "Name": "FAR_DATA",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_DATA",
            "Group": "",
        },
        ".FARDATA?": {
            "Name": "FAR_BSS",
            "Align": 0x10,
            "Combine": "private",
            "Class": "FAR_BSS",
            "Group": "",
        },
        ".DATA": {
            "Name": "_DATA",
            "Align": 2,
            "Combine": "public",
            "Class": "DATA",
            "Group": "DGROUP",
        },
        ".CONST": {
            "Name": "CONST",
            "Align": 2,
            "Combine": "public",
            "Class": "CONST",
            "Group": "DGROUP",
        },
        ".DATA?": {
            "Name": "_BSS",
            "Align": 2,
            "Combine": "public",
            "Class": "BSS",
            "Group": "DGROUP",
        },
        ".STACK": {
            "Name": "STACK",
            "Align": 0x10,
            "Combine": "STACK",
            "Class": "STACK",
            "Group": "DGROUP*",
        },
    },
    "flat": {
        ".CODE": {
            "Name": "_TEXT",
            "Align": 4,
            "Combine": "public",
            "Class": "CODE",
            "Group": "",
        },
        ".FARDATA": {
            "Name": "_DATA",
            "Align": 4,
            "Combine": "public",
            "Class": "DATA",
            "Group": "",
        },
        ".FARDATA?": {
            "Name": "_BSS",
            "Align": 4,
            "Combine": "public",
            "Class": "BSS",
            "Group": "",
        },
        ".DATA": {
            "Name": "_DATA",
            "Align": 4,
            "Combine": "public",
            "Class": "DATA",
            "Group": "",
        },
        ".CONST": {
            "Name": "CONST",
            "Align": 4,
            "Combine": "public",
            "Class": "CONST",
            "Group": "",
        },
        ".DATA?": {
            "Name": "_BSS",
            "Align": 4,
            "Combine": "public",
            "Class": "BSS",
            "Group": "",
        },
        ".STACK": {
            "Name": "STACK",
            "Align": 4,
            "Combine": "public",
            "Class": "STACK",
            "Group": "",
        },
    },
}

class Segment:

    def __init__(self, name: str, offset: int, *, options: Optional[set[str]]=None, segclass: Optional[str]="", comment: str="") -> None:
        """Represents MASM Segment.

        :param name: Segment name
        :param offset: In-memory segment offset in paragraphs. TODO: Used?
        :param options: Segment options
        :param segclass: Segment class name
        :param comment: Source of element
        """
        self.name = name.lower()
        self.offset = offset
        self.original_name = name
        self.used = False
        self.data = "segment"
        self.children: list[Data] = []
        self.options: set[str] = options or set()
        self.segclass = segclass
        self.seglabels = {self.name}
        self.size = 0  # Check if needed
        self.comment = comment

    def getsize(self):
        return self.size

    def append(self, data: "Data") -> None:
        self.children.append(data)
        self.size += data.getsize()

    #def insert_label(self, data):
    #    if data.getlabel() not in self.seglabels:

    def getdata(self):
        return self.children

    def setdata(self, data):
        self.children = data

class DataType(Enum):
    ZERO_STRING = 1
    ARRAY_STRING = 2
    NUMBER = 3
    ARRAY = 4
    OBJECT = 5


class Data(baseop):
    # __slots__ = ['label', 'type', 'data_internal_type', 'array', 'elements', 'size', 'members',
    #             'filename', 'line', 'line_number']

    def __init__(self, label: str, type: str, data_internal_type: DataType, array: list[Any], elements: int, size: int, filename: str="", raw_line: str="",
                 line_number: int=0, comment: str="", align: bool=False, offset: int=0) -> None:
        """One element of data.

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
        """
        super().__init__()
        self.label = label
        self.data_type = type
        self.data_internal_type = data_internal_type
        self.elements = elements
        self.size = size
        self.children = array
        self.__members: list[Data] = []
        self.filename = filename
        self.raw_line = raw_line
        self.line_number = line_number
        self.align = align
        self.real_seg, self.real_offset = None, None
        self.offset = offset
        self.comment = comment

        #self._meta = meta

    def __deepcopy__(self, memo: dict[Any, Any]) -> "Data":
        cls = self.__class__
        result = cls.__new__(cls)
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v))
        return result

    def isobject(self) -> bool:
        return self.data_internal_type == DataType.OBJECT

    def setmembers(self, members: list["Data"]) -> None:
        self.__members = members

    def getmembers(self) -> list["Data"]:
        return self.__members

    def setvalue(self, value: list) -> None:
        if self.isobject():
            for m, v in zip(self.__members, value):
                m.setvalue(v)
        else:
            self.children = [value]

    def getlabel(self) -> str:
        return self.label

    def getsize(self) -> int:
        return self.size

    def gettype(self):
        return self.data_type

    def getinttype(self) -> DataType:
        return self.data_internal_type

    def getdata(self) -> Any:
        return self.label, self.data_type, self.data_internal_type, self.children, self.elements, self.size

    def is_align(self):
        return self.align

    def getrealaddr(self):
        return self.real_seg, self.real_offset

class Struct:
    STRUCT: Final[int] = 1
    UNION: Final[int] = 2

    def __init__(self, name: str, dtype: str) -> None:
        """Represent structure.

        :param name: Name
        :param dtype: Structure or Union?
        """
        self.name = name
        self.original_name = name
        self.used = True
        self.children: OrderedDict[str, Union[Data, Struct]] = OrderedDict()
        self.size = 0
        self.__type = Struct.UNION if dtype.lower() == "union" else Struct.STRUCT

    def append(self, data: Data) -> None:
        self.children[data.label.lower()] = data
        if self.__type == Struct.STRUCT:
            self.size += data.getsize()
        else:  # Union
            self.size = max(self.size, data.getsize())

    def getdata(self) -> OrderedDict:
        return self.children

    def getitem(self, key: str) -> Union[Data, "Struct"]:
        return self.children[key.lower()]

    def getsize(self) -> int:
        return self.size

    def gettype(self):
        return self.__type


class basejmp(baseop):
    pass


class _call(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._call(*self.children)


class _rep(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp"):
        return visitor._rep(*self.children)


class _add(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._add(*self.children)



class _mul(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._mul(self.children)  #


class _div(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._div(*self.children)



class _jne(basejmp):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._jnz(*self.children)


class _je(basejmp):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._jz(*self.children)


class _jb(basejmp):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._jc(*self.children)


class _jae(basejmp):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._jnc(*self.children)


class _jnb(basejmp):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._jnc(*self.children)


"""
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
"""

"""
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
"""


class _ret(baseop):
    def __init__(self, args: list[Any]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._ret(self.children)

class _retn(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._ret(self.children)

class _retf(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._retf(self.children)


class _lodsb(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()

    def accept(self, visitor: "Cpp") -> str:
        return visitor._lodsb()


class _scasb(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()

    def accept(self, visitor: "Cpp") -> str:
        return visitor._scasb()


class _scasw(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()

    def accept(self, visitor: "Cpp") -> str:
        return visitor._scasw()


class _scasd(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()

    def accept(self, visitor: "Cpp") -> str:
        return visitor._scasd()


class _cmpsb(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()

    def accept(self, visitor: "Cpp") -> str:
        return visitor._cmpsb()


class _lodsw(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()

    def accept(self, visitor: "Cpp") -> str:
        return visitor._lodsw()


class _lodsd(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()

    def accept(self, visitor: "Cpp") -> str:
        return visitor._lodsd()


class _stosd(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor: "Cpp") -> str:
        return visitor._stosd()


class _stosw(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor: "Cpp") -> str:
        return visitor._stosw()


class _stosb(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor: "Cpp") -> str:
        return visitor._stosb()


class _movsw(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor: "Cpp") -> str:
        return visitor._movsw()


class _movsd(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor: "Cpp") -> str:
        return visitor._movsd()


class _movsb(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()
        self.repeat = 1
        self.clear_cx = False

    def accept(self, visitor: "Cpp") -> str:
        return visitor._movsb()


class _int(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._int(*self.children)

"""
class _nop(baseop):
    def __init__(self, arg):
        super().__init__()
        pass

    def accept(self, visitor):
        return ""
"""

class label(baseop):

    def __init__(self, name: str, *, proc:str, isproc: bool=False, line_number: int=0, far: bool=False, globl: bool=True) -> None:
        """Label.

        :param name:
        :param proc:
        :param isproc:
        :param line_number:
        :param far:
        :param globl:
        """
        super().__init__()
        self.name = name
        self.original_name = name
        self.line_number = line_number
        self.far = far
        self.isproc = isproc
        self.used = False
        self.globl = globl
        self.proc = proc

    def accept(self, visitor):
        return visitor._label(self.name, self.isproc)


class _lea(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._lea(*self.children)


class _repe(baseop):
    def __init__(self, args) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp"):
        return visitor._repe(*self.children)


class _repne(baseop):
    def __init__(self, args: list[Any]) -> None:
        super().__init__()
        self.children = args

    def accept(self, visitor):
        return visitor._repne(*self.children)


class _jna(basejmp):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._jbe(*self.children)


class _jnbe(basejmp):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._ja(*self.children)


class _imul(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._imul(self.children)


class _movs(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._movs(*self.children)


class _lods(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._lods(*self.children)


class _scas(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._scas(*self.children)


class _leave(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()

    def accept(self, visitor: "Cpp") -> str:
        return visitor._leave()


class _idiv(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._idiv(*self.children)


class _instruction0(baseop):
    def __init__(self, arg: list[Any]) -> None:
        super().__init__()

    def accept(self, visitor: "Cpp") -> str:
        return visitor._instruction0(self.cmd)


class _instruction1(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._instruction1(self.cmd, *self.children)


class _jump(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._jump(self.cmd, *self.children)


class _instruction2(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._instruction2(self.cmd, *self.children)


class _instruction3(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._instruction3(self.cmd, *self.children)


class _equ(baseop):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.original_name = ""
        self.used = True
        self.original_type = ""
        self.implemented = False
        self.size = 0
        self.value: Expression
        self.element_size = 0

    def gettype(self):
        return self.original_type

    def accept(self, visitor):
        if self.implemented is False:
            self.implemented = True
            return visitor._equ(self.name)
        else:
            from masm2c.gen import SkipCode
            raise SkipCode


class _assignment(baseop):
    def __init__(self, args: list[Union[str, lark.Tree]]) -> None:
        super().__init__()
        self.children = args
        self.original_name = ""
        self.used = True
        self.original_type = ""
        self.implemented = False
        self.size = 0
        self.value: Expression

    def gettype(self):
        return self.original_type

    def accept(self, visitor):
        # if self.implemented == False:
        self.implemented = True
        return visitor._assignment(self.children)
        #    raise SkipCode

class _xlat(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        self.children = args

    def accept(self, visitor: "Cpp") -> str:
        return visitor._xlat(self.children)

class _mov(baseop):
    def __init__(self, args: list[Expression]) -> None:
        super().__init__()
        
        self.children = args
        self.syntetic = False

    def accept(self, visitor: "Cpp") -> str:
        return visitor._mov(*self.children)
