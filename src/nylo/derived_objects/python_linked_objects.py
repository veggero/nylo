from nylo.base_objects.Token import Token
from nylo.struct_objects.Struct import Struct

class ValueLayer(Token):
    condition = []
    def __init__(self, value): self.value = value
    def evaluate(self, stack): 
        if hasattr(self.value, 'evaluate'): return self.value.evaluate(stack)
        return self.value
    
class PyStruct(Struct):
    
    def __init__(self, inputs, fun):
        from nylo.derived_objects.syntax_unrelated_objects import TypeDef, Set
        self.values = [ValueLayer(
                            TypeDef([ValueLayer(i) for i in inp])
                        ) 
                       for inp in inputs]
        self.values += [ValueLayer(Set(TypeDef([ValueLayer('_self')]), 
                                       PyFun(fun, [i[-1] for i in inputs])))]
        
class PyFun:
    
    def __init__(self, fun, c): 
        self.fun = fun
        self.condition = c
    def evaluate(self, stack): 
        try: return self.fun(stack)
        except KeyError: raise NameError
