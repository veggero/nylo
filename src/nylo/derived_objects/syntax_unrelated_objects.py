import copy

from nylo.base_objects.Token import Token

class Call(Token):
    
    def __init__(self, keyword, struct):
        self.keyword = keyword
        self.struct = struct
        self.condition = keyword.condition+struct.condition
        
    def evaluate(self, stack):
        from nylo.struct_objects.Struct import Struct
        to_call = copy.deepcopy(self.keyword.evaluate(stack))
        if not isinstance(to_call, Struct): 
            raise TypeError('{name} object is not callable'.format(
                name=self.keyword.value))
        to_call.update(self.struct, stack)
        return to_call.called(stack)
                
class Get(Token):
    
    def __init__(self, source, value):
        self.source = source
        self.value = value
        self.condition = source.condition + value.condition
        
    def evaluate(self, stack): raise Exception('WTF')
        
class Set(Token):
    
    def __init__(self, target, value):
        self.target = target
        self.value = value  
        self.condition = value.condition
        
    def evaluate(self, stack): return self.value.evaluate(stack)

class TypeDef(Token):
    
    def __init__(self, kws):
        self.kws = kws
        self.condition = []
        for kw in kws:
            self.condition.extend(kw.condition)
        
    def evaluate(self, stack): pass
        
class Output(Token):
    
    def __init__(self, value, to):
        self.value = value
        self.to = to
        self.condition = value.condition + to.condition
        
    def evaluate(self, stack): raise Exception('WTF')
