import pygame


class Main:
    def __init__(self, path='', textureList=None, minScale=1, maxScale=32, colorkey=None):
        if textureList is None:
            textureList = []
        self.path = path
        self.textureList = textureList

        self.minScale = minScale
        self.maxScale = maxScale

        self.colorkey = colorkey

        self.textures = {}

        for texture in self.textureList:
            img = pygame.image.load(path + texture + '.png')
            if colorkey is None:
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)

            for scale in range(minScale, maxScale+1):
                self.textures[texture, scale, scale] = pygame.transform.scale(img, (scale, scale))

    def getTexture(self, name, w, h):
        try:
            return self.textures[name, w, h]
        except IndexError:
            return
