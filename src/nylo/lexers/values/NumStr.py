import string

from nylo.lexers.Lexer import Lexer
from nylo.objects.values.Value import Value as ValueObj


class Number(Lexer):
    
    def able(reader): return reader.read() in string.digits + '_'
        
    def lexe(self, reader):
        while reader.read() in string.digits + '_': yield reader.move()
        if reader.read() == '.':
            yield reader.move()
            while reader.read() in string.digits + '_': yield reader.move()
        
    def parse(self, reader):
        lexed = ''.join(self.lexe(reader))
        if '.' in lexed: return ValueObj(float(lexed))
        else: return ValueObj(int(lexed))
    
    
class String(Lexer):
        
        def able(reader): return reader.read() in '\'"'

        def lexe(self, reader):
            start = reader.move()
            while reader.read() != start: yield reader.move()
            reader.move()

        def parse(self, reader):
            return ValueObj(''.join(self.lexe(reader)))
