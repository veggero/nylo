"""
Contains the Struct class definition.
"""

from collections import defaultdict
from nylo.token import Token
from nylo.tokens.keyword import Keyword, TypeDef
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
        return '(%s)' % ', '.join(f'{key}: {value}' for key, value in self.value.items()
                                  if value)
    
    def traspile(self, mesh, path):
        mesh[path] = Keyword('placeholedr'),
        for value in [*self.value.keys()] + self.value[Keyword('atoms')]:
            if isinstance(value, TypeDef):
                value = value.value[-1]
            if isinstance(value, Keyword):
                mesh[path+(key,)] = Keyword('placeholder')
                if value in self.value[Keyword('atoms')]:
                    mesh['arguments'][path].append(value)
        for key, value in self.value.items():
            if isinstance(key, TypeDef):
                key = key.value[-1]
            if len(value)==1:
                mesh[path+(key,)] = value[0].transpile(mesh, path+(key,))
            else:
                for i, vl in enumerate(value):
                    mesh[path+(key,i)] = vl.traspile(mesh, path+(key, i))

#class OLDStruct(Lexer):
#        
#    def transpile_call(self, mesh, path, called):
#        for key, value in ([*self.value.items()]+
#                           [*zip(mesh['arguments'][called],
#                                 self.value['atoms'])]):
#            if key == 'atoms': 
#                continue
#            if not isinstance(key, tuple):
#                if key == 'self':
#                    continue
#                key = key.transpile(mesh, called)
#                value = value[0]
#            key = path+key[len(called):]
#            value = value.transpile(mesh, path)
#            mesh[key] = value
#            
#            
#def get_raw_key(key):
#        if isinstance(key, str):
#            return key
#        key = key.value.value
#        if isinstance(key, Keyword):
#            key = key.value
#        elif isinstance(key, list) and all(isinstance(el, Keyword) for el in key):
#            *types, key = key
#            key = key.value
#        else:
#            raise SyntaxError("Expected dictionary key, found value.")
#        return key
