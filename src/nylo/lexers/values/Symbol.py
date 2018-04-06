from nylo.lexers.Lexer import Lexer
from nylo.objects.values.Keyword import Keyword as KeyObj
from nylo.objects.values.Value import Value as ValObj
from nylo.objects.struct.Struct import Call, Struct


class Symbol(Lexer):
    
    unary_symbols = '+', '-', 'not '
    symbols = ('=', 'and ', '>', 'or ', '<', '!=', 'xor ', '>=',
               '<=', '..', 'in ', '*', '+-', '/', '^', '|', '%',
               '&') + unary_symbols
    to_avoid = ('->',)
    
    
    map_to_function_name = {
        '+': 'sum',
        '-': 'sub',
        '=': 'equal',
        'and ': 'all',
        '>': 'greater',
        '<': 'less_than',
        '!=': 'inequal',
        'xor ': 'single',
        '>=': 'greater_or_equal',
        '<=': 'less_than_or_equal',
        '*': 'mul',
        '/': 'div',
        '^': 'pow',
        '%': 'mod',
        '&': 'sum'
    }
    
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
        else: 
            return Call(KeyObj(self.map_to_function_name[symbol]), 
                        Struct(values + [False]))
