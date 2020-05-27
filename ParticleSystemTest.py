from libs.particles import ParticleSystem
import pygame


class Main:
    def __init__(self):
        pygame.init()

        self.sc = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.particles = ParticleSystem.Main(1366, 768, 'textures/particleBackground.png', 15,
                                             'textures/particle.png', 100)
        self.particles.start()

        self.loop()

    def loop(self):
        while 1:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.particles.stop()
                        exit()

            texture = self.particles.getSurface()
            rect = texture.get_rect()
            self.sc.blit(texture, rect)

            pygame.display.update()


if __name__ == '__main__':
    Main()
