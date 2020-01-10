nat: (
	pos: (
		
		prev: nat
		
		succ: nat.pos(
			prev: nat.pos
		)
		
		if: (
			then: ()
			else: ()
			-> then
		)
	)
	zero: (
		if: (
			then: ()
			else: ()
			-> else
		)
		succ: 1
	)
)
fib: (
	n: ()
	-> n.if(
		then: n.prev.if(
			then: + fib(n: n.prev) fib(n: n.prev.prev)
			else: 1
		)
		else: 1
	)
)

`+`: (
	first: ()
	second: ()
	-> first.if(
		then: + first.prev second.succ
		else: second
	)
)

double: (n: nat -> + n n)
ten: (k: () -> k(n: 5))
curry: double(n: 5 ->)

-> curry()
