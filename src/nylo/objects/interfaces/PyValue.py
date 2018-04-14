from nylo.objects.NyObject import NyObject
from nylo.objects.values    .Keyword import Keyword
from nylo.objects.values.Value import Value


class PyValue(NyObject):

    def __init__(self, value, types):
        self.typefun = types
        super().__init__(value)

    def evaluate(self, stack):
        return Value(self.value(stack))

    def settype(self, types, stack):
        self.types = self.typefun(stack)
        return self.types

    def __str__(self): return '<lambda>'
