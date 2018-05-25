"""
Contains the Stack class definition.
"""

from nylo.objects.struct.struct import Struct


class Stack(list):
    """Stack to store the stack calls
    of nylo functions. Can also wrap a value
    inside a stack.
    """

    def __init__(self, elements=None, wrapped=None):
        self.wrapped = wrapped
        list.__init__(self, elements if elements else [Struct()])

    def wrap(self, element):
        """Create a new stack with the element wrapped"""
        return Stack(self[:], element)

    def evaluate(self, _):
        """Evaluate the element wrapped using this stack"""
        return self.wrapped.evaluate(self)

    def __getitem__(self, value):
        if isinstance(value, (int, slice)):
            return list.__getitem__(self, value)
        return self[-1].getitem(value, self)

    def __contains__(self, value):
        return value in self[-1]

    def __enter__(*args):
        pass

    def __exit__(self, *args):
        self.pop()

    def __call__(self, value):
        self.append(Struct(self[-1].value.copy()))
        self[-1].value.update(value.value)
        return self

    def __str__(self):
        return "{%s}" % '; '.join(map(str, self))
