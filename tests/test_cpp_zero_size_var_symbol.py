from masm2c import op
from masm2c.cpp import Cpp


class _Symbols:
    def __init__(self, obj: op.var) -> None:
        self._obj = obj

    def get_and_mark_global(self, name: str):
        return self._obj if name.lower() == self._obj.name else None


class _Context:
    def __init__(self, obj: op.var) -> None:
        self.proc_list = []
        self.symbols = _Symbols(obj)
        self.args = {}


def test_convert_label_keeps_zero_size_symbol_as_scalar() -> None:
    symbol = op.var(size=0, offset=0, name='ARGC')
    context = _Context(symbol)
    cpp = Cpp(context, outfile='')

    rendered = cpp.convert_label_('argc')

    assert rendered == 'argc'


def test_convert_char_keeps_symbolic_name() -> None:
    symbol = op.var(size=0, offset=0, name='ARGC')
    context = _Context(symbol)
    cpp = Cpp(context, outfile='')

    assert cpp.convert_char('NUL') == 'NUL'
