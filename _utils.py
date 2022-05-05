import os
import pygame



def drawImage(screen,image,pos,trim=False):
    if(trim!=False):
        screen.blit(image,pos,trim)
    else:
        screen.blit(image,pos)

def importFiles(sName,numLetters=3,tDir  = 'sprites/players/'):
    tDir = tDir
    spriteList = [x for x in os.listdir(tDir) if x[:numLetters] == sName]
    spriteList = [pygame.image.load(tDir + x) for x in spriteList]


    return(spriteList)

def impFilesL(sName,tDir = 'pics/assets/mechBox/'):
    """
    Give the example of the first file i.e. bob1.jpg and it will import the rest
    """
    tDir = tDir
    affix       = '.' + str(sName.split('.')[-1])
    prefix      = str(sName.split('.')[0])[:-1]
    numLetters  = len(sName.split(affix)[0])
    numbers     = sorted([int("".join(filter(str.isdigit, x))) for x in os.listdir(tDir) if (prefix in x) and (affix in x)])
    spriteList  = [prefix + str(x) + affix for x in numbers]
    if(len(spriteList) < 1):
        print('spritelist not populated for ' + str(sName))
        exit()
    try:
        spriteList  = [pygame.image.load(tDir + x) for x in spriteList]
    except:
        print('Files can not be found for ' + str(sName))
        exit()
    return(spriteList)




class statsBox():
    def __init__(self,x,y,font):
        self.x          = x
        self.y          = y
        self.font       = font
        self.colour     = (150,150,150)
        self.iboxcol    = (0,0,0)

    def display(self,textarray,game):
        for t in range(len(textarray)):
            text = textarray[t]
            textsurface = self.font.render(text, True, self.colour)
            tw = textsurface.get_rect().width
            th = textsurface.get_rect().height

            pygame.draw.rect(game.screen, (self.iboxcol), [self.x, self.y + t*th,tw ,th])
            game.screen.blit(textsurface,(self.x,self.y + t*th))


