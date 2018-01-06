from . import nydict


def nystr(string: str):
    return nydict.Nydict((('py_string', string),))


def nyint(integer: int):
    return nydict.Nydict((('py_int', integer),))
