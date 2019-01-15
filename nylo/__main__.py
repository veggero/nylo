import sys
from parser import Parser
from code import Code
from pprint import pprint

if not len(sys.argv) - 1:
	exit('usage: nylo file.ny')
	
this, target = sys.argv
name = target.partition('/')[2].partition('.')[0]

parser = Parser(Code('('+open(target, 'r').read()+')'))
parser.parse((name,))
parser.mesh.bind()

print('.'.join(parser.mesh.valueof((name, 'self'))))
