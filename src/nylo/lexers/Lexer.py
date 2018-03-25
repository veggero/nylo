class Lexer:
    
    def __init__(self, reader):
        reader.avoid_whitespace()
        self.reader = reader
        self.value = self.parse(reader)
        reader.avoid_whitespace()
