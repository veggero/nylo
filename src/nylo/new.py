from . import nydict


def nystr(string):
    return nydict.Nydict((('py_string', string),))


def nyint(integer):
    return nydict.Nydict((('py_int', integer),))
