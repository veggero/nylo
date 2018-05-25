"""
Contains the NyObject class definition.
"""

class NyObject:
    """Abstract class for every object
    in Nylo
    """

    def __init__(self, value):
        self.value = value

    def evaluate(self, stack):
        """Evaluate the object"""
        return (self.value.evaluate(stack)
                if hasattr(self.value, 'evaluate') else self)

    def __repr__(self):
        return '%s:{%s}' % (type(self).__name__, repr(self.value))

    def __str__(self):
        return '%s' % self.value

    def __hash__(self):
        return hash(self.value)
