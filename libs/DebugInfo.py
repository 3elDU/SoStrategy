from libs.Constants import *
import pygame


class Main:
    def __init__(self, font, size):
        pygame.init()
        self.font = pygame.font.SysFont(font, size)

    @staticmethod
    def __calculateDelta(prev, current):
        return current - prev

    def calculate(self, prevFrame, eTime, sTime, x, y, blockSize):
        surf = pygame.Surface((500, 100))
        surf.set_colorkey(BLACK)

        delta = self.__calculateDelta(prevFrame, eTime)

        t = self.font.render(str(1 // (eTime - sTime)) + '   ' + str(x) + '  ' + str(y),
                             True,
                             WHITE)

        surf.blit(t, t.get_rect(topleft=(50, 0)))

        d = self.font.render(str(delta), True, WHITE)

        surf.blit(d, d.get_rect(topleft=(50, 30)))

        s = self.font.render(str(blockSize), True, WHITE)

        surf.blit(s, s.get_rect(topleft=(50, 60)))

        return surf
