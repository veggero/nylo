import sys
from pprint import pprint
from parser import Parser
from code import Code
from writer import Writer

if not len(sys.argv) - 1:
	exit('usage: nylo file.ny')
	
this, target = sys.argv
name = target.partition('/')[2].partition('.')[0]

parser = Parser(Code('('+open(target, 'r').read()+')'))
parser.parse((name,))
parser.mesh.bind()
writer = Writer(parser.mesh)

pprint(parser.mesh)
print(writer.write((name, 'self')))
