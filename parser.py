"""
This is the Zero parser for Nylo, wrote by Veggero. This file has been created on the fifth of November.
You can absolutely what you want with this file BUT you can't monetize it. Sorry. You don't have to
give credits to me tho. Aka this is cc-nc. Have fun!

This parser target is to take a formatted_text with nylo_formatting and make it an nylo object. Built-in classes
made by this are:

code: {list command behaviour}
command: {function behaviour, list args}
function: {code/python_function behaviour, argument args}
condition: {list function conditions}
argument: {list variable variables}
variable: {str name, condition cond}
symbol: {str symb}

str: {py_str string}
int: {py_int integer}
float: {py_float floating_point}
python_function: {function}
python_string: {pystr}
python_int: {pyint}
python_float: {pyflt}
"""

from string import *
from collections import namedtuple
from definitions import nydict 
import definitions

def parse(string):
    """
    Parse a string to a Nylo Object.
    """
    # Add start and end of code
    string = '('+string+')'
    # Convert the string to code
    parsed, index = string_to_code(string)
    # Check that everything has been parsed
    if len(string) != index:
        raise SyntaxError("Unmatched closed round bracket at character "+str(index-1))
    else:
        return parsed

"""
#  ISTANCES INITIALIZATORS   #
# they take values and make  #
#    nydicts out of them     #
"""

def new_code(behaviour):
    # Create the behaviour_list_object object
    behaviour_list_object = nydict(tuple([(new_int(couple[0]), couple[1]) for couple in enumerate(behaviour)]))
        
    # And set it as propriety of the nylo code object
    nylo_code_object = nydict(((new_str('behaviour'), behaviour_list_object),))
    return nylo_code_object

def new_str(string):
    return nydict((('py_string', string),))

def new_int(integer):
    return nydict((('py_int', integer),))

def new_float(floating_point):
    return nydict((('py_float', floating_point),))
 
"""
#   STRING TO * PARSERS   #
# they take a string and  #
# create the right object #
#       out of it         #
"""
 
def string_to_code(code, start_index = 0, until = ')', start_character = '('):
    """
    Parse a string and output its code and the index of ending.
    start_index --> start parsing from a character in the code.
    until --> when the until character is met, parsing will stop
    start_character --> will ignore the specified start_character at given index if there is one
    """
    # Set the index
    index = start_index
    # We are going to parse all the components of code, and
    # put them all in a list called every_parsed
    every_parsed = list()
    # First of all, skip the character at start, if there is
    # one:
    if code[index] in start_character:
        index += 1
        
    # Loop thrugh code until we find the until character
    while code[index] != until:
        # Now, we must get what we are parsing by giving a look to
        # the character we're examinating.
        # { is a function
        if code[index] == '{':
            parsed, index = string_to_function(code, index)
        # [ is a list
        elif code[index] == '[':
            parsed, index = string_to_list(code, index)
        # ( is a code
        elif code[index] == '(':
            parsed, index = string_to_code(code, index)
        # // is a comment
        elif code[index:index+2] == '//':
            parsed, index = ignore_comment(code, index)
        # /* is a multiline_comment
        elif code[index:index+2] == '/*':
            parsed, index = ignore_multiline_comment(code, index)
        # ' or " is a string
        elif code[index] == '"' or code[index] == "'":
            parsed, index = string_to_string(code, index)
        # There are actually 2 cases for numbers:
        # 12 31 41 53 (starting with digits)
        # .3 .5 (starting with a ".")
        elif ((code[index] in digits) or
              (code[index] == '.' and code[index+1] in digits)):
            parsed, index = string_to_number(code, index)
        # Then variables are anything that starts with a ascii-letter .
        # This means variables such as "_a" or "__thing" are not allowed.
        elif code[index] in ascii_letter:
            parsed, index = string_to_variable(code, index)
            # Weird case for variables: they could be actually symbols - we
            # just have to check if they're a symbol and if so replace them
            if parsed[new_str('name')][new_str('value')] in symbols:
                parsed = variable_to_symbol(parsed)
        # Anything else is a symbol.
        else:
            parsed, index = string_to_symbol(code, index)
            # Let's check if it's actually a symbol
            if not parsed[new_str('symb')][new_str('value')] in definitions.symbols:
                # it's not, it's probably a space or a tab, kill it with fire
                parsed = None
            # Weird case for symbols, successive symbols should be joined
            # together. We also should check first is there is a symbol before.
            elif len(every_parsed) > 0:
                if new_str('symb') in every_parsed[-1]:
                    # Get the old and the new symbols.
                    old_symb = every_parsed[-1][new_str('symb')][new_str('value')]
                    new_symb = parsed[new_str('symb')][new_str('value')]
                    # Set them.
                    every_parsed[-1] = every_parsed[-1]['symb']('value', old_symb+new_symb)
                    # We don't need the new symbol anymore, as we added it
                    # to the old one.
                    parsed = None
        
        # Okay! Add what we parsed to every_parsed list
        # We need to check *if* we parsed something, things like comments
        # might not parse anything at all
        if parsed != None:
            every_parsed.append(parsed)
            
        # Also check if we are at the end of the file and we didn'tt find
        # any until character
        if index == len(code):
            raise SyntaxError("Unmatched open "+start_character)
            
    # Eat the last character
    index += 1
    return new_code(every_parsed), index

def string_to_string(code, index):
    """
    Parse a string to a string. It's confusing, but just thing about it.
    What this does is making "happy" a happy string object.
    """
    # Remember with what char we started, either ' or ".
    # Obv it's also the char where we should end at.
    end_character, start_character_index = code[index], index
    # Go after it
    index += 1
    # Loop until closing character.
    while code[index] != end_character:
        index += 1
    # Parse the string to a string object.
    string = code[start_character_index + 1 : index]
    string_object = new_str(string)
    # Ignore the ending character.
    index += 1
    return string_object, index

def string_to_number(code, index):
    # Save the start index.
    start_index = index
    # Loop until first non-numeric character.
    while code[index] in digits + '.':
        # If this is the second '.', we should stop
        if code[index] == '.' and '.' in code[start_index:index]:
            break
        index += 1
    # Save the number
    str_number = code[start_index:index]
    # and make it an object
    if '.' in str_number:
        number = new_float(float(str_number))
    else:
        number = new_int(int(str_number))
    return number, index

print(parse('(1.23)1'))
