import pygame, random, numpy

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
        location = (random.randrange(5,635), random.randrange(5,475))
        self.rect = pygame.Rect(location[0], location[1], 64, 48)
        self.speed = (random.randrange(-2, 2), random.randrange(-2, 2))

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
            #self.speed = (random.randrange(-2,2), random.randrange(-2,2))
            location = (self.rect[0], self.rect[1])
            if location[0] < 0:
                self.speed = (self.speed[0]*-1, self.speed[1])
            elif location[0] > 640:
                self.speed = (self.speed[0]*-1, self.speed[1])
            elif location[1] < 0:
                self.speed = (self.speed[0], self.speed[1]*-1)
            elif location[1] > 480:
                self.speed = (self.speed[0], self.speed[1]*-1)

            #if flying to right, dont transform image, if flying to left, flip it.
            if self.speed[0] <= 0:
                self.image = pygame.transform.flip(self.image, True, False)

            location = tuple(numpy.add((self.rect[0], self.rect[1]), self.speed))
            self.rect = pygame.Rect(location[0], location[1], 64, 48)


            print(location)
            #print(self.rect[0])
            #print(self.speed)


def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    backGround = pygame.image.load('background/Full-background.png')
    backGround = pygame.transform.scale(backGround, (640, 480))
    screen = pygame.display.set_mode((640, 480))
    #'myBird/frame-
    my_sprite = TestSprite('myBird/', 8, 'player')
    my_group = pygame.sprite.Group(my_sprite)
    my_sprite = TestSprite('badBirds/Bird A/', 4)
    my_group.add(my_sprite)

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

        print(len(my_group))
        my_group.update()
        my_group.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()