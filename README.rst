|image0|

**Nylo** is a declarative programming language. It takes some constructs
from functional and logic paradigms, but it’s really a new paradigm
itself. It aims to be simple and clear, but powerful. It provides an
easy way to make assertions on the data a function is working on. It
also gives you the possibility to define standard behaviour if asserts
fail.

::

   fib: (
       n: int
       prevs: fib(n: n-1) + fib(n: n-2)
       result: if(cond: n<2, then: n, else: sum_prev_fibs)
       -> result
   )

Contents
========

-  `Present and future of project`_
-  `Markup / Configuration file`_

   1. `Structures`_
   2. `Lists`_
   3. `Multiple words`_
   4. `Other kind of variables`_

-  `Programming Language`_

   1. `It’s simple and orthogonal`_
   2. `It’s explicit and clear`_
   3. `Curried function and classes`_
   4. `Inverse function and classes`_

Present and future of project
-----------------------------

This repo contains the development version of the proof-of-concept of
the programming language. The poc should be finished on the 25th of May,
but due to complications in the type and overloading systems, it might
slip further.

As soon as the proof-of-concept is finished and refined, the work on the
actual interpreter will start. It will be written in Go/Rust/Ida.

Markup / Configuration file
---------------------------

Nylo aims to be clear enough to be used to markup or configuration
files. An example can be found on https://niccolo.venerandi.com .

Structures
~~~~~~~~~~

::

   grades: (
       first_semester: (
           math: 7
           science: 9
           language: 6
       )
       second_semester: (
           math: 8
           science: 8
           language: 7
       )
   )

Lists
~~~~~

::

   numbers: (
       high: (
           4201337,
           3290941,
           4129301
       )
       low: (1, 2, 3)
   )
   
Multiple words
~~~~~~~~~~~~~~

::

   first level: (
       enemy life: 100
       enemy power: 50
   )
   second level: (
       enemy life: 150
       enemy power: 80
   )
   
Other kind of variables
~~~~~~~~~~~~~~~~~~~~~~~

Any variable can be used by putting ` before and after the name.

::

   symbols: (
       `+`: "plus"
       `-`: "minus"
   )
   years: (
       `2017`: "kinda cool"
       `2018`: "please let's go back"
   )
   other weird names: (
       `(!WOW!)`: "WOW!"
       `--> :0 <--`: "WOW!"
   )

Programming Language
--------------------

It’s simple and orthogonal
~~~~~~~~~~~~~~~~~~~~~~~~~~

Nylo has very few constructs. In fact, everything is a structure, which is put 
in the form of (a: b, c: d -> e)

::
       
   // Class
   point: (
       x: int
       y: int
   )
       
   // Function
   double: (
       n: int
       r: n * 2
       -> r
   )
   
   // Call
   twenty: double (
       n: 10
       -> r
   )
   
   // Namespace
   smallnumbers: (
       zero: 0
       one: 1
       two: 2
   )
   
   // Enum
   traffic_lights: (
        green: ()
        yellow: ()
        red: ()
   )

   // List
   languages: (
       "Python"
       "Go"
       "C"
   )

It’s explicit and clear
~~~~~~~~~~~~~~~~~~~~~~~

Nylo makes everything explicit, even function calls!

::

   screen.drawings: (
       rectangle(
           position: point(x: 5, y: 15)
           size: point(x: 10, y: 10)
       )
   )

The same thing with pygame is:

::

   pygame.draw.rect(
       screen,
       (255, 0, 0),
       (5, 15, 10, 10)
   )

As you can see, Nylo easier to understand. 

Curried function and classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not all arguments has to be passed in the first call. You can use -> to curry.

::

   add: (
       a: int
       b: int
       -> a + b
   )

   add(a: 1, b: 2) = 3
   
   add_three: add(a: 3 ->)
   add_three(b: 5) = 8

Also, not all class proprieties has to be passed in the first call.

::

   point: (
       x: int
       y: int
   )

   A: point(x: 5, y: 10)

   x_axis: point(y: 0 ->)
   y_axis: point(x: 0 ->)

   B: x_axis(x: 5)
   C: y_axis(y: 10)

Inverse function and classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can make function that also works backward:

::

   double: (
       n: result / 2
       result: n * 2
       -> result
   )

   double(n: 10) = 20
   double(n: 10 -> result) = 20
   double(result: 20 -> n) = 10

And you can also have multiple ways to define classes:

::

   color: (
       r: hex[1:3].base_10
       g: hex[3:5].base_10
       b: hex[5:7].base_10

       hex: '#' & r.base_16 & g.base_16 & b.base_16
   )
       
   color(r: 255 g: 0 b: 0)
   color(hex: "#ff0000")

   color(r: 0 g: 122 b: 54 -> hex)
   color(hex: "#c8ec8e" -> r)

No one own this, you can do whatever you want with this code, and you should not care about who made it. Have fun!

.. |image0| image:: https://raw.githubusercontent.com/veggero/nylo/master/meta/nylo_logo_banner.png
