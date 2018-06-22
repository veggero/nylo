import operator
import time
from collections import deque

bc_pow = {
    'classes': {
        ('self',):                ('pow',),
        ('pow', 'self'):          ('if',),
        ('pow', 'self', 'else'):  ('pow',),
        },
    ('if', 'self'):                     [('if', 'then'), ('if', 'else'), "IF", ('if', 'cond')],
    ('pow', 'self'):                    ('pow', 'self', 'self'),
    ('pow', 'self', 'cond'):            [operator.eq, ('pow', 'n'), 1],
    ('pow', 'self', 'then'):            1,
    ('pow', 'self', 'else'):            [operator.mul, ('pow', 'n'), ('pow', 'self', 'else', 'self')],
    ('pow', 'self', 'else', 'n'):       [operator.sub, ('pow', 'n'), 1],
    ('self',):                          ('self', 'self'),
    ('self', 'n'):                      16,
}

bc_fib = {
    'classes': {
        ('self',):                      ('fib',),
        ('fib', 'self'):                ('if',),
        ('fib', 'self', 'else', '1'):   ('fib',),
        ('fib', 'self', 'else', '2'):   ('fib',),
        },
    ('if', 'self'):                     [('if', 'then'), ('if', 'else'), "IF", ('if', 'cond')],
    ('fib', 'self'):                    ('fib', 'self', 'self'),
    ('fib', 'self', 'cond'):            [operator.lt, ('fib', 'n'), 2],
    ('fib', 'self', 'then'):            ('fib', 'n'),
    ('fib', 'self', 'else'):            [operator.add, ('fib', 'self', 'else', '1', 'self'), ('fib', 'self', 'else', '2', 'self')],
    ('fib', 'self', 'else', '1', 'n'):  [operator.sub, ('fib', 'n'), 1],
    ('fib', 'self', 'else', '2', 'n'):  [operator.sub, ('fib', 'n'), 2],
    ('self',):                          ('self', 'self'),
    ('self', 'n'):                      20,
}

bc_rec = {
    ('a', 'self'):          ('a', 'self', 'self'),
    ('a', 'self', 'n'):     [operator.add, ('a', 'n'), 1],
    ('a', 'self', 'class'): ('a',),
    ('self',):              ('self', 'self'),
    ('self', 'n'):          0,
    ('self', 'class'):      ('a',)
    }

def execute(mesh):
    targets = [('self',)]
    arguments = []
    tick = 0
    while targets:
        tick += 1
        last = targets.pop()
        if isinstance(last, tuple):
            #print("LOAD", last)
            tickstart = time.time()
            obj = resolve(last, mesh)
            if isinstance(obj, tuple):
                targets.append(obj)
            elif isinstance(obj, list):
                targets.append(last)
                targets.extend(obj)
            else:
                targets.append(obj)
        elif isinstance(last, type(operator.add)):
            #print("EXECUTE", last, arguments[-2:])
            tickstart = time.time()
            arguments.append(last(*(arguments.pop(), arguments.pop())))
            mesh[targets.pop()] = arguments[-1]
        elif isinstance(last, str) and last == 'IF':
            #print("IF")
            tickstart = time.time()
            if arguments.pop():
                targets.pop()
            else:
                targets.pop(-2)
            targets.pop(-2)
        else:
            #print("APPEND", last)
            tickstart = time.time()
            arguments.append(last)
        #print(round((time.time()-tickstart)*100000, 4))
    print(f"Code executed in {tick} ticks.")
    return arguments.pop()

def resolve(path, mesh):
    replaces = []
    while path not in mesh:
        for classpath in sorted(mesh['classes'], key=len, reverse=True):
            subpath = path[:len(classpath)]
            if classpath == subpath:
                fclass = mesh['classes'][classpath]
                replaces.append((subpath, fclass))
                path = fclass+path[len(subpath):]
                break
        else:
            raise NameError(path)
    out = mesh[path]
    for replace in reversed(replaces):
        mesh[path] = out
        out = replace_back(out, *replace)
        path = replace_back(path, *replace)
    return out

def replace_back(obj, subpath, fclass):
    if isinstance(obj, tuple) and obj[:len(fclass)]==fclass:
        return subpath+obj[len(fclass):]
    elif isinstance(obj, list):
        return [replace_back(el, subpath, fclass) for el in obj]
    else:
        return obj
