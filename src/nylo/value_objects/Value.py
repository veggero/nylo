import copy

from nylo.exceptions import unx_char
from nylo.base_objects.Token import Token

class Value(Token):
    
    def parse(self, reader):

        from nylo.syntax_objects.Keyword import Keyword
        from nylo.syntax_objects.Symbol import Symbol
        from nylo.syntax_objects.SymbolOperation import SymbolOperation
        from nylo.struct_objects.Block import Block
        from nylo.struct_objects.Struct import Struct
        from nylo.value_objects.NumStr import Number, String
        from nylo.derived_objects.syntax_unrelated_objects import Call, Get
        from nylo.derived_objects.python_linked_objects import ValueLayer
        
        if reader.any_starts_with(Keyword.starts):
            kw = Keyword(reader)
            if reader.any_starts_with(Struct.starts):
                struct = Struct(reader)
                self.value = Call(kw, struct)
            else:
                self.value = kw
        
        elif reader.any_starts_with(Block.starts):
            self.value = Block(reader)
        
        elif reader.any_starts_with(Number.starts):
            self.value = Number(reader)
        
        elif reader.any_starts_with(String.starts):
            self.value = String(reader)
        
        elif reader.any_starts_with(Struct.starts):
            self.value = Struct(reader)
            
        elif reader.read() == '\0':
            self.value = ValueLayer(None)
            return
            
        else: unx_char(reader.read())
        
        if reader.read() == '[':
            reader.move()
            to_get = Value(reader)
            assert reader.read() == ']'
            reader.move()
            self.value = Get(copy.copy(self), to_get)
            
        if reader.any_starts_with(Symbol.starts):
            symb = Symbol(reader, reader.any_starts_with(Symbol.starts))
            after = Value(reader)
            self.value = SymbolOperation(copy.copy(self), symb, after)
            
    def evaluate(self, stack):
        return self.value.evaluate(stack)
