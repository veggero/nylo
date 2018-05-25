"""
Contains the PyValue class definition.
"""

from nylo.objects.nyobject import NyObject
from nylo.objects.values.value import Value


class PyValue(NyObject):
    """This class is used to define interface
    a python value to Nylo, and it's derived
    from NyObject.

    It's a Nylo value that is evaluated using a
    Python function.
    """

    def __init__(self, value, types):
        self.typefun = types
        super().__init__(value)

    def __str__(self) -> str:
        return '<lambda>'

    def evaluate(self, stack):
        output = self.value(stack)
        if not isinstance(output, NyObject):
            output = Value(output)
        return output
