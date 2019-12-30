"""
This is a class that aims to make parsing a little bit easier.
It creates an abstraction layer between the parser and the
code string itself. This class will provide methods to
get characters from code, automatically removing whitespace,
and checking if there's anything wrong (Wrong syntax or
EOF while parsing)
"""

import string
from typing import List, Optional, Tuple

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
	
	def __init__(self, code: str, consumed=''):
		"Creates a new instance"
		self.code: List[str] = [*code]
		self.consumed = [*consumed]
		# Already remove trailing whitespace
		self.whitespace()
		
	def skip(self, *characters: Tuple[str]) -> str:
		"""
		This method skips the current character by
		removing it from the list of characters.
		It will also assume the current characters is
		within the given characters.
		It will also return the parsed character.
		"""
		popd: str = ''
		self.assume(characters[0])
		self.consumed.append(self.code.pop(0))
		if characters[1:]:
			popd = self.skip(*characters[1:])
		# Remove possible whitespace
		self.whitespace()
		return self.consumed[-1] + popd
	
	def skip_if(self, characters: str) -> Optional[str]:
		"Skip a character if it's there"
		if self.startswith(characters):
			return self.skip(characters)
		
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
		"""
		if not reverse:
			self.assume(characters)
		popd: str = ''
		while self.is_in(characters) != reverse:
			popd += self.code.pop(0)
			self.consumed.append(popd[-1])
		self.whitespace()
		return popd
		
	def is_in(self, characters: str) -> bool:
		"""
		This method checks if the current character is 
		within the given characters. If the code is empty,
		because everything has been parsed, it will return
		False.
		"""
		return bool(self.code and self.code[0] in characters)
	
	def startswith(self, characters: str) -> bool:
		"""
		This method checks if the current code
		starts with the given characters.
		"""
		return ''.join(self.code).startswith(characters)
		
	def whitespace(self):
		"""
		This method removes all the trailing whitespaces.
		"""
		while self.is_in(string.whitespace):
			self.consumed.append(self.code.pop(0))
		
	def assume(self, characters: str):
		"""
		This method assumes the current character is
		within the given characters, and raises an error
		otherwise.
		"""
		assert self.is_in(characters), self.code[0]
