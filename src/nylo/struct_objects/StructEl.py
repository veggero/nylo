import copy

from nylo.base_objects.Token import Token
from nylo.derived_objects.syntax_unrelated_objects import Set, TypeDef, Output
from nylo.value_objects.Value import Value
from nylo.syntax_objects.Keyword import Keyword

class StructEl(Token):

    """
    TODO: CHECK AND REWRITE
    def parse(self, reader):
        if reader.any_starts_with(Keyword.starts): self.parse_keyword(reader)
        elif reader.starts_with('<-'): self.parse_single_set(reader)
        else: self.value = Value(reader)
        
    def parse_keyword(self, reader):
        before_reader = copy.copy(reader)
        kws = [Keyword(reader)]
        
        while reader.any_starts_with(Keyword.starts):
            kws.append(Keyword(reader))
            
        if reader.read() == ':': 
            self.parse_set(reader, kws)
            return
                
        if reader.starts_with('->'): self.parse_output(reader, kws[-1])
        
        else:
            self.value = TypeDef(kws)
            if not reader.read() in ',)':
                reader.goto(before_reader)
                self.value = Value(reader)
        
    def parse_single_set(self, reader):
        reader.move(2)
        kw = Keyword(reader)
        self.value = Set(TypeDef([kw]), kw)
        
    def parse_set(self, reader, kws):
        reader.move()
        self.value = Set(TypeDef(kws), Value(reader))
        
    def parse_output(self, reader, kw):
        reader.move(2)
        while reader.read() in ' \t\n': reader.move()
        if reader.any_starts_with(Keyword.starts): to_kw = Keyword(reader)
        else: to_kw = kw
        self.value = Output(kw, to_kw)
            
    def evaluate(self, stack): return self.value.evaluate(stack)
    """
