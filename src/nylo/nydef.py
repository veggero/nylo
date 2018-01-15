single_symbols = {':', '^', '*', '/', '+', '-', '%',  '=', '<', '>',  '&', ','}

symbols = ['..', '^', '*', '/', '+', '-', '%', '+-', '=', 
           '<', '>', '!=', '>=', '<=', '&', 'is_a', 'and', 
           'or', 'not', 'xor', '>>', '<<', 'with', 'as', 
           ':', 'in', ',', '->', '<-']

unary_symbols = {'+', '-', 'with', 'as'}

function_by_symbol = {
    '=': 'equal',
    'and': 'all',
    '>': 'greater_than',
    'or': 'any',
    '<': 'less_than',
    'not': 'sub',
    '!=': 'different',
    'xor': 'only',
    '>=': 'greater_or_equal',
    '>>': 'shift_right',
    '<=': 'less_or_equal',
    '<<': 'shift_left',
    '+': 'sum',
    '..': 'gradient',
    '-': 'sub',
    'in': 'contains',
    '*': 'mol',
    '+-': 'about',
    '/': 'div',
    ':': 'set',
    '^': 'pow',
    '->': 'pipe',
    '%': 'mod',
    ',': 'to_list',
    }
