"""
Contains the Lexer class definition.
"""

from abc import abstractmethod, ABC as Abstract
from nylo.lexers.parser import Parser

class Token(Abstract):
    """This is the base class for every
    Nylo parser.
    """

    @abstractmethod
    def __init__(self, *values) -> None:
        "Initialize the token object"
    
    @staticmethod
    def can_parse(parser: Parser) -> bool:
        """Check if the Token can be parsed,
        by checking if the parser starts with
        the character that compose the token.
        Some tokens doesn't need this function.
        """

    @abstractmethod
    def parse(self, parser: Parser) -> None:
        """Parse the object by reading parser characters;
        when done, adds the parsed object by calling
        parser.hasparsed; might call parser.parse for
        parsing more tokens.
        """
        
    @abstracmethod
    def transpile(self, mesh: dict, path: tuple) -> Token:
        """Traspile the value into the mesh; initialize
        mesh nodes and their values. Returns the token
        that should go to interpretation."""
        
    @abstracmethod
    def evaluate(self, mesh: dict, interpreting: list, interpreted: list):
        """Evaluate the Token, adding things to interpreter or
        adding things that has been interpreted to the two lists.
        Values will go to interpreted, while tokens such as
        variables will add other tokens to the interpreting list
        to interpreter.
        """
        
    @abstracmethod
    def chroot(self, oldroot: tuple, newroot: tuple) -> None:
        """Change the root location for absolute variable
        references
        """
        
    def __str__(self):
        return f"{type(self).__name__}:{self.value}"
