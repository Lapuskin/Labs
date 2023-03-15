from animals import Lion, Zebra
from places import Place
from plants import Plant
from serializers import Serializer


class Plain:
    grid = []
    steppes_size = 5
    essensials = []
    plants = []
    serializer = Serializer()

    def init(self):
        for row in range(self.steppes_size):
            self.grid.append([])
            for column in range(self.steppes_size):
                self.grid[row].append(Place(row, column))

    def start(self):
        self.init()
        self.print()
        print('----------------------------------------------------------')
        self.serializer.serialize(self)

    def step(self):
        self.init()
        self.serializer.deserialize(self)
        for es in self.essensials:
            self.live(es)
        for es in self.plants:
            self.live(es)
        self.print()
        self.serializer.serialize(self)

    def animal_walk(self, animal):
        if type(animal).__name__ != 'Plant':
            print(type(animal).__name__, animal.x, animal.y)
            def_x = animal.x
            def_y = animal.y
            self.grid[animal.x][animal.y].occupied = False
            self.grid[animal.x][animal.y].target = None
            step = animal.walk()
            if step[0] in range(0, self.steppes_size - 1) and step[1] in range(0, self.steppes_size - 1):
                if not self.grid[step[0]][step[1]].occupied:
                    self.grid[step[0]][step[1]].is_occupied(animal)
                    print("move to", step[0], step[1])
                    animal.x = step[0]
                    animal.y = step[1]
                else:
                    self.grid[def_x][def_y].is_occupied(animal)
                    animal.x = def_x
                    animal.y = def_y
                    print("don't move")
            else:
                self.grid[def_x][def_y].is_occupied(animal)
                animal.x = def_x
                animal.y = def_y
                print("don't move")
            print("and try to eat")

    def live(self, animal):
        def_x = animal.x
        def_y = animal.y + 1
        animal.aging()
        if type(animal).__name__ != "Plant":
            animal.is_hungry()
            if animal.hp <= 0:
                self.grid[animal.x][animal.y].occupied = False
                self.grid[animal.x][animal.y].target = None
                self.essensials.remove(animal)
        elif animal.hp <= 0:
                self.grid[animal.x][animal.y].occupied = False
                self.grid[animal.x][animal.y].target = None
                self.plants.remove(animal)
        if not self.grid[animal.x][animal.y].occupied:
            del animal
        else:
            if def_x in range(self.steppes_size) and def_y in range(0, self.steppes_size - 1):
                if self.grid[animal.x][animal.y + 1].occupied == True and type(animal).__name__ != "Plant":
                    animal.eat(self.grid[animal.x][animal.y + 1].target)
                    if self.grid[animal.x][animal.y + 1].target.hp <= 0:
                        self.grid[animal.x][animal.y + 1].target = None
                        self.grid[animal.x][animal.y + 1].occupied = False
            self.animal_walk(animal)

    def add(self, essence, x, y):
        self.init()
        self.serializer.deserialize(self)
        if essence == 'Lion':
            es = Lion(x, y)
        elif essence == 'Zebra':
            es = Zebra(x, y)
        else:
            es = Plant(x, y)
        self.grid[x][y].is_occupied(es)
        self.print()
        if type(essence).__name__ == 'Plant':
            self.plants.append(es)
        else:
            self.essensials.append(es)
        self.serializer.serialize(self)


    def print(self):
        for x in range(self.steppes_size):
            print(self.grid[x][0], ' ', self.grid[x][1], ' ', self.grid[x][2], ' ', self.grid[x][3], ' ',
                  self.grid[x][4], ' ')
        print('----------------------------------------------------------')

    def remove(self, x, y):
        self.init()
        self.serializer.deserialize(self)
        if not self.grid[x][y].occupied:
            print('there is nothing')
        else:
            self.grid[x][y].occupied = False
            if type(self.grid[x][y].target).__name__ == 'Plant':
                self.plants.remove(self.grid[x][y].target)
            else:
                self.essensials.remove(self.grid[x][y].target)
            self.grid[x][y].target = None
        self.print()
        self.serializer.serialize(self)
