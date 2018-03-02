class Stack(list):

    def __init__(self, *args, **kwargs):
        self.traceback = []
        super().__init__(*args, **kwargs)
        
    def add_call(self, name):
        self.traceback.append(name)
        self.append({})
        
    def close_call(self):
        del self.traceback[-1]
        del self[-1]
        
    def show_traceback(self, Ex):
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
