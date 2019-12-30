from __future__ import annotations
from lexer import Code
from interpreter import Node
from string import ascii_letters, digits, punctuation
from typing import Tuple, Dict, List, Optional, Union

def parse(code: Code) -> Union[ParsedNode, Variable, Call]:
	if code.is_in(ascii_letters + '_`'):
		var = Variable(code)
		if code.is_in('('):
			node = ParsedNode(code)
			return Call(var, node)
		else:
			return var
	elif code.is_in('('):
		return ParsedNode(code)

class ParsedNode:
	
	keys: List[str]
	values: List[Union[ParsedNode, Variable, Call]]
	target: Optional[Tuple[str]] = None
	
	def __init__(self, code: Code):
		code.skip('(')
		self.keys, self.values = [], []
		while not (code.is_in(')') or code.startswith('->')):
			self.keys.append(Variable(code).value[0]) 
				#[0] as (a.b: c) is not supported yet, hacky
			code.skip(':')
			self.values.append(parse(code))
			code.skip_if(',')
		if code.startswith('->'):
			code.skip('-', '>')
			self.target = Variable(code)
		code.skip(')')
		
	def bind(self, parents: Tuple[Node] = (), call: bool = False):
		for value in self.values:
			value.bind(((self,) if not call else ()) + parents, call)
		
	def __repr__(self):
		return f'({self.keys!r}: {self.values!r} -> {self.target!r})'

class Variable:
	
	value: Tuple[str] = ()
	binded: Optional[Union[ParsedNode, Variable, Call]] = None
	
	def __init__(self, code: Code):
		if code.is_in('`'):
			code.skip('`')
			self.value = code.skip_while('`', reverse=True),
			code.skip('`')
		elif code.is_in(ascii_letters + '_'):
			self.value = code.skip_while(ascii_letters + digits + '_'),
		self.value += Variable(code).value if code.skip_if('.') else ()
		
	def __repr__(self):
		return repr(self.value)
	
	def bind(self, parents: Tuple[Node] = (), call: bool = False):
		for parent in parents:
			if self.value[0] in parent.keys:
				self.binded = parent.values[parent.keys.index(self.value[0])]
				break
		else:
			assert f"{self!r} could not be binded. sorry 'bout that!"
	
class Call:
	
	caller: Variable
	called: ParsedNode
	
	def __init__(self, caller: Variable, called: ParsedNode):
		self.caller, self.called = caller, called
	
	def __repr__(self):
		return f'{self.caller!r}{self.called!r}'
	
	def bind(self, parents: Tuple[Node] = (), call: bool = False):
		self.caller.bind(parents, call)
		self.called.bind(parents, True)

a = parse(Code("""(
	nat: (
		pos: (
			prev: nat
			if: (
				then: ()
				else: ()
				-> then
			)
		)
		zero: (
			if: (
				then: ()
				else: ()
				-> else
			)
		)
	)
	test: nat.pos(nat: nat) )"""))

a.bind()
