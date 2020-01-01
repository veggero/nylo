from __future__ import annotations #nb I have no clues how this works
from typing import Tuple, Dict, List, Optional

class Node(Dict[str, "Node"]):
	
	name: Tuple[str] = ()
	parent: Optional[Node] = None
	myclass: Node = False
	fake: bool = False
	
	def walk(self, target: Node, 
	         slyce: dict, fakeSource: Optional[Node] = None, 
	         avoid: Tuple[Node] = (), buildSlyce: Optional[dict] = None) -> dict:
		
		if buildSlyce is None:
			buildSlyce = {}
		else:
			if self in slyce:
				newSelf, newSlice = slyce[self]
				return newSelf.walk(target, newSlice, fakeSource, avoid, buildSlyce)
			if self is not fakeSource:
				buildSlyce[target] = self, slyce
			if self.fake and self not in avoid and len(target)-1: 
				newSelf, newSlice, path = self.resolve(slyce, avoid)
				newSelf, newSlice = newSelf.seek(newSlice, path)
				newSelf.walk(target, newSlice, fakeSource, avoid, buildSlyce)
			if self.myclass:
				newSlice: dict = self.walk(self.myclass, slyce)
				self.myclass.walk(target, newSlice, fakeSource, avoid, buildSlyce)
		
		for key in set(self) & set(target):
			self[key].walk(target[key], slyce, fakeSource, avoid, buildSlyce)
		
		return buildSlyce if buildSlyce else slyce

	def resolve(self, slyce: dict, avoid: Tuple[Node] = (), path: Tuple[str] = ()) -> Tuple[Node, dict, Tuple[str]]:
		parentClass, target, newSlice, newPath = self.getParentClass(slyce)
		newSlice = parentClass.walk(target, slyce, self, avoid+(self,))
		return target, newSlice, path + newPath
	
	def getParentClass(self, slyce: dict, path: Tuple[str] = ()) -> Tuple[Node, Node, dict, Tuple[str]]:
		if self.myclass:
			target, newSlice = self.myclass.seek(slyce)
			return self, target, newSlice, path
		assert self.parent, f'Node {self} {path[::-1]} is not implemented.'
		return self.parent.getParentClass(slyce, path + self.name[-1:])
	
	def seek(self, slyce: dict, path: Tuple[str] = ()) -> Tuple[Node, dict]:
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
