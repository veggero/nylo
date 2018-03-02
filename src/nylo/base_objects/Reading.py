class Reading:
    
    def __init__(self, code, reading_at):
        self.code = code+'\0'
        self.reading_at = reading_at
        self.line = 1
        self.char = 1
        
    def read(self):
        return self.code[self.reading_at]
    
    def move(self, char_num=1):
        for i in range(char_num): self.move_char()
    
    def move_char(self):
        if self.read() == '\n': 
            self.line += 1
            self.char = 1
        else: self.char += 1
        self.reading_at += 1
        if self.reading_at == len(self.code):
            raise SyntaxError("EOL while scanning")
    
    def read_and_move(self):
        value = self.read()
        self.move_char()
        return value
    
    def any_starts_with(self, starts):
        for start in starts:
            if self.starts_with(start): return start
        return False
    
    def starts_with(self, string):
        return self.code.startswith(string, self.reading_at)
        
    def get_reading_char(self):
        return self.reading_at
    
    def get_line(self):
        return self.line
    
    def get_char(self):
        return self.char

    def goto(self, reader):
        self.reading_at = reader.reading_at
        self.line = reader.line
        self.char = reader.char
