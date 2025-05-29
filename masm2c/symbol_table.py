"""Symbol Table for managing global symbols in masm2c."""

import logging
from collections import OrderedDict
from typing import Any, TYPE_CHECKING, Union

# Avoid circular imports for type hints
if TYPE_CHECKING:
    from masm2c.op import Struct, label, var, _equ, _assignment
    from masm2c.proc import Proc
    from lark.lexer import Token

# Define the type alias for possible symbol values
SymbolValue = Union['Struct', 'label', 'Proc', 'var', '_equ', '_assignment']

def _format_object(value: SymbolValue) -> str:
    """Helper to represent object as string (copied from parser.py)."""
    import re
    if not hasattr(value, "__dict__"):
        return ""
    stuff = str(vars(value))
    replacements = (
        (r"\n", " "),
        (r"[{}]", ""),
        (r"'([A-Za-z_0-9]+)'\s*:\s*", r"\g<1>="),
    )
    for old, new in replacements:
        stuff = re.sub(old, new, stuff)
    stuff = f"{value.__class__.__name__}({stuff})"
    return stuff

class SymbolTable:
    """Manages global symbols for the MASM parser."""

    def __init__(self) -> None:
        self.symbols: OrderedDict[str, SymbolValue] = OrderedDict()
        self.pass_number = 0 # Track pass number for definition checks
        self.test_mode = False # To allow redefinition in tests

    def set_pass_info(self, pass_number: int, test_mode: bool) -> None:
        """Set pass number and test mode from the main parser."""
        self.pass_number = pass_number
        self.test_mode = test_mode

    def set_global(self, name: str, value: SymbolValue) -> None:
        """Adds or updates a global symbol."""
        if not name:
            raise NameError("empty name is not allowed")
        value.original_name = name # Keep track of original casing/name
        name = name.lower()

        logging.debug("SymbolTable.set_global(name='%s', value=%s)", name, _format_object(value))
        if name in self.symbols and self.pass_number == 1 and not self.test_mode:
            # Allow redefinition in later passes or test mode
            raise LookupError(f"global {name} was already defined in pass 1")
        value.used = False # Mark as unused initially
        self.symbols[name] = value

    def reset_global(self, name: str, value: SymbolValue) -> None:
        """Forcefully overwrite a global symbol, bypassing normal checks.
        
        Use this method only when intentionally replacing an existing symbol,
        such as during procedure merging or other advanced transformations.
        
        Args:
            name: Original symbol name
            value: New symbol value
        """
        if not name:
            raise NameError("empty name is not allowed")
        value.original_name = name
        name = name.lower()
        logging.debug("SymbolTable.reset_global(name='%s', value=%s)", name, value)
        self.symbols[name] = value

    def get_global(self, name: Union['Token', str]) -> Any:
        """Retrieve a global symbol without marking it as used.
        
        Args:
            name: Symbol name (either as string or Token)
            
        Returns:
            The symbol object if found, otherwise None
        """
        name_str = str(name).lower()
        logging.debug("SymbolTable.get_global(%s)", name_str)
        return self.symbols.get(name_str)

    def get_and_mark_global(self, name: Union['Token', str]) -> Any:
        """Retrieve a global symbol and mark it as used in the current context.
        
        This method both fetches the symbol and updates its 'used' flag,
        which helps track which symbols are actually referenced in the code.
        
        Args:
            name: Symbol name (either as string or Token)
            
        Returns:
            The symbol object if found, otherwise None
        """
        name_str = str(name).lower()
        logging.debug("SymbolTable.get_and_mark_global(%s)", name_str)
        symbol = self.symbols.get(name_str)
        logging.debug("Found type: %s", type(symbol))
        if symbol is None:
            logging.debug("SymbolTable KeyError: %s", name_str)
            return None
        symbol.used = True
        return symbol

    def get_globals(self) -> OrderedDict[str, SymbolValue]:
        """Returns the entire dictionary of global symbols."""
        return self.symbols

    def __contains__(self, name: str) -> bool:
        """Allows checking 'if name in symbol_table'."""
        return name.lower() in self.symbols