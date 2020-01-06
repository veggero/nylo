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
	elif code.is_in(digits):
		return Nat(code)
	else:
		assert False, f'What the fuck is {code.code[0]}'

class ParsedNode:
	
	node: Node
	keys: List[str]
	values: List[Union[ParsedNode, Variable, Call]]
	target: Optional[Union[ParsedNode, Variable, Call]] = None
	name: Optional[Tuple[str]] = None
	parent: Optional[ParsedNode] = None
	_node: Optional[Node] = None
	
	def __init__(self, code: Code):
		code.skip('(')
		self.keys, self.values = [], []
		while not (code.is_in(')') or code.startswith('->')):
			self.keys.append(Variable(code).value[0])  
				#[0] as (a.b: c) is not supported yet, sorry TODO
			code.skip(':')
			self.values.append(parse(code))
			code.skip_if(',')
		if code.startswith('->'):
			code.skip('-', '>')
			self.target = parse(code)
		code.skip(')')
		
	def bind(self, parents: Tuple[ParsedNode] = (), 
		  name: Tuple[str] = ('root',), parent: Optional[ParsedNode] = None, 
		  call: bool = False):
		self.name, self.parent = name, parent
		if self.target:
			self.target.bind(((self,) if not call else ()) + parents, 
			  name + ('target!',), self, call)
		for key, value in zip(self.keys, self.values):
			value.bind(((self,) if not call else ()) + parents, 
			  name + (key,), self, call)
	
	@property
	def node(self) -> Node:
		if self._node:
			return self._node
		self._node = Node()
		self._node.name = self.name
		if self.parent:
			self._node.parent = self.parent.node
		for key, value in zip(self.keys, self.values):
			subnode = value.node
			if key in self._node:
				self._node[key].fake = False
				self._node[key].myclass = subnode #HACK
			self._node[key] = subnode
		self._node['self'] = Node()
		self._node['self'].name = self.name + ('self',)
		self._node['self'].parent = self._node
		if self.target:
			if isinstance(self.target, Variable):
				self._node['self'].myclass = self.target.node.myclass
			else:
				self._node['self'].myclass = self.target.node
		else:
			self._node['self'].myclass = self._node
		return self._node
		
	def __repr__(self):
		return f'({self.keys!r}: {self.values!r} -> {self.target!r})'

class Variable:
	
	node: Node
	value: Tuple[str] = ()
	binded: Optional[Union[ParsedNode, Variable, Call]] = None
	name: Optional[Tuple[str]] = None
	parent: Optional[ParsedNode] = None
	_node: Optional[Node] = None
	
	def __init__(self, code: Code):
		if code.is_in('`'):
			code.skip('`')
			self.value = code.skip_while('`', reverse=True),
			code.skip('`')
		elif code.is_in(ascii_letters + '_'):
			self.value = code.skip_while(ascii_letters + digits + '_'),
		else:
			assert False, f'What the fuck is {code.code[0]}'
		self.value += Variable(code).value if code.skip_if('.') else ()
		
	def __repr__(self):
		return repr(self.value)
	
	def bind(self, parents: Tuple[ParsedNode] = (), 
		  name: Tuple[str] = ('root',), parent: Optional[ParsedNode] = None, 
		  call: bool = False):
		self.name, self.parent = name, parent
		for parent in parents:
			if self.value[0] in parent.keys:
				self.binded = parent.values[parent.keys.index(self.value[0])]
				break
		assert self.binded,  f"{self!r} could not be binded. sorry 'bout that!"
			
	@property
	def node(self) -> Node:
		if self._node:
			return self._node
		self._node = Node()
		self._node.name = self.name
		if self.parent:
			self._node.parent = self.parent.node
		target_node = self.binded.node
		path: List[str] = list(self.value[1:])
		while path:
			if target_node.name[-1] == 'caller!':
				target_node = target_node.myclass.parent  #HACK
			if not path[0] in target_node:
				# IMPORTANT sometimes the node is not ready yet as it's a parent
				target_node[path[0]] = Node()
				target_node[path[0]].fake = True
				target_node[path[0]].name = target_node.name + (path[0],)
				target_node[path[0]].parent = target_node
			target_node = target_node[path[0]]
			del path[0]
		self._node.myclass = target_node
		return self._node
		
	
class Call:
	
	node: Node
	caller: Variable
	called: ParsedNode
	name: Optional[Tuple[str]] = None
	parent: Optional[ParsedNode] = None
	_node: Optional[Node] = None
	
	def __init__(self, caller: Variable, called: ParsedNode):
		self.caller, self.called = caller, called
	
	def __repr__(self):
		return f'{self.caller!r}{self.called!r}'
	
	def bind(self, parents: Tuple[ParsedNode] = (), 
		  name: Tuple[str] = ('root',), parent: Optional[ParsedNode] = None, 
		  call: bool = False):
		self.name, self.parent = name, parent
		self.caller.bind(parents, name, parent, call)
		self.called.bind(parents, name, parent, True)
	
	@property
	def node(self) -> Node:
		if self._node:
			return self._node
		self._node = Node()
		self._node.name = self.name+('caller!',)
		if self.parent:
			self._node.parent = self.parent.node
		caller = self.caller.node
		called = self.called.node
		called.myclass = caller.myclass
		if self.called.target:
			assert isinstance(self.called.target, Variable), "Target value should be a variable"
			word = self.called.target.value[0] 
				#TODO support more values
		else:
			word = 'self'
		called[word] = Node()
		called[word].fake = True
		called[word].name = called.name + (word,)
		called[word].parent = called
		self._node.myclass = called[word]
		return self._node

class Nat:
	#horrible implementation, todo again
	
	node: Node
	value: int
	nat: Call
	name: Optional[Tuple[str]] = None
	parent: Optional[ParsedNode] = None
	_node: Optional[Node] = None
	
	def __init__(self, code: Code):
		self.value = int(code.skip_while(digits))
		self.nat = parse(Code(
			'nat.pos(prev: '*self.value + 'nat.zero' + ')'*self.value))
		
	def bind(self, parents: Tuple[ParsedNode] = (), 
		  name: Tuple[str] = ('root',), parent: Optional[ParsedNode] = None, 
		  call: bool = False):
		self.nat.bind(parents, name, parent, call)
		
	@property
	def node(self) -> Node:
		return self.nat.node
