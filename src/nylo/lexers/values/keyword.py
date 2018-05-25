import string
from nylo.lexers.lexer import Lexer
from nylo.objects.values.keyword import Keyword as KwObj


class Keyword(Lexer):
    """Keyword is used to store variables
    and it returns their values when it's evaluated."""

    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.

        Returns:
            bool: True if the token is readable, False if not.
        """
        return reader.read() in string.ascii_letters + '_'

    def lexe(self, reader):
        """It generates all characters
        associated to the token.

        Args:
            reader (Reader): The reader you're going to use.

        Returns:
            generator: All characters associated to the token.
        """
        while reader.read() in string.ascii_letters + '_':
            yield reader.move()

    def parse(self, reader):
        """It returns all lexer characters using
        an object.

        Args:
            reader (Reader): The reader you're going to use

        Returns:
            ValueObj: The lexer characters object
        """
        return KwObj(''.join(self.lexe(reader)))
