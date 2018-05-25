from collections import defaultdict
from nylo.objects.nyobject import NyObject


class Struct(NyObject):
    """Struct is the main
    type that you could find using
    Nylo. It could be a function, a dictionary: all
    objects that you can find between parenthesis or an
    indented object."""
    
    def __init__(self, value=defaultdict(list)):
        super().__init__(value)

    def __str__(self):
        return '(%s)' % ', '.join(': '.join(map(str, (a, '|'.join(map(str, b)))))
                                  for a, b in self.value.items())

    def __contains__(self, value):
        return self.value[value.value]

    def evaluate(self, stack):
        if ['_arg'] in self.value.values() or not self.value['self']:
            return self
        with stack(self):
            return self.getitem('self', stack)

    def update(self, other, stack):
        for element, key in zip(other.value['atoms'], self.value['_args']):
            self.value[key] = [stack.wrap(element)]
            self.value['_args'] = self.value['_args'][1:]
        self.value.update({a: [*map(stack.wrap, b)] for a, b in other.value.items()
                           if a not in ('self', 'atoms', '_args')})

    def getitem(self, value, stack):
        if not self.value[value]:
            raise ValueError("Value %s is not in %s" % (value, self))
        self.value[value] = self.value[value] + [self.value[value][-1].evaluate(stack)]
        return self.value[value][-1]
