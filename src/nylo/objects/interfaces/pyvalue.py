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

from nylo.objects.nyobject import NyObject
from nylo.objects.values.value import Value


class PyValue(NyObject):
    """
    This class is used to define a value
    and it's derived from NyObject.

    It could be used to store a value and
    evaluate it using a stack.
    """

    def __init__(self, value, types, names):
        self.typefun = types
        super().__init__(value)
        self.names = names


    def __str__(self) -> str:
        """
        It returns a string that
        could represent the object.

        :return: The representation
        :rtype: str
        """
        return '<lambda>'

    def evaluate(self, stack):
        output = self.value(stack)
        if not isinstance(output, NyObject):
            output = Value(output)
        return output

    # def settype(self, types, stack):
    #    self.types = self.typefun(stack)
    #    return self.types
