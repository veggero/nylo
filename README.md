// Nylo. Syntax so good you will riconsider sex.

![](images/NyloBanner.png)

Usually, what programming language you use for a project is given by what kind of project it is. If you're going to do a front-end non-static webpage, you'll probably end up using JavaScript. What you have to deal with, though, it's the syntax and how-easy-to-use that language is.
Nylo's target is providing a very good, clear and concise syntax plus compability with many programming aspects such as front-end and back-end development, android/iOS/Windows app development, etc, in order to give you the possibility to use a confortable, known, good syntax whatever you're doing. 

**Why is Nylo such awesome?**

Good question, thanks for asking. Here's a couple features you might like from Nylo:

**1) Colon as assignation symbol**

    answer: 42

This isn't exactly a exciting feature, but we really have to tell you about this to make you understand most Nylo examples. In order to assign a variable you shall use : instead of =. This is for three reasons: 
First, in this way we can use = instead of == to actually confront two variables, wich makes it more clear .
Second, using a = as assignation symbol doesn't make any sense, as expressions like a=a+1 are impossible for any school-grade kid. Assignation and equalization are simply two different things.
Third, we wanted to make a more dictionary-like assignation. In dictionaries you use colon to separate couples of key and value, and in code you use colon to assign a value.

**2) Quick function syntax**

    double: {x | x+1}
    
In Nylo you will quite often use functions, as we encourage them more than in other languages. We therefore created a more concise and easy function definition: {[arguments |] code}.

    // Arguments are facultative
    mew: {print('meeow')}
    mew()
    
**3) Kinda Dynamic Types**

Is Nylo strongly, weakly or dynamic typed? Well, kinda none of them. In Nylo you can specify the types, although it's facultative:

    int x: 3
    string k: 'hello world'
    
    list int: [1,2,3]
    list list string: [['a', 'b'], ['c']]
    
You can also include some test in this:

    int[>0]: 4
    string[len()<20] = 'short string'
    
    list[len()>5] int[0<<5]: [1, 3, 4, 2, 1, 5]
    list[len()=1] list[len(list[0])=0] string: [['', 'a'], ['', 'b']]
    
Although, you can pretty much save whatever you want in any variable. But if you try to save a value in a variable that doesn't fit its arguments while in debug mode, an exception will be raised.

Of course, you can set types in function definitions too:

    {int x, y | x + y}
    {string[len()>5] k | print(k)}
    
    // Multiple arguments
    ignore_a_bunch: {int x, y, string k, z, list int n}
    
You should always check your function's types and value:

    gimme_binary: {list char[='0' or ='1'] binary | return(binary)}
    
**4) Calling objects with functions**

In Nylo every object or istance can manage being called both with (values) and {functions}, even at the same time. Here's a couple of common examples of it:

    forever {print('hi')}
    if (3=2) {print('math is broken')}
    
Forever and if are two variables referring to buil-it objects, but in Nylo you can also call istances of common types:

    // repeat 2 times a piece of code
    2{} 
    // execute code only if true (this is a if without the if)
    (3=2){}
    // execute code one time for element
    [1,2,3]{x|}
    
Obviusly, you can yourself create objects that can manage being called by functions.

**5) Quick and dirty class definition and istances creation**

Classes and istances are really really easy:

    point: {int x, y}
    point c: 3, -1
    
    money: {string currency, int value}
    money ticket: '$', 20
    
Obviusly you can also add functions to classes:

    point: {int x, y |
        move: {
            // no need to use self or this
            x +: 1
            y +: 1
        }
    }
    

**6) Quick and dirty special args everywhere**

    print('hello console!')
    print('hello file!' | to: 'file.txt')
    
You can pass special arguments to functions, just like in many other programming languages, with (values | *args). This is althogh not limited just to round brackets. 

Let's say you want to get a the i-th value from a list, but returning 4 if i is outside of the list (like, 
    [1,2,3][5] 
or 
    [1,2,3][-2]
). You can add a special argument to the call:

    list[i | standard: 4]
    
And you can even add them to functions that calls objects.

    // while i>0, subtract 1 to i
    // without repeat: inf, this would be a normal if statement
    (i>0){i: i-1 | repeat: inf}
    
    // obv you can also use int numbers here. This will subtract
    // 5 to i unless it reaches 0s
    (i>0){i: i-1 | repeat: 5}
    
**7) Small tasks made easy with the implicit variable**

This is the code to add 1 to a number:

    > add: {+1}
    > add(3)
    < 4

And this is the code to check if a number is inside the range from 0 to 10:

    > is_between: {0<<10}
    > is_between(3)
    < true
    
If there is a function without arguments called with just one argument, it will be set to 'implicit'. Also, if you put a symbol that clearly miss one argument, it will set the missing one to 'implicit'. This is because some functions, such as split, also require a small function. 
Ad ex, this is how you split a string on spaces in nylo

    split ('hello world') {=' '}

The second argument is a quick function that checks if the argument it's called with is a space. If it returns true, split will split the string. This is a more complex example with split:

    > split ('au3oe8eu4a9') {x | int (x | standard: 9) < 5}
    < ['au', 'oe8eu', 'a9']
    
**8) Built-in argument iterations**

    > [1,2,3] + 1
    < [2,3,4]
    
When you call a function that expects a x-type argument with a list of x-type arguments, Nylo will call the function multiple times, one with every argument in the list and join the return values in a single list. Here's a simple example: (& is the join operator)

    > fn: {int x | print('called with ' & x); return(x)}
    > print( fn(1,2,3) )
    < called with 1
    < called with 2
    < called with 3
    < 1,2,3
    
fn expected just an integer, but a list of integer was given. Therefore, the function was called multiple times. This is useful in many cases:

    > // sum expects two int, but two lists of integers were given.
    > // therefore, sum will be called with every combination of them:
    > [1,2,3,5] + [9,10]
    < [[10,11,12,14], [11,12,13,15]]
    
    > [1,2,3] * [1, 10]
    < [[1,2,3], [10,20,30]]
    
    > // getting multiple elements of a list at the same time!
    > [1,2,3][0,2]
    < [1,3]
    
    // printing multiple lines at the same times!
    print('these are all', 'different lines!')
    
    // quick edit on big lists:
    list: [1,2,3,4,5,6,7,8]
    top: max(list)
    list: {int x | x^2 / top^2} (list)
    
**Examples: dealing with recursions and lists**

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
    in the first example we take every couple of successive numbers and we print the sum of them.
    the output would be: 3 5 7 
    you could achieve the same with a special argument:
    [1,2,3,4] {a,b | print(a+b) | items: 2}

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
        (len(layer)=1){return([layer])}
        next_layer: layer(2)sum
        return([layer] & pyramid(next_layer))
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
            (left=right) {parsed[-1]+:1} 
            else {parsed.append(0)}
        }
        return(parsed+1)
    }
        
docs:

   line 1: define the get_binary function with a single 'binary' argument, which is a list of characters that are either '0' or '1'
   
   line 2: define a 'parsed' list - we will edit it as we iterate over the binary string
   
   line 3: we call a function with every two successives numbers in binary, calling them 'left' and 'right'
   
   line 4: if they're equals we add one to the last element of parsed - in this way we count the number of successive equals chars
   
   line 5: if they're not equals we add a 0 to parsed, in order to reset the counter
   
   line 7: we return the parsed list adding one to every element of it (because we ignored the first element of every sequence of 0s and 1s)
            
