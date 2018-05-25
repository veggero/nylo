from nylo.objects.struct.struct import Struct


class Stack(list):

    def __init__(self, elements=[Struct()], wrapped=None):
        self.wrapped = wrapped
        list.__init__(self, elements)

    def wrap(self, element):
        return Stack(self[:], element)

    def evaluate(self, stack):
        return self.wrapped.evaluate(self)

    def __getitem__(self, value):
        if isinstance(value, (int, slice)):
            return list.__getitem__(self, value)
        return self[-1].getitem(value, self)

    def __contains__(self, value):
        return value in self[-1]

    def __enter__(*args): pass

    def __exit__(self, *args): self.pop()

    def __call__(self, value):
        newvalue = Struct(self[-1].value.copy())
        newvalue.value.update(value.value)
        self.append(newvalue)
        return self

    def __str__(self):
        return "{%s}" % '; '.join(map(str, self))
