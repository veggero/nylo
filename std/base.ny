bool: (
	true: ()
	false: ()
)

or: (
	a: bool
	b: bool
	example: or(
		a: bool.false
		b: bool.false
	)
	-> same(
		first: a
		second: bool.true
		then: a
		else: b
	)
)

nat: (
	zero: (
		succ: nat(prev: 0)
	)
	prev: nat
	succ: nat(prev: self)
)

sum: (
	a: nat
	b: nat
	-> same(
		first: a
		second: 0
		then: b
		else: sum(
			a: a.prev
			b: b.succ
		)
	)
)

eq: (
	a: nat
	b: nat
	-> same(
		first: a
		second: 0
		then: same(
			first: b
			second: 0
			then: bool.true
			else: bool.false
		)
		else: same(
			first: b
			second: 0
			then: bool.false
			else: eq(
				a: a.prev
				b: b.prev
			)
		)
	)
)

if: (
	cond: bool
	then: base
	else: base
	-> same(
		first: cond
		second: bool.true
		then: then
		else: else
	)
)

fib: (
	n: nat
	prevs: sum(
		a: fib(n: n.prev) 
		b: fib(n: n.prev.prev)
	)
	-> if(
		cond: or(
			a: eq(a: n, b: 0)
			b: eq(a: n, b: 1) 
		),
		then: nat(prev: 0)
		else: prevs 
	)
)

list: (
	end: ()
	value: base
	next: list
)

-> [1 2]
