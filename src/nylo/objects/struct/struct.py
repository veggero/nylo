from nylo.objects.nyobject import NyObject
from nylo.objects.struct.structel import TypeDef
from nylo.objects.values.keyword import Keyword
from collections import defaultdict


class Struct(NyObject):

    def __init__(self, value=defaultdict(list)):
        self.value = value
        self.names = set()

    def __str__(self): return '(%s)' % ', '.join('%s: ...' % (key)
                                                 for key, val in self.value.items())

    def __contains__(self, value): return len(self.value[value.value]) > 0

    def __getitem__(self, value): return self.value[value]

    def evaluate(self, stack): return self

    def calculate(self, stack):
        with stack(self):
            if 'self' in self.value:
                return self.value['self'][0].evaluate(stack)
            else:
                return self

    def update(self, other, stack, evaluate=True):
        for key, value in other.value.items():
            if key == 'atoms':
                continue
            self.value[key] = self[key] + value
        for element in other.value['atoms']:
            self.drop(element, stack, evaluate)

    def drop(self, element, stack, evaluate=True):
        for key, value in self.value.items():
            if value == []:
                if evaluate and not (isinstance(key, TypeDef) and key.ttype[-1] == 'obj'):
                    element = element.evaluate(stack)
                self.value[key] = self.value[key] + [element]
                return

    def getitem(self, value, stack):
        for element in reversed(self[value]):
            return element.evaluate(stack)
        raise TypeError("Couldn't get '%s' in any way." % value)

    def settype(self, types, stack):
        self.types = types
        with stack(self):
            for key, value in self.value.items():
                for element in value:
                    element.settype(types + [key], stack)
        return self.types

    def typesof(self, element, stack):
        for key in self.value:
            if key == element:
                if isinstance(key, Keyword):
                    return ['obj']
                elif isinstance(key, TypeDef):
                    return key.ttype
        print(self)
        raise TypeError("Couldn't get '%s' in any way." % element)
