from nylo.objects.NyObject import NyObject

class Set(NyObject):
    
    def __init__(self, by, to): self.by, self.to, self.value = by, to, (by, to)
    
    def __str__(self): return '%s: %s' % (self.by, self.to)

    def __contains__(self, value): return self.by == value

    def __getitem__(self, value): return self.to

class TypeDef(NyObject):
    
    def __init__(self, kws): *self.ttype, self.value = kws
    
    def __str__(self): return ' '.join(str(k) for k in self.ttype + [self.value])

    def __eq__(self, other): return other == self.value
