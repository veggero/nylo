class Token:
    
    def __init__(self, reader, start_found=None):
        self.start_found = start_found
        self.line = reader.get_line()
        self.char = reader.get_char()
        while reader.read() in ' \t\n': reader.move()
        self.parse(reader)
        while reader.read() in ' \t\n': reader.move()
        
    def __repr__(self):
        try: return self.name
        except AttributeError: return '<{t} at l{l} c{c}>'.format(
                                           t=t.__class__.__name__,
                                           l=self.line,
                                           c=self.char)
