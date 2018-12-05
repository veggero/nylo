import collections
import string
import random
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
		random_outer = '.'+path[-2]+str(random.random())[2:5]
		path += (random_outer,)
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
				mesh[path[:-1]] = [path, random_outer]
				#kwd = 'self'
			else:
				mesh[path[:-1]] = [path, random_outer, variable(code)]
				#kwd = variable(code)
		else:
			any(code, path+('self',), mesh, call)
	else:
		if call:
			mesh[path[:-1]] = [path, random_outer, 'self']
		else:
			mesh[path+('self',)] = [path, *path]
	code.skip(')')
	if not mesh[path]:
		mesh[path] = None


def variable(code):
	# a.b.c should be moved here
	return code.skip_while(Code.characters_while)


def any(code, path: tuple, mesh, call=False):
	if code.is_in('('):
		structure(code, path, mesh, call)
	elif code.is_in(Code.characters_start):
		if not mesh[path]:
			mesh[path] = [call or path]
		mesh[path].append(variable(code))
		while code.is_in('.'):
			code.skip('.')
			mesh[path].append(variable(code))
		if code.is_in('('):
			any(code, path, mesh, call or path)
	if code.is_in('|'):
		code.skip('|')
		newmesh = collections.defaultdict(list)
		if not mesh['alternatives']:
			mesh['alternatives'] = {}
		mesh['alternatives'][path] = any(code, path, newmesh, call)
		

def static(mesh):
	for key, value in mesh.items():
		if not value:
			continue
		if not isinstance(key, tuple):
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
		
		if (subpath, newsubpath) in mesh['chrootsmade']:
			continue
		if mesh[newsubpath]:
			mesh[subpath] = mesh[newsubpath]
		if mesh[newsubpath+('self',)] and mesh[newsubpath+('self',)] == newsubpath:
			mesh[subpath+('self',)] = subpath
		for oldpath in mesh.copy():
			if not isinstance(oldpath, tuple):
				continue
			newpath = chroot(oldpath, subpath, newsubpath)
			
			if mesh[newpath] and mesh[oldpath] and oldpath != newpath:
				newtype = evaluate(mesh, mesh[newpath])
				oldtype = evaluate(mesh, mesh[oldpath])
				instance = newtype[:len(oldtype)] == oldtype
				if not instance:
					print('fuck', oldtype, newtype)
					print('miscarriage @', newpath)
				
			if oldpath == newpath or mesh[newpath]:
				continue
			mesh[newpath] = chroot(mesh[oldpath], subpath, newsubpath)
		mesh['chrootsmade'].append((subpath, newsubpath))
									
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
			if i > 100:
				return 'infinite'
		if evaluate(mesh, ('root', 'self')+('prev',)*i) != ('root', 'nat', 'zero',):
			raise ValueError('Non-zero value inside nat.prev')
		return i
	if type_to_repr == ('root', 'nat', 'zero',):
		return 0
	return type_to_repr
	

f = static(parse('''(
nat: (
	prev: nat
	zero: ()
	succ: nat(prev: self)
)

bool: (
	true: ()
	false: ()
)

sum: (
	a: nat.zero
	b: nat
	-> b
) | (
	a: nat
	b: nat
	-> sum(
		a: a.prev
		b: b.succ
	)
)

eq: (
	a: nat.zero
	b: nat.zero
	-> bool.true
) | (
	a: nat.zero
	b: nat
	-> bool.false
) | (
	a: nat
	b: nat.zero
	-> bool.false
) | (
	a: nat
	b: nat
	-> bool.true
)

or: (
	a: bool.false
	b: bool
	-> b
) | (
	a: bool.true
	b: bool
	-> b
)

if: (
	cond: bool.true
	then: root
	else: root
	-> then
) | (
	cond: bool.false
	then: root
	else: root
	-> else
)

fib: (
	n: nat.zero | nat(prev: nat.zero)
	-> nat(prev: nat.zero)
) | (
	n: nat(prev: nat)
	-> sum(
		a: fib(n: n.prev)
		b: fib(n: n.prev.prev)
	)
)

fibb: (
	n: nat  
	prevs: sum(
		a: fib(n: n.prev) 
		b: fib(n: n.prev.prev)
	)
	-> if(
		cond: or(
			a: eq(a: n, b: nat.zero)
			b: eq(a: n, b: nat(prev: nat.zero)) 
		),
		then: nat(prev: nat.zero)
		else: prevs 
	)
)

-> fib(n: nat(prev: nat.zero))
)'''))
f = represent(f)
print(f)

print('*****')

g = represent(static(parse('''(
a: ()
b: ()
c: ()
d: ()
e: (k: b -> c) | (k: a -> d)
-> e(k: a)
)''')))

pprint.pprint(g)
