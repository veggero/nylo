"""
Contains the Lexer class definition.
"""

from abc import abstractmethod

class Lexer:
    """This is the base class for every
    Nylo parser.
    """

    def __init__(self, reader):
        reader.avoid_whitespace()
        self.reader = reader
        self.value = self.parse(reader)
        reader.avoid_whitespace()

    @abstractmethod
    def parse(self, reader):
        """Takes the list of characters from lexe
        and return the right object from them.
        """

    @abstractmethod
    def lexe(self, reader):
        """Yield every character that makes
        the object to parse.
        """
