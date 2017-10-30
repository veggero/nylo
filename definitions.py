import functools
import executer

def create_instance(type, value, **kwargs):
    """
    Create a new instance of 'thing'.
    type -> type of instance
    value -> value of instance
    **kwargs -> addittional changes to thing
    """
    output = {'type': type, 'value': value}
    output.update(kwargs)
    return output

symbols = {
    '+': 'sum',
    '-': 'sub',
    '/': 'div',
    '*': 'mol',
    ',': 'make_list',
    '&': 'join',
    'and': 'and',
    'or': 'or',
    '=': 'equal',
    ': ': 'assign',
    '.': 'get_propriety',
    '>': 'greater_than',
    '<': 'less_than',
    'is_a': 'is_instance',
}

symbols_priority = ['*', '/', '+', '-', '&', '=', '>', '<', 'and', 'or', 'is_a', ',',': ', '.']

def nylo_sum(numbers):
    if numbers['type'] == 'list':
        list_nylo_numbers = numbers['value']
        list_numbers = [i['value'] for i in list_nylo_numbers]
        tot_sum = sum(list_numbers)
        return create_instance('int', tot_sum)
    else:
        return numbers

def nylo_sub(numbers):
    if numbers['type'] == 'list':
        list_nylo_numbers = numbers['value']
        list_numbers = [i['value'] for i in list_nylo_numbers]
        tot_sum = functools.reduce(lambda a, b: a-b, list_numbers)
        return create_instance('int', tot_sum)
    else:
        return numbers

def nylo_div(numbers):
    if numbers['type'] == 'list':
        list_nylo_numbers = numbers['value']
        list_numbers = [i['value'] for i in list_nylo_numbers]
        tot_sum = functools.reduce(lambda a, b: a/b, list_numbers)
        return create_instance('int', tot_sum)
    else:
        return numbers

def nylo_mol(numbers):
    if numbers['type'] == 'list':
        list_nylo_numbers = numbers['value']
        list_numbers = [i['value'] for i in list_nylo_numbers]
        tot_sum = functools.reduce(lambda a, b: a*b, list_numbers)
        return create_instance('int', tot_sum)
    else:
        return numbers

def nylo_list(items):
    # actually, work's already done here - assign put
    # all of them already in a list
    return items

def nylo_print(items):
    if items['type'] == 'list':
        list_nylo_numbers = items['value']
        list_values = [i['value'] for i in list_nylo_numbers]
        for value in list_values:
            print(list_values)
    else:
        print(items['value'])

def nylo_repr_int(to_repr):
    return create_instance('string', str(to_repr['value']))
    
def nylo_repr_str(to_repr):
    # already a string. 
    return to_repr
    
def nylo_repr_list(to_repr):
    str_elements = []
    for element in to_repr['value']:
        str_elements.append(executer.call(nylo['to_str'], element, nylo))
    output = '['+', '.join(str_elements)+']'
    return create_instance('string', str(output))
    
def nylo_repr_none(to_repr):
    return create_instance('string', 'none')
    
def nylo_repr_bool(to_repr):
    return create_instance('bool', str(to_repr['value']).lower())
    
def nylo_repr_general(to_repr):
    return create_instance('string', 'object with proprieties '+', '.join(list(to_repr)))
    
def nylo_and(booleans):
    return create_instance('bool', all([s_bool['value'] for s_bool in booleans['value']]))
    
def nylo_or(booleans):
    return create_instance('bool', all([s_bool['value'] for s_bool in booleans['value']]))

def nylo_greater_than(integers):
    integers = integers['value']
    for i in range(len(integers)-1):
        if integers[i]['value']<=integers[i+1]['value']:
            return create_instance('bool', False)
    return create_instance('bool', True)

def nylo_less_than(integers):
    integers = integers['value']
    for i in range(len(integers)-1):
        if integers[i]['value']>=integers[i+1]['value']:
            return create_instance('bool', False)
    return create_instance('bool', True)

def nylo_equal(integers):
    integers = integers['value']
    for i in range(len(integers)-1):
        if integers[i]['value']!=integers[i+1]['value']:
            return create_instance('bool', False)
    return create_instance('bool', True)
    
nylo = {
    # CLASSES
    
    'thing': create_instance('class', 
                            create_instance('arguments',
                                           [])),
    'int': create_instance('class', 
                            create_instance('arguments',
                                           [[['thing', 
                                        create_instance('condition',
                                            create_instance('python_code', 'definitions.create_instance("bool", type(thing)==type(5))')
                                        )
                                           ], ['value']]])),
    'list': create_instance('class', 
                            create_instance('arguments',
                                           [[['thing', 
                                        create_instance('condition',
                                            create_instance('python_code', 'definitions.create_instance("bool", type(thing)==type(list()))')
                                        )
                                           ], ['value']]])),
    'str': create_instance('class', 
                            create_instance('arguments',
                                           [[['thing', 
                                        create_instance('condition',
                                            create_instance('python_code', 'definitions.create_instance("bool", type(thing)==type(str()))')
                                        )
                                           ], ['value']]])),
    'none': create_instance('class', 
                            create_instance('arguments',
                                           [[['thing', 
                                        create_instance('condition',
                                            create_instance('python_code', 'definitions.create_instance("bool", type(thing)==type(None))')
                                        )
                                           ], ['value']]])),
    'bool': create_instance('class', 
                            create_instance('arguments',
                                           [[['thing', 
                                        create_instance('condition',
                                            create_instance('python_code', 'definitions.create_instance("bool", type(thing)==type(True))')
                                        )
                                           ], ['value']]])),
    
    # OVERLOADED FUNCTIONS
    
    'to_str': create_instance('overloaded_functions', [
        create_instance('function', 
            create_instance('python_code', 'definitions.nylo_repr_list(to_repr)'),
            arguments = create_instance('arguments', [[['list'], ['thing'], ['to_repr']]])
        ),
        create_instance('function', 
            create_instance('python_code', 'definitions.nylo_repr_int(to_repr)'),
            arguments = create_instance('arguments', [[['int'], ['to_repr']]])
        ),
        create_instance('function', 
            create_instance('python_code', 'definitions.nylo_repr_str(to_repr)'),
            arguments = create_instance('arguments', [[['str'], ['to_repr']]])
        ),
        create_instance('function', 
            create_instance('python_code', 'definitions.nylo_repr_none(to_repr)'),
            arguments = create_instance('arguments', [[['none'], ['to_repr']]])
        ),
        create_instance('function', 
            create_instance('python_code', 'definitions.nylo_repr_bool(to_repr)'),
            arguments = create_instance('arguments', [[['bool'], ['to_repr']]])
        ),
        create_instance('function', 
            create_instance('python_code', 'definitions.nylo_repr_general(to_repr)'),
            arguments = create_instance('arguments', [[['to_repr']]])
        ),
    ]),
    
    # FUNCTIONS
    
    'sum': create_instance('function', 
                          create_instance('python_code', 'definitions.nylo_sum(numbers)'),
                          arguments = create_instance('arguments', [[['numbers']]])),
    'mol': create_instance('function', 
                          create_instance('python_code', 'definitions.nylo_mol(numbers)'),
                          arguments = create_instance('arguments', [[['numbers']]])),
    'sub': create_instance('function', 
                          create_instance('python_code', 'definitions.nylo_sub(numbers)'),
                          arguments = create_instance('arguments', [[['numbers']]])),
    'div': create_instance('function', 
                          create_instance('python_code', 'definitions.nylo_div(numbers)'),
                          arguments = create_instance('arguments', [[['numbers']]])),
    'make_list': create_instance('function', 
                           create_instance('python_code', 'definitions.nylo_list(items)'),
                           arguments = create_instance('arguments', [[['items']]])),
                           
    'greater_than': create_instance('function', 
                          create_instance('python_code', 'definitions.nylo_greater_than(numbers)'),
                          arguments = create_instance('arguments', [[['numbers']]])),
    'less_than': create_instance('function', 
                          create_instance('python_code', 'definitions.nylo_less_than(numbers)'),
                          arguments = create_instance('arguments', [[['numbers']]])),
    'equal': create_instance('function', 
                          create_instance('python_code', 'definitions.nylo_equal(numbers)'),
                          arguments = create_instance('arguments', [[['numbers']]])),
    'and': create_instance('function', 
                          create_instance('python_code', 'definitions.nylo_and(numbers)'),
                          arguments = create_instance('arguments', [[['numbers']]])),
    'or': create_instance('function', 
                          create_instance('python_code', 'definitions.nylo_or(numbers)'),
                          arguments = create_instance('arguments', [[['numbers']]])),
    
    'print': create_instance('function', 
                            create_instance('python_code', 'definitions.nylo_print(items)'),
                           arguments = create_instance('arguments', [[['items']]])),
    
    'is_instance': create_instance('function', 
                                 create_instance('python_code', 'is_instance(instance, a_class["value"], child_variables)'),
                            arguments = create_instance('arguments', [[['instance']], [['a_class']]])),
    'assign': create_instance('function', 
                              create_instance('nylo_var_assignation', ''),
                              arguments = create_instance('arguments', [[['f_arguments']], [['value']]])),
}
