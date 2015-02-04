#!/usr/bin/env python

import pygame
import os
import random
import numpy
from datetime import datetime
from pygame.locals import *
    #http://stackoverflow.com/questions/28258944/using-pygame-draw-a-copy-of-an-image-in-a-different-location
    #http://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
import sys

pygame.init()
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
pygame.display.set_caption('Lazy Birds')
screen = pygame.display.set_mode((1024, 576))
WINDOWSIZE = (1024, 576)

##CONSTANTS
TRUEBORDER = 20
SPRITESCALE = 15
LASTSECOND = datetime.now().second
MYSCORE = HIGHSCORE = 0
ALLASSETS = []
PlayersGroup = pygame.sprite.Group()
EnemyGroup = pygame.sprite.Group()
AllGroup = pygame.sprite.Group()

# Create an event once every second.
MOVEEVENT, t = pygame.USEREVENT+1, 1000
pygame.time.set_timer(MOVEEVENT, t)



#this function writes something in a pre defined spot.
def write(msg="pygame is cool"):
    myfont = pygame.font.SysFont("None", 32)
    mytext = myfont.render(msg, True, (0,0,0))
    mytext = mytext.convert_alpha()
    return mytext


def load_image(name, scale=tuple(numpy.divide(WINDOWSIZE, SPRITESCALE))):
    image = pygame.transform.scale(pygame.image.load(name), scale)
    return image


#make class to hold the preloaded assets.
class PreLoadedSprites(pygame.sprite.Sprite):
    def __init__(self, strFolder, intFrameCount, strName='enemy'):
        self.images = []
        for i in range(1, intFrameCount+1):
            self.images.append(load_image(strFolder + 'frame-' + str(i) + '.png'))
        self.name = strName
        self.intFrameCount = intFrameCount

        #self.index = 0
        #self.NextFrameCounter = 0
        #self.NextFrameMax = 5  # raise to slow down, lower to speed up
        #self.image = self.images[self.index]
        #self.image = self.image.convert_alpha()
        #self.rect = self.image.get_rect()

#load all my assets
AssetIndex = (0,1,2,3,4,6,7,8,9,10)
ALLASSETS.append(PreLoadedSprites('badBirds/Bird A/', 4))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird B/', 4))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird C/', 4))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird D/', 4))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird E/', 8))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird F/flying/', 8, 'player'))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird G/', 8))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird H/flying/', 8))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird I/', 8))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird J/', 8))
ALLASSETS.append(PreLoadedSprites('badBirds/Bird K/flying/', 8))

#this is a class that holds the sprite the player controls
class PlayerControlled(pygame.sprite.Sprite):
    def __init__(self, PreLoadedSpriteAsset, strName='player'):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images = PreLoadedSpriteAsset.images
        self.name = strName
        self.intFrameCount = PreLoadedSpriteAsset.intFrameCount
        self.index = 0
        self.NextFrameCounter = 0
        self.NextFrameMax = 5
        self.image = self.images[self.index]
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, seconds=0):
        #deal with animation
        if self.NextFrameCounter < self.NextFrameMax:
            self.NextFrameCounter += 1
        else:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.NextFrameCounter = 0
        self.image = self.images[self.index]

        #note how player does not have .move this is because the player follows the mouse.
        self.rect.center = pygame.mouse.get_pos()


#this class contains the enemy birds.
class Bird(pygame.sprite.Sprite):
    def __init__(self, PreLoadedSpriteAsset, area=screen.get_rect(), strName='enemy'):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images = PreLoadedSpriteAsset.images
        self.name = strName
        self.intFrameCount = PreLoadedSpriteAsset.intFrameCount
        self.index = 0
        self.NextFrameCounter = 0
        self.NextFrameMax = 5
        self.image = self.images[self.index]
        self.image = self.image.convert_alpha()

        #get a random location that isnt in the same quadrant as the player (ID as mouse location)
        fPlayer = pygame.mouse.get_pos()
        location = (random.randrange(TRUEBORDER,WINDOWSIZE[0]-TRUEBORDER), random.randrange(TRUEBORDER,350))
        while GetQuadrent(location) == GetQuadrent(fPlayer):
            location = (random.randrange(TRUEBORDER,WINDOWSIZE[0]-TRUEBORDER), random.randrange(TRUEBORDER,350))
            self.quadrant = GetQuadrent(location)
        self.rect = pygame.Rect(location[0], location[1], 0, 0)
        #self.rect[0] = location[0]
        #self.rect[1] = location[1]
        self.area = area

        #this keeps the birds from just staying in one spot, change it to 'or' to make them always move on diagonals
        self.speed = (0, 0)
        while self.speed[0] == 0 and self.speed[1] == 0:
            self.speed = (random.randrange(-3, 3), random.choice((-3, -2, -1, 1, 2, 3)))

    def update(self, second=0):
        #deal with animation
        if self.NextFrameCounter < self.NextFrameMax:
            self.NextFrameCounter += 1
        else:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.NextFrameCounter = 0
        self.image = self.images[self.index]

        #movement is is kept seperate from animation
        self.move()

    def move(self):
        #reverse speed when bird hits a specific border.
        self.bordercheck()
        #flip the image if its going left or right
        if self.speed[0] <= 0:
            self.image = pygame.transform.flip(self.image, True, False)
        #add speed to location.
        location = tuple(numpy.add((self.rect[0], self.rect[1]), self.speed))
        #apply changes to the rectangle that contains the image.
        self.rect = pygame.Rect(location[0], location[1], 0, 0)

    def bordercheck(self):
        #reverse speed when birds reach the borders
        location = (self.rect[0], self.rect[1])
        if location[0] <= TRUEBORDER:
            self.speed = (self.speed[0]*-1, self.speed[1])
        elif location[0] >= WINDOWSIZE[0]-TRUEBORDER:
            self.speed = (self.speed[0]*-1, self.speed[1])
        elif location[1] <= TRUEBORDER:
            self.speed = (self.speed[0], self.speed[1]*-1)
        elif location[1] >= WINDOWSIZE[1]-TRUEBORDER:
            self.speed = (self.speed[0], self.speed[1]*-1)

'''
#todo:
@Paralax the background

@collision can be made better, try looking @ .center of rect...
-I want the screen edges to flash and red screen with 50% transperancy when collision happens.

@make alt+enter toggle between fullscreen/window, i have the key events set up, and i found
    a function that is supposed to do it, but i get errors.
'''


def GetQuadrent(fLocation):
    if fLocation[0] >= WINDOWSIZE[0]/2 and fLocation[1] <= WINDOWSIZE[1]/2:
        return 1
    if fLocation[0] <= WINDOWSIZE[0]/2 and fLocation[1] <= WINDOWSIZE[1]/2:
        return 2
    if fLocation[0] <= WINDOWSIZE[0]/2 and fLocation[1] >= WINDOWSIZE[1]/2:
        return 3
    if fLocation[0] >= WINDOWSIZE[0]/2 and fLocation[1] >= WINDOWSIZE[1]/2:
        return 4


def CollisionDetection(fPlayerGroup, fSpriteGroup):
    global MYSCORE, HIGHSCORE, LASTSECOND
    THISSECOND = datetime.now().second
    for players in fPlayerGroup:
        for enemy in fSpriteGroup:
            #Collision is true
            if pygame.sprite.collide_mask(players, enemy):
                MYSCORE = 0
                LASTSECOND = datetime.now().second
                enemy.kill()
            #collision is not true
            else:
                if THISSECOND != LASTSECOND:
                    MYSCORE += 1
                    LASTSECOND = datetime.now().second
    if MYSCORE > HIGHSCORE:
        HIGHSCORE = MYSCORE
    LASTSECOND = datetime.now().second


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
#background is pulled up old school style, this will be fixed when
#parallaxing is introduced.
    backGround = pygame.image.load('background/Full-background.png')
    backGround = pygame.transform.scale(backGround, WINDOWSIZE)

    #make player controlled object
    newbird = PlayerControlled(ALLASSETS[5])
    PlayersGroup.add(newbird)
    AllGroup.add(newbird)

    #make enemy birds
    for i in range(1, 50):
        rnd = random.choice(AssetIndex)
        newbird = Bird(ALLASSETS[rnd])
        EnemyGroup.add(newbird)
        AllGroup.add(newbird)

    while True:
        clock.tick(60)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        #Birds get added when score is 10, 20, 30 etc. This makes it so only one bird is added per second
        if event.type == MOVEEVENT:
            if len(EnemyGroup) == 0:
                rnd = random.choice(AssetIndex)
                newbird = Bird(ALLASSETS[rnd])
                EnemyGroup.add(newbird)
                AllGroup.add(newbird)
            if MYSCORE % 10 == 0 and MYSCORE >= 10:
                rnd = random.choice(AssetIndex)
                newbird = Bird(ALLASSETS[rnd])
                EnemyGroup.add(newbird)
                AllGroup.add(newbird)

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

        CollisionDetection(PlayersGroup, EnemyGroup)
        #update all our sprites(Animation and Movement)
        AllGroup.update()
        #place BG
        #TODO: Function to Parallax will go here, it should be similar to the sprites.
        screen.blit(backGround, (0, 0))
        #draw all sprites on top of the background
        AllGroup.draw(screen)
        #draw our score on the screen.
        font = pygame.font.Font(None, 36)
        text = font.render('Your Score: ' + str(MYSCORE), 1, (10, 15, 20))
        screen.blit(text,(TRUEBORDER/3, WINDOWSIZE[1]-TRUEBORDER-TRUEBORDER-TRUEBORDER-TRUEBORDER))
        #apply changes, basically.
        pygame.display.flip()

        #debug stuff
        if event.type == MOVEEVENT:
            print('BirdNumber: ' + str(len(AllGroup)))
            print('Highscore: ' + str(HIGHSCORE))

if __name__ == '__main__':
    main()