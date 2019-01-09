Welcome to nylo
========================

WARNING: README IS INCREDIBLY OUTDATED. I'm working on this, but I still need to figure out a lot of things, even the grammar itself. As soon as I have a clear and sure idea of how Nylo is going to be, I will rewrite everything.

[If you're thinking "is he still working on this?": yes, I am.]

|image0|

::

   -> "Tau World! :D"

**Nylo** is a declarative programming language. It takes some constructs
from functional and logic paradigms, but it’s really a new paradigm
itself. It aims to be simple and clear, but powerful. It provides an
easy way to make assertions on the data a function is working on. It
also gives you the possibility to define standard behaviour if asserts
fail.

::

   fib: (
       n: int
       sum_prev_fibs: fib(n-1) + fib(n-2)
       result: if(n<2 n sum_prev_fibs)
       -> result
   )

Contents
========

-  `How to contribute`_
-  `Present and future of project`_
-  `Features`_

   1. `It’s simple and orthogonal`_
   2. `It’s explicit and clear`_
   3. `Curried function and classes`_
   4. `Inverse function and classes`_

How to contribute
-----------------

Just ask @veggero :)

Present and future of project
-----------------------------

This repo contains the development version of the proof-of-concept of
the programming language. The poc should be finished on the 25th of May,
but due to complications in the type and overloading systems, it might
slip further.

As soon as the proof-of-concept is finished and refined, the work on the
actual interpreter will start. It will be written in Go/Rust/Ida.

Features
--------

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

It’s explicit and clear
~~~~~~~~~~~~~~~~~~~~~~~

Nylo makes everything explicit, even function calls!

::

   draw: (
       on: screen
       color: color(r: 0 g: 255 b: 255)
       rectangle: rectangle(
           center: point(x: 5 y: 15)
           size: point(x: 10 y: 10)
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

.. _How to contribute: #how-to-contribute
.. _Present and future of project: present-and-future-of-project
.. _Features: #features
.. _It’s simple and orthogonal: #its-simple-and-orthogonal
.. _It’s explicit and clear: #its-explicit-and-clear
.. _Curried function and classes: #curried-function-and-classes
.. _Inverse function and classes: #inverse-function-and-classes

.. |image0| image:: https://raw.githubusercontent.com/pyTeens/nylo/gh-pages/docs/images/new_big_nylo_banner.png
