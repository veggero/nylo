from nylo.exceptions import need_comma, cant_return, cant_accept, cant_eval
from nylo.base_objects.Token import Token
from nylo.derived_objects.syntax_unrelated_objects import (Set, Output, 
                                                           TypeDef)
from nylo.value_objects.Value import Value

class Struct(Token):
    
    starts = ['(']
    ends = [')']
    
    
    def parse(self, reader):
        from nylo.struct_objects.StructEl import StructEl
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
        """
        Se ci sono TypeDef nella struct torna se stessa,
        se ci sono value torna quelli, 
        altrimenti torna se stessa.
        """
        if any(isinstance(v, TypeDef) for v in self.values): return self
        for el in self.values[::-1]:
            if isinstance(el, Value): 
                stack.add_call(self, self)
                to_return = el.evaluate(stack)
                stack.close_call()
                return to_return
        return self
    
    
    def evaluate_values(self, stack):
        from nylo.derived_objects.python_linked_objects import ValueLayer
        """
        Evaluta tutti i valori di Set e i TypeDef.
        """
        for i, value in enumerate(self.values):
            if isinstance(value, Set): 
                # poetry: evaluation
                # Evaluate the value of the value, put it in a value layer, 
                # and set it to the vaule of the value. Clear?
                value.value = ValueLayer(value.value.evaluate(stack))
            elif isinstance(value, TypeDef):
                if len(value.kws)>1: cant_eval(value)
                self.values[i] = ValueLayer(
                    stack.get_variable(value.kws[0].value))
    
    
    def get_value(self, value, stack):
        """
        Crea la stack call e prende il proprio valore.
        """
        stack.add_call(self, self)
        to_r = stack.get_variable(value)
        stack.close_call()
        return to_r
          
    
    def update(self, struct, stack):
        for element in struct.values:
            self.update_element(element, stack)
            
    
    def update_element(self, el, stack):
        """
        Aggiunge un elemento a se stesso.
        I value finiscono sui TypeDef con solo il tipo,
        gli output danno il valore,
        i Set aggiornano vecchi valori Set oppure 
        trasformano un Set in un TypeDef
        """
        if isinstance(el, Set):
            for i, value in enumerate(self.values):
                if ((isinstance(value, TypeDef) and 
                    value.kws[-1].value == el.target.kws[-1].value) or
                    (isinstance(value, Set) and
                     value.target.kws[-1].value == el.target.kws[-1].value)):
                    del self.values[i]
                    break
            self.values.append(el)
        elif isinstance(el, Output):
            stack[-1][el.to.value] = self.get_value(el.value.value, stack)
        elif isinstance(el, Value):
            for i, value in enumerate(self.values):
                if isinstance(value, TypeDef):
                    if value.kws[-1].value != 'code': el = el.evaluate(stack)
                    if len(value.kws) == 1: 
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
