from nylo.objects.nyobject import NyObject


class TypeDef(NyObject):

    def __init__(self, kws):
        *self.ttype, self.value = kws
        self.value = self.value.value

    def __str__(self): return ' '.join(str(k)
                                       for k in self.ttype + [self.value])

    def __eq__(self, other): return other == self.value

    def __hash__(self): return hash(self.value)
