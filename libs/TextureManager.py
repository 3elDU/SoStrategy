import pygame
pygame.init()


class Main:
    def __init__(self, path=None, textureList=None, colorkey=None):
        self.path = path

        if path is None:
            self.path = ''
        if textureList is None:
            textureList = []
        if colorkey is not None:
            self.colorkey = colorkey
        else:
            self.colorkey = (0, 0, 0)
        self.textures = {}

        if len(textureList) > 0:
            for texture in textureList:
                try:
                    self.textures[texture] = pygame.image.load(self.path + texture + '.png')
                    if colorkey is not None:
                        self.textures[texture] = self.textures[texture].convert()
                        self.textures[texture].set_colorkey(self.colorkey)
                    else:
                        self.textures[texture] = self.textures[texture].convert_alpha()
                except Exception as e:
                    print("TEXTURE LOAD ERROR:", e)

    def getTexture(self, texture):
        try:
            return self.textures[texture]
        except KeyError:
            return

    def loadTexture(self, texture):
        if isinstance(texture, list):

            if len(texture) > 0:

                for text in texture:

                    try:
                        self.textures[text] = pygame.image.load(self.path + text + '.txt')
                        if self.colorkey is not None:
                            self.textures[texture] = self.textures[texture].convert()
                            self.textures[texture].set_colorkey(self.colorkey)
                        else:
                            self.textures[texture] = self.textures[texture].convert_alpha()
                    except pygame.error:
                        pass

        elif isinstance(texture, str):
            try:
                self.textures[texture] = pygame.image.load(self.path + texture + '.png')
                if self.colorkey is not None:
                    self.textures[texture] = self.textures[texture].convert()
                    self.textures[texture].set_colorkey(self.colorkey)
                else:
                    self.textures[texture] = self.textures[texture].convert_alpha()

            except KeyError:
                pass
