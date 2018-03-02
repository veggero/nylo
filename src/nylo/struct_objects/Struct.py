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
        self.condition = []
        reader.move()
        
        while not reader.read() in self.ends:
            self.values.append(StructEl(reader))
            self.condition.extend(self.values[-1].condition)
            while reader.read() == ',': reader.move()
            if reader.read() == '\0': reader.move()
            
        reader.move()
        
        
    def evaluate(self, stack): return self
        
        
    def called(self, stack): 
        from nylo.derived_objects.python_linked_objects import ValueLayer
        if not self.get_element('_self'):
            for el in self.values[::-1]:
                if isinstance(el.value, Value): 
                    self.values[self.values.index(el)] = ValueLayer(Set(
                         TypeDef([ValueLayer('_self')]), el.value))
                    break
            else:
                raise Exception(
                    'Structure {s} is not callable'.format(s=repr(self)))
                
        return self.get_value('_self', stack)
        
        
    def get_value(self, tvalue, stack):
        value = self.get_element(tvalue)
        if not value:
            raise Exception(
                "Requested value {t} not in structure".format(t=tvalue))
        stack.add_call(self)
        
        if value.target.kws[0].value != 'code':
            for cond in value.condition:
                if cond == tvalue: continue
                if self.get_element(cond):
                    stack[-1][cond] = self.get_value(cond, stack)
            to_r = value.evaluate(stack)
        else:
            to_r = value
        stack.close_call()
        return to_r
    
    
    def get_element(self, value):
        for element in self.values:
            if (isinstance(element.value, Set) and 
                element.value.target.kws[-1].value == value):
                return element.value
        
        return None
    
    
    def update(self, struct, stack):
        for element in struct.values:
            self.update_element(element, stack)
          
    
    def update_element(self, el, stack):
        from nylo.derived_objects.python_linked_objects import ValueLayer
        values = [v.value for v in self.values]
        if isinstance(el.value, TypeDef):
            if not el in self.values:
                self.values.append(el)
        elif isinstance(el.value, Set):
            if el.value.target in values:
                del self.values[values.index(el.target)]
            self.values.append(el)
        elif isinstance(el.value, Output):
            stack[el.value.to.value] = self.get_value(
                el.value.value.value, stack)
        elif isinstance(el.value, Value): 
            for value in values:
                if isinstance(value, TypeDef):
                    if value.kws[0].value == 'code':
                        self.values[values.index(value)] = ValueLayer(
                            Set(value, el))
                        return
            el = el.evaluate(stack)
            for value in values:
                if isinstance(value, TypeDef):
                    self.values[values.index(value)] = ValueLayer(
                        Set(value, ValueLayer(el)))
                    return
            raise TypeError('can\'t accept value {value}'.format(value=el))
