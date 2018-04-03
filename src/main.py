import nylo

r = nylo.Reader('''
    
fib:
    int n
    int prevs: 
        fib(n-1) + fib(n-2)
    int result: 
        if
            n<2
            n
            prevs
    -> result
   
-> fib(16)

''')


out = nylo.Symbol(r).value

print(out)

print(out.calculate(nylo.nyglobals))

