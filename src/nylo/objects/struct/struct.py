from nylo.objects.nyobject import NyObject
from nylo.objects.struct.structel import TypeDef
from nylo.objects.values.keyword import Keyword as Kw
from collections import defaultdict


class Struct(NyObject):

    def __init__(self, value=defaultdict(list)):
        self.value = value

    def __str__(self):
        return '(%s)' % (', '.join(
            '%s: %s' % (key, ' | '.join(map(str, val))
                        if not isinstance(val, Struct) else '...') if not key == 'atoms'
            else ', '.join(map(str, val)) for key, val in self.value.items()))

    def __contains__(self, value):
        return (self.value[value.value])
    
    def evaluate(self, stack): 
        if ['_arg'] in self.value.values() or not self.value['self']:
            return self
        with stack(self):
            return self.getitem('self', stack)

    def update(self, other, stack):
        for element in other.value['atoms']:
            self.drop(element, stack)
        self.value.update({a:b for a,b in other.value.items() 
                           if a not in (Kw('self'), Kw('atoms'))})

    def drop(self, element, stack):
        for key in self.value:
            if self.value[key] != [Kw('_arg')]:
                continue
            if not (isinstance(key, TypeDef) and key.ttype[-1] == 'obj'):
                element = element.evaluate(stack)
            self.value[key] = [element]
            break

    def getitem(self, value, stack):
        return self.value[value][-1].evaluate(stack)

    # def settype(self, types, stack):
    #    self.types = types
    #    with stack(self):
    #        for key, value in self.value.items():
    #            for element in value:
    #                element.settype(types + [key], stack)
    #    return self.types

    # def typesof(self, element, stack):
    #    for key in self.value:
    #        if key == element:
    #            if isinstance(key, Keyword):
    #                return ['obj']
    #            elif isinstance(key, TypeDef):
    #                return key.ttype
    #    print(self)
    #    raise TypeError("Couldn't get '%s' in any way." % element)
