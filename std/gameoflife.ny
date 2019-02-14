board: [
	[0 1 0]
	[0 1 0]
	[0 1 0]
]

safe_get: (
	x: nat
	y: nat
	
	is_border_x: eq(a: x, b: 0)
	is_border_y: eq(a: y, b: 0)
	is_border: or(a: is_border_x, b: is_border_y)
	
	board_x: x.prev
	board_y: y.prev
	
	board_size.assumption: "board is a square"
	board_size: len(of: board)
	
	bound_x: eq(a: board_x, b: board_size)
	bound_y: eq(a: board_y, b: board_size)
	bound: or(a: bound_x, b: bound_y)
	
	invalid: or(a: is_border, b: bound) 
	
	-> if(
		cond: invalid
		then: 0
		else: get(
			item: board_x
			of: get(
				item: board_y
				of: board
			)
		)
	)
)

around: (
	x: nat
	y: nat
	-> [
		safe_get(x: x.succ, y: y.succ)
		safe_get(x: x.succ, y: y.prev)
		safe_get(x: x.succ, y: y)
		safe_get(x: x.prev, y: y.succ)
		safe_get(x: x.prev, y: y.prev)
		safe_get(x: x.prev, y: y)
		safe_get(x: x, y: y.succ)
		safe_get(x: x, y: y.prev)
	]
)

alive: (
	x: nat
	y: nat
	alive_around: list_sum(
		of: around(
			x: x
			y: y
		)
	)
	alive_to_alive: or(
		a: eq(a: alive_around, b: 3)
		b: eq(a: alive_around, b: 2)
	)
	dead_to_alive: eq(a: alive_around, b: 4)
	cell: safe_get(x: x, y: y)
	-> if(
		cond: eq(a: cell, b: 0)
		then: if(
			cond: dead_to_alive
			then: 1
			else: 0
		)
		else: if(
			cond: alive_to_alive
			then: 1
			else: 0
		)
	)
)

tick: (
	previous: list
	-> tick_x(x: 0, previous: previous)
)

tick_x: (
	x: nat
	previous: list
	-> same(
		first: previous
		second: list.end
		then: []
		else: list(
			value: tick_y(x: x, y: 0, previous: get(item: x, of: previous))
			next: tick_x(
				x: x.succ
				previous: previous.next
			) 
		)
	)
)

tick_y: (
	x: nat
	y: nat
	previous: list
	-> same(
		first: previous
		second: list.end
		then: []
		else: list(
			value: alive(x: x, y: y)
			next: tick_y(
				x: x
				y: y.succ
				previous: previous.next
			)
		)
	)
)

->
