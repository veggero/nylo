from collections import defaultdict

from nylo.lexers.Lexer import Lexer
from nylo.objects.struct.StructEl import TypeDef
from nylo.objects.struct.Struct import Struct as StructObj


class Struct(Lexer):

    def able(reader): return reader.read() in '('

    def parse(self, reader):
        from nylo.lexers.values.Symbol import Symbol
        atoms = defaultdict(list)
        reader.move()
        reader.avoid_whitespace()
        while not reader.any_starts_with([')', '->']):
            value = Symbol(reader).value
            if reader.read() in ':':
                reader.move()
                key, value = value, Symbol(reader).value
                atoms[key].append(value)
            elif isinstance(value, TypeDef):
                atoms[value] = []
            else:
                atoms['atoms'].append(value)
            if reader.read() in ',':
                reader.move()
                reader.avoid_whitespace()
        if reader.starts_with('->'):
            reader.move(2)
            atoms['self'].append(Symbol(reader).value)
        reader.avoid_whitespace()
        reader.move()
        if len(atoms) == 1 and 'atoms' in atoms and len(atoms['atoms']) == 1:
            return atoms['atoms'][0]
        return StructObj(atoms)
