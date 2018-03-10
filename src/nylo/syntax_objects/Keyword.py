import string

from nylo.base_objects.Token import Token


class Keyword(Token):

    starts = list(string.ascii_letters) + ['_']

    def parse(self, reader):
        out = ''
        while (reader.read() in
               self.starts + ['_'] + list(string.digits)):
            out += reader.read_and_move()
        self.value = out

    def evaluate(self, stack):
        return stack.get_variable(self.value)
