import nylo

r = nylo.Reader('''

double: 
    int n
    int result: n * 2
    -> result
    
testcase:
    int a
    int b: double(n: a)
    int c: double(n: b)
    int d: double(n: c)

-> testcase(a: 3 -> d)
''')


out = nylo.Symbol(r).value

print(out)

print(out.calculate(nylo.Stack()))

