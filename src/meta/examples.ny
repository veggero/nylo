// Project Euler
// projecteuler.ne

// n. 1

(
	list int num_range: 0..1001,
	list int multiple_3: filter(num_range, %3=0),
	list int multiple_5: filter(num_range, %5=0),
	list int multiples: filter(num_range, in multiple_3 and in multiple_5)
	-> sum(multiples)
)

// n. 2

(
	list int num_range: 0..4000001,
	fun fib: (
		int, 
		int prev_fib: fib(int-1)+fib(int-2),
		int n_fib: if(int < 2, int, prev_fib), 
		bool is_even: n_fib % 2 = 0
		-> n_fib
     	),
	list int even_fibs: filter(num_range, int -> fib(int: is_even))
	-> sum(even_fibs)
)

// n. 3

(
	int number: 600851475143,
	number(->divisors),
	fun is_prime: int -> len(int(:divisors)) = 0,
	-> filter(divisors, is_prime)
)

// n. 4

(
	fun char_is_pal: (str, int -> str[int] = str[len(str), int]),
	fun is_pal: (
		int pal
		-> map(0..len(pal.str), (int char_is_pal(pal.str, int)))
	),
	list int numbers: 999..99,
	-> filter(numbers, is_pal)[0]
)
