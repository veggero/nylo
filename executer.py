import definitions
import parser

from pprint import pprint

def execute(raw_code):
    """
    Parse and run raw code.
    """
    code = parser.parse(raw_code)
    return run(code, definitions.nylo)

def run(code, variables):
    """
    Call all the functions in a code object
    """
    last = definitions.create_instance('none', None)
    values = []
    
    # iter all of parsed in code
    for parsed in code['value']:
        # if it's a variable replace it with his value
        if parsed['type'] == 'variable':
            parsed = get_var_value(parsed, variables)
    
        # if this is a code, and obj before was a function,
        # let's hella call that function
        if parsed['type'] == 'code' and last['type'] in 'function overloaded_functions':
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
                if element['type'] == 'code':
                    element = run(element, variables)
                output.append(element)
            values.append(definitions.create_instance('list',output))
            
        else:
            values.append(parsed)
        
        last = parsed
        
    if len(values) == 1:
        return values[0]
    else:
        return definitions.create_instance('none', None)

def call(function, arguments, variables):
    """
    Call a function with given arguments.
    """
    # check if they're overloaded functions
    if function['type'] == 'overloaded_functions':
        accettable_functions = []
        # check which functions are accetable
        for function in function['value']:
            try:
                assign(function['arguments'], [arguments], variables)
                accettable_functions.append(function)
            except TypeError:
                pass
        # we selected the function we wanted?
        if len(accettable_functions) == 1:
            function = accettable_functions[0]
        else:
            # well shit
            raise TypeError('Unclear overloaded functions called')
    
    # assign variables to arguments
    child_variables = assign(function['arguments'], [arguments], variables)
    child_variables['father'] = variables
        
    # run the code (either nylo code or python code)
    if function['value']['type'] == 'code':
        return run(function['value'], child_variables)
        
    elif function['value']['type'] == 'nylo_var_assignation':
        f_arguments = child_variables['f_arguments']
        to_assign_value = child_variables['value']
        new_dictionary = assign(f_arguments, [to_assign_value] if not to_assign_value["type"]=="list" else to_assign_value["value"], variables)
        for key in new_dictionary:
            # we have to check if there is already a function
            # if so, and if we are assigning another function, we need
            # to create a overloaded_functions
            if key in variables and new_dictionary[key]['type'] == 'function':
                if variables[key]['type'] == 'function' :
                    variables[key] = definitions.create_instance('overloaded_functions', [variables[key], new_dictionary[key]]) 
                elif variables[key]['type'] == 'overloaded_functions':
                    variables[key]['value'].append(new_dictionary[key])
                else:
                    variables[key] = new_dictionary
            else:
                variables[key] = new_dictionary[key]
        return definitions.create_instance('none', None)
        
    elif function['value']['type'] == 'python_code':
        # if it's python code we also shall actually create the variables
        for var in child_variables:
            var_value = child_variables[var]
            locals()[var] = var_value
        out = eval(function['value']['value'])
        exec('')
        # python.None -> Nylo.none
        if out == None:
            out = definitions.create_instance('none', None)
        return out
        
    else:
        raise TypeError("Weird Function")

def is_instance(instance, arguments, variables):
    """
    Check if an object is an instance of a class, given instance, class' arguments, and variables (to get other classes).
    """
    py_arguments = arguments['value']
    for argument in py_arguments:
        
        variable_name = argument[-1][0]
        
        # if class wants a 'x' propriety and instance hasn't it,
        # it's not an instance at all 
        if not variable_name in instance:
            return definitions.create_instance('bool', False)
            
        variable_values = [instance[variable_name]]
        
        # now, every propriety has some conditions
        for var_type in argument[:-1]:
            next_variable_values = []
            for variable_value in variable_values:
            
                # first one is always another class that propriety should be
                var_class_var = var_type[0]
                
                var_class = get_var_value(definitions.create_instance('variable', var_class_var), variables)
                if not is_instance(variable_value, var_class['value'], variables)['value']:
                    return definitions.create_instance('bool', False)
                
                # from index 1 to last, there are conditions to be run
                for var_type_cond in var_type[1:]:
                    code = var_type_cond['value']
                    function = definitions.create_instance('function', code, arguments = 
                                                        definitions.create_instance('arguments', [[[var_class_var]], [['implicit']]]))
                    if not call(function, definitions.create_instance('list', [variable_value, variable_value]), variables)['value']:
                        return definitions.create_instance('bool', False)
                        
                if var_class_var == 'list':
                    for element in variable_value['value']:
                        next_variable_values.append(element)
                    
            variable_values = [x for x in next_variable_values]
                    
    
    return definitions.create_instance('bool', True)
            
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
        args_values = [definitions.create_instance('list', args_values)]
        
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
    
    # example of args['value'] to better understand what is going on
    # [[['a']], [['int', {conditions}], ['x']], [['int'], ['y']], [['list'], ['string', {conditions}], ['k']], [['list'], ['string'], ['z']]]
    
    for i, arg in enumerate(args['value']):
        variable_name = arg[-1][0]
        child_variables[variable_name] = args_values[i]
        
        # also set conditions if there aren't
        if len(arg)>1:
            child_variables[variable_name+'_conditions'] = definitions.create_instance('arguments', [arg])
            if not is_instance({variable_name: args_values[i]}, child_variables[variable_name+'_conditions'], variables)['value']:
                raise TypeError
        elif variable_name+'_conditions' in variables:
            if not is_instance({variable_name: args_values[i]}, variables[variable_name+'_conditions'], variables)['value']:
                raise TypeError
    
    return child_variables
