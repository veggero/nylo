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
			
	def startswith(self, characters: str):
		return ''.join(self.code).startswith(characters)
			

def parse(code):
	mesh = collections.defaultdict(list)
	any(Code(code), (), mesh)
	return mesh


def structure(code, path: tuple, mesh, call=False):
	if not mesh[path]:
		mesh[path] = None
	code.skip('(')
	while not (code.is_in(')') or code.startswith('->')):
		key: tuple = variable(code)
		code.skip(':')
		any(code, path+(key,), mesh, call)
		while code.is_in(','):
			code.skip(',')
	if code.startswith('->'):
		code.skip('-')
		code.skip('>')
		any(code, path+('self',), mesh, call)
	code.skip(')')


def variable(code):
	return code.skip_while(string.ascii_letters)


def any(code, path: tuple, mesh, call=False):
	if code.is_in('('):
		structure(code, path, mesh, call)
	elif code.is_in(string.ascii_letters):
		mesh[path] = [call if call else path, variable(code)]
		while code.is_in('.'):
			code.skip('.')
			mesh[path].append(variable(code))
	if code.is_in('('):
		any(code, path, mesh, call=path)
		

def static(mesh):
	for key, value in mesh.items():
		if not value:
			continue
		scope = value.pop(0)
		for n in reversed(range(len(scope))):
			dir = key[:n]+(value[0],)
			if dir in mesh:
				mesh[key] = dir+tuple(value[1:])
				break
		else:
			raise SyntaxError(f'name {value[0]!r} is not defined.')
	return mesh


def evaluate(mesh, path):
	if mesh[path] is None:
		return path
	if mesh[path]:
		return evaluate(mesh, mesh[path])
	for i in reversed(range(len(path))): 
		subpath = path[:i]
		if mesh[subpath]:
			out = evaluate(mesh, mesh[subpath])

f = static(parse('''
(
	natural: (
		zero: ()
		positive: (
			prev: natural
		)
	)
	succ: (
		from: to.prev
		to: natural.positive(prev: from)
	)
	-> natural.positive(prev: natural.positive(prev: natural.zero))
)
'''))

pprint.pprint(f)
