symbols = {'+', '-', '/', '*', ',', '&', 'and', 'or', '=', ': ', '.', '>', '<', 'is_a',  ':'}

symbols_parsing_order = [
    {'.'},
    {':'},
    {'*', '/'},
    {'+', '-'},
    {'&', 'and', 'or', '=', '<', '>', 'is_a'},
    {': ', ','}
    ]

unary_symbols = {'-'}

symbols_functions = {'+': 'sum',
                     '-': 'sub',
                     '/': 'div',
                     '*': 'mul',
                     ',': 'to_list',
                     '&': 'join',
                     'and': 'all',
                     'or': 'any',
                     '=': 'equals',
                     ': ': 'set',
                     '.': 'get_propriety',
                     '>': 'greater_than',
                     '<': 'less_than',
                     'is_a': 'is_instance',
                     ':': 'range'}

class nydict:
    """
    Nylo object is just a dict, but it needs to be hashable.
    Therefore I use tuples, but I create a new class to make
    it prettier (such as, dict-like declaration and dict get and
    assign functions)
    """
    def __init__(self, args):
        self.value = frozenset(args)
    
    def __eq__(x, y):
        try:
            return x.value == y.value
        except AttributeError:
            return False
    
    def __hash__(self):
        return hash(self.value)
    
    def __getitem__(self, key):
        """
        Get an item: nylo_obj(('age',16))['age'] --> 16
        """
        for couple in self.value:
            if couple[0] == key:
                return couple[1]
        raise IndexError("Key "+str(key)+" can't be found in nydict "+str(self)) # newfags can't avoid indexerror
    
    def __contains__(self, key):
        return any([couple[0]==key for couple in self.value])
            
    def __call__(self, key, value):
        """
        Set a value and return the new tupledict. nylo_obj(('age', 16))('age', 17) --> nylo_obj(('age', 17))
        """
        return [couple 
            if couple[0] != key
            else (couple[0], value)
            for couple in self.value]
    
    def __repr__(self):
        return '{'+', '.join([repr(son[0])+': '+repr(son[1]) for son in self.value])+'}'
