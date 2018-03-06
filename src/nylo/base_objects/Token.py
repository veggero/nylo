class Token:
    """
    Token class mostly a placeholder; it manages the initilization of
    parsed tokens and their representations.
    """
    
    def __init__(self, reader, start_found=None):
        "Initialize a Token and call their parse() function"
        self.start_found = start_found
        self.line = reader.get_line()
        self.char = reader.get_char()
        while reader.read() in ' \t\n': reader.move()
        self.parse(reader)
        while reader.read() in ' \t\n': reader.move()
        
    def __repr__(self):
        "Represent the token"
        if hasattr(self, 'name'): return '<'+self.name+'>'
        elif hasattr(self, 'line'):
            return '<{t} at line {l} char {c}>'.format(
                                    t=self.__class__.__name__,
                                    l=self.line,
                                    c=self.char)
        else:
            return '<'+self.__class__.__name__+'>'
