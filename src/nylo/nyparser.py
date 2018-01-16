import string
from typing import Tuple, List

from . import new
from . import nydef
from . import nydict


def parse(code):
    code += '\n'
    parsed, index, indent = parse_multiline_code(code)
    return parsed


def parse_multiline_code(code: str, index=0, prev_indent=-1, indent=0) -> Tuple[object, int, int]:
    lines = []
    while indent > prev_indent:
        line, index = parse_until(code, index, ['\n', ':\n'])
        if code[index] == '\n': index += 1
        elif code[index] == ':': index += 2
        lines.append(line)
        if index == len(code): 
            indent = -1
            break
        next_line_indent, index = get_indentation(code, index)
        if next_line_indent > indent:
            indented_code, index, indent = parse_multiline_code(code, index, indent, next_line_indent)
            lines[-1] = new.nycode(new.pylist(lines[-1][new.nyvar('behaviour')]) + [indented_code])
        else: indent = next_line_indent
    return new.nymultiline_code(lines), index, indent
        

def get_indentation(code: str, index: int) -> Tuple[int, int]:
    start_index = index
    while code[index] in ' \t\n':
        while code[index] == '\n': index += 1
        start_index = index
        while code[index] in ' \t': index += 1
    return index - start_index, index


def parse_until(code: str, index: int, endings: List[str]):
    parsed_objects_sectors = [[]]
    while not any(code.startswith(end_char, index) for end_char in endings):
        parsed_object, index = parse_element(code, index)
        if parsed_object in nydef.symbols: 
            parsed_objects_sectors.extend((parsed_object, []))
        elif parsed_object: parsed_objects_sectors[-1].append(parsed_object)
        if index == len(code): 
            raise Exception("Parsing error: end of file while searching for \""+'" or "'.join(endings)+'"')
    parsed_objects = replace_symbols(parsed_objects_sectors)
    return new.nycode(parsed_objects), index


def parse_round_braces(code: str, index: int) -> Tuple[object, int]:
    index += 1
    parsed, index = parse_until(code, index, [':', ')'])
    if code[index] == ':':
        index += 1
        keys, values = [parsed], []
        value, index = parse_until(code, index, [',', ')'])
        values.append(value)
        while code[index] != ')':
            index += 1
            key, index = parse_until(code, index, [':'])
            index += 1
            value, index = parse_until(code, index, [',', ')'])
            keys.append(key)
            values.append(value)
        parsed = nydict.Nydict(zip(keys, values))
    return parsed, index + 1


def parse_curly_braces(code: str, index: int) -> Tuple[object, int]:
    index += 1
    first_argument, index = parse_until(code, index, ['}', '|'])
    if code[index] == '|':
        second_argument, index = parse_until(code, index + 1, ['}'])
        return new.nyfun(second_argument, first_argument), index + 1
    return new.nyfun(first_argument), index + 1


def parse_square_braces(code: str, index: int) -> Tuple[object, int]:
    index += 1
    labels = []
    while code[index] != ']':
        if code[index] == '[':
            index += 1
            parsed, index = parse_until(code, index, [']'])
            index += 1
            labels.append(parsed)
        else:
            parsed, index = parse_element(code, index)
            if parsed: labels.append(parsed)
        if index == len(code): raise Exception('Parsing error: end of file while searching for "]"')
    index += 1
    return new.reference(labels), index


def parse_element(code: str, index: int) -> Tuple[object, int]:
    for possible_starts in right_parser_by_start:
        if any(code.startswith(start, index) for start in possible_starts):
            parsed_object, new_index = \
                right_parser_by_start[possible_starts](code, index)
            return parsed_object, new_index
    raise Exception('Parsing error: unexpected character "'+str(code[index])+'"')

def parse_inline_comment(code: str, index: int) -> Tuple[type(None), int]:
    while code[index] != '\n': index += 1
    return None, index + 1


def parse_multiline_comment(code: str, index: int) -> Tuple[type(None), int]:
    while code[index:index+2] != '*/': index += 1
    return None, index + 2


def parse_whitespace(code: str, index: int) -> Tuple[type(None), int]:
    return None, index + 1


def parse_prevent_new_line(code: str, index: int) -> Tuple[type(None), int]:
    return None, index + 2


def parse_exa(code: str, index: int) -> Tuple[object, int]:
    index += 1
    start_index = index
    while code[index] in string.hexdigits: index += 1
    return new.nyint(int(code[start_index:index], base=16)), index

def parse_string(code: str, index: int) -> Tuple[object, int]:
    end_character, start_character_index = code[index], index
    index += 1
    while code[index] != end_character:
        index += 1
        if index == len(code): raise Exception("Parsing error: unclosed string.")
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


def replace_symbols(sectors: list):
    for symbol in nydef.symbols:
        while symbol in sectors:
            sectors = replace_symbol(symbol, sectors)
    return sectors[0]


def replace_symbol(symbol: str, sectors: list) -> list:
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

def get_value_from_sector(sectors: list, index: int, unary=False):
    value = []
    if len(sectors[index]) == 0 and not unary: 
        value = [new.nyvar('implicit')]
    elif len(sectors[index]) == 1: value = [sectors[index][0]]
    elif len(sectors[index]) > 1: value = [new.nycode(sectors[index])]
    del sectors[index]
    return value

def parse_symbol(code: str, index: int) -> Tuple[str, str]:
    if code[index:index+2] in nydef.symbols:
        return code[index:index+2], index+2
    else:
        return code[index], index+1

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
        ('(',): parse_round_braces,
        tuple(nydef.symbols): parse_symbol,
        (' ', '\t', '\n',): parse_whitespace,
        ('\\n'): parse_prevent_new_line,
}
        
        
print(parse("""1+1"""))
