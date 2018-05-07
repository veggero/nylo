# This file is a part of nylo
#
# Copyright (c) 2018 The nylo Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import operator
from collections import defaultdict

from nylo.objects.nyobject import NyObject
from nylo.objects.values.value import Value


def nyrange(*args):
    from nylo.objects.struct.struct import Struct
    return Struct(defaultdict(
        list, {'atoms': list(map(lambda x: Value(x), range(*args)))}))


def nyin(value, nylist):
    return value in nylist['atoms']


class Symbol(NyObject):

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
        self.names = self.args[0].names.union(self.args[1].names)

    def __repr__(self): return str(self)

    def __str__(
        self): return (' %s ' %
                       self.value).join(str(k) for k in self.args)

    def evaluate(self, stack):
        args = [k.evaluate(stack) for k in self.args]
        op = self.map_to_py[self.value]
        tor = op(args[0].value, args[1].value)
        if not isinstance(tor, NyObject):
            tor = Value(tor)
        # tor.types = self.types
        return tor

    # def settype(self, types, stack):
    #    self.types = self.args[0].settype(types, stack)
    #    self.args[1].settype(types, stack)
    #    return self.types
