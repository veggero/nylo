from code import Code
from interpreter import Node
from string import ascii_letters, digits, punctuation
from typing import Tuple, Dict, Any, List, Optional

def parse(code: Code) -> Any:
	pass

class ParsedNode:
	
	keys: List[Tuple[str]]
	values: List[Any]
	target: Optional[Tuple[str]] = None
	
	def __init__(self, code: Code):
		code.skip('(')
		self.key, self.values = [], []
		while not (self.code.is_in(')') or self.code.startswith('->')):
			self.keys.append(Variable(code))
			code.skip(':')
			self.values.append(parse(code))
			code.skip_if(',')
		if self.code.startswith('->'):
			code.skip('-', '>')
			self.target = Variable(code)
		code.skip(')')

class Variable:
	
	value: Tuple[str] = ()
	
	def __init__(self, code: Code):
		if self.code.is_in('`'):
			self.code.skip('`')
			self.value = self.code.skip_while('`', reverse=True),
			self.code.skip('`')
		elif self.code.is_in(ascii_letters + '_'):
			self.value = self.code.skip_while(ascii_letters + digits + '_'),
		self.value += Variable(code).value if self.skip_if('.') else ()
	
class Call:
	
	caller: Variable
	called: ParsedNode
	
	def __init__(self, caller: Variable, called: ParsedNode):
		self.caller, self.called = caller, called
