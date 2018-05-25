from nylo.lexers.lexer import Lexer
from nylo.lexers.values.keyword import Keyword
from nylo.lexers.values.numstr import Number, String
from nylo.lexers.values.symbol import Symbol
from nylo.lexers.struct.struct import Struct
from nylo.objects.struct.call import Call as CallObj
from nylo.objects.values.value import GetObj
from nylo.objects.struct.structel import TypeDef
from nylo.objects.values.keyword import Keyword as KeyObj
from nylo.objects.values.value import Value as ValueObj


class Value(Lexer):

    @staticmethod
    def able(reader):
        return (Number.able(reader) or String.able(reader)
                or Keyword.able(reader) or Struct.able(reader))

    def lexe(self, reader):
        v = KeyObj('_implicit')
        if Keyword.able(reader):
            kw = Keyword(reader).value
            if Keyword.able(reader):
                kws = [kw]
                while Keyword.able(reader):
                    kws.append(Keyword(reader).value)
                v = TypeDef(kws)
            else:
                v = kw
        elif Number.able(reader):
            v = Number(reader).value
        elif String.able(reader):
            v = String(reader).value
        elif Struct.able(reader):
            v = Struct(reader).value
        reader.avoid_whitespace()
        if reader.read() in '(':
            return CallObj(v, Struct(reader).value)
        elif reader.read() in '[':
            return GetObj(v, Get(reader).value)
        else:
            return v

    def parse(self, reader): return self.lexe(reader)


class Get(Lexer):

    @staticmethod
    def able(reader): return '[' == reader.read()

    def lexe(self, reader):
        reader.move()
        yield Symbol(reader).value
        while reader.read() == ':':
            reader.move()
            yield Symbol(reader).value
        reader.move()

    def parse(self, reader):
        out = list(self.lexe(reader))
        if len(out) == 1:
            return out[0]
        else:
            return ValueObj(slice(*[o.value for o in out]))
