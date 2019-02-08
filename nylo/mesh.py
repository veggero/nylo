"""
This class stores couples of key: value for nylo variables,
just like a normal dictionary, but provides more methods
to automatically bind variables and move group of variables.
"""

from typing import Tuple

class Mesh(dict):
	"""
	All of the nylo values are saved as a couples of key and values.
	Key is always a path, which is a tuple of strings. Values
	are either None on a couple (path, path) before binded, while
	after they're either None or paths. This is because every
	variable is a tuple of consecutive values, that are splitted
	at '.' in the sintax, e.g. `a.b.c` becomes `('a', 'b', 'c')`.
	The location is the path that should be written to access that
	value, so the path of `k` in `a: (b: (c: k))` is `a.b.c`, and
	the mesh is `{('a', 'b', 'c'): ('k',)}`. But before binding
	the context of the variable is also stored, aka from where you
	should start searching for the variable we're referring to.
	After binding just the absolute path is left.
	"""
	
	# Public:
	
	def __init__(self, *args):
		super().__init__(*args)
	
	def bind(self):
		"""
		This binds all the variable in the mesh.
		At the beginning, all the variable to bind are put in
		this notation: (context_path, referring_path). In order to 
		do this, it look for all the values (different from None),
		and takes the first element from the path, as that is
		the variable we are referring to, and trying to get it
		proprieties.
		e.g.: from `a.b.c` that becomes `('a', 'b', 'c')`, it takes
		just `a`.
		Now, we search for that value inside the mesh, in order
		to bind it. If we had something like:
		`(candy: 1, or: (candy: 2, uh: candy))`
		The `candy` variable (that is `('candy',)` ) is referring to
		the 2 value and not the 1. This is because we start searching
		from the most inner to the outer. The starting path is given
		from the context, so if we have
		`(('x', 'y', 'z',), ('a', 'b'))`
		We will search for, in this order:
		`('x', 'y', 'z', 'a')`
		`('x', 'y', 'a')`
		`('x', 'a')`
		`('a',)`
		If none of this variable exists, an expection will be raised.
		A special case is same, the only built-in function.
		
		>>> m = Mesh({
		...   ('a',): None,
		...   ('x',): (('x',), ('a',)),
		...   ('k',): (('k',), ('same',))
		... })
		>>> m.bind()
		>>> m[('x',)]
		('a',)
		>>> m[('k',)]
		('same',)
		
		>>> m = Mesh({
		...   ('a', 'b', 'c'): None,
		...   ('a', 'b', 'x'): (('a', 'b', 'x'), ('c', 'd'))
		... })
		>>> m.bind()
		>>> m[('a', 'b', 'x')]
		('a', 'b', 'c', 'd')
		
		>>> m = Mesh({
		...   ('a', 'f'): None,
		...   ('x', 'y'): (('a', 'b', 'c', 'd'), ('f', 'y', 'i'))
		... })
		>>> m.bind()
		>>> m[('x', 'y')]
		('a', 'f', 'y', 'i')
		
		>>> m = Mesh({
		...   ('a', 'p'): None,
		...   ('x', 'y'): (('a', 'b', 'c', 'd'), ('f', 'y', 'i'))
		... })
		>>> m.bind()
		Traceback (most recent call last):
			...
		SyntaxError: Name 'f' is not defined.
		"""
		self[('same',)] = None
		for key, value in self.items():
			if value is None:
				continue
			context, (var, *propr) = value
			for i in reversed(range(len(context)+1)):
				possible = context[:i] + (var,)
				if possible in self:
					self[key] = possible + tuple(propr)
					break
			else:
				raise SyntaxError(f'Name {var!r} is not defined in {key!r}.')
			
	def valueof(self, path: Tuple[str], done=()):
		"""
		This method returns the value of a path. The difference
		between this and the get method is that if the value
		is not in the dictionary, valueof will check if
		it's a propriety of another value. E.g., if you have
		`a.x`, maybe `a.x` is not in the dictionary, but
		maybe `x` is defined the `a` class.
		In order to do this, if the path (Tuple[str]) is
		not in the dictionary, it will remove the last
		elements until it finds a value that exists and
		is different from None, e.g.:
		`('a', 'b', 'c')`, then `('a', 'b')`, then `('a',)` then `()`.
		If found, it will call the chroot method, in order
		to transfer the proprieties from the object the found
		path is referring to to the found path itself. E.g.,
		if `('a', 'b')` is a path that refers to `('fib',)`
		`Mesh.chroot(('fib',), ('a', 'b'))` will be called.
		If even after the chroot the value still does not exist,
		it will go on, raising an error after `()`.
		Also, if the value to return is a path to another
		object, it will return the Mesh.valueof(that_path) instead.
		Finally, if the value is None, the path itself is returned.
		The done argument represent the already cloned values, in
		order to avoid them cloning forever.
		
		>>> m = Mesh({
		...   ('a',): None,
		...   ('a', 'k'): None,
		...   ('a', 'k', 'x'): None,
		...   ('b',): ('a',),
		...   ('c',): ('b', 'k'),
		...   ('e',): ('b',),
		...   ('f',): ('e',),
		...   ('g',): ('f', 'k')
		... })
		>>> m.valueof(('a',))
		('a',)
		>>> m.valueof(('a', 'k'))
		('a', 'k')
		>>> m.valueof(('b',))
		('a',)
		>>> m.valueof(('c',))
		('b', 'k')
		>>> m.valueof(('e',))
		('a',)
		>>> m.valueof(('d',))
		Traceback (most recent call last):
			...
		SyntaxError: Name 'd' is not defined.
		>>> m.valueof(('b', 'n'))
		Traceback (most recent call last):
			...
		SyntaxError: Name 'b.n' is not defined.
		>>> m.valueof(('g', 'x'))
		('g', 'x')
		>>> m.valueof(('g',))
		('f', 'k')
		>>> m.valueof(('f', 'k', 'x'))
		('f', 'k', 'x')
		"""
		if path in self:
			if isinstance(self[path], tuple):
				return self.valueof(self[path])
			assert self[path] is None
			return path
		for i in reversed(range(len(path))):
			subpath = path[:i]
			if not subpath in self or self[subpath] is None:
				continue
			if (self[subpath], subpath) in done:
				continue
			oldvalue = self[subpath]
			done += ((oldvalue, subpath),)
			self.clone(self[subpath], subpath, done)
			return self.valueof(path, done)
		raise SyntaxError(f'Name {path!r} is not defined.')
	
	# Private:
		
	def clone(self, oldroot: Tuple[str], newroot: Tuple[str], done=()):
		"""
		This function clones all the values in the dictionary
		where the keys starts with oldroot to the same
		path but with oldroot replaced with newroot, also
		changing the root in the value if it is a path.
		There are a couple of exception: 
		- If the path does not start with oldroot but it *is* 
		oldroot itself, it is cloned to newpath only if the
		value is not None.
		- If the value of a path does not start with oldroot
		but it *is* oldroot itself, it is not changed.
		- If the path ends with ('self',), and the value is
		oldroot itself, the values is changed to newpath.
		- If the path, after changing the oldroot with the newroot,
		already exists and is not None, that value is not cloned,
		and the old one is preserved.
		
		>>> m = Mesh({
		...	  ('fib', 'n'): ('nat',),
		...   ('fib', 'prev'): ('fib', 'n'),
		...   ('fib',): ('fib', 'prev'),
		...   ('fib', 'self'): ('fib',),
		...   ('fib', 'call'): ('fib',),
		...   ('fib', 'none'): None,
		...
		...   ('tgt',): ('fib',),
		...   ('tgt', 'n'): ('k',)
		... })
		>>> m.clone(('fib',), ('tgt',))
		>>> m[('tgt',)]
		('fib', 'prev')
		>>> m[('tgt', 'n')]
		('k',)
		>>> m[('tgt', 'prev')]
		('tgt', 'n')
		>>> m[('tgt', 'self')]
		('tgt',)
		>>> m[('tgt', 'call')]
		('fib',)
		>>> m[('tgt', 'none')] #(None	)
		
		>>> m.clone(('fib', 'none'), ('tgt',))
		>>> m[('tgt',)]
		('fib', 'prev')
		
		A special case is cloning from ('same'). That is the
		only built-in function. When cloning from it, this function
		will check if the Mesh.valueof(newpath+('first',)) is the
		same of newpath+('second',). If so, ('same', 'self') will have
		value ('same', 'then'), else ('same', 'else').
		
		>>> m = Mesh({
		...   ('same',): None,
		...   ('success',): None,
		...   ('fail',): None,
		...   ('c',): None,
		...   ('b',): ('c',),
		...   ('a',): ('same',),
		...   ('a', 'first'): ('b',),
		...   ('a', 'second'): ('c',),
		...   ('a', 'then'): ('success',),
		...   ('a', 'else'): ('fail',)
		... })
		>>> m.clone(('same',), ('a',))
		>>> m[('a', 'self')]
		('a', 'then')
		>>> m.valueof(('a', 'self'))
		('success',)
		"""
		delta = {}
		selfpath = oldroot + ('self',)
		if not oldroot in self:
			self.valueof(oldroot, done)
		blockeds = set()
		for key, value in sorted(self.items(), key=lambda x: x[0]):
			newkey = chroot(key, oldroot, newroot)
			if any(key[:len(b)] == b for b in blockeds):
				continue
			if newkey == key:
				continue
			if not (newkey in self and self[newkey] is not None):
				newval = (chroot(value, oldroot, newroot) 
						  if not value is None else None)
				delta[newkey] = newval
			else:
				blockeds.add(key)
		if oldroot in self and self[oldroot]:
			delta[newroot] = self[oldroot]
		if oldroot == ('same',):
			delta[newroot+('self',)] = newroot + (('then',) 
				if self.valueof(newroot+('first',), done) == self.valueof(newroot+('second',), done)
				else ('else',))
		if selfpath in self and self[selfpath] == oldroot:
			delta[newroot+('self',)] = newroot
		self.update(delta)
		
		
def chroot(path: Tuple[str], oldroot: Tuple[str], newroot: Tuple[str]) -> Tuple[str]:
	"""
	This is an helper function for Mesh.clone, that given a path,
	if it starts with oldroot, it replaces it with newroot.
	If the path is oldroot itself, it is not changed.
	
	>>> chroot(('a', 'b', 'c'), ('a', 'b'), ('x', 'y', 'z'))
	('x', 'y', 'z', 'c')
	>>> chroot(('k', 'y', 's'), (), ('u', 'r'))
	('u', 'r', 'k', 'y', 's')
	>>> chroot(('x', 'y', 'z'), ('x', 'y'), ())
	('z',)
	>>> chroot(('a', 'b'), ('a', 'b'), ('c', 'd'))
	('a', 'b')
	>>> chroot(('x', 'y', 'z'), ('a', 'b'), ('c', 'd'))
	('x', 'y', 'z')
	"""
	if path[:len(oldroot)] == oldroot and path != oldroot:
		return newroot + path[len(oldroot):]
	return path
