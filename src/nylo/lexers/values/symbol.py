from collections import defaultdict
from nylo.lexers.lexer import Lexer
from nylo.objects.values.symbol import Symbol as SymObj
from nylo.objects.struct.struct import Struct
from nylo.objects.values.keyword import Keyword


class Symbol(Lexer):

    unary_symbols = '+', '-', 'not '
    symbols = ('=', 'and ', '>', 'or ', '<', '!=', 'xor ', '>=',
               '<=', '..', 'in ', '*', '+-', '/', '^', '|', '%',
               '&', '.') + unary_symbols
    to_avoid = ('->',)
    symbols_priority = (
        ('|',),
        ('and', 'or'),
        ('=', '!=', '>=', '<=', 'in'),
        ('..', '%'),
        ('+', '-', '&'),
        ('*', '/'),
        ('^', '+-'),
        ('.',)
    )

    def lexe(self, reader):
        from nylo.lexers.values.value import Value
        if not reader.any_starts_with(self.unary_symbols):
            yield Value(reader).value
        if (not reader.any_starts_with(self.symbols)
                or reader.any_starts_with(self.to_avoid)):
            return
        symbol = reader.any_starts_with(self.symbols)
        reader.move(len(symbol))
        yield Symbol(reader).value
        yield symbol

    def parse(self, reader):
        *values, symbol = list(self.lexe(reader))
        if not values:
            return symbol
        newobj = SymObj(symbol, values)
        if isinstance(values[1], SymObj):
            if self.priority(symbol) > self.priority(values[1].value):
                otherobj = newobj.args[1]
                otherobj.args[0], newobj.args[1] = newobj, otherobj.args[0]
                newobj = otherobj
        if Keyword('_implicit') in newobj.args:
            newobj = Struct(defaultdict(list, {Keyword('_args'): [Keyword('_implicit')],
                                               '_implicit': ['_arg'],
                                               Keyword('self'): [newobj]}))
        return newobj

    def priority(self, symbol):
        return [symbol in value for value in self.symbols_priority].index(True)
