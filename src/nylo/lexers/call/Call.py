from nylo.lexers.Lexer import Lexer
from nylo.lexers.call.CallEl import CallEl

class Call(Lexer):
    
    starts = ['(']
    
    def able(reader): return reader.read() == '(' #TODO
    
    def lexe(self, reader):
        from nylo.lexers.values.Value import Value
        reader.move()
        while not reader.any_starts_with([')', '->']):
            yield CallEl(reader).value
            if reader.read() == ',': reader.move() 
        if reader.starts_with('->'): 
            reader.move(2)
            yield Value(reader).value
        else: yield False
        reader.move()
        
    def parse(self, reader):
        return list(self.lexe(reader))
