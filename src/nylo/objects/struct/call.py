"""
Contains the Call class definition.
"""

from collections import defaultdict
from nylo.objects.struct.struct import Struct
from nylo.objects.nyobject import NyObject


class Call(NyObject):
    """Call class is used to do
    calls when an object is found
    between parenthesis.

    It does a copy of the object and update
    it using struct value and then returns the
    evaluated object.
    """

    def __init__(self, called, caller):
        if not isinstance(caller, Struct):
            caller = Struct(defaultdict(list, {'atoms': [caller]}))
        self.called, self.caller = called, caller

    def __str__(self):
        return '%s%s' % (self.called, self.caller)

    def evaluate(self, stack):
        called_struct = Struct(self.called.evaluate(stack).value.copy())
        called_struct.update(self.caller, stack)
        if self.caller.value['self']:
            with stack(called_struct):
                return self.caller.getitem('self', stack)
        return called_struct.evaluate(stack)
