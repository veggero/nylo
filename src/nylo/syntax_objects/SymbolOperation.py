from nylo.exceptions import cant_assign
from nylo.base_objects.Token import Token
from nylo.syntax_objects.Keyword import Keyword

class SymbolOperation(Token):
    
    def __init__(self, before, symb, after):
        self.before = before
        self.symb = symb
        self.after = after
        
    def evaluate(self, stack):
        
        if self.symb.value == ':': 
            if not isinstance(self.before.value, Keyword):
                raise cant_assign()
            to_set = self.after.evaluate(stack)
            try: to_set.name = self.before.value.value
            except AttributeError: pass
            stack[-1][self.before.value.value] = to_set
            return
            
        bef, aft = self.before.evaluate(stack), self.after.evaluate(stack)
        if self.symb.value == '=': return bef == aft
        if self.symb.value == 'and': return bef and aft
        if self.symb.value == '>': return bef > aft
        if self.symb.value == 'or': return bef or aft
        if self.symb.value == '<': return bef < aft
        # TODO NOT
        if self.symb.value == '!=': return bef != aft
        # TODO XOR
        if self.symb.value == '>=': return bef >= aft
        if self.symb.value == '>>': return bef >> aft
        if self.symb.value == '<=': return bef <= aft
        if self.symb.value == '<<': return bef << aft
        if self.symb.value == '+': return bef + aft
        if self.symb.value == '..': return range(bef, aft)
        if self.symb.value == '-': return bef - aft
        if self.symb.value == 'in': return bef in aft
        if self.symb.value == '*': return bef * aft
        if self.symb.value == '+=': return (bef + aft, bef - aft)
        if self.symb.value == '/': return bef / aft
        if self.symb.value == '^': return pow(bef, aft)
        #TODO -> <- % & : . ++ --
