import nylo

r = nylo.Reader("""(main:

    fib:
        int n   
        int prev: 
            fib(n: n-1)+fib(n: n-2)
        int result: 
            if(n<2 n prev)
            
    -> fib
        n: 
            15
        -> result)""")

print(nylo.Call(r).value)
