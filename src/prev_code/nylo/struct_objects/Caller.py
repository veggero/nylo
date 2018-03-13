from nylo.exceptions import need_comma
from nylo.base_objects.Token import Token
from nylo.struct_objects.CallerEl import CallerEl
from nylo.syntax_objects.Keyword import Keyword

class Caller(Token):
    
    ends = [')', '|']
    
    def parse(self, reader):
        reader.move()
        self.values = []
        
        if not reader.any_starts_with(self.ends):
            self.values.append(CallerEl(reader).value)
            
        while not reader.any_starts_with(self.ends):
            # hearot ti voglio bene ma se mi togli pure
            # questi inline mi arrabbio
            if not reader.read() == ',': need_comma()
            reader.move()
            if reader.read() == '\0': reader.move()
            self.values.append(CallerEl(reader))
            
        if reader.read() == '|':
            reader.move()
            self.to_output = Keyword(reader)
        else: self.to_output = Keyword(reader)
        
        reader.move()

"""
class Struct(Token):

    starts = ['(']
    ends = [')', '->']

    def parse(self, reader):
        from nylo.struct_objects.StructEl import StructEl
        self.values = []
        reader.move()

        if not reader.any_starts_with(self.ends):
            self.values.append(StructEl(reader).value)

        while not reader.any_starts_with(self.ends):
            if not reader.read() == ',':
                need_comma()
            reader.move()
            if reader.read() == '\0':
                reader.move()
            self.values.append(StructEl(reader).value)

        if reader.starts_with('->'):
            reader.move(2)
            self.output_value = Value(reader)
        else:
            self.output_value = None

        reader.move()

        if len(self.values) == 1 and isinstance(self.values[0], Value):
            return self.values[0]

    def evaluate(self, stack):
        if self.output_value:
            stack.add_call(self, self)
            to_r = self.output_value.evaluate()
            stack.close_call()
            return to_r
        else:
            return to_r

    def get_value(self, value, stack):
        ""
        Crea la stack call e prende il proprio valore.
        ""
        stack.add_call(self, self)
        to_r = stack.get_variable(value)
        stack.close_call()
        return to_r

    def update(self, struct, stack):
        for element in struct.values:
            self.update_element(element, stack)

    def update_element(self, el, stack):
        ""
        Aggiunge un elemento a se stesso.
        I value finiscono sui TypeDef con solo il tipo,
        gli output danno il valore,
        i Set aggiornano vecchi valori Set oppure
        trasformano un Set in un TypeDef
        """
        # TODO: REVIEW
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
            cant_accept(el)""

    def __setitem__(self, el, value):
        for element in self.values:
            if isinstance(element, Set):
                if element.target.kws[-1].value == el:
                    if element.target.kws[0].value == 'code':
                        continue
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
"""
