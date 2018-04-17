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
from nylo.objects.struct.structel import TypeDef


class Value(Lexer):

    def able(reader):
        return (Number.able(reader) or String.able(reader)
                or Keyword.able(reader) or Struct.able(reader))
                # String.able(reader) or Symbol.able(reader))

    def lexe(self, reader):
        if Keyword.able(reader):
            kw = Keyword(reader).value
            if reader.read() in '(':
                return CallObj(kw, Struct(reader).value)
            elif Keyword.able(reader):
                kws = [kw]
                while Keyword.able(reader):
                    kws.append(Keyword(reader).value)
                return TypeDef(kws)
            else:
                return kw
        elif Number.able(reader):
            return Number(reader).value
        elif String.able(reader):
            return String(reader).value
        elif Struct.able(reader):
            return Struct(reader).value

    def parse(self, reader): return self.lexe(reader)
