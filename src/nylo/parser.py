import collections
import string
import pprint

class Code:
	
	def __init__(self, code):
		self.code = [*code]
		self.whitespace()
		
	def skip(self, characters):
		if not self.is_in(characters):
			print(self.code)
			raise SyntaxError(f'Found {self.code[0]!r} while '
					  f'parsing for {characters!r}')
		popd = self.code.pop(0)
		self.whitespace()
		return popd
	
	def skip_while(self, characters):
		value = self.skip(characters)
		while self.is_in(characters):
			value += self.skip(characters)
		return value
	
	def is_in(self, characters):
		return self.code and self.code[0] in characters
	
	def whitespace(self):
		while self.code and self.code[0] in string.whitespace:
			self.code.pop(0)
			
def parse(code):
	mesh = collections.defaultdict(list)
	any(Code(code), (), mesh)
	return mesh

def structure(code, path, mesh):
	code.skip('(')
	while not code.is_in(')'):
		key = variable(code)
		code.skip(':')
		value = any(code, path+(key,), mesh)
		while code.is_in(','):
			code.skip(',')
	code.skip(')')


def variable(code):
	return code.skip_while(string.ascii_letters)


def any(code, path, mesh):
	while code.is_in('('+string.ascii_letters):
		if code.is_in('('):
			structure(code, path, mesh)
		elif code.is_in(string.ascii_letters):
			mesh[path].append(variable(code))
