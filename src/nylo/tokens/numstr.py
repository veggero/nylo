"""
Contains Number and String classes definitions.
"""

import string
from nylo.token import Token


class Number(Token):
    
    def __init__(self, value=''):
        self.value = value
        
    @staticmethod
    def can_parse(parser):
        return parser.any_starts_with(string.digits)
        
    def parse(self, parser):
        if ((parser.starts_with('.') and 
            parser.code[parser.reading_at + 1] in string.digits
            and not '.' in self.value)
            or parser.any_starts_with(string.digits + '_')):
            parser.parse(self)
            self.value += parser.move()
        else:
            parser.hasparsed(Number(float(self.value) 
                if '.' in self.value else int(self.value)))
    
    def transpile(self, mesh, path):
        pass
    
    def __repr__(self):
        return repr(self.value)
        
    def interprete(self, mesh, interpreting, interpreted):
        interpreting.append(self)
        
    def evaluate(self, interpreting, interpreted):
        interpreted.append(self)
        
    def chroot(self, oldroot, newroot):
        return self
            
class String:

    start_to_ends = {'"': '"', "'": "'", '«': '»'}
    
    def __init__(self, value=''):
        self.value = value
    
    @staticmethod
    def can_parse(parser):
        return parser.any_starts_with(String.start_to_ends)
    
    def parse(self, parser):
        start = parser.move()
        while parser.read() != self.start_to_ends[start]:
            self.value += parser.move()
        parser.move()
        parser.hasparsed(self)
    
    def transpile(self, mesh, path):
        pass
    
    def __repr__(self):
        return self.value
        
    def interprete(self, mesh, interpreting, interpreted):
        interpreting.append(self)
        
    def evaluate(self, interpreting, interpreted):
        interpreted.append(self)
        
    def chroot(self, oldroot, newroot):
        return self
