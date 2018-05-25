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
    Keyword('if'): [Struct(defaultdict(list, {
        '_args': ['cond', 'first', 'second'],
        'cond': ['_arg'], 'first': ['_arg'], 'second': ['_arg'],
        'self': [PyValue(
            lambda stack:
                stack[Keyword('first')].value
                if stack[Keyword('cond')].value
                else stack[Keyword('second')].value,
            lambda stack:
                stack[-1].typesof('first', stack) +
                stack[-1].typesof('second', stack)
        )]
    }))],

    Keyword('for'): [Struct(defaultdict(list, {
        '_args': ['tomap', 'mapfun'],
        'tomap': ['_arg'], 'mapfun': ['_arg'],
        'self': [PyValue(
            lambda stack: Struct(defaultdict(list, {
                'atoms': [Call(stack[-1].value[Keyword('mapfun')][-1], el).evaluate(stack)
                          for el in stack[Keyword('tomap')].value['atoms']]})),
            lambda stack: {'obj', 'list'})]
    }))],

    Keyword('filter'): [Struct(defaultdict(list, {
        '_args': ['tomap', 'mapfun'],
        'tomap': ['_arg'], 'mapfun': ['_arg'],
        'self': [PyValue(
            lambda stack: Struct(defaultdict(list, {
                'atoms': [el
                          for el in stack[Keyword('tomap')].value['atoms']
                          if Call(
                              stack[-1].value[Keyword(
                                  'mapfun')][-1], el).evaluate(stack).value]})),
            lambda stack: {'obj', 'list'})]
    }))],

    Keyword('repeat'): [Struct(defaultdict(list, {
        '_args': ['times', 'todo'],
        'times': ['_arg'], 'todo': ['_arg'],
        'self': [PyValue(
            lambda stack: Struct(defaultdict(list, {
                'atoms': [stack[Keyword('todo')]
                          for _ in range(stack[Keyword('times')].value)]})),
            lambda stack: {'todo'})]
    }))],

    Keyword('print'): [Struct(defaultdict(list, {
        '_args': ['toprint'],
        'toprint': ['_arg'],
        'self': [PyValue(
            lambda stack: print(stack[Keyword('toprint')]),
            lambda stack: {'obj', 'list'})]
    }))],

    Keyword('exit'): [Struct(defaultdict(list, {
        TypeDef(('int', Keyword('code'))): [Value(0)],
        '_args': [Keyword('message')],
        'message': ['_arg'],
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
