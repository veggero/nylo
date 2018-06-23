"""
Contains the Symbol class definition.
"""

import operator as op
from collections import defaultdict
from nylo.lexers.token import Token
from nylo.lexers.values.value import Value


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
    
    def __init__(self, op=None, args=[]):
        self.op, self.args = op, args
        
    def parse(self, parser):
        if not op:
            self.op = True
            parser.parse(Value(), self, Value())
        elif op == True:
            self.op = parser.any_starts_with(self.symbols) or True
            if self.op != True:
                self.args.append(parser.parsed.pop())
            else:
                parser.parsing.pop()
        else:
            self.args.append(parser.parsed.pop())
            if (isinstance(self.args[1], Symbol) and 
                self.priority() > self.args[1].priority()):
                otherobj = self.args[1]
                otherobj.args[0], self.args[1] = self, otherobj.args[0]
                parser.hasparsed(otherobj)
            else:
                parser.hasparsed(self)

    def priority(self, symbol):
        "Get the priority of the symbol"
        return [self in value for value in self.symbols_priority].index(True)
            

#class OLDSymbol(Lexer):
#    
#    def transpile(obj, mesh, path):
#        if isinstance(obj.value, list):
#            op, args = obj.value
#            nw = [lambda x, y: Symbol.map_to_py[op](x, y)]
#            for i, arg in enumerate(args):
#                newarg = arg.transpile(mesh, path+(str(i),))
#                if not isinstance(arg, list):
#                    newarg = [newarg]
#                nw.extend(newarg)
#            return nw
#        else:
#            return obj.value.transpile(mesh, path)
