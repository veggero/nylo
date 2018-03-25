from nylo.objects.NyObject import NyObject

class Value(NyObject):
    
    def evaluate(self, stack): return self.value.evaluate()
