import executer

print('Command Line for Nylo.\n')

while 1:

    try:
        code = input('nylo> ')
        output = executer.execute(code)['value']
        
        if output != None:
            print('<- '+str(output))
        
    except KeyboardInterrupt:
        print('\n')
        break
