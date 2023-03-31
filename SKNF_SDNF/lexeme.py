class Lexeme():
    lex = None
    child_left = None
    child_right = None
    parent = None

    def clac(self):
        pass


class Not(Lexeme):
    def calc(self):
        return not self.child_left.calc()


class And(Lexeme):
    def calc(self):
        return self.child_left.calc() and self.child_right.calc()


class Or(Lexeme):
    def calc(self):
        return self.child_left.calc() or self.child_right.calc()


class Var(Lexeme):
    value = None

    def set_value(self, val):
        self.value = val

    def calc(self):
        return self.value