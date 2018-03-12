from nylo.exceptions import eof_on_scan, file_not_over


class Reading:

    """
    Reading is a class that implements reading code;
    it counts the number of line and character it's reading,
    checks for unexpected EOFs, and so on.
    """

    def __init__(self, code, reading_at):
        "Initizialize Reading instance."
        # Add end of file
        self.code = code + '\0'
        self.reading_at = reading_at
        self.line, self.char = 1, 1

    def read(self):
        "Read the current character."
        return self.code[self.reading_at]

    def move(self, char_num=1):
        "Move the pointer on the next characters."
        for i in range(char_num):
            self.move_char()

    def move_char(self):
        "Move the pointer on the next characters."
        if self.read() == '\n':
            self.line += 1
            self.char = 1
        else:
            self.char += 1
        self.reading_at += 1
        if self.reading_at >= len(self.code):
            eof_on_scan()

    def read_and_move(self):
        "Read and character and skip to the next one."
        value = self.read()
        self.move_char()
        return value

    def any_starts_with(self, starts):
        """
        Check if the code starts with any of the starts,
        and if so returns it.
        """
        for start in starts:
            if self.starts_with(start):
                return start
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
