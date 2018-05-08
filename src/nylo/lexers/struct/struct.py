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

from nylo.lexers.lexer import Lexer
from nylo.objects.struct.structel import TypeDef
from nylo.objects.struct.struct import Struct as StructObj


class Struct(Lexer):

    def able(reader):
        """It checks if the token is
        readable.

        Returns:
            bool: True if the token is readable, False if not.
        """
        return reader.read() in '('

    def parse(self, reader):
        """It returns all lexer characters using
        an object.

        Args:
            reader (Reader): The reader you're going to use

        Returns:
            ValueObj: The lexer characters object
        """
        from nylo.lexers.values.symbol import Symbol
        atoms = defaultdict(list)
        reader.move()
        reader.avoid_whitespace()
        while not reader.any_starts_with([')', '->']):
            if reader.read() in ',':
                reader.move()
                reader.avoid_whitespace()
                continue
            value = Symbol(reader).value
            if reader.read() in ':':
                reader.move()
                key, value = value, Symbol(reader).value
                atoms[key].append(value)
            elif isinstance(value, TypeDef):
                atoms[value] = []
            else:
                atoms['atoms'].append(value)
        if reader.starts_with('->'):
            reader.move(2)
            atoms['self'].append(Symbol(reader).value)
        reader.avoid_whitespace()
        reader.move()
        if (len(atoms) == 1 and 'atoms' in atoms and
                len(atoms['atoms']) == 1):
            return atoms['atoms'][0]
        return StructObj(atoms)
