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
	c: a.if(
		then: add(
			a: a.prev
			b: b.succ
		)
		else: b
	)
	-> c
)
fib: (
	n: ()
	s: n.if(
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
	-> s
)
k: fib(n: 9)


test: (
	a: (
		b: 1
		-> b
	)
	c: a(b: d)
	d: a.b
	e: c.b
)
pk: test.c

-> k
