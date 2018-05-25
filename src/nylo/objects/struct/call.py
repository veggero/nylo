from collections import defaultdict
from nylo.objects.struct.struct import Struct
from nylo.objects.nyobject import NyObject
from nylo.objects.values.keyword import Keyword
from nylo.objects.values.symbol import Symbol


class Call(NyObject):

    def __init__(self, kw, struct):
        if not isinstance(struct, Struct):
            struct = Struct(defaultdict(list, {'atoms': [struct]}))
        self.kw, self.struct, self.value = kw, struct, (kw, struct)

    def __str__(self): return '%s%s' % (self.kw, self.struct)

    def evaluate(self, stack):
        self.tobdcalled = self.kw.evaluate(stack)
        self.called = Struct(self.tobdcalled.value.copy())
        self.called.update(self.struct, stack)
        if self.struct.value['self']:
            with stack(self.called):
                return self.struct.getitem('self', stack)
        return self.called.evaluate(stack)
