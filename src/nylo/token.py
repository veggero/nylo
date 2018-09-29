"""
Contains the Lexer class definition.
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""

from abc import abstractmethod, ABC as Abstract
from nylo.parser import Parser

class Token(Abstract):
    """This is the base class for every
    Nylo parser.
    """

    def __init__(self, *values):
        "Initialize the token object."
    
    def can_parse(parser: Parser) -> bool:
        """Check if the Token can be parsed,
        by checking if the parser starts with
        the character that compose the token.
        Some tokens doesn't need this function.
        """

    def parse(self, parser: Parser):
        """Parse the object by reading parser characters;
        when done, adds the parsed object by calling
        parser.hasparsed; might call parser.parse for
        parsing more tokens.
        """
    
    def transpile(self, mesh: dict, path: tuple):
        """Traspile the value into the mesh; initialize
        mesh nodes and their values. Returns the token
        that should go to interpretation."""
        
    def interprete(self, mesh: dict, interpreting: list, interpreted: list):
        NotImplemented #TODO
        
    def evaluate(self, mesh: dict, interpreting: list, interpreted: list):
        """Evaluate the Token, adding things to interpreter or
        adding things that has been interpreted to the two lists.
        Values will go to interpreted, while tokens such as
        variables will add other tokens to the interpreting list
        to interpreter.
        """
        
    def chroot(self, oldroot: tuple, newroot: tuple):
        """Change the root location for absolute variable
        references.
        """
        
    def __hash__(self):
        return hash(tuple(tuple(x) if isinstance(x, list)
            else x for key, x in self.__dict__.items()
            if key != 'location'))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
