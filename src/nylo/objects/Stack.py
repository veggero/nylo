from nylo.objects.struct.Struct import Struct

class Stack(list):
    
    def __init__(self, elements=[Struct()]):
        list.__init__(self, elements)
    
    def __getitem__(self, value):
        if isinstance(value, (int, slice)): 
            return list.__getitem__(self, value)
        return self[-1].getitem(value, self)
    
    def __contains__(self, value):
        return value in self[-1]

    def __enter__(*args): pass
    
    def __exit__(self, *args): self.pop()
    
    def __call__(self, value):
        newvalue = Struct(self[-1].value.copy())
        newvalue.update(value, self)
        self.append(newvalue)
        return self
