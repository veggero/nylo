from nylo.objects.NyObject import NyObject
from nylo.objects.struct.StructEl import Set, TypeDef
from nylo.objects.values.Keyword import Keyword

class Struct(NyObject):
    
    def __init__(self, elements): *self.value, self.toreturn = elements
    
    def __str__(self): return '(%s -> %s)' % (', '.join(map(str, self.value)), str(self.toreturn))
        
    def __contains__(self, value):
        from nylo.objects.struct.Call import Call
        return any(value in element for element in self.value 
                   if isinstance(element, (Set, Call)) )
    
    def evaluate(self, stack): return self
    
    def calculate(self, stack):
        with stack(self):
            if self.toreturn: return self.toreturn.evaluate(stack)
            else: return self
        
    def update(self, other, stack):
        for element in other.value:
            if isinstance(element, Set):
                if isinstance(element.by, Keyword):
                    element.to = element.to.evaluate(stack)
                    self.value.append(element)
                else: continue 
            for i, el in enumerate(self.value):
                if  isinstance(el, Keyword) or isinstance(el, TypeDef):
                    if isinstance(el, TypeDef) and el.ttype[0] != Keyword('obj'): 
                        element = element.evaluate(stack)
                    self.value[i] = Set(el, element)
                    break
        return self
        
    def getitem(self, value, stack):
        from nylo.objects.struct.Call import Call
        return next(element.getitem(value, stack).evaluate(stack)
            for element in reversed(self.value)
            if isinstance(element, (Set, Call)) and value in element)
