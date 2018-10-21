class Equality:
    def __eq__(self, other):
        if type(other) is type(self):
            return other.__dict__ == self.__dict__
        return False


class ArithmeticExpression(Equality):
    pass


class Int(ArithmeticExpression):
    def __init__(self, i):
        self.i = i

    def eval(self, _):
        return self.i

    def __repr__(self):
        return f'Int({self.i})'


class Var(ArithmeticExpression):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env.get(self.name, 0)

    def __repr__(self):
        return f'Var({self.name})'


class BinaryOperation(ArithmeticExpression):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def eval(self, env):
        left, right = (self.left.eval(env), self.right.eval(env))
        value = {'+': lambda: left + right,
                 '-': lambda: left - right,
                 '*': lambda: left * right,
                 '/': lambda: left / right}[self.operator]

        if not value:
            raise RuntimeError('Unknown operator: ' + self.operator)
        return value()

    def __repr__(self):
        return f'BinaryOperation({self.operation}, {self.left}, {self.right})'


class BooleanExpression(Equality):
    pass


class Relational(BooleanExpression):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def eval(self, env):
        left, right = (self.left.eval(env), self.right.eval(env))
        value = {'<': lambda: left < right,
                 '<=': lambda: left <= right,
                 '>': lambda: left > right,
                 '>=': lambda: left >= right,
                 '=': lambda: left == right,
                 '!=': lambda: left != right}[self.operator]

        if not value:
            raise RuntimeError('Unknown operator: ' + self.operator)
        return value()

    def __repr__(self):
        return f'RelationalExpression({self.operation}, {self.left}, {self.right})'


class And(BooleanExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) and self.right.eval(env)

    def __repr__(self):
        return f'And({self.left}, {self.right})'


class Or(BooleanExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) or self.right.eval(env)

    def __repr__(self):
        return f'Or({self.left}, {self.right})'


class Not(BooleanExpression):
    def __init__(self, expression):
        self.expression = expression

    def eval(self, env):
        return not self.expression.eval(env)

    def __repr__(self):
        return f'Not({self.expression})'


class Statement(Equality):
    pass


class Assign(Statement):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def eval(self, env):
        env[self.name] = self.expression.eval(env)

    def __repr__(self):
        return f'Assign({self.name}, {self.expression})'


class Compound(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

    def __repr__(self):
        return f'Compound({self.first}, {self.second})'


class If(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def eval(self, env):
        condition = self.condition.eval(env)
        if condition:
            self.true_stmt.eval(env)
        elif self.false_stmt:
            self.false_stmt.eval(env)

    def __repr__(self):
        return f'If({self.condition}, {self.true_stmt}, {self.false_stmt})'


class While(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        while self.condition.eval(env):
            self.body.eval(env)

    def __repr__(self):
        return f'While({self.condition}, {self.body})'


class Repeat(Statement):
    def __init__(self, repeat_times, body):
        self.times = repeat_times
        self.body = body

    def eval(self, env):
        for _ in range(self.times):
            self.body.eval(env)

    def __repr__(self):
        return f'Repeat({self.times}, {self.body})'
