import string

from nylo.base_objects.Token import Token


class Number(Token):

    starts = list(string.digits) + ['.' + dig for dig in string.digits]

    def parse(self, reader):
        out = ''
        while (reader.read() in
               string.digits + '_'):

            out += reader.read_and_move()

        if reader.any_starts_with(self.starts):

            out += reader.read_and_move()
            while (reader.read() in
                   string.digits + '_'):
                out += reader.read_and_move()

        if '.' in out:
            self.value = float(out)
        else:
            self.value = int(out)

    def evaluate(self, stack): return self.value


class String(Token):

    starts = ['"', "'"]

    def parse(self, reader):
        out = ''
        start = reader.read_and_move()
        while (reader.read() != start):
            out += reader.read_and_move()
        reader.move()
        self.value = out

    def evaluate(self, stack): return self.value
