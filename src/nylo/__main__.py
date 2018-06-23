import nylo
import sys
import argparse


def main():
    """It starts the NyloCMD that could
    be managed using command line parameters.

    See `nylo -h` for that.
    """
    if len(sys.argv) <= 1:
        sys.argv.append('-h')
    sys.argv: list = sys.argv[1:]

    parser: object = argparse.ArgumentParser(
        description='A cool programming language')
    parser.add_argument('-f', '--file',
                        help='the file you want to evaluate')
    parser.add_argument('-v', '--version',
                        help='print current version',
                        action='version',
                        version='nylo 0.1.0')
    parser.add_argument('-i', '--inline',
                        help='inline command line',
                        action='store_true')
    args: object = parser.parse_args(sys.argv)

    if args.inline:
        previous_code: str = ''
        statement: bool = False
        while True:
            try:
                if not statement:
                    code: str = input(' -> ')
                else:
                    code: str = input('... ')

                if not code:
                    code: str = previous_code
                    statement: bool = False
                    previous_code: str = ''
                elif code[-1] == ':':
                    previous_code += code + '\n'
                    statement: bool = True
                    continue
                elif statement:
                    previous_code += code + '\n'

                if not statement:
                    reader: object = nylo.Reader(code + '\n')
                    struct: object = nylo.Struct(reader).value
                    if hasattr(struct, 'calculate'):
                        out: object = struct.calculate(nylo.nyglobals)
                    else:
                        out: object = struct.evaluate(nylo.nyglobals)
                    if out.value and str(out) != '()':
                        print(out)
                del code
            except Exception as e:
                print(e)

    if args.file is not None:
        with open(args.file, 'r') as codefile:
            code: object = codefile.read()
        reader: object = nylo.Reader(code)
        struct: object = nylo.Struct(reader)
        print(struct)


if __name__ == '__main__':
    main()
