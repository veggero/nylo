import string

# TODO These are the parser that should be defined.
# Since the code isn't ready yet, I
# initialize them with None to use
# their keyword anyway, for testing purposes.
parse_numbers = None
parse_square_bracket = None
parse_string = None
parse_variable = None
parse_curly_bracket = None
parse_inline_comment = None
parse_multiline_comment = None
parse_exa = None
parse_round_bracket = None


class nydict:

    """
    Nylo object is just a dict, but it needs to be hashable.
    Therefore I use tuples, but I create a new class to make
    it prettier (such as, dict-like declaration and dict get and
    assign functions)
    """

    def __init__(self, args):
        self.value = frozenset(args)

    def __eq__(x, y):
        try:
            return x.value == y.value
        except AttributeError:
            return False

    def __hash__(self):
        return hash(self.value)

    def __getitem__(self, key):
        """
        Get an item: nylo_obj(('age',16))['age'] --> 16
        """
        for couple in self.value:
            if couple[0] == key:
                return couple[1]
        raise IndexError(
            "Key " + str(
                key) + " can't be found in nydict " + str(
                    self))  # newfags can't avoid indexerror

    def __contains__(self, key):
        return any([couple[0] == key for couple in self.value])

    def __call__(self, key, value):
        """
        Set a value and return the new tupledict.
        nylo_obj(('age', 16))('age', 17)
        --> nylo_obj(('age', 17))
        """
        return [couple
                if couple[0] != key
                else (couple[0], value)
                for couple in self.value]

    def __repr__(self):
        return ('{' + ', '.join([repr(son[0]) + ': ' +
                repr(son[1]) for son in self.value]) + '}')

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        for key in self.value:
            yield key[0]


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


def new_str(string):
    return nydict((('py_string', string),))


def new_int(integer):
    return nydict((('py_int', integer),))


# See specifications 2.0.0: parse_element
def parse_element(code: str, index: int):
    for possible_starts in right_parser_by_start:
        if any(code.startswith(start, index) for start in possible_starts):
            parsed_object, new_index = right_parser_by_start[
                possible_starts](code, index)
    return parsed_object, new_index


# See specifications 2.0: parsing
right_parser_by_start = {
        (tuple(string.digits) +
         tuple("." + digit for digit in string.digits)): parse_numbers,
        ("["): parse_square_bracket,
        ("'", "\""): parse_string,
        string.ascii_letters: parse_variable,
        ("{"): parse_curly_bracket,
        ("//"): parse_inline_comment,
        ("/*"): parse_multiline_comment,
        ("#"): parse_exa,
        ("("): parse_round_bracket
}
