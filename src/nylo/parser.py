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
from interpreter import Integer, Float, Text, Variable, Struct, Op


def structure(code: list):
    """
    struct ::= "(" ((value | value ":" value) [","])* ("->" value)? ")"
    """
    if not code or not code[0] == '(':
        raise NySyntaxError('Non-structure character while parsing structure.')
    del code[0]
    dirs, atoms, rvalue, hascomma = {}, [], None, False
    while code[0] != ')':
        if code and code[0] == ',':
            del code[0]
            hascomma = True
            whitespace(code)
            if not code:
                raise NySyntaxError('Unexpected EOF while parsing.')
            continue
        if ''.join(code).startswith('->'):
            del code[:2]
            rvalue = sentence(code)
            break
        value = sentence(code)
        if not code:
            raise NySyntaxError('Unexpected EOF while parsing.')
        if code[0] == ':':
            del code[0]
            key, value = value, sentence(code)
            dirs[key] = value
        else:
            atoms.append(value)
    if not code:
        raise NySyntaxError('Unexpected EOF while parsing.')
    elif code[0] != ')':
        raise NySyntaxError('Missing ")" after "->" value.')
    del code[0]
    if not dirs and not rvalue and len(atoms) == 1 and not hascomma:
        return atoms[0]
    return Struct(dirs, tuple(atoms), rvalue)


def sentence(code: list):
    """
    sentence ::= anyvalue? symbol? sentence?
    """
    if not code:
        raise NySyntaxError('Unexpected EOF while parsing.')
    value, symbol, sentence = None, None, None
    if code[0] in (el for l in parsers.keys() for el in l):
        value = anyvalue(code)
        #TODO


def anyvalue(code: list):
    """
    anyvalue ::= number | string | variable
    """
    whitespace(code)
    try:
        value = next(f(code) for v, f in parsers.items() if code[0] in v)
    except StopIteration:
        raise NySyntaxError('Unexpected character "%s" found while parsing.' % repr(code[0]))
    except IndexError:
        raise NySyntaxError('Unexpected EOF while parsing.')
    whitespace(code)
    return value

        
def whitespace(code: list, indent=[0]):
    deque(map(code.remove, [*takewhile(lambda x: x == ' ', code)]))
    if code and code[0] == '\t':
        raise NySyntaxError("Unexpected tab while parsing whitespace.")
    if code and code[0] == '\n':
        while code and code[0] == '\n':
            del code[0]
            newindent = [*takewhile(lambda x: x in ' \t', code)]
            del code[:len(newindent)]
        delta = len(newindent) - indent[0]
        deque(map(partial(code.insert, 0), 
                    (')' * -delta * (delta < 0) +
                    ',' * (delta == 0) +
                    '(' * delta * (delta > 0))))

def number(code: list) -> Union[Integer, Float]:
    """
    number ::= (1-9)* ("." (1-9)*)?
    """
    value: str = ''.join(takewhile(str.isdigit, code))
    if not value:
        raise NySyntaxError('Non-numeric character while parsing number.')
    if code[len(value):][:1] == ['.']:
        value += ('.' + ''.join(takewhile(str.isdigit, code[len(value)+1:])))
    del code[:len(value)]
    return (Float if '.' in value else Integer)(value)


def text(code: list) -> Text:
    """
    text ::= '"' .* '"' | "'" .* "'" | "«" .* "»"
    """
    if not (code and code[0] in '\'"«'):
        raise NySyntaxError('Non-text character while parsing text.')
    try:
        return Text(''.join(iter(partial(code.pop, 0),
            {"'": "'", '"': '"', '«': '»'}[code.pop(0)])))
    except IndexError:
        raise NySyntaxError('Found EOF while parsing for text end.')

def variable(code: list) -> Variable:
    """
    variable ::= (a-Z_) (a-Z_')*
    """
    if not (code and code[0] in letters + '_'):
        raise NySyntaxError('Non-variable character while parsing variable.')
    value = ''.join(takewhile(lambda x: x in letters + digits + "_'", code))
    del code[:len(value)]
    return Variable(value)


symbols_priority = (
    ('|',), ('and ', 'or ', 'xor '),
    ('=', '!=', '>=', '<=', 'in ', '>', '<'),
    ('..', '%'), ('+', '-', '&'),
    ('*', '/'), ('^', '+-'), ('.',))


symbols = tuple(sorted((f for a in symbols_priority for f in a),
                    key=len, reverse=True))


parsers = {digits + '.': number,
            '"\'«': text, 
            letters + '_': variable,
            '(': structure,}
