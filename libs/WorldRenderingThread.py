from threading import *
import pygame


class Main(Thread):
    def __init__(self, world, x, y, size, mgr, creator):
        pygame.init()
        Thread.__init__(self)

        self.world = world
        self.prevBlocks = {}

        self.x = x
        self.y = y
        self.blockSize = size
        self.creator = creator

        self.mgr = mgr

        self.mapSurf = pygame.Surface((66 * self.blockSize, 34 * self.blockSize))
        self.goodSurf = self.mapSurf.copy()
        self.border = pygame.transform.scale(self.mgr.getTexture('border'), (66 * self.blockSize, 34 * self.blockSize))
        self.mapSurf.blit(self.border, self.border.get_rect())

        self.alive = True
        self.toRender = True
        self.done = False

    def updateData(self, newMap, newX, newY, newSize):
        self.world = newMap
        self.x = newX
        self.y = newY
        self.blockSize = newSize

    def getSurf(self):
        return self.goodSurf

    def resize(self):
        self.mapSurf = pygame.transform.scale(self.mapSurf, (66 * self.blockSize, 34 * self.blockSize))
        self.wholeMapSurf = self.creator.getTexture()
        self.wholeMapSurf = pygame.transform.scale(self.wholeMapSurf, (256 * (self.blockSize // 4),
                                                                       128 * (self.blockSize // 4)))

        self.startX = pygame.display.get_surface().get_width() // 2 - (32 * self.blockSize)
        self.startY = pygame.display.get_surface().get_height() // 2 - (16 * self.blockSize)
        self.prevOres = {}

        self.border = pygame.transform.scale(self.mgr.getTexture('border'), (66 * self.blockSize, 34 * self.blockSize))
        self.mapSurf.blit(self.border, self.border.get_rect())

    def run(self):
        prevBlockSize = 16
        while self.alive:
            if True:
                if self.blockSize != prevBlockSize:
                    self.resize()

                self.render()

                prevBlockSize = self.blockSize

                self.goodSurf = self.mapSurf.copy()

                self.toRender = False

        exit()

    def work(self):
        self.toRender = True

    def stop(self):
        self.alive = False

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
