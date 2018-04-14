class NyObject:

    def __init__(self, value):
        self.value = value
        if hasattr(value, 'names'):
            self.names = value.names
        else:
            self.names = set()
        self.avaiable = set()

    def evaluate(self, stack):
        return (self.value.evaluate(stack)
                if hasattr(self.value, 'evaluate') else self)

    def __repr__(self): return '%s:{%s}' % (
        type(self).__name__, repr(self.value))

    def __str__(self): return '%s' % self.value

    def __hash__(self): return hash(self.value)

    def __eq__(self, other): return hash(self) == hash(other)
