from .derived_objects.python_linked_objects import PyStruct
from .base_objects.Stack import Stack

builtins = Stack([{
    'print': PyStruct([['int', 'to_print']], lambda stack: print(stack[-1]['to_print'])),

    'if': PyStruct([['code', 'cond'],
                    ['code', 'todo'],
                    ['code', 'else']], 
        lambda stack: (stack[-1]['todo'].evaluate(stack) 
                        if stack[-1]['cond'].evaluate(stack)
                        else (stack[-1]['else'].evaluate(stack)
                              if 'else' in stack[-1]
                              else None
                              )))
    }])
