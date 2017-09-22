# Nylo. Syntax so good you will riconsider sex.

Nylo's target is providing good and simple syntax for comfortable coding, plus giving a bunch of common built-in function to do most of the hard work.

**1: The Basics**

Use : instead of = for assignations.

    answer: 42
    int nine: 9
    list string names: ['clye', 'yara', 'phyre']
    
Functions' syntax is { arguments | code }. In order to declare a function, assign it to a variable. If no arguments are needed, you can just use { code }. 'return' is facultative on single-line functions.

    double: {x | x * 2}
    sum: {a, b | a + b}
    meow: { print('meow') }
    
You can also specify in the function the types of arguments you expect.

    gimme_an_integer: {int x | print(x)}
    gimme_two_integers_and_a_string: {int x, y, string c | print(a, b, c) }
    gimme_a_list_of_integers: {list int x | print(x)}
    
Classes' syntaxs is { arguments / datas }. 

    point: {int x, y}
    money: {int value, string currency}
    kid: {int age, money purse}
    
You can include functions in classes with the functions' syntax.

    point: {int x, y |
        move: {
            x++
            y++
        }
    }
    
To create a istance of a class, either call it or assign a variable:

    point c: 1, 2
    money ticket: 20, '$'
    kid Yara: 16, money(50, 'EUR')
    
2: Dealing with recursions and lists

Useful functions:

    > list function
    example: [1,2,3,4]{x | print(x)}
    a function after a list will be called one time for every element of the list, with the element as argument
    the example will simply print every element of the list [1,2,3,4]
    since {x | print(x)} works just like the print function itself, we could also write
    > [1,2,3,4] print
    getting the same result
    
    > list (number) function
    example: [1,2,3,4] (2) {a,b | print(a+b)}
    calling a list with a number will create a new list made by successive couples of elements
    example: [1,2,3,4](2)   --> [[1,2], [2,3], [3,4]]
    example: [1,2,3,4,5](3) --> [[1,2,3], [2,3,4], [3,4,5]]
    adding also a function after this, we can work on multiple element of the original list at the same time.
    in the example we take every couple of successive numbers and we print the sum of them.
    the output would be: 3 5 7 

Example 1: Pyramid of numbers 

Given a list of integers, return a pyramid, where each number in each successive layer is the sum of the two
'under' them.

    example input : [3,1,4,2,5]
    example output: [
                    [3,1,4,2,5],
                    [4,5,6,7],
                    [9,11,13],
                    [20,24],
                    [44]
                ]
                
    pyramid: {list int layer|
        len(layer)=1{return [layer]}
        next_layer: layer(2)sum
        return [layer] . pyramid(next_layer)
    } 

docs:
    
   line 1: define the 'pyramid' function, with the argument layer (this will check if the argument is a list of integers and assign it to a 'layers' variable).
    
   line 2: check if the layer is only one element long and if so just return it in a one-element-long list (input: [2] output: [[2]])
    
   line 3: calculate the next layer by summing every couple of successive numbers (layer(2) returns every couple and 'sum' sum all them)
    
   line 4: calculate the pyramid of the next layer, join it with the already known layer, and return the pyramid
    
**Example 2: Parsing binary **

Return the number of successive 0s and 1s for every sequence in a binary string

example input : '00011000111100100000'
example output: [3,2,3,4,2,1,5]

    get_binary: {list char[='0' or ='1'] binary|
        parsed: [0]  
        binary(2){left, right|
            left=right {parsed[-1]++} 
            else {parsed.append(0)}
        }
        return parsed+1
    }
        
docs:

   line 1: define the get_binary function with a single 'binary' argument, which is a list of characters that are either '0' or '1'
   
   line 2: define a 'parsed' list - we will edit it as we iterate over the binary string
   
   line 3: we call a function with every two successives numbers in binary, calling them 'left' and 'right'
   
   line 4: if they're equals we add one to the last element of parsed - in this way we count the number of successive equals chars
   
   line 5: if they're not equals we add a 0 to parsed, in order to reset the counter
   
   line 7: we return the parsed list adding one to every element of it (because we ignored the first element of every sequence of 0s and 1s)
            
