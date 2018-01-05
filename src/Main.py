#!/usr/bin/python3
import sys
import platform
import datetime
import time


def main(argv):
    try:
        command = getCommand(argv)
        if command == 'version':
            print("Nylo 0.10 (" + date(time.time()) + ")\n(" +
                  platform.release() + ") on " + platform.system())
            exit()
        if command == 'help':
            print(helpMessage())
    except KeyError:
        pass


def getCommand(parsedArguments):
    for key, value in parsedArguments.items():
        if key == 'version' and value:
            return 'version'
        elif key == 'help' and value:
            return 'help'


def helpMessage():
    return ("usage: nylo [options] file\n\n" +
            "A new programming language\n\n" +
            "nylo options:\n      --version" +
            "            display version" +
            " number of nylo and platform" +
            " details\n      --help      " +
            "          display this help message")


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


def date(unixtime, format='%m/%d/%Y %H:%M'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)


if __name__ == '__main__':
    main(parseArguments(sys.argv))
