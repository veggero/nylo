from nylo.objects.nyobject import NyObject
from nylo.objects.values.value import Value


class PyValue(NyObject):
    """
    This class is used to define a value
    and it's derived from NyObject.

    It could be used to store a value and
    evaluate it using a stack.
    """

    def __init__(self, value, types):
        self.typefun = types
        super().__init__(value)

    def __str__(self) -> str:
        """
        It returns a string that
        could represent the object.

        :return: The representation
        :rtype: str
        """
        return '<lambda>'

    def evaluate(self, stack):
        output = self.value(stack)
        if not isinstance(output, NyObject):
            output = Value(output)
        return output

    # def settype(self, types, stack):
    #    self.types = self.typefun(stack)
    #    return self.types
