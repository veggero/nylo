from nylo.objects.struct.Struct import Struct
from nylo.objects.NyObject import NyObject
from nylo.objects.struct.StructEl import Set

class Call(NyObject):
    
    def __init__(self, kw, struct): 
        self.kw, self.struct, self.value = kw, struct, (kw, struct)
        if not isinstance(self.struct, Struct):
            self.struct = Struct([self.struct, False])

    def __str__(self): return '%s%s' % (self.kw, self.struct)

    def __contains__(self, value):
        return any(value == element.to for element 
                   in self.struct.value if isinstance(element, Set))
    
    def getitem(self, value, stack):
        self.struct.toreturn = next(element.by
            for element in self.struct.value
            if isinstance(element, Set) and value == element.to)
        return self.evaluate(stack)

    def evaluate(self, stack):
        self.called = stack[self.kw]
        self.called = Struct(self.called.value + [self.called.toreturn])
        if self.struct.toreturn:
            self.called.toreturn = self.struct.toreturn
        self.called = self.called.update(self.struct, stack)
        return self.called.calculate(stack)
