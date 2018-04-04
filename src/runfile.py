import nylo
import sys

with open(sys.argv[-1], 'r') as codefile: code = codefile.read()

reader = nylo.Reader(code)
struct = nylo.Struct(reader).value
print(struct.calculate(nylo.nyglobals))
