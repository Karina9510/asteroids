import physicalobject, resources, math, pyglet, time

class Bullet(physicalobject.PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Bullet, self).__init__(img=resources.bullet_img, *args, **kwargs)
		pyglet.clock.schedule_once(self.die, 2.0)
		
	def update(self, dt, bulletlist):
		self.checkbounds(bulletlist)

		self.x += self.velocity_x * dt
		self.y += self.velocity_y * dt
					
		if self.dead == True:
			bulletlist.remove(self)
			super(Bullet, self).delete()

			
	def die(self, poop=0):
		self.dead = True
				
	def checkbounds(self, bulletlist):
		#super (Bullet, self).check_bounds()
		min_x = 0
		min_y = 0
		max_x = 800
		max_y = 600
		
		if self.x <= min_x:
			self.die()
		if self.y <= min_y:
			self.die()
		if self.x >= max_x:
			self.die()
		if self.y >= max_y:
			self.die()
