from collections import defaultdict
from nylo.lexers.lexer import Lexer
from nylo.objects.struct.structel import TypeDef
from nylo.objects.struct.struct import Struct as StructObj
from nylo.objects.values.keyword import Keyword as KwObj


class Struct(Lexer):

    def able(reader):
    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.

        Returns:
            bool: True if the token is readable, False if not.
        """
        return reader.read() in '('

    def parse(self, reader):
        """It returns all lexer characters using
        an object.

        Args:
            reader (Reader): The reader you're going to use

        Returns:
            ValueObj: The lexer characters object
        """
        from nylo.lexers.values.symbol import Symbol
        atoms = defaultdict(list)
        reader.move()
        reader.avoid_whitespace()
        while not reader.any_starts_with([')', '->']):
            if reader.read() in ',':
                reader.move()
                reader.avoid_whitespace()
                continue
            value = Symbol(reader).value
            if reader.read() in ':':
                reader.move()
                key, value = value, Symbol(reader).value
                atoms[key].append(value)
            elif isinstance(value, TypeDef):
                atoms['_args'].append(value)
                atoms[value].append(KwObj('_arg'))
            else:
                atoms['atoms'].append(value)
        if reader.starts_with('->'):
            reader.move(2)
            atoms['self'].append(Symbol(reader).value)
        reader.avoid_whitespace()
        reader.move()
        if (len(atoms) == 1 and 'atoms' in atoms and
                len(atoms['atoms']) == 1):
            return atoms['atoms'][0]
        return StructObj(atoms)
