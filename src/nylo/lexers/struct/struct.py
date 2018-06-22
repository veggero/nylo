"""
Contains the Struct class definition.
"""

from collections import defaultdict
from nylo.lexers.lexer import Lexer
from nylo.lexers.values.keyword import Keyword


class Struct(Lexer):
    """This class is used in parsing everything inside
    round brackets or indented. It generates a Struct
    object.
    """

    @staticmethod
    def able(reader):
        """It checks if the token is
        readable.
        """
        return reader.read() in '('

    @staticmethod
    def parse(reader):
        """It returns all lexer characters using
        an object.
        """
        from nylo.lexers.values.symbol import Symbol
        atoms = defaultdict(list)
        reader.move()
        reader.avoid_whitespace()
        while not reader.any_starts_with([')', '->']):
            if reader.read() in ',':
                reader.move()
                reader.avoid_whitespace()
                continue
            value = Symbol(reader)
            if reader.read() in ':':
                reader.move()
                key, value = value, Symbol(reader)
                atoms[key].append(value)
            else:
                atoms['atoms'].append(value)
        if reader.starts_with('->'):
            reader.move(2)
            atoms['self'].append(Symbol(reader))
        reader.avoid_whitespace()
        reader.move()
        if (len(atoms) == 1 and 'atoms' in atoms and
                len(atoms['atoms']) == 1):
            return atoms['atoms'][0]
        return atoms

    def transpile(self, mesh, path):
        if isinstance(self.value, defaultdict):
            for key, value in self.value.items():
                if key == "atoms":
                    for el in value:
                        try:
                            arg = path+(get_raw_key(el),)
                            mesh[arg] = ('placeholder',)
                            mesh['arguments'][path].append(arg)
                        except SyntaxError:
                            pass
                key = get_raw_key(key)
                mesh[path+(key,)] = ('placeholder',)
            for i, (key, value) in enumerate(self.value.items()):
                key = get_raw_key(key)
                newpath = path+(key,)
                if len(value)==1:
                    mesh[newpath] = value[0].transpile(mesh, newpath)
                else:
                    for i, vl in enumerate(value):
                        mesh[newpath+(i,)] = vl.transpile(mesh, newpath+(i,))
            return ('placeholder',)
        else:
            return self.value.transpile(mesh, path)
        
    def transpile_call(self, mesh, path, called):
        for key, value in ([*self.value.items()]+
                           [*zip(mesh['arguments'][called],
                                 self.value['atoms'])]):
            if key == 'atoms': 
                continue
            if not isinstance(key, tuple):
                if key == 'self':
                    continue
                key = key.transpile(mesh, called)
                value = value[0]
            key = path+key[len(called):]
            value = value.transpile(mesh, path)
            mesh[key] = value
            
            
def get_raw_key(key):
        if isinstance(key, str):
            return key
        key = key.value.value
        if isinstance(key, Keyword):
            key = key.value
        elif isinstance(key, list) and all(isinstance(el, Keyword) for el in key):
            *types, key = key
            key = key.value
        else:
            raise SyntaxError("Expected dictionary key, found value.")
        return key
