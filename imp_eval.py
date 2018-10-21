#!/usr/bin/env python

import sys
from imp_parser import imp_parse
from imp_lexer import lexer

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: imp filename\n')
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename) as imp_file:
        tokens = lexer(imp_file.read())

    parse_result = imp_parse(tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)

    env = {}
    ast = parse_result.value
    ast.eval(env)

    sys.stdout.write('Final variable values: \n')
    for name in env:
        sys.stdout.write(f'{name}: {env[name]}\n')
