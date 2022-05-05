import pygame
import os
import time
import math
import random
import json
import os
import os, sys


from _game                  import *
from _input                 import *
from _utils                 import *
from _player                import *
from _ball                  import *



# -----------VARIABLES & FLAGS
FPS            = 60
width, height  = 1280,720
themeColour    = (128,0,0)
time = 0


# ---------------PYGAME

pygame.init()
pygame.display.set_caption("Fitba")
clock          = pygame.time.Clock()
nextFrame      = pygame.time.get_ticks()
screen         = pygame.display.set_mode((width,height),pygame.DOUBLEBUF)
#pygame.time.set_timer(pygame.USEREVENT, 20)

# ---------------CLASS OBJECTS
game                  = game(screen,width,height)
user_input            = userInputObject("","",(0.27,0.65,0.45,0.08), game)
modifyInput           = manageInput()
camera                = camera(game.width/2,game.height/2,game)

# -----------game objects

footballSpriteList     = impFilesL('ball1.png',tDir = 'sprites/ball/')
footballSprite         = sprite(footballSpriteList,game.width/2,game.height/2)
fitba                  = fitbaObject(footballSprite)


protoSprite            = impFilesL('proto1.png',tDir='sprites/players/mech/')
squad                  = { 'capt':playerObject('capt',playerSprite(protoSprite),0.5*game.width,0.3*game.height,vx=5,vy=5,originX=0.5*game.mapW,originY=0.3*game.mapH ),
                           'fwdr':playerObject('fwdr',playerSprite(protoSprite),0.6*game.width,0.2*game.height,vx=5,vy=5,originX=0.6*game.mapW,originY=0.2*game.mapH ),
                           'fwdl':playerObject('fwdl',playerSprite(protoSprite),0.4*game.width,0.2*game.height,vx=5,vy=5,originX=0.4*game.mapW,originY=0.2*game.mapH ),
                           'midr':playerObject('midr',playerSprite(protoSprite),0.6*game.width,0.5*game.height,vx=5,vy=5,originX=0.6*game.mapW,originY=0.5*game.mapH ),
                           'midl':playerObject('midl',playerSprite(protoSprite),0.4*game.width,0.5*game.height,vx=5,vy=5,originX=0.4*game.mapW,originY=0.5*game.mapH ),

                           }
squad['capt'].selected = True
selectable = ['capt','fwdr','fwdl','midr','midl']
statsBox            = statsBox(0,0,game.smallFont)


# -----Update game object
game.squad  = squad

# ****TurnDebug on/off***
game.debugSwitch = False 

# ---------------setup finished

game.itercount = 0
while game.running:
    game.itercount+=1

    screen.fill((0, 0, 0))
    drawImage(screen,game.map,(game.mapX-camera.x,game.mapY -camera.y))
    
    game.clicked = False
    # Reset the key each round
    user_input.returnedKey=''

    # Did the user click the window close button?
    for event in pygame.event.get():
        pos            = pygame.mouse.get_pos()
        if event.type == pygame.QUIT: game.running = False
        if event.type == pygame.MOUSEBUTTONDOWN: game.clicked  = True
        user_input     = modifyInput.manageButtons(event,user_input,game)

    # Update game with dynamic vars
    game.userInput  = user_input
    game.mx, game.my = pygame.mouse.get_pos()

    # ------------------------------








    #Update Football 
    fitba.updateSprite(game,camera)


    # Change Players
    if(game.userInput.returnedKey=='y'):
        for a in range(len(selectable)):
            if(game.squad[selectable[a]].selected==True):
                game.squad[selectable[a]].selected = False
                nextPlayer = a+1
                if(nextPlayer>=len(selectable)): nextPlayer = 0
                game.squad[selectable[nextPlayer]].selected = True
                break


    # Iterate thru players
    for s in game.squad:
        member = game.squad[s]
        if(member.selected): 
            player = member
        else:
            member.autoPlay(game,fitba,camera)

    

    # Selected Player
    player.play_selected(game,fitba,camera)
 

     # display debug box
    statsBox.display(['Name ' + str(player.name),
                      'Health ' + str(player.health),
                      'Armour ' + str(player.armour),
                      'Carrying ' + str(player.carryBall),
                      'Facing ' + str(player.facing),
                      'Position ' + str(player.x) + ','+str(player.y)],game),
        
   
    
    
    # update camera
    if(camera.target=='player'):

        camera.x = player.x + camera.offx
        camera.y = player.y + camera.offy
        
        # ---- Borders
        if(player.x>=(game.mapX+game.mapW)-100): player.x = (game.mapX+game.mapW)-100
        if(player.x<=(game.mapX)+100): player.x = (game.mapX)+100
        if(player.y>(game.mapY+ game.mapH)-100): player.y = (game.mapY+ game.mapH)-100
        if(player.y<(game.mapY)+100):player.y = (game.mapY)+100

        if(camera.x>(game.mapX+game.mapW)-game.width):camera.x = (game.mapX+game.mapW) -game.width
        if(camera.x<=(game.mapX)+100): camera.x = (game.mapX)+100
        if(camera.y>(game.mapY + game.mapH)-game.height):camera.y = (game.mapY+ game.mapH)-game.height
        if(camera.y<(game.mapY)):camera.y = (game.mapY)

        if(fitba.x>=(game.mapX+game.mapW)-100): fitba.x = (game.mapX+game.mapW)-100
        if(fitba.x<=(game.mapX)+100):           fitba.x = (game.mapX)+100
        if(fitba.y>(game.mapY+ game.mapH)-100): fitba.y = (game.mapY+ game.mapH)-100
        if(fitba.y<(game.mapY)+100):            fitba.y = (game.mapY)+100


    if(camera.target=='ball'):
        camera.x = fitba.x + camera.offx
        camera.y = fitba.y + camera.offy












    # Flip the display
    pygame.display.flip()
    # Tick
    game.dt           = clock.tick(FPS)
    game.gameElapsed += game.dt/1000

# Done! Time to quit.
pygame.quit()