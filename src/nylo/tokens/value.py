"""
Contains the Value class definition.
"""

from collections import defaultdict
from nylo.token import Token
from nylo.tokens.keyword import TypeDef, Keyword
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
        return repr(self.value)
            
    def interprete(self, mesh, interpreting, interpreted):
        interpreting.append(self)
        
    def evaluate(self, mesh, interpreting, interpreted):
        interpreted.append(self)
        
    def chroot(self, oldroot, newroot):
        return self
                
                
class Call(Token):
    
    def __init__(self, called=None, caller=None):
        self.called, self.caller = called, caller
        
    def parse(self, parser):
        from nylo.tokens.struct import Struct
        if self.called:
            self.caller = parser.getarg()
            parser.hasparsed(self)
            parser.parse(Call())
        else:
            if not parser.starts_with('('): 
                return
            self.called = parser.getarg()
            parser.parse(self, Struct())
            
    def __repr__(self):
        return f'{self.called}{self.caller}'
    
    def transpile(self, mesh, path):
        from nylo.tokens.struct import Struct
        if isinstance(self.called, TypeDef):
            self.called = self.called.value[-1]
        if isinstance(self.called, Keyword):
            self.called.transpile(mesh, path)
            called_path = self.called.ref
        else:
            self.called.transpile(mesh, path+('temp',))
            mesh[path+('temp',)] = self.called
            called_path = path+('temp',)
        if not isinstance(self.caller, Struct):
            self.caller = Struct(defaultdict(list, 
                {Keyword('atoms'): [self.caller]}))
        self.caller.transpile_call(mesh, path, called_path)
        mesh['classes'][path] = called_path
        if Keyword('self') in self.caller.value:
            self.caller.value[Keyword('self')][0].transpile(mesh, called_path)
            mesh[path+(Keyword('self'),)] = \
                self.caller.value[Keyword('self')][0].chroot(path, called_path)
        self.toev = Keyword('self', path+(Keyword('self'),))
            
    def interprete(self, mesh, interpreting, interpreted):
        interpreting.append(self.toev)
        
    def evaluate(self, mesh, interpreting, interpreted):
        interpreted.append(self)
        
    def chroot(self, oldroot, newroot):
        return self.toev.chroot(oldroot, newroot)
