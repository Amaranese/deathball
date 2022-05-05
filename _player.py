from _gun import * 


class playerObject():
    """
    takes in playersprite classs from utils
    """
    def __init__(self,name,playerSprite,x,y,vx,vy,originX,originY):
        self.name               = name
        self.sprite             = playerSprite
        self.x                  = x
        self.y                  = y
        self.vx                 = vx
        self.vy                 = vy
        self.ballpos            = []
        self.facing             = 'u'
        self.stationary         = True
        self.carryBall          = False
        self.pGun               = pgun()
        self.w                  = playerSprite.w
        self.h                  = playerSprite.h
        self.selected           = False           # Not used

        self.health             = 100
        self.armour             = 50


        # ------ Bot behaviour
        self.origin                 = {'x':originX,'y':originY}
        self.botState               = 'origin'
        self.r,self.l,self.u,self.d = False,False,False,False



    def play_selected(self,game,fitba,camera=None):

        # Draw Selected Icon
        game.selectedIconIndex,game.selectedIcnWait = game.animate(self.x+0.3*self.w,self.y-50,game.selectedIcon, game.selectedIconIndex,camera,game.selectedIcnWait,200)

        #self.sprite.animate(game,stop=True)
        self.stationary = (game.userInput.up==False and game.userInput.down==False and game.userInput.left==False and game.userInput.right==False)
        

        # Manage Velocity
        if(game.userInput.up):    
            self.y -= self.vy
            self.facing = 'u'
        if(game.userInput.down):  
            self.y += self.vy
            self.facing = 'd'
        if(game.userInput.left):  
            self.x -= self.vx
            self.facing = 'l'
        if(game.userInput.right): 
            self.x += self.vx
            self.facing = 'r'

        if(game.userInput.up and game.userInput.left):    self.facing = 'ul'
        if(game.userInput.up and game.userInput.right):   self.facing = 'ur'
        if(game.userInput.down and game.userInput.left):  self.facing = 'dl'
        if(game.userInput.down and game.userInput.right): self.facing = 'dr'


        # -------check if colliding with ball
        colliding = self.collides((self.x,self.y),fitba)
        if(colliding and self.carryBall==False):
            self.carryBall = True
        
        inRange   = self.inRange((self.x,self.y),fitba)
        
        # ------ dribble ball
        self.dribble(self.carryBall,fitba,inRange,game)

        self.fireGun(game,camera)
        
        # -------update position
        self.updateSprite(game)

        # ------Animate
        self.sprite.animate(game,self.facing,camera,stop=self.stationary)

    def autoPlay(self,game,fitba,camera=None):

        #self.sprite.animate(game,stop=True)
        self.stationary = (self.r==False and self.l==False and self.u==False and self.d==False)
        
        # -------check if colliding with ball
        colliding = self.collides((self.x,self.y),fitba)
        if(colliding and self.carryBall==False):
            self.carryBall = True
            fitba.carried = True
        
        inRange   = self.inRange((self.x,self.y),fitba)
        
        # Set Direction, set  velocity
        self.u,self.d,self.l,self.r = False,False,False,False
        
        #--------Default behaviour
        if(self.botState=='origin'):
            if(self.x<self.origin['x']): self.r = True
            if(self.x>self.origin['x']): self.l = True
            if(self.y<self.origin['y']): self.d = True
            if(self.y>self.origin['y']): self.u = True


        # Set Running and facing
        if(self.u): 
            self.y -= self.vy
            self.facing = 'u'
        if(self.d): 
            self.y += self.vy
            self.facing = 'd'
        if(self.l): 
            self.x -= self.vx
            self.facing = 'l'
        if(self.r): 
            self.x += self.vx
            self.facing = 'r'
        
        if(self.u and self.l): self.facing = 'ul'
        if(self.u and self.r): self.facing = 'ur'
        if(self.d and self.l): self.facing = 'dl'
        if(self.d and self.r): self.facing = 'dr'

        print(self.stationary)
        # -------update position
        self.updateSprite(game)

        # ------Animate
        self.sprite.animate(game,self.facing,camera,stop=self.stationary)



    def updateSprite(self,game):
        self.sprite.x,self.sprite.y = self.x,self.y



    def dribble(self,carryBall,fitba,inRange,game,bounce=1):
        
        # Ball follows player if true
        if(carryBall==True): fitba.x,fitba.y = self.x,self.y

        # Set ball direction if kicked
        if(game.userInput.kick and carryBall==True):
            self.carryBall='kick'
            if(self.facing=='u'): fitba.kick  ='up'
            if(self.facing=='d'): fitba.kick  ='down'
            if(self.facing=='l'): fitba.kick  ='left'
            if(self.facing=='r'): fitba.kick  ='right'

            if(self.facing=='ur'): fitba.kick  ='ur'
            if(self.facing=='ul'): fitba.kick  ='ul'
            if(self.facing=='dr'): fitba.kick  ='dr'
            if(self.facing=='dl'): fitba.kick  ='dl'





        # After kicking and ball is out of sphere, reset
        if(self.carryBall=='kick' and inRange==False):
            self.carryBall =False
            fitba.carried  = False

    
        

    def inRange(self,playerPos,otherObj):
        x,y,w,h = otherObj.x,otherObj.y,otherObj.w,otherObj.h
        px,py,pw,ph = playerPos[0],playerPos[1],self.sprite.w,self.sprite.h
        
        playerRightside    = px+pw
        playerLeftSide     = px-pw
        playerBottomSide   = py+1.5*ph
        playerTopSide      = py-0.5*ph
        if x > playerLeftSide and x < playerRightside:
            if y > playerTopSide and y < playerBottomSide:
                return(True)
        return(False)

    def collides(self,playerPos,otherObj):
        x,y,w,h = otherObj.x,otherObj.y,otherObj.w,otherObj.h
        px,py,pw,ph = playerPos[0],playerPos[1],self.sprite.w,self.sprite.h
        
        playerRightside    = px+0.5*pw
        playerLeftSide     = px-0.5*pw
        playerBottomSide   = py+ph
        playerTopSide      = py

        # get ball relative pos
        self.ballpos = []
        if(x>playerRightside): self.ballpos.append('l')
        if(x<playerLeftSide):  self.ballpos.append('r')
        if(y<playerTopSide):   self.ballpos.append('u')
        if(y>playerTopSide):   self.ballpos.append('d')

        # check if collides
        if x > playerLeftSide and x < playerRightside:
            if y > playerTopSide and y < playerBottomSide:
                return(True)
        return(False)

    def fireGun(self,game,camera):
        """calls guns shoot method """
        self.pGun.shoot(self.x,self.y, self.facing,game,game.userInput.fire,self.name,camera)
    
    def takeDamage(self,damage):
        """called by impacting bullet"""
        if(self.armour>0): self.armour -= damage
        if(self.armour<1): self.health -= damage

    













class playerSprite():
    def __init__(self,imageFrames):
        self.imageFrames        = imageFrames
        
        self.downF              = self.imageFrames[:6]
        self.upF                = self.imageFrames[6:12]
        self.rightF             = self.imageFrames[12:18]
        self.leftF              = self.imageFrames[18:24]
        self.urF                = self.imageFrames[24:30]
        self.ulF                = self.imageFrames[30:36]
        self.dlF                = self.imageFrames[36:42]
        self.drF                = self.imageFrames[42:]


        self.liveFrames         = self.downF
        self.numFrames          = len(self.downF)

        self.framePos           = 0
        self.x                  = 0
        self.y                  = 0
        self.w                  = self.imageFrames[0].get_rect().w
        self.h                  = self.imageFrames[0].get_rect().h
        self.frameTime          = 0



        self.currentDirection   = None



    

    def getDirection(self,facing):

        direction = None
        if(facing=='u'): self.liveFrames = self.upF
        if(facing=='d'): self.liveFrames = self.downF
        if(facing=='l'): self.liveFrames = self.leftF
        if(facing=='r'): self.liveFrames = self.rightF
        if(facing=='ur'): self.liveFrames = self.urF
        if(facing=='ul'): self.liveFrames = self.ulF
        if(facing=='dr'): self.liveFrames = self.drF
        if(facing=='dl'): self.liveFrames = self.dlF
        


        direction = facing
        return(direction)




    def animate(self,game,facing,camera,interval=0.2,stop=False):
        """
        animages image every interval (in seconds)
        once image reaches end, it resets to first image
        """

        # Update direction Frames
        direction = self.getDirection(facing)


        # --------change sprite templates
        if(self.currentDirection!=direction):
            self.currentDirection = direction
            self.framePos = 0
            self.numFrames = len(self.liveFrames)


        

        if(stop):
            game.screen.blit(self.liveFrames[0],(self.x- camera.x,self.y- camera.y))
            return()
        

        #-----------animate
        # incremented timer
        self.frameTime += game.dt/1000
        
        # increment frame when interval reached
        if(self.frameTime>=interval):
            self.framePos  +=1
            self.frameTime  = 0
        
        # wrap image around
        if(self.framePos>=self.numFrames): 
            self.framePos=0
        
        game.screen.blit(self.liveFrames[self.framePos],(self.x - camera.x,self.y- camera.y))

