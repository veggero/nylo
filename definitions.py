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

def nylo_sum(a, b):
    return create_istance('int', a['value']+b['value'])

nylo = {
    'sum': create_istance('function', 
                          create_istance('python_code', 'definitions.nylo_sum(a, b)'),
                          arguments = create_istance('arguments', [[['a']], [['b']]]))
}
