class Parser:
    def __call__(self, tokens, position):
        return None

    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, func):
        return Process(self, func)


class Concat(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, position):
        left_result = self.left(tokens, position)
        if not left_result:
            return

        right_result = self.right(tokens, left_result.position)
        if not right_result:
            return

        combined_value = (left_result.value, right_result.value)
        return Result(combined_value, right_result.position)


class Exp(Parser):
    def __init__(self, stmt_parser, separator_parser):
        self.stmt_parser = stmt_parser
        self.separator_parser = separator_parser

    def __call__(self, tokens, position):
        result = self.stmt_parser(tokens, position)

        def process_next(parsed_value):
            separator_func, right = parsed_value
            return separator_func(result.value, right)

        next_parser = self.separator_parser + self.stmt_parser ^ process_next

        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.position)
            if next_result:
                result = next_result

        return result


class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, position):
        return self.left(tokens, position) or self.right(tokens, position)


class Process(Parser):
    def __init__(self, parser, func):
        self.parser = parser
        self.func = func

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        if not result:
            return
        result.value = self.func(result.value)
        return result


class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, position):
        if position < len(tokens) and tokens[position][0] == self.value and tokens[position][1] is self.tag:
            return Result(tokens[position][0], position + 1)


class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, position):
        if position < len(tokens) and tokens[position][1] is self.tag:
            return Result(tokens[position][0], position + 1)


class Optional(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, position):
        return self.parser(tokens, position) or Result(None, position)


class Repeated(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, position):
        result_values = []
        result = self.parser(tokens, position)
        while result:
            result_values.append(result.value)
            position = result.position
            result = self.parser(tokens, position)
        return Result(result_values, position)


class Lazy(Parser):
    def __init__(self, create_parser):
        self.parser = None
        self.create_parser = create_parser

    def __call__(self, tokens, position):
        if not self.parser:
            self.parser = self.create_parser()
        return self.parser(tokens, position)


class Phrase(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        if result and result.position == len(tokens):
            return result


class Result:
    def __init__(self, value, position):
        self.value = value
        self.position = position

    def __str__(self):
        return f'Result({self.value}, {self.position})'
