from copy import copy

class Reader:

    """
    Reader is a class that implements reading code;
    it counts the number of line and character it's reading,
    checks for unexpected EOFs, and so on.
    """

    def __init__(self, code, reading_at=0):
        "Initizialize Reader instance."
        prev_indent, endlines = 0, []
        for line in (code+'\n\0').split('\n'):
            indent = 0
            while len(line)>indent and line[indent] in ' \t': indent += 1
            if len(line) == indent: continue
            line = line[indent:]
            if indent > prev_indent: line = '('*(indent-prev_indent)+line
            elif indent < prev_indent: line = ')'*(prev_indent-indent)+line
            prev_indent = indent
            endlines.append(line)
        self.code = '\n'.join(endlines)
        self.reading_at = reading_at
        self.line, self.char = 1, 1

    def read(self):
        "Read the current character."
        return self.code[self.reading_at]

    def move(self, char_num=1):
        "Move the pointer on the next characters."
        for i in range(char_num): last = self.move_char()
        while self.read() in ' \t\n': self.move_char()
        return last

    def move_char(self):
        "Move the pointer on the next characters."
        if self.read() == '\n':
            self.line += 1
            self.char = 1
        else: self.char += 1
        self.reading_at += 1
        if self.reading_at >= len(self.code): eof_on_scan()
        return self.code[self.reading_at-1]

    def any_starts_with(self, starts):
        """
        Check if the code starts with any of the starts,
        and if so returns it.
        """
        for start in starts:
            if self.starts_with(start): return start
        return False

    def starts_with(self, string):
        """
        Check if the code it's reading starts with given string.
        """
        return self.code.startswith(string, self.reading_at)

    def get_line(self):
        return self.line

    def get_char(self):
        return self.char

    def goto(self, reader):
        "Go to the character of another reader."
        self.reading_at = reader.reading_at
        self.line = reader.line
        self.char = reader.char

    def end(self):
        "Raise error if file is not over."
        if self.reading_at < len(self.code) - 1:
            file_not_over()
            
    def avoid_whitespace(self):
        while self.read() in '\n \t': self.move()
        
    def test(self): return copy(self)
