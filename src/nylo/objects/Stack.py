class Stack(list):
    
    def __getitem__(self, value):
        if isinstance(value, (int, slice)): 
            return list.__getitem__(self, value)
        if value in self[0]: return self[0].getitem(value, self)
        for element in reversed(self[1:]):
            if value in element: 
                return element.getitem(value, self)
        raise NameError("Name '%s' is not defined" % value)

    def __enter__(*args): pass
    
    def __exit__(self, *args): self.pop()
    
    def __call__(self, value):
        self.append(value)
        return self
