from nylo.base_objects.Token import Token

class Block(Token):
    
    starts = ['{']
    ends = ['}']
    
    def parse(self, reader):
        
        self.values = []
        self.condition = []
        reader.move()
        
        while not reader.read() in self.ends:
            self.values.append(Value(reader))
            self.condition.extend(self.values[-1].condition)
            
        reader.move()
        
    def evaluate(self, stack):
        stack.add_call(self)
        stack[-1]['_self'] = None
        for val in self.values:
            val.evaluate(stack)
        to_return = stack[-1]['_self']
        stack.close_call()
        return to_return
