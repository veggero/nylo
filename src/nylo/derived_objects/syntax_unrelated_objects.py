import copy

from nylo.exceptions import cant_call
from nylo.base_objects.Token import Token

"""
TODO: DELETE
class Call(Token):
    
    def __init__(self, keyword, struct):
        self.keyword = keyword
        self.struct = struct
        
    def evaluate(self, stack):
        from nylo.struct_objects.Struct import Struct
        to_call = copy.deepcopy(self.keyword.evaluate(stack))
        if not isinstance(to_call, Struct): cant_call(to_call)
        self.struct.evaluate_values(stack)
        to_call.update(self.struct, stack)
        return to_call.evaluate(stack)
"""
                
class Get(Token):
    def __init__(self, source, value): self.source, self.value= source, value
        
class Set(Token):
    def __init__(self, target, value): self.target, self.value = target, value
    def evaluate(self, stack): return self.value.evaluate(stack)

class TypeDef(Token):
    def __init__(self, kws): self.kws = kws
    def evaluate(self, stack): pass
        
class Output(Token):
    def __init__(self, value, to): self.value, self.to = value, to
