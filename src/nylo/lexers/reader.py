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


class Reader:

    def __init__(self, code, reading_at=0):
        self.code = list(f'({code}\n),\n\0')
        self.indent = 0
        self.reading_at = reading_at
        self.line, self.char = 1, 1

    def read(self):
        return self.code[self.reading_at]

    def move(self, todo=1):
        if self.read() == '\n':
            self.line += 1
            self.char = 1
        else:
            self.char += 1
        self.reading_at += 1
        if self.read() == '\0':
            raise SyntaxError('EOF while scanning.')
        if todo > 1:
            self.move(todo-1)
        return self.code[self.reading_at - 1]

    def any_starts_with(self, starts):
        for start in starts:
            if self.starts_with(start):
                return start
        return False

    def starts_with(self, string):
        return ''.join(self.code).startswith(string, self.reading_at)

    def avoid_whitespace(self):
        while self.read() in ' \t':
            self.move()
        if self.read() == '\n':
            i = self.reading_at + 1
            while self.code[i] in '\t ':
                i += 1
            if self.code[i] == '\n':
                self.reading_at = i
                return self.avoid_whitespace()
            newindent = i - (self.reading_at + 1)
            if newindent <= self.indent:
                self.code.insert(i, ',')
            for i in range(abs(self.indent - newindent)):
                if newindent > self.indent:
                    self.code.insert(i, '(')
                elif newindent < self.indent:
                    self.code.insert(i, ')')
            self.move()
            self.indent = newindent
