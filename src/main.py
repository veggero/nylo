import nylo
import sys
import argparse

if len(sys.argv) <= 1:
    sys.argv.append('-h')
sys.argv = sys.argv[1:]

parser = argparse.ArgumentParser(
                                 description='A cool programming language')
parser.add_argument('-f', '--file',
                    help='the file you want to evaluate')
parser.add_argument('-v', '--version',
                    help='print current version',
                    action='version',
                    version='nylo 0.1')
parser.add_argument('-i', '--inline',
                    help='inline command line',
                    action='store_true')
args = parser.parse_args(sys.argv)

if args.inline is not None:
    previous_code = ''
    statement = False
    while True:
        try:
            if not statement:
                code = input('-> ')
            else:
                code = input('... ')

            if not code:
                code = previous_code
                statement = False
                previous_code = ''
            elif code[-1] == ':':
                previous_code += code + '\n'
                statement = True
                continue
            elif statement:
                previous_code += code + '\n'

            if not statement:
                reader = nylo.Reader(code)
                struct = nylo.Struct(reader).value
                print(struct.calculate(nylo.nyglobals))
            del code
        except Exception as e:
            print(e)


if args.file is not None:
    with open(args.file, 'r') as codefile:
        code = codefile.read()

    reader = nylo.Reader(code)
    struct = nylo.Struct(reader).value
    struct.settypes(['obj'], nylo.builtins)

    print(struct.calculate(nylo.nyglobals))
