![](https://raw.githubusercontent.com/pyTeens/nylo/gh-pages/docs/images/NyloPyTeensLogo.png) [![](https://travis-ci.org/pyTeens/nylo.svg?branch=master)](https://travis-ci.org/pyTeens/nylo)

# Welcome to nylo

**nylo** (/nylo/) is a **programming language** written in [Python](https://python.org). It is knows due to its **simplicity** and **style**. As you should know: **nylo** is absolutely **user-friendly**, you could write code in few lines, less than what you would think!

# Contents
* [Files](#files)
* [How to contribute](#how-to-contribute)
* [Release](#release)

## Files

You'll find lots of _not understandable_ **directory** and **files**, so here a list and definitions of them:

* **src/main.py** - _First Nylo Command Line code, used for debugging_
* **src/nylo** - _Main directory_
* **src/nylo/__init__.py** - _Where the code is imported_
* **src/nylo/builtins.py** - _Definitions of some Nylo "built inside" function_ (like **print**, etc..)
* **src/nylo/exceptions.py** - _Definitions of Nylo exceptions_ (like **NameNotDefined**, **NeedComma**, **FileNotOver**, etc..)
* **src/nylo/base_objects** - _It includes some useful Token & Stack definitions and a "Reading" class where they are used _
* **src/nylo/base_objects/Reading.py** - _It checks the number of lines, characters, unexpected EOFs, etc.._
* **src/nylo/base_objects/Stack.py** - _It contains a list of variable dictionaries_
* **src/nylo/base_objects/Token.py** - _It manages the initialization of parsed tokens and their representations_
* **src/nylo/derived_objects** - _Some useful (or maybe useless) derived object for syntax & Python linking_
* **src/nylo/derived_objects/python_linked_objects.py** - _Definitions of some Python linking class_ (such as **PyStruct**)
* **src/nylo/derived_objects/syntax_unrelated_objects.py** - _Derived objects of Token class_
* **src/nylo/struct_objects** - _It contains some Struct management & creator classes_
* **src/nylo/struct_objects/Struct.py** - _Definition of the Struct class, derived of Token class, that evaluates  and parse expressions_
* **src/nylo/struct_objects/StructEl.py** - _Another class, derived of Token class, that evaluates and parse expressions_
* **src/nylo/struct_objects/Caller.py** - _Definition of a Object Caller class_
* **src/nylo/struct_objects/CallerEl.py** - _Another Object Caller class_
* **src/nylo/syntax_objects** - _As the name says, it contains the Syntax classes_
* **src/nylo/syntax_objects/Keyword.py** - _Definition of a Keyword class, derived of Token class, that evaluates and parse expressions_
* **src/nylo/syntax_objects/Symbol.py** - _Definition of all Symbols into a Symbol class, derived of Token class_
* **src/nylo/syntax_objects/SymbolOperation.py** - _Definition of a SymbolOperation class that gives the semantic result of operator expressions_
* **src/nylo/value_objects** - _It contains some Types and Values definitions_
* **src/nylo/value_objects/NumStr.py** - _Definition of the String type as a String class, derived of Token class. Same for Numbers._
* **src/nylo/value_objects/Value.py** - _Definition of a Value class, derived of Token class, that evaluates and parse expressions_
* **src/meta/examples.ny** - _A Nylo code example_
* **src/meta/ny_specs.txt** - _Symbols definitions and specifications_
* **src/meta/ny_style** - _Some examples of Nylo style, in Italian_

## How to contribute

_In primis_ ("firstable"), you **must** be a member of [pyTeens](https://teens.python.it), then **ask** [@veggero](https://github.com/veggero)!

## Release

It will be released on the _25th_ of _May 2018!_

**Copyright** (c) 2017, 2018 [@veggero](https://github.com/veggero). All rights reserved.
**Copyright** (c) 2018 [pyTeens](https://teens.python.it). All rights reserved.
