import pyglet, math, random, time
import physicalobject
from pyglet.window import key

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

	
def center(image):
	image.anchor_x = image.width/2
	image.anchor_y = image.height/2

try:
	player_img = pyglet.resource.image("ship.png")
	bullet_img = pyglet.resource.image("bullet.jpg")
	asteroid_img = pyglet.resource.image("asteroid.png")
	asteroid_img_small = pyglet.resource.image("asteroid_sm.png")
	eng_flame = pyglet.resource.image("eng_flame.png")
	
	center(player_img)
	center(bullet_img)
	center(asteroid_img)
	center(asteroid_img_small)
	eng_flame.anchor_x = eng_flame.width/2
	eng_flame.anchor_y = eng_flame.height * 4

except pyglet.resource.ResourceNotFoundException:
	print ("Image Resources not found. Trying to execute anyway...")


def make_asteroids(number, playerpos, batch=None):
	asteroids = []
	for i in range(number):
		astx = random.randint(0,800)
		asty = random.randint(0,600)
		while get_distance((astx,asty),playerpos) < 100:
			astx = random.randint(0,800)
			asty = random.randint(0,600)
		new_ast = physicalobject.PhysicalObject(img=asteroid_img, x=astx, y=asty, batch=batch, asize=1)
		new_ast.rotation = random.randint(0,360)
		new_ast.velocity_x = random.random()*40
		new_ast.velocity_y = random.random()*40
		asteroids.append(new_ast)
	return asteroids

def make_small_asteroids(number, playerpos, aster, batch=None):
	asteroids = []
	for i in range(number):
		astpos = aster.position
		new_ast = physicalobject.PhysicalObject(img=asteroid_img_small, x=aster.x, y=aster.y, batch=batch, asize=2)
		new_ast.rotation = random.randint(0,360)
		new_ast.velocity_x = random.random() * aster.velocity_x * random.randint(1,4)
		new_ast.velocity_y = random.random() * aster.velocity_y * random.randint(1,4)
		asteroids.append(new_ast)
	return asteroids

def get_distance(point1=(0,0), point2=(0,0)):
	return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
	
def lives_remain(icons, batch=None):
	player_lives = []
	for i in range(icons):
		lifeShip = pyglet.sprite.Sprite(img=player_img, x=785-i*30, y=580, batch=batch)
		lifeShip.scale = 0.5
		player_lives.append(lifeShip)
	return player_lives
	
def distance(point1=(0,0), point2=(0,0)):
	return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
	
def checkDead(player, gamevar, gameobj, batch=None):
	retval = 0
	if player.dead == True:
		restart = False
	
		if gamevar['lives'] > 0:
			retval = 1
		else:
			retval = 2

		if player.key_handler[key.SPACE]:
			player.dead = False
			player.respawn()
	return retval


def levelComplete(player, lvl, ast, batch=None):
	player.levelcomplete = True
	if player.key_handler[key.SPACE]:
		ast.extend(make_asteroids(lvl+3, player.position, batch=batch))
		player.levelcomplete = False
		return True

def GameOver(gamevar, oldast, playerobj, batch=None):
	gamevar['score'] = 0
	gamevar['lives'] = 3
	gamevar['level'] = 1
	
	gamevar['life_left'] = lives_remain(gamevar['lives'], batch)
	
	return make_asteroids(3, playerobj.position, batch)