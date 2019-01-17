natural: (
	zero: ()
	previous: natural
	example: natural(previous: natural(previous: natural.zero))
)

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
