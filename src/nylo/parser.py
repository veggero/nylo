"""
This module implement the parsers for Nylo.
All the parsers have the code as input. The code is a list
of characters. Parser will pop out the values they parse, and
return the parsed value.
"""


from itertools import takewhile
from functools import partial
from collections import deque
from typing import Union
from string import ascii_lowercase as letters, digits


from exceptions import NySyntaxError
from interpreter import Integer, Float, String, Variable


def anyvalue(code: list):
    """
    anyvalue ::= number | string | variable
    >>> code = [*'«strakas»19sailors']
    >>> anyvalue(code)
    'strakas'
    >>> anyvalue(code)
    19
    >>> anyvalue(code)
    $sailors
    >>> anyvalue([*'~'])
    Traceback (most recent call last):
      ...
    exceptions.NySyntaxError: Unexpected character found while parsing.
    >>> anyvalue([])
    Traceback (most recent call last):
      ...
    exceptions.NySyntaxError: Unexpected EOF while parsing.
    """
    try:
        return next(f(code) for v, f in {digits + '.': number,
            '"\'«': string, letters + '_': variable}.items() if code[0] in v)
    except StopIteration:
        raise NySyntaxError('Unexpected character found while parsing.')
    except IndexError:
        raise NySyntaxError('Unexpected EOF while parsing.')
    
    
def whitespace(code: list, indent=[0]):
    r"""
    >>> code = [*'    ']
    >>> whitespace(code)
    >>> code
    []
    >>> whitespace([*" \t \t 3"])
    Traceback (most recent call last):
      ...
    exceptions.NySyntaxError: Unexpected tab while parsing whitespace.
    >>> code = []
    >>> whitespace(code)
    >>> code
    []
    >>> code = [*"\n 3"]
    >>> whitespace(code, [0])
    >>> code
    ['(', '3']
    >>> code = [*"\n\t3"]
    >>> whitespace(code, [1])
    >>> code
    [',', '3']
    >>> code = [*"\n 3"]
    >>> whitespace(code, [2])
    >>> code
    [')', '3']
    >>> code = [*"\n\t3"]
    >>> whitespace(code, [3])
    >>> code
    [')', ')', '3']
    >>> code = [*'\n']
    >>> whitespace(code, [4])
    >>> code
    [')', ')', ')', ')']
    >>> code = [*"\n\t\t\t\n\t3"]
    >>> whitespace(code, [2])
    >>> code
    [')', '3']
    """
    deque(map(code.remove, [*takewhile(lambda x: x == ' ', code)]))
    if code and code[0] == '\t':
        raise NySyntaxError("Unexpected tab while parsing whitespace.")
    if code and code[0] == '\n':
        while code and code[0] == '\n':
            code.pop(0)
            newindent = [*takewhile(lambda x: x in ' \t', code)]
            deque(map(code.remove, newindent))
        delta = len(newindent) - indent[0]
        deque(map(partial(code.insert, 0), 
                    (')' * -delta * (delta < 0) +
                    ',' * (delta == 0) +
                    '(' * delta * (delta > 0))))

def number(code: list) -> Union[Integer, Float]:
    """
    number ::= (1-9)* ["." (1-9)*]
    >>> number([*'123'])
    123
    >>> number([*'1 2 3'])
    1
    >>> number([*'42.2.'])
    42.2
    >>> number([])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Non-numeric character while parsing number.
    >>> number([*'caffe'])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Non-numeric character while parsing number.
    """
    value: str = ''.join(takewhile(str.isdigit, code))
    if not value:
        raise NySyntaxError('Non-numeric character while parsing number.')
    if code[len(value):][:1] == ['.']:
        value += ('.' + ''.join(takewhile(str.isdigit, code[len(value)+1:])))
    deque(map(code.remove, value))
    return (Float if '.' in value else Integer)(value)


def string(code: list) -> String:
    """
    string ::= '"' .* '"' | "'" .* "'" | "«" .* "»"
    >>> string([*"'spam'"])
    'spam'
    >>> string([*'"foo" "bar"'])
    'foo'
    >>> string([*'«42»!'])
    '42'
    >>> string([*'caffe'])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Non-string character while parsing string.
    >>> string([])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Non-string character while parsing string.
    >>> string([*'«this has no end'])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Found EOF while parsing for string end.
    """
    if not (code and code[0] in '\'"«'):
        raise NySyntaxError('Non-string character while parsing string.')
    try:
        return String(''.join(iter(partial(code.pop, 0),
            {"'": "'", '"': '"', '«': '»'}[code.pop(0)])))
    except IndexError:
        raise NySyntaxError('Found EOF while parsing for string end.')

def variable(code: list) -> Variable:
    """
    variable ::= (a-Z_) (a-Z_')*
    >>> variable([*'tau'])
    $tau
    >>> variable([*"k_9' leela"])
    $k_9'
    >>> variable([*'c8e.'])
    $c8e
    >>> variable([*'32'])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Non-variable character while parsing variable.
    >>> variable([])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Non-variable character while parsing variable.
    """
    if not (code and code[0] in letters + '_'):
        raise NySyntaxError('Non-variable character while parsing variable.')
    value = ''.join(takewhile(lambda x: x in letters + digits + "_'", code))
    deque(map(code.remove, value))
    return Variable(value)
