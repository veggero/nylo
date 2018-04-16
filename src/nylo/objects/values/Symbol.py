import operator

from nylo.objects.NyObject import NyObject
from nylo.objects.values.Value import Value
from functools import reduce


class Symbol(NyObject):

    map_to_py = {
        '+': operator.add, '-': operator.sub,
        '=': operator.eq, 'and ': operator.and_,
        '>': operator.gt, '<': operator.lt,
        '!=': operator.ne, 'xor ': operator.xor,
        '>=': operator.ge, '<=': operator.le,
        '*': operator.mul, '/': operator.truediv,
        '^': operator.pow, '%': operator.mod,
        '&': operator.add
    }

    def __init__(self, value, args):
        self.value, self.args = value, args
        self.names = self.args[0].names.union(self.args[1].names)

    def __repr__(self): return str(self)

    def __str__(
        self): return (' %s ' %
                       self.value).join(str(k) for k in self.args)

    def evaluate(self, stack):
        args = [k.evaluate(stack) for k in self.args]
        op = self.map_to_py[self.value]
        tor = Value(op(args[0].value, args[1].value))
        tor.types = self.types
        return tor

    def settype(self, types, stack):
        self.types = self.args[0].settype(types, stack)
        self.args[1].settype(types, stack)
        return self.types
