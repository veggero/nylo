"""
Contains Number and String classes definitions.
"""

import string
from nylo.lexers.lexer import Lexer
from nylo.objects.values.value import Value as ValueObj


class Number(Lexer):
    """
    Manage parsing for numbers.
    """

    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.

        Returns:
            bool: True if the token is readable, False if not.
        """
        return reader.read() in string.digits + '_'

    def lexe(self, reader):
        """It generates all characters
        associated to the token.

        Args:
            reader (Reader): The reader you're going to use.

        Returns:
            generator: All characters associated to the token.
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

        Args:
            reader (Reader): The reader you're going to use

        Returns:
            ValueObj: The lexer characters object
        """
        lexed = ''.join(self.lexe(reader))
        if '.' in lexed:
            return ValueObj(float(lexed))
        return ValueObj(int(lexed))


class String(Lexer):
    """Manage parsing for strings.
    """

    start_to_ends = {'"': '"', "'": "'", '«': '»'}

    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.

        Returns:
            bool: True if the token is readable, False if not.
        """
        return reader.read() in String.start_to_ends

    def lexe(self, reader):
        """It generates all characters
        associated to the token.

        Args:
            reader (Reader): The reader you're going to use.

        Returns:
            generator: All characters associated to the token.
        """
        start = reader.move()
        while reader.read() != self.start_to_ends[start]:
            yield reader.move()
        reader.move()

    def parse(self, reader):
        return ValueObj(''.join(self.lexe(reader)))
