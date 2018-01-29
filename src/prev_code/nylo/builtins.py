from . import new

def overloadedcall(overloadeds, arguments):
    functions = new.pylist(overloadeds[new.nyvar('overloaded_functions')])
    
    for function in reversed(functions):
        condition = function[new.nyvar('arguments')]
        
        if is_instance(condition, nylo['code']):
            condition = pycall(nylo['struct'], condition)
        
        if is_instance(arguments, condition):
            if is_instance(function, nylo['pyfun']):
                return pycall(function, arguments)
            else:
                return call(function, arguments)
            

def struct(variables):
    pass

callargs = None
nylo = {
    
    # BUILTIN TYPES
    
    'int': new.nylist(['py_int']),
    'str': new.nylist(['py_str']),
    'float': new.nylist(['py_float']),
    'pyfun': new.nylist(['python_function', new.nyvar('args')]),
    'overloaded_fun': new.nylist([new.nyvar('overloaded_functions')]),
    'var': new.nylist([new.nystr('label')]),
    'list': new.nylist([new.nyint(0)]),
    'code': new.nylist([new.nyvar('behaviour')]),
    'codeblock': new.nylist([new.nyvar('codelines')]),
    'fun': new.nylist([new.nyvar('function_code'), new.nyvar('arguments')]),
    'reference': new.nylist([new.nyvar('path')]),
    
    
    # NYLO RELATED FUNCTIONS - DO NOT TOUCH
    
    'call': new.nyoverloaded(
        
        new.nypyfun(callargs, new.nylist([new.nyvar('variables', [new.nyvar('list'), new.nyvar('var')])])),
        
        new.nypyfun(call, new.nylist([new.nyvar('function', [new.nyvar('fun')]),
                                               new.nyvar('arguments')])),
        
        new.nypyfun(pycall, new.nylist([new.nyvar('pyfunction', [new.nyvar('pyfun')]),
                                                 new.nyvar('arguments')])),
        
        new.nypyfun(overloadedcall, new.nylist([new.nyvar('overloadeds', [new.nyvar('overloaded_fun')]),
                                                         new.nyvar('arguments')])),
    ),
        
    'struct': new.nypyfun(struct, new.nylist([new.nyvar('variables', [new.nyvar('list'), new.nyvar('var')])]))
    
}
