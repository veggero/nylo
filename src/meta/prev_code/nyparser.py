import string
from typing import Tuple, List

import instance_creator as new
import definitions as nydef
import nylo_object as nydict
import exceptions as nyexp


def parse(code):
    code += '\n'
    parsed, index, indent = parse_multiline_code(code)
    return parsed


def parse_multiline_code(code: str, index=0, prev_indent=-1, 
                         indent=0) -> Tuple[nydict.NyloObject, int, int]:
    lines = []
    while indent > prev_indent:
        line, index = parse_until(code, index, ['\n', ':\n'])
        while index < len(code) and code[index] in ':\n': index += 1
        lines.append(line)
        if index == len(code): 
            indent = -1
            break
        next_line_indent, index = get_indentation(code, index)
        if next_line_indent > indent:
            indented_code, index, indent = \
                parse_multiline_code(code, index, indent, next_line_indent)
            lines[-1][new.variable('behaviour')].append(indented_code)
        else: indent = next_line_indent
        
    return new.codelines(lines), index, indent
        

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
        if isinstance(parsed_object, str) \
            and parsed_object in nydef.readable_symbols: 
            parsed_objects_sectors.extend((parsed_object, []))
        elif isinstance(parsed_object, list):
            parsed_objects_sectors = parsed_object
        elif parsed_object: parsed_objects_sectors[-1].append(parsed_object)
        if index == len(code): 
            raise nyexp.UnexpectedCharacter("Parsing error: end of file while searching for \""
                +'" or "'.join(endings)+'"')
    parsed_objects = replace_symbols(parsed_objects_sectors)
    return new.code(parsed_objects), index


def parse_element(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
    for possible_starts in right_parser_by_start:
        if any(code.startswith(start, index) for start in possible_starts):
            parsed_object, new_index = \
                right_parser_by_start[possible_starts](code, index)
            return parsed_object, new_index
    raise nyexp.UnexpectedCharacter('Parsing error: unexpected character "'+str(code[index])+'"')


def parse_round_braces(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
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
        parsed = new.evaluable_obj(zip(keys, values))
    return parsed, index + 1


def parse_square_braces(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
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
        if index == len(code): raise nyexp.UnexpectedCharacter('Parsing error: end of file while searching for "]"')
    index += 1
    return new.path(labels), index


def parse_curly_braces(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
    try:
        structure, index = parse_struct_until(code, index + 1, ['|', '}'])
        if code[index] == '}':
            return structure, index + 1
    except nyexp.StructSyntaxError:
        funct_code, index = parse_until(code, index + 1, ['}'])
        return new.function(funct_code, new.struct([])), index + 1
    function_code, index = parse_until(code, index + 1, ['}'])
    return new.function(new.codelines([function_code]), structure), index + 1


def parse_struct_until(code: str, index: int, 
                       endings: List[str]) -> Tuple[nydict.NyloObject, int]: #TODO Ma col cazzo che torni sta roba
    variables = [[]]
    while not any(code[index] == end for end in endings):
        last_element, index = parse_element(code, index)
        if last_element == None:
            pass
        elif last_element == ',':
            variables.append([])
        elif isinstance(last_element, str):
            raise nyexp.StructSyntaxError(str(last_element))
        elif (new.string('variable_name') in last_element
              or new.variable('path') in last_element):
            if len(variables[-1]) == 0:
                variables[-1].append(last_element)
            else:
                last_element[new.string('class')] = variables[-1][0]
                variables[-1][0] = last_element
        elif new.variable('function_code') in last_element:
            variables[-1][0][new.string('condition')] = last_element
        else:
            raise nyexp.StructSyntaxError(str(last_element))
    return new.struct([el[0] for el in variables]), index


def parse_assignation(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
    while code != -1 and code[index] != '\n': index -= 1
    parsed, index = parse_struct_until(code, index, [':'])
    return [[parsed], ':', []], index+1

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


def parse_exa(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
    index += 1
    start_index = index
    while code[index] in string.hexdigits: index += 1
    return new.integer(int(code[start_index:index], base=16)), index


def parse_string(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
    end_character, start_character_index = code[index], index
    index += 1
    while code[index] != end_character:
        index += 1
        if index == len(code): raise nyexp.StringSyntaxError("Parsing error: unclosed string.")
    string = code[start_character_index + 1: index]
    string_object = new.string(string)
    index += 1
    return string_object, index


def parse_number(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
    start_index = index
    while code[index] in string.digits + '.':
        if code[index] == '.' and '.' in code[start_index:index]: break
        index += 1
    str_number = code[start_index:index]
    if '.' in str_number: number = new.floating(float(str_number))
    else: number = new.integer(int(str_number))
    return number, index


def parse_variable(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
    start_index = index
    while code[index] in string.ascii_letters + '_': index += 1
    variable_name = code[start_index:index]
    if variable_name in nydef.all_symbols: return variable_name, index
    variable_objects = new.variable(variable_name)
    return variable_objects, index


def replace_symbols(sectors: list): 
    for importance_class in nydef.symbols_priority:
        for symbol in importance_class:
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
                    [new.variable(nydef.all_symbols[symbol]),
                    new.code(arguments)])
    return sectors


def get_value_from_sector(sectors: list, index: int, unary=False):
    value = []
    if len(sectors[index]) == 0 and not unary: 
        value = [new.variable('implicit')]
    elif len(sectors[index]) == 1: value = [sectors[index][0]]
    elif len(sectors[index]) > 1: value = [new.code(sectors[index])]
    del sectors[index]
    return value


def parse_symbol(code: str, index: int) -> Tuple[str, str]:
    if code[index:index+2] in nydef.all_symbols:
        return code[index:index+2], index+2
    else:
        return code[index], index+1


right_parser_by_start = {
        nydef.number_starts: parse_number, #OK
        nydef.square_brace_start: parse_square_braces, #OK
        nydef.string_starts: parse_string, #OK, \.* TODO
        nydef.variable_starts: parse_variable, #OK
        nydef.curly_braces_start: parse_curly_braces, #{int x:3} #TODO #riscrivere TODO
        nydef.inline_comment_start: parse_inline_comment, #OK
        nydef.multiline_comment_start: parse_multiline_comment, #OK
        nydef.exa_start: parse_exa, #OK
        nydef.round_braces_start: parse_round_braces, #OK
        tuple(nydef.readable_symbols): parse_symbol, #OK
        nydef.whitespaces: parse_whitespace, #OK
        nydef.prevent_new_line: parse_prevent_new_line, #OK
        nydef.assignation: parse_assignation,
}
