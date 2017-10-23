import executer

print('Command Line for Nylo.\n')

while 1:
    try:
        code = input('nylo> ')
        executer.execute(code)
    except KeyboardInterrupt:
        break
