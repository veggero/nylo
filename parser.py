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

str: {python_str string}
int: {python_int integer}
float: {python_float floating_point}
python_function: {function}
python_string: {pystr}
python_int: {pyint}
python_float: {pyflt}
"""

from string import *
from collections import namedtuple
import definitions

def new_code(behaviour):
    # Create the behaviour_list_object object
    behaviour_list_object = frozenset(enumerate(behaviour))
    # And set it as propriety of the nylo code object
    nylo_code_object = frozenset((new_str('behaviour'), behaviour_list_object))
    return nylo_code_object

def new_str(string):
    return frozenset(('string', frozenset(('pystr', string))))

def new_int(integer):
    return frozenset(('integer', frozenset(('pyint', integer))))

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
        # There are actually 3 cases for numbers:
        # 12 31 41 53 (starting with digits)
        # -12 -42 .2 .5 (starting with ".-" and then a digit)
        # -.3 -.5 (a "-", a "." and then a digit)
        elif ((code[index] in digits) or
              (code[index] in '-.' and code[index+1] in digits) or
              (code[index] == '.' and code[index+1] == '-' and code[index+2] in digits)):
            parsed, index = string_to_number(code, index)
        # Then variables are anything that starts with a ascii-letter .
        # This means variables such as "_a" or "__thing" are not allowed.
        elif code[index] in ascii_letter:
            parsed, index = string_to_variable(code, index)
            # Weird case for variables: they could be actually symbols - we
            # just have to check if they're a symbol and if so replace them
            if parsed['name']['value'] in symbols:
                parsed = variable_to_symbol(parsed)
        # Anything else is a symbol.
        else:
            parsed, index = string_to_symbol(code, index)
            # Let's check if it's actually a symbol
            if not parsed['symb']['value'] in definitions.symbols:
                # it's not, it's probably a space or a tab, kill it with fire
                parsed = None
            # Weird case for symbols, successive symbols should be joined
            # together. We also should check first is there is a symbol before
            elif len(every_parsed) > 0:
                if 'symb' in every_parsed[-1]:
                    every_parsed[-1]['symb']['value'] = every_parsed[-1]['symb']['value'] + parsed['symb']['value']
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

print(parse('(())()'))
