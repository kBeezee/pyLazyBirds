import pygame
import random, numpy
from datetime import datetime
from pygame.locals import *

import sys
##CONSTANTS
WINDOWSIZE = (640, 480)
TRUEBORDER = 20
SPRITESCALE = 10
MOVEEVENT, t = pygame.USEREVENT+1, 1000
LASTSECOND = datetime.now().second
MYSCORE = HIGHSCORE = 0

pygame.time.set_timer(MOVEEVENT, t)
#http://stackoverflow.com/questions/14044147/animated-sprite-from-few-images


'''
#todo:
@make speed better, some of it it is hard coded
@all asset loading is done from the disk, i want to preload alel assets as global vars
    and then copy those vars (leaving them untouched) to the assets being added to ingame vars.
@collision is messed up, fix it.
@make it so on collision, the cornrs of the screen flash a red alpha
@make alt+enter toggle between fullscreen/window, i have the key events set up, and i found
    a function that is supposed to do it, but i get errors.
'''

def load_image(name, scale=tuple(numpy.divide(WINDOWSIZE, SPRITESCALE))):
    image = pygame.transform.scale(pygame.image.load(name), (scale))
    return image


def load_assets():
    AssetGroup = []
    AssetGroup.append(BirdSprites('badBirds/Bird A/', 4))
    AssetGroup.append(BirdSprites('badBirds/Bird B/', 4))
    AssetGroup.append(BirdSprites('badBirds/Bird C/', 4))
    AssetGroup.append(BirdSprites('badBirds/Bird D/', 4))
    AssetGroup.append(BirdSprites('badBirds/Bird E/', 8))
    AssetGroup.append(BirdSprites('badBirds/Bird F/flying/', 8))
    AssetGroup.append(BirdSprites('badBirds/Bird G/', 8))
    AssetGroup.append(BirdSprites('badBirds/Bird H/flying/', 8))
    AssetGroup.append(BirdSprites('badBirds/Bird I/', 8))
    return AssetGroup

def GetQuadrent(fLocation):
    if fLocation[0] >= WINDOWSIZE[0]/2 and fLocation[1] <= WINDOWSIZE[1]/2:
        return 1
    if fLocation[0] <= WINDOWSIZE[0]/2 and fLocation[1] <= WINDOWSIZE[1]/2:
        return 2
    if fLocation[0] <= WINDOWSIZE[0]/2 and fLocation[1] >= WINDOWSIZE[1]/2:
        return 3
    if fLocation[0] >= WINDOWSIZE[0]/2 and fLocation[1] >= WINDOWSIZE[1]/2:
        return 4

class BirdSprites(pygame.sprite.Sprite):
    def __init__(self, strFolder, intFrameCount, strName='enemy'):
        super(BirdSprites, self).__init__()
        self.images = []
        for i in range(1, intFrameCount+1):
            self.images.append(load_image(strFolder + 'frame-' + str(i) + '.png'))

        self.name = strName
        self.intFrameCount = intFrameCount
        self.index = 0
        self.delayanimation = 0
        self.image = self.images[self.index]

        #lets see if this works better for collision detection
        self.mask = pygame.mask.from_surface(self.image)

        #get a random location that isnt in the same quadrant as the player (ID as mouse location)
        fPlayer = pygame.mouse.get_pos()
        location = (random.randrange(TRUEBORDER,WINDOWSIZE[0]-TRUEBORDER), random.randrange(TRUEBORDER,WINDOWSIZE[1]-TRUEBORDER))
        self.quadrant = GetQuadrent(location)
        while self.quadrant == GetQuadrent(fPlayer):
            location = (random.randrange(TRUEBORDER,WINDOWSIZE[0]-TRUEBORDER), random.randrange(TRUEBORDER,WINDOWSIZE[1]-TRUEBORDER))
            self.quadrant = GetQuadrent(location)

        self.rect = pygame.Rect(location[0], location[1], 0, 0)

        #this keeps the birds from just staying in one spot, change it to 'or' to make them always move on diagonals
        self.speed = (0, 0)
        while self.speed[0] == 0 and self.speed[1] == 0:
            self.speed = (random.randrange(-3, 3), random.randrange(-3, 3))

        # uncomment to keep birds from moving (testing)
        #self.speed = (0, 0)

    def player(self):
        #this gets the player... prol a better way to do this but whatever.
        for x in self.groups():
            for y in x:
                if y.name == 'player':
                    return y

    def update(self):
        #this controls the animation of the frames (ie. Idle Animation)
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
            self.rect = pygame.Rect(pos[0], pos[1], numpy.divide(WINDOWSIZE[0],SPRITESCALE), numpy.divide(WINDOWSIZE[1],SPRITESCALE))
        else:  # define monster movement.
            #reverse speed when bird hits a specific border.
            self.BorderCheck()
            if self.speed[0] <= 0:
                self.image = pygame.transform.flip(self.image, True, False)
            #add speed to location.
            location = tuple(numpy.add((self.rect[0], self.rect[1]), self.speed))
            self.rect = pygame.Rect(location[0], location[1], 0, 0)


        #print(self.player().name)
        #CollisionDetection(self.player())

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

def CollisionDetection(fPLAYER):
    global MYSCORE, HIGHSCORE, LASTSECOND
    THISSECOND = datetime.now().second
    for x in fPLAYER.groups():
#using sprite.collide_mask makes it eaiser because its based on pixels not rect.
        #Collision is true
        if pygame.sprite.collide_mask(fPLAYER, x) and x.name != 'player':
            MYSCORE = 0
            LASTSECOND = datetime.now().second
            #PLAYER.rect = pygame.draw.circle(fPLAYER.images[fPLAYER.index], (255,0,0), (fPLAYER.rect.center), 250)
        #collision is not true
        else:
            if THISSECOND != LASTSECOND:
                MYSCORE += 1
                LASTSECOND = datetime.now().second
    if MYSCORE > HIGHSCORE:
        HIGHSCORE = MYSCORE
    LASTSECOND = datetime.now().second

def AddRandomBirdToGroup():
    pass
    #rnd = random.randrange(1, len(BADBIRDS))
    #return BADBIRDS[rnd]

    '''
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
    elif rnd == 7:
        return TestSprite('badBirds/Bird F/flying/', 8)
    elif rnd == 8:
        return TestSprite('badBirds/Bird G/', 8)
    elif rnd == 9:
        return TestSprite('badBirds/Bird H/flying/', 8)
    else:
        return TestSprite('badBirds/Bird I/', 8)
    '''

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
    BADBIRDS = []
    BADBIRDS = load_assets()
    my_group = pygame.sprite.Group()
    '''Another important thing, don't use the same Sprite() nor the same Rectangle
    in different locations. If you want to draw another copy of the same image in
    a new location make a copy of the rectangle, then create a new Sprite() object.
    '''
    my_group.add(BADBIRDS[1])
    my_group.add(BADBIRDS[1].clone)

    print(len(my_group))

    backGround = pygame.image.load('background/Full-background.png')
    backGround = pygame.transform.scale(backGround, WINDOWSIZE)
    PLAYERSPRITE = BirdSprites('myBird/', 8, 'player')
    my_group.add(PLAYERSPRITE)




    while True:
        clock.tick(60)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        #Birds get added when score is 10, 20, 30 etc. This makes it so only one bird is added per second
        if event.type == MOVEEVENT:
            if MYSCORE % 10 == 0 and MYSCORE >= 10:
                pass
                #my_group.add(GetRandomBird(BADBIRDS))

        #Catch Key Presses
        if event.type == pygame.KEYDOWN:
            pressedkeys = pygame.key.get_pressed()
            if pressedkeys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit(0)
            if pressedkeys[pygame.K_RETURN] and pressedkeys[pygame.K_LALT]:
                pass
                #toggle_fullscreen()

        #update all our sprites
        my_group.update()
        #place BG
        screen.blit(backGround, (0, 0))
        #draw them all
        my_group.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render('Your Score: ' + str(MYSCORE), 1, (10, 15, 20))
        screen.blit(text,(TRUEBORDER/3, WINDOWSIZE[1]-TRUEBORDER-TRUEBORDER-TRUEBORDER-TRUEBORDER))
        pygame.display.flip()

        #debug stuff
        if event.type == MOVEEVENT:
            pass
            #print('BirdNumber: ' + str(len(my_group)))
            #print('Highscore: ' + str(HIGHSCORE))

if __name__ == '__main__':
    main()