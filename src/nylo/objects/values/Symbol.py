from nylo.objects.NyObject import NyObject
from nylo.objects.values.Value import Value
from functools import reduce

class Symbol(NyObject):
    
    map_to_py = {
        '+': '__add__',
        '-': '__sub__',
        '=': '__eq__',
        'and ': '__and__',
        '>': '__gt__',
        '<': '__lt__',
        '!=': '__ne__',
        'xor ': '__xor__',
        '>=': '__ge__',
        '<=': '__le__',
        '*': '__mul__',
        '/': '__div__',
        '^': '__pow__',
        '%': '__mod__',
        '&': '__sum__'
        }
    
    def __init__(self, value, args): self.value, self.args = value, args

    def __repr__(self): return str(self)

    def __str__(self): return (' %s ' % self.value).join(str(k) for k in self.args)
    
    def evaluate(self, stack):
        self.args = [k.evaluate(stack) for k in self.args]
        return Value(getattr(self.args[0].value, 
                self.map_to_py[self.value])(self.args[1].value))
