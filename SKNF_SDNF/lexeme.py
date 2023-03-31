class Lexeme():
    lex = None
    child_left = None
    child_right = None
    parent = None
    value = None

    def set_expression(self, tokens):
        if len(tokens) <= 4:
            if tokens[0] == ')' or tokens[0] == '(':
                tokens.pop(0)
            elif tokens[-1] == ')' or tokens[-1] == '(':
                tokens.pop(-1)
        self.expression = tokens

    def clac(self):
        pass


class Not(Lexeme):
    def calc(self):
        self.value = not self.child_left.calc()
        return self.value

class And(Lexeme):
    def calc(self):
        self.value = self.child_left.calc() and self.child_right.calc()
        return self.value

class Or(Lexeme):
    def calc(self):
        self.value = self.child_left.calc() or self.child_right.calc()
        return self.value

class Var(Lexeme):
    value = None

    def set_value(self, val):
        self.value = val

    def calc(self):
        return self.value