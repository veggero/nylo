class Integer(int):
    pass

class Float(float):
    pass

class String(str):
    pass

class Variable(str):
    
    def __repr__(self):
        return '$%s' % self
