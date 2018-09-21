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


def structure(code, path: tuple, mesh, call=False):
	mesh[path]
	code.skip('(')
	while not code.is_in(')'):
		key: tuple = variable(code)
		code.skip(':')
		any(code, path+(key,), mesh, call)
		while code.is_in(','):
			code.skip(',')
	code.skip(')')


def variable(code):
	return code.skip_while(string.ascii_letters)


def any(code, path: tuple, mesh, call=False):
	if code.is_in('('):
		structure(code, path, mesh, call)
	elif code.is_in(string.ascii_letters):
		mesh[path].append(variable(code))
	if code.is_in('.'):
		code.skip('.')
		any(code, path, mesh)
	elif code.is_in('('):
		any(code, path, mesh, call=True)
		

def static(mesh):
	for key, value in mesh.items():
		if not value:
			continue
		for n in range(len(key)+1):
			dir = key[:n]+(value[0],)
			if dir in mesh:
				mesh[key] = dir+tuple(value[1:])
				break
		else:
			raise SyntaxError(f'name {value[0]} is not defined.')
	return mesh
			

f = static(parse('''
(n: (), f: ()).n(f: f)
'''))

pprint.pprint(f)
