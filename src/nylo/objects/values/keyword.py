"""
Contains the definition of Keyword class.
"""

from nylo.objects.nyobject import NyObject


class Keyword(NyObject):
    """Any variable in the code.
    """

    def evaluate(self, stack):
        return stack[self]

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        elif isinstance(other, Keyword):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)
