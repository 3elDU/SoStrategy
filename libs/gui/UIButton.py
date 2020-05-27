import pygame


class Button:
    regular: pygame.Surface
    hovered: pygame.Surface

    def __init__(self, textureName, bX, bY, pathToTexture='', textureFormat='.png', width=None, height=None):
        self.textureName = textureName
        self.x, self.y = bX, bY
        self.pathToTexture = pathToTexture
        self.textureFormat = textureFormat
        self.width, self.height = width, height

        self.error = False
        self.isHovered = False
        self.click = False

        self.errorSurface = pygame.Surface((self.width, self.height))
        self.errorSurface.fill((255, 255, 255))

        try:
            self.regular = pygame.image.load(self.pathToTexture + self.textureName + self.textureFormat)
            self.regular = self.regular.convert_alpha(self.regular)

            self.hovered = pygame.image.load(self.pathToTexture + self.textureName + '-hovered' + self.textureFormat)
            self.hovered = self.hovered.convert_alpha(self.hovered)

            if self.width is not None and self.height is not None:
                self.regular = pygame.transform.scale(self.regular, (self.width, self.height))
                self.hovered = pygame.transform.scale(self.hovered, (self.width, self.height))
            else:
                self.width = self.regular.get_width()
                self.height = self.regular.get_height()

            self.bx = self.x + self.regular.get_width()
            self.by = self.y + self.regular.get_height()

        except pygame.error as e:
            self.error = True
            print(e)

    def getButton(self):
        if not self.error:
            if self.isHovered:
                return self.hovered
            else:
                return self.regular
        else:
            return self.errorSurface

    def isClicked(self, x, y):
        if self.bx - x >= 0 and self.by - y >= 0:
            if self.x - x <= 0 and self.y - y <= 0:
                return True
            else:
                return False
        else:
            return False

    def isHovered(self):
        pass

    def tick(self, x, y):
        if self.bx - x >= 0 and self.by - y >= 0:
            if x - self.x >= 0 and y - self.y >= 0:
                self.isHovered = True
            else:
                self.isHovered = False
        else:
            self.isHovered = False
