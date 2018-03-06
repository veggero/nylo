from nylo.exceptions import name_not_defined

class Stack(list):
    """
    The Stack is a list of variables dictionaries.
    A var dict can be either an actual dict or 
    a Struct element behaving so.
    This class manages reading variables,
    adding calls, traceback, etc.
    """

    def __init__(self, *args, **kwargs):
        "Initialize the Stack"
        self.traceback = []
        super().__init__(*args, **kwargs)
        
    def add_call(self, name, obj={}):
        "Add a new variable dict to the stack."
        self.traceback.append(name)
        self.append(obj)
        
    def close_call(self):
        "Remove the last dict of the stack."
        del self.traceback[-1]
        del self[-1]
        
    def get_variable(self, value):
        "Read a variable from the stack and returns its value."
        from nylo.struct_objects.Struct import Struct
        # Loop backward in the variable dicts to find
        # the most recent variable.
        for vardict in self[::-1]:
            if value in vardict:
                
                if isinstance(vardict, Struct): 
                    
                    if hasattr(vardict[value], 'evaluate'):
                        # If the var dict is a Struct, we need to
                        # evaluate the value if it's the first time,
                        # and set the new evalued value.
                        # This will avoid doing multiple times the
                        # same math.
                        struct_el_val = vardict[value].evaluate(self)
                        vardict[value] = struct_el_val
                        return struct_el_val
                        
                return vardict[value]
        name_not_defined(value)
        
    def show_traceback(self, Ex):
        """
        Show the traceback in the event of an exception.
        """
        if len(self.traceback):
            print('Traceback:')
            for t in self.traceback[::-1]:
                if hasattr(t, 'line'):
                    print('in {n} <@l{l} c{c}>'.format(n=repr(t),
                                             l=t.line,
                                             c=t.char))
                else: print('in '+repr(t))
        print("{c}: {e}".format(c=Ex.__class__.__name__,
                                e=str(Ex)))
        self.traceback = []
        while len(self) > 1: del self[1]
