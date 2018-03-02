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
        input_value = nylo.Value(
                nylo.Reading(input('nylo> '), 0)
            )
        stack = nylo.builtins
        try:
            print('<- '+str(
                input_value.evaluate(stack)
            ))
        except Exception as Ex:
            stack.show_traceback(Ex)
