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
        print(self.traceback)
