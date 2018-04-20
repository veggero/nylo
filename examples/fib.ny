"Fibonacci in Nylo"

"To execute:"
"[veggero@yara nylo]$ python3 src/main.py -f examples/fib.ny"

fib:
    int n
    int prevs: fib(n-1) + fib(n-2)
    int result: if(n<2, n, prevs)
    example: fib(16)
    -> result
   
-> fib
    ->example
