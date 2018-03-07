from nylo.base_objects.Token import Token

class Symbol(Token):
    
    starts = ['=', 'and', '>', 'or', '<', 'not', '!=', 'xor', '>=',
              '>>', '<=', '<<', '+', '..', '-', 'in', '*', '+-',
              '/', '^', '%', '&', ':', '.']
    
    def parse(self, reader):
        reader.move(len(self.start_found))
        self.value = self.start_found
