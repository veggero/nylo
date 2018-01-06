import string
from . import tokens
from . import new


# TODO: FUNCTIONS TO TAKE HERE
# Old code link:
# https://github.com/pyTeens/nylo/blob/f1d7b6edbce36a7b8272d1457354942f1efcc0d0/nylo.py
#
# parse -> parse (as is)
# parse_code_until -> parse_until (a lot of changes needed)
# parse_string -> parse_variable (adding new.var before output)
# parse_string_to_code -> parse_round_braces (little change needed)
# parse_string_to_multiline_code -> parse_multiline_code
# <- (major changes needed.)
# parse_string_to_indentation -> parse_indent (no changes)
# ignore_comment -> parse_inline_comment (no changes)
# ignore_multiline_comment -> parse_multiline_comment (no changes)
# parse_string_to_symbol -> parse_symbol (no changes)
# parse_string_to_list -> parse_square_braces (little changes I think)
# parse_string_to_function -> parse_curly_braces (major changes)
# replace_symbols -> replace_symbols (completly rewritten)
# parsed_to_argument -> possibly to rewrite
#
# CHANGES
# new_str, new_int etc --> new.str, new.int etc
# call_right_parser --> parse_element
# parse_string_to_string --> parse_string
# parse_string_to_number --> parse_number
#


# These are the parser that should be defined.
# Since the code isn't ready yet, I
# initialize them with None to use
# their keyword anyway, for testing purposes.
parse_square_braces = None
parse_variable = None
parse_curly_braces = None
parse_inline_comment = None
parse_multiline_comment = None
parse_exa = None
parse_round_braces = None


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
    string_object = new.nystr(string)
    index += 1
    return string_object, index


# See specifications 2.0.2: parse_number
def parse_number(code, index):
    start_index = index
    while code[index] in string.digits + '.':
        if code[index] == '.' and '.' in code[start_index:index]:
            break
        index += 1
    str_number = code[start_index:index]
    if '.' in str_number:
        number = new.nyfloat(float(str_number))
    else:
        number = new.nyint(int(str_number))
    return number, index


# See specifications 2.0: parsing
right_parser_by_start = {
        (tuple(string.digits) +
         tuple("." + digit for digit in string.digits)): parse_number,
        (tokens.OPEN_LIST): parse_square_braces,
        (tokens.OPEN_SINGLEQUOTE, tokens.OPEN_DOUBLEQUOTE): parse_string,
        string.ascii_letters: parse_variable,
        (tokens.OPEN_NODE,): parse_curly_braces,
        (tokens.COMMENT_ONELINE,): parse_inline_comment,
        (tokens.OPEN_MULTILINECOMMENT,): parse_multiline_comment,
        (tokens.EXA,): parse_exa,
        (tokens.OPEN_ROUNDBRACES,): parse_round_braces
}
