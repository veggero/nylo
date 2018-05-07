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

from nylo.lexers.lexer import Lexer
from nylo.lexers.values.keyword import Keyword
from nylo.lexers.values.numstr import Number, String
from nylo.lexers.values.symbol import Symbol
from nylo.lexers.struct.struct import Struct
from nylo.objects.struct.call import Call as CallObj
from nylo.objects.values.value import GetObj
from nylo.objects.struct.structel import TypeDef
from nylo.objects.values.keyword import Keyword as KeyObj
from nylo.objects.values.value import Value as ValueObj


class Value(Lexer):
    """Value class is similar to PyValue, but it calls a
    Python object, not a function. It could be used to create an
    interface between a Nylo and a Python object."""

    def able(reader):
        return (Number.able(reader) or String.able(reader)
                or Keyword.able(reader) or Struct.able(reader))

    def lexe(self, reader):
        v = KeyObj('_implicit')
        if Keyword.able(reader):
            kw = Keyword(reader).value
            if Keyword.able(reader):
                kws = [kw]
                while Keyword.able(reader):
                    kws.append(Keyword(reader).value)
                v = TypeDef(kws)
            else:
                v = kw
        elif Number.able(reader):
            v = Number(reader).value
        elif String.able(reader):
            v = String(reader).value
        elif Struct.able(reader):
            v = Struct(reader).value
        reader.avoid_whitespace()
        if reader.read() in '(':
            return CallObj(v, Struct(reader).value)
        elif reader.read() in '[':
            return GetObj(v, Get(reader).value)
        else:
            return v

    def parse(self, reader): return self.lexe(reader)


class Get(Lexer):
    """Get is used to return
    an element from a list or a similar
    object - it returns an element associated to
    an index"""

    def able(reader):
        return '[' == reader.read()

    def lexe(self, reader):
        reader.move()
        yield Symbol(reader).value
        while reader.read() == ':':
            reader.move()
            yield Symbol(reader).value
        reader.move()

    def parse(self, reader):
        out = list(self.lexe(reader))
        if len(out) == 1:
            return out[0]
        else:
            return ValueObj(slice(*[o.value for o in out]))
