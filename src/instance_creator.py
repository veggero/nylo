import nylo_object as no

nynone = no.NyloObject()

def codelines(lines): 
    return no.NyloObject([variable('codelines'), nylist(lines)])

def string(pystr):
    return no.NyloObject(['python_string', pystr])

def integer(pyint):
    return no.NyloObject(['python_integer', pyint])

def floating(pyfloat):
    return no.NyloObject(['python_floating_point', pyfloat])

def code(objects):
    return no.NyloObject([variable('behaviour'), nylist(objects)])

def path(gets):
    return no.NyloObject([variable('path'), nylist(gets)])

def struct(variables):
    return no.NyloObject([variable('struct'), nylist(variables)])

def function(code, args):
    return no.NyloObject([variable('function_code'), code],
                         [variable('arguments'), args])

def variable(name, motherclass=nynone, condition=nynone, default=nynone):
    return no.NyloObject([string('variable_name'), name],
                         [string('class'), motherclass],
                         [string('condition'), condition],
                         [string('default'), default])

def overload(functions):
    return no.NyloObject([variable('overloaded_functions'), nylist(functions)])

def nylist(pylist):
    return no.NyloObject(*[[integer(i), value] for i, value in enumerate(pylist)])
