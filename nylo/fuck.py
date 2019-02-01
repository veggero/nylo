"""
This module manages when nylo or the user fuck up. It manages exception
and try to make the user understand fully how badly he screwd up.
"""

import string
import sys
	
def fuck(message: str, code):
	"""
	This function handles formatting of errors.
	
	>>> from code import Code
	>>> fuck('me!', Code('ya!', '\\nny'))
	Traceback (most recent call last):
		...
	SystemExit
	"""
	print('FUCK.') #most important part
	line_number = code.consumed.count('\n') + 1
	last_newline = ''.join(['\n']+code.consumed).rindex('\n')
	first_newline = ''.join(code.code+['\n']).index('\n')
	last_line = code.consumed[last_newline:] + code.code[:first_newline]
	last_line = ''.join(last_line).replace('\t', '    ')
	print(f"{line_number}| {last_line}")
	print(' '*(len(code.consumed)-last_newline+len(str(line_number))+2)
	   +'   '*code.consumed[last_newline:].count('\t')+'^ right here')
	print(f'Error: {message}')
	sys.exit()

def unexpected(characters: str, code):
	"""
	This function will handle raising exception when an unexpected
	character is found while parsing for some characters.
	
	>>> from code import Code
	>>> unexpected('(', Code('15'))
	Traceback (most recent call last):
		...
	SystemExit
	
	>>> unexpected('(', Code(''))
	Traceback (most recent call last):
		...
	SystemExit
	
	>>> unexpected(string.digits, Code('hello'))
	Traceback (most recent call last):
		...
	SystemExit
	
	>>> unexpected(string.ascii_letters, Code('15'))
	Traceback (most recent call last):
		...
	SystemExit
	"""
	unexpected = 'EOF' if not code.code else f'character {code.code[0]!r}'
	characters = ('variable' if string.ascii_letters in characters else
			      'digits' if string.digits in characters else
			      repr(characters))
	fuck(f'Unexpected {unexpected} while parsing for {characters}.', code)
