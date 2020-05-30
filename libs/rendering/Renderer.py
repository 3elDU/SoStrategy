import pygame
from libs.Constants import *


class RenderingMode2:
    def __init__(self, w, h, mgr):
        self.w, self.h = w, h
        self.mgr = mgr

        self.blockSize = 16


class RenderingMode1:
    def __init__(self, x, y, world, buildings, ores, w, h, mgr, creator, rescaler):
        self.rescaler = rescaler
        self.x, self.y = x, y
        self.world = world
        self.buildings = buildings
        self.ores = ores
        self.w, self.h = w, h
        self.mgr = mgr
        self.creator = creator

        self.blockSize = 16
        self.showingOres = False
        self.showingBuildings = True

        self.prevBlocks = {}
        self.prevOres = {}

        self.mapSurf = pygame.Surface((66 * self.blockSize, 34 * self.blockSize))
        self.border = pygame.transform.scale(self.mgr.getTexture('border'),
                                             (66 * self.blockSize, 34 * self.blockSize))
        self.mapSurf.blit(self.border, self.border.get_rect())
        self.wholeMapSurf = self.creator.getTexture()
        self.oresSurf = pygame.Surface((66 * self.blockSize, 34 * self.blockSize))
        self.oresSurf.fill(BG_COLOR)
        self.oresSurf.set_colorkey((1, 1, 1))
        self.buildingsSurf = pygame.Surface((66 * self.blockSize, 34 * self.blockSize))
        self.buildingsSurf.fill(BG_COLOR)
        self.buildingsSurf.set_colorkey(BG_COLOR)

    def updateData(self, newx, newy, newBlockSize, showingOres, showingBuildings, world, ores):
        self.x = newx
        self.y = newy
        if newBlockSize != self.blockSize:
            self.blockSize = newBlockSize
            self.resize()
        self.showingOres = showingOres
        self.showingBuildings = showingBuildings
        self.world = world
        self.ores = ores

    def renderAll(self):
        self.render()
        if self.showingOres:
            self.renderOres()
        if self.showingBuildings:
            self.renderBuildings()

    def getSurf(self):
        toreturn = {"map": self.mapSurf}
        if self.showingOres:
            toreturn['ores'] = self.oresSurf
        if self.showingBuildings:
            toreturn['buildings'] = self.buildingsSurf
        return toreturn

    def renderBuildings(self):
        self.buildingsSurf.fill(BG_COLOR)

        for x in range(64):
            for y in range(32):
                xcord = x + self.x
                ycord = y + self.y

                if (xcord, ycord) in self.buildings:
                    building = self.buildings[xcord, ycord]

                    texture = self.rescaler.getTexture(building[0], self.blockSize, self.blockSize)
                    rect = texture.get_rect(topleft=((x + 1) * self.blockSize, (y + 1) * self.blockSize))

                    self.buildingsSurf.blit(texture, rect)

    def render(self):
        for x in range(64):
            for y in range(32):
                xcord = self.x + x
                ycord = self.y + y

                if 0 <= xcord <= 255 and 0 <= ycord <= 127:
                    block = self.world[xcord, ycord]

                    if self.prevBlocks.__contains__((x, y)):
                        if self.prevBlocks[x, y] != block[1]:
                            pygame.draw.rect(self.mapSurf, block[1],
                                             ((x + 1) * self.blockSize, (y + 1) * self.blockSize,
                                              self.blockSize, self.blockSize))
                            self.prevBlocks[x, y] = block[1]
                    else:
                        pygame.draw.rect(self.mapSurf, block[1], ((x + 1) * self.blockSize, (y + 1) * self.blockSize,
                                                                  self.blockSize, self.blockSize))
                        self.prevBlocks[x, y] = block[1]

    def renderOres(self):
        b = self.blockSize

        for x in range(64):
            for y in range(32):
                xcord = self.x + x
                ycord = self.y + y

                ore = self.ores[xcord, ycord]

                if (x, y) in self.prevOres:
                    if self.prevOres[x, y] != ore:
                        pygame.draw.rect(self.oresSurf, (1, 1, 1), (b + x * self.blockSize,
                                                                    b + y * self.blockSize,
                                                                    self.blockSize,
                                                                    self.blockSize))

                        if ore != 'empty':
                            texture = self.rescaler.getTexture(ore, self.blockSize, self.blockSize)
                            textureRect = texture.get_rect(topleft=(b + x * self.blockSize,
                                                                    b + y * self.blockSize))

                            self.oresSurf.blit(texture, textureRect)

                        self.prevOres[x, y] = ore
                else:
                    pygame.draw.rect(self.oresSurf, (1, 1, 1), (b + x * self.blockSize,
                                                                b + y * self.blockSize,
                                                                self.blockSize,
                                                                self.blockSize))

                    if ore != 'empty':
                        texture = self.rescaler.getTexture(ore, self.blockSize, self.blockSize)
                        textureRect = texture.get_rect(topleft=(b + x * self.blockSize,
                                                                b + y * self.blockSize))

                        self.oresSurf.blit(texture, textureRect)

                    self.prevOres[x, y] = ore

    def resize(self):
        self.mapSurf = pygame.transform.scale(self.mapSurf, (66 * self.blockSize, 34 * self.blockSize))
        self.oresSurf = pygame.transform.scale(self.oresSurf, (66 * self.blockSize, 34 * self.blockSize))
        self.buildingsSurf = pygame.transform.scale(self.buildingsSurf, (66 * self.blockSize, 34 * self.blockSize))
        self.wholeMapSurf = self.creator.getTexture()
        self.wholeMapSurf = pygame.transform.scale(self.wholeMapSurf, (256 * (self.blockSize // 4),
                                                                       128 * (self.blockSize // 4)))

        self.startX = pygame.display.get_surface().get_width() // 2 - (32 * self.blockSize)
        self.startY = pygame.display.get_surface().get_height() // 2 - (16 * self.blockSize)
        self.prevOres = {}

        self.border = pygame.transform.scale(self.mgr.getTexture('border'), (66 * self.blockSize, 34 * self.blockSize))
        self.mapSurf.blit(self.border, self.border.get_rect())
