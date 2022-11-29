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


#from masm2c.gen import IndirectionType

SQEXPR = 'sqexpr'


class Token(lark.Tree):
    __slots__ = ('data', 'children')

    def __init__(self, type, value):
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
        elif isinstance(expr, list):
            for i in range(len(expr)):
                if result := Token.find_tokens(expr[i], lookfor):
                    l += result
        if not l:
            l = None
        return l

    @staticmethod
    def find_and_replace_tokens(expr, lookfor: str, call: Callable):
        if isinstance(expr, Tree):
            if expr.data == lookfor:
                if call:
                    expr = call(expr)
            elif not isinstance(expr.children, str):
                expr.children = Token.find_and_replace_tokens(expr.children, lookfor, call)
        elif isinstance(expr, list):
            expr = [Token.find_and_replace_tokens(i, lookfor, call) for i in expr]
        return expr

    @staticmethod
    def remove_squere_bracets(expr, index=None):
        if index is None:
            index = 0
        if isinstance(expr, Tree):
            if expr.data == SQEXPR:
                expr = expr.children
                expr, index = Token.remove_squere_bracets(expr, index)
            else:
                oldindex = index
                expr.children, index = Token.remove_squere_bracets(expr.children, index)
                if isinstance(expr.children, str) and not (expr.data == 'integer' and expr.children[0] in ['-', '+']):
                    index = oldindex
                    index += 1
                    if index != 1:
                        expr = ['+', expr]
            return expr, index
        elif isinstance(expr, list):
            for i in range(len(expr)):
                expr[i], index = Token.remove_squere_bracets(expr[i], index)
        else:
            index = 0
        return expr, index

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

    def __init__(self):
        super().__init__("expr", [])
        #self.data = "expr"
        #self.children = []
        self.element_size = 0
        self.element_number = 1
        self.element_size_guess = 0
        self.ptr_size = 0
        self.mods = set()
        self.registers = set()
        self.segment_register = "ds"

    def size(self):
        if 'ptrdir' in self.mods:
            return self.ptr_size
        else:
            result = self.element_size * self.element_number
            try:
                from masm2c.parser import Parser
                from masm2c.cpp import IR2Cpp
                from masm2c.gen import guess_int_size
                result = max(result, self.element_size_guess, guess_int_size(eval("".join(IR2Cpp(Parser()).visit(self)))))  # TODO is this required? Reduces perf?
            except:
                pass
            return result
