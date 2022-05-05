
class sprite():
    def __init__(self,imageFrames,x,y):
        self.imageFrames = imageFrames
        self.numFrames   = len(self.imageFrames)
        self.framePos    = 0
        self.x           = x
        self.y           = y
        self.w           = self.imageFrames[0].get_rect().w
        self.h           = self.imageFrames[0].get_rect().h
        self.vx          = 0
        self.vy          = 0
        self.frameTime   = 0
        self.carried     = False

    def animate(self,game,camera, interval=0.5):
        """
        animages image every interval (in seconds)
        once image reaches end, it resets to first image
        """
        
        # incremented timer
        self.frameTime += game.dt/1000
        
        # increment frame when interval reached
        if(self.frameTime>=interval):
            self.framePos  +=1
            self.frameTime  = 0
        
        # wrap image around
        if(self.framePos>=self.numFrames): 
            self.framePos=0
        

        game.screen.blit(self.imageFrames[self.framePos],(self.x-camera.x,self.y-camera.y))



class fitbaObject():
    """
    takes in sprite classs from utils
    """
    def __init__(self,football):
        self.sprite             = football
        self.x                  = self.sprite.x
        self.y                  = self.sprite.y
        self.w                  = self.sprite.w
        self.h                  = self.sprite.h
        self.kick               = None
        self.kicked             = False
        self.defaultKickSpeed   = 30
        self.kickSpd            = self.defaultKickSpeed 
    
    def kickBall(self,kickDirection,inc=2):
        """
        self.kick is the direction, it needs resetting at the end
        """
        
        #print('self.kicked ' + str(self.kicked))
        #print('self.kick ' + str(self.kick))
        #print('kickDirection ' + str(kickDirection))
        #print('kickSpd ' + str(self.kickSpd))
        #print(' ')


        if(self.kicked):
            if(kickDirection=='down'): 
                self.y+=self.kickSpd
            if(kickDirection=='up'): 
                self.y-=self.kickSpd
            if(kickDirection=='left'): 
                self.x-=self.kickSpd
            if(kickDirection=='right'): 
                self.x+=self.kickSpd

            if(kickDirection=='ur'): 
                self.y-=self.kickSpd
                self.x+=self.kickSpd
            if(kickDirection=='ul'): 
                self.y-=self.kickSpd
                self.x-=self.kickSpd
            if(kickDirection=='dl'): 
                self.y+=self.kickSpd
                self.x-=self.kickSpd
            if(kickDirection=='dr'): 
                self.y+=self.kickSpd
                self.x+=self.kickSpd




            self.kickSpd -=1
            if(self.kickSpd<0.5):
                self.kicked  = False
                self.kickSpd = self.defaultKickSpeed 
                self.kick=None
    


    def updateSprite(self,game,camera):

        self.sprite.x,self.sprite.y = self.x,self.y
        self.sprite.animate(game,camera)

        if(self.kick!=None): self.kicked = True 
        
        self.kickBall(self.kick)