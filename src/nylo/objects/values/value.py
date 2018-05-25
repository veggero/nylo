from collections import defaultdict
from nylo.objects.nyobject import NyObject


class Value(NyObject): pass


class GetObj(NyObject):

    def __init__(self, value, index):
        self.value, self.index = value, index

    def evaluate(self, stack):
        from nylo.objects.struct.struct import Struct
        i = self.index.evaluate(stack).value
        l = self.value.evaluate(stack)['atoms']
        o = l[i]
        if isinstance(o, list):
            return Struct(defaultdict(list, {'atoms': o}))
        else:
            return o.evaluate(stack)
