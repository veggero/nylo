from nylo.objects.NyObject import NyObject

class Symbol(NyObject):
    
    def __init__(self, value, args): self.value, self.args = value, args
    
    def evaluate(self, stack): return 'oh'

    def __repr__(self): return '%s:%s' % (repr(self.value), repr(self.args))
