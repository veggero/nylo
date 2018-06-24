"""
Contains the Value class definition.
"""

from collections import defaultdict
from nylo.token import Token
from nylo.tokens.keyword import TypeDef
from nylo.tokens.numstr import Number, String


class Value(Token):
    
    def __init__(self, value=None):
        self.value = value
        
    def parse(self, parser):
        from nylo.tokens.struct import Struct
        from nylo.tokens.symbol import Symbol
        for token in (TypeDef, Number, String, Struct):
            if token.can_parse(parser):
                return parser.parse(Symbol(), Call(), token())
        parser.hasparsed(None)
        
    def __repr__(self):
        return '(Value)'
                
                
class Call(Token):
    
    def __init__(self, called=None, caller=None):
        self.called, self.caller = called, caller
        
    def parse(self, parser):
        from nylo.tokens.struct import Struct
        if not parser.starts_with('('): 
            return
        if self.called:
            self.caller = parser.getarg()
            parser.hasparsed(self)
            parser.parse(Call())
        else:
            self.called = parser.getarg()
            parser.parse(self, Struct())
            
    def __repr__(self):
        return f'{self.called}{self.caller}'
            

#class OLDValue(Lexer):
#    def transpile(self, mesh, path):
#        if isinstance(self.value, list):
#            return self.value[-1].transpile(mesh, path)
#        if isinstance(self.value, tuple):
#            called, caller = self.value
#            if isinstance(called, Keyword):
#                called = called.transpile(mesh, path)
#            else:
#                called, newcalled = path+('temp',), called
#                mesh[called] = newcalled.transpile(mesh, called)
#            if not isinstance(caller.value, defaultdict):
#                caller.value = defaultdict(list, {'atoms': [caller.value]})
#            caller.transpile_call(mesh, path, called)
#            mesh['classes'][path] = called
#            if 'self' in caller.value:
#                return caller.value['self'][0].transpile(mesh, called)
#            return path+('self',)
#        else:
#            return self.value.transpile(mesh, path)
