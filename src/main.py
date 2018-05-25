# This file is a part of nylo
#
# Copyright (c) 2018 The nylo Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
                    print(struct.evaluate(nylo.nyglobals))
                del code
            except Exception as e:
                print(e)

    if args.file is not None:
        with open(args.file, 'r') as codefile:
            code: object = codefile.read()
        reader: object = nylo.Reader(code)
        struct: object = nylo.Struct(reader).value
        #struct.settype(['obj'], nylo.nyglobals)
        print(struct.evaluate(nylo.nyglobals))


if __name__ == '__main__':
    main()
