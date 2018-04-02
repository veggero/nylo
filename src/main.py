import nylo

r = nylo.Reader('''

double: (int n -> n * 2)

-> double(n: 4)
''')
out = nylo.Symbol(r).value

print(out)

print(out.evaluate(nylo.Stack()))

