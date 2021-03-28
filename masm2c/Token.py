from typing import Callable

SQEXPR = 'sqexpr'


class Token:
    __slots__ = ('type', 'value')

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token(%s, %s)" % (self.type, self.value)

    def __repr__(self):
        return "Token('%s', '%s')" % (self.type, self.value)

    @staticmethod
    def find_tokens(expr, lookfor: str):
        l = []
        if isinstance(expr, Token):
            if expr.type == lookfor:
                l.append(expr.value)

            result = None
            if not isinstance(expr.value, str):
                result = Token.find_tokens(expr.value, lookfor)
            if result:
                l = l + result
        elif isinstance(expr, list):
            for i in range(0, len(expr)):
                result = Token.find_tokens(expr[i], lookfor)
                if result:
                    l = l + result
        if not l:
            l = None
        return l

    @staticmethod
    def find_and_replace_tokens(expr, lookfor: str, call: Callable):
        if isinstance(expr, Token):
            if expr.type == lookfor:
                if call:
                    expr = call(expr)
            elif not isinstance(expr.value, str):
                expr.value = Token.find_and_replace_tokens(expr.value, lookfor, call)
        elif isinstance(expr, list):
            expr = [Token.find_and_replace_tokens(i, lookfor, call) for i in expr]
        return expr

    @staticmethod
    def remove_squere_bracets(expr, index=None):
        if index == None:
            index = 0
        if isinstance(expr, Token):
            if expr.type == SQEXPR:
                expr = expr.value
                expr, index = Token.remove_squere_bracets(expr, index)
            else:
                oldindex = index
                expr.value, index = Token.remove_squere_bracets(expr.value, index)
                if isinstance(expr.value, str) and not (expr.type == 'INTEGER' and expr.value[0] in ['-', '+']):
                    index = oldindex
                    index += 1
                    if index != 1:
                        expr = ['+', expr]
            return expr, index
        elif isinstance(expr, list):
            for i in range(0, len(expr)):
                expr[i], index = Token.remove_squere_bracets(expr[i], index)
        else:
            index = 0
        return expr, index


    @staticmethod
    def remove_tokens(expr, lookfor: list):
        if isinstance(expr, Token):
            if expr.type in lookfor:
                if isinstance(expr.value, str):
                    expr = None
                else:
                    expr = expr.value
                    expr = Token.remove_tokens(expr, lookfor)
                return expr
            else:
                expr.value = Token.remove_tokens(expr.value, lookfor)
                return expr
        elif isinstance(expr, list):
            l = []
            for i in range(0, len(expr)):
                result = Token.remove_tokens(expr[i], lookfor)
                if result != None:
                    l.append(result)
            #if not l:
            #    l = None
            return l
        return expr
