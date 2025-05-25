from pygame import *
import random

x2, y2 = (275,370)
x1, y1 = (450,150)

class GameSprite(sprite.Sprite): #Основной класс спрайта
    def __init__(self, player_image, player_x, player_y, player_speed, size_x=65, size_y=65):
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
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x >= 15:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <= 620:
            self.rect.x += self.speed

lost = 0
score = 0
font.init()
font1 = font.Font(None , 36)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 485:
            self.rect.y = 0
            self.rect.x = (random.randint(15, 620))
            self.speed = random.randint(2, 3)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        global score
        self.rect.y -= self.speed

player = Player('am.png', x2, y2, 15)
monsters = sprite.Group()
for i in range(4):
    monsters.add(Enemy('kripochek.png', random.randint(0,600), random.randint(-150, 0), random.randint(3, 5)))
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1):
    asteroids.add(Enemy('asteroid.png', random.randint(0,600), random.randint(-150, 0), 3, 80, 80))

window = display.set_mode((700, 500))
display.set_caption('qeqoqeq')
background = transform.scale(image.load('map.png'), (700, 500))
blink = transform.scale(image.load('blink.png'), (50, 50))

cooldown = 0
timeout = 0

mixer.init()
mixer.music.load('dotamusic.mp3')
mixer.music.play()

finish = False
run = True
clock = time.Clock()
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
    
    if finish == False: 
        window.blit(background,(0,0))

        player.reset()
        player.update()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        asteroids.update()
        monsters.update()
        bullets.update()
        text_blink = font1.render(
            str(cooldown), 1 ,(127,255,0)
        )
        text_lose = font1.render('Пропущено:'+str(lost), 1, (255,255,225))
        text_score = font1.render('Счёт:'+str(score), 1,(255,255,255))

        if key.get_pressed()[K_SPACE] and timeout > 8:
            bullets.add(Bullet('midas.png', player.rect.centerx, player.rect.top - 30, 5, 30, 30))
            timeout = 0
        if sprite.spritecollide(player, monsters, False) or lost >= 3:
            text_lose1 = font1.render('купи радик и по новой', 1, (255,255,255))
            window.blit(text_lose1, (200, 200))
            finish = True
        collides = sprite.groupcollide(monsters, bullets, True, True)

        if sprite.spritecollide(player, asteroids, False):
            text_lose1 = font1.render('купи радик и по новой', 1, (255,255,255))
            window.blit(text_lose1, (200, 200))
            finish = True
        for c in collides:
            score += 1
            monsters.add(Enemy('kripochek.png', random.randint(0,600), random.randint(-150, 0), random.randint(3, 4)))

        if score == 20:
            text_win = font1.render('красавчик', 1, (255,255,255))
            window.blit(text_win, (200, 200))
            finish = True
        timeout += 1
            
        window.blit(text_lose,(20, 20))
        window.blit(text_score,(20, 45))
        window.blit(blink,(20,80))
        window.blit(text_blink,(30, 95))
        display.update()
        clock.tick(60)
cooldown