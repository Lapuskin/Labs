class Plant:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    fresh = 7
    hp = 1

    def is_hurt(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(type(self).__name__, ' ', self.x, ' ', self.y, 'was eaten')
            del self

    def aging(self):
        self.fresh -= 1
        if self.fresh <= 0:
            self.hp = self.fresh
            print(type(self).__name__, ' ', self.x, ' ', self.y, 'is gone')
            del self