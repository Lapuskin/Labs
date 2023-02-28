class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    hp = 1

    def was_eaten(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(type(self), ' ', self.x, ' ', self.y, 'was eaten')
            del self
