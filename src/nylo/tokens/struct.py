"""
Contains the Struct class definition.
"""

from collections import defaultdict
from nylo.token import Token
from nylo.tokens.keyword import Keyword
from nylo.tokens.symbol import Symbol


class Struct(Token):
    
    def __init__(self, value=None):
        self.value = value if value else defaultdict(list)
        self.key = Keyword('atoms')
        
    @staticmethod
    def can_parse(parser):
        return parser.starts_with('(')
    
    def parse(self, parser):
        if parser.any_starts_with(('(', ':', ',')):
            parser.move()
            parser.parse(self, Symbol())
        elif parser.starts_with(')'):
            parser.hasparsed(self)
        elif parser.starts_with('->'):
            parser.move(2)
            parser.parse(self, Symbol())
            self.key = Keyword('self')
        else:
            parser.parse(self, Symbol)
        if parser.starts_with(':'):
            self.key = parser.getarg()
        elif not parser.starts_with('('):
            self.value[self.key].append(parser.getarg())
            self.key = Keyword('atoms')

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
