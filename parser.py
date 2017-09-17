# import what I need
import string;

symbols = {
    '+': 'sum',
    '-': 'sub',
    '/': 'div',
    '*': 'mol',
    ',': 'list',
}

def parse(code):
    """
    Inputs Nylo raw code, and outputs a code-object, in order to make
    execution easier. Types created by this:
     name      -> object repr                                              -> value type
     ------------------------------------------------------------------------------------------
     string    -> {'value': 'hello world', 'type': 'number'}               -> string           
     number    -> {'value': 3, 'type': 'number'}                           -> int/float        
     code      -> {value: [], 'type': 'code'}                              -> list parsed      
     list      -> {value: [], 'type: 'list''}                              -> list list parsed 
     function  -> {value: [], 'type': 'function', 'arguments': [[], 'x']}  -> list parsed      
     variable  -> {value: 'i', 'type': 'variable'}                         -> string           
     symbol    -> {value: '+', 'type': 'symbol'}                           -> string 
    """

    # initialize the counter and put code into brackets
    # [0] instead of just 0 because it is a workaround
    # best way both in python and python3
    i = [0]
    # adding EOF
    code += ')'

    def parse_code_until(end):
        """
        Main function to parse raw Nilo code.
        calls:
        > callParse
        > parse_string
        > parse_number
        > parse_bracket
        > > parse_key
        > > parse_value
        > parse_function
        > > parse_arguments
        > parse_variable
        > parse_symbol
        """

        # skip beginnings
        if code[i[0]] == '(':
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
            while code[i[0]] in string.digits + '.':
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
                # skip first , (sometimes there is one)
                if code[i[0]] == ',':
                    i[0] += 1
                    
                # loop everithing (such pro!)
                key = parse_code_until(':,]')
                
                # if we ended on a : we are probably in a dict,
                # so let's call the parse_value
                if code[i[0]-1] == ':':
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

            while code[i[0]-1] != ']':
                parsed.append(parse_key())
            return {'value': parsed, 'type': 'list'}

        def parse_function():
            """
            Parse a raw Nylo function into a Nylo Function Object.
            """
            # get over the { and ' '
            while code[i[0]] in '{ ':
                i[0] += 1

            def parse_arguments(): #{int x, y, list float n |...}
                """
                Parse the arguments of a function.
                """

                # arguments is the list of arguments and will be
                # edited and checked by parse_arg globally
                arguments = [[[], '']] # [[['int'], 'x'], [['int'], 'y'], [['list', 'float'], 'n']]
                
                while code[i[0]] != '|' and code[i[0]] != ':':
                    name = ''
                    # getting the single name
                    while code[i[0]] != ' ' and code[i[0]] != ',' and code[i[0]] != '|':
                        name += code[i[0]]
                        i[0] += 1
                    # let's also eat the space[s]
                    while code[i[0]] == ' ':
                        i[0] += 1
                    # now let's check if we ended on ',' or ' '
                    if code[i[0]] == ',' or code[i[0]] == '|':
                        # okay, this is a name of a variable
                        # so we check if we specified what type it has to be
                        # and also if this is *not* the first variable it's declared
                        if len(arguments[-1][0]) == 0 and len(arguments) > 1:
                            # well it is not specified the type,
                            # then we might just as well assume that the type is the same
                            # of the last variable, so we take it
                            arguments[-1][0] = arguments[-2][0]
                        # we have the name of the variable, let's set it
                        arguments[-1][1] = name
                        # this variable is all setted, so let's set up a new one
                        arguments.append([[], ''])
                        # let's eat the ',' or ' ' if needed
                        while code[i[0]] == ' ' or code[i[0]] == ',':
                            i[0] += 1
                    else:
                        # we ended on a space, wich means that what
                        # we have is actually a type, so we add it
                        # to the list of types
                        arguments[-1][0].append(name)
                i[0] += 1

                # delete last element, because it was a proto-variable -> [[], '']
                del arguments[-1]
                return arguments


            # parse arguments
            args = parse_code_until('|')
            parsed = parse_code_until('}')
            return {'arguments': args, 'value': parsed, 'type': 'function'}

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
        
        def replace_symbols(parsed):
            """
            Replacing symbols with functions
            1+1 --> sum(1,1)
            """
            # reading every character
            reading = 0
            while reading < len(parsed):
                if parsed[reading]['type'] == 'symbol':
                    
                    symbol = parsed[reading]
                    # taking values before the symbol (the one after will be taken later)
                    arguments = [parsed[reading-1]]
                    # delete the value we took (we need to replace it w/ the function)
                    del parsed[reading-1]
                    # move the reader back of a place because we deleted the value before
                    reading -= 1
                    
                    # loop every symbol to get all of the args (1+1+1+1 --> sum(1,1,1,1))
                    while parsed[reading] == symbol:
                        # delete the symbol from parsed
                        del parsed[reading]
                        # add the value after the symbol to the arguments
                        arguments.append(parsed[reading])
                        # delete it from parser
                        del parsed[reading]
                        # do this until we stop finding the same symbol
                        # check EOF
                        if reading == len(parsed):
                            break;
                        
                    # get the function name
                    name = symbols[symbol['value']]
                    # make arguments a list
                    arguments = {'type': 'list', 'value': arguments}
                    # now we add the function as a variable
                    parsed.insert(reading, {'value': name, 'type': 'variable'})
                    # and the arguments as code
                    parsed.insert(reading+1, {'value': arguments, 'type': 'code'})
                    
                reading += 1
            return parsed

        # checking every char and calling the right parser until end of code or
        # breakline or end of string (repr by ~)
        while not (code+' ') [i[0]] in end and not i[0] == len(code):
            if code[i[0]] in '"\'':
                parsed.append(parse_string())
            elif code[i[0]] in string.digits or (code[i[0]] in '-.' and code[i[0]+1] in string.digits + '.'):
                parsed.append(parse_number())
            elif code[i[0]] == '(':
                parsed.append(parse_code_until(')'))
            elif code[i[0]] == '[':
                parsed.append(parse_bracket())
            elif code[i[0]] == '{':
                parsed.append(parse_function())
            elif code[i[0]] in string.ascii_letters:
                parsed.append(parse_variable())
            elif code[i[0]] in ' \n': #(spaces and newlines are ignored)
                i[0] += 1
            else:
                parsed.append(parse_symbol())
        
        parsed = replace_symbols(parsed)
        # eat last character
        i[0]+=1
        
        return {'value': parsed, 'type': 'code'}

    return parse_code_until(')')

assert parse('1 +1 + 1') == {'value': [{'value': 'sum', 'type': 'variable'}, {'value': {'value': [{'value': 1, 'type': 'int'}, {'value': 1, 'type': 'int'}, {'value': 1, 'type': 'int'}], 'type': 'list'}, 'type': 'code'}], 'type': 'code'}
parse('1/ciao') == {'value': [{'value': 'div', 'type': 'variable'}, {'value': {'value': [{'value': 1, 'type': 'int'}, {'value': 'ciao', 'type': 'variable'}], 'type': 'list'}, 'type': 'code'}], 'type': 'code'}
parse('sum(1,2)') == {'value': [{'value': 'sum', 'type': 'variable'}, {'value': [{'value': 'list', 'type': 'variable'}, {'value': {'value': [{'value': 1, 'type': 'int'}, {'value': 2, 'type': 'int'}], 'type': 'list'}, 'type': 'code'}], 'type': 'code'}], 'type': 'code'}
parse('[1,2,3]') == {'value': [{'value': [{'value': [{'value': 1, 'type': 'int'}], 'type': 'code'}, {'value': [{'value': 2, 'type': 'int'}], 'type': 'code'}, {'value': [{'value': 3, 'type': 'int'}], 'type': 'code'}], 'type': 'list'}], 'type': 'code'}
parse('[1:2]') == {'value': [{'value': [{'value': [{'value': [{'value': 1, 'type': 'int'}], 'type': 'code'}, {'value': [{'value': 2, 'type': 'int'}], 'type': 'code'}], 'type': 'couple'}], 'type': 'list'}], 'type': 'code'}
parse('{x|print("hello")}') == {'value': [{'value': {'value': [{'value': 'print', 'type': 'variable'}, {'value': [{'value': 'hello', 'type': 'string'}], 'type': 'code'}], 'type': 'code'}, 'arguments': {'value': [{'value': 'x', 'type': 'variable'}], 'type': 'code'}, 'type': 'function'}], 'type': 'code'}
