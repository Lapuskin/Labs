from animals import Lion
from places import Place


class Plain:
    grid = []
    steppes_size = 5

    def step(self):
        for row in range(self.steppes_size):
            self.grid.append([])
            for column in range(self.steppes_size):
                self.grid[row].append(Place(row, column))

        Lion1 = Lion(1, 2)
        self.add(Lion1)

        for x in range(self.steppes_size):
            print(self.grid[x][0], ' ', self.grid[x][1], ' ', self.grid[x][2], ' ', self.grid[x][3], ' ',
                  self.grid[x][4], ' ')

        self.live(Lion1)
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
            if self.grid[step[0]][step[1]].occupied == False:
                self.grid[step[0]][step[1]].is_occupied(animal)
            else:
                self.grid[def_x][def_y].is_occupied(animal)
        else:
            self.grid[def_x][def_y].is_occupied(animal)

    def live(self, animal):
        self.animal_walk(animal)
        animal.is_hungry()

    def add(self, essence):
        self.grid[essence.x][essence.y].is_occupied(essence)
