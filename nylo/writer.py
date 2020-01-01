from interpreter import Node, Stack
from typing import Union

def write(node: Node, stack: Stack) -> str:
	if node.name[-2:] == ('nat', 'zero'):
		return '0'
	elif node.name[-2:] == ('nat', 'pos'):
		i = 0
		while node.name[-2:] != ('nat', 'zero'):
			i += 1
			node, stack = node.seek(stack, ('prev',))
		return i
	else:
		return repr(node)
