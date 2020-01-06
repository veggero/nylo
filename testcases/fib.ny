nat: (
	pos: (
		
		succ: nat.pos(
			prev: nat.pos
		)
		
		prev: nat
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
add: (
	a: ()
	b: ()
	-> a.if(
		then: add(
			a: a.prev
			b: b.succ
		)
		else: b
	)
)
fib: (
	n: ()
	-> n.if(
		then: n.prev.if(
			then: add(
				a: fib(
					n: n.prev
				)
				b: fib(
					n: n.prev.prev
				)
			)
			else: 1
		)
		else: 1
	)
)

-> fib(n: 11)
