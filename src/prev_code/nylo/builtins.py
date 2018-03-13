from .derived_objects.python_linked_objects import PyStruct
from .base_objects.Stack import Stack

builtins = Stack([{
    'print': PyStruct([['int', 'to_print']],
                      lambda stack: print(stack.get_variable('to_print'))),

    'if': PyStruct([['code', 'cond'],
                    ['code', 'todo'],
                    ['code', 'else']],
                   lambda stack: (stack.get_variable('todo')
                                  if stack.get_variable('cond')
                                  else (stack.get_variable('else')
                                        if 'else' in stack[-1]
                                  else None
                                        )))
}])
