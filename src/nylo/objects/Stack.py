class Stack(list):
    
    def __getitem__(self, value):
        if isinstance(value, int): return list.__getitem__(self, value)
        if value in self[0]: return self[0].getitem(value, self)
        for element in reversed(self):
            if value in element: return element.getitem(value, self)
        raise NameError("Name '%s' is not defined" % value)
