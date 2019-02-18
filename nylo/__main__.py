import sys
from pprint import pprint, pformat
from parser import Parser, newParser
from code import Code
from mesh import newMesh
from writer import Writer
import time

if not len(sys.argv) - 1:
	exit('usage: nylo file.ny')
	
this, target = sys.argv
name = target.partition('/')[2].partition('.')[0]

first_before = time.time()

for i in range(5):
	std_parser = Parser(Code('('+open('std/base.ny', 'r').read()+')'))
	std_parser.parse(('base',))
	parser = Parser(Code('('+open(target, 'r').read()+')'))
	parser.parse(('base', name,))
	parser.mesh.update(std_parser.mesh)
	parser.mesh.bind()
	writer = Writer(parser.mesh)
	(writer.write(('base', name, 'self')))

second_before = time.time()


for i in range(5):
	std_parser = newParser(Code('('+open('std/base.ny', 'r').read()+')'))
	parser = newParser(Code('('+open(target, 'r').read()+')'))
	std_obj = (None, {'base': std_parser.parse(('base',))})
	obj = parser.parse(('base', name))
	std_obj[1]['base'][1][name] = obj
	nM = newMesh(std_obj)
	nM.obj = nM.bind()
	writer = Writer(nM)
	(writer.write(('base', name, 'self')))

after = time.time()

old = round(second_before-first_before, 2)
new = round(after-second_before, 2)
ratio = round(old/new, 2)

print(f'\nNew: {new}s\nOld: {old}s\nRatio: {ratio}')
