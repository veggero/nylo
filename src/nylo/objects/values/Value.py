from nylo.objects.NyObject import NyObject

class Value(NyObject): 
    
    obj_types = {
        int: ('obj', 'value', 'num', 'int'),
        float: ('obj', 'value', 'num', 'float'),
        str: ('obj', 'value', 'num', 'str'),
        }

    def settype(self, types, stack):
        self.types = self.obj_types[type(self.value)]
        return self.types
