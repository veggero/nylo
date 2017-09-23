# import what I need
import string;
import definitions;

def parse(code):
    """
    Inputs Nylo raw code, and outputs a code-object, in order to make
    execution easier. Types created by this:
     name      -> object repr                                              -> value type
     ------------------------------------------------------------------------------------------
     string    -> {'value': 'hello world', 'type': 'number'}                -> string           
     number    -> {'value': 3, 'type': 'number'}                            -> int/float        
     code      -> {'value': [], 'type': 'code'}                             -> list parsed      
     list      -> {'value': [], 'type: 'list''}                             -> list list parsed 
     function  -> {'value': [], 'type': 'function', 'arguments': [[], 'x']} -> list parsed      
     variable  -> {'value': 'i', 'type': 'variable'}                        -> string           
     symbol    -> {'value': '+', 'type': 'symbol'}                          -> string
     arguments -> {'value': [[[],'']], 'type': 'arguments'}                 -> list list[len()=2] (string, condition)
     class     -> {'value': (arguments), 'type': 'class'}                   -> arguments 
     condition -> {'value': (code), 'type': 'condition'}                    -> code
    """

    # initialize the counter and put code into brackets
    # [0] instead of just 0 because it is a workaround
    # of python 2. This really makes me question why I still use Python 2... 
    # https://stackoverflow.com/questions/13985671 
    i = [0]
    # add EOF
    code += ')'

    def parse_code_until(end='', raw=False):
        """
        Main function to parse raw Nilo code.
        calls:
        > parse_string
        > parse_number
        > parse_bracket
        > > parse_key
        > > parse_value
        > parse_function
        > parse_arguments
        > parse_variable
        > parse_symbol
        > elab_assignation
        > replace_symbols
        
        raw flag: do not execute replace_symbols at the end 
        """

        # skip beginnings
        if code[i[0]] in '([':
            i[0] += 1;
        parsed = [];

        def parse_string():
            """
            Parse a Nylo string into a Nylo String Object.
            """
            j, value = i[0]+1, ''
            # loop the whole string until closing match
            while code[j]!=code[i[0]]:
                value += code[j]
                j += 1
            i[0] = j+1
            return {'value': value, 'type': 'string'}

        def parse_number():
            """
            Parse a Nylo number into a Nylo Number Object.
            """
            value = ''
            # loop the whole number and return it 
            while code[i[0]] in string.digits + '.-':
                value += code[i[0]]
                i[0] += 1
            if '.' in value:
                return {'value': float(value), 'type': 'float'}
            else:
                return {'value': int(value), 'type': 'int'}

        def parse_bracket():
            """
            Parse [] brackets, wich is either a list or a dictionary.
            """
            # get over the '['
            i[0] += 1
            parsed = []

            def parse_key():
                """
                Parse the first element of a bracket, either an entire
                element of the list, or the key of a dictionary.
                """
                # skip first , (sometimes there is)
                if code[i[0]] == ',':
                    i[0] += 1
                    
                # loop everithing (such pro!)
                key = parse_code_until(':,]')
                
                # if we ended on a : we are probably in a dict,
                # so let's call the parse_value
                if code[i[0]] == ':':
                    value = parse_value()
                    return {'value': [key, value], 'type': 'couple'}
                else:
                    # it was a list element so let's just return it
                    return key

            def parse_value():
                """
                When parsing a dictionary, this parse the
                value of a key.
                """
                return parse_code_until(',]')

            while code[i[0]] != ']':
                parsed.append(parse_key())
            i[0]+=1
            return {'value': parsed, 'type': 'list'}

        def parse_function():
            """
            Parse a raw Nylo function into a Nylo Function Object.
            """
            # get over the { and ' '
            while code[i[0]] in '{ ':
                i[0] += 1

            # parse arguments RAW!
            args = parse_code_until('|}', True)
            # is there more to parse? (aka: was everything before just arguments)
            if code[i[0]-1] == '|': 
                args = parse_arguments(args)
                parsed = parse_code_until('}')
                return {'arguments': args, 'value': parsed, 'type': 'function'}
            else:
                # this is either a class or a function with no arguments
                # if it's only variables and ',' and conditions it's a class
                if all([parse['type']=='variable' or parse['value']==',' or parse['type']=='condition' for parse in args['value']]):
                    args = parse_arguments(args)
                    return {'value': args, 'type': 'class'}
                else:
                    # still RAW, so let's elab it
                    args = replace_symbols(args['value']) 
                    return {'value': args, 'arguments': {'type': 'arguments', 'value': []}, 'type': 'function'}

        def parse_arguments(code): #{int x, y, list float n |...}
            """
            Parse the arguments of a function, given their parsed code.
            """
            
            code = code['value'] + [{'value': 'End Of Code', 'type':'symbol'}];
            # arguments is the list of arguments and will be
            # edited and checked by parse_arg globally
            arguments, i = [[]], 0 
            
            while len(code) != i:

                # this is because of things like int[=2]
                # it's all because of them
                if code[i]['type'] == 'condition':
                    arguments[-1][-1].append(code[i])
                    i += 1
                    while code[i]['value'] == ',':
                        i += 1
                
                name, i = code[i]['value'], i+1;
                # now let's check if we ended on symbol or another variable
                if code[i]['type'] == 'symbol':
                    # okay then, this is a name of a variable
                    # so we check if we specified what type it has to be
                    # and also if this is *not* the first variable it's declared
                    if len(arguments[-1]) == 0 and len(arguments) > 1:
                        # well it is not specified the type,
                        # then we might just as well assume that the type is the same
                        # of the last variable, so we take it
                        arguments[-1] = arguments[-2][:-1]
                    # we have the name of the variable, let's set it
                    arguments[-1].append([name])
                    # this variable is all setted, so let's set up a new one
                    arguments.append([])
                    i += 1;
                else:
                    # we ended on a variable, wich means that what
                    # we have is actually a type, so we add it
                    # to the list of types
                    arguments[-1].append([name])

            # delete last element, because it was a proto-variable -> [[], '']
            del arguments[-1]
            return {'value': arguments, 'type': 'arguments'}


        def parse_variable():
            """
            Parse a raw Nylo variable into a Nylo Variable Object.
            """
            name = ''
            while code[i[0]] in string.ascii_letters:
                name += code[i[0]]
                i[0] += 1
            return {'value': name, 'type': 'variable'}

        def parse_symbol():
            """
            Parse a single character into a Nylo Symbol Object.
            """
            i[0] += 1
            return {'value': code[i[0]-1], 'type': 'symbol'}

        def elab_assignation():
            """
            Rewrite parsed to add a arguments object.
            """
            # okay, this is an assignation. No shit. We need to go back and
            # take every variable / ',' / condition, remove them from parsed and
            # parse_arguments them, and then add then new object to
            # parsed again
            # also, we need to call parse_arguments with a code obj, so
            # let's create it
            code = {'value': [], 'type': 'code'}
            while ([{'type': ''}]+parsed)[-1]['type'] == 'variable' or ([{'value': ''}]+parsed)[-1]['value'] == ',' or ([{'type': ''}]+parsed)[-1]['type'] == 'condition':
                code['value'].append(parsed[-1])
                del parsed[-1]
            # we took them backward, so we need to reverse them
            code['value'].reverse()
            parsed.append(parse_arguments(code))
            # also, we also should parse the ': '
            parsed.append({'value': ': ', 'type': 'symbol'})
            i[0] += 2
        
        def replace_symbols(parsed): # TODO MAKE THIS WORK TOO
            """
            Replacing symbols with functions
            1+1 --> sum(1,1)
            """
            # reading every character
            reading = 0
            while reading < len(parsed):
                if parsed[reading]['type'] == 'symbol':
                    
                    symbol = parsed[reading]
                    # if there is a value before,
                    # take values before the symbol (the one after will be taken later)
                    
                    if not reading == 0:
                        if parsed[reading-1]['type'] != 'symbol':
                            arguments = [parsed[reading-1]]
                            # delete the value we took (we need to replace it w/ the function)
                            del parsed[reading-1]
                            # move the reader back of a place because we deleted the value before
                            reading -= 1
                        else:
                            arguments = [{'type':'variable', 'value': 'implicit'}]
                    else:
                        arguments = [{'type':'variable', 'value':'implicit'}]
                    
                    # loop every symbol to get all of the args (1+1+1+1 --> sum(1,1,1,1))
                    while parsed[reading] == symbol:
                        # delete the symbol from parsed
                        del parsed[reading]
                        # add the value after the symbol to the arguments
                        if len(parsed)!=0:
                            if parsed[reading]['type'] != 'symbol':
                                arguments.append(parsed[reading])
                                # delete it from parser
                                del parsed[reading]

                            else:
                                arguments.append([{'type':'variable', 'value': 'implicit'}])                            
                        else:
                            arguments.append([{'type':'variable', 'value': 'implicit'}])
                        # do this until we stop finding the same symbol
                        # check EOF
                        if reading == len(parsed):
                            break;
                        
                    # get the function name
                    name = definitions.symbols[symbol['value']]
                    # make arguments a list
                    arguments = {'type': 'list', 'value': arguments}
                    # now we add the function as a variable
                    parsed.insert(reading, {'value': name, 'type': 'variable'})
                    # and the arguments as code
                    parsed.insert(reading+1, {'value': [arguments], 'type': 'code'})
                    
                reading += 1
            return parsed

        # checking every char and calling the right parser until end of code or
        # breakline or end of string
        while not (code+' ') [i[0]] in end and not i[0] == len(code):
            if code[i[0]] in '"\'':
                parsed.append(parse_string())
            elif code[i[0]] in string.digits or (code[i[0]] in '-.' and code[i[0]+1] in string.digits + '.'):
                parsed.append(parse_number())
            elif code[i[0]] == '(':
                parsed.append(parse_code_until(')'))
            elif code[i[0]] == '[':
                # this is either a (list/dict) or a condition.
                # every condition is just after a variable, so we check that
                if ([{'type':''}]+parsed)[-1]['type'] == 'variable':
                    parsed.append({'value': parse_code_until(']'), 'type': 'condition'})
                else:
                    parsed.append(parse_bracket())
            elif code[i[0]] == '{':
                parsed.append(parse_function())
            elif code[i[0]] in string.ascii_letters:
                parsed.append(parse_variable())
            elif code[i[0]] in ' \n': #(spaces and newlines are ignored)
                i[0] += 1
            elif code[i[0]:i[0]+2] == ': ':
                # this directly edits parsed
                elab_assignation()
            elif code[i[0]:i[0]+2] == '//':
                # inline comment. Ignore until newline
                while code[i[0]] != '\n':
                    i[0] += 1
            elif code[i[0]:i[0]+2] == '/*':
                # multiline comment. Ignore until '*/'
                while code[i[0]:i[0]+2] != '*/':
                    i[0] += 1
                i[0] += 2
            else:
                parsed.append(parse_symbol())

        # if it's not needed raw, elaborate it by replacing
        # symbols with functions
        if not raw:
            parsed = replace_symbols(parsed)
        # eat last character
        i[0]+=1
        
        return {'value': parsed, 'type': 'code'}

    return parse_code_until(')')

print(parse('int[2=] point: {int[=3] x, y}'))
