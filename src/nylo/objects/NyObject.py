class NyObject:
    
    def __init__(self, value): self.value = value
    
    def evaluate(self, stack): return self.value

    def __repr__(self): return '%s:{%s}' % (type(self).__name__, repr(self.value))
