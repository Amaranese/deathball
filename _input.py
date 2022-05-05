
import pygame
import os

global shift

#################################    MANAGE INPUT      ################################# 


# MODIFIES USER INPUT
class manageInput():
    
    def __init__(self,shift=False):
        self.shift = shift
    def help():
        print('Pass user_input class into this, to include shift modifier')
    def manageButtons(self,event,user_input,game):
        
        # -------------return entered key
        if event.type == pygame.KEYDOWN: user_input.returnedKey = str(pygame.key.name(event.key))
        

        #---------------INGAME

        user_input.up    = pygame.key.get_pressed()[pygame.K_UP]
        user_input.down  = pygame.key.get_pressed()[pygame.K_DOWN]
        user_input.left  = pygame.key.get_pressed()[pygame.K_LEFT]
        user_input.right = pygame.key.get_pressed()[pygame.K_RIGHT]
        
        if(game.gameState=='ingame'):
            user_input.kick = None
            user_input.fire = None

            if(user_input.returnedKey.upper()=='H'): user_input.kick  = True

            if(pygame.key.get_pressed()[pygame.K_j]): user_input.fire    =True
            
            if(pygame.key.get_pressed()[pygame.K_w]): user_input.up    =True
            if(pygame.key.get_pressed()[pygame.K_s]): user_input.down  =True
            if(pygame.key.get_pressed()[pygame.K_a]): user_input.left  =True
            if(pygame.key.get_pressed()[pygame.K_d]): user_input.right =True






        #---------------END INGAME
        

        if (event.type == pygame.KEYDOWN):
            if(str(user_input.returnedKey) == 'left shift'): self.shift = True

            if(self.shift and (str(user_input.returnedKey) != 'left shift')):
                if(str(user_input.returnedKey) == "'"): user_input.returnedKey = '"'
                
                if(str(user_input.returnedKey) == "1"): user_input.returnedKey = "!"
                if(str(user_input.returnedKey) == "2"): user_input.returnedKey = "@"
                if(str(user_input.returnedKey) == "3"): user_input.returnedKey = "£"
                if(str(user_input.returnedKey) == "4"): user_input.returnedKey = "$"
                if(str(user_input.returnedKey) == "5"): user_input.returnedKey = "%"
                if(str(user_input.returnedKey) == "6"): user_input.returnedKey = "^"
                if(str(user_input.returnedKey) == "7"): user_input.returnedKey = "&"
                if(str(user_input.returnedKey) == "8"): user_input.returnedKey = "*"
                if(str(user_input.returnedKey) == "9"): user_input.returnedKey = "("
                if(str(user_input.returnedKey) == "0"): user_input.returnedKey = ")"
                if(str(user_input.returnedKey) == "-"): user_input.returnedKey = "_"
                if(str(user_input.returnedKey) == "="): user_input.returnedKey = "+"
                if(str(user_input.returnedKey) == ";"): user_input.returnedKey = ":"
                if(str(user_input.returnedKey) == "["): user_input.returnedKey = "{"
                if(str(user_input.returnedKey) == "]"): user_input.returnedKey = "}"
                if(str(user_input.returnedKey) == ","): user_input.returnedKey = "<"
                if(str(user_input.returnedKey) == "."): user_input.returnedKey = ">"
                if(str(user_input.returnedKey) == "/"): user_input.returnedKey = "?"
                if(str(user_input.returnedKey) == '\\'): user_input.returnedKey = "|"

                if(str(user_input.returnedKey).isalpha()): user_input.returnedKey = user_input.returnedKey.upper()

                self.shift = False


        return(user_input)













#################################    USER INPUT      ################################# 






class userInputObject():
    def __init__(self,returnedKey,enteredString,boxDims, game,directionBtn=None,  inputLimit = 30):
        self.returnedKey   = returnedKey
        self.pressedKey    = None
        self.up            = False
        self.down          = False
        self.left          = False
        self.right         = False
        self.kick          = False

        


        self.enteredString = enteredString
        self.boxDims       = boxDims
        self.game           = game
        self.directionBtn  = directionBtn
        self.inputLimit    = inputLimit
    
    def help():
        print('This object holds a current returned key and builds up an entered string. It also can draw text with blink at end value and draw a box.')






    # -------------------------Text input
    def processInput(self):

        # Clear out lingering direction Button
        self.directionBtn = None
        if((self.returnedKey.upper()=="UP") or (self.returnedKey.upper()=="DOWN")): self.directionBtn = self.returnedKey.upper()
        
        # If input given
        if((self.returnedKey!="") and (len(self.enteredString) < self.inputLimit)):
            # if space
            if(self.returnedKey.upper()=='SPACE'): self.returnedKey = " "
            # If single value, append to string
            if(len(self.returnedKey) == 1): self.enteredString = self.enteredString +  self.returnedKey
        
        # if backspace delete value
        if(self.returnedKey.upper()=='BACKSPACE'): self.enteredString = self.enteredString[:-1]
        if(self.returnedKey.upper()=='RETURN'): 
            self.returnedKey = 'complete'
            return(self.enteredString)
        # clear out
        self.returnedKey   = ""

        return(self.enteredString)



    def drawTextInput(self,text,x,y,colour=(0, 128, 0), blink = {'blinkDuration':5,'blinkValue':5,'displayInterval':5,'displayValue':5},chosenFont=None,limit=None):

        game = self.game
        if(chosenFont==None): chosenFont=game.font


        # --------------BLINK TEXT ON/OFF
        blink['blinkValue'] -= 1
        if(blink['blinkValue'] < 0):
            blink['displayValue'] -= 1
            text = text + '_'
            if(blink['displayValue']<0):
                blink['blinkValue']   = blink['blinkDuration']
                blink['displayValue']   = blink['displayInterval']
        
        # --------------DRAW TEXT SURFACE
        text = text.rstrip()
        textsurface = chosenFont.render(text, True, colour)

        # --------------LIMIT TEXT TO FIT IN BOX
        if(limit):
            if(textsurface.get_rect().width > limit):
                maxLen = round(limit/textsurface.get_rect().width * len(text))
                text = text[0:maxLen-9] + '...'  
                textsurface = chosenFont.render(text, True, colour)

        # --------------BLIT TEXT 
        game.screen.blit(textsurface,(x,y))


    def drawInputBox(self):
        game       = self.game
        boxX      = self.boxDims[0] * self.game.width
        boxY      = self.boxDims[1] * self.game.height
        boxWidth  = self.boxDims[2] * self.game.width
        boxHeight = self.boxDims[3] * self.game.height

        textX         = boxX + (0.1*boxWidth)
        textY         = boxY + (0.44*boxHeight)
        boardingBox   = buildColouredBox(game,boxX,boxY,boxWidth,boxHeight)
        self.drawTextInput(self.enteredString ,textX,textY,colour=game.white)







