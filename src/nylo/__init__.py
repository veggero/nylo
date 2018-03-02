import string
import copy
import readline

from .builtins import builtins
from .base_objects.Reading import *
from .base_objects.Token import *
from .derived_objects.python_linked_objects import *
from .derived_objects.syntax_unrelated_objects import *
from .struct_objects.Block import *
from .struct_objects.Struct import *
from .struct_objects.StructEl import *
from .syntax_objects.Keyword import *
from .syntax_objects.Symbol import *
from .syntax_objects.SymbolOperation import *
from .value_objects.NumStr import *
from .value_objects.Value import *

def run(code):
    global builtins
    struct = Struct(Reading('({c})'.format(c=code), 0)).evaluate(builtins)
    return struct.get_value('main', nylo)
