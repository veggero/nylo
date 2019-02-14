from code import Code
from pprint import pformat
from parser import newParser, Parser
c = open('../std/base.ny', 'r').read()
p = newParser(Code('('+c+')'))
o = p.parse(('base',))
p.convert(o, ('base',))
open('dopo.txt', 'w').write(pformat(p.mesh))

p = Parser(Code('('+c+')'))
p.parse(('base',))
open('prima.txt', 'w').write(pformat(p.mesh))
