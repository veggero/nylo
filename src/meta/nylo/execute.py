import nyparser
import exceptions
import nylo_object as no
import instance_creator as new
import manage_base_structs as mbs
import time
import copy

"""
FUNCTION TO CALL OBJECTS
"""


def run(code):
    global calls
    calls = 0
    parsed_code = nyparser.parse(code)
    call_multiline_code(parsed_code)
    print("CODE EXECUTED WITH {n} CALLS".format(n=calls))


def call_multiline_code(multiline_code):
    multiline_code = multiline_code[new.variable('codelines')]
    out = no.NyloObject()
    for line_number, codeline in multiline_code:
        new_out = call(codeline)
        if new_out != no.NyloObject():
            out = new_out
    return out


def call(code):
    code = code[new.variable('behaviour')]
    new_code = no.NyloObject()
    for index, obj in code:
        new_code[index] = call_overloaded(evaluate, obj)
    return call_overloaded(nycall, new_code)


def call_structure(struct, args):
    struct = struct[new.variable('struct')]
    if len(struct) != len(args):
        raise exceptions.NyloValueError
    obj = no.NyloObject()
    for ((index, param),
         (index, value)) in zip(struct, args):
        if new.string('class') in param and param[new.string('class')]:
            if not mbs.is_instance(value, param[new.string('class')]):
                raise exceptions.NyloValueError
        obj[param] = value
    return obj


def arrange(args, struct):
    struct = struct[new.variable('struct')]

    # {x|} "hi" --> {x|}(list "hi")
    args = new.nylist([args])

    # {x|}(list((1, 2, 3))) --> {x|}(1,2,3)
    while mbs.is_instance(args[new.integer(0)], mbs.nylist):
        args = args[new.integer(0)]

    if len(struct) == 1 and len(args) > 1:
        args = new.nylist([args])

    return args


def call_overloaded(overloadeds, args):
    global context
    global calls
    calls += 1
    overloadeds = overloadeds[new.variable("overloaded_functions")]
    for index, function in overloadeds.data[::-1]:
        try:
            args = arrange(args, function[new.variable('arguments')])
            local_variables = call_structure(
                function[new.variable('arguments')], args)
        except exceptions.NyloValueError:
            continue
        context.append(local_variables)
        if mbs.is_instance(function, mbs.function):
            out = call_multiline_code(function[new.variable('function_code')])
        else:
            python_args = [obj for index, obj in args]
            out = function['python_function'](*python_args)
        context.pop()
        return out
    raise exceptions.NyloValueError


def call_function(funct, args):
    # if mbs.is_instance(funct, mbs.function): funct = copy.deepcopy(funct)
    return call_overloaded(
        new.overload([funct]),
        args
    )

nycall = new.overload([
    new.pyfunction(
        lambda x: x,
        new.struct([new.variable('to_ignore')])
    ),
    new.pyfunction(
        lambda a, b: call_function(nylo_related_function[new.variable('if')],
                                   new.nylist([a, b])),
        new.struct([new.variable('if_condition', mbs.boolean),
                    new.variable('if_code', mbs.codelines)])
    ),
    new.pyfunction(
        lambda a, b, c, d: call_function(a, new.nylist([b, c, d])),
        new.struct([new.variable('def_fun'),
                    new.variable('funct_name', mbs.variable),
                    new.variable('params', mbs.struct),
                    new.variable('funct_code', mbs.codelines)])
    ),
    new.pyfunction(
        lambda a, b, c: call_function(a, new.nylist([b, c])),
        new.struct([new.variable('if_fun'),
                    new.variable('condition', mbs.boolean),
                    new.variable('if_code', mbs.codelines)])
    ),
    new.pyfunction(
        lambda x, y: call_overloaded(x, y),
        new.struct([new.variable('to_call', mbs.overload),
                    new.variable('to_args')])
    ),
    new.pyfunction(
        lambda x, y: call_function(x, y),
        new.struct([new.variable('to_call', mbs.function),
                    new.variable('to_args')])
    ),
    new.pyfunction(
        lambda x, y: call_function(x, y),
        new.struct([new.variable('to_call', mbs.pyfunction),
                    new.variable('to_args')])
    ),
])

"""
FUNCTIONS TO EVALUATE
"""


def evaluate_variable(var):
    try:
        var = var + fetch_variable(var)
    except exceptions.NyloNameError:
        pass
    if var[new.string("class")]:
        var[new.string("class")] = fetch_variable(
            var[new.string("class")])  # TODO
    return var


def fetch_variable(var):
    global context
    for vardict in context[::-1]:
        if var in vardict:
            return vardict[var]
    raise exceptions.NyloNameError(var)

evaluate = new.overload([
    new.pyfunction(
        lambda x: x,
        new.struct([new.variable('to_ignore')])
    ),
    new.pyfunction(
        lambda x: call(x),
        new.struct([new.variable('to_evaluate',
                                 mbs.code)])
    ),
    new.pyfunction(
        lambda x: evaluate_variable(x),
        new.struct([new.variable('to_evaluate',
                                 mbs.variable)])
    ),
])

"""
NYLO RELATED FUNCTIONS
"""


def pyassign(struct, values):
    global context
    context[-3].add(call_structure(struct, arrange(values, struct)))


def define(v_name, params, cdlines):
    global context
    nf = new.function(cdlines, params)
    context[-3].add(no.NyloObject([v_name, nf]))


def pyif(condition, codelines):
    global context
    context[-3].add(no.NyloObject([new.variable('else'),
                                   new.boolean(not condition['python_boolean'])]))
    context.append(no.NyloObject())
    out = no.NyloObject()
    if condition['python_boolean']:
        out = call_multiline_code(codelines)
    del context[-1]
    return out

nylo_related_function = no.NyloObject(
    [new.variable(
        'assign'), new.pyfunction(pyassign, new.struct([new.variable('to_assign_struct'),
                                                        new.variable(
                                                        'value_to_check')]))],
    [new.variable(
        'def'), new.pyfunction(define, new.struct([new.variable('variable_name_to_def'),
                                                   new.variable(
                                                   'params'),
                                                   new.variable(
                                                   'def_codelines')]))],
    [new.variable(
        'if'), new.pyfunction(pyif, new.struct([new.variable('if_condition'),
                                                new.variable('if_codelines')]))]
)

"""
GENERAL PURPOSE FUNCTIONS
"""


def pysum(nums):
    return new.integer(sum(k['python_integer'] for index, k in nums))


def pysub(a, b):
    return new.integer(a['python_integer'] - b['python_integer'])


def pymol(a, b):
    return new.integer(a['python_integer'] * b['python_integer'])


def pyeq(a, b):
    a = a - new.variable('this')
    b = b - new.variable('this')
    return new.boolean(a == b)


def pyany(to_any):
    return new.boolean(any(a['python_boolean'] for index, a in to_any))

builtins_functions = no.NyloObject(
    [new.variable('print'), new.pyfunction(
        print, new.struct([new.variable('to_print')]))],
    [new.variable('sum'), new.pyfunction(pysum,
                                         new.struct(
                                             [new.variable(
                                                 'integers_to_sum')]))],
    [new.variable('sub'), new.pyfunction(pysub,
                                         new.struct(
                                             [new.variable('integers_to_sub'),
                                              new.variable(
                                              'other_integer')]))],
    [new.variable('mol'), new.pyfunction(pymol,
                                         new.struct(
                                             [new.variable('integers_to_mol'),
                                              new.variable(
                                              'other_integer')]))],
    [new.variable('equal'), new.pyfunction(pyeq,
                                           new.struct([new.variable('a'),
                                                       new.variable('b')]))],
    [new.variable('any'), new.pyfunction(pyany,
                                         new.struct(
                                             [new.variable('to_any')]))],
)

"""
BUILTIN GLOBAL VARIABLES
"""

builtins_execute = no.NyloObject(
    [new.variable("evaluate_on_runtime"), evaluate],
    [new.variable("true"), new.boolean(True)],
    [new.variable("false"), new.boolean(False)]
)

context = [builtins_execute +
           mbs.builtins_struct +
           builtins_functions +
           nylo_related_function]

run('''
def k {n}:
    if ((n = 0) or (n = 1)):
        n
    else:
        k(n - 1) + k(n - 2)

print(k 16)
''')
