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

import string

from nylo.lexers.lexer import Lexer
from nylo.objects.values.value import Value as ValueObj


class Number(Lexer):

    def able(reader): return reader.read() in string.digits + '_'

    def lexe(self, reader):
        while reader.read() in string.digits + '_':
            yield reader.move()
        if reader.read() == '.':
            if reader.code[reader.reading_at + 1] in string.digits:
                yield reader.move()
                while reader.read() in string.digits + '_':
                    yield reader.move()

    def parse(self, reader):
        lexed = ''.join(self.lexe(reader))
        if '.' in lexed:
            return ValueObj(float(lexed))
        else:
            return ValueObj(int(lexed))


class String(Lexer):

        def able(reader): return reader.read() in '\'"'

        def lexe(self, reader):
            start = reader.move()
            while reader.read() != start:
                yield reader.move()
            reader.move()

        def parse(self, reader):
            return ValueObj(''.join(self.lexe(reader)))
