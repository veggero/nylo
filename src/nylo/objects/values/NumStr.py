from nylo.objects.NyObject import NyObject

class Number(NyObject):
    
    def __add__(self, other): return Number(self.value + other.value)

    def __sub__(self, other): return Number(self.value - other.value)

class String(NyObject): 
    
    def __str__(self): return '"%s"' % self.value
