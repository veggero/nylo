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

__version__ = '0'
__author__ = 'Niccolo\' "Veggero" Venerandi'

"""
TODO - b4 Nylo 

TODO - b4 Nylo One
- Binary, oct, ascii/utf string/number declarations
- Special arguments
- Special chars in strings
- Errorrs raising

TODO - should be okay but not sure
- Functions (done? executer-side?)
- Calling (executer-side?)
"""

from string import *\

# I also import all definitions, but I want to quickly use nydict
from definitions import nydict 
import definitions

def parse(string):
	"""
	Parse a string to Nylo Objects.
	"""
	# Add end of code
	string += '\n)'
	# Convert the string to code
	parsed, index = parse_string_to_multiline_code(string)
	
	# TODO index != len(code) should raise exception

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
	elif code[index:index+2] == ': ': 
		parsed, index = new_sym(': '), index+2
	elif code[index:index+2] == ':\n':
		parsed, index = new_sym(': '), index+1
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

def parse_code_until(code, index, until='', ignore='\n\t'):
	# First of all, skip the character at start, if there is one:
	# We will store every element we'll parse in
	# every_parsed.
	every_parsed = [];
		
	# Loop thrugh code until we find the until character
	while not code[index] in until:
		
		# Check if the character to parse is not to ignore
		if code[index] in ignore: 
			index +=1
			continue
		
		# Parse the right type, depending on the character
		parsed, index = call_right_parser(code, index)
	
		# If we parsed ': ', we also need to create the arguments before
		if parsed == new_sym(': '): every_parsed = [parsed_to_argument(every_parsed)]
	
		# Okay! Add what we parsed to the every_parsed list
		# We need to check *if* we parsed something, things like comments
		# might not parse anything at all
		if parsed != None: every_parsed.append(parsed)
		
	# Also check if we are at the end of the file and we didn't find
	# any ending character
	if index == len(code): raise SyntaxError("Unmatched open bracket.")
		
	# Eat the last character
	index += 1
	
	return every_parsed, index

def parse_string(code, index):
	# Rembember the start.
	start_index = index
	# Go on until space.
	while code[index] in digits + ascii_letters + '_': index += 1
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
	parsed, index = parse_code_until(code, index, ')')
	parsed = replace_symbols(parsed)
	
	return new_code(parsed), index

def parse_string_to_multiline_code(code, index = 0, until = ')'):
	"""
	Parse a string and output its code and the index of ending.
	"""
	# Parse first line
	last_line_indentation, index = parse_string_to_indentation(code, index)
	parsed, index = parse_code_until(code, index, until+'\n', ignore = '')
	
	# Start saving every parsed line
	parsed_lines = [parsed] if len(parsed)>0 else []
	
	# Keep parsing until you get to until character
	while not code[index-1] in until: 
		indentation, after_indentation_index = parse_string_to_indentation(code, index)
		# If code is indented, there is a function ahead
		if indentation > last_line_indentation:
			parsed, index = parse_string_to_function(code, index)
			parsed_lines[-1].append(parsed)
			
		# If code is de-indented, we are actually in a function, 
		# that is finished, so we need to return
		elif indentation < last_line_indentation:
			for i in range(len(parsed_lines)): parsed_lines[i] = new_code(replace_symbols(parsed_lines[i]))
			return new_multiline_code(parsed_lines), index
			
		else:
			parsed, index = parse_code_until(code, after_indentation_index, until+'\n', ignore = '')
			if len(parsed)>0: parsed_lines.append(parsed)
	
	# Replace every code with its code nylo object
	for i in range(len(parsed_lines)): parsed_lines[i] = new_code(replace_symbols(parsed_lines[i]))

	return new_multiline_code(parsed_lines), index

def parse_string_to_indentation(code, index):
	indentation_level = 0
	# Raise indentation_level at every space or tab until first non
	# whitespace element
	while code[index] in '\t ':
		indentation_level += 1
		index += 1
		
	if code[index] == '\n':
		indentation_level, index = parse_string_to_indentation(code, index+1)

	return indentation_level, index

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
	while code[index] != end_character: index += 1
		# TODO, if EOF should raise exception
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
	while code[index] != '\n': index += 1
	return None, index

def ignore_multiline_comment(code, index):
	# This simply has to wait until */
	while code[index:index+2] != '*/': index += 1
		# TODO len(code)=index+2 should raise exception
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
	# Create the list of the bracket items.
	py_bracket_items = []
	# Parse code until every item separator (,)
	# until we find end of list (]).
	while code[index-1] != ']':
		key, index = parse_code_until(code, index, until=':,]')
		key = replace_symbols(key)
		key = new_code(key)
		# If we ended on a :, this is actually a dictionary
		if code[index-1] == ':':
			# If we still though this was a list, convert it
			# to a dict
			if type(py_bracket_items) == list:
				# TODO if len(py_bracket_items) exception should be raised
				py_bracket_items = {}
			# parse the value
			value, index = parse_code_until(code, index, until=',]')
			value = replace_symbols(value)
			
			value = new_code(value)
			py_bracket_items[key] = value
		# TODO elif type(py_bracket_items) == dict should raise exception
		else:
			# this is a list element, add it
			py_bracket_items.append(key)
			
	# if it was a list
	if type(py_bracket_items) == list:
		return new_list(py_bracket_items), index
	# else it was a dict
	else:
		return new_dict(py_bracket_items), index

def parse_string_to_function(code, index):
	"""
	Take a string of a funcion and make a funct object.
	"""
	# {x|x*2} / {*2} / {x}
	# Get over the '{'
	if code[index] == '{':
		index += 1
		
	function_indent, end_index = parse_string_to_indentation(code, index)
	
	last_indent = function_indent
	first_argument = []
	while last_indent == function_indent:
		# We need to check if first argument is code or argument
		# therefore, we check that everything is either variable, code or ","
		first_argument_parsed, end_index = parse_code_until(code, end_index, '|}\n')
		
		first_argument += first_argument_parsed
		
		if code[end_index-1] == '\n':
			last_indent, end_index = parse_string_to_indentation(code, end_index)
		else:
			break
		
	if all(new_str('name') in element or
		   (new_str('behaviour') in element and not new_str('args') in element) or
		   element == new_sym(',') or
		   element == new_sym('.') for element in first_argument):
		first_argument_type = 'argument'
		index = end_index
		first_argument = parsed_to_argument(first_argument)
	else:
		first_argument_type = 'code'
		# Parse the first argument until | or }
		first_argument, index = parse_string_to_multiline_code(code, index, until = '|}')

	# Check if there is more to parse, like in {x | x+1}
	if code[index-1] == '|':
		# There is a second argument. Parse it.
		# Also, replicate function indent with insert(code, ' '*function_indent, index)
		second_argument, index = parse_string_to_multiline_code(insert(code, ' '*function_indent, index)
														  , index, until = '}')
		# Remove the spaces we put 
		index -= function_indent
		# In this case, first argument is the function's argument,
		# and the second one is the behaviour
		# TODO check if first_argument_type is 'argument'
		return new_fun(first_argument, second_argument), index
	else:
		# This is either something like {+1}, aka code
		# or like {int x, y}, aka argument
		if first_argument_type == 'code':
			return new_fun(new_code([]), first_argument), index
		else:
			return first_argument, index
		
	

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
	return nydict(((new_str('variables'), new_list(variables)),))

def new_list(todo_list):
	# [1] = 1 actually
	if len(todo_list) == 1: 
		return todo_list[0]
	return nydict(tuple(
		[(new_int(couple[0]), couple[1]) 
		for couple 
		in enumerate(todo_list)]))
		
def new_dict(todo_dict):
	return nydict(tuple(todo_dict.items()))

"""
# FUNCTIONS #
"""

def replace_symbols(parsed_elements):
	"""
	Parse code's symbols, 1+1 --> sum(1,1)
	"""
	# Parse symbols in order:
	for parsing_symbols in definitions.symbols_parsing_order:
		index = 0
		while index < len(parsed_elements):
			parsed_element = parsed_elements[index]
			# Check if it'sa a symbol
			if new_str('symb') in parsed_element:
				# Check if it's a symbol we're searching for
				if parsed_element[new_str('symb')]['py_string'] in parsing_symbols:

					# Let's parse the symbol! Such a fun
					# Take the elements before the symbol
					before_symbol = parsed_elements[:index]
					# Take the elements aftwer the symbol
					after_symbol = parsed_elements[index+1:]
					# Store the symbol on a var and remove it, we don't
					# need it where we're going
					symbol = parsed_element
					del parsed_elements[index]
					index -= 1
					
					# elements is a list of coded (aka, list of list of parsed)
					# where we'll store the values to pass to the symbol's function
					# like, for 1+1, elements = [new_code(new_int(1)), new_code(new_int(1))]
					elements = [[]]
					
					# Now we have to take every element before the symbol
					# and add it to element, but we'll iter backwards!
					while before_symbol:
						# If there is the same symbol, ignore
						# it and keep parsing another element
						if before_symbol[-1] == symbol:
							del before_symbol[-1]
							elements.append([])
						# Any other symbol? stop.
						elif new_str('symb') in before_symbol[-1]: break
						# If it's anything else, add it to the parsed elements
						else: elements[-1].insert(0, before_symbol.pop())
						index -= 1
						
					# Parse elements *after* the symbol
					elements.append([])
					while after_symbol:
						# If there is the same symbol, ignore
						# it and keep parsing another element
						if after_symbol[0] == symbol:
							del after_symbol[0]
							elements.append([])
						# Any other symbol? stop.
						elif new_str('symb') in after_symbol[0]: break
						# If it's anything else, add it to the parsed elements
						else: elements[-1].append(after_symbol.pop(0))
							
					# Replace every element of elements with his code
					elements = [new_code(element) if len(element)>0
												  else new_code([new_var('implicit')])
												for element in elements]
					# Make the list and the code
					elements = new_code([new_list(elements)])
					# Re-make the entire parsed
					parsed_elements = before_symbol + [new_var(definitions.symbols_functions[symbol[new_str('symb')]['py_string']]), elements] + after_symbol
				
			index += 1
	return parsed_elements

def parsed_to_argument(parsed):
	
	# Here we will store variables we'll parse
	variables = []
	# Here we store conditions we'll parse - this should be reset
	# for every variable
	conditions = []
	# We also need to remember the previous conditions, because if condition
	# is empity, such as in 'int x, y' for y, we'll take the previous condition
	last_conditions = []
	parsed_iter = iter(parsed)
	for i, parse in enumerate(parsed_iter):

		# If it's a variable, add it to the conditions (e.g.: the 'int' in 'int x')
		if new_str('name') in parse:
			conditions.append([parse])
			
		# If it's a code, we also need to add it as condition (e.g.: 'int[=2] x')
		elif new_str('behaviour') in parse and not new_str('args') in parse:
			conditions[-1].append(parse)
		
		# Actually . is fine too ('x.y: 3')
		elif parse == new_sym('.'):
			conditions[-1].append(parsed[i+1][new_str('name')])
			next(parsed_iter)
			i+=1
			
		# If it's a ",", we finished parsing the conditions
		# If parse is last element of parsed, we're also over
		if parse == new_sym(',') or i+1==len(parsed):
			for i, conds in enumerate(conditions):
				last_var_conditions = conds[1:]
				conditions[i] = new_var(conds[0][new_str('name')]['py_string'], conds[1:])
			# The last variable we parsed it's actually the variable we're doing
			# e.g.: 'x' in 'int x'
			variable = conditions.pop()
			# If there is no condition, we have to take the previous one
			if len(conditions) == 0:
				conditions = [i for i in last_conditions]
			# Create the new variable with the conditions.
			new_variable = new_var(variable[new_str('name')]['py_string'], conditions+last_var_conditions)
			# Append it to the parsed variables
			variables.append(new_variable)
			
			last_conditions = [i for i in conditions]
			conditions = []
			
	return new_arg(variables)

def insert (source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]
