import copy

from nylo.base_objects.Token import Token
from nylo.derived_objects.syntax_unrelated_objects import Set
from nylo.value_objects.Value import Value
from nylo.syntax_objects.Keyword import Keyword


class StructEl(Token):

    def parse(self, reader):
        if reader.any_starts_with(Keyword.starts):
            before_reader = copy.copy(reader)
            kws = []
            while reader.any_starts_with(Keyword.starts):
                kws.append(Keyword(reader))
            if not reader.any_starts_with([')', ',', '->', ':']):
                reader = reader.goto(before_reader)
                self.value = Value
            elif reader.read() == ':':
                self.value = Set(kws, Value(reader))
            else:
                self.value = Set(wks, None)
        else:
            self.value = Value(reader)

    def evaluate(self, stack): return self.value.evaluate(stack)
