from collections import defaultdict

from nylo.objects.interfaces.PyValue import PyValue
from nylo.objects.struct.Struct import Struct
from nylo.objects.struct.StructEl import TypeDef
from nylo.objects.values.Keyword import Keyword

builtins = Struct(defaultdict(list, {
    'if': [Struct(defaultdict(list, {
        'cond': [],
        TypeDef(('obj', Keyword('first'))): [],
        TypeDef(('obj', Keyword('second'))): [],
        'self': [PyValue(
            lambda stack: 
                stack[Keyword('first')].value 
                if  stack[Keyword('cond')].value
                else stack[Keyword('second')].value,
            lambda stack:
                stack[-1].typesof('first', stack) +
                stack[-1].typesof('second', stack) )]
        }))],
    }))
