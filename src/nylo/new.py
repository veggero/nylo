import nydict

def new_str(string):
    return nydict.Nydict((('py_string', string),))


def new_int(integer):
    return nydict.Nydict((('py_int', integer),))
