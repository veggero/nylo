import nylo
import sys
import argparse

if len(sys.argv) <= 1:
    sys.argv.append('-h')
sys.argv = sys.argv[1:]

parser = argparse.ArgumentParser(description='A cool programming language')
parser.add_argument('-f', '--file',
                     help='the file you want to evaluate')
parser.add_argument('-v', '--version',
                     help='print current version',
                     action='version',
                     version='nylo 0.1')
args = parser.parse_args(sys.argv)

with open(args.file, 'r') as codefile:
    code = codefile.read()

reader = nylo.Reader(code)
struct = nylo.Struct(reader).value

struct.settype(['obj'], nylo.nyglobals)

print(struct.calculate(nylo.nyglobals))

