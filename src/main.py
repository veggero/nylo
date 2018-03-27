import nylo

#r = nylo.Reader("""(main:
#
#    fib:
#        int n   
#        int prev: 
#            fib(n: n-1)+fib(n: n-2)
#        int result: 
#            if(n<2 n prev)
#            
#    -> fib
#        n: 
#            15
#        -> result)""")

r = nylo.Reader('test(1, 2, 3 -> 4)')

print(nylo.Symbol(r).value)
