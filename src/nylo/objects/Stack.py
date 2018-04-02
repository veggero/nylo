class Stack(list):
    
    def __getitem__(self, value):
        for element in reversed(self):
            if value in element: return element.getitem(value, self)
        raise NameError("Name '%s' is not defined" % value)
