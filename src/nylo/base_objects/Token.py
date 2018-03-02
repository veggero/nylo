class Token:
    
    def __init__(self, reader, start_found=None):
        self.start_found = start_found
        self.line = reader.get_line()
        self.char = reader.get_char()
        while reader.read() in ' \t\n': reader.move()
        self.parse(reader)
        while reader.read() in ' \t\n': reader.move()
        
    def __repr__(self):
        if hasattr(self, 'name'): return self.name
        if hasattr(self, 'line'):
            return '<{t} at l{l} c{c}>'.format(
                                    t=self.__class__.__name__,
                                    l=self.line,
                                    c=self.char)
        else:
            return self.__class__.__name__
