ind = 0 #keyword: obv

class Node(dict):
	
	__slots__ = 'reference', 'name', 'parent'
	
	def walk(self, other, stack, slyce, depends, avoid_t, avoid_f):
        
		##print(f'wanking {other} over {self}, deplen is {len(depends)}')
		
		if not slyce is None:

			if self in stack:
				target, dependencies = stack[self]
				return target.walk(other, stack + dependencies, 
					   slyce, dependencies, avoid_t, avoid_f) #removed depends+ here because it was ##printing 350k lines. was it useful? dunno. remember to try understand why old dependencies could be useful when getting into stack sh$t
			
			if self is not avoid_t:
				slyce[other] = self, depends
			
			if isinstance(self, FakeNode) and self not in avoid_f and len(other): #can this become recursive? especially without the len(other) which does not make sense as I have to force it
				deps, target = self.resolvefake(stack, avoid_f)
				deps = Stack([list.__getitem__(deps, -1)]) #IMPORTANT
				# deps here is an entire stack trying to get to the result with a lot of useless shit around. If I don't get only the last element, the entire thing gets to sit on top of the stack anyway and then it pops elements from the top until you get to a stack element inside deps while you wanted to pop back to your actual stack. why the fuck does this happen!
				target.walk(other, stack + deps, slyce, depends + deps, avoid_t, avoid_f)
			
			if hasattr(self, 'reference'):
				dependencies = self.walk(self.reference, stack, None, [], avoid_t, avoid_f)
				self.reference.walk(other, stack, slyce, 
						depends + Stack([dependencies]), avoid_t, avoid_f)
		
		else:
			slyce = Slice(other)
	
		for key in set(self) & set(other):
			self[key].walk(other[key], stack, slyce, depends, avoid_t, avoid_f)
			
		return slyce
	
	def daddy(self, of, stack):
		global ind
		if hasattr(self, 'reference'):
			try: #needed?
				#print(f'{"  "*ind}START GETTING WALK TARGET:')
				ind = ind + 1
				tgt, newstack = self.reference.seek(stack)
				ind = ind - 1
				#print(f'{"  "*ind}END GETTING WALK TARGET')
				return self, tgt, newstack, of
			except AssertionError as s:
				##print('Branch failed', str(s))
				pass
		assert self.parent, f"parent {self} / {of[::-1]} of FakeNode hasn't any reference."
		return self.parent.daddy(of + self.name[-1:], stack)
		
	def resolvefake(self, stack, but): #delta stack, target
		global ind
		parent, ref, deps, targetpath = self.parent.daddy((self.name[-1],), stack)
		if deps: stack = stack + deps
		newdeps = parent.walk(ref, stack, None, [], self, but+(self,))
		#print(f'{"  "*ind}START GETTING PATH TARGET:')
		ind = ind + 1
		target, newnewdeps = ref.seek(stack + Stack([newdeps]), targetpath, but=())
		ind = ind -1
		##print(f'{"  "*ind}END GETTING PATH TARGET')
		##print()
		##print('CHOOOOOSE CAREFULLY')
		##print('press A for')
		##print((deps or Stack()))
		##print('press B for')
		##print(newdeps)
		##print('press C for')
		##print(newnewdeps)
		##print()
		##print('------------')
		return (deps or Stack()) + Stack([newdeps]) + newnewdeps, target # questo butta l'intero stack dentro a una dependency
	
	def seek(self, stack, path=(), newstack=None, but=()): #delta stack, target
		global ind
		if newstack is None:
			newstack = Stack()
		
		##print(f'{"  "*ind}=====> {self} ', len(stack+newstack))
		##print(f"    PATH IS {path}")
		if newstack:
			newstack = newstack.check(self)
		else:
			stack = stack.check(self)
		##print('    Current stack:')
		cstack = stack + newstack
		##print('\n\n'.join(map(str, cstack)))
		##print('   ', list.__getitem__(cstack, len(cstack)-1) if cstack else None)
		
		if path and path[0] in self:
			##print('   --> path\n')
			return self[path[0]].seek(stack, path[1:], newstack, but)
		
		##print(self in cstack)
		if self in (stack + newstack):
			##print('   --> stack\n')
			target, dependencies = cstack[self]
			return target.seek(stack, path,  newstack + dependencies, but) #newstack + deps obv
			
		if isinstance(self, FakeNode):
			##print('   --> walk\n')
			deps, target = self.resolvefake(cstack, but)
			return target.seek(stack, path, newstack + deps, but)
			
		if hasattr(self, 'reference'):
			##print('   --> reference\n')
			deps = Stack([self.walk(self.reference, stack, None, [], None, but)])
			return self.reference.seek(stack, path, newstack + deps, but)
		
		##print('   --> end\n')
		assert not path, (path, type(path))
		##print(cstack)
		return self, newstack
	
	def named(self, name, parent=None):
		self.name, self.parent = name, parent
		[son.named(name + (key,), self) for key, son in self.items()]
		
		return self
	
	def son(self, daddy): #to be improved with magic
		return self.name[:len(daddy.name)] == daddy.name or \
			self.name[0] != daddy.name[0]
		
	def __eq__(self, other):
		return self is other
	
	def __hash__(self):
		return hash(id(self))
	
	def __repr__(self):
		return '.'.join(self.name)
	
class FakeNode(Node):
	pass

class Slice:
	
	__slots__ = 'root', 'links', 'deps'
	
	def __init__(self, root):
		self.root, self.links, self.deps = root, {}, {}
		
	def __setitem__(self, key, item):
		self.links[key] = item[0]
		self.deps[key] = item[1]
	
	def __getitem__(self, item):
		return self.links[item], self.deps[item]
	
	def __repr__(self, o=''):
		return (repr(self.root) + '\n' +
		  '\n'.join(f'[{key!r}\t-> {self[key][0]!r}\t]'
			  + ''.join(f'\n\t\t{i}: ' + repr(k).replace('\n', '\n\t\t') for i, k in enumerate(self[key][1]))
			  for key in self.links)
		  )
	
class Stack(list):
	
	def __init__(self, iterable=()):
		super().__init__(filter(lambda x: len(x.links), iterable))
	
	def check(self, loc):
		newstack = Stack(self)
		while newstack and not loc.son(list.__getitem__(newstack, -1).root):
			###print(list.__getitem__(self, -1))
			#print(f'<-> <=> POP <=> <-> {list.__getitem__(newstack, -1).root}')
			del newstack[-1]
		return newstack

	def __getitem__(self, item):
		return next(sl[item] for sl in reversed(self) if item in sl.links)
	
	def __contains__(self, item):
		return any(item in sl.links for sl in self)
	
	def __add__(self, other):
		return Stack([*self, *other])
	
	def __radd__(self, other):
		return Stack([*other, *self])

root = Node(
	fib = Node(
		n = Node(
			prev = FakeNode(
				if_ = FakeNode(),
				prev = FakeNode()
			),
			if_ = FakeNode()
		),
		self_ = Node()
	),
	add = Node(
		a = Node(
			if_ = FakeNode(),
			prev = FakeNode()
		),
		b = Node(prev=FakeNode()), #adding prev here I force the evaluation, check if it works anyway because it's wrong #OF COURSE NOT
		self_ = Node()
	),
	nat = Node(
		pos = Node(
			prev = Node(),
			if_ = Node(
				else_ = Node(),
				then = Node(),
				self_ = Node()
			)
		),
		zero = Node(
			if_ = Node(
				else_ = Node(),
				then = Node(),
				self_ = Node()
			)
		)
	),
	self_ = Node()
).named(('root',))
root['nat']['pos']['if_']['self_'].reference = root['nat']['pos']['if_']['then']
root['nat']['zero']['if_']['self_'].reference = root['nat']['zero']['if_']['else_']

add_call_nat = Node(
	prev = Node()
).named(root['add'].name+('add_call_nat',), root['add'])
add_call_nat.reference = root['nat']['pos']
add_call_nat['prev'].reference = root['add']['b']

add_call_add = Node(
	a = Node(),
	b = Node(),
	self_ = FakeNode()
).named(root['add'].name+('add_call_add',), root['add'])
add_call_add.reference = root['add']
add_call_add['a'].reference = root['add']['a']['prev']
add_call_add['b'].reference = add_call_nat

add_call_if = Node(
	else_ = Node(),
	then = Node(),
	self_ = FakeNode()
).named(root['add'].name+('add_call_if',), root['add'])
add_call_if.reference = root['add']['a']['if_']
add_call_if['else_'].reference = root['add']['b']
add_call_if['then'].reference = add_call_add['self_']

root['add']['self_'].reference = add_call_if['self_']

fib_call_ifa = Node(
	else_ = Node(prev=Node()),
	then = Node(),
	self_ = FakeNode()
).named(root['fib'].name+('fib_call_ifa',), root['fib'])
fib_call_ifa.reference = root['fib']['n']['if_']
fib_call_ifa['else_'].reference = root['nat']['pos']
fib_call_ifa['else_']['prev'].reference = root['nat']['zero']
root['fib']['self_'].reference = fib_call_ifa['self_']

fib_call_ifb = Node(
	else_ = Node(),
	then = Node(),
	self_ = FakeNode()
).named(root['fib'].name+('fib_call_ifb',), root['fib'])
fib_call_ifb.reference = root['fib']['n']['prev']['if_']
fib_call_ifb['else_'].reference = root['fib']['n']
fib_call_ifa['then'].reference = fib_call_ifb['self_']

fib_call_sum = Node(
	a = Node(),
	b = Node(),
	self_ = FakeNode()
).named(root['fib'].name+('fib_call_sum',), root['fib'])
fib_call_sum.reference = root['add']
fib_call_ifb['then'].reference = fib_call_sum['self_']

fib_call_fiba = Node(
	n = Node(),
	self_ = FakeNode()
).named(root['fib'].name+('fib_call_fiba',), root['fib'])
fib_call_fiba.reference = root['fib']
fib_call_fiba['n'].reference = root['fib']['n']['prev']
fib_call_sum['a'].reference = fib_call_fiba['self_']

fib_call_fibb = Node(
	n = Node(),
	self_ = FakeNode()
).named(root['fib'].name+('fib_call_fibb',), root['fib'])
fib_call_fibb.reference = root['fib']
fib_call_fibb['n'].reference = root['fib']['n']['prev']['prev']
fib_call_sum['b'].reference = fib_call_fibb['self_']

root_call_fib = Node(
	n = Node(prev=Node(prev=Node(prev=Node(prev=Node(prev=Node(prev=Node(prev=Node(prev=Node(prev=Node()))))))))),
	self_ = FakeNode()
).named(root.name+('root_call_fib',), root)
root_call_fib.reference = root['fib']
root_call_fib['n'].reference = root['nat']['pos']
root_call_fib['n']['prev'].reference = root['nat']['pos']
root_call_fib['n']['prev']['prev'].reference = root['nat']['pos']
root_call_fib['n']['prev']['prev']['prev'].reference = root['nat']['pos']
root_call_fib['n']['prev']['prev']['prev']['prev'].reference = root['nat']['pos']
root_call_fib['n']['prev']['prev']['prev']['prev']['prev'].reference = root['nat']['pos']
root_call_fib['n']['prev']['prev']['prev']['prev']['prev']['prev'].reference = root['nat']['pos']
root_call_fib['n']['prev']['prev']['prev']['prev']['prev']['prev']['prev'].reference = root['nat']['pos']
root_call_fib['n']['prev']['prev']['prev']['prev']['prev']['prev']['prev']['prev'].reference = root['nat']['pos']
root_call_fib['n']['prev']['prev']['prev']['prev']['prev']['prev']['prev']['prev']['prev'].reference = root['nat']['zero']

root['self_'].reference = root_call_fib['self_']
a, b = root['self_'].seek(Stack(), ())

def count(a, b, n=0):
	if a is root['nat']['zero']:
		return n
	else:
		return count(*a.seek(b, ('prev',)), n+1)

print(count(a, b))
