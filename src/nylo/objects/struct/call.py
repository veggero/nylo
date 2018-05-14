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

from collections import defaultdict
from nylo.objects.struct.struct import Struct
from nylo.objects.nyobject import NyObject
from nylo.objects.values.keyword import Keyword
from nylo.objects.values.symbol import Symbol


class Call(NyObject):

    def __init__(self, kw, struct):
        if not isinstance(struct, Struct):
            struct = Struct(defaultdict(list, {'atoms': [struct]}))
        self.kw, self.struct, self.value = kw, struct, (kw, struct)
        self.names = self.kw.names.union(self.struct.names)

    def __str__(self): return '%s%s' % (self.kw, self.struct)

    def evaluate(self, stack):
        self.tobdcalled = self.kw.evaluate(stack)
        self.called = Struct(self.tobdcalled.value.copy())
        # self.called.types = self.tobdcalled.types
        self.called.update(self.struct, stack)
        if self.struct['self']:
            with stack(self.called):
                return self.struct['self'][0].evaluate(stack)
        return self.called.evaluate(stack)

    # def settype(self, types, stack):
    #    self.called = stack[self.kw]
    #    self.called = Struct(self.called.value.copy())
    #    if 'self' in self.struct.value:
    #        self.called.value['self'] = self.struct.value['self']
    #    self.called.update(self.struct, stack, evaluate=False)
    #    with stack(self.called):
    #        self.struct.settype(types, stack)
    #        self.types = self.called.value['self'][0].settype(types, stack)
    #    return self.types
