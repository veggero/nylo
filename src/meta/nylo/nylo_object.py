class NyloObject:

    def __init__(self, *args):
        self.data = list(args)
        self.hashy = hash(tuple(tuple(x) for x in self.data))

    def __add__(self, other):
        return NyloObject(*[[key, self[key]]
                            if not key in other
                            else [key, other[key]]
                            for key, value in self.data + other.data])

    def __sub__(self, other):
        return NyloObject(*[[a, b] for a, b in self if not a in other])

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __getitem__(self, key_to_get):
        for key, value in self.data:
            if key == key_to_get:
                return value
        raise IndexError("Key " + str(key_to_get) +
                         " can't be found in object " +
                         str(self))

    def __contains__(self, key_to_search):
        return any(key == key_to_search for
                   key, value in self.data)

    def __setitem__(self, key_to_set, value_to_set):
        for couple in self.data:
            if couple[0] == key_to_set:
                couple[1] = value_to_set
                return
        self.data.append([key_to_set, value_to_set])

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        # return str(id(self))[-4:]+'['+', '.join(repr(k)+': '+repr(v) for k, v
        # in self)+']'
        if 'python_string' in self:
            return str(self['python_string'])
        if 'python_integer' in self:
            return str(self['python_integer'])
        if NyloObject(['python_integer', 0]) in self:
            return str([v for i, v in self.data])
        return ('{' +
                ', '.join(str(key) + ': ' + str(value)
                          for key, value in self.data
                          if value != NyloObject()) +
                '}')

    def add(self, other):
        self.data = [[key, self[key]]
                     if not key in other
                     else [key, other[key]]
                     for key, value in self.data + other.data]

    def append(self, thing):
        i = 0
        while NyloObject(['python_integer', i]) in self:
            i += 1
        self.add(NyloObject([NyloObject(['python_integer', i]), thing]))

    def __hash__(self):
        return self.hashy
