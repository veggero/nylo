"""
This modules contains all the function related to interpreting.
"""


from .tokens.keyword import Keyword


def interprete(mesh, starting_point=(Keyword('self'),)):
    interpreting, interpreted = [], []
    mesh[starting_point].interprete(mesh, interpreting, interpreted)
    while interpreting:
        interpreting.pop().evaluate(mesh, interpreting, interpreted)
    return interpreted.pop()
