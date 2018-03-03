from nylo.exceptions import need_comma, cant_return, cant_accept
from nylo.base_objects.Token import Token
from nylo.struct_objects.StructEl import StructEl
from nylo.derived_objects.syntax_unrelated_objects import (Set, Output, 
                                                           TypeDef)
from nylo.value_objects.Value import Value

class Struct(Token):
    
    starts = ['(']
    ends = [')']
    
    
    def parse(self, reader):
        self.values = []
        reader.move()

        if reader.read() != ')': self.values.append(StructEl(reader).value)
        
        while not reader.read() in self.ends:
            if not reader.read() == ',': need_comma()
            reader.move()
            if reader.read() == '\0': reader.move()
            self.values.append(StructEl(reader).value)
            
        reader.move()
        
        
    def evaluate(self, stack): 
        if any(isinstance(v, TypeDef) for v in self.values): return self
        for el in self.values[::-1]:
            if isinstance(el, Value): 
                stack.add_call(self, self)
                to_return = el.evaluate(stack)
                stack.close_call()
                return to_return
        raise cant_return(repr(self))
    
    
    def get_value(value, stack):
        stack.add_call(self, self)
        to_r = stack.get_variable(value)
        stack.close_call()
        return to_r
          
    
    def update(self, struct, stack):
        for element in struct.values:
            self.update_element(element, stack)
            
    
    def update_element(self, el, stack):
        if isinstance(el, TypeDef):
            if not el in self.values: self.values.append(el)
        elif isinstance(el, Set):
            if el.value.target in values: 
                del self.values[values.index(el.target)]
            self.values.append(el)
        elif isinstance(el, Output):
            stack[-1][el.value.to.value] = self.get_value(
                el.value.value.value, stack)
        elif isinstance(el, Value): 
            for i, value in enumerate(self.values):
                if isinstance(value, TypeDef):
                    if not value.kws[0].value == 'code':
                        el = el.evaluate(stack)
                    self.values[i] = Set(value, el)
                    return
            cant_accept(el)

    
    def __setitem__(self, el, value):
        for element in self.values:
            if isinstance(element, Set):
                if element.target.kws[-1].value == el:
                    if element.target.kws[0].value == 'code': continue
                    element.value = value
        

    def __contains__(self, element):
        return element in [el.target.kws[-1].value
                           for el in self.values
                           if isinstance(el, Set)]
    
    def __getitem__(self, element):
        return [el.value
                for el in self.values
                if isinstance(el, Set) and
                el.target.kws[-1].value == element][0]
