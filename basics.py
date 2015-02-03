import pygame, time, random, numpy
WindowSize = (640, 480)


class AnimatedSprite(pygame.sprite.Group):
    def __init__(self):
        pass

class Game(object):
    def main(self, screen):
        while True:
            pressed_keys = pygame.key.get_pressed()
            print(pressed_keys)


if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode(WindowSize)
    Game().main(screen)

    #Happens after the game quits
    print("Close.")

