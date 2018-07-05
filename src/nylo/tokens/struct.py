"""
Contains the Struct class definition.
"""

from collections import defaultdict
from nylo.token import Token
from nylo.tokens.keyword import Keyword, TypeDef
from nylo.tokens.symbol import Symbol
from nylo.tokens.value import Value


class Struct(Token):
    
    def __init__(self, value=None):
        self.value = value if value else defaultdict(list)
        self.key = Keyword('atoms')
        
    @staticmethod
    def can_parse(parser):
        return parser.starts_with('(')
    
    def parse(self, parser):
        if parser.starts_with(':'):
            self.key = parser.getarg()
        elif not parser.starts_with('('):
            self.value[self.key].append(parser.getarg())
            if self.value[self.key][-1] is None:
                self.value[self.key].pop()
            self.key = Keyword('atoms')
        if parser.any_starts_with(('(', ':', ',')):
            parser.move()
            parser.parse(self, Value())
        elif parser.starts_with(')'):
            parser.move()
            if (len(self.value) == 1 and
                len(self.value[Keyword('atoms')]) == 1):
                return parser.hasparsed(self.value[Keyword('atoms')][0])
            parser.hasparsed(self)
        elif parser.starts_with('->'):
            parser.move(2)
            parser.parse(self, Value())
            self.key = Keyword('self')
        else:
            parser.parse(self, Value())
            
    def __repr__(self):
        return ('('+', '.join(f'{key}: {value}' for key, value in self.value.items()
                        if value and key not in ('atoms', 'self')) +
                    ', '.join(map(repr, self.value['atoms'])) +
                    ('-> ' + repr(self.value['self'])) * bool(self.value['self']) 
                    + ')')
    
    def transpile(self, mesh, path):
        self.path = path
        for key, value in self.value.items():
            if key == Keyword('atoms'):
                for i, el in enumerate(value):
                    if isinstance(el, TypeDef):
                        el = el.value[-1]
                    if isinstance(el, Keyword):
                        arg = path+(el.value,)
                        mesh[arg] = Value()
                        mesh['arguments'][path].append(arg)
                    else:
                        mesh[path+(Value(i),)] = el
            if isinstance(key, TypeDef):
                key = key.value[-1]
            if isinstance(key, Keyword):
                mesh[path+(key.value,)] = Keyword('placeholder', (Keyword('placeholder'),))
        for key, value in self.value.items():
            if isinstance(key, TypeDef):
                key = key.value[-1]
            newpath = path+(key,)
            if len(value) == 1:
                value[0].transpile(mesh, newpath)
                mesh[newpath] = value[0]
            else:
                for i, vl in enumerate(value):
                    vl.transpile(mesh, newpath+(i,))
                    mesh[newpath+(i,)] = vl
                    
    def transpile_call(self, mesh, path, called):
        for key, value in ([*self.value.items()]+
                           [*zip(mesh['arguments'][called],
                                 self.value[Keyword('atoms')])]):
            if isinstance(key, TypeDef):
                key = key.value[-1]
            if key == Keyword('atoms'): 
                continue
            if isinstance(key, Keyword):
                if key == Keyword('self'):
                    continue
                key.transpile(mesh, called)
                key = key.ref
                value = value[0]
            key = path+key[len(called):]
            value.transpile(mesh, path)
            mesh[key] = value
        mesh['arguments'][path] = \
            mesh['arguments'][called][len(self.value[Keyword('atoms')]):]
        
    def interprete(self, mesh, interpreting, interpreted):
        if self.path+(Keyword('self'),) in mesh:
            return interpreting.append(Keyword('self', self.path+(Keyword('self'),)))
        interpreting.append(self)
    
    def evaluate(self, mesh, interpreting, interpreted):
        from nylo.interpreter import interprete as interpr
        interpreted.append(self)
        for key, value in self.value.items():
            if isinstance(key, TypeDef):
                key = key.value[-1]
            newpath = self.path+(key,)
            if len(value) == 1:
                self.value[key][0] = interpr(mesh, newpath)
            else:
                for i, vl in enumerate(value):
                    self.value[key][i] = interpr(mesh, newpath+(i,))
        
    def chroot(self, oldroot, newroot):
        return self
