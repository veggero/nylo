from nylo.lexers.Reader import Reader
from nylo.lexers.values.Value import Value
from nylo.lexers.values.Keyword import Keyword
from nylo.lexers.values.Symbol import Symbol
from nylo.lexers.values.NumStr import Number, String
from nylo.lexers.struct.Struct import Struct
from nylo.objects.Stack import Stack
from nylo.objects.interfaces.builtins import builtins

builtins.settype(['obj'], Stack())
nyglobals = Stack([builtins])
