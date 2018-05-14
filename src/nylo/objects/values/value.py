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
from nylo.objects.nyobject import NyObject


class Value(NyObject):

    obj_types = {
        int: ('obj', 'value', 'num', 'int'),
        float: ('obj', 'value', 'num', 'float'),
        str: ('obj', 'value', 'num', 'str'),
    }

    # def settype(self, types, stack):
    #    self.types = self.obj_types[type(self.value)]
    #    return self.types


class GetObj(NyObject):

    def __init__(self, value, index):
        self.value, self.index = value, index

    def evaluate(self, stack):
        from nylo.objects.struct.struct import Struct
        i = self.index.evaluate(stack).value
        l = self.value.evaluate(stack)['atoms']
        o = l[i]
        if isinstance(o, list):
            return Struct(defaultdict(list, {'atoms': o}))
        else: return o.evaluate(stack)
