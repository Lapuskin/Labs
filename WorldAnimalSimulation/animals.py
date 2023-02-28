import random


class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    speed = 0
    hp = 1
    damage = 1
    max_hunger = 3
    hunger = 3

    def walk(self):
        moves = [(0, self.speed),
                 (0, -self.speed),
                 (self.speed, 0),
                 (-self.speed, 0)]
        step = moves[random.randint(0, 4)]
        self.x += step[0]
        self.y += step[1]

    def is_hurt(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(type(self), ' ', self.x, ' ', self.y, 'was eaten')
            del self

    def eat(self, prey, type_of_pray):
        if type(prey) is type_of_pray:
            prey.is_hurt(self.damage)
            self.hunger += 1

    def is_hungry(self):
        if self.hunger <= 0:
            self.hunger -= 1
        else:
            self.hp -= 1
            if self.hp <= 0:
                del self
                print(type(self), ' ', self.x, ' ', self.y, 'died of hunger')

    def aging(self):
        self.hp -= 1
        if self.hp <= 0:
            print(type(self), ' ', self.x, ' ', self.y, 'died of aging')
            del self

    def reproduce(self, target):
        if type(self) == type(target) & self.hunger == self.max_hunger:
            pass
