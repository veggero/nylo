"""
Contains the Symbol class definition.
"""

import operator

from collections import defaultdict
from nylo.lexers.lexer import Lexer


class Symbol(Lexer):
    """Symbol class is used to
    define all keywords (e.g. ``+``, ``-``, etc..) and to
    evaluate all their uses (ex. `'1 + 1``)."""

    unary_symbols = '+', '-', 'not '
    
    symbols = ('=', 'and ', '>', 'or ', '<', '!=', 'xor ', '>=',
               '<=', '..', 'in ', '*', '+-', '/', '^', '|', '%',
               '&', '.') + unary_symbols
    
    to_avoid = '->',
    
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
    
    map_to_py = {
        '+': operator.add, '-': operator.sub,
        '=': operator.eq, 'and ': operator.and_,
        '>': operator.gt, '<': operator.lt,
        '!=': operator.ne, 'xor ': operator.xor,
        '>=': operator.ge, '<=': operator.le,
        '*': operator.mul, '/': operator.truediv,
        '^': operator.pow, '%': operator.mod,
        '&': operator.add
    }

    def lexe(self, reader):
        """It generates all characters
        associated to the token.
        """
        from nylo.lexers.values.value import Value
        if not reader.any_starts_with(self.unary_symbols):
            yield Value(reader)
        if (not reader.any_starts_with(self.symbols)
                or reader.any_starts_with(self.to_avoid)):
            return
        symbol = reader.any_starts_with(self.symbols)
        reader.move(len(symbol))
        yield Symbol(reader)
        yield symbol

    def parse(self, reader):
        """It returns all lexer characters using
        an object.
        """
        *values, symbol = list(self.lexe(reader))
        if not values:
            return symbol
        newobj = [symbol, values]
        if isinstance(values[1], Symbol) and isinstance(values[1].value, list):
            if self.priority(symbol) > self.priority(values[1].value[0]):
                otherobj = values[1]
                otherobj.value[1][0], values[1] = newobj, otherobj.value[1][0]
                newobj = otherobj
        #if Keyword('_implicit') in newobj.args:
        #    newobj = Struct(defaultdict(list, {Keyword('_args'): [Keyword('_implicit')],
        #                                       '_implicit': ['_arg'],
        #                                       Keyword('self'): [newobj]}))
        return newobj

    def priority(self, symbol):
        """Get the priority of the symbol"""
        return [symbol in value for value in self.symbols_priority].index(True)
    
    def transpile(obj, mesh, path):
        if isinstance(obj.value, list):
            op, args = obj.value
            return ([Symbol.map_to_py[op]]+
                    [arg.transpile(mesh, path+(str(i),)) for i, arg in enumerate(args)])
        else:
            return obj.value.transpile(mesh, path)
