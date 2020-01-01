import sys
from lexer import Code
from parser import parse
from writer import write

if not len(sys.argv) - 1:
	#sys.exit('Usage: python3.7 nylo/ file.py')
	this = sys.argv[0]
	target = 'testcases/fib.ny'
else:
	this, target = sys.argv

name = target.partition('/')[2].partition('.')[0]

with open(target, 'r') as file:
	parsed = parse(Code(f'({file.read()})'))

parsed.bind(name = ('base', name))

print(write(*parsed.node['self'].seek({})))
