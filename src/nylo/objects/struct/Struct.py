from nylo.objects.NyObject import NyObject
from nylo.objects.struct.StructEl import Set, TypeDef
from nylo.objects.values.Keyword import Keyword
from time import sleep

class Struct(NyObject):
    
    def __init__(self, elements): *self.value, self.toreturn = elements
    
    def __str__(self): return '(%s -> %s)' % (', '.join(map(str, self.value)), str(self.toreturn))
        
    def __contains__(self, value):
        return any(element.by == value for element in self.value 
                   if isinstance(element, Set))
    
    def evaluate(self, stack): return self
    
    def calculate(self, stack):
        with stack(self):
            if self.toreturn: return self.toreturn.evaluate(stack)
            else: return self
        
    def update(self, other, stack):
        for element in other.value:
            if isinstance(element, Set):
                if isinstance(element.by, Keyword):
                    element.to = element.to.evaluate(stack)
                    self.value.append(element)
            else: 
                for i, el in enumerate(self.value):
                    if  isinstance(el, Keyword) or isinstance(el, TypeDef):
                        if isinstance(el, TypeDef) and el.ttype[0] != Keyword('obj'): 
                            element = element.evaluate(stack)
                        self.value[i] = Set(el, element)
                        break
        return self
        
    def getitem(self, value, stack):
        return next(element[value].evaluate(stack)
            for element in reversed(self.value)
            if isinstance(element, (Set, Call)) and value in element)

class Call(NyObject):
    
    def __init__(self, kw, struct): 
        self.kw, self.struct, self.value = kw, struct, (kw, struct)
        if not isinstance(self.struct, Struct):
            self.struct = Struct([self.struct, False])

    def __str__(self): return '%s%s' % (self.kw, self.struct)

    def evaluate(self, stack):
        self.called = stack[self.kw]
        self.called = Struct(self.called.value + [self.called.toreturn])
        if self.struct.toreturn:
            self.called.toreturn = self.struct.toreturn
        self.called = self.called.update(self.struct, stack)
        return self.called.calculate(stack)
