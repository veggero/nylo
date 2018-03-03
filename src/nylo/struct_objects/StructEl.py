import copy

from nylo.base_objects.Token import Token

class StructEl(Token):

    def parse(self, reader):
        
        from nylo.derived_objects.syntax_unrelated_objects import (Set,
                                                                   TypeDef,
                                                                   Output)
        from nylo.value_objects.Value import Value
        from nylo.syntax_objects.Keyword import Keyword
        
        before_reader = copy.copy(reader)
        
        if reader.any_starts_with(Keyword.starts):
            kw = Keyword(reader)
            
            if reader.any_starts_with(Keyword.starts):
                kws = [kw]
                
                while reader.any_starts_with(Keyword.starts):
                    kws.append(Keyword(reader))
                    
                if reader.read() == ':':
                    reader.move()
                    val = Value(reader)
                    self.value = Set(TypeDef(kws), val)
                    return
                    
                elif reader.read() in ',)':
                    self.value = TypeDef(kws)
                    return
                    
            elif reader.starts_with('->'):
                reader.move(2)
                while reader.read() in ' \t\n': reader.move()
                if reader.any_starts_with(Keyword.starts):
                    to_kw = Keyword(reader)
                else:
                    to_kw = kw
                self.value = Output(kw, to_kw)
            
            else:
                reader.goto(before_reader)
                self.value = Value(reader)
            
        elif reader.starts_with('<-'):
            reader.move(2)
            kw = Keyword(reader)
            self.value = Set(TypeDef([kw]), kw)
            
        else:
            self.value = Value(reader)
            
    def evaluate(self, stack): return self.value.evaluate(stack)
