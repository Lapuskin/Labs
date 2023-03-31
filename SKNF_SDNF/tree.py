import re
from lexeme import Or, And, Not, Var


class Tree:
    def __init__(self, expression):
        self.tokens = re.findall(r'\d+|[()+*!]|[A-Z]', expression)

    priority = ['!', '+', '*']
    root = None
    variables = []

    def build(self):
        self.root = self.find_inflection_point(self.tokens, None)
        print('end')

    def find_inflection_point(self, tokens, parent):
        if not tokens:
            return None
        self_priority = 0
        max_priority = 0
        inflection_place = 0
        offset = 0
        for i in range(0, len(tokens) - 1):
            if tokens[i] == '(':
                offset -= 1
                self_priority = 0
            elif tokens[i] == ')':
                offset += 1
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
            self.variables.append(lexeme)
            return lexeme
        lexeme.parent = parent
        left_lexeme = tokens[:inflection_place]
        right_lexeme = tokens[inflection_place + 1:]
        lexeme.child_left = self.find_inflection_point(left_lexeme, lexeme)
        lexeme.child_right = self.find_inflection_point(right_lexeme, lexeme)
        return lexeme

    def calc(self):
        return self.root.calc()
