// Fibonacci in Nylo

impfib:
    int n
    int prevs: impfib(n-1) + impfib(n-2)
    int result: if(n<2, n, prevs)
    example: impfib(16)
    -> result

expfib:
    int n
    int prevs: expfib(int n: n-1) + expfib(n: n-2)
    int result: if(n<2, n, prevs)
    example: expfib(int n: 16)
    -> result
    
-> expfib(-> example) + impfib(-> example)
