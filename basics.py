import pygame, time, random, numpy
WindowSize = (640, 480)


class AnimatedSprite(pygame.sprite.Group):
    def __init__(self):
        pass

class Game(object):
    def main(self, screen):
        x = 0
        while x != 5:
            x += 1
        print(x)


if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode(WindowSize)
    Game().main(screen)

    #Happens after the game quits
    print("Close.")