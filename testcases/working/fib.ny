// Fibonacci in Nylo

fib:
    int n
    prevs: fib(n-1) + fib(n-2)
    result: if(n<2, n, prevs)
    example:
        fib(16)
    -> result
    
-> fib.example
