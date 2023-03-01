import random

from plants import Plant


class Animal:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    speed = 0
    hp = 1
    damage = 1
    max_hunger = 3
    hunger = 3
    type_of_pray = 'Animal'

    def walk(self):
        moves = [(0, self.speed),
                 (0, -self.speed),
                 (self.speed, 0),
                 (-self.speed, 0)]
        step = moves[random.randint(0, 3)]
        self.x += step[0]
        self.y += step[1]
        return [self.x, self.y]

    def is_hurt(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(type(self).__name__, ' ', self.x, ' ', self.y, 'was eaten')
            del self

    def eat(self, prey):
        if type(prey).__name__ is self.type_of_pray:
            prey.is_hurt(self.damage)
            self.hunger += 1

    def is_hungry(self):
        if self.hunger > 0:
            self.hunger -= 1
        else:
            self.hp -= 1
            if self.hp <= 0:
                print(type(self).__name__, ' ', self.x, ' ', self.y, 'died of hunger')
                del self

    def aging(self):
        self.hp -= 1
        if self.hp <= 0:
            print(type(self).__name__, ' ', self.x, ' ', self.y, 'died of aging')
            del self

    def reproduce(self, target):
        if type(self).__name__ == type(target).__name__ & self.hunger == self.max_hunger:
            pass


class Zebra(Animal):
    speed = 2
    hp = 3
    damage = 1
    max_hunger = 3
    hunger = 3
    type_of_pray = type(Plant).__name__


class Lion(Animal):
    speed = 1
    hp = 5
    damage = 2
    max_hunger = 3
    hunger = 3
    type_of_pray = type(Animal).__name__
