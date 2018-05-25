import operator
from collections import defaultdict
from nylo.objects.nyobject import NyObject
from nylo.objects.values.value import Value


class Symbol(NyObject):

    def nyrange(*args):
        from nylo.objects.struct.struct import Struct
        return Struct(defaultdict(list, {'atoms':
                                         list(map(lambda x: Value(x), range(*args)))}))

    def nyin(value, nylist):
        return value in nylist['atoms']

    map_to_py = {
        '+': operator.add, '-': operator.sub,
        '=': operator.eq, 'and ': operator.and_,
        '>': operator.gt, '<': operator.lt,
        '!=': operator.ne, 'xor ': operator.xor,
        '>=': operator.ge, '<=': operator.le,
        '*': operator.mul, '/': operator.truediv,
        '^': operator.pow, '%': operator.mod,
        '&': operator.add, '..': nyrange,
        'in ': nyin,
    }

    def __init__(self, value, args):
        self.value, self.args = value, args

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (' %s ' % self.value).join(str(k) for k in self.args)

    def evaluate(self, stack):
        args = [k.evaluate(stack).value for k in self.args]
        tor = self.map_to_py[self.value](*args)
        if not isinstance(tor, NyObject):
            tor = Value(tor)
        return tor
