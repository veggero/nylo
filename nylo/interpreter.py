from __future__ import annotations
from typing import Tuple, Dict, List, Optional

class Node(Dict[str, "Node"]):
	
	name: Tuple[str] = ()
	parent: Optional[Node] = None
	myclass: Node = False
	fake: bool = False
	
	def walk(self, target: Node, 
	         stack: Stack, fakeSource: Optional[Node] = None, 
	         avoid: Tuple[Node] = (), slyce: Optional[Slice] = None) -> Stack:
		
		if slyce is None:
			slyce = Slice()
			
		else:
			
			if self in stack:
				newSelf, newStack = stack[self]
				return newSelf.walk(target, newStack, fakeSource, avoid, slyce)
			
			if self is not fakeSource:
				slyce[target] = self, stack
				
			if self.fake and self not in avoid and len(target)-1: #self is always there, remove it. could cause bugs?
				newSelf, newStack, path = self.resolve(stack, avoid)
				newSelf, newStack = newSelf.seek(newStack, path)
				newSelf.walk(target, newStack, fakeSource, avoid, slyce)
			
			if self.myclass:
				newStack: Stack = self.walk(self.myclass, stack)
				self.myclass.walk(target, newStack, fakeSource, avoid, slyce)
		
		for key in set(self) & set(target):
			self[key].walk(target[key], stack, fakeSource, avoid, slyce)
			
		return stack + slyce if slyce.links else stack

	def resolve(self, stack: Stack, avoid: Tuple[Node] = (), path: Tuple[str] = ()) -> Tuple[Node, Stack, Tuple[str]]:
		parentClass, target, newStack, newPath = self.getParentClass(stack)
		newStack = parentClass.walk(target, stack, self, avoid+(self,))
		return target, newStack, path + newPath
	
	def getParentClass(self, stack: Stack, path: Tuple[str] = ()) -> Tuple[Node, Node, Stack, Tuple[str]]:
		if self.myclass:
			target, newStack = self.myclass.seek(stack)
			return self, target, newStack, path
		assert self.parent, f'Node {self} {path[::-1]} is not implemented.'
		return self.parent.getParentClass(stack, path + self.name[-1:])
	
	def seek(self, stack: Stack, path: Tuple[str] = ()) -> Tuple[Node, Stack]:
		while 1:
			if path and path[0] in self:
				self, stack, path = self[path[0]], stack, path[1:]
			elif self in stack:
				self, stack = stack[self]
			elif self.fake:
				self, stack, path = self.resolve(stack, path=path)
			elif self.myclass:
				self, stack = self.myclass, self.walk(self.myclass, stack)
			else:
				assert not path, f'Node at {path} not defined at {self}'
				return self, stack
	
	def makefake(self):
		self.fake = True
		return self
	
	def __eq__(self, other):
		return self is other
	
	def __hash__(self):
		return id(self)
	
	def __repr__(self):
		return '.'.join(self.name)
	
	def __bool__(self):
		return True
	
class Slice:
	
	def __init__(self): #the fact that root is not used makes me think that something's wrong, I can feel it
		self.links, self.deps = {}, {}
		
	def __setitem__(self, key: str, item: Tuple[Node, Stack]):
		self.links[key], self.deps[key] = item
		 
	def __getitem__(self, item: str) -> Tuple[Node, Stack]:
		return self.links[item], self.deps[item]

class Stack(list):

	def __getitem__(self, item):
		return next(sl[item] for sl in reversed(self) if item in sl.links)
	
	def __contains__(self, item):
		return self and (item in list.__getitem__(self, -1).links) # I think the other elements might be interesting as well
	
	def __add__(self: Stack, other: Slice):
		return Stack(list.__add__(self, [other]))
		
