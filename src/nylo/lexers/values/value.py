"""
Contains the Value class definition.
"""

from collections import defaultdict
from nylo.lexers.lexer import Lexer
from nylo.lexers.values.keyword import Keyword
from nylo.lexers.values.numstr import Number, String
from nylo.lexers.values.symbol import Symbol
from nylo.lexers.struct.struct import Struct

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
        value = '_implicit'
        if Keyword.able(reader):
            found_keyword = Keyword(reader)
            if Keyword.able(reader):
                kws = [found_keyword]
                while Keyword.able(reader):
                    kws.append(Keyword(reader))
                value = kws
            else:
                value = found_keyword
        elif Number.able(reader):
            value = Number(reader)
        elif String.able(reader):
            value = String(reader)
        elif Struct.able(reader):
            value = Struct(reader)
        reader.avoid_whitespace()
        if reader.read() in '(':
            return (value, Struct(reader))
        elif reader.read() in '[':
            return (value, Get(reader))
        return value

    def parse(self, reader):
        """It returns all lexer characters using
        an object.

        Args:
            reader (Reader): The reader you're going to use
        """
        return self.lexe(reader)
    
    def transpile(self, mesh, path):
        if isinstance(self.value, list):
            return self.value[-1].transpile(mesh, path)
        if isinstance(self.value, tuple):
            called, caller = self.value
            if isinstance(called, Keyword):
                called = called.transpile(mesh, path)
            else:
                called, newcalled = path+('temp',), called
                mesh[called] = newcalled.transpile(mesh, called)
            if not isinstance(caller.value, defaultdict):
                caller.value = defaultdict(list, {'atoms': [caller.value]})
            caller.transpile_call(mesh, path, called)
            mesh['classes'][path] = called
            print(caller.value, 'self' in caller.value)
            if 'self' in caller.value:
                return caller.value['self'][0].transpile(mesh, called)
            return path+('self',)
        else:
            return self.value.transpile(mesh, path)


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
        """
        reader.move()
        yield Symbol(reader)
        while reader.read() == ':':
            reader.move()
            yield Symbol(reader)
        reader.move()

    def parse(self, reader):
        """It returns all lexer characters using
        an object.

        Args:
            reader (Reader): The reader you're going to use
        """
        out = list(self.lexe(reader))
        if len(out) == 1:
            return out[0]
        return slice(*[o for o in out])
