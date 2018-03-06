from nylo.base_objects.Token import Token

class Block(Token):
    
    starts = ['{']
    ends = ['}']
    
    def parse(self, reader):
        
        from nylo.value_objects.Value import Value
        
        self.values = []
        reader.move()
        
        while not reader.read() in self.ends:
            self.values.append(Value(reader))
            if reader.read() == '\0': reader.move()
            
        reader.move()
        
    def evaluate(self, stack):
        stack.add_call(self)
        stack[-1]['_self'] = None
        for val in self.values: val.evaluate(stack)
        to_return = stack[-1]['_self']
        stack.close_call()
        return to_return
