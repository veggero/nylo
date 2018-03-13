import string

from nylo.lexers.Lexer import Lexer
from nylo.objects.values.NumStr import Number as NumObj, String as StrObj

class Number(Lexer):
        
        
    def lexe(reader):
        while reader.read() in string.digits + '_': yield reader.move()
        if reader.read() == '.':
            yield reader.move()
            while reader.read() in string.digits + '_': yield reader.move()
            
            
        
    def parse(reader):
        lexed = ''.join(self.lexe(reader))
        if '.' in lexed: return NumObj(float(lexed))
        else: return NumObj(int(lexed))
    
    
class String(Lexer):


        def lexe(reader):
            start = reader.move()
            while reader.read() != start: yield reader.move()
            reader.move()
            

        def parse(reader):
            return StrObj(''.join(self.lexe(reader)))
