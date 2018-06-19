import operator

bc_pow = {
    ('if', 'self'):                     ["IF", ('if', 'cond'), ('if', 'then'), ('if', 'else')],
    ('pow', 'self'):                    ('pow', 'self', 'self'),
    ('pow', 'self', 'cond'):            [operator.eq, ('pow', 'n'), 1],
    ('pow', 'self', 'then'):            1,
    ('pow', 'self', 'else'):            [operator.mul, ('pow', 'n'), ('pow', 'self', 'else', 'self')],
    ('pow', 'self', 'class'):           ('if',),
    ('pow', 'self', 'else', 'n'):       [operator.sub, ('pow', 'n'), 1],
    ('pow', 'self', 'else', 'class'):   ('pow',),
    ('self',):                          ('self', 'self'),
    ('self', 'n'):                      140,
    ('self', 'class'):                  ('pow',)
}

bc_fib = {
    ('if', 'self'):                     ["IF", ('if', 'cond'), ('if', 'then'), ('if', 'else')],
    ('fib', 'self'):                    ('fib', 'self', 'self'),
    ('fib', 'self', 'cond'):            [operator.lt, ('fib', 'n'), 2],
    ('fib', 'self', 'then'):            ('fib', 'n'),
    ('fib', 'self', 'else'):            [operator.add, ('fib', 'self', 'else', '1', 'self'), ('fib', 'self', 'else', '2', 'self')],
    ('fib', 'self', 'class'):           ('if',),
    ('fib', 'self', 'else', '1', 'n'):  [operator.sub, ('fib', 'n'), 1],
    ('fib', 'self', 'else', '1', 'class'): ('fib',),
    ('fib', 'self', 'else', '2', 'n'):  [operator.sub, ('fib', 'n'), 2],
    ('fib', 'self', 'else', '2', 'class'): ('fib',),
    ('self',):                          ('self', 'self'),
    ('self', 'n'):                      16,
    ('self', 'class'):                  ('fib',)
}

def evaluate(obj, mesh):
    if isinstance(obj, list):
        op, *args = obj
        if isinstance(op, str):
            if op == 'IF':
                args[0] = evaluate(args[0], mesh)
                if args[0]: return evaluate(args[1], mesh)
                else: return evaluate(args[2], mesh)
        args = [evaluate(el, mesh) for el in args]
        return op(*args)
    elif isinstance(obj, tuple):
        tmp = resolve(obj, mesh)
        out = evaluate(tmp, mesh)
        mesh[obj] = out
        return out
    return obj

def resolve(path, mesh):
    if path in mesh:
        return mesh[path] #*orgasm here*
    # shit.
    for i in range(len(path)):
        classpath = path[:i]+('class',)
        if classpath in mesh:
            replaced = mesh[classpath]+path[i:]
            try:
                replaced_out = resolve(replaced, mesh)
            except NameError:
                continue
            out = replace_back(path, i, replaced_out, mesh[classpath])
            mesh[path] = out
            return out
    raise NameError(path)
    
def replace_back(path, i, obj, beginning):
    if isinstance(obj, tuple) and obj[:len(beginning)]==beginning:
        return path[:i]+obj[len(beginning):]
    elif isinstance(obj, list):
        return [obj[0]]+[replace_back(path, i, el, beginning) for el in obj[1:]]
    else:
        return obj
    
print(evaluate(('self',), bc_fib))
