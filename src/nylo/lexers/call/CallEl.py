from nylo.lexers.Lexer import Lexer
from nylo.objects.call.CallEl import Set
from nylo.lexers.values.Keyword import Keyword

class CallEl(Lexer):
    
    def able(reader): return True #TODO
    
    def lexe(self, reader):
        from nylo.lexers.values.Value import Value
        vl = Value(reader).value
        if reader.read() == ':':
            reader.move()
            yield Set(vl, Value(reader).value)
        else: yield vl
        
    def parse(self, reader): return list(self.lexe(reader))[0]
