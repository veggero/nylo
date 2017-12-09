"""
# NYLO LANGUAGE DESCRIPTIVE OBJECTS #
"""

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
	new_var('print'): new_pyfunction(nyprint),
	new_var('sum'): new_pyfunction(nysum),
	new_var('to_list'): new_pyfunction(to_list),
	
	# CLASSES
	new_var('int'): new_arg([new_var('py_int')]), 
	new_var('str'): new_arg([new_var('py_string')]), 
	new_var('float'): new_arg([new_var('py_float')]),
	new_var('list'): new_arg([new_subtle_var(new_int(0))]),
	
	new_var('test'): new_pyfunction(test),
	
	}

"""
# BUILT-IN FUNCTIONS #
"""

def nyprint(thing):
	print(thing)
	return nydict(())

def nysum(numbers):
	return new_int(sum(numbers))

def to_list(args):
	# Actually, nyexecuter.assign made the whole work for us
	return new_list(args)

def int_to_python(ny_int):
	return ny_int['py_int']

def str_to_python(ny_str):
	return ny_str['py_string']

def test(k):
	print(k)
	return nydict(())
	
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
		yield nylist
		
	i = 0
	while 1:
		nyint_i = new_int(i) 
		if not nyint_i in nylist:
			raise StopIteration
		yield nylist[nyint_i]
		i+=1
		
def is_nylo_list(nyp): return new_int(0) in nyp
	
