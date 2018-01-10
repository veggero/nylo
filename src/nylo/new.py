from . import nydict


def nystr(string: str):
    return nydict.Nydict((('py_str', string),))


def nyint(integer: int):
    return nydict.Nydict((('py_int', integer),))


def nyfloat(floating: float):
    return nydict.Nydict((('py_float', floating),))


def nyvar(variable_name: str, variable_types=False, variable_condition=False, default=False):
    nyvar = nydict.Nydict((('label', nystr(variable_name)),))
    if variable_types: nyvar = nyvar('types', variable_types)
    if variable_condition: nyvar = nyvar('condition', variable_condition)
    if default: nyvar = nyvar('default', default)
    return nyvar

def nylist(elements):
    return nydict.Nydict((nyint(index), value) for index, value in enumerate(elements))

def nycode(elements):
    return nydict.Nydict(((nystr('behaviour'), nylist(elements)),))
