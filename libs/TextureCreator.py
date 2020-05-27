from threading import *
import pygame
import time


class TextureCreator(Thread):
    def __init__(self, world, ores, w, h, textures):
        Thread.__init__(self)

        self.world = world
        self.ores = ores
        self.w = w
        self.h = h
        self.textures = textures

        self.done = False

        self.texture = pygame.Surface((w * 16, h * 16))

    def run(self):
        s = time.time()

        for x in range(self.w):
            for y in range(self.h):
                pygame.draw.rect(self.texture, self.world[x, y][1], (x * 16, y * 16, 16, 16))
                if self.ores[x, y] != 'empty':
                    t = self.textures.getTexture(self.ores[x, y])
                    self.texture.blit(t, t.get_rect(topleft=(x * 16, y * 16)))

        e = time.time()

        print('Texture generated in', e - s, 'seconds')

        self.done = True

    def isDone(self):
        return self.done

    def getTexture(self):
        return self.texture
