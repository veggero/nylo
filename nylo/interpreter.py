from __future__ import annotations #nb I have no clues how this works
from typing import Tuple, Dict, List, Optional as Opt
scope: Dict[str, Tuple[Node, scope]]

class Node(Dict[str, "Node"]):
	
	name: Tuple[str] = ()
	parent: Opt[Node] = None
	myclass: Node = False
	fake: bool = False
	
	def walk(self, target: Node, 
	         slyce: scope, fakeSource: Opt[Node] = None, 
	         avoid: Tuple[Node] = (), wipSlice: Opt[scope] = None) -> scope:
		
		if wipSlice is None:
			wipSlice = {}
		else:
			if self is not fakeSource:
				wipSlice[target] = self, slyce
			if self in slyce:
				newSelf, newSlice = slyce[self]
				return newSelf.walk(target, newSlice, fakeSource, avoid, wipSlice)
			if self.fake and self not in avoid and len(target)-1: 
				newSelf, newSlice, path = self.resolve(slyce, avoid)
				newSelf, newSlice = newSelf.seek(newSlice, path)
				newSelf.walk(target, newSlice, fakeSource, avoid, wipSlice)
			if self.myclass:
				newSlice: scope = self.walk(self.myclass, slyce)
				self.myclass.walk(target, newSlice, fakeSource, avoid, wipSlice)
		
		for key in set(self) & set(target):
			self[key].walk(target[key], slyce, fakeSource, avoid, wipSlice)
		
		return wipSlice if wipSlice else slyce

	def resolve(self, slyce: scope, avoid: Tuple[Node] = (), 
			 path: Tuple[str] = ()) -> Tuple[Node, scope, Tuple[str]]:
		parentClass, target, newSlice, newPath = self.getParentClass(slyce)
		newSlice = parentClass.walk(target, slyce, self, avoid+(self,))
		return target, newSlice, path + newPath
	
	def getParentClass(self, slyce: scope, path: Tuple[str] = ()
					) -> Tuple[Node, Node, scope, Tuple[str]]:
		while not self.myclass:
			assert self.parent, f'Node {self} {path[::-1]} is not implemented.'
			self, path = self.parent, path + self.name[-1:]
		target, newSlice = self.myclass.seek(slyce)
		return self, target, newSlice, path
	
	def seek(self, slyce: scope, path: Tuple[str] = ()) -> Tuple[Node, scope]:
		while 1:
			if path and path[0] in self:
				self, slyce, path = self[path[0]], slyce, path[1:]
			elif self in slyce:
				self, slyce = slyce[self]
			elif self.fake:
				self, slyce, path = self.resolve(slyce, path=path)
			elif self.myclass:
				self, slyce = self.myclass, self.walk(self.myclass, slyce)
			else:
				return self, slyce
	
	def __eq__(self, other):
		return self is other
	
	def __hash__(self):
		return id(self)
	
	def __repr__(self):
		return '.'.join(self.name)
	
	def __bool__(self):
		return True
