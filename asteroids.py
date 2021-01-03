import pyglet, random
import resources, physicalobject, player

window = pyglet.window.Window(800,600)
mbatch = pyglet.graphics.Batch()
deadbatch = pyglet.graphics.Batch()

gamevars = {'lives':0, 'level' : 1, 'lives' : 3, 'score':0, 'retval':''}

info_label = pyglet.text.Label(text="Score: "+str(gamevars['score'])+" Level: "+str(gamevars['level']), x=10, y=575, batch=mbatch)
life_label = pyglet.text.Label(text="Lives:", x=785-(gamevars['lives']*40), y=575, batch=mbatch)

playership = player.Player(x=400, y=300, batch=mbatch)
asteroids = resources.make_asteroids(gamevars['level']+2, playership.position, mbatch)
gamevars['life_left'] = resources.lives_remain(gamevars['lives'],mbatch)
anykey = False

gameobjects = [playership] + asteroids
window.push_handlers(playership)
window.push_handlers(playership.key_handler)

def update(dt):
	global gamevars
	
	to_remove = []
	
	if len(asteroids) <= 0:
		if resources.levelComplete(playership, gamevars['level'], asteroids, mbatch) == True:
			gamevars['level'] += 1
			info_label.text = "Score: "+str(gamevars['score'])+" Level: "+str(gamevars['level'])

		
		
	for obj in asteroids:

		for blt in playership.bullets:
			if blt.check_collide(obj) and obj.react_to_bullets == True and blt.dead == False:
				blt.handle_collision(obj)
				obj.handle_collision(blt)
				obj.die()
				to_remove.append(obj)
				
				if obj.asize == 1: 
					gamevars['score'] += 10
							
					asteroids.extend(resources.make_small_asteroids(2,playership.position,obj,mbatch))
				if obj.asize == 2:
					gamevars['score'] += 5
				
				info_label.text = "Score: "+str(gamevars['score'])+" Level: "+str(gamevars['level'])
		
		if obj.check_collide(playership) == True and playership.visible == True:
			playership.die()
			gamevars['lives'] -= 1
			gamevars['life_left'].pop(gamevars['lives'])
	
		
		obj.update(dt)
	
	for blt in playership.bullets:
		blt.update(dt, playership.bullets)
		
	playership.update(dt)

	gamevars['retval'] = resources.checkDead(playership, gamevars, asteroids, deadbatch)
	if gamevars['retval'] == 2 and playership.dead == False:
		new_remove = []
		for old in asteroids:
			new_remove.append(old)
			old.delete()
		asteroids.remove(new_remove[0])
		del asteroids[:]
		asteroids.extend(resources.GameOver(gamevars, asteroids, playership, mbatch))
		
				
	if len(to_remove) > 0:
		delast = to_remove[0]
		asteroids.remove(delast)
	
	

@window.event
def on_draw():
	global gamevars
	window.clear()
	mbatch.draw()
	deadbatch.draw()
	
	
	if playership.levelcomplete == True:
		lvl_label = pyglet.text.Label(text="Level complete. Press spacebar to continue!", x=275, y=400)
		lvl_label.draw()
		
	if gamevars['retval'] == 1:
		start_label = pyglet.text.Label(text="You died. Press Space to Restart!", x=300, y=300)
		start_label.draw()
	if gamevars['retval'] == 2: 
		start_label = pyglet.text.Label(text="Game Over. Press Space to Restart!", x=300, y=300)
		start_label.draw()



if __name__ == '__main__':
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.app.run()