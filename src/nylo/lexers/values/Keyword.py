import string

from nylo.lexers.Lexer import Lexer
from nylo.objects.values.Keyword import Keyword as KwObj


class Keyword(Lexer):
    
    def able(reader): return reader.read() in string.ascii_letters + '_'
    
    def lexe(self, reader):
        while reader.read() in string.ascii_letters + '_': yield reader.move()
        
    def parse(self, reader): 
        return KwObj(''.join(self.lexe(reader)))
