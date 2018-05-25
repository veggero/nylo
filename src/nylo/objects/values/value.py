"""
Contains Value and GetObj class definitions.
"""

from collections import defaultdict
from nylo.objects.nyobject import NyObject


class Value(NyObject):
    """Simple value wrapper"""
    pass


class GetObj(NyObject):
    """Class to manage index gets, such as
    ```(1,2,3)[2]```
    """

    def __init__(self, value, index):
        self.index = index
        super().__init__(value)

    def evaluate(self, stack):
        """Get the given index from the value"""
        from nylo.objects.struct.struct import Struct
        index = self.index.evaluate(stack).value
        output = self.value.evaluate(stack)['atoms'][index]
        if isinstance(output, list):
            return Struct(defaultdict(list, {'atoms': output}))
        return output.evaluate(stack)
