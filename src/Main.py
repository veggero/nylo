#!/usr/bin/python3
import sys
import platform
import datetime
import time

def main(argv):
    try:
        if argv['version']:
            print("Nylo 0.10 (" + date(time.time()) + ")\n(" + platform.release() + ") on " + platform.system())
    except KeyError:
        pass


def parseArguments(argv):
    parsedArguments = {}
    lastArgument = 'script'
    for argument in argv:
        if argument.startswith('--'):
            parsedArguments[argument.replace('--', '')] = ''
            if parsedArguments[lastArgument] == '':
                parsedArguments[lastArgument] = True
            lastArgument = argument.replace('--', '')
        else:
            parsedArguments[lastArgument] = argument
    for key, value in parsedArguments.items():
        if value == '':
            parsedArguments[key] = True
    return parsedArguments


def date(unixtime, format = '%m/%d/%Y %H:%M'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

if __name__ == '__main__':
    main(parseArguments(sys.argv))
