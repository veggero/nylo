import string

tokens = {
     "COMMENT_ONELINE": '//',
     "OPEN_QUICKFUNCTION": '{',
     "CLOSE_QUICKFUNCTION": '}',
     "ASSIGNMENT": ':',
     "OPEN_LIST": '[',
     "CLOSE_LIST": ']',
     "GREATER": '>',
     "LESS": '<',
     "EQUAL": '=',
     "PLUS": '+',
     "MINUS": '-',
     "MOLTIPLICATE": '*',
     "DIVIDE": '/',
     "POW": '**',
     "CONCATENATION": '&',
     "OPEN_DOUBLEQUOTE": '"',
     "CLOSE_DOUBLEQUOTE": '"',
     "OPEN_SINGLEQUOTE": '\'',
     "CLOSE_SINGLEQUOTE": '\'',
     "OPEN_NODE": '{',
     "CLOSE_NODE": '}',
     "OPEN_MULTILINECOMMENT": '/*',
     "CLOSE_MULTILINECOMMENT": '*/',
     "OPEN_ROUNDBRACES": '(',
     "CLOSE_ROUNDBRACES": ')',
     "EXA": '#'}
types = {
     "INTEGER": 'int',
     "STRING": 'string',
     "LIST": 'list',
     "FLOAT": 'float',
     "DICTIONARY": 'dict'}

# TODO These are the parser that should be defined.
# Since the code isn't ready yet, I
# initialize them with None to use
# their keyword anyway, for testing purposes.
parse_square_bracket = None
parse_variable = None
parse_curly_bracket = None
parse_inline_comment = None
parse_multiline_comment = None
parse_exa = None
parse_round_bracket = None


# See specifications 2.0.0: parse_element
def parse_element(code: str, index: int):
    for possible_starts in right_parser_by_start:
        if any(code.startswith(start, index) for start in possible_starts):
            parsed_object, new_index = right_parser_by_start[
                possible_starts](code, index)
    return parsed_object, new_index


# See specifications 2.0.1: parse_string
def parse_string(code, index):
    end_character, start_character_index = code[index], index
    index += 1
    while code[index] != end_character:
        index += 1
        # TODO, if EOF should raise exception
    string = code[start_character_index + 1: index]
    string_object = new_str(string)
    index += 1
    return string_object, index


# See specifications 2.0.2: parse_numbers
def parse_numbers(code, index):
    start_index = index
    while code[index] in string.digits + '.':
        if code[index] == '.' and '.' in code[start_index:index]:
            break
        index += 1
    str_number = code[start_index:index]
    if '.' in str_number:
        number = new_float(float(str_number))
    else:
        number = new_int(int(str_number))
    return number, index


# See specifications 2.0: parsing
right_parser_by_start = {
        (tuple(string.digits) +
         tuple("." + digit for digit in string.digits)): parse_numbers,
        (tokens['OPEN_LIST']): parse_square_bracket,
        (tokens['OPEN_SINGLEQUOTE'], tokens['OPEN_DOUBLEQUOTE']): parse_string,
        string.ascii_letters: parse_variable,
        (tokens['OPEN_NODE']): parse_curly_bracket,
        (tokens['COMMENT_ONELINE']): parse_inline_comment,
        (tokens['OPEN_MULTILINECOMMENT']): parse_multiline_comment,
        (tokens['EXA']): parse_exa,
        (tokens['OPEN_ROUNDBRACES']): parse_round_bracket
}
