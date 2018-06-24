"""
Contains the Symbol class definition.
"""

import operator as op
from collections import defaultdict
from nylo.token import Token
from nylo.tokens.value import Value


class Symbol(Token):
    
    map_to_py = {
        '+': op.add, '-': op.sub, '=': op.eq, 
        'and ': op.and_, '>': op.gt, '<': op.lt,
        '!=': op.ne, 'xor ': op.xor, '>=': op.ge, 
        '<=': op.le, '*': op.mul, '/': op.truediv,
        '^': op.pow, '%': op.mod, '&': op.add, 
        'or ': op.or_, '..': NotImplemented, 
        'in ': NotImplemented, '+-': NotImplemented, 
        '|': NotImplemented,'.': NotImplemented, 
        'not ': op.not_}
    
    symbols, to_avoid = [*map_to_py], ('->',)
    
    symbols_priority = (
        ('|',), ('and ', 'or ', 'xor '),
        ('=', '!=', '>=', '<=', 'in ', '>', '<'),
        ('..', '%'), ('+', '-', '&'),
        ('*', '/'), ('^', '+-'), ('.',))
    
    def __init__(self, op=None, args=None):
        self.op, self.args = op, args if args else []
        
    def parse(self, parser):
        if not self.op:
            self.op = parser.any_starts_with(self.symbols) or None
            if self.op and not parser.any_starts_with(self.to_avoid):
                parser.move(len(self.op))
                self.args.append(parser.getarg())
                parser.parse(self, Value())
        else:
            self.args.append(parser.getarg())
            if (isinstance(self.args[1], Symbol) and 
                self.priority() > self.args[1].priority()):
                otherobj = self.args[1]
                otherobj.args[0], self.args[1] = self, otherobj.args[0]
                parser.hasparsed(otherobj)
            else:
                parser.hasparsed(self)

    def priority(self):
        "Get the priority of the symbol"
        return [self.op in value for value in self.symbols_priority].index(True)
    
    def traspile(self, mesh, path):
        for i, arg in enumerate(self.args):
            arg.transpile(mesh, path+(i,))
    
    def __repr__(self):
        return str(self.op) + ' ' + ' '.join(map(repr, self.args))
