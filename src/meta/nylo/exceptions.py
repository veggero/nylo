class NyloSyntaxError(SyntaxError): pass

class NyloIndentError(NyloSyntaxError): pass

class WrongSyntaxError(NyloSyntaxError): pass

class PathSyntaxError(WrongSyntaxError): pass

class StructSyntaxError(WrongSyntaxError): pass

class StringSyntaxError(WrongSyntaxError): pass

class UnexpectedCharacter(NyloSyntaxError): pass

class NyloValueError(ValueError): pass

class NyloNameError(NameError): pass
