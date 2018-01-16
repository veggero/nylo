from . import builtins
from . import new

nylo = {
    
    # BUILTIN TYPES
    
    'int': new.nylist(['py_int']),
    'str': new.nylist(['py_str']),
    'float': new.nylist(['py_float']),
    'pyfun': new.nylist(['python_function', new.nyvar('args')]),
    'overloaded_fun': new.nylist([new.nyvar('overloaded_functions')]),
    'var': new.nylist([new.nystr('label')]),
    'list': new.nylist([new.nyint(0)]),
    'code': new.nylist[new.nyvar('behaviour')],
    'codeblock': new.nylist([new.nyvar('codelines')]),
    'fun': new.nylist([new.nyvar('function_code'), new.nyvar('arguments')]),
    'reference': new.nylist([new.nyvar('path')]),
    
    
    # NYLO RELATED FUNCTIONS - DO NOT TOUCH
    
    'call': new.nyoverloaded(
        
        new.nypyfun(builtins.callargs, new.nylist([new.var('variables', [new.var('list'), new.var('var')])])),
        
        new.nypyfun(builtins.call, new.nylist([new.var('function', [new.var('fun')]),
                                               new.var('arguments')])),
        
        new.nypyfun(builtins.pycall, new.nylist([new.var('pyfunction', [new.var('pyfun')]),
                                                 new.var('arguments')])),
        
        new.nypyfun(builtins.overloadedcall, new.nylist([new.var('overloadeds', [new.var('overloaded_fun')]),
                                                         new.var('arguments')])),
    )
    
}
