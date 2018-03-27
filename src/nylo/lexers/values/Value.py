from nylo.lexers.Lexer import Lexer
from nylo.lexers.values.Keyword import Keyword
from nylo.lexers.values.NumStr import Number, String
from nylo.lexers.values.Symbol import Symbol
from nylo.lexers.struct.Struct import Struct
from nylo.objects.struct.Struct import Call as CallObj


class Value(Lexer):
    
    def able(reader): 
        return (Number.able(reader) or String.able(reader) 
                or Keyword.able(reader) or Struct.able(reader))
                #String.able(reader) or Symbol.able(reader))
    
    def lexe(self, reader):
        if Keyword.able(reader): 
            kw = Keyword(reader).value
            if reader.read() in '(': 
                return CallObj(kw, Struct(reader).value)
            else: return kw
        elif Number.able(reader): return Number(reader).value
        elif String.able(reader): return String(reader).value
        elif Struct.able(reader): return Struct(reader).value
        
    def parse(self, reader): return self.lexe(reader)
