import definitions
import parser

def execute(raw_code):
    code = parser.parse(raw_code)
    return run(code, definitions.nylo)
        
    # if only one value is left, return it
    if len(values) == 1:
        return values[0]
        
    else:
        # nothing to return actually. No 'return' function was
        # called and we can't return all the values of every function
        return definitions.create_istance('none', None)

def run(code, variables):
    """
    Call all the functions in a code object
    """
    last = definitions.create_istance('none', None)
    values = []
    
    # iter all of parsed in code
    for parsed in code['value']:
            
        # if it's a variable replace it with his value
        if parsed['type'] == 'variable':
            parsed = get_var_value(parsed, variables)
    
        # if this is a code, and obj before was a function,
        # let's hella call that function
        if parsed['type'] == 'code' and last['type'] == 'function':
            # delete from the values the function, and replace it with its output
            del values[-1]
            values.append(call(last, run(parsed, variables), variables))
            
        # run round brackets
        elif parsed['type'] == 'code':
            values.append(run(parsed, variables))
            
        # also, run every element in a list, because they're all codes
        elif parsed['type'] == 'list':
            output = []
            for element in parsed['value']:
                output.append(run(element, variables))
            values.append(definitions.create_istance('list',output))
            
        else:
            values.append(parsed)
        
        last = parsed
        
    if len(values) == 1:
        return values[0]
    else:
        return None

def call(function, arguments, variables):
    """
    Call a function with given arguments.
    """
    # assign variables to arguments
    child_variables = assign(function['arguments'], [arguments], variables)
    
    # run the code (either nylo code or python code)
    if function['value']['type'] == 'code':
        return run(function['value'], child_variables)
        
    elif function['value']['type'] == 'python_code':
        # if it's python code we also shall actually create the variables
        for var in child_variables:
            var_value = child_variables[var]
            exec(var+'='+str(var_value))
        return eval(function['value']['value'])
            
def get_var_value(to_get_var, variables):
    """
    Get the value of a variable from the object it's called in
    """
    while 1:
        # if it's a known variable, return it
        if to_get_var['value'] in variables:
            return variables[to_get_var['value']]
        # else, let's check if it was defined in the father object
        else:
            if 'father' in variables:
                variables = variables['father']
            # no father? it's over. No such variable.
            else:
                raise NameError(to_get_var)
                
def assign(args, args_values, variables):
    """
    Create a child dictionary from variable by assigning arguments to their values
    """
    child_variables = {}
    
    #{x|}(1,2,3) --> {x|}([1,2,3])
    if len(args['value']) == 1 and len(args_values)>1: 
        args_values = [definitions.create_istance('list', args_values)]
        
    # {x|}([[[1,2,3]]]) --> {x|}([1,2,3])
    while len(args['value']) == 1 and len(args_values)==1 and args_values[0]['type'] == 'list' and len(args_values[0]['value']) == 0:
        args_values = args_values[0]['value']
        
    #{a,b,c|}([1,2,3]) --> {a,b,c|}(1,2,3)
    while len(args['value']) > 1 and len(args_values)==1 and args_values[0]['type'] == 'list': 
        args_values = args_values[0]['value']
        
    #{>1}(2) --> {x|x>1}(2)
    if len(args['value']) == 0 and len(args_values) == 1: 
        args['value'] = [[['implicit']]]
        
    #{a,b|}(1,2,3) --> fk u
    if len(args['value']) != len(args_values):
        raise TypeError
    
    # loop thru arguments to set 'em all
    for i, arg in enumerate(args['value']):
        child_variables[arg[-1][-1]] = args_values[i]
        
    child_variables['father'] = variables
    
    return child_variables
