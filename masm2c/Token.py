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
from typing import Callable

import lark
from lark import Tree

SQEXPR = 'sqexpr'


class Token(lark.Tree):
    __slots__ = ('data', 'children')

    def __init__(self, type, value):
        raise Exception("Dead code?")
        self.data = type
        self.children = value


    # def __str__(self):
    #    return f"Token({self.data}, {self.children})"

    # def __repr__(self):
    #    return f"Token({self.data}, {self.children})"

    @staticmethod
    def find_tokens(expr, lookfor: str):
        l = []
        if isinstance(expr, Tree):
            if expr.data == lookfor:
                if len(expr.children) == 1:
                    l.append(expr.children[0])
                else:
                    l.append(expr.children)
            result = None
            if not isinstance(expr.children, str):
                result = Token.find_tokens(expr.children, lookfor)
            if result:
                l += result
        elif isinstance(expr, lark.Token):
            if expr.type == lookfor:
                l.append(expr.value)
        elif isinstance(expr, list):
            for i in range(len(expr)):
                if result := Token.find_tokens(expr[i], lookfor):
                    l += result
        if not l:
            l = None
        return l


    @staticmethod
    def remove_tokens(expr, lookfor: list):
        if isinstance(expr, Tree):
            if expr.data in lookfor:
                #if len(expr.children) == 1 and isinstance(expr.children[0], str):
                #    expr = None
                #else:
                expr = expr.children
                expr = Token.remove_tokens(expr, lookfor)
            else:
                expr.children = Token.remove_tokens(expr.children, lookfor)
            return expr
        elif isinstance(expr, list):
            l = []
            for i in range(len(expr)):
                result = Token.remove_tokens(expr[i], lookfor)
                if result != None:
                    if isinstance(result, list):
                        l.extend(result)
                    else:
                        l.append(result)
            # if not l:
            #    l = None
            return l
        return expr



class Expression(lark.Tree):

    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            args = "expr", []
        super().__init__(*args, **kwargs)
        from masm2c.enum import IndirectionType
        #kwargs['children'] = kwargs.get('children', [])
        self.data = "expr"
        #self.children = []
        self.indirection: IndirectionType = IndirectionType.VALUE
        self.element_size = 0
        self.element_number = 1
        self.element_size_guess = 0
        self.ptr_size = 0
        self.mods = set()
        self.registers = set()
        self.segment_register = "ds"
        self.segment_overriden = False
        #import traceback
        #self.source = traceback.format_stack()

    def size(self):
        from masm2c.enum import IndirectionType
        if self.indirection == IndirectionType.POINTER:
            return self.ptr_size
        #elif self.indirection == IndirectionType.OFFSET:
        #    return 2
        else:
            result = self.element_size * self.element_number
            return result
            try:
                from masm2c.parser import Parser
                from masm2c.cpp import IR2Cpp
                from masm2c.gen import guess_int_size
                result = result or max(self.element_size_guess, guess_int_size(eval("".join(IR2Cpp(Parser()).visit(self)))))  # TODO is this required? Reduces perf?
            except:
                pass
            return result

