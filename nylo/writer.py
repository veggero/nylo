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
		if evvalue in (('base', 'natural'), ('base', 'natural', 'zero')):
			return self.natural(value)
		else:
			return self.structure(value)
		
	def structure(self, value: Tuple[str]):
		"""
		This function will return the path to the value
		formatted using the point notation.
		
		>>> Writer.structure(None, ('x', 'y', 'z'))
		'x.y.z'
		>>> Writer.structure(None, ('a',))
		'a'
		"""
		return '.'.join(value)
	
	def natural(self, value: Tuple[str], n=0):
		"""
		This writer will check the previous value of the value,
		the previous of the previous, and so on, until the 
		base.natural.zero value is found. It will then return
		a string containing the number of previous it found.
		The n argument is beginning value. natural.zero with
		n=0 will be 0, natural.zero with n=10 will be 10.
		
		>>> w = Writer(Mesh({
		... ('base', 'natural'): None,
		... ('base', 'natural', 'zero'): None,
		... ('n',): ('base', 'natural'),
		... ('n', 'previous'): ('base', 'natural'),
		... ('n', 'previous', 'previous'): ('base', 'natural', 'zero'),
		... }))
		>>> w.natural(('n',))
		'2'
		
		>>> w = Writer(Mesh({
		... ('base', 'natural'): None,
		... ('base', 'natural', 'zero'): None,
		... ('n',): ('base', 'natural', 'zero'),
		... }))
		>>> w.natural(('n',))
		'0'
		
		>>> w = Writer(Mesh({
		... ('base', 'natural'): None,
		... ('base', 'natural', 'zero'): None,
		... ('not', 'a', 'natural'): None,
		... ('n',): ('base', 'natural'),
		... ('n', 'previous'): ('not', 'a', 'natural'),
		... }))
		>>> w.natural(('n',))
		Traceback (most recent call last):
			...
		ValueError: 'not.a.natural' found in a number.
		"""
		while self.mesh.valueof(value) != ('base', 'natural', 'zero'):
			if self.mesh.valueof(value) != ('base', 'natural'):
				nan = self.write(self.mesh.valueof(value))
				raise ValueError(f'{nan!r} found in a number.')
			value += ('previous',)
			n += 1
		return str(n)
		
