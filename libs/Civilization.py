import random


class Civ:
    def __init__(self, world, buildings, ores):
        self.world = world
        self.buildings = buildings
        self.ores = ores

        x = 0
        y = 0
        while not world[x, y][0] == 'land':
            x = random.randrange(1, 255)
            y = random.randrange(1, 127)

        self.x, self.y = x, y

        self.ores[self.x, self.y] = 'empty'

        self.buildings[self.x, self.y] = ['town_hall', 0]
