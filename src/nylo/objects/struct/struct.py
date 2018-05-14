from nylo.objects.nyobject import NyObject
from nylo.objects.struct.structel import TypeDef
from nylo.objects.values.keyword import Keyword
from collections import defaultdict


class Struct(NyObject):

    def __init__(self, value=defaultdict(list)):
        self.value = value
        self.names = set().union(*[n.names for n in value['atoms']])

    def __str__(self):
        dictlike = ', '.join(
            '%s: %s' % (key, ' | '.join(map(str, val))
                        if not isinstance(val, Struct) else '...') if not key == 'atoms'
            else ', '.join(map(str, val)) for key, val in self.value.items())
        return '(%s)' % dictlike

    def __contains__(self, value):
        if isinstance(value, str):
            value = Keyword(value)
        return (self.value[value.value])

    def __getitem__(self, value): return self.value[value]

    def __setitem__(self, key, value): self.value[key] = value
    
    def evaluate(self, stack): 
        if ['_arg'] in self.value.values() or not self['self']:
            return self
        with stack(self):
            return self['self'][0].evaluate(stack)

    def update(self, other, stack, evaluate=True):
        for element in other.value['atoms']:
            self.drop(element, stack, evaluate)
        self.value.update({a:b for a,b in other.value.items() 
                           if a not in ('self', 'atoms')})

    def drop(self, element, stack, evaluate=True):
        for key in self.value:
            if self.value[key] != [Keyword('_arg')]:
                continue
            if evaluate and not (isinstance(key, TypeDef) and key.ttype[-1] == 'obj'):
                element = element.evaluate(stack)
            self[key] = [element]
            return

    def getitem(self, value, stack):
        for element in reversed(self[value]):
            return element.evaluate(stack)
        raise TypeError("Couldn't get '%s' in any way." % value)

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
