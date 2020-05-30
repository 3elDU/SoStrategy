from libs.gui import UIButton
import pygame


class Menu:
    def __init__(self, sc, w, h):
        pygame.init()

        self.sc = sc
        self.w = w
        self.h = h

        self.backGround = pygame.image.load('textures/pauseMenu.png')
        self.backGround = self.backGround.convert_alpha()
        self.backGround = pygame.transform.scale(self.backGround, (self.w, self.h))

        self.backGroundRect = self.backGround.get_rect()

        self.buttonX = pygame.display.get_surface().get_width() // 2
        self.buttonY = pygame.display.get_surface().get_height() // 2

        self.mode1 = UIButton.Button('renderingMode1', self.buttonX - 200 - 240, self.buttonY * 1.1,
                                     pathToTexture='textures/', width=240, height=60)

        self.mode2 = UIButton.Button('renderingMode2', self.buttonX + 200, self.buttonY * 1.1,
                                     pathToTexture='textures/', width=240, height=60)

        self.result = 0
        self.alive = True

        self.loop()

    def getResult(self):
        return self.result

    def loop(self):
        while self.alive:
            pos = pygame.mouse.get_pos()
            self.mode1.tick(pos[0], pos[1])
            self.mode2.tick(pos[0], pos[1])

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.alive = False
                    self.result = 0
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.alive = False
                        self.result = 1
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        clicked1 = self.mode1.isClicked(e.pos[0], e.pos[1])
                        clicked2 = self.mode2.isClicked(e.pos[0], e.pos[1])
                        if clicked1:
                            self.alive = False
                            self.result = 2
                        elif clicked2:
                            self.alive = False
                            self.result = 1

            self.sc.blit(self.backGround, self.backGroundRect)

            texture = self.mode1.getButton()
            self.sc.blit(texture, texture.get_rect(topleft=(self.buttonX - 200 - 240, self.buttonY * 1.1)))

            texture1 = self.mode2.getButton()
            self.sc.blit(texture1, texture1.get_rect(topleft=(self.buttonX + 200, self.buttonY * 1.1)))

            pygame.display.update()
