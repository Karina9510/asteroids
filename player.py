import physicalobject, resources, math, pyglet, bullet, time
from pyglet.window import key

class Player(physicalobject.PhysicalObject):
	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=resources.player_img, *args, **kwargs)
		
		self.thrust = 100.0
		self.rotate_speed = 200.0
		self.keys = dict(left=False, right=False, up=False)
		self.key_handler = key.KeyStateHandler()
		self.eng_sprite = pyglet.sprite.Sprite(img=resources.eng_flame, *args, **kwargs)
		self.eng_sprite.visible = False
		self.bullets = []
		self.lastfire = time.time()
		self.firerate = 0.4
		self.maxspeed = 100.0
		self.bulletspeed = 420.0
		self.react_to_bullets = False
		self.levelcomplete = False
			
	def update(self, dt):
		super(Player, self).update(dt)
				
		if self.key_handler[key.LEFT]:
			self.rotation -= (self.rotate_speed * dt)
		if self.key_handler[key.RIGHT]:
			self.rotation += (self.rotate_speed * dt)
			
		
		if self.key_handler[key.UP]:
			angle_radians = -math.radians(self.rotation-90)
			fx = math.cos(angle_radians) * self.thrust * dt
			fy = math.sin(angle_radians) * self.thrust * dt
			self.velocity_x += fx
			self.velocity_y += fy
			self.check_magnitude()
			
			self.eng_sprite.rotation = self.rotation
			self.eng_sprite.x = self.x
			self.eng_sprite.y = self.y
			
			if self.dead == False:
				self.eng_sprite.visible = True
		else:
			self.eng_sprite.visible = False

		if self.key_handler[key.DOWN]:
			angle_radians = -math.radians(self.rotation-90)
			fx = math.cos(angle_radians) * self.thrust * dt
			fy = math.sin(angle_radians) * self.thrust * dt
			self.velocity_x -= fx
			self.velocity_y -= fy
			self.check_magnitude()

			
		if self.key_handler[key.SPACE]:
			if ((time.time() - self.lastfire) >= self.firerate):
				self.lastfire = time.time()
				if self.dead == False:
					self.fire()
		
	
	def respawn(self):
		self.visible = True
		self.x = 400
		self.y = 300
		self.velocity_x, self.velocity_y = 0,0
			
	def die(self):
		self.bullets = []
		self.eng_sprite.visible = False
		self.visible = False
		self.dead = True
		#super(Player, self).delete()
	
	def check_magnitude(self):		
		magnitude = math.sqrt((self.velocity_x **2) + (self.velocity_y **2))
		if magnitude > self.maxspeed:
			self.velocity_x *= self.maxspeed/magnitude
			self.velocity_y *= self.maxspeed/magnitude
			
	def fire(self):
			ship_radius = self.image.width/2
			angle_radians = -math.radians(self.rotation-90)
			bullet_x = self.x + math.cos(angle_radians) * ship_radius
			bullet_y = self.y + math.sin(angle_radians) * ship_radius
			bulletvx = self.velocity_x + math.cos(angle_radians) * self.bulletspeed
			bulletvy = self.velocity_y + math.sin(angle_radians) * self.bulletspeed
							
			newbullet = bullet.Bullet(x=bullet_x, y=bullet_y, batch=self.batch)
			newbullet.velocity_x, newbullet.velocity_y = bulletvx, bulletvy
			self.bullets.append(newbullet)