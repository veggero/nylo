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
		succ: nat(prev: nat.zero)
	)
	prev: nat
	succ: nat(prev: self)
)

sum: (
	a: nat
	b: nat
	-> same(
		first: a
		second: nat.zero
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
		second: nat.zero
		then: same(
			first: b
			second: nat.zero
			then: bool.true
			else: bool.false
		)
		else: same(
			first: b
			second: nat.zero
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
			a: eq(a: n, b: nat.zero)
			b: eq(a: n, b: nat(prev: nat.zero)) 
		),
		then: nat(prev: nat.zero)
		else: prevs 
	)
)
