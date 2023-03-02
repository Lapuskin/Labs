from animals import Lion, Zebra
from places import Place


class Plain:
    grid = []
    steppes_size = 5
    essensials = []

    def start(self):
        for row in range(self.steppes_size):
            self.grid.append([])
            for column in range(self.steppes_size):
                self.grid[row].append(Place(row, column))

        Lion1 = Lion(1, 2)
        self.add(Lion1)
        self.essensials.append(Lion1)
        Zebra1 = Zebra(1, 3)
        self.add(Zebra1)
        self.essensials.append(Zebra1)
        Lion2 = Lion()
        self.add(Lion2)
        self.essensials.append(Lion2)

        for x in range(self.steppes_size):
            print(self.grid[x][0], ' ', self.grid[x][1], ' ', self.grid[x][2], ' ', self.grid[x][3], ' ',
                  self.grid[x][4], ' ')
        self.step()

    def step(self):
        self.live(self.essensials[0])
        self.live(self.essensials[1])
        self.live(self.essensials[2])
        print('----------------------------------------------------------')
        for x in range(self.steppes_size):
            print(self.grid[x][0], ' ', self.grid[x][1], ' ', self.grid[x][2], ' ', self.grid[x][3], ' ',
                  self.grid[x][4], ' ')

    def animal_walk(self, animal):
        def_x = animal.x
        def_y = animal.y
        self.grid[animal.x][animal.y].occupied = False
        self.grid[animal.x][animal.y].target = None
        step = animal.walk()
        if step[0] in range(0, self.steppes_size - 1) and step[1] in range(0, self.steppes_size - 1):
            if not self.grid[step[0]][step[1]].occupied:
                self.grid[step[0]][step[1]].is_occupied(animal)
                animal.x = step[0]
                animal.y = step[1]
            else:
                self.grid[def_x][def_y].is_occupied(animal)
                animal.x = def_x
                animal.y = def_y
        else:
            self.grid[def_x][def_y].is_occupied(animal)
            animal.x = def_x
            animal.y = def_y

    def live(self, animal):
        def_x = animal.x
        def_y = animal.y + 1
        if self.grid[animal.x][animal.y].occupied == False:
            del animal
        else:
            animal.is_hungry()
            if def_x in range(self.steppes_size) and def_y in range(0, self.steppes_size-1):
                if self.grid[animal.x][animal.y + 1].occupied == True:
                    animal.eat(self.grid[animal.x][animal.y + 1].target)
                    if self.grid[animal.x][animal.y + 1].target.hp <= 0:
                        self.grid[animal.x][animal.y + 1].target = None
                        self.grid[animal.x][animal.y + 1].occupied = False
            self.animal_walk(animal)

    def add(self, essence):
        self.grid[essence.x][essence.y].is_occupied(essence)
