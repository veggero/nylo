from nylo.objects.interfaces.PyValue import PyValue
from nylo.objects.struct.Struct import Struct
from nylo.objects.struct.StructEl import Set, TypeDef
from nylo.objects.values.Keyword import Keyword

builtins = Struct([
    
    Set(Keyword('double'), Struct([
            TypeDef([Keyword('int'), Keyword('n')])
            , PyValue(lambda stack: stack[Keyword('n')].value*2) ])),
    
    Set(Keyword('if'), Struct([
            TypeDef([Keyword('bool'), Keyword('cond')]),
            TypeDef([Keyword('obj'), Keyword('first')]),
            TypeDef([Keyword('obj'), Keyword('second')])
            , PyValue(
    lambda stack: 
        stack[Keyword('first')].value 
        if stack[Keyword('cond')].value
        else stack[Keyword('second')].value )]))
    
    , False])
