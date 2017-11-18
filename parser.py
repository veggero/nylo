"""
This is the Parser Zero for Nylo, wrote by Veggero. This file has been created on the fifth of November.
You can absolutely what you want with this file BUT you can't monetize it. Sorry. You don't have to
give credits to me tho. Aka this is cc-nc. Have fun!

This parser target is to take a formatted_text with nylo_formatting and make it an nylo object. Built-in classes
made by this are:

multiline_code: {list code lines}
code: {list command behaviour}
command: {function behaviour, list args}
function: {code/python_function behaviour, argument args}
condition: {list function conditions}
argument: {list variable variables}
variable: {str name, condition cond}
symbol: {str symb}

python_function: {function}
python_string: {pystr}
python_int: {pyint}
python_float: {pyflt}
"""

"""
TODO - b4 Nylo Zero
- Replacing symbols

TODO - b4 Nylo One
- Indent control
- Binary, oct, ascii/utf string/number declarations
- Special arguments
- Special chars in strings

TODO - should be okay but not sure
- Functions (done? executer-side?)
- Arguments (executer-side?)
- Calling (executer-side?)
"""

from string import *
from collections import namedtuple
# I also import all definitions, but I want to quickly use nydict
from definitions import nydict 

import definitions

def parse(string):
    """
    Parse a string to Nylo Objects.
    """
    # Add end of code
    string += ')'
    # Convert the string to code
    parsed, index = parse_string_to_multiline_code(string, until = ')')

    return parsed
 
"""
#   GENERAL PURPOSE PARSERS      #
#  they do not take a string and #
#  create out of it a type, but  #
#  they're more general purpose  #
"""    

def call_right_parser(code, index):
    """
    TYPES TO PARSE
    - function  (parse_string_to_function)    {}
    - list      (parse_string_to_list)        []
    - code      (parse_string_to_code)        ()
    - comment   (ignore_comment)        //\n
    - ml_cmment (ignore_ml_comment)     /**/
    - string    (parse_string_to_string)      ''
    - number    (parse_string_to_number)      . digits
    - variable  (parse_string_to_variable)     ascii_letters
    - symbol    (parse_string_to_symbol)      in definitions.symbols
    """
    # Now, we must get what we are parsing by giving a look to
    # the character we're examinating.
    # { is a function
    if code[index] == '{':
        parsed, index = parse_string_to_function(code, index)
    # [ is a list
    elif code[index] == '[':
        parsed, index = parse_string_to_list(code, index)
    # ( is a code
    elif code[index] == '(':
        parsed, index = parse_string_to_code(code, index)
    # // is a comment
    elif code[index:index+2] == '//':
        parsed, index = ignore_comment(code, index)
    # /* is a multiline_comment
    elif code[index:index+2] == '/*':
        parsed, index = ignore_multiline_comment(code, index)
    # ' or " is a string
    elif code[index] == '"' or code[index] == "'":
        parsed, index = parse_string_to_string(code, index)
    # There are actually 2 cases for numbers:
    # 12 31 41 53 (starting with digits)
    # .3 .5 (starting with a ".")
    elif ((code[index] in digits) or (code[index] == '.' and code[index+1] in digits)):
        parsed, index = parse_string_to_number(code, index)
    # Anything in the symbols set, is a symbol.
    elif code[index] in definitions.symbols:
        parsed, index = parse_string_to_symbol(code, index)
    # Then variables are anything that starts with a ascii-letter .
    # This means variables such as "_a" or "__thing" are not allowed.
    elif code[index] in ascii_letters:
        start_index = index
        string, index = parse_string(code, index)
        # The string is either a symbol, a argument, or a variable
        # If it's in symbols, it's a symbol
        if string in definitions.symbols:
            parsed = new_sym(string)
        # If it's in arguments, it's a arg
        # Any other case, it's a variable
        else:
            parsed = new_var(string)
    # ignore spaces and tabs 
    elif code[index] in ' \t':
        index += 1
        parsed = None
    else:
        # Unrecognized character
        raise SyntaxError("Unrecognized character while parsing: '"+code[index]+"'")
    return parsed, index

def parse_code_until(code, index, until = '', ignore = ''):
    # First of all, skip the character at start, if there is one:
    # We will store every element we'll parse in
    # every_parsed.
    every_parsed = [];
        
    # Loop thrugh code until we find the until character
    while not code[index] in until:
        
        # Check if the character to parse is not to ignore
        if not code[index] in ignore:
            # Parse the right type, depending on the character
            parsed, index = call_right_parser(code, index)
        
            # Okay! Add what we parsed to the every_parsed list
            # We need to check *if* we parsed something, things like comments
            # might not parse anything at all
            if parsed != None:
                every_parsed.append(parsed)
                
        else:
            # Move over
            index += 1
            
        # Also check if we are at the end of the file and we didn't find
        # any ending character
        if index == len(code):
            raise SyntaxError("Unmatched open bracket.")
            
    # Eat the last character
    index += 1
    
    return every_parsed, index

def parse_string(code, index):
    # Rembember the start.
    start_index = index
    # Go on until space.
    while code[index] in digits + ascii_letters + '_':
        index += 1
    # Return the string and the final index
    return code[start_index:index], index
 
"""
#   STRING TO * PARSERS   #
# they take a string and  #
# create the right object #
#       out of it         #
"""    

def parse_string_to_code(code, index):
    """
    Parse a string and output its code and the index of ending.
    """
    # get past the (
    index += 1
    
    # Parse until the until character
    parsed, index = parse_code_until(code, index, ')', ignore = '\n\t ')
    
    return new_code(parsed), index

def parse_string_to_multiline_code(code, index = 0, until = ')'):
    """
    Parse a string and output its code and the index of ending.
    """
    # Parse until the until character
    parsed, index = parse_code_until(code, index, until)
    
    # Split code at new lines
    parsed = split(parsed, new_sym('\n'))
    
    # Replace every code with its code nylo object
    for i in range(len(parsed)):
        parsed[i] = new_code(parsed[i])
        
    return new_multiline_code(parsed), index

def parse_string_to_string(code, index):
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

def parse_string_to_number(code, index):
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

def ignore_comment(code, index):
    # This simply has to wait until new line.
    while code[index] != '\n':
        index += 1
    return None, index

def ignore_multiline_comment(code, index):
    # This simply has to wait until */
    while code[index:index+2] != '*/':
        index += 1
    # Getting past */
    index += 2
    return None, index

def parse_string_to_symbol(code, index):
    # Create the symbol object
    symbol_obj = new_sym(code[index])
    # Move index past the symbol
    index += 1
    return symbol_obj, index

def parse_string_to_list(code, index):
    # Get past the [
    index += 1
    # Parse the list with parse_string_to_code.
    parsed_list, index = parse_code_until(code, index, ']')
    # Split the elements at ','s
    pylist = split(parsed_list, new_sym(','))
    # [] might be also a dict, we need to loop thru it and
    # check if there are ':'s, and if so make a dict.
    # We still don't know if it's a dict, but we need to get
    # an empity list to store couples that will be the dict
    # just for sure.
    protodict = []
    for element in pylist:
        if not new_sym(':') in element:
            # Not a dict.
            # This should be a list
            return new_list([new_list(element) for element in pylist]), index
        
        # Split the key and the value
        key, value = split(element, new_sym(':'))
        # Add them to the list of key values
        protodict.append((new_list(key), new_list(value)))
    # If no break was called, this is officially a dict.
    # Create it.
    else:
        return nydict(protodict), index

def parse_string_to_function(code, index):
    """
    Take a string of a funcion and make a funct object.
    """
    # {x|x*2} / {*2} / {x}
    # Get over the '{'
    index += 1
    # Parse the first argument until | or }
    first_argument, index = parse_code_until(code, index, '|}')
    # Check if there is more to parse, like in {x | x+1}
    if code[index-1] == '|':
        # There is a second argument. Parse it.
        second_argument, index = parse_code_until(code, index, '}')
        # In this case, first argument is the function's argument,
        # and the second one is the behaviour
        args, behaviour = new_code(first_argument), new_code(second_argument)
    else:
        # If function ends on a }, the only argument is code
        args, behaviour = new_code([]), new_code(first_argument)
        
    return new_fun(args, behaviour), index

def parse_string_to_argument(code, index):
    argument = []
    conditions = []
    # Parse the first word
    word, index = parse_string(code, index)
    # [ is a condition, like in int[=2] x
    if code[index] == '[':
        condition, index = parse_code_until(code, index, ']', ignore = '\n\t ')
    # Comma to separate 'em all.
    if code[index] == ',':
        new_var(word)

"""
#  ISTANCES INITIALIZATORS   #
# they take values and make  #
#    nydicts out of them     #
"""

def new_multiline_code(lines):
    return nydict(((new_str('lines'), new_list(lines)),))

def new_code(behaviour):
    return nydict(((new_str('behaviour'), new_list(behaviour)),))

def new_str(string):
    return nydict((('py_string', string),))

def new_int(integer):
    return nydict((('py_int', integer),))

def new_float(floating_point):
    return nydict((('py_float', floating_point),))

def new_sym(symbol):
    return nydict(((new_str('symb'), new_str(symbol)),))

def new_var(variable, conds=[]):
    return nydict(((new_str('name'), new_str(variable)),
                   (new_str('condition'), new_list(conds))))

def new_fun(arguments, code):
    return nydict(((new_str('args'), arguments),
                   (new_str('behaviour'), code)))

def new_arg(variables):
    return nydict(((new_str('variables'), variables),))

def new_list(todo_list):
    # [1] = 1 actually
    if len(todo_list) == 1: 
        return todo_list[0]
    return nydict(tuple(
        [(new_int(couple[0]), couple[1]) 
         for couple 
         in enumerate(todo_list)]))

"""
# LITTLE USEFUL FUNCTIONS #
"""

def split(alist, value):
    output = []
    going = []
    for element in alist:
        if element == value:
            output.append(tuple(going))
            going = []
        else:
            going.append(element)
    output.append(tuple(going))
    return output

print(parse('''{x | x+1}'''))
