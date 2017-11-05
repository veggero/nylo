from string import *

"""
These are the global variables during the Nylo scripts
executions.
"""
global_nylo_variables = dict()

""" 
Here I declare how you can recognige every type in the nylo formatting system, 
using a dictionary where every key is a type and its value is a function that
takes in argument the string that's getting parsed and the index we're examinating.
I don't take just the character because I might want to check also chars after or
before the one we're looking at.
"""
types_declarations_beginnings = {
    # A function begins where there's a "{".
    # By the way, with functions we also mean classes and 
    # functions with no arguments.
    'function': lambda string, index: string[index] == '{',
    # A dictionary *or a list* always start with [.
    # We prefer to use dictionary over list because you can
    # also declare lists with round brackets.
    'dictionary': lambda string, index: string[index] == '[',
    # The "(" character defines a piece of code.
    'code': lambda string, index: string[index] == '(',
    # " and ' declares strings.
    'string': lambda string, index: string[index] == '"' or string[index] == "'",
    # // is the start of an inline comment. 
    'inline_comment': lambda string, index: string[index:index+2] == '//',
    # /* defines a block comment
    'comment': lambda string, index: string[index:index+1] == '/*',
    # A number can start with any digit or also . and - *if* there
    # are digits afterwards. We must also check for numbers like
    # -.2, aka "-", ".", and digits.
    'number': lambda string, index: ((string[index] in digits) or 
                                   (string[index] in '.-' and string[index+1] in digits) or
                                   (string[index] == '.' and string[index+1] == '-' and string[index+2] in digits)),
    # A variable is everything that starts with a letter.
    # Please notice that this means variables such as _a are not
    # accepted. Also, we are only reading ascii.
    'variable': lambda string, index: string[index] in ascii_letters,
    # Anything is a symbol actually.
    'symbol': lambda string, index: True,
}
    
"""
I also declare here how every type ends. By doing this, I can check where
any class starts and finish, and give the whole string to the right type
parser. 
"""
types_declarations_endings = {
    # Function ends with '}'
    'function': lambda string, index: string[index] == '}',
    # Dictionaries ends with ']'
    'dictionary': lambda string, index: string[index] == ']',
    # And code ends with ) - plain and simple
    'code': lambda string, index: string[index] == ')',
    # Strings ends with ' and ", just like they starts
    'string': lambda string, index: string[index] == '"' or string[index] == "'",
    # Inline comments simply finish with the new line
    'inline_comment': lambda string, index: string[index] == '\n',
    # Comments blocks finish with "*/"
    'comment': lambda string, index: string[index:index+1] == '*/',
    # Numbers finish on any character that is not a digit or a "."
    # If the char is a "." we need to check if there is a digit aftewards though.
    # (0. is not a valid floating point number, sorry)
    'number': lambda string, index: ((not string[index+1] in digits + '.') or
                                   (string[index+1] == '.' and not string[index+2] in digits)),
    # Variable finish on first non-ascii-letter character. In the string you
    # can also use digits and underscores too, so those are fine too.
    'variable': lambda string, index: not string[index+1] in ascii_letters + digits + '_',
    # Symbols are single-digits, so they are already over
    'symbol': lambda string, index: True,
}
    
"""
Some types are special and do not want their content parsed. Like:
(() <-- this is clearly wrong, because we open a code we never close
"(" <-- this is okay, because string content is not parsed
"""
ignore_content_types = {'string', 'comment', 'inline_comment'}

"""
Some types need the first character and last to parse, others do not:
{*2} can live without the brackets
1342 can't live without the 1 and the 2
Here we set those wich does NOT need those declaration
"""
type_doesnt_need_starting_and_ending_declarations = {'function', 'dictionary', 'code', 'string', 'inline_comment', 'comment'}

"""
Parser functions! 
Your parser function will be automatically called with the string it needs to parse
if you set in the right way its start and end in the above dictionaries. If you add a custom
type you also need to specify its parser function down to the type_parser_function dict.
"""
def string_to_code(string):
    """
    Takes Nylo code you write and output parsed commands.
    This one gets called with what you wrote, so it's quite important. 
    This one calls all the other parsers.
    """
    """
    Some check for types starts and endings does not check
    just the character we're looking at but also up to 2 after that,
    and if they're near EOF this could cause IndexError. 
    To avoid that, we add 5 empity spaces at the end of the code.
    Spaces are ignored anyway, and if you need 5 character to decide 
    if your type is there or not, you are terrible. 
    (You usually need just one char, like "{" and you know it's a function,
    but numbers and other things need a couple more because yes)
    """
    string = string + '     '
    """
    Now. We will iter over string, without ever modifing it, and when we
    meet a type start (like "{") we will search until its end, and give the whole
    string to the type parser (like string_to_function).
    This means we need to "jump" over what has been parsed by the type parser - therefore
    we can't just loop over every character, so we will use a index variable instaed.
    We must remember and return everything we parse, so we'll also use a list to save
    what we parsed.
    """
    index, parsed = 0, list()
    # Loop thru every character of string
    while index < len(string):
        """
        Now, we loop over the types_declarations_beginnings to see what type we are
        dealing with.
        """
        for type_name in types_declarations_beginnings:
            declaration = types_declarations_beginnings[type_name]
            if declaration(string, index):
                """
                We now know what we are dealing with. We need to find where 
                it ends first of all. 
                There is a weird case here, aka if a type start and ends in the same
                way (like for strings), we need to start fetching the end from the 
                successive character.
                """
                type_str_start = index
                start_and_end_in_the_same_way = (declaration == types_declarations_endings[type_name])
                type_str_end = fetch_end_from(type_name, index if not start_and_end_in_the_same_way else index + 1)
                """
                Now that we have the start and the end, we can pass it to
                the parser and get the output. But we also need to check if 
                type_doesnt_need_starting_and_ending_declarations
                """
                if type_name in type_doesnt_need_starting_and_ending_declarations:
                    type_string_to_parse = string[type_str_start+1, type_str_end]
                else:
                    type_string_to_parse = string[type_str_start, type_str_end+1]
                """
                Now we have the string to parse, call the parser
                """
                type_parser = type_parser_functions[type_name]
                output = type_parser(type_string_to_parse)
                # If there *is* an output, add it to the parsed list
                if output != None:
                    parsed.append(output)
                # move the index
                index = type_str_end + 1
                # and end the loop in type_name (there are no other types to execute)
                break
        # but what if we find no type that can start in types_declarations_beginnings?
        else:
            # should be spaces or tabs or something like that - ignore it.
            index += 1
                    
    return parsed

"""
We need to know from each built-in type name what functions parse
it. In Nylo it's always to_[type](str) e.g.: to_function("{x*2}")
"""
type_parser_functions = {
    'function': string_to_function,
    'dictionary': string_to_dict,
    'code': string_to_code,
    # string to string should just keep the original one
    'string': string_to_string,
    # to_comment functions just return nothing
    'inline_comment': string_to_inline_comment,
    'comment': string_to_comment,
    'number': string_to_number,
    # this one creates a variable instance (var != str)
    'variable': string_to_variable,
    'symbol': string_to_symbol,
}
