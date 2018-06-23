"""
Contains Number and String classes definitions.
"""

import string
from nylo.lexers.token import Token


class Number(Token):
    
    def __init__(self, value=''):
        self.value = value
        
    @staticmethod
    def can_parse(parser):
        return parser.any_starts_with(string.digits)
        
    def parse(self, parser):
        if ((parser.starts_with('.') and 
            reader.code[reader.reading_at + 1] in string.digits
            and not '.' in self.value)
            or parser.any_starts_with(string.digits + '_')):
            parser.parse(self)
            self.value += parser.move()
        else:
            parser.hasparsed(Number(float(self.value) 
                if '.' in self.value else int(self.value)))
    
    def transpile(self, mesh, path):
        pass
            
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
        reader.move()
        parser.hasparsed(self)
    
    def transpile(self, mesh, path):
        pass
