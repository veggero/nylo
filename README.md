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
    
In order to repeat code multiple times, use brackets after integers

    2{
        print("This will be printed 2 times.")
    }
    
To write an if statement, use brackets after a boolean

    2>3{
        print("Math is clearly broken.")
    }

To iterate a list, use a function with a single argument after a list

    [1,2,3,4,5] {int number |
        print (number)
    }

Also, ranges syntax is start:stop[:step]

    5:10
    list int numbers: 2:10:2 
    1:100 {x | print(x)}
    
Here's an example where every number from 1 to 100 is printed 4 times if it's bigger than 12:

    1:100 { int x |
        x > 12 {
            4 {
                print (x)
            }
        }
    }
    
In order to join lists or strings use &

    'hello ' & 'world'
    ['sugar'] & ['salt']
    
If a function expects just an argument but a list is given, the function will be called one time for every element in the list. Example: 

    > hungry: { string x | print('Ate ' & x) }
    
    > hungry( ['chocolate', 'apple', 'banana'] )
    
    Ate chocolate
    Ate apple
    Ate banana
    
This also apply where there is more than one argument:

    > [1,2,3,4,5,6] + 1
    [2,3,4,5,6,7]
    
    > [1,2,3] + [3,4,5]
    [[4,5,6], [5,6,7], [6,7,8]]
    
Here is a bit more complicated example of that. Let's say you want to do this, per ex. to create a 50^ line:

    [[20*sin(50), 20*cos(50)], [40*sin(50)], [40*cos(50)]
    
This can be written in Nylo as

    [20, 40] * [sin(50), cos(50)]
    
because Nylo will automatically do all the combinations (20*sin(50), 20*cos(50) etc) as the symbol * expected only one int argument on the left and on the right but found int lists in both.
    
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

    example_input : [3,1,4,2,5]
    example_output: [
                    [3,1,4,2,5],
                    [4,5,6,7],
                    [9,11,13],
                    [20,24],
                    [44]
                ]
                
    pyramid: {list int layer|
        len(layer)=1{return [layer]}
        next_layer: layer(2)sum
        return [layer] & pyramid(next_layer)
    } 

docs:
    
   line 1: define the 'pyramid' function, with the argument layer (this will check if the argument is a list of integers and assign it to a 'layers' variable).
    
   line 2: check if the layer is only one element long and if so just return it in a one-element-long list (input: [2] output: [[2]])
    
   line 3: calculate the next layer by summing every couple of successive numbers (layer(2) returns every couple and 'sum' sum all them)
    
   line 4: calculate the pyramid of the next layer, join it with the already known layer, and return the pyramid
    
**Example 2: Parsing binary **

Return the number of successive 0s and 1s for every sequence in a binary string

    example_input : '00011000111100100000'
    example_output: [3,2,3,4,2,1,5]

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
            
