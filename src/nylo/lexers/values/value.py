"""
Contains the Value class definition.
"""

from nylo.lexers.lexer import Lexer
from nylo.lexers.values.keyword import Keyword
from nylo.lexers.values.numstr import Number, String
from nylo.lexers.values.symbol import Symbol
from nylo.lexers.struct.struct import Struct
from nylo.objects.struct.call import Call as CallObj
from nylo.objects.values.value import GetObj
from nylo.objects.struct.structel import TypeDef
from nylo.objects.values.keyword import Keyword as KeyObj
from nylo.objects.values.value import Value as ValueObj


class Value(Lexer):
    """
    Value manages parsing for any type of value.
    """

    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.

        Returns:
            bool: True if the token is readable, False if not.
        """
        return (Number.able(reader) or String.able(reader)
                or Keyword.able(reader) or Struct.able(reader))

    def lexe(self, reader):
        """It generates all characters
        associated to the token.

        Args:
            reader (Reader): The reader you're going to use.

        Returns:
            generator: All characters associated to the token.
        """
        value = KeyObj('_implicit')
        if Keyword.able(reader):
            found_keyword = Keyword(reader).value
            if Keyword.able(reader):
                kws = [found_keyword]
                while Keyword.able(reader):
                    kws.append(Keyword(reader).value)
                value = TypeDef(kws)
            else:
                value = found_keyword
        elif Number.able(reader):
            value = Number(reader).value
        elif String.able(reader):
            value = String(reader).value
        elif Struct.able(reader):
            value = Struct(reader).value
        reader.avoid_whitespace()
        if reader.read() in '(':
            return CallObj(value, Struct(reader).value)
        elif reader.read() in '[':
            return GetObj(value, Get(reader).value)
        return value

    def parse(self, reader):
        """It returns all lexer characters using
        an object.

        Args:
            reader (Reader): The reader you're going to use

        Returns:
            ValueObj: The lexer characters object
        """
        return self.lexe(reader)


class Get(Lexer):
    """Get is used to return
    an element from a list or a similar
    object - it returns an element associated to
    an index"""

    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.

        Returns:
            bool: True if the token is readable, False if not.
        """
        return reader.read() == '['

    def lexe(self, reader):
        """It generates all characters
        associated to the token.

        Args:
            reader (Reader): The reader you're going to use.

        Returns:
            generator: All characters associated to the token.
        """
        reader.move()
        yield Symbol(reader).value
        while reader.read() == ':':
            reader.move()
            yield Symbol(reader).value
        reader.move()

    def parse(self, reader):
        """It returns all lexer characters using
        an object.

        Args:
            reader (Reader): The reader you're going to use

        Returns:
            ValueObj: The lexer characters object
        """
        out = list(self.lexe(reader))
        if len(out) == 1:
            return out[0]
        return ValueObj(slice(*[o.value for o in out]))
