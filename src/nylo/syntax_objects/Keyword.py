import string

from nylo.base_objects.Token import Token

class Keyword(Token):
    
    starts = list(string.ascii_letters)+['_']
        
    def parse(self, reader):
        out = ''
        while (reader.read() in 
               self.starts + ['_'] + list(string.digits)): 
            out += reader.read_and_move()
        self.value = out
        self.condition = [self.value]
        
    def evaluate(self, stack):
        for vardict in stack[::-1]:
            if self.value in vardict:
                return vardict[self.value]
        raise NameError('name {name} is not defined'.format(name=self.value))
