class Integer(int):
    pass

class Float(float):
    pass

class Text(str):
    pass

class Variable(str):
    
    def __repr__(self):
        return '$%s' % self
    
class Op:
    
    def __init__(self, op, args):
        self.op, self.args = op, args
        
    def __repr__(self):
        return '(%s)(%s)' % (self.op, ' '.join(map(repr, self.args)))

class Struct:

    def __init__(self, dirs, atoms, value):
        self.dirs, self.atoms, self.value = dirs, atoms, value
        
    def __repr__(self):
        return "%s/%s/%s" % (self.dirs, self.atoms, self.value)
