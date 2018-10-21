from functools import reduce

from rules import RESERVED, INT, ID
from generic_parser import Reserved, Tag, Lazy, Optional, Phrase
from imp_ast import Int, Var, BinaryOperation, Relational, Not, And, Or, Assign, Compound, If, While, Repeat


def to_int(a_string): return int(a_string)


def keyword(a_string): return Reserved(a_string, RESERVED)


(id, number) = (Tag(ID), Tag(INT) ^ to_int)


def imp_parse(tokens):
    ast = parser()(tokens, 0)
    return ast


def parser():
    return Phrase(statement_list())


def statement_list():
    separator = keyword(';') ^ (lambda _: lambda left, right: Compound(left, right))
    return statement() * separator


def statement():
    return (
        assign_statement() |
        if_statement() |
        while_statement() |
        repeat_statement()
    )


def assign_statement():
    def process(parsed_result):
        ((name, _), expression) = parsed_result
        return Assign(name, expression)

    return id + keyword(':=') + arithmetic_expression() ^ process


def if_statement():
    def process(parsed_result):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed_result
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return If(condition, true_stmt, false_stmt)

    return (
        keyword('if') + boolean_expression() +
        keyword('then') + Lazy(statement_list) +
        Optional(keyword('else') + Lazy(statement_list)) +
        keyword('end') ^ process
    )


def while_statement():
    def process(parsed_result):
        ((((_, condition), _), body), _) = parsed_result
        return While(condition, body)

    return (
        keyword('while') + boolean_expression() +
        keyword('do') + Lazy(statement_list) +
        keyword('end') ^ process
    )


def repeat_statement():
    def process(parsed_result):
        ((((_, repeat_times), _), body), _) = parsed_result
        return Repeat(repeat_times, body)

    return (
        keyword('repeat') + number +
        keyword('times') + Lazy(statement_list) +
        keyword('end') ^ process
    )


def arithmetic_expression_value():
    return (
        (number ^ (lambda n: Int(n))) |
        (id ^ (lambda i: Var(i)))
    )


def only_expression_inside_parenthesis(parsed_result):
    ((_, expr), _) = parsed_result
    return expr


def arithmetic_expression_in_parenthesis():
    return keyword('(') + Lazy(arithmetic_expression) + keyword(')') ^ only_expression_inside_parenthesis


def arithmetic_expression_term():
    return arithmetic_expression_value() | arithmetic_expression_in_parenthesis()


def process_binary_operation(operation):
    return lambda left, right: BinaryOperation(operation, left, right)


def any_operator_in_list(operations):
    operation_parsers = [keyword(o) for o in operations]
    return reduce(lambda l, r: l | r, operation_parsers)


def precedence(value_parser, precedence_levels, combine):
    def operation_parser(lvl):
        return any_operator_in_list(lvl) ^ combine

    for precedence_level in precedence_levels:
        value_parser = value_parser * operation_parser(precedence_level)

    return value_parser


def arithmetic_expression():
    return precedence(
        arithmetic_expression_term(),
        [['*', '/'], ['+', '-']],
        process_binary_operation
    )


def process_relational(parsed_result):
    ((left, operation), right) = parsed_result
    return Relational(operation, left, right)


def boolean_expression_binary_operation():
    operators = ['<', '<=', '>', '>=', '=', '!=']
    return arithmetic_expression() + any_operator_in_list(operators) + arithmetic_expression() ^ process_relational


def boolean_expression_not():
    return keyword('not') + Lazy(boolean_expression_term) ^ (lambda parsed: Not(parsed[1]))


def boolean_expression_in_parenthesis():
    return keyword('(') + Lazy(boolean_expression) + keyword(')') ^ only_expression_inside_parenthesis


def boolean_expression_term():
    return (
        boolean_expression_not() |
        boolean_expression_binary_operation() |
        boolean_expression_in_parenthesis()
    )


def process_logic(operator):
    if operator == 'and':
        return lambda left, right: And(left, right)
    if operator == 'or':
        return lambda left, right: Or(left, right)
    raise RuntimeError('Unknown logic operator: ' + operator)


def boolean_expression():
    return precedence(
        boolean_expression_term(),
        [['and'], ['or']],
        process_logic,
    )


