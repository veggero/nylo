# This file is a part of nylo
#
# Copyright (c) 2018 The nylo Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections import defaultdict

from nylo.objects.interfaces.pyvalue import PyValue
from nylo.objects.struct.struct import Struct
from nylo.objects.struct.structel import TypeDef
from nylo.objects.values.keyword import Keyword
from nylo.objects.struct.call import Call
from nylo.objects.values.value import Value
import sys


def nylo_exit(code: int = 0, message: str = None) -> bool:
    """It defines an exit function for
    nylo.

    Args:
      code(int): The exit code
      message(str): The exit message
      code: int:  (Default value = 0)
      message: str:  (Default value = None)

    Returns:
      bool: True if all succeeded, False on fails
    """
    try:
        if message is not None:
            print(message)
        sys.exit(code)
        return True
    except BaseException:
        return False


def stack_keyword(stack: dict, keyword: str, default_value=None):
    """This function is used
    to get a keyword from a stack.

    Args:
      stack(Stack): The stack you're going to use
      keyword(str): The keyword you want to get
      default_value: The default value you get if the Keyword doesn't exist
      stack: dict:
      keyword: str:

    Returns:
      The got keyword from the stack, the default value on fails
    """
    try:
        return stack[Keyword(keyword)]
    except BaseException:
        return default_value


builtins: object = Struct(defaultdict(list, {
    'if': [Struct(defaultdict(list, {
        'cond': [],
        TypeDef(('obj', Keyword('first'))): [],
        TypeDef(('obj', Keyword('second'))): [],
        'self': [PyValue(
            lambda stack:
                stack[Keyword('first')].value
                if stack[Keyword('cond')].value
                else stack[Keyword('second')].value,
            lambda stack:
                stack[-1].typesof('first', stack) +
                stack[-1].typesof('second', stack),
        )]
    }))],

    'for': [Struct(defaultdict(list, {
        TypeDef(('list', 'obj', Keyword('tomap'))): [],
        TypeDef(('obj', Keyword('mapfun'))): [],
        'self': [PyValue(
            lambda stack: Struct(defaultdict(list, {
                'atoms': [Call(stack[-1][Keyword('mapfun')][-1], el).evaluate(stack)
                          for el in stack[Keyword('tomap')]['atoms']]})),
            lambda stack: {'obj', 'list'},)]
    }))],

    'filter': [Struct(defaultdict(list, {
        TypeDef(('list', 'obj', Keyword('tomap'))): [],
        TypeDef(('obj', Keyword('mapfun'))): [],
        'self': [PyValue(
            lambda stack: Struct(defaultdict(list, {
                'atoms': [el
                          for el in stack[Keyword('tomap')]['atoms']
                          if Call(
                              stack[-1][Keyword(
                                  'mapfun')][-1], el).evaluate(stack).value]})),
            lambda stack: {'obj', 'list'},)]
    }))],

    'repeat': [Struct(defaultdict(list, {
        TypeDef(('int', Keyword('times'))): [],
        TypeDef(('obj', Keyword('todo'))): [],
        'self': [PyValue(
            lambda stack: Struct(defaultdict(list, {
                'atoms': [stack[Keyword('todo')]
                          for _ in range(stack[Keyword('times')].value)]})),
            lambda stack: {'todo'},)]
    }))],

    'print': [Struct(defaultdict(list, {
        Keyword('toprint'): [],
        'self': [PyValue(
            lambda stack: print(stack[Keyword('toprint')]),
            lambda stack: {'obj', 'list'})]
    }))],

    'exit': [Struct(defaultdict(list, {
        TypeDef(('int', Keyword('code'))): [Value(0)],
        Keyword('message'): [],
        'self': [PyValue(
            lambda stack: nylo_exit(stack[Keyword('code')],
                                    stack_keyword(stack, 'message', None)),
            lambda stack: {'obj', 'list'})]
    }))],

}))

"""
The builtins struct defines all the builtins
methods and keywords
"""
