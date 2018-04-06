from nylo.objects.interfaces.PyValue import PyValue
from nylo.objects.struct.Struct import Struct
from nylo.objects.struct.StructEl import Set, TypeDef
from nylo.objects.values.Keyword import Keyword

builtins = Struct([
    
    Set(Keyword('double'), Struct([
            TypeDef([Keyword('int'), Keyword('n')]),
            PyValue(lambda stack: stack[Keyword('n')].value*2) ])),
    
    Set(Keyword('if'), Struct([
            TypeDef([Keyword('bool'), Keyword('cond')]),
            TypeDef([Keyword('obj'), Keyword('first')]),
            TypeDef([Keyword('obj'), Keyword('second')]),
            PyValue(
    lambda stack: 
        stack[Keyword('first')].value 
        if  stack[Keyword('cond')].value
        else stack[Keyword('second')].value )])),
    
    Set(Keyword('sum'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('b')].value +
                stack[Keyword('a')].value)])),
    
    Set(Keyword('sub'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value -
                stack[Keyword('b')].value )])),
    
    Set(Keyword('mul'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value *
                stack[Keyword('b')].value )])),
    
    Set(Keyword('div'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value /
                stack[Keyword('b')].value )])),
    
    Set(Keyword('equal'), Struct([
            TypeDef([Keyword('obj'), Keyword('a')]),
            TypeDef([Keyword('obj'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value ==
                stack[Keyword('b')].value )])),
    
    Set(Keyword('all'), Struct([
            TypeDef([Keyword('bool'), Keyword('a')]),
            TypeDef([Keyword('bool'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value and
                stack[Keyword('b')].value )])),
    
    Set(Keyword('greater'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value >
                stack[Keyword('b')].value )])),
    
    Set(Keyword('less_than'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value <
                stack[Keyword('b')].value )])),
    
    Set(Keyword('inequal'), Struct([
            TypeDef([Keyword('obj'), Keyword('a')]),
            TypeDef([Keyword('obj'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value !=
                stack[Keyword('b')].value )])),
    
    Set(Keyword('div'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value /
                stack[Keyword('b')].value )])),
    
    Set(Keyword('greater_or_equal'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value >=
                stack[Keyword('b')].value )])),
            
    Set(Keyword('less_than_or_equal'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value >=
                stack[Keyword('b')].value )])),
            
    Set(Keyword('pow'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value **
                stack[Keyword('b')].value )])),
            
    Set(Keyword('mod'), Struct([
            TypeDef([Keyword('int'), Keyword('a')]),
            TypeDef([Keyword('int'), Keyword('b')]),
            PyValue(lambda stack: 
                stack[Keyword('a')].value %
                stack[Keyword('b')].value )])),
            
    False])
