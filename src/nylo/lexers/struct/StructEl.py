from nylo.lexers.Lexer import Lexer
from nylo.objects.struct.StructEl import Set
from nylo.lexers.values.Keyword import Keyword

class StructEl(Lexer):
    
    def lexe(self, reader):
        from nylo.lexers.values.Symbol import Symbol
        vl = Symbol(reader).value
        if reader.read() == ':':
            reader.move()
            yield Set(vl, Symbol(reader).value)
        else: yield vl
        
    def parse(self, reader): return list(self.lexe(reader))[0]
