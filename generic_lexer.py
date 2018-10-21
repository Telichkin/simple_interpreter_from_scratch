import re
import sys


def lexer(a_string, token_expressions):
    position = 0
    tokens = []
    while position < len(a_string):
        match = None
        for expression in token_expressions:
            pattern, tag = expression
            regex = re.compile(pattern)
            match = regex.match(a_string, position)
            if match:
                if tag:
                    token = (match.group(0), tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write(f'Illegal character: {a_string[position]}')
            sys.exit(1)
        else:
            position = match.end(0)
    return tokens
