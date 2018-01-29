from . import nydict


DEBUG = True


def nystr(string: str):
    if DEBUG: return string
    return nydict.Nydict((('py_str', string),))


def nyint(integer: int):
    if DEBUG: return integer
    return nydict.Nydict((('py_int', integer),))


def nyfloat(floating: float):
    if DEBUG: return floating
    return nydict.Nydict((('py_float', floating),))


def nyvar(variable_name: str, variable_types=False, variable_condition=False, default=False):
    nyvar = nydict.Nydict(((nystr('label'), nystr(variable_name)),))
    if variable_types: nyvar = nyvar(nystr('types'), variable_types)
    if variable_condition: nyvar = nyvar(nystr('condition'), variable_condition)
    if default: nyvar = nyvar(nystr('default'), default)
    return nyvar


def nylist(elements):
    if DEBUG: return tuple(elements)
    return nydict.Nydict((nyint(index), value) for index, value in enumerate(elements))


def nycode(elements):
    return nydict.Nydict(((nyvar('behaviour'), nylist(elements)),))


def nymultiline_code(lines):
    return nydict.Nydict(((nyvar('codelines'), nylist(lines)),))


def pylist(nylist):
    return [nylist[index] for index in (nyint(k) for k in range(len(nylist)))]


def nyfun(code, args=nycode([])):
    return nydict.Nydict(((nyvar('function_code'), code), (nyvar('arguments'), args)))


def nypyfun(pyfun, args=nycode([])):
    return nydict.Nydict((('python_function', pyfun), (nyvar('arguments'), nylist(args))))


def nyoverloaded(funs):
    return nydict.Nydict(((nyvar('overloaded_functions'), nylist(funs)),))

    
def reference(labels):
    return nydict.Nydict(((nyvar('path'), nylist(labels)),))
