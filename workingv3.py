import pygame
import random, numpy
from datetime import datetime
from pygame.locals import *
    #http://stackoverflow.com/questions/28258944/using-pygame-draw-a-copy-of-an-image-in-a-different-location
    #http://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
import sys
##CONSTANTS
#
WINDOWSIZE = (1024, 576)
TRUEBORDER = 20
SPRITESCALE = 15
MOVEEVENT, t = pygame.USEREVENT+1, 1000
LASTSECOND = datetime.now().second
MYSCORE = HIGHSCORE = 0
pygame.time.set_timer(MOVEEVENT, t)

'''
#todo:

@Paralax the background

#http://stackoverflow.com/questions/28258944/using-pygame-draw-a-copy-of-an-image-in-a-different-location
@all asset loading is done from the disk, i want to preload alel assets as global vars
    and then copy those vars (leaving them untouched) to the assets being added to ingame vars.

@collision is messed up, fix it.
-I want the screen edges to flash and red screen with 50% transperancy when collision happens.
@make alt+enter toggle between fullscreen/window, i have the key events set up, and i found
    a function that is supposed to do it, but i get errors.
'''

def load_image(name, scale=tuple(numpy.divide(WINDOWSIZE, SPRITESCALE))):
    image = pygame.transform.scale(pygame.image.load(name), (scale))
    return image


def GetQuadrent(fLocation):
    if fLocation[0] >= WINDOWSIZE[0]/2 and fLocation[1] <= WINDOWSIZE[1]/2:
        return 1
    if fLocation[0] <= WINDOWSIZE[0]/2 and fLocation[1] <= WINDOWSIZE[1]/2:
        return 2
    if fLocation[0] <= WINDOWSIZE[0]/2 and fLocation[1] >= WINDOWSIZE[1]/2:
        return 3
    if fLocation[0] >= WINDOWSIZE[0]/2 and fLocation[1] >= WINDOWSIZE[1]/2:
        return 4


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
        self.PreviousPosition = (0, 0)
        #lets see if this works better for collision detection
        self.mask = pygame.mask.from_surface(self.image)

        #get a random location that isnt in the same quadrant as the player (ID as mouse location)
        fPlayer = pygame.mouse.get_pos()
        location = (random.randrange(TRUEBORDER,WINDOWSIZE[0]-TRUEBORDER), random.randrange(TRUEBORDER,350))
        self.quadrant = GetQuadrent(location)
        while self.quadrant == GetQuadrent(fPlayer):
            location = (random.randrange(TRUEBORDER,WINDOWSIZE[0]-TRUEBORDER), random.randrange(TRUEBORDER,350))
            self.quadrant = GetQuadrent(location)

        self.rect = pygame.Rect(location[0], location[1], 0, 0)

        #this keeps the birds from just staying in one spot, change it to 'or' to make them always move on diagonals
        self.speed = (0, 0)
        while self.speed[0] == 0 and self.speed[1] == 0:
            self.speed = (random.randrange(-3, 3), random.choice((-3, -2, -1, 1, 2, 3)))

        # uncomment to keep birds from moving (testing)
        #self.speed = (0, 0)

    def update(self):
        #this controlls the animation of the frames (ie. Idle Animation)
        if self.delayanimation < 5:
            self.delayanimation +=   1
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
            self.speed = numpy.subtract(self.PreviousPosition, pos)
            self.rect = pygame.Rect(pos[0], 476, numpy.divide(WINDOWSIZE[0],SPRITESCALE), numpy.divide(WINDOWSIZE[1],SPRITESCALE))
            if self.speed[0] > 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.PreviousPosition = pos
        else:  # define monster movement.
            #reverse speed when bird hits a specific border.
            self.BorderCheck()
            if self.speed[0] <= 0:
                self.image = pygame.transform.flip(self.image, True, False)
            #add speed to location.
            location = tuple(numpy.add((self.rect[0], self.rect[1]), self.speed))
            self.rect = pygame.Rect(location[0], location[1], 0, 0)

    def BorderCheck(self):
        #reverse speed on borders
        #self.speed = (random.randrange(-2,2), random.randrange(-2,2))
        location = (self.rect[0], self.rect[1])
        if location[0] <= TRUEBORDER:
            self.speed = (self.speed[0]*-1, self.speed[1])
        elif location[0] >= WINDOWSIZE[0]-TRUEBORDER:
            self.speed = (self.speed[0]*-1, self.speed[1])
        elif location[1] <= TRUEBORDER:
            self.speed = (self.speed[0], self.speed[1]*-1)
        elif location[1] >= WINDOWSIZE[1]-TRUEBORDER:
            self.speed = (self.speed[0], self.speed[1]*-1)


def CollisionDetection(fPLAYER, fSpriteGroup):
    global MYSCORE, HIGHSCORE, LASTSECOND
    THISSECOND = datetime.now().second
    for x in fSpriteGroup:
        #Collision is true
#        if pygame.sprite.collide_rect(fPLAYER, x) and x.name != 'player':
# this makes the game eaiser beacause the sprites are mapped and collision is not based on rectangles.
        if pygame.sprite.collide_mask(fPLAYER, x) and x.name != 'player':
            MYSCORE = 0
            LASTSECOND = datetime.now().second
        #collision is not true
        else:
            if THISSECOND != LASTSECOND:
                MYSCORE += 1
                LASTSECOND = datetime.now().second
    if MYSCORE > HIGHSCORE:
        HIGHSCORE = MYSCORE
    LASTSECOND = datetime.now().second


def GetRandomBird():
    rnd = random.randrange(1, 9)
    if rnd == 1:
        return TestSprite('badBirds/Bird A/', 4)
    elif rnd == 2:
        return TestSprite('badBirds/Bird B/', 4)
    elif rnd == 3:
        return TestSprite('badBirds/Bird C/', 4)
    elif rnd == 4:
        return TestSprite('badBirds/Bird D/', 4)
    elif rnd == 6:
        return TestSprite('badBirds/Bird E/', 8)
    elif rnd == 0:
        return TestSprite('badBirds/Bird F/flying/', 8)
    elif rnd == 8:
        return TestSprite('badBirds/Bird G/', 8)
    elif rnd == 9:
        return TestSprite('badBirds/Bird I/', 8)
    else:
        return TestSprite('badBirds/Bird J/', 8)


def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007

    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()

    print((w, h))
    print(flags ^ pygame.FULLSCREEN)
    print(bits)

    #pygame.display.quit()
    pygame.display.init()

    screen = pygame.display.set_mode((w, h), flags^pygame.FULLSCREEN, bits)
    screen.blit(tmp,(0,0))
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

    pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007

    return screen

def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Lazy Birds')
    screen = pygame.display.set_mode(WINDOWSIZE)
#ASS---------->ETS
    backGround = pygame.image.load('background/Full-background.png')
    backGround = pygame.transform.scale(backGround, WINDOWSIZE)
    PLAYERSPRITE = TestSprite('badBirds/Bird F/flying/', 8, 'player')
    my_group = pygame.sprite.Group(PLAYERSPRITE)   # declaration of important group.

    print(backGround)
    for i in range(1, 3):
        my_group.add(GetRandomBird())

    while True:
        clock.tick(50)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        #Birds get added when score is 10, 20, 30 etc. This makes it so only one bird is added per second
        if event.type == MOVEEVENT:
            if MYSCORE % 10 == 0 and MYSCORE >= 10:
                my_group.add(GetRandomBird())

        #Catch Key Presses
        if event.type == pygame.KEYDOWN:
            pressedkeys = pygame.key.get_pressed()
            if pressedkeys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit(0)
            if pressedkeys[pygame.K_RALT] or pressedkeys[pygame.K_LALT]:
                if event.type is pygame.KEYDOWN and event.key == pygame.K_f:
                    pass
                    #pygame.display.set_mode(WINDOWSIZE, pygame.FULLSCREEN)
                if event.type is pygame.KEYDOWN and event.key == pygame.K_w:
                    pass
                    #pygame.display.set_mode(WINDOWSIZE)

        #place BG
        screen.blit(backGround, (0, 0))
        #update all our sprites
        my_group.update()
        #draw them all
        CollisionDetection(PLAYERSPRITE, my_group)
        my_group.draw(screen)
        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render('Your Score: ' + str(MYSCORE), 1, (10, 15, 20))
        screen.blit(text,(TRUEBORDER/3, WINDOWSIZE[1]-TRUEBORDER-TRUEBORDER-TRUEBORDER-TRUEBORDER))
        pygame.display.flip()

        #debug stuff
        if event.type == MOVEEVENT:
            print('BirdNumber: ' + str(len(my_group)))
            print('Highscore: ' + str(HIGHSCORE))

if __name__ == '__main__':
    main()