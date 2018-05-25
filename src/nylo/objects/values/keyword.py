from nylo.objects.nyobject import NyObject


class Keyword(NyObject):

    def __init__(self, value):
        self.value = value

    def evaluate(self, stack): return stack[self]

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return self.value == other.value

    def __hash__(self): return hash(self.value)
