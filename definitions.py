import functools

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
    '=': 'equal',
    ': ': 'assign',
    '.': 'get_propriety',
    'is_a': 'is_instance',
}

symbols_priority = ['*', '/', '+', '-', '&', '=', ',',': ', '.']

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
    
    # OVERLOADED FUNCTIONS
    
    
    
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
    'print': create_instance('function', 
                            create_instance('python_code', 'definitions.nylo_print(items)'),
                           arguments = create_instance('arguments', [[['items']]])),
    
    'is_instance': create_instance('function', 
                                 create_instance('python_code', 'is_instance(instance, class["value"], child_variables)'),
                            arguments = create_instance('arguments', [[['instance']], [['class']]])),
    'assign': create_instance('function', 
                              create_instance('nylo_var_assignation', ''),
                              arguments = create_instance('arguments', [[['f_arguments']], [['value']]])),
}
