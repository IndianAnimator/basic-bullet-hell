import pygame, random, math


class Config(object):
	fullscreen = True
	width = 1920
	height = 1080
	fps = 60


class Player(pygame.sprite.Sprite):  #player class
	s = (pygame.K_s)
	w = (pygame.K_w)
	d = (pygame.K_d)
	a = (pygame.K_a)
	
	def __init__(self, startpos=(102, 579), hp=100,	atk=10, bulk=0, dex=30, speed=0):
		super().__init__()
		self.hp = hp
		self.pos = list(startpos)
		self.atk = 0.5 + (atk / 50)
		self.orig_dex = dex
		self.dex = round(75 / 6.5 * self.orig_dex)
		self.bulk = bulk
		self.speed = round(4 + 5.6 * (speed / 75))
		self.image = pygame.image.load('player.png')
		self.orig_image = self.image
		self.rect = self.image.get_rect(center=startpos)
		
	def shoot(self, pos, bullet_img, angle):
		bullet = Bullet(pos, bullet_img, angle)
		all_sprites_list.add(bullet)
		bullets.add(bullet)
	
	def update(self):
		self.dex = 75 / 6.5 * self.orig_dex
		pressedkeys = pygame.key.get_pressed()
		if pressedkeys[self.s]:
			self.rect.y += self.speed
		if pressedkeys[self.w]:
			self.rect.y -= self.speed
		if pressedkeys[self.a]:
			self.rect.x -= self.speed
		if pressedkeys[self.d]:
			self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):  #enemy class

	def __init__(self, img, damage=1):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.damage = damage
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(200, Config.width)
		self.rect.y = random.randrange(200, Config.height)
		self.speedy = random.randrange(3, 6)
		
	def update(self):
		dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
		dist = math.hypot(dx, dy)
		if dist == 0:
			dist = 1
		dx, dy = dx / dist, dy / dist
		self.rect.x += dx * self.speedy
		self.rect.y += dy * self.speedy
		if (self.rect.right > 1920 or self.rect.left < 0 or self.rect.bottom > 1080 or self.rect.top < 0):
			self.rect.x = 1920


class Bullet(pygame.sprite.Sprite):  #bullet class

	def __init__(self, pos, img, angle = 0, speed = 10, acceleration = 0, curve = 30, curve_mod = 0):
		super().__init__()
		if curve > 0 or curve_mod > 0:
			angle = 0
		self.dir = angle
		self.angle = (180 / math.pi) * -self.dir - 90
		#turns towards the mouse
		self.image = pygame.transform.rotate(img, self.angle)
		self.rect = self.image.get_rect()
		self.pos = list(pos)
		self.spd = speed
		self.acl = acceleration
		self.curve = curve
		self.curve_mod = curve_mod
		#start lifetime of bullet
		self.born = pygame.time.get_ticks()
		
	
	def update(self):
		#destroys itself if more than 10 secs have past from birth
		self.live = pygame.time.get_ticks() - self.born
		if self.live > 5000:
			bullets.remove(self)
			all_sprites_list.remove(self)
			
		#move the bullet
		if self.curve == 0:
			self.pos[0] += math.cos(self.dir) * (self.spd)
			self.pos[1]+= math.sin(self.dir) * (self.spd)
		else:	
			r = self.dir ** 0.5
			self.pos[0] += r * math.cos(math.radians(self.dir))
			self.pos[1]+= r * math.sin(math.radians(self.dir))
		
		self.rect.center = int(self.pos[0].real), int(self.pos[1].real)
		#update stats of bullet
		self.dir += self.curve
		self.spd += self.acl
		self.curve += self.curve_mod
		if self.curve > 360:
			self.curve = self.curve % 360
			
class Pattern(pygame.sprite.Sprite):
		def __init__(self, pos, img, radius, speed, num_bullets, angle_offset=0, acceleration = 0, curve = 30, curve_mod = 0):
				super().__init__()	
				self.pos = pos
				self.img = img
				self.radius = radius
				self.speed = speed
				self.num_bullets = num_bullets
				self.angle_offset = angle_offset
				self.acl = acceleration
				self.curve = curve
				self.curve_mod = curve_mod
				

		def shoot(self):
				for i in range(self.num_bullets):
						angle = (360 / self.num_bullets+1) * i + self.angle_offset
						# Calculate the x and y offset based on the angle
						x_offset = math.cos(angle) * self.radius
						y_offset = math.sin(angle) * self.radius
						# Calculate the starting position for the bullet
						start_pos = (self.pos[0] + x_offset, self.pos[1] + y_offset)
						bullet = Bullet(start_pos, self.img, angle, self.speed, self.acl, self.curve, self.curve_mod)
						all_sprites_list.add(bullet)
						bullets.add(bullet)

					
class Boss(pygame.sprite.Sprite):

	def __init__(self, img, startpos=(102, 579)):
		super().__init__()
		self.image = img
		self.rect = self.image.get_rect()
		self.pos = list(startpos)
		self.damage = 30
		self.spd = 7
	
	def update(self):
		dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
		dist = math.hypot(dx, dy)
		if dist == 0:
			dist = 1
		dx, dy = dx / dist, dy / dist
		self.rect.x += dx * self.spd
		self.rect.y += dy * self.spd



player = Player()

#add imgs
enemy_img = pygame.image.load('evilpizzaman.png')
bullet_img = pygame.image.load("pbullet.png")
ebullet_img = pygame.image.load("ebullet.png")
boss_img = pygame.image.load("pizza.png")

#create groups
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
for x in range(0, 11):
	enemy = Enemy(enemy_img)
	enemies.add(enemy)

# all sprite handling list
all_sprites_list = pygame.sprite.Group()
allgroup = pygame.sprite.LayeredUpdates()
allgroup.add(player)

#create enemies
for i in enemies:
	all_sprites_list.add(i)


def main():
	#INTILIZE PYGAME
	pygame.init()
	screen = pygame.display.set_mode((Config.width, Config.height))
	pygame.display.set_caption("basic bullet hell")
	
	font = pygame.font.Font('freesansbold.ttf', 64)
	
	prev_time = pygame.time.get_ticks()
	boss_spawn = 0
	mainloop = True
	while mainloop:  #control handling
		clock = pygame.time.Clock()
	
		millisecond = clock.tick(Config.fps)
		for event in pygame.event.get():
			pressedkeys = pygame.key.get_pressed()
			if event.type == pygame.QUIT:
				mainloop = False
			if pressedkeys[pygame.K_SPACE]:
				pattern = Pattern(player.rect.center, bullet_img, radius=100, speed=10, num_bullets=10, angle_offset=45)
				pattern.shoot()


			mouse_x, mouse_y = pygame.mouse.get_pos()
			
			distance_x = mouse_x - player.rect.x
			distance_y = mouse_y - player.rect.y
			
			angle = math.atan2(distance_y, distance_x)

		current_time = pygame.time.get_ticks()
		if current_time - prev_time >= 667 - player.dex:
			player.shoot((player.rect.x, player.rect.y), bullet_img,angle)
			prev_time = current_time
		
		#update graphics
		screen.fill((0, 0, 0))
		
		for bullet in bullets:
			if bullet.rect.x > Config.width or bullet.rect.y > Config.height or bullet.rect.x < 0 or bullet.rect.y < 0:
				bullets.remove(bullet)
				all_sprites_list.remove(bullet)
		
		kill_list = pygame.sprite.groupcollide(enemies, bullets, True, True)
		game_over = pygame.sprite.groupcollide(allgroup, enemies, False, False)
		if bool(kill_list) == True:
			boss_spawn += 1
			buff = random.randrange(0, 3)
			if buff == 0:
				player.bulk += random.randrange(1, 3)
				print("bulk", player.bulk)
			if buff == 1:
				player.orig_dex += random.randrange(5, 10)
				print("orig_dex", player.orig_dex)
				print("dex", player.dex)
			if buff == 2:
				player.speed += random.randrange(1, 3)
				print("speed", player.speed)
		elif boss_spawn == 10:
			boss = Boss(boss_img)
			enemies.add(boss)
			all_sprites_list.add(boss)
		elif bool(game_over) == True:
			if player.bulk >= enemy.damage:
				player.hp -= round(enemy.damage * 0.1)
			else:
				player.hp -= enemy.damage - player.bulk
			print(player.hp)
		if player.hp <= 0:
			allgroup.remove(player)
		if len(allgroup) == 0:
			game_over_text = font.render("GAME OVER", True, (255, 255, 255))
			screen.blit(game_over_text, (Config.width / 2, Config.height / 2))
			pygame.display.update()
		elif len(enemies) == 0:
			game_over_text = font.render("YOU WIN!", True, (255, 255, 255))
		allgroup.update()
		all_sprites_list.update()
		allgroup.draw(screen)
		all_sprites_list.draw(screen)
		pygame.display.update()
				
		

print("wasd to move. Objective is to kill all enemies on screen")
main()
pygame.quit()
