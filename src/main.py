import nylo
import sys
import argparse
from pprint import pprint as print

sys.argv.pop(0)
if not sys.argv:
    sys.argv.append('-h')
parser = argparse.ArgumentParser("Nylo Programming Language")
parser.add_argument('-f', '--file',
                    help='the file you want to evaluate')
parser.add_argument('-v', '--version',
                    help='print current version',
                    action='version',
                    version='nylo 0.1.0')
args = parser.parse_args(sys.argv)

if args.file:
    with open(args.file, 'r') as codefile:
        code = codefile.read()
    struct = nylo.Parser.parsecode(code)
    mesh = nylo.builtins
    struct.transpile(mesh, ())
    print(struct)
    print(mesh)
