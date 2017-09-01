# import what I need
import string;

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
    # of python 2. This really makes me question why I still use Python 2... 
    # https://stackoverflow.com/questions/13985671 
    i = [0]

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
                key = parse_code_until(',]')
                
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
                # get over the : and get to the actual value 
                i[0] += 1
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
            i[0] += 1
            parsed = parse_code_until('}')
            i[0] += 1
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

        return {'value': parsed, 'type': 'code'}

    return parse_code_until('')

# quick testcase of everything
assert parse('[a,1,"h",{int x, y | print("ok")}, 1: 2]') == {'type': 'code', 'value': [{'type': 'list', 'value': [{'type': 'code', 'value': [{'type': 'variable', 'value': 'a'}]}, {'type': 'code', 'value': [{'type': 'int', 'value': 1}]}, {'type': 'code', 'value': [{'type': 'string', 'value': 'h'}]}, {'type': 'code', 'value': [{'type': 'function', 'arguments': {'type': 'code', 'value': [{'type': 'variable', 'value': 'int'}, {'type': 'variable', 'value': 'x'}, {'type': 'symbol', 'value': ','}, {'type': 'variable', 'value': 'y'}]}, 'value': {'type': 'code', 'value': [{'type': 'variable', 'value': 'print'}, {'type': 'code', 'value': [{'type': 'string', 'value': 'ok'}]}, {'type': 'symbol', 'value': ')'}]}}]}, {'type': 'code', 'value': [{'type': 'int', 'value': 1}, {'type': 'symbol', 'value': ':'}, {'type': 'int', 'value': 2}]}]}]}
