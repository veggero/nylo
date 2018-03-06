def name_not_defined(name): 
    raise NameError("name {n} is not defined".format(n=name))

def cant_call(name):
    raise TypeError("object '{n}' is not callable".format(n=name))

def need_comma(): 
    raise SyntaxError('struct elements should be separated by comma')

def eof_on_scan(): 
    raise SyntaxError('EOF while scanning')

def file_not_over(): 
    raise SyntaxError('unexpected end of code')

def cant_return(s):
    raise Exception('structure {s} has no value to return'.format(s=s))

def cant_accept(value):
    raise TypeError("can't accept value {v}".format(v=value))

def cant_assign():
    raise SyntaxError("can't assign to literal")

def unx_char(char):
    raise SyntaxError("unexpected character '{c}'".format(c=char))

def cant_eval(obj):
    raise TypeError("can't call with value {o}".format(o=obj))
