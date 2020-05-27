from threading import *
import pygame
import random


PARTICLES = 0


class Particle(pygame.sprite.Sprite):
    rect: pygame.Rect

    def __init__(self, x, y, size, texture, rotation, sw, sh, speed, direction, group):
        pygame.sprite.Sprite.__init__(self)
        self.add(group)

        self.x, self.y = x, y
        self.size = size
        self.sw, self.sh = sw, sh
        self.speed = speed
        self.direction = direction

        self.image = texture
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.rotation = rotation

    def update(self):
        global PARTICLES

        if self.direction == 0:
            self.x -= random.randint(0, 3)
        elif self.direction == 1:
            self.x += random.randint(0, 3)

        self.y -= self.speed

        # self.rotation += random.randint(-2, 2)

        """if self.rotation < 0 or self.rotation > 180:
            self.rotation = 90

        self.image = pygame.transform.rotate(self.image, self.rotation)"""

        self.rect.centerx = self.x
        self.rect.centery = self.y

        x = self.rect.centerx
        y = self.rect.centery

        if x < 0 or x > self.sw or\
           y < 0 or y > self.sh:
            PARTICLES -= 1
            self.kill()


class Main(Thread):
    def __init__(self, width, height, backgroundTexture, particleCount, particleTexture, particleSize):
        Thread.__init__(self)
        pygame.init()

        self.width, self.height = width, height

        self.backgroundTexture = pygame.image.load(backgroundTexture)
        self.backgroundTexture = self.backgroundTexture.convert_alpha()
        self.backgroundTexture = pygame.transform.scale(self.backgroundTexture,
                                                        (self.width, self.height))
        self.backgroundRect = self.backgroundTexture.get_rect()

        self.particleCount = particleCount
        self.particleSize = particleSize

        self.particleTexture = pygame.image.load(particleTexture)
        self.particleTexture = self.particleTexture.convert_alpha()
        self.particleTexture = pygame.transform.scale(self.particleTexture,
                                                      (self.particleSize, self.particleSize))

        self.particleRect = self.particleTexture.get_rect()

        self.surface = pygame.Surface((self.width, self.height))
        self.goodSurf = self.surface.copy()

        self.alive = True
        self.toRender = True

        self.group = pygame.sprite.Group()

    def getSurface(self):
        return self.goodSurf

    def render(self):
        self.toRender = True

    def stop(self):
        self.alive = False

    def run(self):
        global PARTICLES

        while self.alive:
            if self.toRender:
                self.surface.blit(self.backgroundTexture, self.backgroundRect)
                self.group.update()

                if PARTICLES < self.particleCount:
                    Particle(random.randint(50, self.width-50),
                             self.height,
                             self.particleSize,
                             self.particleTexture,
                             random.randint(0, 180),
                             self.width, self.height,
                             random.randint(3, 20),
                             random.randint(0, 1),
                             self.group)

                    PARTICLES += 1

                self.group.draw(self.surface)

                self.goodSurf = self.surface.copy()

                self.toRender = False

        exit()
