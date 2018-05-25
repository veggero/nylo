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
