from nylo.objects.NyObject import NyObject

class Set(NyObject):
    
    def __init__(self, by, to): self.by, self.to, self.value = by, to, [by, to]
