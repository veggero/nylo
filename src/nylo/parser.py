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
from interpreter import Integer, Float, String, Variable, Struct


def structure(code: list):
    """
    struct ::= "(" ((value | value ":" value) [","])* ("->" value)? ")"
    >>> structure([*'(a:  1  5  :b   c  3  d  ->   5)'])
    {$a: 1, 5: $b}/($c, 3, $d)/5
    >>> structure([*'(  5  1:1, , 6:b 6 , 8 d: f  ,->10)'])
    {1: 1, 6: $b, $d: $f}/(5, 6, 8)/10
    >>> structure([*'(r g b)'])
    {}/($r, $g, $b)/None
    >>> structure([])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Non-structure character while parsing structure.
    >>> structure([*'(2, 4 b'])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Unexpected EOF while parsing.
    >>> structure([*'(2, 4 b,,'])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Unexpected EOF while parsing.
    >>> structure([*'(2, 4 b: '])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Unexpected EOF while parsing.
    >>> structure([*'(2, 4 -> 3'])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Unexpected EOF while parsing.
    >>> structure([*'(1, 4, -> 2 4)'])
    Traceback (innermost last):
      ....
    exceptions.NySyntaxError: Missing ")" after "->" value.
    """
    if not code or not code[0] == '(':
        raise NySyntaxError('Non-structure character while parsing structure.')
    code.pop(0)
    dirs, atoms, rvalue = {}, [], None
    while code[0] != ')':
        while code and code[0] == ',':
            code.pop(0)
            whitespace(code)
        if ''.join(code).startswith('->'):
            del code[:2]
            rvalue = anyvalue(code)
            break
        value = anyvalue(code)
        if not code:
            raise NySyntaxError('Unexpected EOF while parsing.')
        if code[0] == ':':
            code.pop(0)
            key, value = value, anyvalue(code)
            dirs[key] = value
        else:
            atoms.append(value)
    if not code:
        raise NySyntaxError('Unexpected EOF while parsing.')
    elif code[0] != ')':
        raise NySyntaxError('Missing ")" after "->" value.')
    code.pop(0)
    return Struct(dirs, tuple(atoms), rvalue)

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
    exceptions.NySyntaxError: Unexpected character "'~'" found while parsing.
    >>> anyvalue([])
    Traceback (most recent call last):
      ...
    exceptions.NySyntaxError: Unexpected EOF while parsing.
    """
    whitespace(code)
    try:
        value = next(f(code) for v, f in {digits + '.': number,
            '"\'«': string, letters + '_': variable,
            '(': structure}.items() if code[0] in v)
    except StopIteration:
        raise NySyntaxError('Unexpected character "%s" found while parsing.' % repr(code[0]))
    except IndexError:
        raise NySyntaxError('Unexpected EOF while parsing.')
    whitespace(code)
    return value
    
    
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
    number ::= (1-9)* ("." (1-9)*)?
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
