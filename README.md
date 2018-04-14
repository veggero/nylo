![](https://github.com/pyTeens/nylo/blob/gh-pages/docs/images/new_nylo_banner.png) [![](https://travis-ci.org/pyTeens/nylo.svg?branch=master)](https://travis-ci.org/pyTeens/nylo)

# Welcome to Nylo

**Nylo** is a new programming language. It uses a declarative paradigm, but it's not function nor logical. In fact, its paradigm is a new one, that aims to be clear, easy and very logical. Nylo has a very few construct, without losing power.

```
// Namespaces:
main:

    // New types:
    point:
        int x, int y
        
    // Function definitions:
    fib:
        int n
        int prev_fibs: fib(n-1) + fib(n-2)
        -> if(n<2, n, prev_fibs)
        
    // List and dict declarations:
    todo:
        "Put a star to this project."
        "Follow the project."
        "Contribute"
    food_quality:
        "Nougat": 50
        "Chocolate": 25
        "Honey": 35


// Function calls:
draw
    on: screen
    at: point
        x: 10
        y: 10
    todraw: rectangle
        size: point
            x: 10
            y: 10
        color: color
            r: 0
            g: 0
            b: 255
```

# Contents
* [How to contribute](#how-to-contribute)
* [Release](#release)


## How to contribute

_In primis_ ("firstable"), you **must** be a member of [pyTeens](https://teens.python.it), then **ask** [@veggero](https://github.com/veggero)!

## Release

It will be released on the _25th_ of _May 2018!_


Special contributors:

[@veggero](https://github.com/veggero) since June 2017 

[pyTeens](https://teens.python.it) since January 2018

[@AmerigoGuadagno](https://github.com/AmerigoGuadagno) Since December 2017
