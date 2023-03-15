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
    type_of_pray = None

    def walk(self):
        moves = [(0, self.speed),
                 (0, -self.speed),
                 (self.speed, 0),
                 (-self.speed, 0)]
        step = moves[random.randint(0, 3)]
        return [self.x + step[0], self.y + step[1]]

    def is_hurt(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(type(self).__name__, ' ', self.x, ' ', self.y, 'was eaten')
            del self
        else: print(type(self).__name__, ' ', self.x, ' ', self.y, 'hurted')

    def eat(self, prey):
        if issubclass(type(prey), self.type_of_pray):
            prey.is_hurt(self.damage)
            if self.hunger <= self.max_hunger:
                self.hunger += 1
        else:
            print(self, type(prey), self.type_of_pray)

    def is_hungry(self):
        if self.hunger > 0:
            self.hunger -= 1
        else:
            self.hp -= 1
            if self.hp <= 0:
                print(type(self).__name__, ' ', self.x, ' ', self.y, 'died of hunger')
                return True
            return False

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
    max_hunger = 5
    hunger = 5
    type_of_pray = Plant


class Lion(Animal):
    speed = 1
    hp = 5
    damage = 2
    max_hunger = 3
    hunger = 3
    type_of_pray = Animal
