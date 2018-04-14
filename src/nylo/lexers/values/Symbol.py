from nylo.lexers.Lexer import Lexer
from nylo.objects.values.Symbol import Symbol as SymObj
from nylo.objects.values.Value import Value as ValObj
from nylo.objects.struct.Struct import Struct
from nylo.objects.struct.Call import Call


class Symbol(Lexer):
    
    unary_symbols = '+', '-', 'not '
    symbols = ('=', 'and ', '>', 'or ', '<', '!=', 'xor ', '>=',
               '<=', '..', 'in ', '*', '+-', '/', '^', '|', '%',
               '&') + unary_symbols
    to_avoid = ('->',)
    symbols_priority = (
        ('|',),
        ('and', 'or'),
        ('=', '!=', '>=', '<=', 'in'),
        ('..', '%'),
        ('+', '-', '&'),
        ('*', '/'),
        ('^', '+-'),
        )
    
    def able(reader): 
        from nylo.lexers.values.Value import Value
        reader = reader.test()
        if reader.any_starts_with(Symbol.unary_symbols):
            reader.move(len(reader.any_starts_with(Symbol.unary_symbols)))
            return Value.able(reader)
        if not Value.able(reader): return False
        Value.lexe(None, reader)
        return True
        
    def lexe(self, reader):
        from nylo.lexers.values.Value import Value
        if not reader.any_starts_with(self.unary_symbols):
            yield Value(reader).value
        if (not reader.any_starts_with(self.symbols)
            or reader.any_starts_with(self.to_avoid)): return
        self.symbol = reader.any_starts_with(self.symbols)
        reader.move(len(self.symbol))
        yield Symbol(reader).value
        yield self.symbol
	    

    def parse(self, reader): 
        *values, symbol = list(self.lexe(reader))
        if len(values) == 0: return symbol
        newobj = SymObj(symbol, values)
        if isinstance(values[1], SymObj):
            if self.priority(symbol) > self.priority(values[1].value):
                otherobj = newobj.args[1]
                otherobj.args[0], newobj.args[1] = newobj, otherobj.args[0]
                newobj = otherobj
        return newobj
    
    def priority(self, symbol):
        for index, value in enumerate(self.symbols_priority):
            if symbol in value: return index
