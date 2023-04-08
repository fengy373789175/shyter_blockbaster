#Создай собственный Шутер!

from pygame import *
from random import *
from time import sleep
from time import time as timer

window = display.set_mode ((1200, 800))
display.set_caption('тише-тише')
backround = transform.scale(image.load('galaxy.jpg'), (1200, 800))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (115, 110))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self): 
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < 1100:
            self.rect.x += self.speed
    def fire(self):
        keys = key.get_pressed()
        
        bullets.add(Bullet('bullet.png', 50, self.rect.x, self.rect.y))
    
            
        

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y == window.get_size()[1]:
            self.rect.y = 0
            self.rect.x = randint(0, window.get_size()[0])
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y == window.get_size()[1]:
            self.rect.y = 0
            self.rect.x = randint(0, window.get_size()[0])


counter = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == window.get_size()[1]:
            self.kill()
    




font.init()
mixer.init()
mixer.music.load('Zxcursed_New_era.mp3')
mixer.music.play()

font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 42)
font3 = font.SysFont('Arial', 50)
font4 = font.SysFont('Arial', 60)

num_fire = 0

rel_time = False


bullets = sprite.Group()

hero = Player('rocket.png', 20, 550, 680)
ufos = sprite.Group()

asteroid = sprite.Group()

for i in range(2):
    asteroid.add(Enemy('asteroid.png', 10, randint(0, window.get_size()[0]-60), 0))

for i in range(5):
    ufos.add(Enemy('ufo.png', 10, randint(0, window.get_size()[0]-60), 0))


clock = time.Clock()
game = True
while game:
    for y in event.get():
        if y.type == QUIT:
            game = False
        elif y.type == KEYDOWN:
            if y.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire = num_fire + 1
                    hero.fire()
                if num_fire >= 5 and rel_time:
                    last_time = timer()
                    rel_time = True


    window.blit(backround,(0, 0))
    clock.tick(60)
    hero.reset()
    hero.update()

    ufos.update()
    ufos.draw(window)

    bullets.update()
    bullets.draw(window)

    asteroid.update()
    asteroid.draw(window)

    if rel_time:
        now_time = timer()

        if now_time - last_time < 3:
            reload = font2.render('wait, reload...', 1, (150, 0, 0))
            window.blit(reload, (260, 460))
        else:
            num_fire = 0
            rel_time = False



    if num_fire < 5 and rel_time:
        hero.fire()


    sprites_list = sprite.groupcollide(
        ufos, bullets, True, True
    )
    for e in sprites_list:
        counter += 1
        ufo = (Enemy('ufo.png', 10, randint(0, window.get_size()[0]- 100), 50))
        ufos.add(ufo)
    if sprite.spritecollide(hero, asteroid, False):
        break


    if counter >= 50:
        window.blit(font3.render('broooo, eeeee', 1, (255, 255, 255)), (500, 400))
        break
        
        
    if lost >= 100 or sprite.spritecollide(hero, ufos, False):
        window.blit(font4.render('lose, bro...', 1, (255, 255, 255)), (500, 400))
        break

    if counter == sprite.spritecollide(hero, asteroid, False):
        window.blit(font4.render('lose, bro...', 1, (255, 255, 255)), (500, 400))
        break

        

    window.blit(font1.render('Пропущено:' + str(lost), 1, (255, 255, 255)), (0, 0))

    window.blit(font2.render('счет:' + str(counter), 1, (255, 255, 255)), (0, 40))






    display.update()
display.update()
sleep(3)
