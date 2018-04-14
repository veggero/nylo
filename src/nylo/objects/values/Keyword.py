from nylo.objects.NyObject import NyObject


class Keyword(NyObject):
    
    def __init__(self, value):
        self.value = value
        self.avaiable = {value}
        self.names = {self.value}

    def evaluate(self, stack): return stack[self]

    def __eq__(self, other):
        if isinstance(other, Keyword):
            return self.value == other.value
        elif isinstance(other, str):
            return self.value == other

    def __hash__(self): return hash(self.value)

    def settype(self, types, stack):
        self.types = types + stack[-1].typesof(self, stack)
        return self.types
