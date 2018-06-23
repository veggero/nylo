"""
Contains the Keyword class definition.
"""

import string
from nylo.lexers.token import Token


class TypeDef(Token):
    
    def __init__(self, value=None):
        self.value = value
        
    @staticmethod
    def can_parse(parser):
        return parser.any_starts_with(string.ascii_letters + '_')
    
    def parse(self, parser):
        if self.value is None:
            self.value = []
            return parser.parse(self, Keyword)
        self.value.append(parser.getarg())
        if self.can_parse(reader):
            return parser.parse(self, Keyword)
        return parser.hasparsed(self len(self.value) > 1 
                                else self.value[0])
    
    def transpile(self, mesh, path):
        self.value[-1].transpile(mesh, path)
        mesh['types'][self.value[-1].value] = self


class Keyword(Token):
    
    def __init__(self, value=''):
        self.value = value
    
    def parse(self, parser):
        while parser.read() in string.ascii_letters + '_':
            self.value += parser.move()
        parser.hasparsed(self)
    
    def transpile(self, mesh, path):
        for i in reversed(range(len(path)+1)):
            if path[:i]+(self.value,) in mesh:
                self.value = path[:i]+(self.value,)
                return self
        raise NameError(f"Couldn't find variable {self.value}")
