import pygame
from _utils                 import *



class game():
    def __init__(self,screen,width,height):
        self.screen       = screen
        self.width        = width
        self.height       = height
        self.font         = pygame.font.Font('fonts/nokiafc22.ttf', 32)
        self.smallFont    = pygame.font.Font('fonts/nokiafc22.ttf', 18)


        self.gameState         = 'ingame'
        self.userInput         = None # Loaded at runtime
        self.running           = True
        self.dt                = 0
        self.gameElapsed       = 0
        self.debugSwitch       = False
        self.mx                = 0
        self.my                = 0


        self.white             = (255,255,255)
        self.green             = (0,255,0)
        self.blue              = (176,224,230)

        self.selectedIcon      = impFilesL('selected1.png',tDir='sprites/icons/')
        self.selectedIconIndex = 0
        self.selectedIcnWait   = 200





        # --------- images

        self.snowField           = pygame.image.load('sprites/snowFieldBig.png')
        self.field               = pygame.image.load('sprites/fieldBig.png')
        self.map                 = self.snowField
        self.mapX                = 0
        self.mapY                = 0
        self.mapW                = self.map.get_rect().w
        self.mapH                = self.map.get_rect().h


        # ---------runtime 

        self.squad               = {} # Loaded at runtime


    def debug(self,debugMessage):
        if(self.debugSwitch):
            print(debugMessage)

    def animate(self,x,y,imageList,imageIndex,camera,wait,waitDefault):
        """
        supply an image list to be animated
        supply a wait duration (frame speed) and a default value
        """

        # Frame to be blitted
        blitFrame = imageList[imageIndex]
        self.screen.blit(blitFrame,(x - camera.x,y- camera.y))

        # increment index
        wait-=self.dt
        if(wait<0):
            wait=waitDefault
            imageIndex +=1
            if(imageIndex>=len(imageList)): imageIndex = 0

        return(imageIndex,wait)

    def collides(self,objPos,x,y,w,h):
        if objPos[0] > x and objPos[0] < x + w:
            if objPos[1] > y and objPos[1] < y + h:
                return(True)
        return(False)


class camera():
    def __init__(self, x, y,gui):
        self.x      = x
        self.y      = y
        self.offx   = -gui.width/2
        self.offy   = -gui.height/2
        self.target = 'player'
