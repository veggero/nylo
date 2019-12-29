from __future__ import annotations
from typing import Tuple, Dict, List, Optional

class Node(Dict[str, "Node"]):
	
	name: Tuple[str] = ()
	parent: Optional[Node] = None
	myclass: Optional[Node] = False
	fake: bool = False
	
	def walk(self, target: Node, 
	         stack: Stack, fakeSource: Optional[Node] = None, 
	         avoid: Tuple[Node] = (), slyce: Optional[Slice] = None) -> Stack:
		
		if slyce is None:
			slyce = Slice(target)
			
		else:
			
			stack = stack.at(self)
			
			if self in stack:
				newSelf, newStack = stack[self]
				return newSelf.walk(target, newStack, fakeSource, avoid, slyce)
			
			if self is not fakeSource:
				slyce[target] = self, stack
				
			if self.fake and self not in avoid and len(target):
				newSelf, newStack = self.resolve(stack, avoid)
				newSelf.walk(target, newStack, fakeSource, avoid, slyce)
			
			if self.myclass:
				newStack: Stack = self.walk(self.myclass, stack)
				self.myclass.walk(target, newStack, fakeSource, avoid, slyce)
		
		for key in set(self) & set(target):
			self[key].walk(target[key], stack, fakeSource, avoid, slyce)
			
		return stack + Stack([slyce])

	def resolve(self, stack: Stack, avoid: Tuple[Node] = ()) -> Tuple[Node, Stack]:
		parentClass, target, newStack, path = self.getParentClass(stack)
		newStack = parentClass.walk(target, stack, self, avoid+(self,))
		return target.seek(newStack, path)
	
	def getParentClass(self, stack: Stack, path: Tuple[str] = ()) -> Tuple[Node, Node, Stack, Tuple[str]]:
		if self.myclass:
			target, newStack = self.myclass.seek(stack)
			return self, target, newStack, path
		assert self.parent, f'Node {self} {path[::-1]} is not implemented.'
		return self.parent.getParentClass(stack, path + self.name[-1:])
	
	def seek(self, stack: Stack, path: Tuple[str] = ()) -> Tuple[Node, Stack]:
		
		stack = stack.at(self)
		
		if path and path[0] in self:
			return self[path[0]].seek(stack, path[1:])
		
		if self in stack:
			newSelf, newStack = stack[self]
			return newSelf.seek(newStack, path)
		
		if self.fake:
			newSelf, newStack = self.resolve(stack)
			return newSelf.seek(newStack, path)
		
		if self.myclass:
			newStack = self.walk(self.myclass, stack)
			return self.myclass.seek(newStack, path)
		
		assert not path, 'Node at {path} not defined at {self}'
		return self, stack
	
	def named(self, name: Tuple[str], parent: Optional[Node] = None) -> Node:
		self.name, self.parent = name, parent
		[son.named(name + (key,), self) for key, son in self.items()]
		return self
	
	def makefake(self):
		self.fake = True
		return self
	
	def isSon(self, possibleDad: Node) -> bool:
		# I know this can improved
		return self.name[:len(possibleDad.name)] == possibleDad.name
	
	def __eq__(self, other):
		return self is other
	
	def __hash__(self):
		return hash(id(self))
	
	def __repr__(self):
		return '.'.join(self.name)
	
	def __bool__(self):
		return True
	
class Slice:
	
	def __init__(self, root):
		self.root, self.links, self.deps = root, {}, {}
		
	def __setitem__(self, key: str, item: Tuple[Node, Stack]):
		self.links[key] = item[0]
		self.deps[key] = item[1]
	
	def __getitem__(self, item: str) -> Tuple[Node, Stack]:
		return self.links[item], self.deps[item]
	
	def __repr__(self) -> str:
		return (repr(self.root) + '\n' +
		  '\n'.join(f'[{key!r}\t-> {self[key][0]!r}\t]'
			  + ''.join(f'\n\t\t{i}: ' + repr(k).replace('\n', '\n\t\t') for i, k in enumerate(self[key][1]))
			  for key in self.links))

class Stack(list):
	
	def __init__(self, iterable=()):
		super().__init__(filter(lambda x: len(x.links), iterable))
	
	def at(self, loc: Node) -> Stack:
		newstack = Stack(self)
		while newstack and not loc.isSon(list.__getitem__(newstack, -1).root):
			del newstack[-1]
		return newstack

	def __getitem__(self, item):
		return next(sl[item] for sl in reversed(self) if item in sl.links)
	
	def __contains__(self, item):
		return any(item in sl.links for sl in self)
	
	def __add__(self, other):
		return Stack(list.__add__(self, other))
	
	def __radd__(self, other):
		return Stack(list.__add__(other, self))
