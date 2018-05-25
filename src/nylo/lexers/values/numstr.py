import string
from nylo.lexers.lexer import Lexer
from nylo.objects.values.value import Value as ValueObj


class Number(Lexer):

    @staticmethod
    def able(reader): return reader.read() in string.digits + '_'

    def lexe(self, reader):
        while reader.read() in string.digits + '_':
            yield reader.move()
        if reader.read() == '.':
            if reader.code[reader.reading_at + 1] in string.digits:
                yield reader.move()
                while reader.read() in string.digits + '_':
                    yield reader.move()

    def parse(self, reader):
        lexed = ''.join(self.lexe(reader))
        if '.' in lexed:
            return ValueObj(float(lexed))
        else:
            return ValueObj(int(lexed))


class String(Lexer):

    start_to_ends = {'"': '"', "'": "'", '«': '»'}

    def able(reader): return reader.read() in String.start_to_ends

    def lexe(self, reader):
        start = reader.move()
        while reader.read() != self.start_to_ends[start]:
            yield reader.move()
        reader.move()

    def parse(self, reader):
        return ValueObj(''.join(self.lexe(reader)))
