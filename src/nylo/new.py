from . import nydict


def str(string):
    return nydict.Nydict((('py_string', string),))


def int(integer):
    return nydict.Nydict((('py_int', integer),))
