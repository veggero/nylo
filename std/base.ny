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
	pos: (
		prev: nat
		succ: nat.pos(prev: self)
	)
	zero: ()
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
		then: 1
		else: prevs 
	)
)

list: (
	element: (
		value: base
		next: list
	)
	end: ()
)

string: (
	characters: list
)

get: (
	item: nat
	of: list
	-> same(
		first: of
		second: list.end
		then: "error"
		else: same(
			first: item
			second: 0
			then: of.value
			else: get(
				item: item.prev
				of: of.next
			)
		)
	)
)

len: (
	of: list
	-> len_(of: of, items: 1)
)

len_: (
	items: nat
	of: list
	-> same(
		first: of.next
		second: list.end
		then: items
		else: len_(
			items: items.succ
			of: of.next
		)
	)
)

list_sum: (
	of: list
	-> list_sum_(of: of, total: 0)
)

list_sum_: (
	of: list
	total: nat
	-> same(
		first: of.next
		second: list.end
		then: sum(a: total, b: of.value)
		else: list_sum_(
			of: of.next
			total: sum(a: total, b: of.value)
		)
	)
)
