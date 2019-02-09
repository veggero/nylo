bool: (
	true: (
		(|): (
			args: [bool.true bool]
			-> bool.true
		)
		(=): (
			args: [bool.true bool]
			-> args.next.value
		)
	)
	false: (
		(|): (
			args: [bool.true bool]
			-> args.next.value
		)
		(=): (
			args: [bool.false bool]
			-> same(
				first: args.next.value
				second: bool.false
				then: bool.true
				else: bool.false
			)
		)
	)
)

nat: (
	pos: (
		prev: nat
		succ: nat.pos(prev: self)
		
		(+): (
			args: [nat.pos nat]
			tests: [= + 1 0 1, = + 1 1 2]
			-> + args.value.prev args.next.value.succ
		)
		(=): (
			args: [nat.pos nat]
			tests: [= = 1 1 bool.true, = = 1 0 bool.false]
			-> same(
				first: args.next.value
				second: 0
				then: bool.false
				else: = args.value.prev args.next.value.prev
			)
		)
		tests: & (+).tests (=).tests 
	)
	zero: (
		succ: nat.pos(prev: 0)
		
		(+): (
			args: [nat.zero nat] 
			tests: [= + 0 1 1, = + 0 0 0]
			-> args.next.value
		)
		(=): (
			args: [nat.zero nat]
			tests: [= = 0 0 bool.true, = = 0 1 bool.false]
			-> same(
				first: args.next.value
				second: 0
				then: bool.true
				else: bool.false
			)
		)
		tests: & (+).tests (=).tests 
	)
	tests: & pos.tests zero.tests
)

list: (
	element: (
		value: base
		next: list
		(&): (
			args: [list.element list]
			-> & 
				args.value.next 
				list.element(value: args.value.value, next: args.next.value)
		)
	)
	end: (
		(&): (
			args: [list.end list]
			-> args.next.value
		)
	)
)

string: (
	characters: list
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
	prevs: + fib(n: n.prev) fib(n: n.prev.prev)
	-> if(
		cond: | = n 0 = n 1 
		then: 1
		else: prevs 
	)
)

get: (
	item: nat
	of: list
	error: ()
	-> same(
		first: of
		second: list.end
		then: error
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
		then: + total of.value
		else: list_sum_(
			of: of.next
			total: + total of.value
		)
	)
)
