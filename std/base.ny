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
	zero: ()
	prev: nat
	succ: nat(prev: self)
)

-> nat(prev: nat.zero -> succ)
