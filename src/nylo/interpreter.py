class Integer(int):
    pass

class Float(float):
    pass

class String(str):
    pass

class Variable(str):
    
    def __repr__(self):
        return '$%s' % self

class Struct:

    def __init__(self, dirs, atoms, value):
        self.dirs, self.atoms, self.value = dirs, atoms, value
        
    def __repr__(self):
        return "%s/%s/%s" % (self.dirs, self.atoms, self.value)
