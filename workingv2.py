import pygame, random, numpy
WINDOWSIZE = (800, 600)
TRUEBORDER = 20

#print(numpy.divide(WINDOWSIZE, 2))

import sys
#http://stackoverflow.com/questions/14044147/animated-sprite-from-few-images



def load_image(name, scale=(64,48)):
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
        location = (random.randrange(1,635), random.randrange(5,475))
        self.rect = pygame.Rect(location[0], location[1], 64, 48)
        self.speed = (0,0)
        while self.speed[0] == 0 and self.speed[1] == 0:
            self.speed = (random.randrange(-3, 3), random.randrange(-3, 3))

    def update(self):
        #this controlls the animation of the frames (ie. Idle Animation)
        if self.delayanimation < 3:
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
            pos = pygame.mouse.get_pos()
            self.rect = pygame.Rect(pos[0], pos[1], 64, 48)
        else: #define monster movement.
            #reverse speed on borders
            self.BorderCheck()

            #if flying to right, dont transform image, if flying to left, flip it.
            if self.speed[0] <= 0:
                self.image = pygame.transform.flip(self.image, True, False)

            #add speed to location.
            location = tuple(numpy.add((self.rect[0], self.rect[1]), self.speed))
            self.rect = pygame.Rect(location[0], location[1], 64, 48)

            #print(location)
            #print(self.rect[0])
            #print(self.speed)


    def BorderCheck(self):
        #reverse speed on borders
        #self.speed = (random.randrange(-2,2), random.randrange(-2,2))
        location = (self.rect[0], self.rect[1])
        if location[0] < 15:
            self.speed = (self.speed[0]*-1, self.speed[1])
        elif location[0] > 615:
            self.speed = (self.speed[0]*-1, self.speed[1])
        elif location[1] < 15:
            self.speed = (self.speed[0], self.speed[1]*-1)
        elif location[1] > 450:
            self.speed = (self.speed[0], self.speed[1]*-1)


def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()


#ASS---------->ETS
    backGround = pygame.image.load('background/Full-background.png')
    backGround = pygame.transform.scale(backGround, (640, 480))
    screen = pygame.display.set_mode((640, 480))
    PLAYERSPRITE = TestSprite('myBird/', 8, 'player')# use this sprite name for loading assets
    my_group = pygame.sprite.Group(PLAYERSPRITE)   # declaration looks different

    for i in range(1,25):
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
        screen.blit(backGround, (0, 0))
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit(0)

        # Calling the 'my_group.update' function calls the 'update' function of all
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.

        #print(len(my_group))
        my_group.update()
        my_group.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()