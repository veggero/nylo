"""
Main Nylo file parser. Contains all the parser that act based on the
informations on nydef.py.
"""

import string
from typing import Tuple, List

import instance_creator as new
import definitions as nydef
import nylo_object as nydict


parse_assignation = None


def parse(code):
    """
    Parse a string to a Nylo Object.
    """
    # Add end of file, for sure.
    code += '\n'
    
    # Actually parse the code as a multiline_code element
    parsed, index, indent = parse_multiline_code(code)
    
    # Return the code.
    return parsed


def parse_multiline_code(code: str, index=0, prev_indent=-1, 
                         indent=0) -> Tuple[nydict.NyloObject, int, int]:
    """
    Parse a multiline code starting from index. This is used
    recursevly to parse indented code: every new indent will
    call a new parse_multiline_code, passing the index, the
    previous indent and the new indent.
    """
    # We are going to store here all the lines we parse.
    lines = []
    
    # As soon as the code deindents, we should stop.
    while indent > prev_indent:
        # Parse the first line, aka until new line, or :\n that's
        # supposed to introduce indented code.
        line, index = parse_until(code, index, ['\n', ':\n'])
        # Get past the \n. If there is a :\n, we need to skip
        # two characters.
        while index < len(code) and code[index] in ':\n': index += 1
        # Append the parsed line to the lines.
        lines.append(line)
        # If the string is over, we need to finish the function
        # and return what we parsed, so we break the loop.
        if index == len(code): 
            # Indent is set to -1 so that every parse_multiline_code
            # knows that the code is over and will return its value.
            indent = -1
            break
        
        # Calculate the indent of the following line, to 
        # choose what to do next (parse a indented line, or
        # parse normally a line, or finish)
        next_line_indent, index = get_indentation(code, index)
        # If the indent of the next line is greater than the indent
        # of the function, there is an indented code we should parse
        if next_line_indent > indent:
            indented_code, index, indent = \
                parse_multiline_code(code, index, indent, next_line_indent)
            # Indented code should be added at the and of the last line, that's
            # a nylo code object, so we transform it to a normal list, append the
            # indented parsed code, and re-transform it back to a nylo code.
            lines[-1].add(indented_code)
        # Else, the indent of the next line is the indent
        # of this multiline_code we're working on.
        else: indent = next_line_indent
        
    # Return a new instance of nymultiline_code based on the 
    # parsed lines.
    return new.codelines(lines), index, indent
        

def get_indentation(code: str, index: int) -> Tuple[int, int]:
    """
    This is a parser for indentation. 
    """
    start_index = index
    while code[index] in ' \t\n':
        # First of all, we need to get to the first
        # non empity line.
        while code[index] == '\n': index += 1
        # We save the index of the beginning of the line
        start_index = index
        # Skip indentation
        while code[index] in ' \t': index += 1
    # If after the last line there is something different
    # from a whitespace, and therefore it's not an empity line,
    # we should return the indentaton level and the index
    # we're at.
    return index - start_index, index


def parse_until(code: str, index: int, endings: List[str]):
    """
    Parse_until will call multiple times parse_element until
    a endind is met. This allows to parse multiple successive
    elements.
    This functions also manages symbols by calling 
    replace_symbols.
    """
    # A line of code is divided into sectors, separated by
    # symbols. E.g.:
    # 1+1 will produce [[1], '+', [1]]
    # wich will be replaced with replace_symbols into
    # ['sum', [1, 1]] 
    parsed_objects_sectors = [[]]
    # endings might be of more than one character, so we check
    # if the code starts with any of the endings at the index we're at.
    while not any(code.startswith(end_char, index) for end_char in endings):
        # Parse a single element
        parsed_object, index = parse_element(code, index)
        # If the element is in the symbols, we add both the symbol
        # to the list of sectors, and a new empity sector after the
        # symbol
        if isinstance(parsed_object, str) \
            and parsed_object in nydef.symbols: 
            parsed_objects_sectors.extend((parsed_object, []))
        # If it's not a symbol, but it's also not None, just
        # append it to the last sector.
        elif parsed_object: parsed_objects_sectors[-1].append(parsed_object)
        # If the file is over while still searching for the end, raise an
        # error
        if index == len(code): 
            raise SyntaxError("Parsing error: end of file while searching for \""
                +'" or "'.join(endings)+'"')
    # Replace the symbols.
    parsed_objects = replace_symbols(parsed_objects_sectors)
    return new.code(parsed_objects), index


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
        parsed = nydict.NyloObject(zip(keys, values))
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
        if index == len(code): raise SyntaxError('Parsing error: end of file while searching for "]"')
    index += 1
    return new.path(labels), index


def parse_curly_braces(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
    try:
        structure, index = parse_struct_until(code, index + 1, ['|', '}'])
        if code[index] == '}':
            return structure, index + 1
    except TypeError:
        funct_code, index = parse_until(code, index + 1, ['}'])
        return new.function(funct_code, new.struct([])), index + 1
    function_code, index = parse_until(code, index + 1, ['}'])
    return new.function(function_code, structure), index + 1

def parse_struct_until(code: str, index: int, 
                       endings: List[str]) -> Tuple[nydict.NyloObject, int]:
    variables = [[]]
    while not any(code[index] == end for end in endings):
        last_element, index = parse_element(code, index)
        if last_element == None:
            pass
        elif last_element == ',':
            variables.append([])
        elif isinstance(last_element, str):
            raise TypeError
        elif new.string('variable_name') in last_element:
            if len(variables[-1]) == 0:
                variables[-1].append(last_element)
            else:
                last_element[new.string('class')] = variables[-1][0]
                variables[-1][0] = last_element
        elif new.variable('function_code') in last_element:
            variables[-1][0][new.string('condition')] = last_element
        else:
            raise TypeError
    return new.struct([el[0] for el in variables]), index

def parse_element(code: str, index: int) -> Tuple[nydict.NyloObject, int]:
    for possible_starts in right_parser_by_start:
        if any(code.startswith(start, index) for start in possible_starts):
            parsed_object, new_index = \
                right_parser_by_start[possible_starts](code, index)
            return parsed_object, new_index
    raise SyntaxError('Parsing error: unexpected character "'+str(code[index])+'"')

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
        if index == len(code): raise SyntaxError("Parsing error: unclosed string.")
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
    if variable_name in nydef.symbols: return variable_name, index
    variable_objects = new.variable(variable_name)
    return variable_objects, index


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
                    [new.variable(nydef.symbols[symbol]),
                    new.nylist(arguments)])
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
    if code[index:index+2] in nydef.symbols:
        return code[index:index+2], index+2
    else:
        return code[index], index+1

right_parser_by_start = {
        nydef.number_starts: parse_number, #OK
        nydef.square_brace_start: parse_square_braces, #OK
        nydef.string_starts: parse_string, #OK, \n
        nydef.variable_starts: parse_variable, #OK
        nydef.curly_braces_start: parse_curly_braces, #{int x:3}
        nydef.inline_comment_start: parse_inline_comment, #OK
        nydef.multiline_comment_start: parse_multiline_comment, #OK
        nydef.exa_start: parse_exa, #OK
        nydef.round_braces_start: parse_round_braces, #OK
        tuple(nydef.symbols): parse_symbol, #OK
        nydef.whitespaces: parse_whitespace, #OK
        nydef.prevent_new_line: parse_prevent_new_line, #OK
        nydef.assignation: parse_assignation, #TODO
}
        
print(parse("""namespace test:

    def {fun int {>10} duble} {int {>5} duble}:
        duble*2
        
    if (x>10) {print(2+2+2)}
    else:
        say('Hurra!!')"""))
