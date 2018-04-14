from collections import defaultdict
from copy import deepcopy

from nylo.objects.struct.Struct import Struct
from nylo.objects.NyObject import NyObject

class Call(NyObject):
    
    def __init__(self, kw, struct): 
        if not isinstance(struct, Struct):
            struct = Struct(defaultdict(list, {'atoms': [struct]}))
        self.kw, self.struct, self.value = kw, struct, (kw, struct)
        self.names = {self.kw.value}

    def __str__(self): return '%s%s' % (self.kw, self.struct)

    def evaluate(self, stack):
        self.tobdcalled = stack[self.kw]
        self.called = Struct(self.tobdcalled.value.copy())
        if 'self' in self.struct.value:
            self.called.value['self'] = self.struct.value['self']
        self.called.update(self.struct, stack)
        return self.called.calculate(stack)

    def settype(self, types, stack):
        self.called = stack[self.kw]
        self.called = Struct(self.called.value.copy())
        if 'self' in self.struct.value:
            self.called.value['self'] = self.struct.value['self']
        self.called.update(self.struct, stack, evaluate=False)
        with stack(self.called):
            self.types = self.called.value['self'][0].settype(types, stack)
        return self.types
