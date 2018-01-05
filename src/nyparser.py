import string

# TODO These are the parser that should be defined. Since the code isn't ready yet, I
# initialize them with None to use their keyword anyway, for testing purposes.
parse_numbers, parse_square_bracket, parse_string, parse_variable, parse_curly_bracket, parse_inline_comment, parse_multiline_comment, parse_exa, parse_round_bracket = [None] * 9

# See specifications 2.0.0: parse_element
def parse_element(code: str, index: int):
	for possible_starts in right_parser_by_start:
		if any(code.startswith(start, index) for start in possible_starts):
			parsed_object, new_index = right_parser_by_start[possible_starts](code, index)
	return parsed_object, new_index
	

# See specifications 2.0: parsing
right_parser_by_start = {
	tuple(string.digits) + tuple("."+digit for digit in string.digits): parse_numbers,
	("["): parse_square_bracket,
	("'", "\""): parse_string,
	string.ascii_letters: parse_variable,
	("{"): parse_curly_bracket,
	("//"): parse_inline_comment,
	("/*"): parse_multiline_comment,
	("#"): parse_exa,
	("("): parse_round_bracket
	}
