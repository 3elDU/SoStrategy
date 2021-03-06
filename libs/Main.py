from libs.Constants import *
from libs import WorldGen
from libs import Functions
from libs import DebugInfo
from libs import TextureManager
from libs import TextureCreator
# from libs import OresRenderingThread
# from libs import WorldRenderingThread
from menus import PauseMenu
# from libs.particles import ParticleSystem
from libs import TextureRescaler
from libs import MainGUI
from libs import Civilization
from libs.rendering import Renderer
from menus import SettingsMenu
from menus import MainMenu
import pygame
import random
import time


class Main:
    def __init__(self):

        # Making window
        pygame.init()

        self.sc = pygame.display.set_mode((0, 0),
                                          pygame.FULLSCREEN)

        pygame.display.set_caption("SoStrategy v0.1.21")

        icon = pygame.image.load('textures/icon3.png').convert_alpha()
        icon.set_colorkey(WHITE)

        pygame.display.set_icon(icon)

        w, h = pygame.display.get_surface().get_size()

        # Displaying start menu
        self.mainMenu = MainMenu.Menu(self.sc, w, h)

        result = self.mainMenu.getResult()
        if result == -1:
            exit()

        # Initializing classes

        # World generator
        self.noise = WorldGen.Noise()

        # Some functions ( like clamp )
        self.functions = Functions.Functions()

        # Overlay with some debug info like fps and coordinates ( F3 to turn on and off )
        self.debug = DebugInfo.Main('arial', 36)

        # Texture manager, to easily load and store textures
        self.mgr = TextureManager.Main(path='textures/', textureList=['border'])

        # Generating world
        self.noise.generateWorld(256, 128, 0.03,
                                 random.randint(-10000, 10000),
                                 random.randint(-10000, 10000))

        # Generating ores
        self.noise.generateOres(256, 128, 0.03,
                                random.randint(-10000, 10000),
                                random.randint(-10000, 10000))

        # Second texture manager, to store textures with ores, because they all have white bg that we must remove
        self.mgr1 = TextureManager.Main(path='textures/', textureList=['coal', 'fish', 'wood',
                                                                       'iron', 'gold', 'diamond'],
                                        colorkey=(255, 255, 255))

        # This will be initialized pause menu class, we will initializing if we want to go in pause menu
        self.pauseMenu = None

        # This will be UI overlay with all game information, score, images, and so on.
        self.mainGui = MainGUI.Main(w, h)

        # Dictionaries
        self.world = self.noise.get()[0]
        self.ores = self.noise.get()[1]
        self.buildings = {}
        self.prevBlocks = {}
        self.prevOres = {}

        # Initializing texture creator class, that allows us to show the whole world with good fps
        self.creator = TextureCreator.TextureCreator(self.world, self.ores, 256, 128, self.mgr1)
        self.creator.run()

        # Initializing texture rescaler class, that allows us to show ores with good fps
        self.rescaler = TextureRescaler.Main(path='textures/', textureList=['coal', 'fish', 'wood',
                                                                            'iron', 'gold', 'diamond',
                                                                            'town_hall'],
                                             minScale=8, maxScale=32, colorkey=WHITE)

        # Floats
        self.xFloat = 0.0
        self.yFloat = 0.0

        # Integers
        self.w, self.h = w, h
        self.cameraSpeed = 60
        self.blockSize = 16
        self.renderingMode = 1
        self.x = 0
        self.y = 0
        self.cursorVisibility = 128
        self.startX = pygame.display.get_surface().get_width() // 2 - (33 * self.blockSize)
        self.startY = pygame.display.get_surface().get_height() // 2 - (17 * self.blockSize)
        self.centerX = pygame.display.get_surface().get_width() // 2
        self.centerY = pygame.display.get_surface().get_height() // 2

        # Bools
        self.displayDebugInfo = False
        self.showingOres = False
        self.showingBuildings = True
        self.showingAllMap = False

        # Initializing font
        self.font = pygame.font.SysFont('arial', 36)

        # Creating pygame surfaces
        self.mapSurf = pygame.Surface((66 * self.blockSize, 34 * self.blockSize))
        self.border = pygame.transform.scale(self.mgr.getTexture('border'), (66 * self.blockSize, 34 * self.blockSize))
        self.mapSurf.blit(self.border, self.border.get_rect())
        self.wholeMapSurf = self.creator.getTexture()
        self.oresSurf = pygame.Surface((66 * self.blockSize, 34 * self.blockSize))
        self.oresSurf.fill(BG_COLOR)
        self.oresSurf.set_colorkey((1, 1, 1))
        self.cursor = pygame.Surface((16, 16))
        self.cursor.fill(RED)
        self.cursor.set_alpha(self.cursorVisibility)
        self.buildingsSurf = pygame.Surface((66 * self.blockSize, 34 * self.blockSize))
        self.buildingsSurf.fill(BG_COLOR)
        self.buildingsSurf.set_colorkey(BG_COLOR)

        # Creating pygame rects
        self.GUIRect = pygame.Rect(0, 0, w, h)

        # Creating our civilization
        self.civ = Civilization.Civ(self.world, self.buildings, self.ores)
        self.xFloat = self.functions.clamp(self.civ.x - 33, 0, 255)
        self.yFloat = self.functions.clamp(self.civ.y - 17, 0, 127)

        # Rendering classes
        self.renderer1 = Renderer.RenderingMode1(self.x, self.y, self.world, self.buildings, self.ores,
                                                 self.w, self.h, self.mgr, self.creator, self.rescaler)

        # Starting main loop
        self.loop()

    @staticmethod
    def calculateDelta(current, prev):
        return current - prev

    def resize(self):
        self.wholeMapSurf = self.creator.getTexture()
        self.wholeMapSurf = pygame.transform.scale(self.wholeMapSurf, (256 * (self.blockSize // 4),
                                                                       128 * (self.blockSize // 4)))

        self.startX = pygame.display.get_surface().get_width() // 2 - (32 * self.blockSize)
        self.startY = pygame.display.get_surface().get_height() // 2 - (16 * self.blockSize)

    def loop(self):
        prevFrame = time.time()
        prevSize = self.blockSize
        d = 0
        frame = 0

        while 1:

            sTime = time.time()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.pauseMenu = PauseMenu.PauseMenu(self.sc, self.w, self.h)
                        r = self.pauseMenu.getResult()
                        if r == 0:
                            # self.particles.stop()
                            # self.worldThread.stop()
                            exit()
                        elif r == 1:
                            self.prevOres = {}
                            self.prevBlocks = {}
                        elif r == 2:
                            s = SettingsMenu.Menu(self.sc, self.w, self.h)
                            result = s.getResult()
                            print(result)
                    if e.key == pygame.K_F2:
                        pygame.image.save(self.sc, 'screenshot' + str(time.time()) + '.png')
                    if e.key == pygame.K_F3:
                        self.displayDebugInfo = not self.displayDebugInfo
                    if e.key == pygame.K_m:
                        self.showingAllMap = not self.showingAllMap
                        if self.showingAllMap:
                            self.resize()
                    if e.key == pygame.K_o:
                        self.showingOres = not self.showingOres
                    if e.key == pygame.K_b:
                        self.showingBuildings = not self.showingBuildings
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        bX = e.pos[0] - self.blockSize
                        bY = e.pos[1] - self.blockSize

                        lUX = self.centerX - 33 * self.blockSize
                        lUY = self.centerY - 17 * self.blockSize

                        rDX = self.centerX + 33 * self.blockSize
                        rDY = self.centerY + 17 * self.blockSize

                        if lUX <= bX <= rDX and \
                           lUY <= bY <= rDY:
                            realx = self.functions.clamp(self.x + (bX - lUX) // self.blockSize, 0, 255)
                            realy = self.functions.clamp(self.y + (bY - lUY) // self.blockSize, 0, 127)

                            self.world[realx, realy] = ['userblock', RED]

            # Moving map
            pos = pygame.mouse.get_pos()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.yFloat -= d
            if keys[pygame.K_a]:
                self.xFloat -= d
            if keys[pygame.K_s]:
                self.yFloat += d
            if keys[pygame.K_d]:
                self.xFloat += d
            if keys[pygame.K_z]:
                self.blockSize -= 1
            if keys[pygame.K_x]:
                self.blockSize += 1

            self.xFloat = self.functions.clamp(self.xFloat, 0, 192)
            self.yFloat = self.functions.clamp(self.yFloat, 0, 96)
            self.blockSize = self.functions.clamp(self.blockSize, 8, 32)

            self.x = int(self.xFloat)
            self.y = int(self.yFloat)

            if prevSize != self.blockSize:
                self.resize()

            # Rendering all

            self.mainGui.updateData(self.x, self.y)
            self.renderer1.updateData(self.x, self.y, self.blockSize, self.showingOres, self.showingBuildings,
                                      self.world, self.ores)

            self.sc.fill((255, 125, 0))

            if not self.showingAllMap:
                self.renderer1.renderAll()

                s = self.renderer1.getSurf()
                gamemap = s['map']
                self.sc.blit(gamemap, gamemap.get_rect(center=(self.centerX, self.centerY)))
                if self.showingOres:
                    ores = s['ores']
                    self.sc.blit(ores, ores.get_rect(center=(self.centerX, self.centerY)))
                if self.showingBuildings:
                    buildings = s['buildings']
                    self.sc.blit(buildings, buildings.get_rect(center=(self.centerX, self.centerY)))
            else:
                self.sc.blit(self.wholeMapSurf, self.wholeMapSurf.get_rect(center=(self.centerX, self.centerY)))

            self.sc.blit(self.mainGui.getSurf(), self.GUIRect)

            self.sc.blit(self.cursor, self.cursor.get_rect(center=(pos[0], pos[1])))

            # Setting some variables to show fps, and frametime

            eTime = time.time()

            if self.displayDebugInfo:
                s = self.debug.calculate(prevFrame, eTime, sTime, self.x, self.y, self.blockSize)

                self.sc.blit(s, self.GUIRect)

            pygame.display.update()

            d = (eTime - sTime) * self.cameraSpeed

            prevFrame = time.time()
            prevSize = self.blockSize

            frame += 1
