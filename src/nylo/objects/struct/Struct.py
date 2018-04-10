from nylo.objects.NyObject import NyObject
from nylo.objects.struct.StructEl import TypeDef
from nylo.objects.values.Keyword import Keyword

class Struct(NyObject):
    
    def __init__(self, value):
        self.value = value
        self.names = set()
    
    def __str__(self): return '(%s)' % ', '.join('%s: %s' % (key, ' | '.join(map(str, val))) 
                                                 for key, val in self.value.items())
        
    def __contains__(self, value): return len(self.value[value.value]) > 0

    def __getitem__(self, value): return self.value[value]
    
    def evaluate(self, stack): return self
    
    def calculate(self, stack):
        with stack(self):
            if 'self' in self.value: 
                return self.value['self'][0].evaluate(stack)
            else: return self
        
    def update(self, other, stack):
        for key, value in other.value.items():
            if key in ('atoms', 'self'): continue
            self[key] = self[key] + value
        for element in other.value['atoms']:
            self.drop(element, stack)
            
    def drop(self, element, stack):
        for key, value in self.value.items():
            if value == []:
                if not (isinstance(key, TypeDef) and key.ttype[-1] == 'obj'):
                    element = element.evaluate(stack)
                self.value[key] = self.value[key] + [element]
                return
        raise TypeError('Structure %s cannot accept value "%s"' % (self, element))
        
    def getitem(self, value, stack):
        for element in self[value]:
            return element.evaluate(stack)
        raise TypeError("Couldn't get '%s' in any way." % value)
