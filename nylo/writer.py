"""
This class is the opposite of a parser. Given a mesh and a value to
represent, it will give you back a string that would be parsed to
the such value.
"""

from mesh import Mesh
from typing import Tuple

class Writer:
	"""
	The writer works in the same way of the parser. There are
	many methods to write (=represent) all the possible data
	structures (numbers, lists, structures) plus a generic method
	write that picks the correct write function to call.
	The function will recursively call each other until the
	whole structure is written.
	"""
	
	def __init__(self, mesh: Mesh):
		"Creates a new instance of the writer."
		self.mesh = mesh
		
	def write(self, value: Tuple[str]):
		"""
		This function will check what type is the structure to
		represent (number, string, list, etc) and will call
		the right writer. It will before start with more specific
		types, such as naturals and strings, but if no type matches 
		it will eventually call the structure writer, as everything
		is a structure.
		
		>>> w = Writer(Mesh({
		...    ('x', 'y', 'z'): None
		... }))
		>>> w.write(('x', 'y', 'z'))
		'x.y.z'
		"""
		evvalue = self.mesh.valueof(value)
		if evvalue in (('base', 'nat', 'pos'), ('base', 'nat', 'zero')):
			return self.natural(value)
		elif evvalue in (('base', 'list', 'element'), ('base', 'list', 'end')):
			return self.wlist(value)
		elif evvalue == ('base', 'string'):
			return self.string(value)
		else:
			return self.structure(evvalue)
		
	def structure(self, value: Tuple[str]):
		"""
		This function will return the path to the value
		formatted using the point notation.
		
		>>> Writer.structure(None, ('x', 'y', 'z'))
		'x.y.z'
		>>> Writer.structure(None, ('a',))
		'a'
		>>> Writer.structure(None, ('a', 'a.'))
		'a'
		"""
		return '.'.join(v for v in value if not v.endswith('.'))
	
	def natural(self, value: Tuple[str], n=0):
		"""
		This writer will check the previous value of the value,
		the previous of the previous, and so on, until the 
		base.natural.zero value is found. It will then return
		a string containing the number of previous it found.
		The n argument is beginning value. natural.zero with
		n=0 will be 0, natural.zero with n=10 will be 10.
		
		>>> w = Writer(Mesh({
		... ('base', 'nat', 'pos'): None,
		... ('base', 'nat', 'zero'): None,
		... ('n',): ('base', 'nat', 'pos'),
		... ('n', 'prev'): ('base', 'nat', 'pos'),
		... ('n', 'prev', 'prev'): ('base', 'nat', 'zero'),
		... }))
		>>> w.natural(('n',))
		'2'
		
		>>> w = Writer(Mesh({
		... ('base', 'nat', 'pos'): None,
		... ('base', 'nat', 'zero'): None,
		... ('n',): ('base', 'nat', 'zero'),
		... }))
		>>> w.natural(('n',))
		'0'
		
		>>> w = Writer(Mesh({
		... ('base', 'nat', 'pos'): None,
		... ('base', 'nat', 'zero'): None,
		... ('not', 'a', 'nat'): None,
		... ('n',): ('base', 'nat', 'pos'),
		... ('n', 'prev'): ('not', 'a', 'nat'),
		... }))
		>>> w.natural(('n',))
		Traceback (most recent call last):
			...
		ValueError: 'not.a.nat' found in a number.
		"""
		while self.mesh.valueof(value) != ('base', 'nat', 'zero'):
			if self.mesh.valueof(value) == ('base', 'nat'):
				return 'base.nat.pos'
			if self.mesh.valueof(value) != ('base', 'nat', 'pos'):
				nan = self.write(self.mesh.valueof(value))
				raise ValueError(f'{nan!r} found in a number.')
			value += ('prev',)
			n += 1
		return str(n)
		
	def wlist(self, value: Tuple[str]):
		"""
		This writer will represent the linked list. It will
		print the 'value' and then proceed to the 'next' node.
		
		>>> w = Writer(Mesh({
		... ('base', 'list', 'element'): None,
		... ('base', 'list', 'end'): None,
		... ('l',): ('base', 'list', 'end'),
		... }))
		>>> w.wlist(('l',))
		'[]'
		
		>>> w = Writer(Mesh({
		... ('base', 'list', 'element'): None,
		... ('base', 'list', 'end'): None,
		... ('hi',): None,
		... ('l',): ('base', 'list', 'element'),
		... ('l', 'value'): ('hi',),
		... ('l', 'next'): ('base', 'list', 'end')
		... }))
		>>> w.wlist(('l',))
		'[hi]'
		
		>>> w = Writer(Mesh({
		... ('base', 'list', 'element'): None,
		... ('base', 'list', 'end'): None,
		... ('hi',): None,
		... ('l',): ('base', 'list', 'element'),
		... ('l', 'value'): ('hi',),
		... ('l', 'next'): ('base', 'list', 'element'),
		... ('l', 'next', 'value'): ('hi',),
		... ('l', 'next', 'next'): ('base', 'list', 'end')
		... }))
		>>> w.wlist(('l',))
		'[hi hi]'
		
		>>> w = Writer(Mesh({
		... ('base', 'list', 'element'): None,
		... ('base', 'list', 'end'): None,
		... ('hi',): None,
		... ('not', 'a', 'list'): None,
		... ('l',): ('base', 'list', 'element'),
		... ('l', 'value'): ('hi',),
		... ('l', 'next'): ('not', 'a', 'list')
		... }))
		>>> w.wlist(('l',))
		Traceback (most recent call last):
			...
		ValueError: 'not.a.list' found in a list.
		"""
		elements = []
		while self.mesh.valueof(value) != ('base', 'list', 'end'):
			if self.mesh.valueof(value) == ('base', 'list'):
				return 'base.list.element'
			if self.mesh.valueof(value) != ('base', 'list', 'element'):
				nal = self.write(self.mesh.valueof(value))
				raise ValueError(f'{nal!r} found in a list.')
			elements.append(self.write(value+('value',)))
			value += ('next',)
		return f'[{" ".join(elements)}]'
	
	def string(self, value: Tuple[str]):
		"""
		This writer will represent a string. It will do so
		by getting the represented list of character, and
		then mapping chr over them. This is quite ugly, but
		right now it should work well enough.
		"""
		if self.mesh.valueof(value+('characters',)) != ('base', 'list', 'element'):
			return 'base.string'
		elements = self.wlist(value+('characters',))
		return ''.join(map(chr, map(int, elements[1:-1].split(' '))))
