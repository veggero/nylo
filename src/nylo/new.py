from . import nydict


def nystr(string: str):
    return nydict.Nydict((('py_str', string),))


def nyint(integer: int):
    return nydict.Nydict((('py_int', integer),))


def nyfloat(floating: float):
    return nydict.Nydict((('py_float', floating),))


def nyvar(variable_name: str, variable_types=False, variable_condition=False, default=False):
    nyvar = nydict.Nydict(((nystr('label'), nystr(variable_name)),))
    if variable_types: nyvar = nyvar(nystr('types'), variable_types)
    if variable_condition: nyvar = nyvar(nystr('condition'), variable_condition)
    if default: nyvar = nyvar(nystr('default'), default)
    return nyvar


def nylist(elements):
    return nydict.Nydict((nyint(index), value) for index, value in enumerate(elements))


def nycode(elements):
    return nydict.Nydict(((nystr('behaviour'), nylist(elements)),))

def nymultiline_code(lines):
    return nydict.Nydict(((nystr('codelines'), nylist(lines)),))

def pylist(nylist):
    return [nylist[index] for index in (nyint(k) for k in range(len(nylist)))]
