class NyloObject:
    
    def __init__(self, *args):
        self.data = list(args)
    
    def __eq__(self, other):
        if not isinstance(other, NyloObject): 
            return None
        return self.data == other.data
    
    def __getitem__(self, key_to_get):
        for key, value in self.data:
            if key == key_to_get: return value
        raise IndexError("Key "+str(key_to_get)+
                         " can't be found in object "+
                         str(self))

    def __contains__(self, key_to_search):
        return any(key == key_to_search for
                   key, value in self.data)
    
    def __setitem__(self, key_to_set, value_to_set):
        for couple in self.data:
            if couple[0] == key_to_set:
                couple[1] = value_to_set
                return
        self.data.add([key_to_set, value_to_set])
        
    def __repr__(self):
        if 'python_string' in self: 
            return str(self['python_string'])
        if 'python_integer' in self:
            return str(self['python_integer'])
        if NyloObject(['python_integer', 0]) in self:
            return str([v for i, v in self.data])
        return ('{'+
            ', '.join(str(key)+': '+str(value)
                        for key, value in self.data
                        if value != NyloObject())+
                '}')
    
    def __add__(self, value):
        return self.data +value.data
    
    def add(self, value):
        self.data += value.data
