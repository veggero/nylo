from nylo.lexers.Lexer import Lexer
from nylo.lexers.values.Keyword import Keyword
from nylo.lexers.values.NumStr import Number, String
from nylo.lexers.values.Symbol import Symbol
from nylo.lexers.call.Call import Call
from nylo.objects.call.Call import Call as CallObj


class Value(Lexer):
    
    def able(reader): 
        return (Number.able(reader) or String.able(reader) 
                or Keyword.able(reader) or Call.able(reader))
                #String.able(reader) or Symbol.able(reader))
    
    def lexe(self, reader):
        if Keyword.able(reader): 
            kw = Keyword(reader).value
            if reader.read() in '(': 
                cl = Call(reader).value
                print(cl)
                return CallObj(kw, cl)
            else: return kw
        elif Number.able(reader): return Number(reader).value
        elif String.able(reader): return String(reader).value
        elif Call.able(reader): return Call(reader).value
        
    def parse(self, reader): return self.lexe(reader)
