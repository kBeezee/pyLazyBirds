import pygame, random, numpy
import sys
WINDOWSIZE = (640, 480)
TRUEBORDER = 20
SPRITESCALE = 10
mySCORE = 0
#http://stackoverflow.com/questions/14044147/animated-sprite-from-few-images

'''
#todo:
make speed better, some of it it is hard coded
'''


def load_image(name, scale=tuple(numpy.divide(WINDOWSIZE, SPRITESCALE))):
    image = pygame.transform.scale(pygame.image.load(name), (scale))
    return image


class TestSprite(pygame.sprite.Sprite):
    def __init__(self, strFolder, intFrameCount, strName='enemy'):
        super(TestSprite, self).__init__()
        self.images = []
        for i in range(1, intFrameCount+1):
            self.images.append(load_image(strFolder + 'frame-' + str(i) + '.png'))

        self.name = strName
        self.intFrameCount = intFrameCount
        self.index = 0
        self.delayanimation = 0
        self.image = self.images[self.index]
        location = (random.randrange(TRUEBORDER,WINDOWSIZE[0]-TRUEBORDER), random.randrange(TRUEBORDER,WINDOWSIZE[1]-TRUEBORDER))
        self.rect = pygame.Rect(location[0], location[1], 64, 48)
        self.speed = (0, 0)
        while self.speed[0] == 0 and self.speed[1] == 0:
            self.speed = (random.randrange(-3, 3), random.randrange(-3, 3))

    def update(self):
        #this controlls the animation of the frames (ie. Idle Animation)
        if self.delayanimation < 1:
            self.delayanimation += 1
        else:
            self.delayanimation = 0
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        #this move the sprite.
        self.move()

    def move(self):
        #place player where the mouse is.
        if self.name == 'player':
            #player movement
            pos = pygame.mouse.get_pos()
            self.rect = pygame.Rect(pos[0], pos[1], numpy.divide(WINDOWSIZE[0],SPRITESCALE), numpy.divide(WINDOWSIZE[1],SPRITESCALE))
        else:  # define monster movement.
            #reverse speed when bird hits a specific border.
            self.BorderCheck()
            if self.speed[0] <= 0:
                self.image = pygame.transform.flip(self.image, True, False)
            #add speed to location.
            location = tuple(numpy.add((self.rect[0], self.rect[1]), self.speed))
            self.rect = pygame.Rect(location[0], location[1], numpy.divide(WINDOWSIZE[0],SPRITESCALE), numpy.divide(WINDOWSIZE[1],SPRITESCALE))

    def BorderCheck(self):
        #reverse speed on borders
        #self.speed = (random.randrange(-2,2), random.randrange(-2,2))
        location = (self.rect[0], self.rect[1])
        if location[0] < TRUEBORDER:
            self.speed = (self.speed[0]*-1, self.speed[1])
        elif location[0] > WINDOWSIZE[0]-TRUEBORDER:
            self.speed = (self.speed[0]*-1, self.speed[1])
        elif location[1] < TRUEBORDER:
            self.speed = (self.speed[0], self.speed[1]*-1)
        elif location[1] > WINDOWSIZE[1]-TRUEBORDER:
            self.speed = (self.speed[0], self.speed[1]*-1)




def CollisionDetection(fPLAYER, fSpriteGroup):
    global mySCORE
    for x in fSpriteGroup:
        if pygame.sprite.collide_rect(fPLAYER, x) and x.name != 'player':
            mySCORE = 0
        else:
            mySCORE += 1

    #BAM! now we got a game.
    print(mySCORE)


def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

#ASS---------->ETS
    backGround = pygame.image.load('background/Full-background.png')
    backGround = pygame.transform.scale(backGround, WINDOWSIZE)
    screen = pygame.display.set_mode(WINDOWSIZE)
    PLAYERSPRITE = TestSprite('myBird/', 8, 'player')# use this sprite name for loading assets
    my_group = pygame.sprite.Group(PLAYERSPRITE)   # declaration looks different

    for i in range(1,10):
        rnd = random.randrange(1, 9)
        if rnd == 1:
            my_group.add(TestSprite('badBirds/Bird A/', 4))
        elif rnd == 2:
            my_group.add(TestSprite('badBirds/Bird B/', 4))
        elif rnd == 3:
            my_group.add(TestSprite('badBirds/Bird C/', 4))
        elif rnd == 4:
            my_group.add(TestSprite('badBirds/Bird D/', 4))
        elif rnd == 6:
            my_group.add(TestSprite('badBirds/Bird E/', 8))
        elif rnd == 7:
            my_group.add(TestSprite('badBirds/Bird F/flying/', 8))
        else:
            my_group.add(TestSprite('badBirds/Bird G/', 8))

    while True:
        clock.tick(60)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit(0)

        #place BG
        screen.blit(backGround, (0, 0))
        #update all our sprites
        my_group.update()
        #draw them all
        CollisionDetection(PLAYERSPRITE, my_group)
        my_group.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()