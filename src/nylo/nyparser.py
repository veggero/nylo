import string
from typing import Tuple

from . import new
from . import nydef

parse_variable = None
parse_curly_braces = None
parse_inline_comment = None
parse_multiline_comment = None
parse_exa = None
parse_round_braces = None
parse_square_braces = None

def parse_until(code: str, index: int, end_character: str):
    parsed_objects_sectors = [[]]
    while code[index] != end_character:
        parsed_object, index = parse_element(code, index)
        if parsed_object in nydef.symbols: 
            parsed_objects_sectors.extend((parsed_object, []))
        elif parsed_object: parsed_objects_sectors[-1].append(parsed_object)
    parsed_objects = replace_symbols(parsed_objects_sectors)
    return new.nylist(parsed_objects)


def parse_element(code: str, index: int) -> Tuple[object, int]:
    for possible_starts in right_parser_by_start:
        if any(code.startswith(start, index) for start in possible_starts):
            parsed_object, new_index = \
                right_parser_by_start[possible_starts](code, index)
            return parsed_object, new_index
    if code[index] in nydef.symbols: return code[index], index+1


def parse_string(code: str, index: int) -> Tuple[object, int]:
    end_character, start_character_index = code[index], index
    index += 1
    while code[index] != end_character:
        index += 1
        # TODO, if EOF should raise exception
    string = code[start_character_index + 1: index]
    string_object = new.nystr(string)
    index += 1
    return string_object, index


def parse_number(code: str, index: int) -> Tuple[object, int]:
    start_index = index
    while code[index] in string.digits + '.':
        if code[index] == '.' and '.' in code[start_index:index]: break
        index += 1
    str_number = code[start_index:index]
    if '.' in str_number: number = new.nyfloat(float(str_number))
    else: number = new.nyint(int(str_number))
    return number, index

def parse_variable(code: str, index: int) -> Tuple[object, int]:
    start_index = index
    while code[index] in string.ascii_letters + '_': index += 1
    variable_name = code[start_index:index]
    if variable_name in nydef.symbols: return variable_name, index
    variable_object = new.nyvar(variable_name)
    return variable_object, index


def replace_symbols(sectors):
    for symbol in nydef.symbols:
        while symbol in sectors:
            sectors = replace_symbol(symbol, sectors)
    return sectors[0]


def replace_symbol(symbol, sectors):
    symbol_index = sectors.index(symbol) - 1
    arguments = get_value_from_sector(sectors, symbol_index, 
                                      unary=(symbol in nydef.unary_symbols))
    while len(sectors) > symbol_index and sectors[symbol_index] == symbol:
        del sectors[symbol_index]
        arguments += get_value_from_sector(sectors, symbol_index)
    sectors.insert(symbol_index, 
                    [new.nyvar(nydef.function_by_symbol[symbol]),
                    new.nylist(arguments)])
    return sectors

def get_value_from_sector(sectors, index, unary=False):
    value = []
    if len(sectors[index]) == 0 and not unary: 
            value = [new.nyvar('implicit')]
    elif len(sectors[index]) == 1: value = [sectors[index][0]]
    elif len(sectors[index]) > 1: value = [new.nycode(sectors[index])]
    del sectors[index]
    return value

right_parser_by_start = {
        (tuple(string.digits) +
         tuple("." + digit for digit in string.digits)): parse_number,
        ('['): parse_square_braces,
        ("'", '"'): parse_string,
        string.ascii_letters: parse_variable,
        ('{',): parse_curly_braces,
        ('//',): parse_inline_comment,
        ('/*',): parse_multiline_comment,
        ('#',): parse_exa,
        ('(',): parse_round_braces
}
