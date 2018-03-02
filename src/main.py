import nylo

# TODO:
# Features:
# (easy) Informative Errors with line and character
# (easy) Fix facultative comma in structures
# (hard) Right symbols priority

if __name__ == '__main__':
    print("Nylo Command Line!")
    print()
    print('You can now write code in Value Mode, aka everything is a value.')
    print('Remember tho, .ny files will be executed in Struct Mode,')
    print('to get the same results as here use `obj main: {code}`')
    print()
    while 1:
        stack = nylo.builtins
        try: 
            reader = nylo.Reading(input('nylo> '), 0)
            input_value = nylo.Value(reader)
            reader.end()
            out = input_value.evaluate(stack)
            if not out is None: print('<- '+str(out))
        except Exception as Ex:
            stack.show_traceback(Ex)
