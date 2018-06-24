"""
Contains the Struct class definition.
"""

from collections import defaultdict
from nylo.token import Token
from nylo.tokens.keyword import Keyword
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
        return '(%s)' % ', '.join(f'{key}:{value}' for key, value in self.value.items())

#class OLDStruct(Lexer):
#
#    def transpile(self, mesh, path):
#        if isinstance(self.value, defaultdict):
#            for key, value in self.value.items():
#                if key == "atoms":
#                    for el in value:
#                        try:
#                            arg = path+(get_raw_key(el),)
#                            mesh[arg] = ('placeholder',)
#                            mesh['arguments'][path].append(arg)
#                        except SyntaxError:
#                            pass
#                key = get_raw_key(key)
#                mesh[path+(key,)] = ('placeholder',)
#            for i, (key, value) in enumerate(self.value.items()):
#                key = get_raw_key(key)
#                newpath = path+(key,)
#                if len(value)==1:
#                    mesh[newpath] = value[0].transpile(mesh, newpath)
#                else:
#                    for i, vl in enumerate(value):
#                        mesh[newpath+(i,)] = vl.transpile(mesh, newpath+(i,))
#            return ('placeholder',)
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
