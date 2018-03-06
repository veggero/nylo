from nylo.base_objects.Token import Token
from nylo.struct_objects.Struct import Struct
from nylo.value_objects.Value import Value

class ValueLayer(Value):
    def __init__(self, value): self.value = value
    def evaluate(self, stack): 
        if hasattr(self.value, 'evaluate'): return self.value.evaluate(stack)
        return self.value
    
class PyStruct(Struct):
    
    def __init__(self, inputs, fun):
        from nylo.derived_objects.syntax_unrelated_objects import TypeDef, Set
        self.values = [TypeDef([ValueLayer(i) for i in inp]) for inp in inputs]
        self.values += [PyFun(fun, [i[-1] for i in inputs])]
        
class PyFun(Value):
    def __init__(self, fun, c): self.fun = fun
    def evaluate(self, stack): return self.fun(stack)
