import pyglet, resources
class PhysicalObject(pyglet.sprite.Sprite):

	def __init__(self, asize=0, *args, **kwargs):
		super(PhysicalObject, self).__init__(*args, **kwargs)
		
		self.velocity_x, self.velocity_y = 0.0, 0.0
		self.dead = False
		self.react_to_bullets = True
		self.asize = asize
		
	def update(self, dt):
		self.x += self.velocity_x * dt
		self.y += self.velocity_y * dt
		self.check_bounds()
		
	def check_bounds(self):
		min_x = 0 + self.image.width/2
		min_y = 0 + self.image.height/2
		max_x = 800 - self.image.width/2
		max_y = 600 - self.image.height/2
		
		if self.x < min_x:
			self.x = min_x
			self.velocity_x = -self.velocity_x
		if self.y < min_y:
			self.y = min_y
			self.velocity_y = -self.velocity_y
		if self.x > max_x:
			self.x = max_x
			self.velocity_x = -self.velocity_x
		if self.y > max_y:
			self.y = max_y
			self.velocity_y = -self.velocity_y
			
	def check_collide(self, other):
		col_distance = self.image.width/2.0 + other.width/2.0
		realdist = resources.distance(self.position, other.position)
		return (realdist <= col_distance)
		
	def handle_collision(self, other):
		if other.__class__ == self.__class__:
			self.dead = False
		else:
			self.dead = True
			
	def die(self):
		self.visible = False
		