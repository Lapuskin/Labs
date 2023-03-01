class Place:
    def __init__(self, x, y):
        self.target = None
        self.occupied = False
        self.x = x
        self.y = y

    def is_occupied(self, target):
        self.target = target
        self.occupied = True

    def walk(self):
        self.occupied = False
        ret = self.target.walk
        self.target = None
        return ret

    def __str__(self):
        coordinates = f"| x: {self.x}, y:{self.y} "
        if self.occupied:
            return "| " + type(self.target).__name__.upper() + " |"
        else:
            return "|" + "      " + "|"

