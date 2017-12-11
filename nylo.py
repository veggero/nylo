"""
This is the Parser Zero for Nylo, wrote by Veggero. This file has been created on the fifth of November.
You can absolutely what you want with this file. Please, be gentle, Senpai.

# TODO inb4 Nylo Zero					Dec 25 2017
00| ??? | Quick Instance Creation
01| ??? | Get Propriety
02| ??? | Set Propriety
03| FES | Make Getted Functions Working
04| ??? | Multiple Calls?
05| ??? | Exception Managing
06| FES | Built-in Function & Types
07| FES | Actual Error Traceback
08| FES | Return, Break, Continue, Else
09| FES | Better Object Calling
10| FES | Iteration on too many arguments
11| FES | Colons;

# TODO inb4 Nylo One					May 25 2018
00| FES | Special Arguments
01| FES | Binary, oct, ascii/utf string/number declarations
02| ??? | Special arguments
03| FES | Special chars in strings
04| FES | Errrors raising
"""

"""
# NYLO LANGUAGE DESCRIPTIVE OBJECTS #
"""

import string
import readline

__version__ = '0'
__author__ = 'Niccolo\' "Veggero" Venerandi'

symbols = {'+', '-', '/', '*', ',', '&', 'and', 'or', '=', ': ', '.', '>', '<', 'is_a',  ':'}

# TODO: sort
symbols_parsing_order = [
	{'.'},
	{':'},
	{'*', '/'},
	{'+', '-'},
	{'&', 'and', 'or', '=', '<', '>', 'is_a'},
	{': ', ','}
	]

unary_symbols = {'-', '+'}

symbols_functions = {'+': 'sum',
					 '-': 'sub',
					 '/': 'div',
					 '*': 'mul',
					 ',': 'to_list',
					 '&': 'join',
					 'and': 'all',
					 'or': 'any',
					 '=': 'equals',
					 ': ': 'set',
					 '.': 'get_propriety',
					 '>': 'greater_than',
					 '<': 'less_than',
					 'is_a': 'is_instance',
					 ':': 'range'}

def nylo():
	return {
		
	# VARIABLES
	new_var('print'): new_pyfunction(nyprint, new_arg([new_var('k')])),
	new_var('sum'): new_pyfunction(nysum, new_arg([new_var('k')])),
	new_var('to_list'): new_pyfunction(to_list, new_arg([new_var('k')])),
	
	# CLASSES
	# to-user
	new_var('int'): new_arg([new_var('py_int')]), 
	new_var('str'): new_arg([new_var('py_string')]), 
	new_var('float'): new_arg([new_var('py_float')]),
	new_var('list'): new_arg([new_subtle_var(new_int(0))]),	
	# to-nylo
	new_var('argument'): new_arg([new_var('variables', [new_var('list'), new_var('variable')])]),
	new_var('variable'): new_arg([new_var('name', [new_var('str')]), new_var('condition')]),
	new_var('function'): new_arg([new_var('behaviour'), new_var('args')]),
	new_var('pyfunction'): new_arg([new_var('python_function')]),
	new_var('overloaded_function'): new_arg([new_var('functions', [new_var('list', new_var('function'))])]),
	
	# NYLO-RELATED
	new_var('to_python'): new_overloded_fun([
		new_pyfunction(pass_argument, new_arg([new_var('k')])),
		new_pyfunction(nylo_integer_to_python, new_arg([new_var('k', [new_var('int')])])),
		new_pyfunction(nylo_string_to_python, new_arg([new_var('k', [new_var('str')])])),
		new_pyfunction(nylo_list_to_python, new_arg([new_var('k', [new_var('list')])])),
	]),
	new_var('to_str'): new_overloded_fun([
		new_pyfunction(to_str, new_arg([new_var('k')])),
		new_pyfunction(to_str, new_arg([new_var('k', [new_var('int')])])),
		new_pyfunction(to_str, new_arg([new_var('k', [new_var('str')])])),
		new_pyfunction(list_to_str, new_arg([new_var('k', [new_var('list')])])),
	]),
	new_var('call'): new_overloded_fun([
		new_pyfunction(call_argument, new_arg([new_var('k', [new_var('argument')]), new_var('g')])),
		new_pyfunction(call_function, new_arg([new_var('k', [new_var('function')]), new_var('g')])),
		new_pyfunction(call_pyfunction, new_arg([new_var('k', [new_var('pyfunction')]), new_var('g')])),
		new_pyfunction(call_overloaded_function, new_arg([new_var('k', [new_var('overloaded_function')]), new_var('g')])),
	]),
	new_var('set'): new_pyfunction(nyset, new_arg([new_var('arguments'), new_var('values')])),
	
	}

"""
# BUILT-IN FUNCTIONS #
"""

# TOOLS

def nyprint(thing):
	print(call_overloaded_function(fetch_variable(new_var('to_str')), to_nylo(thing))['py_string'])

def to_list(arg):
	# Actually, assign made the whole work for us
	return arg

# MATH

def nysum(numbers):
	if not type(numbers) == list:
		numbers = [numbers]
	return sum(numbers)

# NYLO-RELATED

def nylo_integer_to_python(nyint):
	return nyint['py_int']

def nylo_string_to_python(nystr):
	return nystr['py_string']

def nylo_list_to_python(pylist):
	return [call_overloaded_function(fetch_variable(new_var('to_python')), element) for element in nyparsed_to_iterable(pylist)]

def nyset(arguments, values):
	arguments, values = nylo_call_to_python(arguments, to_nylo(values))
	arguments, values = elaborate_arguments(arguments, values)
	if not arguments_follows_conditions(arguments, values): 
		raise_traceback_exception('Error with arguments types.')
		
	# Assign might've raised an exception, check for it
	if len(traceback[-1]['events']) > 0: return nydict(())

	traceback[-1]['variables'].update(assign(arguments, values))

def to_str(k):
	return str(k)

def list_to_str(k):
	return '['+', '.join([call_overloaded_function(fetch_variable(new_var('to_str')), to_nylo(element))['py_string'] for element in k])+']'

def to_nylo(python):
	if type(python) == int:
		return new_int(python)
	elif type(python) == float:
		return new_float(python)
	elif type(python) == str:
		return new_str(python)
	elif type(python) == list:
		return new_list([to_nylo(element) for element in python])
	elif python == None:
		return nydict(())
	else:
		return python

def call_function(function, values):
	values = to_nylo(values)
		
	arguments, values = nylo_call_to_python(function[new_str('args')], values)
	arguments, values = elaborate_arguments(arguments, values)
	arguments, values = elaborate_implicit_arguments(arguments, values)
	if not arguments_follows_conditions(arguments, values): 
		raise_traceback_exception('Error with arguments types.')
		
	# Assign might've raised an exception, check for it
	if len(traceback[-1]['events']) > 0: return nydict(())

	local_variables = assign(arguments, values)
	
	# Get the Nylo object of function's code
	function_code = function[new_str('behaviour')]
	# Run and return function's value
	return run_multiline_code(function_code, local_variables)

def call_argument(argument, values):
	values = to_nylo(values)
	arguments, values = nylo_call_to_python(argument, values)
	arguments, values = elaborate_arguments(arguments, values)
	if not arguments_follows_conditions(arguments, values): 
		raise_traceback_exception('Error with arguments types.')
		
	# Assign might've raised an exception, check for it
	if len(traceback[-1]['events']) > 0: return nydict(())

	# Manually assign values
	variables = {}
	for argument, value in zip(arguments, values): 
		variables[argument[new_str('name')]] = value
	return nydict(variables.items())
	
def call_pyfunction(pyfun, values):
	values = to_nylo(values)
	ny_to_python = fetch_variable(new_var('to_python'))
	arguments, values = nylo_call_to_python(pyfun[new_str('args')], values)
	arguments, values = elaborate_arguments(arguments, values)
	
	# A call to to_python will make a nylo object like {'py_int': 3} --> 3, 
	# making it easier to be used on the function. We should not do that if 
	# we are calling to_python function, or we'd have a loop
	if not pyfun in nyparsed_to_iterable(ny_to_python[new_str('functions')]):
		for i, value in enumerate(values):
			values[i] = call_overloaded_function(ny_to_python, value)

	# If there is only one argument, like [3], we should call just with it
	if len(values) == 0:
		values = values[0]
	#print(values)		
	# Call the python function, just like a python function
	python_output = pyfun['python_function'](*values)
	# Again, if this isn't to_python, we should make the output back to 
	# be nylonic
	if not pyfun in nyparsed_to_iterable(ny_to_python[new_str('functions')]):
		python_output = to_nylo(python_output)
	
	return python_output
	
def call_overloaded_function(overloaded, to_call_values):
	to_call_values = to_nylo(to_call_values)

	# So we check wich ones are good
	functions = nyparsed_to_iterable(overloaded[new_str('functions')])
	
	ok_functions = []
	for function in functions:
		arguments, values = nylo_call_to_python(function[new_str('args')], to_call_values)
		arguments, values = elaborate_arguments(arguments, values)
		arguments, values = elaborate_implicit_arguments(arguments, values)
		if arguments_follows_conditions(arguments, values):
			ok_functions.append(function)
		
	if len(ok_functions) == 0: raise_traceback_exception('Wrong types.')
	if len(traceback[-1]['events']) > 0: return nydict(())
	# Call last ok function
	return call(ok_functions[-1], to_call_values)

def pass_argument(arg):
	return arg

"""
#  ISTANCES INITIALIZATORS   #
# they take values and make  #
#    nydicts out of them     #
"""

# ABOUT CODING

def new_multiline_code(lines):
	return nydict(((new_str('lines'), new_list(lines)),))

def new_code(behaviour):
	return nydict(((new_str('behaviour'), new_list(behaviour)),))

# BASE ELEMENTS

def new_str(string):
	return nydict((('py_string', string),))

def new_int(integer):
	return nydict((('py_int', integer),))

def new_float(floating_point):
	return nydict((('py_float', floating_point),))

# CONSTRUCTS

def new_bool(boolean):
	if boolean:
		return nydict(((new_str('truthfulness'), new_int(1)),))
	else:
		return nydict(((new_str('truthfulness'), new_int(0)),))
	# Plot twist: {'thruthfulness': 0.5}

def new_sym(symbol):
	return nydict(((new_str('symb'), new_str(symbol)),))

def new_var(variable, conds=[]):
	return nydict(((new_str('name'), new_str(variable)),
				(new_str('condition'), new_list(conds))))

def new_subtle_var(variable, conds=[]):
	return nydict(((new_str('name'), variable),
				(new_str('condition'), new_list(conds))))

def new_fun(arguments, code):
	return nydict(((new_str('args'), arguments),
				(new_str('behaviour'), code)))

def new_pyfunction(pyf, arguments=[]):
	if arguments==[]:
		arguments = new_list([])
	return nydict((('python_function', pyf),
				(new_str('args'), arguments)))

def new_overloded_fun(functions):
	return nydict(((new_str('functions'), new_list(functions)),))

def new_arg(variables):
	return nydict(((new_str('variables'), new_list(variables)),))

def new_list(todo_list):
	# [1] = 1 actually
	#if len(todo_list) == 1: 
	#	return todo_list[0]
	return nydict(tuple(
		[(new_int(couple[0]), couple[1]) 
		for couple 
		in enumerate(todo_list)]))
		
def new_dict(todo_dict):
	return nydict(tuple(todo_dict.items()))

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
		raise IndexError("Key "+str(key)+" can't be found in nydict "+str(self)) # newfags can't avoid indexerror
	
	def __contains__(self, key):
		return any([couple[0]==key for couple in self.value])
			
	def __call__(self, key, value):
		"""
		Set a value and return the new tupledict. nylo_obj(('age', 16))('age', 17) --> nylo_obj(('age', 17))
		"""
		return [couple 
			if couple[0] != key
			else (couple[0], value)
			for couple in self.value]
	
	def __repr__(self):
		return '{'+', '.join([repr(son[0])+': '+repr(son[1]) for son in self.value])+'}'
	
	def __len__(self):
		return len(self.value)
	
	def __iter__(self):
		for key in self.value:
			yield key[0]
	
"""
# HELPER FUNCTIONS #
"""
	
def nyparsed_to_iterable(nylist):
	if nylist == nydict(()):
		return []
	
	if not new_int(0) in nylist:
		return [nylist]
		
	elements = []
	i = 0
	while 1:
		nyint_i = new_int(i) 
		if not nyint_i in nylist:
			return elements
		elements.append(nylist[nyint_i])
		i+=1
		
def is_nylo_list(nyp): return new_int(0) in nyp

"""
************************************************************ PARSER **********************************************************

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

def parse(string_code):
	"""
	Parse a string to Nylo Objects.
	"""
	# Add end of code
	string_code += '\n)'
	# Convert the string to code
	parsed, index = parse_string_to_multiline_code(string_code)
	
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
	- symbol    (parse_string_to_symbol)      in symbols
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
	elif ((code[index] in string.digits) or (code[index] == '.' and code[index+1] in string.digits)):
		parsed, index = parse_string_to_number(code, index)
	# Anything in the symbols set, is a symbol.
	elif code[index] in symbols:
		parsed, index = parse_string_to_symbol(code, index)
	# Then variables are anything that starts with a ascii-letter .
	# This means variables such as "_a" or "__thing" are not allowed.
	elif code[index] in string.ascii_letters:
		start_index = index
		parsed_string, index = parse_string(code, index)
		# The string is either a symbol, a argument, or a variable
		# If it's in symbols, it's a symbol
		if parsed_string in symbols:
			parsed = new_sym(parsed_string)
		# If it's in arguments, it's a arg
		# Any other case, it's a variable
		else:
			parsed = new_var(parsed_string)
	# ignore spaces and tabs 
	elif code[index] in ' \t':
		index += 1
		parsed = None
	else:
		# Unrecognized character
		raise SyntaxError("Unrecognized character while parsing: '"+code[index]+"'")
	return parsed, index

def parse_code_until(code, index, until='', ignore='\n\t;'):
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
	while code[index] in string.digits + string.ascii_letters + '_': index += 1
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
	parsed, index = parse_code_until(code, index, until+'\n;', ignore = '')
	
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
		# that is finished, so we need to return nydict(())
		elif indentation < last_line_indentation:
			for i in range(len(parsed_lines)): parsed_lines[i] = new_code(replace_symbols(parsed_lines[i]))
			return new_multiline_code(parsed_lines), index
			
		else:
			parsed, index = parse_code_until(code, after_indentation_index, until+'\n;', ignore = '')
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
		
	if code[index] in '\n;':
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
	while code[index] in string.digits + '.':
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
	while not code[index] in '\n;': index += 1
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
		first_argument_parsed, end_index = parse_code_until(code, end_index, '|}\n;')
		
		first_argument += first_argument_parsed
		
		if code[end_index-1] == '\n;':
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
			return new_fun(new_arg([]), first_argument), index
		else:
			return first_argument, index

"""
# FUNCTIONS #
"""

def replace_symbols(parsed_elements):
	"""
	Parse code's symbols, 1+1 --> sum(1,1)
	"""
	# Parse symbols in order:
	for parsing_symbols in symbols_parsing_order:
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
					
					if (symbol[new_str('symb')]['py_string'] in unary_symbols
							and elements[0] == []):
						del elements[0]
						
					# Replace every element of elements with his code
					elements = [(new_code(element) 	if len(element)>0
														else new_code([new_var('implicit')]))
												for element in elements]
						
					# Make the list and the code
					elements = new_code([new_list(elements)])
					# Re-make the entire parsed
					parsed_elements = before_symbol + [new_var(symbols_functions[symbol[new_str('symb')]['py_string']]), elements] + after_symbol
				
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
			
		# If it's a list, it contains only a code obj, therefore
		# we also need to add it as condition (e.g.: 'int[=2] x')
		elif is_nylo_list(parse) and len(parse) == 1:
			# TODO assert the only element is a function
			function_condition = parse[new_int(0)]
			conditions[-1].append(function_condition)
		
		# TODO
		"""# Actually . is fine too ('x.y: 3')
		elif parse == new_sym('.'):
			conditions[-1].append(parsed[i+1][new_str('name')])
			next(parsed_iter)
			i+=1"""
			
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


"""
********************************************************* EXECUTER ***********************************************************
"""

def run(code):
	"""
	Run some Nylo code.
	code --> string containing Nylo code to parse.
	"""
	
	# Parse the code, in order ta make it
	# easily readable.
	nylo_multiline_code = parse(code)
	
	# Clear the traceback; we'll write here
	# every call done.
	clear_traceback()
	
	return run_multiline_code(nylo_multiline_code, nylo())

def run_multiline_code(nylo_multiline_code, with_arguments):
	
	# We called a function; add the call to the
	# traceback stack.
	add_call_to_traceback({
		'code': nylo_multiline_code,
		'events': [],
		'line': -1,
		'variables': with_arguments,
		})
	
	# Get the Nylo object for codelines
	nylo_codelines = nylo_multiline_code[new_str('lines')]
	
	# Parse the codelines to an python iterable
	codelines = nyparsed_to_iterable(nylo_codelines)
	
	# Iter on the codelines and execute them all.
	for codeline in codelines:
		
		# Increase the line we're at
		increase_traceback_line()
		# Run the codeline
		output = run_codeline(codeline)

		# Manage the events (such as return, break, exceptions)
		for event in get_traceback_events():
			
			# If an exception is raised
			if 'raise' in event:
				
				# If an excepiton is raised, we should stop executing
				# lines, so stop the call
				close_traceback_call()
				
				if len(traceback)>1:
					# Pass the exception to the next call, until
					# it reaches the first one and it's print out`
					raise_traceback_event(event)
				else:
					# This is the last layer, therefore we should
					# print out the exception
					show_raised_exception(event['raise'])
					
				# Return standard value
				return nydict(())
			
			# If a value is returned
			elif 'return' in event:
				
				# Close the call and return the value
				close_traceback_call()
				return event['return']
			
	
	# If the code was one line long, we should juust return nydict(())
	# THIS NEEDS THE TRACEBACK TO BE STILL OPEN
	if traceback[-1]['line'] == 0:
		close_traceback_call()
		return output
	
	close_traceback_call()
	return nydict(())
		
		
def run_codeline(codeline):
	"""
	Run a single Nylo Codeline object.
	"""
	# Get the object for the line
	nylo_code = codeline[new_str('behaviour')]
	# Convert the Nylo list to a Python list
	py_code = (nyparsed_to_iterable(nylo_code))

	# Execute every bracket and replace variables
	py_code = execute_brackets(py_code)
	if len(traceback[-1]['events'])>0: return nydict(())

	# The first element of a line is the object that's gonna be called
	# e.g.: print 'hi' --> print is gonna be called
	called = py_code.pop(0)
	
	# While there are arguments after the calling object, take
	# them and use them to call the called object.
	while py_code: 
		called = call_overloaded_function(fetch_variable(new_var('call')), to_nylo([called, py_code.pop(0)]) )
		if len(traceback[-1]['events']) > 0: return nydict(())
		
	# What's left is what we should return nydict(())
	return called
	
def call(called, argument):
	"""
	Manage a call of an object (called) with another (argument).
	### TODO: THIS IS GOING TO BE COMPLETLY REPLACED WITH 
	### A CALL TO THE NYLO FUNCTION CALL(), IN ORDER TO PROVIDE
	### CUSTOMIZABLE CALLS; yeahh let's code something I'm not gonna use
	"""
	# Check what type of callable object is 'called':
	
	# If it has 'python_function', it's actually a Python
	# function; You can't really define them within Nylo
	# syntax, so usually they're built-ins
	if 'python_function' in called:
		
		return call_pyfunction(called, argument)
	
	return call_overloaded_function(fetch_variable(new_var('call')), argument)
	
"""
# DATA MANIPULATION RELATED #
"""
	
def fetch_variable(variable, default=None):
	"""
	Get the value of a variable from the trackeback.
	"""
	# Get the name of the variable to fetch
	to_fetch_variable_name = variable[new_str('name')]
	
	# Iter in the traceback reversed, to get all the variables, 
	# from the most local ones to the global ones
	for flow in traceback[::-1]:
		local_variables = flow['variables']
		for local_variable in local_variables:
			# If has the same name as the one we're searching, return it's value
			if local_variable[new_str('name')] == to_fetch_variable_name:
				return local_variables[local_variable]
	
	if default != None:
		return default
	# We found nothing; return an exception
	raise_traceback_exception('Variable '+to_fetch_variable_name['py_string']+' not found.')
	
def show_raised_exception(Ex):
	"""
	Print onscreen an exception.
	"""
	print('~~ ERROR ~~')
	print(Ex['py_string'])
	
def nylo_call_to_python(ny_arguments, ny_values):
	"""
	Take a Nylo argument and object and return it as python lists.
	"""
	py_arguments = (nyparsed_to_iterable(ny_arguments[new_str('variables')]))
	py_values = (nyparsed_to_iterable(ny_values))
	return py_arguments, py_values

def elaborate_arguments(py_arguments, py_values):
	"""
	Change arguments and values to match the best, e.g.: sum ([[1,2]]) --> sum (1,2)
	"""
	# {x|}(1,2,3) --> {x|}([1,2,3])
	py_values = [new_list(py_values)]
	
	# {x|}([[[1,2,3]]]) --> {x|}([1,2,3]) 
	if len(py_arguments) == 1 :
		while len(py_values[0]) == 1 and is_nylo_list(py_values[0]):
			py_values = (nyparsed_to_iterable(py_values[0]))
			
	# {a,b,c|}([1,2,3]) --> {a,b,c|}(1,2,3) 
	else:
		while len(py_values) == 1 and is_nylo_list(py_values[0]):
			py_values = (nyparsed_to_iterable(py_values[0]))
			
	return py_arguments, py_values
	
def elaborate_implicit_arguments(py_arguments, py_values):
	"""
	Add to arguments implicit variable if needed, e.g.: {>3} --> {implicit|implicit>3}
	"""
	# {>2}(3) --> {i|i>2}(3)
	if len(py_arguments) == 0:
		py_arguments = [new_var('implicit')]
			
	# {n|1+}(3) --> {n|1+n}(3)
	if len(py_arguments) == 1 and len(py_values) == 1:
		py_arguments.append(new_var('implicit'))
		py_values *= 2
		
	return py_arguments, py_values
	
def assign(py_arguments, py_values):
	"""
	Assign a list of argument to theirs values, and return the new python
	dictionary of variables.
	"""
	# Iter on both list of arguments and values at the same time
	variables = {}
	for argument, value in zip(py_arguments, py_values): 
		if new_str('behaviour') in value and new_str('args') in value:
			var_to_replace = fetch_variable(argument, default=[])
			# If the variable to be replaced is a overloaded function, we should add
			# ours to the overloadeds
			if new_str('behaviour') in var_to_replace and new_str('args') in var_to_replace:
				variables[argument] = new_overloded_fun([var_to_replace, value])
			elif new_str('functions') in var_to_replace:
				variables[argument] = new_overloded_fun(nyparsed_to_iterable(var_to_replace[new_str('functions')])+[value])
			else:
				variables[argument] = value
		else:
			variables[argument] = value

	return variables

def arguments_follows_conditions(py_arguments, py_values):
	"""
	Check if an an arguments can be called with a value.
	"""
	# {a,b|}(1,2,3) --> fk u
	if len(py_arguments) != len(py_values):
		raise_traceback_exception('Wrong nuber of arguments.')
		return True
	
	# Iter on both list of arguments and values at the same time
	conditions_outs = all(
		follows_conditions(value, 
				nyparsed_to_iterable(argument[new_str('condition')]))
		for argument, value in zip(py_arguments, py_values))
		
	return conditions_outs

def follows_conditions(value, conditions):
	"""
	Check if a value follow a condition.
	point: {int x, y}
	point k: ['x':3, 'y':4]
	"""
	
	# No condition? Value's okay
	if len(conditions) == 0:
		return True
	
	# We only check ONE condition here (the first one), and the
	# other recursively. So we take the first one.
	condition_to_check = conditions.pop(0)
		
	# First of all, the parser puts in the condition of the condition_to_check
	# Check if it's there first obviusly: (lol, not so obvius apparently, forgot about it at first time)
	if len(condition_to_check[new_str('condition')]) == 1:
		# the code we should call - but its' code and not a function, so we make it up
		function_code = condition_to_check[new_str('condition')][new_int(0)]
		# We'll use the same name of the class we're checking as argument - like, in int[=0], the function
		# is gonna be {int|=0}
		function_arguments = new_arg([
			new_var(
				condition_to_check[new_str('name')]
				)
			])
		function_to_check = new_fun(function_arguments, function_code)
		# Nice, we just have to call it!
		function_condition_is_ok = call(function_to_check, value)
		if function_condition_is_ok == new_bool(False):
			return False
	
	class_to_check = fetch_variable(condition_to_check)
	# fetch_variable might've raise an error, if so return nydict(())
	if len(traceback[-1]['events']) > 0:
		return nydict(())
	variables_to_check = class_to_check[new_str('variables')]
	py_variables_to_check = nyparsed_to_iterable(variables_to_check)
		
	# If it's a built-in, such as strings, has python strings instead of 
	# nylo strings - we need to make them nylo strings
	if str in (type(prop) for prop in value):
		value = nydict((new_str(prop), value[prop]) for prop in value)
	
	# Now we iterate both on value proprieties and class
	# variables and check if the conditions for every
	# propriety are ok
	for class_propriety in py_variables_to_check:
		if class_propriety[new_str('name')] in value:
			class_condition_is_ok = follows_conditions(value[class_propriety[new_str('name')]],
				(nyparsed_to_iterable(class_propriety[new_str('condition')])))
			if not class_condition_is_ok:
				return False
			
		# If value hasn't a propriety of the class, it's not
		# that class
		else:
			return False

	# If value is a list we iter on it and call follows_conditions
	# again for every argument - in this way, "[1,2,3]" "list int"
	# will pass [1,2,3] to "list" and every single number to "int"
	# TODO use nylo iterable instead of for
	return all(follows_conditions(new_value, conditions)
			for new_value in nyparsed_to_iterable(value))

def execute_brackets(py_code):
	"""
	Execute every variable, bracket and list in a Nylo codeline.
	"""
	for i, parsed_element in enumerate(py_code): 
		# If it has behaviour and not args, it's a code, and we should execute it
		if new_str('behaviour') in parsed_element and not new_str('args') in parsed_element:
			py_code[i] = run_codeline(parsed_element)
			if len(traceback[-1]['events'])>0: return nydict(())
			
		# If it's a list we execute it
		# just like a piece of code.
		elif is_nylo_list(parsed_element):
			py_code[i] = new_list(
				execute_brackets(
					list(
						nyparsed_to_iterable(
							parsed_element))))
			if len(traceback[-1]['events'])>0: return nydict(())
						
		parsed_element = py_code[i]
		# We also need to check if any propriety of the parsed element
		# has 'behaviour' in proprieties and if so execute them
		new_parsed_element = {}
		for prop in parsed_element:
			val = parsed_element[prop]
			if not type(prop) == str:
				if new_str('behaviour') in prop and not new_str('args') in prop:
					prop = run_codeline(prop)
				if new_str('behaviour') in val and not new_str('args') in val:
					val = run_codeline(val)
			new_parsed_element[prop] = val
			
		py_code[i] = nydict(new_parsed_element.items())
		parsed_element = py_code[i]
		
		# If it has a condition, it's a variable, and we should
		# fetch its value
		if new_str('condition') in parsed_element:
			py_code[i] = fetch_variable(parsed_element)
		if len(traceback[-1]['events'])>0: return nydict(())
	return py_code

"""
# TRACEBACK MANAGING RELATED #
"""

def clear_traceback():
	global traceback
	traceback = []
	
def add_call_to_traceback(call):
	traceback.append(call)
	
def increase_traceback_line():
	traceback[-1]['line'] += 1
	
def raise_traceback_event(event):
	traceback[-1]['events'].append(event)

def raise_traceback_exception(message):
	raise_traceback_event({'raise': new_str(message)})
	
def get_traceback_events():
	for i, event in enumerate(traceback[-1]['events']):
		del traceback[-1]['events'][i]
		yield event
		
def close_traceback_call():
	del traceback[-1]


if __name__ == "__main__":
	clear_traceback()
	
	# Base process to remember variables
	add_call_to_traceback({
		'code': None,
		'events': [],
		'line': None,
		'variables': nylo(),
	})
		
	while 1:
	
		out = run_codeline(nyparsed_to_iterable(parse(input("nylo> "))[new_str('lines')])[0])
		
		# Manage the events (such as return, break, exceptions)
		for event in get_traceback_events():
			
			# If an exception is raised
			if 'raise' in event:
				
				# This is the last layer, therefore we should
				# print out the exception
				show_raised_exception(event['raise'])
			
		if out != nydict(()):
			call_pyfunction(fetch_variable(new_var('print')), out)
