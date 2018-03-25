from nylo.objects.NyObject import NyObject

class Call(NyObject):
    
    def __init__(self, kw, call): 
        self.kw, (*self.call, self.out), self.value = kw, call, [kw, call]
    
    def evaluate(self, stack): pass #TODO
