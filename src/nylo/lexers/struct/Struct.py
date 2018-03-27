from nylo.lexers.Lexer import Lexer
from nylo.lexers.struct.StructEl import StructEl
from nylo.objects.struct.StructEl import Set
from nylo.objects.struct.Struct import Struct as StructObj

class Struct(Lexer):
    
    def able(reader): return reader.read() in '('
    
    def lexe(self, reader):
        from nylo.lexers.values.Value import Value
        reader.move()
        while not reader.any_starts_with([')', '->']):
            yield StructEl(reader).value
            if reader.read() == ',': 
                reader.move()
                reader.avoid_whitespace()
        if reader.starts_with('->'): 
            reader.move(2)
            yield Value(reader).value
        else: yield False
        reader.move()
        
    def parse(self, reader):
        elements = list(self.lexe(reader))
        if len(elements) == 2 and not isinstance(elements[0], Set):
            return elements[0]
        else: return StructObj(elements)
