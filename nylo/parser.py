"""
This class brings together all the function used to parse nylo
code using the Code class.
"""

from code import Code
from string import ascii_letters, digits
from mesh import Mesh
from typing import Tuple, Dict, Union

Path = Tuple[str]
Call = Union[None, Path]

me: Path = ('self',)

class Parser:
	"""
	Here are all the parsers. The parser are called with a Code
	object where they can read values, while the output is stored
	into the mesh variable. Where to store the parsed values is
	given by the path argument. Path's type is Tuple[str].
	Parsing the value x with the path y means mesh[y] = x.
	Possible values are either no value (None), or a tuple with
	the context the variable is used, and the variable itself.
	"""
	
	def __init__(self, code: Code):
		"Creates a new instance of the parser."
		self.code = code
		self.mesh = Mesh({})
		
	def parse(self, path: Path, call: Call = None):
		"""
		This parses any value. This checks to what value the first
		character does corrispond and call the right parser.
		The call flag specifies if we're parsing a structure or a
		call. This is because calls behave differently: the variable
		inside are based on the context outside the call, and the
		standard return value for structures is different.
		
		>>> c = '(a: b)'
		>>> p = Parser(Code(c))
		>>> p.parse(('root',), None)
		>>> p.mesh[('root', 'a')]
		(('root', 'a'), ('b',))
		
		>>> c = '(d: x.y.z)'
		>>> p = Parser(Code(c))
		>>> p.parse(('a', 'b', 'c'), None)
		>>> p.mesh[('a', 'b', 'c', 'd')]
		(('a', 'b', 'c', 'd'), ('x', 'y', 'z'))
		
		>>> c = '(a: b)'
		>>> p = Parser(Code(c))
		>>> p.parse(('root',), ('root', 'a', 'r', 'y'))
		>>> p.mesh[('root', 'a')]
		(('root', 'a', 'r', 'y'), ('b',))
		
		>>> c = '_c.m'
		>>> p = Parser(Code(c))
		>>> p.parse(('root',), None)
		>>> p.mesh[('root',)]
		(('root',), ('_c', 'm'))
		
		>>> c = '0'
		>>> p = Parser(Code(c))
		>>> p.parse(('root',), None)
		>>> p.mesh[('root',)]
		(('root',), ('base', 'nat', 'zero'))
		
		>>> c = 'fib(n: n)'
		>>> p = Parser(Code(c))
		>>> p.parse(('x',), None)
		>>> p.mesh[('x', 'x.',)]
		(('x',), ('fib',))
		>>> p.mesh[('x',)]
		(('x', 'x.'), ('x.', 'self'))
		>>> p.mesh[('x', 'x.', 'n')]
		(('x',), ('n',))
		
		>>> c = '[1 2]'
		>>> p = Parser(Code(c))
		>>> p.parse(('x',), None)
		
		>>> c = "[I don't like square brackets]"
		>>> p = Parser(Code(c))
		>>> p.parse(('root',), None)
		Traceback (most recent call last):
			...
		SystemExit
		>>> p.parse((), None)
		Traceback (most recent call last):
			...
		ValueError: parse first argument cannot be ().
		"""
		if not path:
			raise ValueError('parse first argument cannot be ().')
		# Lists
		if self.code.is_in('['):
			self.plist(path)
		# Natural
		elif self.code.is_in(digits):
			self.nat(path)
		# Structure
		elif self.code.is_in('('):
			self.structure(path, call)
		# Variable
		elif self.code.is_in(ascii_letters + '$_'):
			self.mesh[path] = (call or path, self.var())
			# Call
			if self.code.is_in('('):
				hide = ('.'.join(path)+'.',)
				self.mesh[path+hide] = self.mesh[path]
				self.structure(path+hide, call or path)
		else:
			self.code.skip('string or structure')
				
	def var(self) -> Path:
		"""
		This method parses a variable. A variable is a tuple of string,
		that's taken by the variable split at '.' e.g.: ab.cd.ef will
		becode ('ab, 'cd', 'ef').
		
		>>> Parser(Code('ab1.cd2.ef3')).var()
		('ab1', 'cd2', 'ef3')
		>>> Parser(Code('abcd5')).var()
		('abcd5',)
		>>> Parser(Code('a_.$$._b')).var()
		('a_', '$$', '_b')
		
		These cases will raise an exception:
		
		>>> Parser(Code('')).var()
		Traceback (most recent call last):
			...
		SystemExit
		>>> Parser(Code('()')).var()
		Traceback (most recent call last):
			...
		SystemExit
		"""
		return tuple(
			self.code.skip_while(ascii_letters + digits + '$_.').split('.'))
	
	def nat(self, path: Path):
		"""
		This method parses a natural. It will build the nat data structure
		0 -> nat.zero
		1 -> nat(prev: nat.zero)
		2 -> nat(prev: nat(prev: nat.zero))
		
		>>> p = Parser(Code('0'))
		>>> p.nat(('x',))
		>>> p.mesh[('x',)]
		(('x',), ('base', 'nat', 'zero'))
		>>> p = Parser(Code('1'))
		>>> p.nat(('x',))
		>>> p.mesh[('x',)]
		(('x',), ('base', 'nat'))
		>>> p.mesh[('x', 'prev')]
		(('x', 'prev'), ('base', 'nat', 'zero'))
		>>> Parser(Code('hi!')).nat(('x',))
		Traceback (most recent call last):
			...
		SystemExit
		"""
		n = int(self.code.skip_while(digits))
		for i in range(n):
			self.mesh[path] = (path, ('base', 'nat'))
			path += ('prev',)
		self.mesh[path] = (path, ('base', 'nat', 'zero'))
		
	def plist(self, path: Path):
		"""
		This method parses a list. It will build the list data structure
		[] -> list.end
		[1] -> list(value: 1, next: list.end)
		[2] -> list(value: 1, next: list(value: 2, next: list.end))
		
		>>> p = Parser(Code('[]'))
		>>> p.plist(('x',))
		>>> p.mesh[('x',)]
		(('x',), ('base', 'list', 'end'))
		>>> p = Parser(Code('[0]'))
		>>> p.plist(('x',))
		>>> p.mesh[('x',)]
		(('x',), ('base', 'list'))
		>>> p.mesh[('x', 'value')]
		(('x', 'value'), ('base', 'nat', 'zero'))
		>>> p.mesh[('x', 'next')]
		(('x', 'next'), ('base', 'list', 'end'))
		>>> Parser(Code('hi!')).plist(('x',))
		Traceback (most recent call last):
			...
		SystemExit
		>>> Parser(Code('[1, 2]')).plist(('x',))
		>>> Parser(Code('[1 2]')).plist(('x',))
		"""
		self.code.skip('[')
		while not self.code.is_in(']'):
			self.parse(path+('value',))
			if self.code.is_in(','):
				self.code.skip(',')
			self.mesh[path] = (path, ('base', 'list'))
			path += ('next',)
		self.mesh[path] = (path, ('base', 'list', 'end'))
		self.code.skip(']')
	
	def structure(self, path: Path, call: Call):
		"""
		This method parses a structure. 
		First of all, it scans all couples of key: values inside the
		brackets and parses the values using path+key as path. An
		example is, if (a: 1) is parsed and the path is ('c', 'b'),
		the value 1 will stay with path ('c', 'b', 'a').
		After all the values, the structure either finish with ')', or
		there's another value after '->'.
		The structure can also either be a normal structure, like
		(a: 1), or a call, like b(a: 1).
		
		If the structure ends on ')' and is not a call: 
			A 'self' value will be created automatically, with a variable
			as value that refers to the structure itself. This is because
			writing `a.self` should be the same as `a`, and `b: (a: self)`
			will become `b: (a: b)`, so that `b.a` is `b`.
			The `me` variable refers to `('self',)`
			
		If the structure ends on '->' and is not a call:
			A 'self' value will also be created automatically, and any
			value after the -> will be put as value. This means that
			given a structure like `a: (-> 5)`, the variable `a.self`
			will return `5`. A variable is necessary, so `a: (b: 5 ->)`
			will raise an exception.
			
		When the structure is a call, we are parsing not in the 
		path itself, but rather in a 'hidden place'. This hidden
		place is given by `path+('.',)` or `path+hide`, as
		`hide`'s value is `('.',)`. This is because in path we
		want to put which value we want to extract from the call.
		I'll give you an example: let's take `fib(n: 10 -> sums)`.
		In `path+hide` we have `fib`, while in `path+hide + (n,)`
		we have `10`. This is a normal call, and we want to take
		from that call the `sums` value, so in `path` we will
		put a variable reference to `(hide, sums)` because we
		want to take the `sums` value in the hidden structure.
		fib(n: 10 -> sums) becomes (
		                               path: hide + ('sums',)
		                               path + hide: ('fib',)
		                               path + hide + ('n',): 10
								   )
		In order to avoid different value clashing, all hide values
		should have a different value. I therefore set the
		hide variable to the path i'm hiding plus .
								   
		If the structure ends on ')' and it is a call:
			When we have something like `fib(n: 10)` we want
			to get the standand value from the structure,
			so we reference hide+me, as `me` is `('self',)`.
			This is because function saves their standard
			return value in the 'self' variable, as we've seen
			before.
			If we're not calling a function but a class,
			'self' will not reference a value but the
			object itself. Since the value saved in `path` 
			is actually `path+hide`, we need to take off 
			the last value to save the value on `path`
			itself.
			
		If the structure ends on '->' and it is a call:
			If we have a value like `fib(n: 10 -> sums)`, we
			want to get that value, so we set `path` to
			`hide + ('sums',)`. This means that the variable
			that comes after '->' should be joined with `hide`
			and referenced in `path`.
			It could happen that no variable is provided
			after '->'.
			It would be something like `fib(n: 10 ->)`. We 
			don't want to take any specific value from the
			called structure, so we just reference the
			hidden structure itself.
			
		>>> c = '()'
		>>> p = Parser(Code(c))
		>>> p.structure(('x', 'y'), None)
		>>> p.mesh[('x', 'y')] #It should be None, so nothing
		>>> p.mesh[('x', 'y', 'self')]
		(('x', 'y'), ('x', 'y'))
		
		>>> c = '(a: ())'
		>>> p = Parser(Code(c))
		>>> p.structure(('k', 'y'), None)
		>>> p.mesh[('k', 'y', 'a')] #None, so nothing
		>>> p.mesh[('k', 'y')] #None, so nothing
		
		>>> c = '(a: (), b: (c: x.y.z))'
		>>> p = Parser(Code(c))
		>>> p.structure((), None)
		>>> p.mesh[('a',)] #None
		>>> p.mesh[('b', 'c')]
		(('b', 'c'), ('x', 'y', 'z'))
		>>> p.mesh[('self',)]
		((), ())
		
		>>> c = '(a: (), b: (-> x.y.z))'
		>>> p = Parser(Code(c))
		>>> p.structure((), None)
		>>> p.mesh[('a',)] #None
		>>> p.mesh[('b',)] #None
		>>> p.mesh[('b', 'self')]
		(('b', 'self'), ('x', 'y', 'z'))
		
		>>> c = '(n: n, m: ())'
		>>> p = Parser(Code(c))
		>>> p.structure(('x', 'y', '.'), ('x',))
		>>> p.mesh[('x', 'y', '.', 'n')]
		(('x',), ('n',))
		>>> p.mesh[('x', 'y', '.', 'm')] #None
		>>> p.mesh[('x', 'y')]
		(('x', 'y', '.'), ('.', 'self'))
		
		>>> c = '(n: () -> sums)'
		>>> p = Parser(Code(c))
		>>> p.structure(('x', '.'), ('x',))
		>>> p.mesh[('x',)]
		(('x', '.'), ('.', 'sums'))
		>>> p.mesh[('x', '.', 'n')] #None
		
		>>> c = '(->)'
		>>> p = Parser(Code(c))
		>>> p.structure(('x', '.'), ('x',))
		>>> p.mesh[('x',)]
		(('x', '.'), ('.',))
		
		>>> c = 'wait this is not a structure'
		>>> p = Parser(Code(c))
		>>> p.structure((), None)
		Traceback (most recent call last):
			...
		SystemExit
		"""
		listpath = path
		self.code.skip('(')
			
		while not (self.code.is_in(')') or self.code.startswith('->')):
			key: Path = self.var()
			self.code.skip(':')
			self.parse(path+key, call)
			while self.code.is_in(','):
				self.code.skip(',')
			
		if self.code.startswith('->'):
			[*map(self.code.skip, '->')]
			if call:
				self.mesh[path[:-1]] = (path, (path[-1],) + 
					(() if self.code.is_in(')') else self.var()))
			else:
				self.parse(path + me, call)
		else:
			if call:
				self.mesh[path[:-1]] = (path, (path[-1],) + me)
			else:
				self.mesh[path + me] = (path, path)
				
		if not path in self.mesh:
			self.mesh[path] = None
			
		self.code.skip(')')
			
