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
import readline
from collections import defaultdict

def main():
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
                        version='nylo 0.1.0')
    parser.add_argument('-i', '--inline',
                        help='inline command line',
                        action='store_true')
    args = parser.parse_args(sys.argv)

    if args.inline:
        previous_code = ''
        statement = False
        while True:
            try:
                if not statement:
                    code = input(' -> ')
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
                    reader = nylo.Reader(code + '\n')
                    struct = nylo.Struct(reader).value
                    if hasattr(struct, 'calculate'):
                        out = struct.calculate(nylo.nyglobals)
                    else:
                        out = struct.evaluate(nylo.nyglobals)
                    if isinstance(out, nylo.objects.struct.struct.Struct):
                        nylo.nyglobals = nylo.nyglobals(out)
                    if out.value != None and str(out) != '()': print(out)
                del code 
            except Exception as e:
                print(e)

    if args.file is not None:
        with open(args.file, 'r') as codefile:
            code = codefile.read()
        reader = nylo.Reader(code)
        struct = nylo.Struct(reader).value
        # struct.settype(['obj'], nylo.nyglobals)
        print(struct.calculate(nylo.nyglobals))


if __name__ == '__main__':
    main()
