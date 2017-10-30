# by veggero 

# import what I need
import string
import definitions

def parse(code):
    """
    Inputs Nylo raw code, and outputs a code-object, in order to make
    execution easier. Types created by this:
     name      -> object repr                                              -> value type
     ------------------------------------------------------------------------------------------
     string    -> {'value': 'hello world', 'type': 'string'}                -> string           
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
    # add start of code and end of code
    code = '('+code+')'

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
        if code[i[0]] in '(':
            i[0] += 1
        parsed = []
        output = []

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
            return definitions.create_instance('string', value)

        def parse_number():
            """
            Parse a Nylo number into a Nylo Number Object.
            """
            # we already gave a look to first char
            # (we wouldn't be here oterwise)
            value = code[i[0]]
            i[0]+=1
            # loop the whole number and return it 
            while code[i[0]] in string.digits + '.':
                if code[i[0]] == '.' and '.' in value:
                    # there is a "." and the number already has a "."?
                    # something's off. (this is to avoid 2.2.2.2 to be just one number)
                    # ("2.2.2.2" is number: 2.2 number: 0.2 number: 0.2 by the way)
                    break
                value += code[i[0]]
                i[0] += 1
            if '.' in value:
                return definitions.create_instance('float', float(value))
            else:
                return definitions.create_instance('int', int(value))

        def parse_bracket():
            """
            Parse [] brackets, which is either a list or a dictionary.
            """
            # get over the '['
            i[0] += 1
            parsed = []

            def parse_key():
                """
                Parse the first element of a bracket, either an entire
                element of the list, or the key of a dictionary.
                """
                # skip first , (sometimes there is one)
                if code[i[0]] == ',':
                    i[0] += 1
                    
                # loop everithing (such pro!)
                key = parse_code_until(':,]')
                
                # if we ended on a : we are probably in a dict,
                # so let's call the parse_value
                if code[i[0]-1] == ':':
                    value = parse_value()
                    return definitions.create_instance('couple', [key, value])
                else:
                    # it was a list element so let's just return it
                    return key

            def parse_value():
                """
                When parsing a dictionary, this parse the
                value of a key.
                """
                return parse_code_until(',]')

            while code[i[0]-1] != ']':
                parsed.append(parse_key())
            return definitions.create_instance('list', parsed)

        def parse_function():
            """
            Parse a raw Nylo function into a Nylo Function Object.
            """
            # get over the {
            if code[i[0]] == '{':
                i[0] += 1

            # parse arguments RAW!
            args = parse_code_until('|}', True)
            # is there more to parse? (aka: was everything before just arguments)
            if code[i[0]-1] == '|': 
                args = parse_arguments(args)
                parsed = parse_code_until('}')
                return definitions.create_instance('function', parsed, arguments = args)
            else:
                # this is either a class or a function with no arguments
                # if it's only variables and ',' and conditions it's a class
                if all([parse['type']=='variable' or parse['value']==',' or parse['type']=='condition' for parse in args['value']]):
                    args = parse_arguments(args)
                    return definitions.create_instance('class', args)
                else:
                    # still RAW, so let's elab it
                    args = replace_symbols(args['value']) 
                    return definitions.create_instance('function', definitions.create_instance('code', args), arguments = definitions.create_instance('arguments', []))

        def parse_arguments(code): #{int x, y, list float n |...}
            """
            Parse the arguments of a function, given their parsed code.
            """
            
            code = code['value'] + [{'value': 'End Of Code', 'type':'symbol'}]
            # arguments is the list of arguments and will be
            # edited and checked by parse_arg globally
            arguments, i = [[]], 0 
            
            # just an EOF? nothing to do here
            if len(code) == 1:
                return []
            
            while len(code) != i:
                
                # read first word and move pointer forward
                name, i = code[i]['value'], i+1
                
                # this is because of things like int[=2]
                # it's all because of them
                args = []
                while code[i]['type'] == 'condition':
                    args.append(code[i])
                    i += 1
                
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
                    arguments[-1].append([name]+args)
                    # this variable is all setted, so let's set up a new one
                    arguments.append([])
                    i += 1
                else:
                    # we ended on a variable, wich means that what
                    # we have is actually a type, so we add it
                    # to the list of types
                    arguments[-1].append([name]+args)

            # delete last element, because it was a proto-variable -> [[], '']
            del arguments[-1]
            return definitions.create_instance('arguments', arguments)


        def parse_variable():
            """
            Parse a raw Nylo variable into a Nylo Variable Object.
            """
            # already checked the first character
            # we wouldn't be here otherwise
            name = code[i[0]]
            i[0]+=1
            while code[i[0]] in string.ascii_letters + '_' + string.digits:
                name += code[i[0]]
                i[0] += 1
            return definitions.create_instance('variable', name)

        def parse_symbol():
            """
            Parse a single character into a Nylo Symbol Object.
            """
            i[0] += 1
            return definitions.create_instance('symbol', code[i[0]-1])

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
            nonlocal parsed
            code = definitions.create_instance('code', [])
            parsed = [{'type': '', 'value': ''}]+parsed
            while parsed[-1]['type'] == 'variable' or parsed[-1]['value'] == ',' or parsed[-1]['type'] == 'condition':
                code['value'].append(parsed[-1])
                del parsed[-1]
            del parsed[0]
            # we took them backward, so we need to reverse them
            code['value'].reverse()
            parsed.append(parse_arguments(code))
            # also, we also should parse the ': '
            parsed.append(definitions.create_instance('symbol', ": "))
            i[0] += 2
        
        def replace_symbols(parsed):
            """
            Replacing symbols with functions
            1+1 --> sum(1,1)
            """
            
            # reading every character
            for symbol_to_search in definitions.symbols_priority:
                reading = 0
                while reading < len(parsed):
                    if parsed[reading]['type'] == 'symbol' and parsed[reading]['value'] == symbol_to_search:
                        
                        # get the symbol we're parsing
                        symbol = parsed[reading]
                        # and remove it from parsed
                        del parsed[reading]
                        reading -= 1
                        arguments = [definitions.create_instance('code', [])]
                        
                        if reading != -1:
                            # now loop all thru the elements before the symbol until we find a different symbol
                            while parsed[reading]['type'] != 'symbol' or parsed[reading] == symbol:
                                
                                # kill the symbols, we don't need them where we're going # excuse me, what!?
                                if parsed[reading]['type'] == 'symbol':
                                    arguments.append(definitions.create_instance('code', []))
                                else:
                                    arguments[-1]['value'].insert(0, parsed[reading])
                                del parsed[reading]
                                reading -= 1
                                
                                if reading == -1:
                                    break
                        else:
                            arguments[-1]['value'].append(definitions.create_instance('variable', 'implicit'))
                        if len(arguments[-1]['value']) == 0:
                            arguments[-1]['value'].append(definitions.create_instance('variable', 'implicit'))
                        
                        reading += 1
                        arguments.append(definitions.create_instance('code', []))
                        if reading != len(parsed):
                            # then loop forward and take every value after the symbol
                            while parsed[reading]['type'] != 'symbol' or parsed[reading] == symbol:
                                
                                # kill the symbols, we don't need them where we're going
                                if parsed[reading]['type'] == 'symbol':
                                    arguments.append(definitions.create_instance('code', []))
                                else:
                                    arguments[-1]['value'].append(parsed[reading])
                                del parsed[reading]
                                
                                if reading == len(parsed):
                                    break
                        else:
                            arguments[-1]['value'].append(definitions.create_instance('variable', 'implicit'))
                        if len(arguments[-1]['value']) == 0:
                            arguments[-1]['value'].append(definitions.create_instance('variable', 'implicit'))
                            
                        # get the function name
                        name = definitions.symbols[symbol['value']]
                        # make arguments a list
                        arguments = definitions.create_instance('list', arguments)
                        # now we add the function as a variable
                        parsed.insert(reading, definitions.create_instance('variable', name))
                        # and the arguments as code
                        parsed.insert(reading+1, definitions.create_instance('code', [arguments]))
                        
                    reading += 1
            return parsed

        # checking every char and calling the right parser until end of code or
        # breakline or end of string
        while not (code+' ') [i[0]] in end and not i[0] == len(code):
            if code[i[0]] in '"\'':
                parsed.append(parse_string())
            elif code[i[0]] in string.digits + '-.': #42 .42 -42 -.42 4.2 -4.2  
                # Okay, numbers are a little tough. all of them starts with 0123456789-.
                # if first digit is - tho, we need to know there's a number after that, or
                # it might be just a symbol
                if code[i[0]] == '-':
                    # if there isn't a symbol before, it's clearly a symbol (1-1 is not number:1 number:-1
                    # but number: 1 symbol: - number: 1)
                    if len(parsed)>0:
                        if parsed[-1]['type']!='symbol':
                            parsed.append(parse_symbol())
                    # but it still could be -.3, so a . after a - is fine to...
                    elif code[i[0]+1] == '.':
                        # IF there is a digit after the -.
                        if code[i[0]+2] in string.digits:
                            parsed.append(parse_number())
                        else:
                            parsed.append(parse_symbol())
                    elif code[i[0]+1] in string.digits:
                        parsed.append(parse_number())
                    else:
                        parsed.append(parse_symbol())
                elif code[i[0]] == '.':
                    if code[i[0]+1] in string.digits:
                        parsed.append(parse_number())
                    else:
                        parsed.append(parse_symbol())
                else:
                    parsed.append(parse_number())
            elif code[i[0]] == '(':
                parsed.append(parse_code_until(')'))
            elif code[i[0]] == '[':
                # this is either a (list/dict) or a condition.
                # every condition is just after a variable, so we check that
                if ([{'type':''}]+parsed)[-1]['type'] == 'variable':
                    # skip initial [
                    i[0]+=1
                    # parse the condition until end
                    parsed.append(definitions.create_instance('condition', parse_code_until(']')))
                else:
                    parsed.append(parse_bracket())
            elif code[i[0]] == '{':
                parsed.append(parse_function())
            elif code[i[0]] in string.ascii_letters+'_':
                parsed.append(parse_variable())
                # but let's check for things like "is_a" -- they're
                # symbols, not variables
                if parsed[-1]['value'] in definitions.symbols:
                    parsed[-1] = definitions.create_instance('symbol', parsed[-1]['value'])
            elif code[i[0]] in ' \t': #(spaces and tabs are ignored)
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
            elif code[i[0]] in ';\n':
                i[0] += 1
                # end of line of code. Elab what there's to elab and add to output
                if not raw:
                    parsed = replace_symbols(parsed)
                output.append(parsed)
                parsed = []
            else:
                parsed.append(parse_symbol())

        # if it's not needed raw, elaborate it by replacing
        # symbols with functions
        if not raw:
            parsed = replace_symbols(parsed)
        output.append(parsed)
        parsed = []
        # eat last character
        i[0]+=1
        
        # the output is a list of parsed, but we
        # only want one parsed, so we join every
        # element in output 
        output = [j for i in output for j in i]
        
        return definitions.create_instance('code', output)

    return parse_code_until(')')
