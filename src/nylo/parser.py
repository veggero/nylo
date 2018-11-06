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
					  f'parsing for {characters!r} #SAD')
		
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
	
	characters_start = string.ascii_letters + "$_"
	characters_while = characters_start + string.digits
			

def parse(code):
	mesh = collections.defaultdict(list)
	any(Code(code), ('root',), mesh)
	return mesh


def structure(code, path: tuple, mesh, call=False):
	if call:
		path += ('.outer',)
		mesh[path] = mesh[path[:-1]]
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
		if call:
			if code.is_in(')'):
				kwd = 'self'
			else:
				kwd = variable(code)
			mesh[path[:-1]] = [path, '.outer', kwd]
		else:
			any(code, path+('self',), mesh, call)
	elif call:
		mesh[path[:-1]] = [path, '.outer']
	code.skip(')')
	if not mesh[path]:
		mesh[path] = None


def variable(code):
	return code.skip_while(Code.characters_while)


def any(code, path: tuple, mesh, call=False):
	if code.is_in('('):
		structure(code, path, mesh, call)
	elif code.is_in(Code.characters_start):
		if not mesh[path]:
			mesh[path] = [call if call else path]
		mesh[path].append(variable(code))
		while code.is_in('.'):
			code.skip('.')
			mesh[path].append(variable(code))
		if code.is_in('('):
			any(code, path, mesh, call or path)
		

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
			raise SyntaxError(f'name {value[0]!r}'
					   ' is not defined. #SIGH')
	return mesh


def evaluate(mesh, path):
	value = seek(mesh, path)
	if value is None:
		return path
	if value == []:
		raise SyntaxError(f'Could not find value of {path!r}'
				   ' while interpreting. #BAD')
	return evaluate(mesh, value)


def seek(mesh, path):
	if mesh[path] != []:
		if isinstance(mesh[path], tuple) and mesh[path][-1] == '$':
			toev = evaluate(mesh, mesh[path][:-1])[-1]
			mesh[path] = path[:-1]+(toev+'$',)
			return seek(mesh, path)
		else:
			return mesh[path]
	for i in reversed(range(len(path))):
		subpath = path[:i]
		if not mesh[subpath]:
			continue
		newsubpath = mesh[subpath]
		for oldpath in mesh.copy():
			newpath = chroot(oldpath, subpath, newsubpath)
			if mesh[newsubpath]:
				mesh[subpath] = mesh[newsubpath]
			if oldpath == newpath or mesh[newpath]:
				continue
			mesh[newpath] = chroot(mesh[oldpath], subpath, newsubpath)
		return chroot(path, subpath, newsubpath)
	return []
		
		
def chroot(path, oldsubpath, newsubpath):
	if not isinstance(path, tuple):
		return path
	if path[:len(newsubpath)] == newsubpath and path != newsubpath:
		return oldsubpath + path[len(newsubpath):]
	return path


def represent(mesh):
	type_to_repr = evaluate(mesh, ('root', 'self'))
	if type_to_repr == ('root', 'nat',):
		i = 1
		while evaluate(mesh, ('root', 'self')+('prev',)*i) == ('root', 'nat',):
			i += 1
		if evaluate(mesh, ('root', 'self')+('prev',)*i) != ('root', 'nat', 'zero',):
			raise ValueError('Non-zero value inside nat.prev')
		return i
	if type_to_repr == ('root', 'nat', 'zero',):
		return 0
	return type_to_repr
	

f = represent(static(parse('''(
nat: (
	prev: nat
	zero: ()
)
bool: (
	true: ()
	false: ()
)
sum: (
	a: nat
	b: nat
	nat$: sum(
		a: a.prev
		b: nat(prev: b)
	->)
	zero$: b
	-> a.$
)
eq: (
	a: nat
	b: nat
	left: (
		result: a.$
		nat$: aright.result
		zero$: bright.result
	)
	aright: (
		result: b.$
		nat$: eq(
			a: a.prev
			b: b.prev
		->)
		zero$: bool.false
	)
	bright: (
		result: b.$
		nat$: bool.false
		zero$: bool.true
	)
	-> left.result
)
or: (
	a: bool
	b: bool
	true$: bool.true
	false$: b
	-> a.$
)
if: (
	cond: bool
	then: root
	else: root
	true$: then
	false$: else
	-> cond.$
)
fib: (
	n: nat  
	prevs: sum(
		a: fib(n: n.prev ->) 
		b: fib(n: n.prev.prev ->)
	->)
	end: or(
		a: eq(a: n, b: nat.zero ->)
		b: eq(a: n, b: nat(prev: nat.zero) ->) 
	->)
	-> if(
		cond: end,
		then: nat(prev: nat.zero)
		else: prevs 
	->)
)
-> fib(n: nat.zero ->)
)''')))

pprint.pprint(f)
