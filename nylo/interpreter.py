from __future__ import annotations #nb I have no clues how this works
from typing import Tuple, Dict, List, Optional

class Node(Dict[str, "Node"]):
	
	name: Tuple[str] = ()
	parent: Optional[Node] = None
	myclass: Node = False
	fake: bool = False
	
	def walk(self, target: Node, 
	         slyce: Slice, fakeSource: Optional[Node] = None, 
	         avoid: Tuple[Node] = (), buildSlyce: Optional[Slice] = None) -> Slice:
		
		if buildSlyce is None:
			buildSlyce = Slice()
			
		else:
			
			if slyce and self in slyce:
				newSelf, newSlice = slyce[self]
				return newSelf.walk(target, newSlice, fakeSource, avoid, buildSlyce)
			if self is not fakeSource:
				buildSlyce[target] = self, slyce
			if self.fake and self not in avoid and len(target)-1: 
				newSelf, newSlice, path = self.resolve(slyce, avoid)
				newSelf, newSlice = newSelf.seek(newSlice, path)
				newSelf.walk(target, newSlice, fakeSource, avoid, buildSlyce)
			if self.myclass:
				newSlice: Slice = self.walk(self.myclass, slyce)
				self.myclass.walk(target, newSlice, fakeSource, avoid, buildSlyce)
		
		for key in set(self) & set(target):
			self[key].walk(target[key], slyce, fakeSource, avoid, buildSlyce)
		
		return buildSlyce if buildSlyce.links else slyce

	def resolve(self, slyce: Slice, avoid: Tuple[Node] = (), path: Tuple[str] = ()) -> Tuple[Node, Slice, Tuple[str]]:
		parentClass, target, newSlice, newPath = self.getParentClass(slyce)
		newSlice = parentClass.walk(target, slyce, self, avoid+(self,))
		return target, newSlice, path + newPath
	
	def getParentClass(self, slyce: Slice, path: Tuple[str] = ()) -> Tuple[Node, Node, Slice, Tuple[str]]:
		if self.myclass:
			target, newSlice = self.myclass.seek(slyce)
			return self, target, newSlice, path
		assert self.parent, f'Node {self} {path[::-1]} is not implemented.'
		return self.parent.getParentClass(slyce, path + self.name[-1:])
	
	def seek(self, slyce: Slice, path: Tuple[str] = ()) -> Tuple[Node, Slice]:
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
	
class Slice:
	
	def __init__(self):
		self.links, self.deps = {}, {}
		
	def __setitem__(self, key: str, item: Tuple[Node, Slice]):
		self.links[key], self.deps[key] = item
		 
	def __getitem__(self, item: str) -> Tuple[Node, Slice]:
		return self.links[item], self.deps[item]
	
	def __contains__(self, item) -> bool:
		return item in self.links
