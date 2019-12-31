from interpreter import Node, Stack
from typing import Union

def write(node: Node, stack: Stack) -> str:
	if node.name[-2:] == ('nat', 'zero'):
		return '0'
	elif node.name[-2:] == ('nat', 'pos'):
		return str(1 + int(write(*node.seek(stack, ('prev',)))))
	else:
		return repr(node)
