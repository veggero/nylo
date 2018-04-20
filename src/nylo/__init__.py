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

# noinspection PyUnresolvedReferences
from nylo.lexers.reader import Reader
# noinspection PyUnresolvedReferences
from nylo.lexers.values.value import Value
# noinspection PyUnresolvedReferences
from nylo.lexers.values.keyword import Keyword
# noinspection PyUnresolvedReferences
from nylo.lexers.values.symbol import Symbol
# noinspection PyUnresolvedReferences
from nylo.lexers.values.numstr import Number, String
# noinspection PyUnresolvedReferences
from nylo.lexers.struct.struct import Struct
# noinspection PyUnresolvedReferences
from nylo.objects.stack import Stack
# noinspection PyUnresolvedReferences
from nylo.objects.interfaces.builtins import builtins

# builtins.settype(['obj'], Stack())
nyglobals = Stack([builtins])

__author__ = 'veggero'
__team__ = 'pyTeens'
__license__ = 'GNU GENERAL PUBLIC LICENSE'
__url__ = 'https://github.com/pyTeens/nylo'
__version__ = '0.1.0'
