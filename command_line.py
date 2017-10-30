import executer
import definitions

print('Command Line for Nylo.\n')

while 1:

    try:
        code = input('nylo> ')
        output = executer.execute(code)
        output = executer.call(definitions.nylo['to_str'], output, definitions.nylo)
        if 'value' in output:
            if type(output['value']) == type(str()) and output['value'] != 'none':
                print( '<- '+output['value'] )
        
        
    except KeyboardInterrupt:
        print('\n')
        break
