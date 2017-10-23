import functools

def create_istance(type, value, **kwargs):
    """
    Create a new istance of 'thing'.
    type -> type of istance
    value -> value of istance
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
    ',': 'list',
    '&': 'join',
    '=': 'equal',
    ': ': 'assign',
    '.': 'join'
}

symbols_priority = ['*', '/', '+', '-', '&', '=', ',',': ', '.']

def nylo_sum(numbers):
    if numbers['type'] == 'list':
        list_nylo_numbers = numbers['value']
        list_numbers = [i['value'] for i in list_nylo_numbers]
        tot_sum = sum(list_numbers)
        return create_istance('int', tot_sum)
    else:
        return numbers

def nylo_sub(numbers):
    if numbers['type'] == 'list':
        list_nylo_numbers = numbers['value']
        list_numbers = [i['value'] for i in list_nylo_numbers]
        tot_sum = functools.reduce(lambda a, b: a-b, list_numbers)
        return create_istance('int', tot_sum)
    else:
        return numbers

def nylo_div(numbers):
    if numbers['type'] == 'list':
        list_nylo_numbers = numbers['value']
        list_numbers = [i['value'] for i in list_nylo_numbers]
        tot_sum = functools.reduce(lambda a, b: a/b, list_numbers)
        return create_istance('int', tot_sum)
    else:
        return numbers

def nylo_mol(numbers):
    if numbers['type'] == 'list':
        list_nylo_numbers = numbers['value']
        list_numbers = [i['value'] for i in list_nylo_numbers]
        tot_sum = functools.reduce(lambda a, b: a*b, list_numbers)
        return create_istance('int', tot_sum)
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
    'sum': create_istance('function', 
                          create_istance('python_code', 'definitions.nylo_sum(numbers)'),
                          arguments = create_istance('arguments', [[['numbers']]])),
    'mol': create_istance('function', 
                          create_istance('python_code', 'definitions.nylo_mol(numbers)'),
                          arguments = create_istance('arguments', [[['numbers']]])),
    'sub': create_istance('function', 
                          create_istance('python_code', 'definitions.nylo_sub(numbers)'),
                          arguments = create_istance('arguments', [[['numbers']]])),
    'div': create_istance('function', 
                          create_istance('python_code', 'definitions.nylo_div(numbers)'),
                          arguments = create_istance('arguments', [[['numbers']]])),
    'list': create_istance('function', 
                           create_istance('python_code', 'definitions.nylo_list(items)'),
                           arguments = create_istance('arguments', [[['items']]])),
    'print': create_istance('function', 
                            create_istance('python_code', 'definitions.nylo_print(items)'),
                           arguments = create_istance('arguments', [[['items']]])),
}
