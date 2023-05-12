import re
from lexeme import Or, And, Not, Var


class Tree:
    def __init__(self, expression):
        self.expression = expression
        self.tokens = re.findall(r'\d+|[()+*!]|[A-Z]', expression)

    values = {}
    priority = ['!', '+', '*']
    root = None
    variables = []
    operations = []
    variable_number = 0

    def build(self):
        self.root = self.find_inflection_point(self.tokens, None)

    def find_inflection_point(self, tokens, parent):
        if not tokens:
            return None
        if tokens[-1] == ')' and tokens[0] == '(':
            tokens.pop(-1)
            tokens.pop(0)
        self_priority = 0
        max_priority = 0
        inflection_place = 0
        offset = 0
        for i in range(0, len(tokens) - 1):
            if tokens[i] == '(':
                offset -= 3
                self_priority = 0
            elif tokens[i] == ')':
                offset += 3
                self_priority = 0
            elif tokens[i] in self.priority:
                self_priority = self.priority.index(tokens[i]) + offset + 1
            else:
                self_priority = 0
            if self_priority >= max_priority:
                max_priority = self_priority
                inflection_place = i

        if tokens[inflection_place] == '*':
            lexeme = And()
        elif tokens[inflection_place] == '+':
            lexeme = Or()
        elif tokens[inflection_place] == '!':
            lexeme = Not()
        else:
            lexeme = Var()
            lexeme.set_expression(tokens)
            for var in self.variables:
                if lexeme.expression == var.expression:
                    self.variables.append(lexeme)
                    return lexeme
            self.values[tokens[0]] = None
            self.variables.append(lexeme)
            return lexeme

        lexeme.set_expression(tokens)
        self.operations.append(lexeme)
        lexeme.parent = parent
        left_lexeme = tokens[:inflection_place]
        right_lexeme = tokens[inflection_place + 1:]
        lexeme.child_left = self.find_inflection_point(left_lexeme, lexeme)
        lexeme.child_right = self.find_inflection_point(right_lexeme, lexeme)
        return lexeme

    def calc(self):
        for var in self.variables:
            value = self.values[var.expression[0]]
            var.set_value(value)
        return self.root.calc()