import sys
from lexer import Code
from parser import parse
from interpreter import Stack

if not len(sys.argv) - 1:
	sys.exit('Usage: python3.7 nylo/ file.py')
	
this, target = sys.argv
name = target.partition('/')[2].partition('.')[0]
with open(target, 'r') as file:
	parsed = parse(Code(f'({file.read()})'))
parsed.bind(name = ('base', name))
output, stack = parsed.node['self'].seek(Stack())
print(output)
