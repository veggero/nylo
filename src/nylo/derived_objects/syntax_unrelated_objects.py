import copy

from nylo.exceptions import cant_call
from nylo.base_objects.Token import Token


class Get(Token):

    def __init__(self, source, value): self.source, self.value = source, value


class Set(Token):

    def __init__(self, target, value): self.target, self.value = target, value

    def evaluate(self, stack): return self.value.evaluate(stack)


class Output(Token):

    def __init__(self, value, to): self.value, self.to = value, to
