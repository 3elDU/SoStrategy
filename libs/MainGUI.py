from libs.Constants import *
import pygame


class Main:
    sc: pygame.Surface

    def __init__(self, w, h):
        pygame.init()

        self.w, self.h = w, h

        self.sc = pygame.Surface((w, h))
        self.sc.fill(BG_COLOR)
        self.sc.set_colorkey(BG_COLOR)

        self.font = pygame.font.SysFont('arial', 36)

    def updateData(self, x, y):
        self.sc.fill(BG_COLOR)

        xtext = self.font.render(str(x), True, WHITE)
        ytext = self.font.render(str(y), True, WHITE)

        self.sc.blit(xtext, xtext.get_rect(topleft=(0, 0)))
        self.sc.blit(ytext, ytext.get_rect(topleft=(0, 50)))

    def getSurf(self):
        return self.sc
