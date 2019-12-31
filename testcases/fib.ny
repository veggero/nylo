nat: (
	pos: (
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
	)
)
add: (
	a: ()
	b: ()
	c: a.if(
		then: add(
			a: a.prev
			b: nat.pos(prev: b)
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
			else: nat.pos(prev: nat.zero)
		)
		else: nat.pos(prev: nat.zero)
	)
	-> s
)
k : fib(n: nat.pos(prev: nat.pos(prev: nat.pos(prev: nat.pos(prev: nat.pos(prev: nat.pos(prev: nat.pos(prev: nat.pos(prev: nat.pos(prev: nat.zero))))))))))
-> k
