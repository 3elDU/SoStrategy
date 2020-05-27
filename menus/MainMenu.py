from libs.gui import UIButton
import pygame


class Menu:
    def __init__(self, screen, w, h):
        pygame.init()

        self.sc = screen
        self.w, self.h = w, h

        self.backGround = pygame.image.load('textures/mainScreen.png')
        self.backGround = self.backGround.convert_alpha()
        self.backGround = pygame.transform.scale(self.backGround, (self.w, self.h))

        self.backGroundRect = self.backGround.get_rect()

        self.buttonX = pygame.display.get_surface().get_width() // 2
        self.buttonY = pygame.display.get_surface().get_height() // 2

        self.button = UIButton.Button('playButton', self.buttonX-120, int(self.buttonY * 1.25)-30,
                                      pathToTexture='textures/', width=240, height=60)

        self.exitButton = UIButton.Button('exitButton', self.buttonX-120, int(self.buttonY * 1.6)-30,
                                          pathToTexture='textures/', width=240, height=60)

        self.alive = True
        self.result = 0

        self.loop()

    def getResult(self):
        return self.result

    def loop(self):
        while self.alive:
            pos = pygame.mouse.get_pos()
            self.button.tick(pos[0], pos[1])
            self.exitButton.tick(pos[0], pos[1])

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.alive = False
                    self.result = -1
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.alive = False
                        self.result = -1
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        clicked = self.button.isClicked(e.pos[0], e.pos[1])
                        exitClicked = self.exitButton.isClicked(e.pos[0], e.pos[1])
                        if clicked:
                            self.alive = False
                            self.result = 1
                        elif exitClicked:
                            self.result = -1
                            exit()

            self.sc.blit(self.backGround, self.backGroundRect)

            texture = self.button.getButton()
            self.sc.blit(texture, texture.get_rect(topleft=(self.buttonX-120, int(self.buttonY * 1.25)-30)))

            exitTexture = self.exitButton.getButton()
            self.sc.blit(exitTexture, exitTexture.get_rect(topleft=(self.buttonX-120, int(self.buttonY * 1.6)-30)))

            pygame.display.update()
