![](https://raw.githubusercontent.com/pyTeens/nylo/gh-pages/docs/images/new_big_nylo_banner.png) [![](https://travis-ci.org/pyTeens/nylo.svg?branch=master)](https://travis-ci.org/pyTeens/nylo)

# Welcome to nylo

**nylo** (/nylo/) is a **programming language** written in [Python](https://python.org). It is knows due to its **simplicity** and **style**. As you should know: **nylo** is absolutely **user-friendly**, you could write code in few lines, less than what you would think!

```
fib:
    int n
    -> if
       n<2
       n
       fib(n-1)+fib(n-2)
```

* [**Main Repository**](https://github.com/pyTeens/nylo)

# Contents
* [How to contribute](#how-to-contribute)
* [Release](#release)
* The 6 commandments_
    1. [Beautiful is better than ugly](#beautiful-is-better-than-ugly)
    2. [Explicit is better than implicit](#explicit-is-better-than-implicit)
    3. [Simple is better than complex](#simple-is-better-than-complex)
    4. [Complex is better than complicated](#complex-is-better-than-complicated)
    5. [Flat is better than nested](#flat-is-better-than-nested)
    6. [Sparse is better than dense](#sparse-is-better-than-dense)

## How to contribute

_In primis_ ("firstable"), you **must** be a member of [pyTeens](https://teens.python.it), then **ask** [@veggero](https://github.com/veggero)!

## Release

It will be released on the _25th_ of _May 2018!_

## The 6 commandments

### Beautiful is better than ugly

**Indentation**, **colons** and **few symbols** makes nylo beautiful.

```
fib:
    int n
    -> if
       n<2
       n
       fib(n-1)+fib(n-2)
```

*Feel the chapeau?*

### Explicit is better than implicit

Nylo makes everything explicit, even function calls!

```
draw:
    rectangle:
        center: point
            x: 0
            y: 0
        size: point
            x: 10
            y: 10
        color: color
            r: 0
            g: 255
            b: 255
    on: screen
```

*Nylo is similar to English, isn't it?*

### Simple is better than complex

Nylo has few constructs - it's intrinsically simple!

```
struct ::= "("(value ":" value)*("->"value)?")"
value ::= valueel | valueel ? (symb valueel?)+
valueel ::= number | string | keyword | call
call ::= keyword struct
```

### Complex is better than complicated

Complicated means rule-exceptions. We have nothing like that.

### Flat is better than nested

Yes, that's rig-NO! Nylo is about data, data should always be nested!

### Sparse is better than dense

Nylo flawlessy supports modulation into multiple files

| File        | Code             |
| ----------- |:----------------:|
| double.py   | `int -> int * 2` |
| test.ny     | `-> double(30)`  |

And then..
```
>>> nylo test.ny
60
```

**Copyright** (c) 2017, 2018 [@veggero](https://github.com/veggero). All rights reserved.

**Copyright** (c) 2018 [pyTeens](https://teens.python.it). All rights reserved.

**Copyright** (c) 2018 [@AmerigoGuadagno](https://github.com/AmerigoGuadagno). All rights reserved.
