import string
from nylo.lexers.lexer import Lexer
from nylo.objects.values.keyword import Keyword as KwObj


class Keyword(Lexer):

    @staticmethod
    def able(reader): return reader.read() in string.ascii_letters + '_'

    def lexe(self, reader):
        while reader.read() in string.ascii_letters + '_':
            yield reader.move()

    def parse(self, reader):
        return KwObj(''.join(self.lexe(reader)))
