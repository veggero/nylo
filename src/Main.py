#!/usr/bin/python3
import sys
import platform
import datetime
import time
from io import IOBase
import nylo

nodeSpace = '    '


def main(argv):
    try:
        command = getCommand(argv)
        if isinstance(command, str):
            if command == 'version':
                print("Nylo 0.10 (" + date(time.time()) + ")\n(" +
                      platform.release() + ") on " + platform.system())
                exit()
            elif command == 'help':
                print(helpMessage())
            elif command == 'file_not_found':
                print("Error: File not found\n\n" + helpMessage())
        elif isinstance(command, IOBase):
            program(command)
    except KeyError:
        pass


def program(code):
    with code as obj:
        lines = list(obj)
    for line in lines:
        node = getNode(line)
        if not isComment(line):
            pass
            # TODO - Parsing function
        else:
            continue


def isComment(line: str):
    global tokens
    return (line.lstrip()).startswith(tokens['COMMENT_ONELINE'])


def getNode(line: str):
    global nodeSpace
    whitespace = line.replace(line.lstrip(), '')
    return whitespace.count(nodeSpace)


def getCommand(parsedArguments):
    for key, value in parsedArguments.items():
        if key == 'version' and value:
            return 'version'
        elif key == 'help' and value:
            return 'help'
        elif key == 'i' and value:
            try:
                file = open(value, 'r')
                return file
            except FileNotFoundError:
                return 'file_not_found'


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
