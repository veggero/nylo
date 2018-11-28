"""
This is a class that aims to make parsing a little bit easier.
It creates an abstraction layer between the parser and the
code string itself. This class will provide methods to
get characters from code, automatically removing whitespace,
and checking if there's anything wrong (Wrong syntax or
EOF while parsing)
"""

import string
from typing import List

class Code:
	"""
	Abstraction layer between parsers and code string.
	The code is stored as a list of characters to make removing
	parsed characters easier.
	Every time a character is parsed, it will be removed from
	the list of characters. In this way, the character that's being
	parsed, or 'current character', is always the first one.
	This class implements methods to check what's the current character,
	and to parse a character (that removes it from the list).
	This class also implements method to get charaters until a
	certain one (e.g.: parse until the character is ").
	Whitespace is always ignored, except in "parse until [x]"
	methods, as spaces should be parsed in strings.
	"""
	
	# Public
	
	def __init__(self, code: str):
		"Creates a new instance"
		self.code: List[str] = [*code]
		# Already remove trailing whitespace
		self.whitespace()
		
	def skip(self, characters: str) -> str:
		"""
		This method skips the current character by
		removing it from the list of characters.
		It will also assume the current characters is
		within the given characters.
		It will also return the parsed character.
		
		>>> abc = Code('abc')
		
		The first current character is 'a', which is
		inside the string 'a', so it is removed and returned.
		>>> abc.skip('a')
		'a'
		
		The next current character is 'b', which
		is in 'bc', so it will be returned.
		>>> abc.skip('bc')
		'b'
		
		The next current character is 'c', which
		is not in 'ab', so an exception will be raised.
		>>> abc.skip('ab')
		Traceback (most recent call last):
			...
		SyntaxError: Unexpected 'c' while parsing for 'ab'.
		
		'c' has not be removed, so it's still in the code.
		>>> abc.code
		['c']
		
		Trying to skip a character from an empty code will also
		raise an exception.
		>>> Code.skip(Code(''), 'abc')
		Traceback (most recent call last):
			...
		SyntaxError: Unexpected 'EOF' while parsing for 'abc'.
		"""
		self.assume(characters)
		popd: str = self.code.pop(0)
		# Remove possible whitespace
		self.whitespace()
		return popd
		
	def skip_while(self, characters: str, reverse=False) -> str:
		"""
		This method will return all the charaters that
		are inside the given character list. It will also
		assume that the current charater (the first
		charater to be returned) is indeed within the
		given characters.
		The reverse flag will make this method check
		until [x] insead of while [x]. This means that
		all the charaters will be returned while they're
		not inside the characters.
		
		>>> abc = Code('abcdefghilmn')
		>>> abc.skip_while('cab')
		'abc'
		
		We are left with 'defghilmn'.
		Return chars until 'h', 'g' or 'i' is met. In
		this case, 'g' is met after 'def'.
		>>> abc.skip_while('hgi', reverse=True)
		'def'
		
		Try to skip all character in 'xyz'. No character
		is in 'xyz', so an error is raised.
		>>> abc.skip_while('xyz')
		Traceback (most recent call last):
			...
		SyntaxError: Unexpected 'g' while parsing for 'xyz'.
		
		We are left with 'ghilmn'.
		This returns all character until anything in 'ghi',
		but 'g' is immediately met, so '' is returned.
		>>> abc.skip_while('ghi', reverse=True)
		''
		
		An empty string will also raise an exception.
		>>> Code.skip_while(Code(''), 'abc')
		Traceback (most recent call last):
			...
		SyntaxError: Unexpected 'EOF' while parsing for 'abc'.
		"""
		# Check if there's at least one character.
		# This is unnecessary if we're skipping until
		# we meet a certain value
		if not reverse:
			self.assume(characters)
		popd: str = ''
		# != is a xor. If reverse is true, then it's
		# "while not self.is_in". If reverse is false,
		# it's "while self.is_in".
		while self.is_in(characters) != reverse:
			popd += self.code.pop(0)
		self.whitespace()
		return popd
		
	def is_in(self, characters: str) -> bool:
		"""
		This method checks if the current character is 
		within the given characters. If the code is empty,
		because everything has been parsed, it will return
		False.
		
		>>> Code('abc').is_in('a')
		True
		>>> Code('abc').is_in('b')
		False
		>>> Code('abc').is_in('kaz')
		True
		>>> Code('').is_in('kaz')
		False
		>>> Code('').is_in('')
		False
		>>> Code('abc').is_in('')
		False
		"""
		return bool(self.code and self.code[0] in characters)
		
	# Private
		
	def whitespace(self):
		"""
		This method removes all the trailing whitespaces.
		
		Removes all the whitespace from the code proprety.
		(automatic .whitespace() call in __init__)
		>>> abc = Code(' 	abc')
		>>> abc.code
		['a', 'b', 'c']
		
		If no whitespace is there, nothing is removed.
		(automatic .whitespace() in __init__)
		>>> abc = Code('abc')
		>>> abc.code
		['a', 'b', 'c']
		"""
		while self.is_in(string.whitespace):
			self.code.pop(0)
		
	def assume(self, characters: str):
		"""
		This method assumes the current character is
		within the given characters, and raises an error
		otherwise.
		
		>>> Code('abc').assume('a')
		>>> Code('abc').assume('b')
		Traceback (most recent call last):
			...
		SyntaxError: Unexpected 'a' while parsing for 'b'.
		
		Please refer to is_in for more examples.
		"""
		if not self.is_in(characters):
			if self.code:
				unexpected: str = self.code[0]
			else:
				unexpected: str = 'EOF'
			raise SyntaxError(
			f'Unexpected {unexpected!r} while parsing '
			f'for {characters!r}.')
