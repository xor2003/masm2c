"""
Defines enumerations for different types of data and addressing modes used in the translation process.
"""
from enum import Enum


class IndirectionType(Enum):
    OFFSET = -1
    VALUE = 0
    POINTER = 1
