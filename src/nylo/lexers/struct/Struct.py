from nylo.lexers.Lexer import Lexer
from nylo.lexers.struct.StructEl import StructEl
from nylo.objects.struct.StructEl import Set, TypeDef
from nylo.objects.struct.Struct import Struct as StructObj

class Struct(Lexer):
    
    def able(reader): return reader.read() in '('
    
    def lexe(self, reader):
        from nylo.lexers.values.Symbol import Symbol
        reader.move()
        reader.avoid_whitespace()
        while not reader.any_starts_with([')', '->']):
            yield StructEl(reader).value
            if reader.read() == ',': 
                reader.move()
                reader.avoid_whitespace()
        if reader.starts_with('->'): 
            reader.move(2)
            yield Symbol(reader).value
        else: yield False
        reader.avoid_whitespace()
        reader.move()
        
    def parse(self, reader):
        elements = list(self.lexe(reader))
        if (len(elements) == 2 and not isinstance(elements[0], Set)
            and not elements[-1] and not isinstance(elements[0], TypeDef)):
            return elements[0]
        else: return StructObj(elements)
