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
    def find_and_call_tokens(expr, lookfor, call=None):
        l = []
        if isinstance(expr, Token):
            if expr.type == lookfor:
                if call:
                    expr.value = call(expr.value)
                l.append(expr.value)

            result = None
            if not isinstance(expr.value, str):
                result = Token.find_and_call_tokens(expr.value, lookfor, call)
            if result:
                l = l + result
        elif isinstance(expr, list):
            for i in range(0, len(expr)):
                result = Token.find_and_call_tokens(expr[i], lookfor, call)
                if result:
                    l = l + result
        if not l:
            l = None
        return l


    @staticmethod
    def remove_squere_bracets(expr, index=0):
        if isinstance(expr, Token):
            index += 1
            expr.value, _ = Token.remove_squere_bracets(expr.value, index)
            if expr.type == SQEXPR:
                expr = expr.value
                if index != 1:
                    expr = ['+', expr]
            return expr, index
        elif isinstance(expr, list):
            for i in range(0, len(expr)):
                expr[i], index = Token.remove_squere_bracets(expr[i], index)
        else:
            index += 1
        return expr, index


    @staticmethod
    def remove_tokens(expr, lookfor):
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
                if result:
                    l.append(result)
            if not l:
                l = None
            return l
        return expr
