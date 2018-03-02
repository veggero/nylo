import instance_creator as new
import nylo_object as no

codelines = new.struct([new.variable('codelines')])

string = new.struct(['python_string'])

integer = new.struct(['python_integer'])

floating = new.struct(['python_floating_point'])

code = new.struct([new.variable('behaviour')])

path = new.struct([new.variable('path')])

struct = new.struct([new.variable('struct')])

function = new.struct([new.variable('function_code'),
                       new.variable('arguments')])

pyfunction = new.struct(['python_function',
                       new.variable('arguments')])

variable = new.struct([new.string('variable_name'),
                       new.string('class'),
                       new.string('condition'),
                       new.string('default')])

boolean = new.struct(['python_boolean'])

overload = new.struct([new.variable('overloaded_functions')])

nylist = new.struct([new.integer(0)])

evaluable_obj = new.struct(['to_evaluate'])


def is_instance(obj, struct):
    struct = struct[new.variable('struct')]
    for index, value in struct:
        if not value in obj: return False
    return True

builtins_struct = no.NyloObject(
    [new.variable('codelines'), codelines],
    [new.variable('str'), string],
    [new.variable('int'), integer],
    [new.variable('float'), floating],
    [new.variable('code'), code],
    [new.variable('pathgetter'), path],
    [new.variable('struct'), struct],
    [new.variable('function'), function],
    [new.variable('python_function'), pyfunction],
    [new.variable('var'), variable],
    [new.variable('overload'), overload],
    [new.variable('list'), nylist],
    [new.variable('to_eval_on_runtime'), evaluable_obj]
    )
