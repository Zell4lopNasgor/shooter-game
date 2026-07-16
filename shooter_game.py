from pygame import *
from random import randint

win_width = 700 
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Shooter game by Zellalala')
background = transform.scale(image.load("bg sunset.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load("Dawn.ogg")
mixer.music.set_volume(0.2)
mixer.music.play()

font.init()
font1 = font.Font(None, 35)
missed = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
         
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            missed = missed + 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
            
    
player = Player('roket.png', 5, win_height-100, 65, 65, 8)
enemies = sprite.Group()
for i in range(1,6):
    enemy = Enemy('ufoo.png', randint(80, win_width-80), -50, 80, 50, randint(1,3))
    enemies.add(enemy)
    
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(80, win_width-80), -50, 80, 50, randint(1,2))
    asteroids.add(asteroid)
    
bullets = sprite.Group()
    
clock = time.Clock()
FPS = 60
run = True
finish = False

num_fire = 0
reaload_time = False
life = 5

fire_sound = mixer.Sound('fire.ogg')

from time import time as timer

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and reaload_time == False:
                    num_fire = num_fire + 1
                    fire_sound.set_volume(0.3)
                    fire_sound.play()
                    player.fire()
                if num_fire >= 10 and reaload_time == False:
                    last_time = timer()
                    reaload_time = True
                
            
    if not finish:  
        window.blit(background,(0,0))
        text_score = font1.render('Score: '+ str(score), 1, (255,255,255))
        window.blit(text_score, (10, 20))
        text_missed = font1.render('Missed: '+ str(missed), 1, (255,255,255))
        window.blit(text_missed, (win_width-150, 20))
        
        if life == 5:
            life_color = (50, 250, 50)
        if life == 4:
            life_color = (150, 200, 50)
        if life == 3:
            life_color = (150, 150, 50)
        if life == 2:
            life_color = (180, 90, 50)
        if life == 1:
            life_color = (200, 30, 30)
            
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (350, 10))
        
        player.reset()
        player.update()
        enemies.draw(window)
        enemies.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        
        if reaload_time == True:
            now_time = timer()
            if now_time - last_time < 3 :
                reload_text = font1.render("Wait, reload...", 1, (180,0,80))
                window.blit(reload_text, (240, 460))
            else:
                num_fire = 0
                reaload_time = False
        
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score = score + 1
            enemy = Enemy('ufoo.png', randint(80, win_width-80), -50, 80, 50, randint(1,3))
            enemies.add(enemy)
            
        if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, enemies, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1
                    
        if life == 0 or missed > 20:
            finish = True
            font2 = font.Font(None, 75)
            lose = font2.render("YOU LOSE AHAHAH", True, (180,0,80))
            window.blit(lose, (85, 200))
            
        if score > 15:
            finish = True
            font2 = font.Font(None, 100)
            win = font2.render("YOU WIN YAY", True, (250,200,140))
            window.blit(win, (125, 200))
    
        
        display.update()
    
    else:
        finish = False
        score = 0
        missed = 0
        life = 5
        num_fire = 0
        for peluru in bullets:
            peluru.kill()
        for musuh in enemies:
            musuh.kill()
            
        time.delay(5000)
        for i in range(1,6):
            enemy = Enemy('ufoo.png', randint(80, win_width-80), -50, 80, 50, randint(1,3))
            enemies.add(enemy)
        
    clock.tick(FPS)
        