"""
Contains the Keyword class definition.
"""

import string
from nylo.lexers.lexer import Lexer


class Keyword(Lexer):
    """Keyword is used to store variables
    and it returns their values when it's evaluated."""

    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.
        """
        return reader.read() in string.ascii_letters + '_'

    def lexe(self, reader):
        """It generates all characters
        associated to the token.
        """
        while reader.read() in string.ascii_letters + '_':
            yield reader.move()

    def parse(self, reader):
        """It returns all lexer characters using
        an object.
        """
        return ''.join(self.lexe(reader))

    def transpile(self, mesh, path):
        for i in reversed(range(len(path)+1)):
            if path[:i]+(self.value,) in mesh:
                return path[:i]+(self.value,)
        raise NameError(f"Couldn't find variable {self.value}")
