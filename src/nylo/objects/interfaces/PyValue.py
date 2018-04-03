from nylo.objects.NyObject import NyObject
from nylo.objects.values    .Keyword import Keyword
from nylo.objects.values.Value import Value

class PyValue(NyObject):
    
    def evaluate(self, stack): 
        return Value(self.value(stack))
