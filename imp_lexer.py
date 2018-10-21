import generic_lexer
from rules import token_expressions


def lexer(string):
    return generic_lexer.lexer(string, token_expressions)
