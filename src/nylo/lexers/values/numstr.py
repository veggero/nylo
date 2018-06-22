"""
Contains Number and String classes definitions.
"""

import string
from nylo.lexers.lexer import Lexer


class Number(Lexer):
    """
    Manage parsing for numbers.
    """

    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.
        """
        return reader.read() in string.digits + '_'

    def lexe(self, reader):
        """It generates all characters
        associated to the token.
        """
        while reader.read() in string.digits + '_':
            yield reader.move()
        if reader.read() == '.':
            if reader.code[reader.reading_at + 1] in string.digits:
                yield reader.move()
                while reader.read() in string.digits + '_':
                    yield reader.move()

    def parse(self, reader):
        """It returns all lexer characters using
        an object.
        """
        lexed = ''.join(self.lexe(reader))
        if '.' in lexed:
            return float(lexed)
        return int(lexed)
    
    def transpile(self, mesh, path):
        return self.value


class String(Lexer):
    """Manage parsing for strings.
    """

    start_to_ends = {'"': '"', "'": "'", '«': '»'}

    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.
        """
        return reader.read() in String.start_to_ends

    def lexe(self, reader):
        """It generates all characters
        associated to the token.
        """
        start = reader.move()
        while reader.read() != self.start_to_ends[start]:
            yield reader.move()
        reader.move()

    def parse(self, reader):
        return ''.join(self.lexe(reader))
    
    def transpile(self, mesh, path):
        return self.value
