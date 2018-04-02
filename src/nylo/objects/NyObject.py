class NyObject:
    
    def __init__(self, value): self.value = value
    
    def evaluate(self, stack):
        if hasattr(self.value, 'evaluate'):
            return self.value.evaluate(stack)
        else: return self

    def __repr__(self): return '%s:{%s}' % (type(self).__name__, repr(self.value))
    
    def __str__(self): return str(self.value)

    def __eq__(self, other): return self.value == other.value
