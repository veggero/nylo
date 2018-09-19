import collections
import string
import pprint

class Code:
	
	def __init__(self, code: str):
		self.code: list = [*code]
		self.whitespace()
		
	def assume(self, characters: str):
		if not self.is_in(characters):
			raise SyntaxError(f'Found {self.code[0]!r} while '
					  f'parsing for {characters!r}')
		
	def skip(self, characters: str):
		self.assume(characters)
		popd = self.code.pop(0)
		self.whitespace()
		return popd
	
	def skip_while(self, characters: str, value=''):
		self.assume(characters)
		while self.is_in(characters):
			value += self.code.pop(0)
		self.whitespace()
		return value
	
	def is_in(self, characters: str):
		return self.code and self.code[0] in characters
	
	def whitespace(self):
		while self.code and self.code[0] in string.whitespace:
			self.code.pop(0)
			

def parse(code):
	mesh = collections.defaultdict(list)
	any(Code(code), (), mesh)
	return mesh


def structure(code, path: tuple, mesh):
	code.skip('(')
	while not code.is_in(')'):
		key: tuple = variable(code)
		code.skip(':')
		any(code, path+(key,), mesh)
		while code.is_in(','):
			code.skip(',')
	code.skip(')')


def variable(code):
	return code.skip_while(string.ascii_letters)


def any(code, path: tuple, mesh):
	if code.is_in('('):
		structure(code, path, mesh)
	elif code.is_in(string.ascii_letters):
		mesh[path].append(variable(code))
	if code.is_in('.'):
		code.skip('.')
		any(code, path, mesh)
	elif code.is_in('('):
		any(code, path, mesh)
