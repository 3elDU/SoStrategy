from libs import Functions
from libs.Constants import *
import noise
import time
import random


class Noise:
    def __init__(self):
        self.functions = Functions.Functions()

        self.rawWorld = {}
        self.rawOres = {}

        self.world = {}
        self.ores = {}

    @staticmethod
    def perlin(x, y):
        return noise.pnoise2(x, y)

    def generateWorld(self, w, h, multiplier, px, py):
        s = time.time()

        for x in range(w):
            for y in range(h):
                if x == 0 or x == w-1 or y == 0 or y == h-1:
                    self.rawWorld[x, y] = 'border'
                else:
                    xpos = x * multiplier + px
                    ypos = y * multiplier + py

                    n = abs(self.perlin(xpos, ypos) * 255)
                    n = self.functions.clamp(n, 0, 255)

                    if n < 64:
                        self.rawWorld[x, y] = 'water'
                    elif 64 < n < 76:
                        self.rawWorld[x, y] = 'sand'
                    elif 76 < n < 128:
                        self.rawWorld[x, y] = 'land'
                    elif 128 < n < 150:
                        self.rawWorld[x, y] = 'mountains'
                    elif 150 < n <= 255:
                        self.rawWorld[x, y] = 'snow'
                    else:
                        self.rawWorld[x, y] = 'empty'

        for x1 in range(w):
            for y1 in range(h):
                rawBlock = self.rawWorld[x1, y1]

                block = []

                if rawBlock == 'border':
                    color1 = DARKGRAY
                elif rawBlock == 'water':
                    color1 = BLUE
                elif rawBlock == 'sand':
                    color1 = YELLOW
                elif rawBlock == 'land':
                    color1 = GREEN
                elif rawBlock == 'mountains':
                    color1 = GRAY
                elif rawBlock == 'snow':
                    color1 = WHITE
                elif rawBlock == 'empty':
                    color1 = BLACK

                """finalColor = []

                for clr in color1:
                    finalColor.append(self.functions.clamp(self.functions.noise(clr), 0, 255))"""

                block.append(rawBlock)
                block.append(color1)

                self.world[x1, y1] = block

        e = time.time()

        print('World generated in', e - s, ' seconds.')

    def generateOres(self, w, h, multiplier, px, py):
        s = time.time()

        oreStartX = px * random.randint(-15, 15)
        oreStartY = py * random.randint(-15, 15)

        for x in range(w):
            for y in range(h):
                if x == 0 or x == w-1 or y == 0 or y == h-1:
                    self.rawOres[x, y] = 'empty'
                else:
                    oreX = x * multiplier + oreStartX
                    oreY = y * multiplier + oreStartY

                    ore = int(abs(self.perlin(oreX, oreY) * 14))
                    ore = self.functions.clamp(ore, 0, 7)

                    chance = random.randrange(1, 100)

                    finalOre = 'empty'

                    if ore <= 1:
                        finalOre = 'empty'
                    elif 1 < ore <= 2:
                        if not self.rawWorld[x, y] == 'water':
                            if chance <= 50:
                                finalOre = 'coal'
                        else:
                            if chance <= 90:
                                finalOre = 'fish'
                    elif 2 < ore <= 4:
                        if self.rawWorld[x, y] == 'land':
                            if chance <= 80:
                                finalOre = 'wood'
                        elif self.rawWorld[x, y] in ['mountains', 'snow']:
                            if chance <= 50:
                                finalOre = 'iron'
                        else:
                            finalOre = 'empty'
                    elif 4 < ore < 6:
                        if self.rawWorld[x, y] == 'mountains':
                            if chance <= 20:
                                finalOre = 'gold'
                        else:
                            finalOre = 'empty'
                    elif 6 < ore <= 7:
                        if self.rawWorld[x, y] != 'water':
                            if chance < 5:
                                finalOre = 'diamond'
                    else:
                        finalOre = 'empty'

                    self.rawOres[x, y] = finalOre

        e = time.time()
        print('Ores generated in', e - s, 'seconds.')

    def get(self):
        return self.world, self.rawOres
