class Lexer:
    
    def __init__(self, reader):
        self.reader = reader
        self.value = self.parse(reader)
