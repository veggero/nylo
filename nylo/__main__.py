import sys
from pprint import pprint
from parser import Parser, newParser
from code import Code
from writer import Writer

if not len(sys.argv) - 1:
	exit('usage: nylo file.ny')
	
this, target = sys.argv
name = target.partition('/')[2].partition('.')[0]

std_parser = newParser(Code('('+open('std/base.ny', 'r').read()+')'))
o = std_parser.parse(('base',))
std_parser.convert(o, ('base',))

parser = newParser(Code('('+open(target, 'r').read()+')'))
o = parser.parse(('base', name,))
parser.convert(o, ('base', name))
parser.mesh.update(std_parser.mesh)
parser.mesh.bind()
writer = Writer(parser.mesh)

#print("size in >", len(parser.mesh), sys.getsizeof(parser.mesh)/1000)
print(writer.write(('base', name, 'self')))
#print("size out <", len(parser.mesh), sys.getsizeof(parser.mesh)/1000)
