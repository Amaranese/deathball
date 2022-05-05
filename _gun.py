from _utils                 import *

class _bullet():
	"""
	Initialised by gun class (below)
	"""
	def __init__(self,x,y,v,muzzle,image,impact,direction,shooter,damage):
		self.x          = x
		self.y          = y
		self.vx         = v
		self.vy         = v
		self.muzz       = muzzle
		self.image      = image
		self.impact     = impact
		self.direction  = direction
		self.shooter	= shooter
		self.damage     = damage

		# default
		self.state      = None
		self.mzleCount  = 0


		# angle bullet
		angle = 0
		if(self.direction=='u'): angle=90
		if(self.direction=='d'): angle=270
		if(self.direction=='r'): angle=0
		if(self.direction=='l'): angle=180
		if(self.direction=='ur'): angle=45
		if(self.direction=='ul'): angle=135
		if(self.direction=='dr'): angle=315
		if(self.direction=='dl'): angle=225

		self.image = pygame.transform.rotate(self.image, angle)
		self.muzzle = []
		for m in self.muzz: self.muzzle.append(pygame.transform.rotate(m, angle))
		self.impactS = []
		for i in self.impact: self.impactS.append(pygame.transform.rotate(i, angle))


	def fire(self,game,camera):
		"""
		Called by Gun object
		"""

		# -----muzzle flash

		if(self.state==None):
			drawImage(game.screen,self.muzzle[self.mzleCount],(self.x-camera.x,self.y-camera.y))
			self.mzleCount+=1
			if(self.mzleCount>= len(self.muzzle)):
				self.state='firing'

		# ------Firing
		if(self.state=='firing'):
			if(self.direction=='u'):
				self.y -= self.vy
			if(self.direction=='d'):
				self.y += self.vy
			if(self.direction=='l'):
				self.x -= self.vx
			if(self.direction=='r'):
				self.x += self.vx
			# diagonals
			if(self.direction=='ur'):
				self.y -= self.vy
				self.x += self.vx
			if(self.direction=='ul'):
				self.y -= self.vy
				self.x -= self.vx
			if(self.direction=='dr'):
				self.y += self.vy
				self.x += self.vx
			if(self.direction=='dl'):
				self.y += self.vy
				self.x -= self.vx
			
			# -----------Collissions
			for m in game.squad:
				member = game.squad[m]
				if(member.name ==self.shooter):
					continue
				if(game.collides((self.x,self.y),member.x,member.y,member.w,member.h)):
					self.state     ='impacted'
					member.takeDamage(self.damage)




			drawImage(game.screen,self.image,(self.x-camera.x,self.y-camera.y))




class pgun():
	def __init__(self):
		self.image       = impFilesL('pBullets1.png',tDir='sprites/bullets/')
		self.x           = None
		self.y           = None
		self.direction   = None
		self.fired       = False
		self.created     = False
		self.timeCreated = None
		self.bullets     = []

	def kill(self):
		"""
		Cleans up bullets 
		"""
		for i in range(0,len(self.bullets)):
			try:
				if(self.bullets[i]!= None and ((self.bullets[i].x>3000) or (self.bullets[i].x<-3000) or (self.bullets[i].y>3000) or (self.bullets[i].y<-3000))): 
					del self.bullets[i]
			except:
				pass
		for i in range(0,len(self.bullets)):
			try:
				if(self.bullets[i].state=='impacted'):
					del self.bullets[i]
			except:
				pass



	def shoot(self,x,y,direction,game,shoot,shooter,camera):
		"""
		Creates a bullet object
		cleans up
		"""
		
		# Cyclic Firing (bullets need init only once)
		if(self.fired==False and shoot):
			self.fired       = True
			self.timeCreated = game.gameElapsed
			self.bullets.append(_bullet(x,y,25,self.image[:2],self.image[2],self.image[2:],direction,shooter,5))
			self.bullets = [x for x in self.bullets if x!=None]


		self.kill()


		# Fire bullets
		for i in range(0,len(self.bullets)): self.bullets[i].fire(game,camera)
			
		# Reseting to create another
		if((self.fired) and (game.gameElapsed-self.timeCreated>0.2)):
			self.fired       =False
			self.timeCreated = None
